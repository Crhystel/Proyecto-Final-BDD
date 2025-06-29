from app.database import get_connection

def obtener_personas():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerPERSONA")
        return cursor.fetchall()

def crear_persona(nombre, apellido, tipo_persona, telefono, correo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearPERSONA ?, ?, ?, ?, ?", (nombre, apellido, tipo_persona, telefono, correo))
        cursor.connection.commit()

def actualizar_persona(id_persona, nombre, apellido, tipo_persona, telefono, correo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarPERSONA ?, ?, ?, ?, ?, ?", (id_persona, nombre, apellido, tipo_persona, telefono, correo))
        cursor.connection.commit()

def eliminar_persona(id_persona):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarPERSONA ?", id_persona)
        cursor.connection.commit()

def obtener_persona_por_id(id_persona):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM PERSONA WHERE id_persona = ?", id_persona)
        return cursor.fetchone()
