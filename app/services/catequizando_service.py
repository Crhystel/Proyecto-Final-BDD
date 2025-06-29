from app.database import get_connection

def obtener_catequizandos():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerCATEQUIZANDO")
        return cursor.fetchall()

def crear_catequizando(apellido, nombre, fecha_nacimiento, doc_identidad, fecha_registro, bautizado, id_parroquia):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearCATEQUIZANDO ?, ?, ?, ?, ?, ?, ?",
                       (apellido, nombre, fecha_nacimiento, doc_identidad, fecha_registro, bautizado, id_parroquia))
        cursor.connection.commit()

def actualizar_catequizando(id_catequizando, apellido, nombre, fecha_nac, doc_id, fecha_reg, bautizado, id_parroquia):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarCATEQUIZANDO ?, ?, ?, ?, ?, ?, ?, ?",
                       (id_catequizando, apellido, nombre, fecha_nac, doc_id, fecha_reg, bautizado, id_parroquia))
        cursor.connection.commit()

def eliminar_catequizando(id_catequizando):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarCATEQUIZANDO ?", id_catequizando)
        cursor.connection.commit()

def obtener_catequizando_por_id(id):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM CATEQUIZANDO WHERE id_catequizando = ?", id)
        return cursor.fetchone()
