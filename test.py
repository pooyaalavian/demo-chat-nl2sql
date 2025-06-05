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
        # conversation_id = init()
        conversation_id = '4976d0a5-941d-4a73-a748-1c174c6bca72'
        print(f'Conversation ID: {conversation_id}')

        # send_msg(conversation_id, 'How many customers do we have? Use `[SalesLT].[Customer]` table.')
        send_msg(conversation_id, 'Yes, please break it down by the sales person.')
        # print(f'Response: {response}')

        # response= send_msg(conversation_id, 'What is my name?')

def test_sql():
    endpoint = 'http://localhost:4000/sql/query'
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({
        'query': 'SELECT TOP 10 * FROM sys.objects',
        'params': ()
    })
    response = requests.post(endpoint, headers=headers, data=data)
    
    if response.status_code == 200:
        results = response.json()['results']
        print('SQL Query Results:')
        for row in results:
            print(row)
    else:
        print(f"Error: {response.json().get('error', 'Unknown error')}")

if __name__ == '__main__':
    test_conversation()
    # test_sql()