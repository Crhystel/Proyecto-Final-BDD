
from app.database import get_db_connection
from extensions import bcrypt 
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

def crear_usuario_service(nombre, contrasena_plana, rol):
    db = get_db_connection()
    
    # Revisar si el usuario ya existe para evitar duplicados
    if db.usuarios.find_one({"nombre": nombre}):
        return None # Indica que el usuario ya existe

    contrasena_hash = bcrypt.generate_password_hash(contrasena_plana).decode('utf-8')
    
    nuevo_usuario = {
        # "_id": _get_next_id('usuarios'), # Descomentar si usas IDs numéricos
        "nombre": nombre,
        "contrasena": contrasena_hash,
        "rol": rol,
        "notificaciones": []
    }
    
    resultado = db.usuarios.insert_one(nuevo_usuario)
    return resultado.inserted_id

def obtener_usuarios_service():
    db = get_db_connection()
    # Usamos proyección para no enviar nunca el hash de la contraseña al cliente
    return list(db.usuarios.find({}, {"contrasena": 0}))

def obtener_usuario_por_id_service(id_usuario):
    db = get_db_connection()
    
    oid = ObjectId(id_usuario)
    return db.usuarios.find_one({"_id": oid}, {"contrasena": 0})
  

def actualizar_usuario_service(id_usuario, nombre, rol, nueva_contrasena=None):
  
    db = get_db_connection()
    oid = ObjectId(id_usuario)
    
    update_data = {
        "$set": {
            "nombre": nombre,
            "rol": rol
        }
    }
    
    # Si se proporcionó una nueva contraseña, la hasheamos y la añadimos al update
    if nueva_contrasena:
        contrasena_hash = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')
        update_data["$set"]["contrasena"] = contrasena_hash
        
    resultado = db.usuarios.update_one({"_id": oid}, update_data)
    return resultado.modified_count > 0

def eliminar_usuario_service(id_usuario):
    
    db = get_db_connection()
    oid = ObjectId(id_usuario)
    resultado = db.usuarios.delete_one({"_id": oid})
    return resultado.deleted_count > 0