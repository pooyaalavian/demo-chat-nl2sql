import os 
from openai import AzureOpenAI
from src.sqlutil import run_sql_query, get_db_tables, get_db_columns_and_types
import json 

SYSTEM_MESSAGE = {
    'role': 'system',
    'content': '''You are a helpful assistant.
You help users who are in our sales department with their questions. You have access to a SQL database that contains information about our products, customers, and sales.
You can execute multiple queries in order to generate an answer.
Always check the table names and column names before executing a query.
You can answer questions about our products, customers, and sales.
'''
}

endpoint = os.getenv("OPENAI_ENDPOINT_URL")
deployment = os.getenv("OPENAI_DEPLOYMENT_NAME")
subscription_key = os.getenv("OPENAI_API_KEY")

# Initialize Azure OpenAI client with key-based authentication
oai_client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2025-03-01-preview",
)


class Conversation:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.messages = [SYSTEM_MESSAGE]
        self.tools = [
            {
                'executor': run_sql_query,
                'definition': {
                    'type': 'function',
                    'name': 'run_sql_query',
                    'description': 'Run a SQL query against the database.',
                    'strict': True,
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'query': {
                                'type': 'string',
                                'description': 'The SQL query to execute.'
                            },
                            'params': {
                                'type': 'array',
                                'items': {
                                    'type': 'string'
                                },
                                'description': 'Optional parameters for the SQL query.'
                            }
                        },
                        'required': ['query','params'],
                        'additionalProperties': False
                    }
                }
            },
            {
                'executor': get_db_tables,
                'definition': {
                    'type': 'function',
                    'name': 'get_db_tables',
                    'description': 'Lists all tables in the database',
                    'strict': True,
                    'parameters': {
                        'type': 'object',
                        'properties': {},
                        'required': [],
                        'additionalProperties': False
                    }
                }
            },
            {
                'executor': get_db_columns_and_types,
                'definition': {
                    'type': 'function',
                    'name': 'get_db_columns_and_types',
                    'description': 'Lists all columns in a table and their types.',
                    'strict': True,
                    'parameters': {
                        'type': 'object',
                        'properties': {
                            'schema_name': {
                                'type': 'string',
                                'description': 'The Stable name to look up.'
                            },
                            'table_name': {
                                'type': 'string',
                                'description': 'The Stable name to look up.'
                            }
                        },
                        'required': ['schema_name','table_name'],
                        'additionalProperties': False
                    }
                }
            }
        ]
    
    def get_tools(self):
        tool_definitions = []
        for tool in self.tools:
            tool_definitions.append(tool['definition'])
        return tool_definitions

    def get_messages(self):
        messages = []
        for message in self.messages:
            try:
                if message['role'] in ['user', 'assistant']:
                    messages.append(message)
            except:
                pass 
        return messages

    def to_dict(self):
        return {
            'conversation_id': self.conversation_id,
            'messages': self.get_messages(),
        }
    
    def execute_function(self, name, args):
        for tool in self.tools:
            if tool['definition']['name'] == name:
                fn = tool['executor']
                results = fn(**args)
                return str(results)
        raise ValueError(f"Function {name} not found")
    
    def add_message(self, message):
        msg = {
            'role': 'user',
            'content': message
        }
        self.messages.append(msg)
        
        finished = False
        
        while not finished:
            finished = True
            tools = self.get_tools()
            response = oai_client.responses.create(
                input=self.messages,
                model=deployment,
                # max_output_tokens=1000,
                temperature=0.7,
                stream=False,
                tools=tools,
            )
            for item in response.output:
                if item.type == 'function_call': 
                    finished = False
                    call_id = item.call_id
                    function_name = item.name
                    args = json.loads(item.arguments)
                    function_result = self.execute_function(function_name, args)
                    
                    self.messages.append(item)
                    self.messages.append({
                        'type': 'function_call_output',
                        'call_id': call_id,
                        'output': function_result,
                    })
                    
        
        response_message = response.output_text
        response_dict = {
            'role': 'assistant',
            'content': response_message
        }
        self.messages.append(response_dict)
        return
        