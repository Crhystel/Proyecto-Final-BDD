from app.database import get_connection

def obtener_fichas():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerFICHA_DATOS")
        return cursor.fetchall()

def crear_ficha(id_catequizando, tiene_bautismo, requiere_especial, observaciones, lugar, fecha):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearFICHA_DATOS ?, ?, ?, ?, ?, ?",
                       (id_catequizando, tiene_bautismo, requiere_especial, observaciones, lugar, fecha))
        cursor.connection.commit()

def actualizar_ficha(id_ficha, id_catequizando, tiene_bautismo, requiere_especial, observaciones, lugar, fecha):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarFICHA_DATOS ?, ?, ?, ?, ?, ?, ?",
                       (id_ficha, id_catequizando, tiene_bautismo, requiere_especial, observaciones, lugar, fecha))
        cursor.connection.commit()

def eliminar_ficha(id_ficha):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarFICHA_DATOS ?", id_ficha)
        cursor.connection.commit()

def obtener_ficha_por_id(id_ficha):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM FICHA_DATOS WHERE id_ficha = ?", id_ficha)
        return cursor.fetchone()
