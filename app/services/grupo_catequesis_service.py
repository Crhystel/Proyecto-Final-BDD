from app.database import get_connection

def obtener_grupos():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerGRUPOCATEQUESIS")
        return cursor.fetchall()

def crear_grupo(nombre, id_parroquia, id_ciclo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearGRUPOCATEQUESIS ?, ?, ?", (nombre, id_parroquia, id_ciclo))
        cursor.connection.commit()

def actualizar_grupo(id_grupo, nombre, id_parroquia, id_ciclo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarGRUPOCATEQUESIS ?, ?, ?, ?", (id_grupo, nombre, id_parroquia, id_ciclo))
        cursor.connection.commit()

def eliminar_grupo(id_grupo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarGRUPOCATEQUESIS ?", id_grupo)
        cursor.connection.commit()

def obtener_grupo_por_id(id_grupo):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM GRUPOCATEQUESIS WHERE id_grupo_catequesis = ?", id_grupo)
        return cursor.fetchone()
