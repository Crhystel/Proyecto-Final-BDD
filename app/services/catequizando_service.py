from app.database import get_db_connection
from bson import ObjectId
import datetime
from pymongo import ReturnDocument

def _get_next_id(collection_name):
    db=get_db_connection()
    sequence_document=db.counters.find_one_and_update(
        {'_id':f"{collection_name}_id"},
        {'$inc':{'sequence_value':1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return sequence_document['sequence_value']
def sincronizar_contador(collection_name):
    db=get_db_connection()
    documento_max_id=list(db[collection_name].find().sort("_id",-1).limit(1))
    max_id=0
    if documento_max_id:
        max_id=documento_max_id[0]["_id"]
    db.counters.update_one(
        {'_id':f"{collection_name}_id"},
        {'$max':{'sequence_value':max_id}},
        upsert=True
    )
    

# Funciones CRUD principales

#Crear catequizando
def crear_catequizando(apellido,nombre,fecha_nacimiento, doc_identidad, fecha_registro, bautizado, id_parroquia):
    db=get_db_connection()
    nuevo_catequizando={
        "_id":_get_next_id('catequizandos'),
        "nombre": nombre,
        "apellido":apellido,
        "fecha_nacimiento":datetime.datetime.fromisoformat(fecha_nacimiento),
        "documento_identidad":doc_identidad,
        "fecha_registro":datetime.datetime.fromisoformat(fecha_registro),
        "parroquia_ref":ObjectId(id_parroquia) if id_parroquia else None,
       "ficha_datos":{
           "tiene_bautismo":bool(bautizado),
           "requiere_atencion_especial":False,
           "observaciones": "",
           "lugar_bautismo":None,
           "fecha_bautismo":None
       },
       "documentos":[],
       "historial_parroquial":[],
       "inscripciones":[],
       "progresos":[],
       "asistencias":[],
        "sesiones_especiales":[],
        "sacramentos":[]
        
    }
    resultado=db.catequizandos.insert_one(nuevo_catequizando)
    return resultado.inserted_id

#Obtener catequizando
def obtener_catequizandos():
    db=get_db_connection()
    return list(db.catequizandos.find({}))

#Obtener catequizando por id
def obtener_catequizando_por_id(id_catequizando):
    db=get_db_connection()
    return db.catequizandos.find_one({"_id":int(id_catequizando)})

#Actualizar catequizando

def actualizar_catequizando(id_catequizando,apellido,nombre,fecha_nac,doc_id,fecha_reg,bautizado,id_parroquia):
    db=get_db_connection()
    update_data={
        "$set":{
            "nombre":nombre,
            "apellido":apellido,
            "fecha_nacimiento":fecha_nac,
            "documento_identidad":doc_id,
            "fecha_registro":datetime.datetime.fromisoformat(fecha_reg),
            "parroquia_ref":ObjectId(id_parroquia) if id_parroquia else None,
            "ficha_datos.tiene_bautismo":bool(bautizado)
        }
    }
    resultado=db.catequizandos.update_one(
        {
            "_id":int(id_catequizando)
        },
        update_data
    )
    return resultado.modified_count > 0

#Eliminar catequizando
def eliminar_catequizando(id_catequizando):
    db=get_db_connection()
    resultado=db.catequizandos.delete_one({"_id":int(id_catequizando)})
    return resultado.deleted_count > 0


# Funciones para datos embebidos
def agregar_inscripcion(id_catequizando,datos_inscipcion):
    db=get_db_connection()
    resultado=db.catequizandos.update_one(
        {"_id":int(id_catequizando)},
        {"$push":{"inscripciones":datos_inscipcion}}
    )
    return resultado.modified_count>0