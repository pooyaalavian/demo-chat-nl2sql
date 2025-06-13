import requests
import json

def init():
    endpoint = 'http://localhost:4000/conversation'
    response = requests.post(endpoint)
    conversation_id = response.json()['conversation']['conversation_id']
    return conversation_id


def send_msg(conversation_id, message):
    endpoint = f'http://localhost:4000/conversation/{conversation_id}'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'message': message})
    response = requests.post(endpoint, headers=headers, data=data)
    payload = response.json()
    if 'error' in payload:
        raise Exception(f"Error: {payload['error']}")
    messages = payload['conversation']['messages']
    print('----------------')
    for msg in messages:
        if msg['role'] == 'assistant':
            print(f"Assistant: {msg['content']}")
        elif msg['role'] == 'user':
            print(f"User: {msg['content']}")
    print('----------------')
    return response.json()


def test_conversation():
        conversation_id = init()  # Create a new conversation
        print(f'Conversation ID: {conversation_id}')

        # Test with a simple question first
        send_msg(conversation_id, 'How many tables are in the database?')
        
        # Test with a more complex query
        # send_msg(conversation_id, 'What tables are available? List their names.')

def test_sql():
    """Test direct SQL connectivity"""
    endpoint = 'http://localhost:4000/sql/query'
    headers = {'Content-Type': 'application/json'}
    
    # Test with a simple system query that should work on any SQL Server
    data = json.dumps({
        'query': 'SELECT @@VERSION as sql_version',
        'params': ()
    })
    response = requests.post(endpoint, headers=headers, data=data)
    
    print("🔍 Testing SQL Connectivity:")
    if response.status_code == 200:
        results = response.json()['results']
        print('✅ SQL Connection successful!')
        for row in results:
            print(f"SQL Server Version: {row}")
    else:
        print(f"❌ SQL Connection failed: {response.json().get('error', 'Unknown error')}")
    
    # Test table query
    data = json.dumps({
        'query': 'SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\'',
        'params': ()
    })
    response = requests.post(endpoint, headers=headers, data=data)
    
    if response.status_code == 200:
        results = response.json()['results']
        print(f"📊 Number of tables in database: {results[0]['table_count'] if results else 0}")
    else:
        print(f"❌ Table count query failed: {response.json().get('error', 'Unknown error')}")

if __name__ == '__main__':
    # test_sql()  # Test SQL connectivity first
    print('test started')
    test_conversation()  # Then test conversation