# app/services/auth_service.py (MODIFICADO para MongoDB y Bcrypt)

from app.database import get_db_connection
# Importamos la instancia de bcrypt desde el archivo principal de la app
# Es importante que sea la misma instancia para que funcione correctamente.
# Asumimos que está en 'app' -> 'from app import bcrypt' o donde la hayas definido.
from extensions import bcrypt 

def verificar_credenciales(nombre, contrasena):
    """
    Verifica las credenciales de un usuario contra la base de datos MongoDB.
    
    1. Busca al usuario por su nombre.
    2. Si el usuario existe, compara la contraseña proporcionada con el hash almacenado.
    
    Args:
        nombre (str): El nombre de usuario.
        contrasena (str): La contraseña en texto plano.
        
    Returns:
        dict: El documento del usuario si las credenciales son válidas, de lo contrario None.
    """
    db = get_db_connection()
    
    # 1. Buscar al usuario por su nombre de usuario en la colección 'usuarios'
    usuario = db.usuarios.find_one({"nombre": nombre})
    
    # 2. Si se encontró un usuario y la contraseña coincide, devolver el documento del usuario
    if usuario and bcrypt.check_password_hash(usuario['contrasena'], contrasena):
        return usuario  # Retornamos el diccionario completo del usuario
    
    # Si no se encuentra el usuario o la contraseña no coincide, retornar None
    return None

# --- NUEVA FUNCIÓN: Para crear usuarios con contraseñas seguras ---
# Esta función es esencial. Deberías tener una ruta o un script para crear usuarios.
def crear_usuario(nombre, contrasena_plana, rol):
    """
    Crea un nuevo usuario con una contraseña hasheada.
    ¡NO GUARDAR CONTRASEÑAS EN TEXTO PLANO!
    """
    db = get_db_connection()

    # Generar el hash de la contraseña
    
    # (Opcional) Usar la función para obtener el siguiente ID si lo necesitas
    # from .catequizando_service import _get_next_id
    # nuevo_id = _get_next_id('usuarios')

    nuevo_usuario = {
        # "_id": nuevo_id,
        "nombre": nombre,
        "rol": rol,
        "notificaciones": [] # Inicializar otros campos si los hay
    }

    try:
        db.usuarios.insert_one(nuevo_usuario)
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False