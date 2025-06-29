from pymongo import MongoClient
import json
import os

_db_instance=None

def get_db_connection():
    global _db_instance
    
    if _db_instance is not None:
        return _db_instance
    try:
        config_path= os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.json')
        with open(config_path) as config_file:
            config=json.load(config_file)['mongodb']
            uri_template = config['uri_template']
            db_name = config['database']
            username = config['username']
            password = config['password']
            uri = uri_template.format(
            username=username,
            password=password,
            database=db_name
        )
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            _db_instance = client[db_name]
        return _db_instance
    except Exception as e:
        print(f"Ocurrió un error inesperado al conectar a la base de datos: {e}")
        return None
    db = get_db_connection()