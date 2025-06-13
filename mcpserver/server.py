from dotenv import load_dotenv
load_dotenv()

from src.config import config
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Sales Data Agent ", "1.0.0")


import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.tool()
def run_sql_query(query: str, params: tuple = ()) -> float:
    """Receives a Microsoft SQL Server-compliant query and parameters and returns the result of the query"""
    from src.sqlutils import run_sql_query
    return run_sql_query(query, params)


@mcp.tool()
async def get_db_tables() -> str:
    """Lists the name of all tables accessible to the user in the database"""
    from src.sqlutils import get_db_tables
    return get_db_tables()

@mcp.tool()
async def get_tables_columns_and_types(schema_name: str, table_name: str) -> str:
    """Lists the columns and their types for a specified table in the database"""
    from src.sqlutils import get_db_columns_and_types
    return get_db_columns_and_types(schema_name, table_name)

if __name__ == "__main__":
    config.log_config_status()
    print("🚀 Starting MCP Server...")
    mcp.run(transport='streamable-http', )
    # mcp.run(transport='stdio', )
    print("🌐 MCP Server is running on http://localhost:8000")