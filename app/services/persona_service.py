from app.database import get_db_connection
from .catequizando_service import _get_next_id

def crear_persona(nombre, apellido, tipo_persona, telefono, correo):
    db = get_db_connection()
    nueva_persona = {
        "_id": _get_next_id('personas'),
        "nombre": nombre,
        "apellido": apellido,
        "tipo_persona": tipo_persona, # P: Padre, M: Madre, D: Padrino, N: Madrina
        "telefono": telefono,
        "correo": correo
    }
    db.personas.insert_one(nueva_persona)
    return nueva_persona['_id']

def obtener_personas():
    db = get_db_connection()
    return list(db.personas.find().sort("apellido", 1))

def obtener_persona_por_id(id_persona):
    db = get_db_connection()
    return db.personas.find_one({"_id": int(id_persona)})

def actualizar_persona(id_persona, nombre, apellido, tipo_persona, telefono, correo):
    db = get_db_connection()
    update_data = {
        "$set": {
            "nombre": nombre, "apellido": apellido, "tipo_persona": tipo_persona,
            "telefono": telefono, "correo": correo
        }
    }
    db.personas.update_one({"_id": int(id_persona)}, update_data)

def eliminar_persona(id_persona):
    db = get_db_connection()
    db.personas.delete_one({"_id": int(id_persona)})