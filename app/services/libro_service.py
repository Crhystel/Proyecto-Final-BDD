from app.database import get_connection

def obtener_libros():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerLIBRO")
        return cursor.fetchall()

def crear_libro(titulo, autor, editorial, anio_edicion):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearLIBRO ?, ?, ?, ?", (titulo, autor, editorial, anio_edicion))
        cursor.connection.commit()

def actualizar_libro(id_libro, titulo, autor, editorial, anio_edicion):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarLIBRO ?, ?, ?, ?, ?", (id_libro, titulo, autor, editorial, anio_edicion))
        cursor.connection.commit()

def eliminar_libro(id_libro):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarLIBRO ?", id_libro)
        cursor.connection.commit()

def obtener_libro_por_id(id_libro):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM LIBRO WHERE id_libro = ?", id_libro)
        return cursor.fetchone()
