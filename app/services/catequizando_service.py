from app.database import get_db_connection
import datetime
from pymongo import ReturnDocument

# ===============================================
# === FUNCIONES AUXILIARES
# ===============================================

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

def _parse_date_from_string(date_string):
    """
    Convierte un string de fecha (formato YYYY-MM-DD o ISO) a un objeto datetime.
    Es robusto para manejar entradas vacías o None.
    """
    if not date_string:
        return None
    try:
        # Prioriza el formato de <input type="date">
        return datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except (ValueError, TypeError):
        try:
            # Fallback para formato ISO
            return datetime.datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except (ValueError, TypeError):
            return None

# ===============================================
# === GESTIÓN PRINCIPAL DEL CATEQUIZANDO
# ===============================================

def crear_catequizando(nombre, apellido, doc_identidad, fecha_nacimiento, 
                       fecha_registro, id_parroquia, tiene_bautismo, 
                       lugar_bautismo, fecha_bautismo):
    db = get_db_connection()
    
    nuevo_catequizando = {
        "_id": _get_next_id('catequizandos'),
        "nombre": nombre, "apellido": apellido,
        "documento_identidad": doc_identidad,
        "fecha_nacimiento": _parse_date_from_string(fecha_nacimiento),
        "fecha_registro": _parse_date_from_string(fecha_registro) or datetime.datetime.now(datetime.timezone.utc),
        "parroquia_ref": int(id_parroquia) if id_parroquia else None,
        "tiene_bautismo": tiene_bautismo,
        "lugar_bautismo": lugar_bautismo if tiene_bautismo else None,
        "fecha_bautismo": _parse_date_from_string(fecha_bautismo) if tiene_bautismo else None,
        "documentos": [], "historial_parroquial": [], "inscripciones": [],
        "progresos": [], "asistencias": [], "sesiones_especiales": [], "sacramentos": []
    }
    
    result = db.catequizandos.insert_one(nuevo_catequizando)
    
    if id_parroquia:
        agregar_a_historial_parroquial(result.inserted_id, nuevo_catequizando['fecha_registro'], id_parroquia)
        
    return result.inserted_id

def obtener_catequizandos():
    db = get_db_connection()
    pipeline = [
        {"$lookup": {"from": "parroquias", "localField": "parroquia_ref", "foreignField": "_id", "as": "parroquia_info"}},
        {"$unwind": {"path": "$parroquia_info", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "_id": 1, "nombre": 1, "apellido": 1, "documento_identidad": 1, "fecha_nacimiento": 1, 
            "tiene_bautismo": 1, "nombre_parroquia": "$parroquia_info.nombre"}},
        {"$sort": {"apellido": 1, "nombre": 1}}
    ]
    return list(db.catequizandos.aggregate(pipeline))

def obtener_catequizando_por_id(id_catequizando):
    db = get_db_connection()
    return db.catequizandos.find_one({"_id": int(id_catequizando)})

def actualizar_catequizando_principal(id_catequizando, datos_actualizacion):
    db = get_db_connection()
    id_num = int(id_catequizando)
    
    for campo in ['fecha_nacimiento', 'fecha_bautismo']:
        if campo in datos_actualizacion:
            datos_actualizacion[campo] = _parse_date_from_string(datos_actualizacion[campo])
    
    catequizando_actual = db.catequizandos.find_one({"_id": id_num}, {"parroquia_ref": 1})
    if not catequizando_actual: return

    parroquia_anterior_ref = catequizando_actual.get('parroquia_ref')
    nueva_parroquia_ref = datos_actualizacion.get('parroquia_ref')
    if nueva_parroquia_ref is not None and nueva_parroquia_ref != parroquia_anterior_ref:
        finalizar_historial_actual(id_num, datetime.datetime.now(datetime.timezone.utc))
        agregar_a_historial_parroquial(id_num, datetime.datetime.now(datetime.timezone.utc), nueva_parroquia_ref)

    db.catequizandos.update_one({"_id": id_num}, {"$set": datos_actualizacion})

def eliminar_catequizando(id_catequizando):
    db = get_db_connection()
    db.catequizandos.delete_one({"_id": int(id_catequizando)})

# ===============================================
# === GESTIÓN DE DOCUMENTOS
# ===============================================

