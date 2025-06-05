import pyodbc
from typing import Any, List, Dict
import os 
connection_string = os.getenv("SQL_SERVER_CONN_STR")

def run_sql_query( query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Executes a SQL query against a Microsoft SQL Server and returns the results as a list of dictionaries.
    Args:
        connection_string (str): The ODBC connection string for SQL Server.
        query (str): The SQL query to execute.
        params (tuple): Optional query parameters.
    Returns:
        List[Dict[str, Any]]: Query results as a list of dictionaries.
    Raises:
        Exception: If the query fails.
    """
    try:
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                columns = [column[0] for column in cursor.description] if cursor.description else []
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return results
    except Exception as e:
        return f"SQL query failed: {e}"

def get_db_tables() -> List[str]:
    """
    Retrieves a list of all table names in the database.
    Returns:
        List[str]: A list of table names.
    """
    query = "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    results = run_sql_query(query)
    return [f"[{row['TABLE_SCHEMA']}].[{row['TABLE_NAME']}]" for row in results] if results else []

def get_db_columns_and_types(schema_name:str, table_name: str) -> List[str]:
    """
    Retrieves a list of column names and their data types for a given table.
    Args:
        table_name (str): The name of the table to inspect.
    Returns:
        List[str]: A list of strings in the format "column_name: data_type".
    """
    query = f"""
    SELECT COLUMN_NAME, DATA_TYPE 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE 
    TABLE_SCHEMA = ?
    AND TABLE_NAME = ? 
    """
    results = run_sql_query(query, (schema_name, table_name))
    return [f"{row['COLUMN_NAME']}: {row['DATA_TYPE']}" for row in results] if results else []