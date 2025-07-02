from app.database import get_db_connection
from bson import ObjectId
from .catequizando_service import _get_next_id

def crear_parroquia(nombre, direccion, ciudad, telefono, correo, id_parroquia_principal=None):
    db = get_db_connection()
    
    nueva_parroquia = {
        "_id": _get_next_id('parroquias'),
        "nombre": nombre,
        "direccion": direccion,
        "ciudad": ciudad,
        "telefono": int(telefono) if telefono else None,
        "correo_electronico": correo,
        # Inicializamos el array embebido de grupos
        "grupos_catequesis": [] 
    }
    
    if id_parroquia_principal:
        nueva_parroquia["parroquia_principal"] = ObjectId(id_parroquia_principal)
    else:
        nueva_parroquia["parroquia_principal"] = None

    resultado = db.parroquias.insert_one(nueva_parroquia)
    return resultado.inserted_id

def obtener_parroquias():
    db=get_db_connection()
    pipeline=[
        # self-join
        {
            "$lookup": {
                "from": "parroquias",
                "localField": "parroquia_principal",
                "foreignField": "_id",
                "as": "info_principal"
            }
        },
        {
            "$unwind": {
                "path": "$info_principal",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 1,
                "nombre": 1,
                "direccion": 1,
                "ciudad": 1,
                "telefono": 1,
                "correo_electronico": 1,
                "nombre_principal": "$info_principal.nombre" 
            }
        }
    ]
    return list(db.parroquias.aggregate(pipeline))

def obtener_parroquias_principales():
    db = get_db_connection()
    # Buscamos documentos donde 'parroquia_principal' sea nulo
    return list(db.parroquias.find({"parroquia_principal": None}))

def obtener_parroquia_por_id(id_parroquia):
    db = get_db_connection()
    return db.parroquias.find_one({"_id": int(id_parroquia)})

def actualizar_parroquia(id_parroquia, nombre, direccion, ciudad, telefono, correo, id_parroquia_principal=None):
    db = get_db_connection()
    update_data = {
        "$set": {
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "telefono": int(telefono) if telefono else None,
            "correo_electronico": correo,
            "parroquia_principal": ObjectId(id_parroquia_principal) if id_parroquia_principal else None
        }
    }
    
    resultado = db.parroquias.update_one({"_id": int(id_parroquia)}, update_data)
    return resultado.modified_count > 0

def eliminar_parroquia(id_parroquia):
    db = get_db_connection()
    resultado = db.parroquias.delete_one({"_id": int(id_parroquia)})
    return resultado.deleted_count > 0