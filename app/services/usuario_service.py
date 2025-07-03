from app.database import get_db_connection
from extensions import bcrypt 
import datetime
from .catequizando_service import _get_next_id

def crear_usuario_service(nombre, contrasena_plana, rol):
    db = get_db_connection()
    
    if db.usuarios.find_one({"nombre": nombre}):
        return None

    contrasena_hash = bcrypt.generate_password_hash(contrasena_plana).decode('utf-8')
    
    nuevo_usuario = {
        "_id": _get_next_id('usuarios'), 
        "nombre": nombre,
        "contrasena": contrasena_hash,
        "rol": rol,
        "notificaciones": [] 
    }
    
    resultado = db.usuarios.insert_one(nuevo_usuario)
    return resultado.inserted_id

def obtener_usuarios_service():
    db = get_db_connection()
    return list(db.usuarios.find({}, {"contrasena": 0}))

def obtener_usuario_por_id_service(id_usuario):
    db = get_db_connection()
    try:
        return db.usuarios.find_one({"_id": int(id_usuario)}, {"contrasena": 0})
    except (ValueError, TypeError):
        return None

def actualizar_usuario(id_usuario, nombre, rol, nueva_contrasena=None):
    db = get_db_connection()
    try:
        id_num = int(id_usuario)
    except (ValueError, TypeError):
        return False
    
    update_data = {
        "$set": {
            "nombre": nombre,
            "rol": rol
        }
    }
    
    if nueva_contrasena:
        contrasena_hash = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
        update_data["$set"]["contrasena"] = contrasena_hash
        
    resultado = db.usuarios.update_one({"_id": id_num}, update_data)
    return resultado.modified_count > 0

def eliminar_usuario(id_usuario):
    db = get_db_connection()
    try:
        resultado = db.usuarios.delete_one({"_id": int(id_usuario)})
        return resultado.deleted_count > 0
    except (ValueError, TypeError):
        return 0