def agregar_documento(id_catequizando, ruta_archivo, tipo, descripcion):
    db = get_db_connection()
    documento = {"_id": _get_next_id('documentos'), "ruta_archivo": ruta_archivo, "tipo": tipo, "descripcion": descripcion}
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"documentos": documento}})

def actualizar_documento(id_catequizando, id_documento, datos_actualizacion):
    db = get_db_connection()
    update_fields = {f"documentos.$[elem].{key}": value for key, value in datos_actualizacion.items()}
    db.catequizandos.update_one(
        {"_id": int(id_catequizando)},
        {"$set": update_fields},
        array_filters=[{"elem._id": int(id_documento)}]
    )

def eliminar_documento(id_catequizando, id_documento):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"documentos": {"_id": int(id_documento)}}})

# ===============================================
# === GESTIÓN DE INSCRIPCIONES
# ===============================================

def agregar_inscripcion(id_catequizando, fecha_inscripcion, observaciones, estado_pago, id_grupo, id_registrador):
    db = get_db_connection()
    inscripcion = {
        "_id": _get_next_id('inscripciones'), "fecha_inscripcion": _parse_date_from_string(fecha_inscripcion), 
        "observaciones": observaciones, "estado_pago": estado_pago,
        "grupo_ref": int(id_grupo) if id_grupo else None, 
        "registrado_por_ref": int(id_registrador) if id_registrador else None, "certificado": None
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"inscripciones": inscripcion}})

def actualizar_inscripcion(id_catequizando, id_inscripcion, datos_actualizacion):
    db = get_db_connection()
    update_fields = {}
    for key, value in datos_actualizacion.items():
        if key == "fecha_inscripcion": update_fields[f"inscripciones.$[elem].{key}"] = _parse_date_from_string(value)
        elif key == "grupo_ref": update_fields[f"inscripciones.$[elem].{key}"] = int(value) if value else None
        else: update_fields[f"inscripciones.$[elem].{key}"] = value
    
    db.catequizandos.update_one(
        {"_id": int(id_catequizando)},
        {"$set": update_fields},
        array_filters=[{"elem._id": int(id_inscripcion)}]
    )

def eliminar_inscripcion(id_catequizando, id_inscripcion):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"inscripciones": {"_id": int(id_inscripcion)}}})

# --- Certificados de Inscripción ---
def generar_certificado_para_inscripcion(id_catequizando, id_inscripcion, contenido):
    db = get_db_connection()
    certificado = {"id_certificado": _get_next_id('certificados'), "contenido": contenido, "fecha_emision": datetime.datetime.now(datetime.timezone.utc)}
    db.catequizandos.update_one({"_id": int(id_catequizando), "inscripciones._id": int(id_inscripcion)}, {"$set": {"inscripciones.$.certificado": certificado}})

def eliminar_certificado_de_inscripcion(id_catequizando, id_inscripcion):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando), "inscripciones._id": int(id_inscripcion)}, {"$set": {"inscripciones.$.certificado": None}})

# ===============================================
# === GESTIÓN DE PROGRESOS ACADÉMICOS
# ===============================================

def agregar_progreso(id_catequizando, id_nivel, id_catequista, intento=1, aprobado=False):
    db = get_db_connection()
    progreso = {
        "_id": _get_next_id('progresos'), 
        "aprobado": bool(aprobado),  
        "fecha_fin": datetime.datetime.now(datetime.timezone.utc) if aprobado else None, 
        "certificado_emitido": False, 
        "intento": int(intento), 
        "nivel_ref": int(id_nivel) if id_nivel else None, 
        "catequista_aprobador_ref": int(id_catequista) if id_catequista else None, 
        "autorizacion": None
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"progresos": progreso}})


