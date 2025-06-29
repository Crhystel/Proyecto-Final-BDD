import json
import pyodbc

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

def get_connection():
    connection_string = (
        f"DRIVER={{{config['controlador_odbc']}}};"
        f"SERVER={config['name_server']};"
        f"DATABASE={config['database']};"
        f"UID={config['username']};"
        f"PWD={config['password']}"
    )
    return pyodbc.connect(connection_string)
