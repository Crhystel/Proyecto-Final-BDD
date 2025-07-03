from app.database import get_db_connection
import datetime
from .catequista_service import _get_next_id

def crear_ciclo(nombre, fecha_inicio, fecha_fin, id_nivel):
    db = get_db_connection()
    
    nuevo_ciclo = {
        "_id": _get_next_id('ciclos_catequisticos'), # Usamos nuestro generador de IDs
        "nombre": nombre,
        "fecha_inicio": datetime.datetime.fromisoformat(fecha_inicio),
        "fecha_fin": datetime.datetime.fromisoformat(fecha_fin),
        "nivel_ref": int(id_nivel) if id_nivel else None
    }
    
    resultado = db.ciclos_catequisticos.insert_one(nuevo_ciclo)
    return resultado.inserted_id

def obtener_ciclos():
    db = get_db_connection()
    pipeline = [
        {
            "$lookup": {
                "from": "niveles_catequesis", 
                "localField": "nivel_ref",  
                "foreignField": "_id",     
                "as": "nivel_info"          
            }
        },
        {
            "$unwind": {
                "path": "$nivel_info",
                "preserveNullAndEmptyArrays": True 
            }
        },
        {
            "$project": {
                "_id": 1,
                "nombre": 1,
                "fecha_inicio": 1,
                "fecha_fin": 1,
                "nombre_nivel": "$nivel_info.nombre_nivel" # Proyectamos el nombre del nivel
            }
        }
    ]
    return list(db.ciclos_catequisticos.aggregate(pipeline))

def obtener_ciclo_por_id(id_ciclo):
    db = get_db_connection()
    try:
        id_num = int(id_ciclo)
        return db.ciclos_catequisticos.find_one({"_id": id_num})
    except (ValueError, TypeError):
        return None
    
def actualizar_ciclo(id_ciclo, nombre, fecha_inicio, fecha_fin, id_nivel):
    db = get_db_connection()
    try:
        id_num = int(id_ciclo)
    except (ValueError, TypeError):
        return False
        
    update_data = {
        "$set": {
            "nombre": nombre,
            "fecha_inicio": datetime.datetime.fromisoformat(fecha_inicio),
            "fecha_fin": datetime.datetime.fromisoformat(fecha_fin),
            "nivel_ref": int(id_nivel) if id_nivel else None
        }
    }
    resultado = db.ciclos_catequisticos.update_one({"_id": id_num}, update_data)
    return resultado.modified_count > 0

def eliminar_ciclo(id_ciclo):
    db = get_db_connection()
    try:
        id_num = int(id_ciclo)
        resultado = db.ciclos_catequisticos.delete_one({"_id": id_num})
        return resultado.deleted_count > 0
    except (ValueError, TypeError):
        return False