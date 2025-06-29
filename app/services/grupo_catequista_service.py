from app.database import get_connection

def obtener_grupos_catequistas():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerGRUPO_CATEQUISTA")
        return cursor.fetchall()

def crear_grupo_catequista(id_grupo, id_catequista_principal, id_catequista_secundario):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearGRUPO_CATEQUISTA ?, ?, ?", (id_grupo, id_catequista_principal, id_catequista_secundario))
        cursor.connection.commit()

def actualizar_grupo_catequista(id_grupo, id_catequista_principal, id_catequista_secundario):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarGRUPO_CATEQUISTA ?, ?, ?", (id_grupo, id_catequista_principal, id_catequista_secundario))
        cursor.connection.commit()

def eliminar_grupo_catequista(id_grupo, id_catequista):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarGRUPO_CATEQUISTA ?, ?", (id_grupo, id_catequista))
        cursor.connection.commit()

# Funciones auxiliares para combos
def obtener_grupos():
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT id_grupo_catequesis, nombre FROM GRUPOCATEQUESIS")
        return cursor.fetchall()

def obtener_catequistas_por_rol(rol):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT id_catequista, nombre FROM CATEQUISTA WHERE rol = ?", rol)
        return cursor.fetchall()
