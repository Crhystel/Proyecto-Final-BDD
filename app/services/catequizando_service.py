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

def crear_catequizando(nombre, apellido, fecha_nacimiento, doc_identidad, fecha_registro, id_parroquia):
    db = get_db_connection()
    nuevo_catequizando = {
        "_id": _get_next_id('catequizandos'),
        "nombre": nombre, "apellido": apellido,
        "fecha_nacimiento": datetime.datetime.fromisoformat(fecha_nacimiento),
        "documento_identidad": doc_identidad,
        "fecha_registro": datetime.datetime.fromisoformat(fecha_registro),
        "parroquia_ref": int(id_parroquia) if id_parroquia else None,
        "tiene_bautismo": False, "lugar_bautismo": None, "fecha_bautismo": None,
        "documentos": [], "historial_parroquial": [], "inscripciones": [],
        "progresos": [], "asistencias": [], "sesiones_especiales": [], "sacramentos": []
    }
    db.catequizandos.insert_one(nuevo_catequizando)
    if id_parroquia:
        agregar_a_historial_parroquial(nuevo_catequizando['_id'], id_parroquia)
    return nuevo_catequizando['_id']

def obtener_catequizandos():
    db = get_db_connection()
    pipeline = [
        {"$lookup": {"from": "parroquias", "localField": "parroquia_ref", "foreignField": "_id", "as": "parroquia_info"}},
        {"$unwind": {"path": "$parroquia_info", "preserveNullAndEmptyArrays": True}},
        {"$project": { "_id": 1, "nombre": 1, "apellido": 1, "nombre_parroquia": "$parroquia_info.nombre" }},
        {"$sort": {"apellido": 1, "nombre": 1}}
    ]
    return list(db.catequizandos.aggregate(pipeline))

def obtener_catequizando_por_id(id_catequizando):
    db = get_db_connection()
    return db.catequizandos.find_one({"_id": int(id_catequizando)})

def actualizar_catequizando_principal(id_catequizando, datos_actualizacion):
    db = get_db_connection()
    id_num = int(id_catequizando)
    catequizando_actual = db.catequizandos.find_one({"_id": id_num}, {"parroquia_ref": 1})
    parroquia_anterior_ref = catequizando_actual.get('parroquia_ref')
    
    db.catequizandos.update_one({"_id": id_num}, {"$set": datos_actualizacion})
    
    nueva_parroquia_ref = datos_actualizacion.get('parroquia_ref')
    if nueva_parroquia_ref is not None and nueva_parroquia_ref != parroquia_anterior_ref:
        finalizar_historial_actual(id_num)
        agregar_a_historial_parroquial(id_num, nueva_parroquia_ref)

def eliminar_catequizando(id_catequizando):
    db = get_db_connection()
    db.catequizandos.delete_one({"_id": int(id_catequizando)})
    
def agregar_documento(id_catequizando, ruta_archivo, tipo, descripcion):
    db = get_db_connection()
    documento = { "_id": _get_next_id('documentos'), "ruta_archivo": ruta_archivo, "tipo": tipo, "descripcion": descripcion }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"documentos": documento}})

def eliminar_documento(id_catequizando, id_documento):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"documentos": {"_id": int(id_documento)}}})

# --- Historial Parroquial ---
def agregar_a_historial_parroquial(id_catequizando, id_parroquia):
    db = get_db_connection()
    historial_entry = { "fecha_inicio": datetime.datetime.utcnow(), "fecha_fin": None, "parroquia_ref": int(id_parroquia) }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"historial_parroquial": historial_entry}})
    
def finalizar_historial_actual(id_catequizando):
    db = get_db_connection()
    db.catequizandos.update_one(
        {"_id": int(id_catequizando), "historial_parroquial.fecha_fin": None},
        {"$set": {"historial_parroquial.$.fecha_fin": datetime.datetime.now(datetime.timezone.utc)}}
    )

