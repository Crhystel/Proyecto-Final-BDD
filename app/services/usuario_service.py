from app.database import get_connection

def obtener_usuarios():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerUSUARIO")
        return cursor.fetchall()

def crear_usuario(contrasena, nombre, rol):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearUSUARIO ?, ?, ?", (contrasena, nombre, rol))
        cursor.connection.commit()

def actualizar_usuario(id, contrasena, nombre, rol):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarUSUARIO ?, ?, ?, ?", (id, contrasena, nombre, rol))
        cursor.connection.commit()

def eliminar_usuario(id):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarUSUARIO ?", id)
        cursor.connection.commit()

def obtener_usuario_por_id(id):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM USUARIO WHERE id_usuario = ?", id)
        return cursor.fetchone()
