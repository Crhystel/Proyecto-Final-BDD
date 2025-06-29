from app.database import get_connection

def verificar_credenciales(nombre, contrasena):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM USUARIO WHERE nombre = ? AND contrasena = ?", (nombre, contrasena))
        return cursor.fetchone()
