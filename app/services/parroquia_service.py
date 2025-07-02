from app.database import get_db_connection
from .catequizando_service import _get_next_id
from .ciclo_catequistico_service import obtener_ciclo_por_id

def crear_parroquia_grupo(nombre, direccion, ciudad, telefono, correo, id_principal_seleccionado,nombre_grupo,id_ciclo):
    db = get_db_connection()
    
    nueva_parroquia = {
        "_id": _get_next_id('parroquias'),
        "nombre": nombre,
        "direccion": direccion,
        "ciudad": ciudad,
        "telefono": int(telefono) if telefono and telefono.isdigit() else None,
        "correo_electronico": correo,
        "grupos_catequesis": [] 
    }
    
    if id_principal_seleccionado:
        parroquia_principal_doc = db.parroquias.find_one(
            {"_id": int(id_principal_seleccionado)},
            {"_id": 1, "nombre": 1, "direccion": 1, "ciudad": 1}
        )

        if parroquia_principal_doc:
            sub_documento = {
                "id_parroquia_principal": parroquia_principal_doc['_id'],
                "nombre": parroquia_principal_doc['nombre'],
                "direccion": parroquia_principal_doc['direccion'],
                "ciudad": parroquia_principal_doc['ciudad']
            }
            nueva_parroquia["parroquia_principal"] = sub_documento
        if nombre_grupo and id_ciclo:
            ciclo_data=obtener_ciclo_por_id(id_ciclo)
            grupo={
                "id_grupo_catequesis":_get_next_id('grupos_catequesis'),
                "nombre_grupo":nombre_grupo,
                "ciclo_ref":ciclo_data['_id'] if ciclo_data else None
            }
            nueva_parroquia["grupos_catequesis"].append(grupo)
            
    
    resultado = db.parroquias.insert_one(nueva_parroquia)
    return resultado.inserted_id

def obtener_parroquias():
    db=get_db_connection()
    pipeline=[
        
        {
            "$project": {
                "_id": 1,
                "nombre": 1,
                "direccion": 1,
                "ciudad": 1,
                "telefono": 1,
                "correo_electronico": 1,
                "nombre_principal": {"$ifNull": ["$parroquia_principal.nombre", "— (Principal)"]}
            }
        }
    ]
    return list(db.parroquias.aggregate(pipeline))

def obtener_parroquias_principales():
    db = get_db_connection()
    return list(db.parroquias.find(
        {"parroquia_principal": {"$exists": False}},
        {"_id": 1, "nombre": 1} 
    ))

def obtener_parroquia_por_id(id_parroquia):
    db = get_db_connection()
    try:
        id_num = int(id_parroquia)
        return db.parroquias.find_one({"_id": id_num})
    except (ValueError, TypeError):
        return None

def actualizar_parroquia(id_parroquia, nombre, direccion, ciudad, telefono, correo, id_parroquia_principal=None):
    db = get_db_connection()
    try:
        id_num = int(id_parroquia)
    except (ValueError, TypeError):
        return False
        
    update_data = {
         "$set": {
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "telefono": int(telefono) if telefono and telefono.isdigit() else None,
            "correo_electronico": correo
        }
    }
    if id_parroquia_principal:
        parroquia_principal_doc = db.parroquias.find_one({"_id": int(id_parroquia_principal)})
        if parroquia_principal_doc:
            sub_documento = {
                "id_parroquia_principal": parroquia_principal_doc['_id'],
                "nombre": parroquia_principal_doc['nombre'],
                "direccion": parroquia_principal_doc.get('direccion'), 
                "ciudad": parroquia_principal_doc.get('ciudad')
            }
            update_data["$set"]["parroquia_principal"] = sub_documento
    else:
        update_data["$unset"] = {"parroquia_principal": ""}
    resultado = db.parroquias.update_one({"_id": id_num}, update_data)
    return resultado.modified_count > 0

def eliminar_parroquia(id_parroquia):
    db = get_db_connection()
    try:
        id_num = int(id_parroquia)
        resultado = db.parroquias.delete_one({"_id": id_num})
        return resultado.deleted_count > 0
    except (ValueError, TypeError):
        return False