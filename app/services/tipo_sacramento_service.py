from app.database import get_db_connection
from .catequizando_service import _get_next_id

def crear_tipo_sacramento(nombre):
    db = get_db_connection()
    
    nuevo_tipo_sacramento = {
        "_id": _get_next_id('tipo_sacramentos'),
        "nombre": nombre
    }
    
    try:
        resultado = db.tipo_sacramentos.insert_one(nuevo_tipo_sacramento)
        return resultado.inserted_id
    except Exception as e:
        print(f"Error al crear tipo de sacramento: {e}")
        return None
    
def obtener_tipos_sacramento():
    db = get_db_connection()
    return list(db.tipo_sacramentos.find().sort("_id", 1))

def obtener_tipo_sacramento_por_id(id_tipo_sacramento):
    db = get_db_connection()
    try:
        return db.tipo_sacramentos.find_one({"_id": int(id_tipo_sacramento)})
    except (ValueError, TypeError):
        return None
    
def actualizar_tipo_sacramento(id_tipo_sacramento, nombre):
    db = get_db_connection()
    try:
        id_num = int(id_tipo_sacramento)
    except (ValueError, TypeError):
        return False
        
    update_data = {
        "$set": {
            "nombre": nombre
        }
    }
    
    resultado = db.tipo_sacramentos.update_one({"_id": id_num}, update_data)
    return resultado.modified_count > 0

def eliminar_tipo_sacramento(id_tipo_sacramento):
    db = get_db_connection()
    try:
        resultado = db.tipo_sacramentos.delete_one({"_id": int(id_tipo_sacramento)})
        return resultado.deleted_count > 0
    except (ValueError, TypeError):
        return False