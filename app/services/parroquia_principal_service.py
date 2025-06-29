from app.database import get_connection

def obtener_parroquias():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerPARROQUIA_PRINCIPAL")
        return cursor.fetchall()

def crear_parroquia(nombre, direccion, ciudad, telefono, correo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearPARROQUIA_PRINCIPAL ?, ?, ?, ?, ?",
                       (nombre, direccion, ciudad, telefono or None, correo or None))
        cursor.connection.commit()

def actualizar_parroquia(id, nombre, direccion, ciudad, telefono, correo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarPARROQUIA_PRINCIPAL ?, ?, ?, ?, ?, ?",
                       (id, nombre, direccion, ciudad, telefono or None, correo or None))
        cursor.connection.commit()

def eliminar_parroquia(id):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarPARROQUIA_PRINCIPAL ?", id)
        cursor.connection.commit()
