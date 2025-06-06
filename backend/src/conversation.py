from openai import AzureOpenAI
from src.sqlutil import run_sql_query, get_db_tables, get_db_columns_and_types
from src.config import config
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

# Initialize Azure OpenAI client for Responses API
oai_client = AzureOpenAI(
    base_url=f"{config.azure_openai_endpoint.rstrip('/')}/openai/v1/",
    api_key=config.azure_openai_api_key,
    api_version="preview"  # Use "preview" for the new v1 Responses API
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
                                'description': 'The schema name to look up.'
                            },
                            'table_name': {
                                'type': 'string',
                                'description': 'The table name to look up.'
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
                if isinstance(message, dict) and message.get('role') in ['user', 'assistant']:
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
        try:
            for tool in self.tools:
                if tool['definition']['name'] == name:
                    fn = tool['executor']
                    results = fn(**args)
                    return str(results)
            raise ValueError(f"Function {name} not found")
        except Exception as e:
            error_msg = f"Error executing function {name}: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def add_message(self, message):
        print(f"🔄 Starting add_message with: '{message}'")
        
        msg = {
            'role': 'user',
            'content': message
        }
        self.messages.append(msg)
        print(f"📝 Added user message, total messages: {len(self.messages)}")
        
        try:
            # Convert messages to simple format for Responses API
            input_messages = []
            supported_roles = ['user', 'assistant', 'system']

            for msg in self.messages:
                # todo: update to include all roles in self.messages
                if isinstance(msg, dict) and msg.get('role'):
                    role = msg.get('role')
                    if role in supported_roles:
                        input_messages.append({
                            'role': role,
                            'content': msg['content']
                        })
                    else:
                        # Log unsupported message types for debugging
                        print(f"🔍 Skipping message with unsupported role: {role}")
                        print(f"🔍 Message content preview: {str(msg)[:100]}...")

            print(f"🔄 Prepared {len(input_messages)} messages for API call")
            
            # Get tools in the format expected by Responses API
            tools = self.get_tools()
            print(f"🔧 Using {len(tools)} tools")
            
            # Make the API call to Responses API
            print(f"🚀 Making Responses API call...")
            response = oai_client.responses.create(
                input=input_messages,
                model=config.azure_openai_deployment_name,
                temperature=0.7,
                tools=tools,
            )
            print(f"✅ Responses API call completed, status: {response.status}")
            
            # Handle function calls - loop until we get a text response
            max_iterations = 5  # Prevent infinite loops
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                print(f"🔄 Function call iteration {iteration}")
                
                function_calls_to_process = []
                
                for item in response.output:
                    if hasattr(item, 'type') and item.type == 'function_call':
                        function_calls_to_process.append(item)
                
                print(f"🔧 Found {len(function_calls_to_process)} function calls to process")
                
                # If no function calls, break the loop
                if not function_calls_to_process:
                    break
                
                # Process function calls and create follow-up responses
                function_inputs = []
                
                for item in function_calls_to_process:
                    try:
                        call_id = getattr(item, 'call_id', None)
                        function_name = getattr(item, 'name', None)
                        arguments = getattr(item, 'arguments', None)
                        
                        print(f"🔧 Processing function: {function_name}")
                        
                        # Handle arguments - they might be a string or already parsed
                        if isinstance(arguments, str):
                            try:
                                args = json.loads(arguments)
                            except json.JSONDecodeError:
                                print(f"⚠️  Failed to parse arguments as JSON: {arguments}")
                                args = {}
                        elif isinstance(arguments, dict):
                            args = arguments
                        else:
                            print(f"⚠️  Unexpected arguments type: {type(arguments)}")
                            args = {}
                        
                        # Execute the function
                        function_result = self.execute_function(function_name, args)
                        print(f"✅ Function {function_name} result: {function_result[:100]}...")
                        
                        function_inputs.append({
                            'type': 'function_call_output',
                            'call_id': call_id,
                            'output': function_result,
                        })
                        
                    except Exception as func_error:
                        print(f"❌ Error processing function call: {func_error}")
                        function_inputs.append({
                            'type': 'function_call_output',
                            'call_id': getattr(item, 'call_id', 'unknown'),
                            'output': f"Error: {str(func_error)}",
                        })
                
                # Create follow-up response with function results
                print(f"🔄 Making follow-up API call with function results...")
                response = oai_client.responses.create(
                    model=config.azure_openai_deployment_name,
                    previous_response_id=response.id,
                    input=function_inputs,
                    temperature=0.7,
                    tools=tools,
                )
                print(f"✅ Follow-up API call completed")
                
                # Check if we got a final text response
                if hasattr(response, 'output_text') and response.output_text:
                    print(f"✅ Got final response with output_text")
                    break
                
                # Check for message items
                has_message = any(hasattr(item, 'type') and item.type == 'message' for item in response.output)
                if has_message:
                    print(f"✅ Got final response with message items")
                    break
                
                print(f"🔄 No final response yet, continuing to iteration {iteration + 1}")
            
            if iteration >= max_iterations:
                print(f"⚠️  Reached maximum iterations ({max_iterations}), stopping")
            
            # Extract the final response text
            response_message = ""
            
            # Try to get output_text first
            if hasattr(response, 'output_text') and response.output_text:
                response_message = response.output_text
                print(f"✅ Got response from output_text: {response_message[:100]}...")
            else:
                # Fallback to extract text from output array
                print(f"🔍 Extracting from output array with {len(response.output)} items")
                
                for i, item in enumerate(response.output):
                    if hasattr(item, 'type') and item.type == 'message':
                        if hasattr(item, 'content'):
                            for j, content in enumerate(item.content):
                                if hasattr(content, 'type') and content.type == 'output_text':
                                    response_message = getattr(content, 'text', '')
                                    print(f"✅ Got response from content: {response_message[:100]}...")
                                    break
                        if response_message:
                            break
                    else:
                        print(f"🔍 Debug: Item {i} is not a message, it's: {getattr(item, 'type', 'unknown')}")
            
            if not response_message:
                print(f"⚠️  No response text found, using default message")
                response_message = "I'm sorry, I couldn't generate a response."
            
            response_dict = {
                'role': 'assistant',
                'content': response_message
            }
            self.messages.append(response_dict)
            print(f"✅ Added assistant response, total messages: {len(self.messages)}")
            
        except Exception as e:
            print(f"❌ Error in add_message: {e}")
            import traceback
            print(f"🔍 Full traceback: {traceback.format_exc()}")
            error_response = {
                'role': 'assistant',
                'content': f"I'm sorry, there was an error processing your request: {str(e)}"
            }
            self.messages.append(error_response)
        
        print(f"🏁 Finished add_message processing")
        return
        