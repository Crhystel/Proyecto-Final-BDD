from app.database import get_connection

def obtener_tipos_sacramento():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerTIPO_SACRAMENTO")
        return cursor.fetchall()

def crear_tipo_sacramento(nombre):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearTIPO_SACRAMENTO ?", nombre)
        cursor.connection.commit()

def actualizar_tipo_sacramento(id_sacramento_tipo, nombre):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarTIPO_SACRAMENTO ?, ?", (id_sacramento_tipo, nombre))
        cursor.connection.commit()

def eliminar_tipo_sacramento(id_sacramento_tipo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarTIPO_SACRAMENTO ?", id_sacramento_tipo)
        cursor.connection.commit()

def obtener_tipo_sacramento_por_id(id_sacramento_tipo):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM TIPO_SACRAMENTO WHERE id_sacramento_tipo = ?", id_sacramento_tipo)
        return cursor.fetchone()