def actualizar_progreso(id_catequizando, id_progreso, datos_actualizacion):
    db = get_db_connection()
    update_fields = {}
    
    if datos_actualizacion.get('aprobado') is True:
        progreso_actual = db.catequizandos.find_one(
            {"_id": int(id_catequizando), "progresos._id": int(id_progreso)},
            {"progresos.$": 1}
        )
        if progreso_actual and progreso_actual['progresos'][0].get('fecha_fin') is None:
            datos_actualizacion['fecha_fin'] = datetime.datetime.now(datetime.timezone.utc)

    for key, value in datos_actualizacion.items():
        update_key = f"progresos.$[elem].{key}"
        if key == "fecha_fin":
            fecha_dt = _parse_date_from_string(value)
            if fecha_dt:
                update_fields[update_key] = fecha_dt
            else: 
                update_fields["$unset"] = {update_key: ""}
        elif key in ["nivel_ref", "catequista_aprobador_ref"]:
            update_fields[update_key] = int(value) if value else None
        elif key == "intento":
            update_fields[update_key] = int(value) if value else 1
        elif key == "aprobado":
            update_fields[update_key] = bool(value)
    set_data = {k: v for k, v in update_fields.items() if k != "$unset"}
    unset_data = update_fields.get("$unset", {})
    
    update_query = {}
    if set_data:
        update_query["$set"] = set_data
    if unset_data:
        update_query["$unset"] = unset_data

    if not update_query:
        return

    db.catequizandos.update_one(
        {"_id": int(id_catequizando)},
        update_query,
        array_filters=[{"elem._id": int(id_progreso)}]
    )

def eliminar_progreso(id_catequizando, id_progreso):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"progresos": {"_id": int(id_progreso)}}})

# ===============================================
# === GESTIÓN DE ASISTENCIAS
# ===============================================

def registrar_asistencia(id_catequizando, fecha_str, estado, id_nivel, id_grupo, id_catequista):
    db = get_db_connection()
    asistencia = {
        "_id": _get_next_id('asistencias'), "fecha": _parse_date_from_string(fecha_str), "estado": estado,
        "nivel_ref": int(id_nivel) if id_nivel else None, "grupo_ref": int(id_grupo) if id_grupo else None, 
        "catequista_ref": int(id_catequista) if id_catequista else None
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"asistencias": asistencia}})

def actualizar_asistencia(id_catequizando, id_asistencia, datos_actualizacion):
    db = get_db_connection()
    update_fields = {}
    for key, value in datos_actualizacion.items():
        if key == "fecha": update_fields[f"asistencias.$[elem].{key}"] = _parse_date_from_string(value)
        elif key in ["nivel_ref", "grupo_ref", "catequista_ref"]: update_fields[f"asistencias.$[elem].{key}"] = int(value) if value else None
        else: update_fields[f"asistencias.$[elem].{key}"] = value

    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$set": update_fields}, array_filters=[{"elem._id": int(id_asistencia)}])

def eliminar_asistencia(id_catequizando, id_asistencia):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"asistencias": {"_id": int(id_asistencia)}}})

# ===============================================
# === GESTIÓN DE SESIONES ESPECIALES
# ===============================================

def agregar_sesion_especial(id_catequizando, tipo_sesion, observaciones, id_autorizador, fecha_sesion_str):
    db = get_db_connection()
    sesion = {
        "_id": _get_next_id('sesiones_especiales'), 
        "tipo_sesion": tipo_sesion, 
        "observaciones": observaciones,
        # ¡CAMBIO! Usamos la fecha del formulario. Si no se provee, usamos la actual.
        "fecha": _parse_date_from_string(fecha_sesion_str) or datetime.datetime.now(datetime.timezone.utc),
        "autorizado_por_ref": int(id_autorizador) if id_autorizador else None
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"sesiones_especiales": sesion}})

def actualizar_sesion_especial(id_catequizando, id_sesion, datos_actualizacion):
    db = get_db_connection()
    update_fields = {}
    for key, value in datos_actualizacion.items():
        if key == "fecha": 
            update_fields[f"sesiones_especiales.$[elem].{key}"] = _parse_date_from_string(value)
        elif key == "autorizado_por_ref": 
            update_fields[f"sesiones_especiales.$[elem].{key}"] = int(value) if value else None
        else: 
            update_fields[f"sesiones_especiales.$[elem].{key}"] = value

    db.catequizandos.update_one(
        {"_id": int(id_catequizando)}, 
        {"$set": update_fields}, 
        array_filters=[{"elem._id": int(id_sesion)}]
    )

def eliminar_sesion_especial(id_catequizando, id_sesion):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"sesiones_especiales": {"_id": int(id_sesion)}}})

# ===============================================
# === GESTIÓN DE SACRAMENTOS
# ===============================================

