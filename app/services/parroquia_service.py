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
    if id_parroquia_principal and int(id_parroquia_principal) == id_num:
        print("Error: Una parroquia no puede ser su propia parroquia principal.")
        return -1 
    
    update_data = {
         "$set": {
            "nombre": nombre,
            "direccion": direccion,
            "ciudad": ciudad,
            "telefono": int(telefono) if telefono and telefono.isdigit() else None,
            "correo_electronico": correo
        }
    }
    if id_parroquia_principal :
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
        update_data["$set"]["grupos_catequesis"]=[]
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
    
def agregar_grupo_a_parroquia(id_parroquia, nombre_grupo, id_ciclo):
    db = get_db_connection()
    
    ciclo_data = obtener_ciclo_por_id(id_ciclo)

    if not ciclo_data:
        return False
    nuevo_grupo = {
        "id_grupo_catequesis": _get_next_id('grupos_catequesis'), 
        "nombre_grupo": nombre_grupo,
        "ciclo_ref": ciclo_data['_id'] 
    }
    
    resultado = db.parroquias.update_one(
        {"_id": int(id_parroquia)},
        {"$push": {"grupos_catequesis": nuevo_grupo}}
    )
    
    return resultado.modified_count > 0
def obtener_grupos_de_parroquia(id_parroquia):
    db = get_db_connection()
    parroquia = db.parroquias.find_one(
        {"_id": int(id_parroquia)},
        {"grupos_catequesis": 1, "_id": 0} 
    )
    
    if parroquia and 'grupos_catequesis' in parroquia:
        grupos = []
        for g in parroquia['grupos_catequesis']:
            grupo_info = {
                '_id': g.get('id_grupo_catequesis'), 
                'nombre': g.get('nombre_grupo', '').strip(),
                'ciclo': g.get('ciclo_ref')
            }
            grupos.append(grupo_info)
        return grupos
    
    return []


def obtener_detalles_completos_parroquia(id_parroquia):
    db = get_db_connection()
    try:
        id_num = int(id_parroquia)
    except (ValueError, TypeError):
        return None

    pipeline = [
        {"$match": {"_id": id_num}},
        {"$unwind": {"path": "$grupos_catequesis", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "ciclos_catequisticos",
            "localField": "grupos_catequesis.ciclo_ref",
            "foreignField": "_id",
            "as": "ciclo_completo"
        }},
        {"$unwind": {"path": "$ciclo_completo", "preserveNullAndEmptyArrays": True}},
        {"$lookup": {
            "from": "niveles_catequesis",
            "localField": "ciclo_completo.nivel_ref",
            "foreignField": "_id",
            "as": "nivel_completo"
        }},
        {"$unwind": {"path": "$nivel_completo", "preserveNullAndEmptyArrays": True}},
        {"$group": {
            "_id": "$_id",
            "nombre": {"$first": "$nombre"},
            "direccion": {"$first": "$direccion"},
            "ciudad": {"$first": "$ciudad"},
            "telefono": {"$first": "$telefono"},
            "correo_electronico": {"$first": "$correo_electronico"},
            "parroquia_principal": {"$first": "$parroquia_principal"},
            "grupos_catequesis": {
                "$push": {
                    "$cond": {
                        "if": "$grupos_catequesis.id_grupo_catequesis",
                        "then": {
                            "id_grupo_catequesis": "$grupos_catequesis.id_grupo_catequesis",
                            "nombre_grupo": "$grupos_catequesis.nombre_grupo",
                            "nombre_ciclo": {
                                "$ifNull": ["$ciclo_completo.nombre", "Sin ciclo asignado"]
                            },
                        
                            "nombre": {
                                "$ifNull": ["$nivel_completo.nombre", "Sin nivel"]
                            }
                        },
                        "else": "$$REMOVE" 
                    }
                }
            }
        }}
    ]
    resultado = list(db.parroquias.aggregate(pipeline))
    if resultado and "grupos_catequesis" in resultado[0]:
        if len(resultado[0]["grupos_catequesis"]) == 1 and not resultado[0]["grupos_catequesis"][0]:
            resultado[0]["grupos_catequesis"] = []
            
    return resultado[0] if resultado else None