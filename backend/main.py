from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, request
from flask_cors import CORS
from uuid import uuid4
from src.conversation import Conversation
from src.config import config
from typing import Dict

app = Flask(__name__)
CORS(app)

# todo: Use a database or persistent storage for conversations like Azure CosmosDB
conversations: Dict[str, Conversation] = {}

@app.route('/test', methods=['GET'])
def test_endpoint():
    return jsonify({'message': 'Test endpoint is working!'}), 200

@app.route('/conversation', methods=['POST'])
def create_conversation():
    conversation_id = str(uuid4())
    conversations[conversation_id] = Conversation(conversation_id)
    conversation = conversations[conversation_id]
    return jsonify({'conversation':conversation.to_dict()}), 200

@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    if conversation_id in conversations:
        return jsonify({'conversation':conversations[conversation_id].to_dict()}), 200
    else:
        return jsonify({'error': 'Conversation not found'}), 404

@app.route('/conversation/<conversation_id>', methods=['POST'])
def add_message_to_conversation(conversation_id):
    if conversation_id not in conversations:
        return jsonify({'error': 'Conversation not found'}), 404

    try:
        conversation = conversations[conversation_id]
        # get message from request body
        message = request.json.get('message')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        print(f"📝 Processing message: '{message}' for conversation {conversation_id}")
        
        # Add message and process response
        conversation.add_message(message)
        
        # Get the updated conversation
        updated_conversation = conversation.to_dict()
        
        print(f"✅ Message processed successfully. Conversation now has {len(updated_conversation['messages'])} messages")
        
        return jsonify({'message': 'Message added successfully', 'conversation': updated_conversation}), 200
        
    except Exception as e:
        print(f"❌ Error in add_message_to_conversation: {e}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/sql/query', methods=['POST'])
def run_query():
    from src.sqlutil import run_sql_query
    query = request.json.get('query')
    params = request.json.get('params', ())
    
    try:
        results = run_sql_query(query, params)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting NL2SQL Chat Backend...")
    config.log_config_status()
    print("🌐 Starting Flask server on port 4000...")
    app.run(debug=True, port=4000)
