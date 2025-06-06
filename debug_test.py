import requests
import json
import time

BASE_URL = 'http://localhost:4000'

def test_endpoint(endpoint, method='GET', data=None):
    """Test a specific endpoint and return the response"""
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == 'POST':
            response = requests.post(f"{BASE_URL}{endpoint}", 
                                   headers={'Content-Type': 'application/json'},
                                   data=json.dumps(data) if data else None)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"❌ {method} {endpoint}: {e}")
        return None

def test_conversation_workflow():
    """Test the complete conversation workflow with various query types"""
    
    print("🧪 Testing Complete Conversation Workflow")
    print("=" * 50)
    
    # Test 1: Basic connection
    print("\n1️⃣ Testing basic connectivity...")
    health = test_endpoint('/test')
    if not health:
        print("❌ Backend not responding")
        return
    
    # Test 2: Create conversation
    print("\n2️⃣ Creating conversation...")
    conv_data = test_endpoint('/conversation', 'POST')
    if not conv_data:
        print("❌ Failed to create conversation")
        return
    
    conversation_id = conv_data['conversation']['conversation_id']
    print(f"✅ Conversation ID: {conversation_id}")
    
    # Test 3: Simple queries that should work
    test_queries = [
        "How many tables are in the database?",
        "What tables are available?",
        "Show me the Customer table structure",
        "How many customers do we have?",
        "What is the latest order?",
        "Show me product categories"
    ]
    
    for i, query in enumerate(test_queries, 3):
        print(f"\n{i}️⃣ Testing query: '{query}'")
        
        response = test_endpoint(f'/conversation/{conversation_id}', 'POST', 
                               {'message': query})
        
        if response and 'conversation' in response:
            messages = response['conversation']['messages']
            last_message = messages[-1] if messages else None
            
            if last_message and last_message.get('role') == 'assistant':
                content = last_message.get('content', '')
                if "couldn't generate a response" in content:
                    print(f"❌ Got default error response: {content}")
                elif len(content) > 20:
                    print(f"✅ Got valid response: {content[:100]}...")
                else:
                    print(f"⚠️  Short response: {content}")
            else:
                print(f"❌ No assistant response found")
        else:
            print(f"❌ Request failed")
        
        # Small delay between requests
        time.sleep(1)
    
    print(f"\n🎯 Testing complete for conversation {conversation_id}")

def test_direct_sql():
    """Test direct SQL queries"""
    print("\n🔍 Testing Direct SQL Queries")
    print("=" * 30)
    
    sql_tests = [
        ("SELECT COUNT(*) as table_count FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'", "Table count"),
        ("SELECT TOP 5 * FROM SalesLT.Customer", "Customer data"),
        ("SELECT COUNT(*) as customer_count FROM SalesLT.Customer", "Customer count"),
        ("SELECT TOP 3 Name FROM SalesLT.ProductCategory", "Product categories")
    ]
    
    for query, description in sql_tests:
        print(f"\n🔍 {description}: {query}")
        response = test_endpoint('/sql/query', 'POST', {'query': query, 'params': ()})
        
        if response and 'results' in response:
            results = response['results']
            print(f"✅ Got {len(results)} results")
            if results:
                print(f"📊 Sample: {results[0]}")
        else:
            print(f"❌ Query failed")

if __name__ == '__main__':
    test_direct_sql()
    test_conversation_workflow() 