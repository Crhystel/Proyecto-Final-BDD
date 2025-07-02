from app.database import get_db_connection
from .catequista_service import _get_next_id

def crear_libro(titulo, autor, editorial, anio_edicion):
    db = get_db_connection()
    
    nuevo_libro = {
        "_id": _get_next_id('libros'),
        "titulo": titulo,
        "autor": autor,
        "editorial": editorial,
        "anio_edicion": int(anio_edicion) if anio_edicion and anio_edicion.isdigit() else None
    }
    
    try:
        resultado = db.libros.insert_one(nuevo_libro)
        return resultado.inserted_id
    except Exception as e:
        print(f"Error al crear libro: {e}")
        return None
    
def obtener_libros():
    db = get_db_connection()
    return list(db.libros.find().sort("titulo", 1))

def obtener_libro_por_id(id_libro):
    db = get_db_connection()
    try:
        return db.libros.find_one({"_id": int(id_libro)})
    except (ValueError, TypeError):
        return None
    
def actualizar_libro(id_libro, titulo, autor, editorial, anio_edicion):
    db = get_db_connection()
    try:
        id_num = int(id_libro)
    except (ValueError, TypeError):
        return False
        
    update_data = {
        "$set": {
            "titulo": titulo,
            "autor": autor,
            "editorial": editorial,
            "anio_edicion": int(anio_edicion) if anio_edicion and anio_edicion.isdigit() else None
        }
    }
    
    resultado = db.libros.update_one({"_id": id_num}, update_data)
    return resultado.modified_count > 0

def eliminar_libro(id_libro):
    db = get_db_connection()
    try:
        resultado = db.libros.delete_one({"_id": int(id_libro)})
        return resultado.deleted_count > 0
    except (ValueError, TypeError):
        return False