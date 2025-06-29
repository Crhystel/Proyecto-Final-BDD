from app.database import get_connection

def obtener_niveles():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerNIVELCATEQUESIS")
        return cursor.fetchall()

def obtener_nivel_por_id(id_nivel):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM NIVELCATEQUESIS WHERE id_nivel_catequesis = ?", id_nivel)
        return cursor.fetchone()

def crear_nivel(orden, nombre_nivel, descripcion, id_libro, id_tipo_sacramento):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearNIVELCATEQUESIS ?, ?, ?, ?, ?", 
                       (orden, nombre_nivel, descripcion, id_libro, id_tipo_sacramento))
        cursor.connection.commit()

def actualizar_nivel(id_nivel, orden, nombre_nivel, descripcion, id_libro, id_tipo_sacramento):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarNIVELCATEQUESIS ?, ?, ?, ?, ?, ?", 
                       (id_nivel, orden, nombre_nivel, descripcion, id_libro, id_tipo_sacramento))
        cursor.connection.commit()

def eliminar_nivel(id_nivel):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarNIVELCATEQUESIS ?", id_nivel)
        cursor.connection.commit()
