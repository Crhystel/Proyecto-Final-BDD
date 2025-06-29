from app.database import get_connection

def obtener_catequistas():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerCATEQUISTA")
        return cursor.fetchall()

def crear_catequista(telefono, apellido, nombre, correo, rol):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearCATEQUISTA ?, ?, ?, ?, ?", (telefono, apellido, nombre, correo, rol))
        cursor.connection.commit()

def actualizar_catequista(id_catequista, telefono, apellido, nombre, correo, rol):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarCATEQUISTA ?, ?, ?, ?, ?, ?", (id_catequista, telefono, apellido, nombre, correo, rol))
        cursor.connection.commit()

def eliminar_catequista(id_catequista):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarCATEQUISTA ?", id_catequista)
        cursor.connection.commit()

def obtener_catequista_por_id(id_catequista):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM CATEQUISTA WHERE id_catequista = ?", id_catequista)
        return cursor.fetchone()
