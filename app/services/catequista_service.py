from app.database import get_db_connection

from .catequizando_service import _get_next_id

def crear_catequista(nombre, apellido, correo, telefono, rol):
    db = get_db_connection()
    
    nuevo_catequista = {
        "_id": _get_next_id('catequistas'), 
        "nombre": nombre,
        "apellido": apellido,
        "telefono": int(telefono),  
        "correo_electrico": correo,
        "rol": rol.strip().upper(),  # 'P' para Principal, 'A' para Ayudante
        "grupos_como_principal": [],
        "grupos_como_secundario": []
    }
    resultado = db.catequistas.insert_one(nuevo_catequista)
    return resultado.inserted_id

def obtener_catequistas():
    db = get_db_connection()
    return list(db.catequistas.find({}))

def obtener_catequista_por_id(id_catequista):
    db = get_db_connection()
    return db.catequistas.find_one({"_id": int(id_catequista)})

def actualizar_catequista(id_catequista, nombre, apellido, correo, telefono, rol):
    db = get_db_connection()
    
    update_data = {
        "$set": {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": int(telefono),
            "correo_electrico": correo,
            "rol": rol.strip().upper(),
        }
    }
    
    resultado = db.catequistas.update_one(
        {"_id": int(id_catequista)},
        update_data
    )
    return resultado.modified_count > 0

def eliminar_catequista(id_catequista):
    db = get_db_connection()
    resultado = db.catequistas.delete_one({"_id": int(id_catequista)})
    return resultado.deleted_count > 0

def asignar_grupo_a_catequista(id_catequista, id_grupo, nombre_grupo, rol_catequista):
    db = get_db_connection()
    rol_normalizado = rol_catequista.strip().upper()
    rol_en_grupo = "Principal" if rol_normalizado == "P" else "Ayudante"
    grupo_data = {
        "_id": int(id_grupo),
        "nombre_grupo": nombre_grupo,
        "rol_en_grupo": rol_en_grupo
    }

    array_a_actualizar = "grupos_como_principal" if rol_normalizado == "P" else "grupos_como_secundario"

    resultado = db.catequistas.update_one(
        {"_id": int(id_catequista)},
        {"$push": {array_a_actualizar: grupo_data}}
    )
    return resultado.modified_count > 0

def eliminar_grupo_de_catequista(id_catequista, id_grupo):
    db = get_db_connection()
    resultado = db.catequistas.update_one(
        {"_id": int(id_catequista)},
        {
            "$pull": {
                "grupos_como_principal": {"_id": int(id_grupo)},
                "grupos_como_secundario": {"_id": int(id_grupo)}
            }
        }
    )
    return resultado.modified_count > 0
def obtener_todos_los_grupos():
    db = get_db_connection()
    pipeline = [
        {"$unwind": "$grupos_catequesis"}, 
        {"$replaceRoot": {"newRoot": "$grupos_catequesis"}} 
    ]
    return list(db.parroquias.aggregate(pipeline))

def obtener_grupo_por_id(id_grupo):
    db = get_db_connection()
    parroquia = db.parroquias.find_one(
        {"grupos_catequesis._id": int(id_grupo)},
        {"grupos_catequesis.$": 1} 
    )
    if parroquia and parroquia.get('grupos_catequesis'):
        return parroquia['grupos_catequesis'][0]
    return None