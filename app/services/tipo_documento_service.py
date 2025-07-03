from app.database import get_db_connection
from .catequizando_service import _get_next_id

def crear_tipo_documento(tipo, descripcion):
    db = get_db_connection()
    nuevo_tipo = {
        "_id": _get_next_id('tipo_documentos'),
        "tipo": tipo,
        "descripcion": descripcion
    }
    db.tipo_documentos.insert_one(nuevo_tipo)
    return nuevo_tipo['_id']

def obtener_tipos_documento():
    db = get_db_connection()
    return list(db.tipo_documentos.find().sort("_id", 1))

def obtener_tipo_documento_por_id(id_tipo):
    db = get_db_connection()
    return db.tipo_documentos.find_one({"_id": int(id_tipo)})

def actualizar_tipo_documento(id_tipo, tipo, descripcion):
    db = get_db_connection()
    update_data = {"$set": {"tipo": tipo, "descripcion": descripcion}}
    db.tipo_documentos.update_one({"_id": int(id_tipo)}, update_data)

def eliminar_tipo_documento(id_tipo):
    db = get_db_connection()
    db.tipo_documentos.delete_one({"_id": int(id_tipo)})