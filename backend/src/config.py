import os
from typing import Optional

class Config:
    """Configuration class that validates and provides access to environment variables."""
    
    def __init__(self):
        self.validate_environment()
    
    def validate_environment(self):
        """Validates that all required environment variables are present."""
        required_vars = [
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_DEPLOYMENT_NAME',

        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                f"Please check your .env file and ensure all required variables are set."
            )
    
    @property
    def azure_openai_endpoint(self) -> str:
        return os.getenv('AZURE_OPENAI_ENDPOINT')
    
    @property
    def azure_openai_api_key(self) -> str:
        return os.getenv('AZURE_OPENAI_API_KEY')
    
    @property
    def azure_openai_deployment_name(self) -> str:
        return os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
    
    @property
    def azure_openai_api_version(self) -> str:
        return os.getenv('AZURE_OPENAI_API_VERSION', 'preview')
    

    
    def log_config_status(self):
        """Logs the configuration status (without sensitive data)."""
        print("✅ Environment configuration loaded successfully:")
        print(f"   Azure OpenAI Endpoint: {self.azure_openai_endpoint}")
        print(f"   Azure OpenAI Deployment: {self.azure_openai_deployment_name}")
        print(f"   Azure OpenAI API Version: {self.azure_openai_api_version}")
        print("   🔒 Sensitive credentials loaded but not displayed")

# Create a global config instance
config = Config() 