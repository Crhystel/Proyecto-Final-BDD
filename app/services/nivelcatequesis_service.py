from app.database import get_db_connection
from .catequizando_service import _get_next_id

def crear_nivel( nombre_nivel, descripcion, id_libro=None, id_tipo_sacramento=None):
    db = get_db_connection()
    
    nuevo_nivel = {
        "_id": _get_next_id('niveles_catequesis'),
        "nombre": nombre_nivel,
        "descripcion": descripcion
    }

    if id_libro:
        libro_doc = db.libros.find_one({"_id": int(id_libro)})
        if libro_doc:
            nuevo_nivel['libro'] = libro_doc

    if id_tipo_sacramento:
        sacramento_doc = db.tipo_sacramentos.find_one({"_id": int(id_tipo_sacramento)})
        if sacramento_doc:
            nuevo_nivel['tipo_sacramento'] = sacramento_doc

    resultado = db.niveles_catequesis.insert_one(nuevo_nivel)
    return resultado.inserted_id

def obtener_niveles():
    db = get_db_connection()
    
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "nombre": 1,
                "descripcion": 1,
                "nombre_libro": {"$ifNull": ["$libro.titulo", "— Sin libro —"]},
                "nombre_sacramento": {"$ifNull": ["$tipo_sacramento.nombre", "— Sin sacramento —"]}
            }
        },
        {"$sort": {"_id": 1}}
    ]
    
    return list(db.niveles_catequesis.aggregate(pipeline))

def obtener_nivel_por_id(id_nivel):
    db = get_db_connection()
    try:
        return db.niveles_catequesis.find_one({"_id": int(id_nivel)})
    except (ValueError, TypeError):
        return None
    
def actualizar_nivel(id_nivel, nombre_nivel, descripcion, id_libro=None, id_tipo_sacramento=None):
    db = get_db_connection()
    id_num = int(id_nivel)
    
    update_doc = {
        "$set": {
            "nombre": nombre_nivel,
            "descripcion": descripcion
        }
    }
    if id_libro:
        libro_doc = db.libros.find_one({"_id": int(id_libro)})
        if libro_doc:
            update_doc["$set"]['libro'] = libro_doc
    else:
        update_doc["$unset"] = {"libro": ""}

    if id_tipo_sacramento:
        sacramento_doc = db.tipo_sacramentos.find_one({"_id": int(id_tipo_sacramento)})
        if sacramento_doc:
            update_doc["$set"]['tipo_sacramento'] = sacramento_doc
    else:
        update_doc.setdefault("$unset", {})["tipo_sacramento"] = ""

    resultado = db.niveles_catequesis.update_one({"_id": id_num}, update_doc)
    return resultado.modified_count > 0

def eliminar_nivel(id_nivel):
    db = get_db_connection()
    try:
        id_num = int(id_nivel)
        resultado = db.niveles_catequesis.delete_one({"_id": id_num})
        return resultado.deleted_count > 0
    except (ValueError, TypeError):
        return 0