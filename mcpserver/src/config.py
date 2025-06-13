import os
from typing import Optional

class Config:
    """Configuration class that validates and provides access to environment variables."""
    
    def __init__(self):
        self.validate_environment()
    
    def validate_environment(self):
        """Validates that all required environment variables are present."""
        required_vars = [
            'AZURE_SQL_SERVER',
            'AZURE_SQL_DATABASE',
            'AZURE_SQL_USERNAME',
            'AZURE_SQL_PASSWORD'
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
    def azure_sql_server(self) -> str:
        return os.getenv('AZURE_SQL_SERVER')
    
    @property
    def azure_sql_database(self) -> str:
        return os.getenv('AZURE_SQL_DATABASE')
    
    @property
    def azure_sql_username(self) -> str:
        return os.getenv('AZURE_SQL_USERNAME')
    
    @property
    def azure_sql_password(self) -> str:
        return os.getenv('AZURE_SQL_PASSWORD')
    
    @property
    def sql_connection_string(self) -> str:
        """Builds the SQL Server connection string from individual components."""
        return (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={self.azure_sql_server};"
            f"Database={self.azure_sql_database};"
            f"Uid={self.azure_sql_username};"
            f"Pwd={self.azure_sql_password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )
    
    def log_config_status(self):
        """Logs the configuration status (without sensitive data)."""
        print("✅ Environment configuration loaded successfully:")
        print(f"   Azure SQL Server: {self.azure_sql_server}")
        print(f"   Azure SQL Database: {self.azure_sql_database}")
        print(f"   Azure SQL Username: {self.azure_sql_username}")
        print("   🔒 Sensitive credentials loaded but not displayed")

# Create a global config instance
config = Config() 