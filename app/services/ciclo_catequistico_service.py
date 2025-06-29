from app.database import get_connection

def obtener_ciclos():
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_LeerCICLO_CATEQUISTICO")
        return cursor.fetchall()

def crear_ciclo(nombre, fecha_inicio, fecha_fin, id_nivel):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_CrearCICLO_CATEQUISTICO ?, ?, ?, ?", 
                       (nombre, fecha_inicio, fecha_fin, id_nivel))
        cursor.connection.commit()

def actualizar_ciclo(id_ciclo, nombre, fecha_inicio, fecha_fin, id_nivel):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_ActualizarCICLO_CATEQUISTICO ?, ?, ?, ?, ?", 
                       (id_ciclo, nombre, fecha_inicio, fecha_fin, id_nivel))
        cursor.connection.commit()

def eliminar_ciclo(id_ciclo):
    with get_connection().cursor() as cursor:
        cursor.execute("EXEC sp_EliminarCICLO_CATEQUISTICO ?", id_ciclo)
        cursor.connection.commit()

def obtener_ciclo_por_id(id_ciclo):
    with get_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM CICLO_CATEQUISTICO WHERE id_ciclo = ?", id_ciclo)
        return cursor.fetchone()