# --- Inscripciones ---
def agregar_inscripcion(id_catequizando, observaciones, estado_pago, id_grupo, id_registrador):
    db = get_db_connection()
    inscripcion = {
        "_id": _get_next_id('inscripciones'), "observaciones": observaciones, "estado_pago": estado_pago,
        "fecha_inscripcion": datetime.datetime.utcnow(), "grupo_ref": int(id_grupo), "registrado_por_ref": int(id_registrador), "certificado": None
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"inscripciones": inscripcion}})
def eliminar_inscripcion(id_catequizando, id_inscripcion):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"inscripciones": {"_id": int(id_inscripcion)}}})
# --- Progresos ---
def agregar_progreso(id_catequizando, id_nivel, id_catequista):
    db = get_db_connection()
    progreso = {
        "_id": _get_next_id('progresos'), "aprobado": False, "fecha_fin": None, "certificado_emitido": False, "intento": 1,
        "nivel_ref": int(id_nivel), "catequista_aprobador_ref": int(id_catequista), "autorizacion": None
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"progresos": progreso}})

def actualizar_progreso(id_catequizando, id_progreso, datos_actualizacion):
    db = get_db_connection()
    update_query = {f"progresos.$.{key}": value for key, value in datos_actualizacion.items()}
    db.catequizandos.update_one({"_id": int(id_catequizando), "progresos._id": int(id_progreso)}, {"$set": update_query})

def eliminar_progreso(id_catequizando, id_progreso):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"progresos": {"_id": int(id_progreso)}}})

# --- Asistencias ---
def registrar_asistencia(id_catequizando, fecha, estado, id_nivel, id_grupo, id_catequista):
    db = get_db_connection()
    asistencia = {
        "_id": _get_next_id('asistencias'), "fecha": datetime.datetime.fromisoformat(fecha), "estado": estado,
        "nivel_ref": int(id_nivel), "grupo_ref": int(id_grupo), "catequista_ref": int(id_catequista)
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"asistencias": asistencia}})

def eliminar_asistencia(id_catequizando, id_asistencia):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"asistencias": {"_id": int(id_asistencia)}}})

# --- Sesiones Especiales ---
def agregar_sesion_especial(id_catequizando, tipo_sesion, observaciones, id_autorizador):
    db = get_db_connection()
    sesion = {
        "_id": _get_next_id('sesiones_especiales'), "tipo_sesion": tipo_sesion, "observaciones": observaciones,
        "fecha": datetime.datetime.utcnow(), "autorizado_por_ref": int(id_autorizador)
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"sesiones_especiales": sesion}})

def eliminar_sesion_especial(id_catequizando, id_sesion):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"sesiones_especiales": {"_id": int(id_sesion)}}})

# --- Sacramentos ---
def registrar_sacramento(id_catequizando, datos_sacramento):
    db = get_db_connection()
    sacramento = {
        "_id": _get_next_id('sacramentos'), "estado": "R", **datos_sacramento
    }
    # Convertir IDs a enteros
    for key in ['tipo_sacramento_ref', 'padre_ref', 'madre_ref', 'padrino_ref', 'madrina_ref']:
        if key in sacramento and sacramento[key]:
            sacramento[key] = int(sacramento[key])
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"sacramentos": sacramento}})

def eliminar_sacramento(id_catequizando, id_sacramento):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"sacramentos": {"_id": int(id_sacramento)}}})
    
def generar_certificado_para_inscripcion(id_catequizando, id_inscripcion, contenido):
    db = get_db_connection()
    certificado = { "id_certificado": _get_next_id('certificados'), "contenido": contenido, "fecha_emision": datetime.datetime.utcnow() }
    db.catequizandos.update_one(
        {"_id": int(id_catequizando), "inscripciones._id": int(id_inscripcion)},
        {"$set": {"inscripciones.$.certificado": certificado}}
    )

def eliminar_certificado_de_inscripcion(id_catequizando, id_inscripcion):
    db = get_db_connection()
    db.catequizandos.update_one(
        {"_id": int(id_catequizando), "inscripciones._id": int(id_inscripcion)},
        {"$set": {"inscripciones.$.certificado": None}}
    )
