from app.database import get_connection

def obtener_parroquias():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerPARROQUIA")
        return cursor.fetchall()

def crear_parroquia(nombre, direccion, ciudad, telefono, correo, id_parroquia_principal):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearPARROQUIA ?, ?, ?, ?, ?, ?",
                       (nombre, direccion, ciudad, telefono, correo, id_parroquia_principal))
        cursor.connection.commit()

def actualizar_parroquia(id_parroquia, nombre, direccion, ciudad, telefono, correo, id_parroquia_principal):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarPARROQUIA ?, ?, ?, ?, ?, ?, ?",
                       (id_parroquia, nombre, direccion, ciudad, telefono, correo, id_parroquia_principal))
        cursor.connection.commit()

def eliminar_parroquia(id_parroquia):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarPARROQUIA ?", id_parroquia)
        cursor.connection.commit()

def obtener_parroquias_principales():
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT id_parroquia_principal, nombre FROM PARROQUIA_PRINCIPAL")
        return cursor.fetchall()
