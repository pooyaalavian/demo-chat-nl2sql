import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables
load_dotenv()

def test_responses_api():
    """Test the Azure OpenAI Responses API configuration"""
    
    # Get environment variables
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    print("🧪 Testing Azure OpenAI Responses API Configuration")
    print("=" * 50)
    print(f"Endpoint: {endpoint}")
    print(f"Deployment: {deployment_name}")
    print(f"API Key: {'✅ Present' if api_key else '❌ Missing'}")
    print()
    
    if not all([endpoint, api_key, deployment_name]):
        print("❌ Missing required environment variables!")
        return False
    
    try:
        # Initialize client for Responses API
        client = AzureOpenAI(
            base_url=f"{endpoint.rstrip('/')}/openai/v1/",
            api_key=api_key,
            api_version="preview"
        )
        
        print("🔄 Testing simple Responses API call...")
        
        # Test simple response
        response = client.responses.create(
            model=deployment_name,
            input="Hello! This is a test of the Responses API.",
            temperature=0.7
        )
        
        print("✅ Responses API call successful!")
        print(f"Response ID: {response.id}")
        print(f"Model: {response.model}")
        print(f"Status: {response.status}")
        
        # Extract response text
        if hasattr(response, 'output_text') and response.output_text:
            response_text = response.output_text
        else:
            response_text = ""
            for item in response.output:
                if item.type == 'message' and hasattr(item, 'content'):
                    for content in item.content:
                        if hasattr(content, 'type') and content.type == 'output_text':
                            response_text = content.text
                            break
                if response_text:
                    break
        
        print(f"Response: {response_text}")
        print()
        
        # Test with function calling
        print("🔄 Testing function calling...")
        
        response_with_tools = client.responses.create(
            model=deployment_name,
            input="What tables are available in the database?",
            temperature=0.7,
            tools=[
                {
                    "type": "function",
                    "name": "get_db_tables",
                    "description": "Lists all tables in the database",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                        "additionalProperties": False
                    }
                }
            ]
        )
        
        print("✅ Function calling test successful!")
        print(f"Response ID: {response_with_tools.id}")
        
        # Check if function was called
        function_called = False
        for item in response_with_tools.output:
            if item.type == 'function_call':
                function_called = True
                print(f"Function called: {item.name}")
        
        if not function_called:
            print("ℹ️  No function was called (this is normal for a simple test)")
        
        print()
        print("🎉 All tests passed! Your Responses API configuration is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Responses API: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check your .env file has all required variables")
        print("2. Verify your Azure OpenAI deployment name is correct")
        print("3. Ensure your endpoint URL is correct")
        print("4. Check that your API key is valid")
        return False

if __name__ == "__main__":
    test_responses_api() 