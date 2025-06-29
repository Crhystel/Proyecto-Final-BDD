from app.database import get_connection

def obtener_inscripciones():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerINSCRIPCION")
        return cursor.fetchall()

def crear_inscripcion(observaciones, estado_pago, fecha_inscripcion, id_catequizando, registrado_por, id_grupo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearINSCRIPCION ?, ?, ?, ?, ?, ?", 
                       (observaciones, estado_pago, fecha_inscripcion, id_catequizando, registrado_por, id_grupo))
        cursor.connection.commit()

def actualizar_inscripcion(id_inscripcion, observaciones, estado_pago, fecha_inscripcion, id_catequizando, registrado_por, id_grupo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarINSCRIPCION ?, ?, ?, ?, ?, ?, ?",
                       (id_inscripcion, observaciones, estado_pago, fecha_inscripcion, id_catequizando, registrado_por, id_grupo))
        cursor.connection.commit()

def eliminar_inscripcion(id_inscripcion):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarINSCRIPCION ?", id_inscripcion)
        cursor.connection.commit()

def obtener_inscripcion_por_id(id_inscripcion):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM INSCRIPCION WHERE id_inscripcion = ?", id_inscripcion)
        return cursor.fetchone()

def obtener_catequistas():
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT id_catequista, nombre FROM CATEQUISTA")
        return cursor.fetchall()

