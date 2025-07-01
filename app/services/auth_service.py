from app.database import get_db_connection
from extensions import bcrypt 

def verificar_credenciales(nombre, contrasena):
    db = get_db_connection()
    
    usuario = db.usuarios.find_one({"nombre": nombre})
    
    if usuario and bcrypt.check_password_hash(usuario['contrasena'], contrasena):
        return usuario 
    return None

def crear_usuario(nombre, contrasena_plana, rol):
    db = get_db_connection()


    nuevo_usuario = {
        "nombre": nombre,
        "rol": rol,
        "notificaciones": [] 
    }

    try:
        db.usuarios.insert_one(nuevo_usuario)
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False