from app.database import get_connection

def obtener_certificados():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerCERTIFICADO")
        return cursor.fetchall()

def crear_certificado(contenido, fecha_emision, id_inscripcion):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearCERTIFICADO ?, ?, ?", (contenido, fecha_emision, id_inscripcion))
        cursor.connection.commit()

def actualizar_certificado(id_certificado, contenido, fecha_emision, id_inscripcion):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarCERTIFICADO ?, ?, ?, ?", (id_certificado, contenido, fecha_emision, id_inscripcion))
        cursor.connection.commit()

def eliminar_certificado(id_certificado):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarCERTIFICADO ?", id_certificado)
        cursor.connection.commit()

def obtener_certificado_por_id(id_certificado):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM CERTIFICADO WHERE id_certificado = ?", id_certificado)
        return cursor.fetchone()

def obtener_inscripciones():
    with get_connection().cursor() as cursor:
        cursor.execute("""
            SELECT I.id_inscripcion, C.nombre + ' ' + C.apellido AS nombre_completo
            FROM INSCRIPCION I
            JOIN CATEQUIZANDO C ON I.id_catequizando = C.id_catequizando
        """)
        return cursor.fetchall()