def registrar_sacramento(id_catequizando, datos_sacramento):
    db = get_db_connection()
    sacramento = {
        "_id": _get_next_id('sacramentos'), "estado": "R", # Registrado
        "lugar": datos_sacramento.get("lugar"), "fecha_sacramento": _parse_date_from_string(datos_sacramento.get("fecha_sacramento")),
        "observaciones": datos_sacramento.get("observaciones"),
        "tipo_sacramento_ref": int(datos_sacramento.get("tipo_sacramento_ref")) if datos_sacramento.get("tipo_sacramento_ref") else None,
        "padre_ref": int(datos_sacramento.get("padre_ref")) if datos_sacramento.get("padre_ref") else None,
        "madre_ref": int(datos_sacramento.get("madre_ref")) if datos_sacramento.get("madre_ref") else None,
        "padrino_ref": int(datos_sacramento.get("padrino_ref")) if datos_sacramento.get("padrino_ref") else None,
        "madrina_ref": int(datos_sacramento.get("madrina_ref")) if datos_sacramento.get("madrina_ref") else None,
    }
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$push": {"sacramentos": sacramento}})

def actualizar_sacramento(id_catequizando, id_sacramento, datos_actualizacion):
    db = get_db_connection()
    update_fields = {}
    campos_ref = ['tipo_sacramento_ref', 'padre_ref', 'madre_ref', 'padrino_ref', 'madrina_ref']
    for key, value in datos_actualizacion.items():
        if key == "fecha_sacramento": update_fields[f"sacramentos.$[elem].{key}"] = _parse_date_from_string(value)
        elif key in campos_ref: update_fields[f"sacramentos.$[elem].{key}"] = int(value) if value and str(value).isdigit() else None
        else: update_fields[f"sacramentos.$[elem].{key}"] = value

    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$set": update_fields}, array_filters=[{"elem._id": int(id_sacramento)}])

def eliminar_sacramento(id_catequizando, id_sacramento):
    db = get_db_connection()
    db.catequizandos.update_one({"_id": int(id_catequizando)}, {"$pull": {"sacramentos": {"_id": int(id_sacramento)}}})
    
# ===============================================
# === GESTIÓN DE HISTORIAL PARROQUIAL (INTERNO)
# ===============================================

def agregar_a_historial_parroquial(id_catequizando, fecha_inicio, id_parroquia):
    db = get_db_connection()
    id_parroquia_num = int(id_parroquia)
    historial_entry = {
        "fecha_inicio": fecha_inicio, 
        "fecha_fin": None, 
        "parroquia_ref": id_parroquia_num
    }
    db.catequizandos.update_one(
        {"_id": int(id_catequizando)}, 
        {"$push": {"historial_parroquial": historial_entry}}
    )
    
def finalizar_historial_actual(id_catequizando, fecha_fin):
    db = get_db_connection()
    db.catequizandos.update_one(
        {"_id": int(id_catequizando), "historial_parroquial.fecha_fin": None}, 
        {"$set": {"historial_parroquial.$.fecha_fin": fecha_fin}}
    )
    
def obtener_datos_para_certificado(id_catequizando, id_progreso):
    db = get_db_connection()
    pipeline = [
        {"$match": {"_id": int(id_catequizando)}},
        {"$unwind": "$progresos"},
        {"$match": {"progresos._id": int(id_progreso), "progresos.aprobado": True}},
        {"$lookup": {
            "from": "parroquias", "localField": "parroquia_ref",
            "foreignField": "_id", "as": "parroquia_info"
        }},
        {"$lookup": {
            "from": "niveles_catequesis", "localField": "progresos.nivel_ref",
            "foreignField": "_id", "as": "nivel_info"
        }},
        {"$lookup": {
            "from": "catequistas", "localField": "progresos.catequista_aprobador_ref",
            "foreignField": "_id", "as": "catequista_info"
        }},
        {"$project": {
            "_id": 0,
            "catequizando_nombre_completo": {"$concat": ["$nombre", " ", "$apellido"]},
            "parroquia_nombre": {"$arrayElemAt": ["$parroquia_info.nombre", 0]},
            "nivel_nombre": {"$arrayElemAt": ["$nivel_info.nombre", 0]},
            "fecha_aprobacion": "$progresos.fecha_fin",
            "catequista_aprobador_nombre": {
                "$concat": [
                    {"$arrayElemAt": ["$catequista_info.nombre", 0]},
                    " ",
                    {"$arrayElemAt": ["$catequista_info.apellido", 0]}
                ]
            }
        }}
    ]
    
    resultado = list(db.catequizandos.aggregate(pipeline))
    return resultado[0] if resultado else None