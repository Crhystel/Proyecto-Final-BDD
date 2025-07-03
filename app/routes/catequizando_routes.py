from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import datetime
from collections import defaultdict

# Importa los servicios necesarios
from app.services.parroquia_service import *
from app.services.catequista_service import *
from app.services.catequizando_service import *
from app.services.nivelcatequesis_service import obtener_niveles
from app.services.tipo_sacramento_service import obtener_tipos_sacramento
from app.services.persona_service import obtener_personas
from app.services.tipo_documento_service import obtener_tipos_documento

catequizando_bp = Blueprint("catequizando", __name__, url_prefix='/catequizandos')

@catequizando_bp.before_request
def solo_admin():
    if 'rol' not in session or session["rol"] != "A":
        flash("Acceso no autorizado", "warning")
        return redirect("/")

# ===============================================
# === 1. GESTIÓN GENERAL DEL CATEQUIZANDO
# ===============================================

@catequizando_bp.route("/")
def index():
    lista_catequizandos = obtener_catequizandos()
    return render_template("catequizando/index.html", catequizandos=lista_catequizandos)

@catequizando_bp.route('/insertar', methods=["GET", "POST"])
def insertar():
    if request.method == "POST":
        id_nuevo = crear_catequizando(
            nombre=request.form.get("nombre"), apellido=request.form.get("apellido"),
            doc_identidad=request.form.get("documento_identidad"), fecha_nacimiento=request.form.get("fecha_nacimiento"), 
            fecha_registro=request.form.get("fecha_registro"), id_parroquia=request.form.get("id_parroquia"),
            tiene_bautismo="tiene_bautismo" in request.form,
            lugar_bautismo=request.form.get("lugar_bautismo"), fecha_bautismo=request.form.get("fecha_bautismo")
        )
        flash("Catequizando creado. Ahora puede gestionar sus detalles.", "success")
        return redirect(url_for("catequizando.detalles", id=id_nuevo))
    
    parroquias = obtener_parroquias()
    return render_template("catequizando/insertar.html", parroquias=parroquias, now=datetime.datetime.utcnow())

@catequizando_bp.route('/<int:id>/detalles')
def detalles(id):
    seccion_a_editar = request.args.get('editar', None)
    catequizando = obtener_catequizando_por_id(id)
    if not catequizando:
        flash("Catequizando no encontrado.", "danger")
        return redirect(url_for('catequizando.index'))

    id_parroquia_actual = catequizando.get('parroquia_ref')
    grupos_de_la_parroquia = []
    if id_parroquia_actual:
        grupos_de_la_parroquia = obtener_grupos_de_parroquia(id_parroquia_actual)
    context = {
        "catequizando": catequizando,
        "seccion_a_editar": seccion_a_editar,
        "todas_las_parroquias": obtener_parroquias(),
        "grupos_disponibles": grupos_de_la_parroquia, 
        "todos_los_catequistas": obtener_catequistas(),
        "todos_los_niveles": obtener_niveles(), 
        "todos_los_sacramentos": obtener_tipos_sacramento(),
        "todos_los_tipos_doc": obtener_tipos_documento(),
        "todas_las_personas": obtener_personas()
    }
    return render_template('catequizando/detalles.html', **context)

@catequizando_bp.route('/<int:id>/actualizar-principal', methods=['POST'])
def actualizar_datos_principales(id):
    datos = {
        "nombre": request.form.get("nombre"), "apellido": request.form.get("apellido"),
        "fecha_nacimiento": request.form.get("fecha_nacimiento"), "documento_identidad": request.form.get("documento_identidad"),
        "parroquia_ref": int(request.form.get("parroquia_ref")) if request.form.get("parroquia_ref") else None,
        "tiene_bautismo": "tiene_bautismo" in request.form,
        "lugar_bautismo": request.form.get("lugar_bautismo"), "fecha_bautismo": request.form.get('fecha_bautismo')
    }
    actualizar_catequizando_principal(id, datos)
    flash("Datos principales actualizados.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

@catequizando_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    catequizando = obtener_catequizando_por_id(id)
    return render_template('catequizando/eliminar.html', catequizando=catequizando)

@catequizando_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_catequizando(id)
    flash("Catequizando eliminado permanentemente.", "info")
    return redirect(url_for('catequizando.index'))

# ===============================================
# === 2. GESTIÓN DE DOCUMENTOS
# ===============================================

@catequizando_bp.route('/<int:id_catequizando>/agregar-documento', methods=['POST'])
def agregar_documento_route(id_catequizando):
    ruta_archivo = "ruta/ficticia/al/archivo.pdf" # Placeholder para la subida de archivos
    agregar_documento(id_catequizando, ruta_archivo, request.form.get("tipo_documento"), request.form.get("descripcion_documento"))
    flash("Documento añadido.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/actualizar-documentos', methods=['POST'])
def actualizar_multiples_documentos(id_catequizando):
    documentos_data = defaultdict(dict)
    for key, value in request.form.items():
        if '_' in key and key.rsplit('_', 1)[1].isdigit():
            campo, doc_id_str = key.rsplit('_', 1)
            documentos_data[int(doc_id_str)][campo] = value

    for doc_id, datos in documentos_data.items():
        actualizar_documento(id_catequizando, doc_id, datos)
    
    flash("Documentos actualizados.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-documento/<int:id_documento>', methods=['POST'])
def eliminar_documento_route(id_catequizando, id_documento):
    eliminar_documento(id_catequizando, id_documento)
    flash("Documento eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# ===============================================
# === 3. GESTIÓN DE INSCRIPCIONES Y CERTIFICADOS
# ===============================================

@catequizando_bp.route('/<int:id_catequizando>/agregar-inscripcion', methods=['POST'])
def agregar_inscripcion_route(id_catequizando):
    agregar_inscripcion(
        id_catequizando, 
        request.form.get("fecha_inscripcion"), 
        request.form.get("observaciones_inscripcion"),
        request.form.get("estado_pago"), 
        request.form.get("id_grupo"), 
        request.form.get("id_registrador") # <--- Ahora solo hay 6 argumentos
    )
    flash("Inscripción añadida.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/actualizar-inscripciones', methods=['POST'])
def actualizar_multiples_inscripciones(id_catequizando):
    inscripciones_data = defaultdict(dict)
    for key, value in request.form.items():
        if '_' in key and key.rsplit('_', 1)[1].isdigit():
            campo, insc_id_str = key.rsplit('_', 1)
            inscripciones_data[int(insc_id_str)][campo] = value

    for insc_id, datos in inscripciones_data.items():
        actualizar_inscripcion(id_catequizando, insc_id, datos)
    
    flash("Inscripciones actualizadas.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-inscripcion/<int:id_inscripcion>', methods=['POST'])
def eliminar_inscripcion_route(id_catequizando, id_inscripcion):
    eliminar_inscripcion(id_catequizando, id_inscripcion)
    flash("Inscripción eliminada.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/inscripcion/<int:id_inscripcion>/generar-certificado', methods=['POST'])
def generar_certificado_route(id_catequizando, id_inscripcion):
    contenido = request.form.get("contenido_certificado", f"Certificado para la inscripción #{id_inscripcion}")
    generar_certificado_para_inscripcion(id_catequizando, id_inscripcion, contenido)
    flash("Certificado generado.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/inscripcion/<int:id_inscripcion>/eliminar-certificado', methods=['POST'])
def eliminar_certificado_route(id_catequizando, id_inscripcion):
    eliminar_certificado_de_inscripcion(id_catequizando, id_inscripcion)
    flash("Certificado eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# ===============================================
# === 4. GESTIÓN DE PROGRESOS
# ===============================================

@catequizando_bp.route('/<int:id_catequizando>/agregar-progreso', methods=['POST'])
def agregar_progreso_route(id_catequizando):
    id_nivel = request.form.get("id_nivel_progreso")
    id_catequista = request.form.get("id_catequista_aprobador")
    intento = request.form.get("intento", 1)
    aprobado = 'aprobado' in request.form 
    agregar_progreso(
        id_catequizando=id_catequizando, 
        id_nivel=id_nivel, 
        id_catequista=id_catequista,
        intento=intento,
        aprobado=aprobado
    )
    flash("Progreso añadido.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/actualizar-progresos', methods=['POST'])
def actualizar_multiples_progresos(id_catequizando):
    progresos_data = defaultdict(dict)
    
    catequizando = obtener_catequizando_por_id(id_catequizando)
    ids_progresos_existentes = {str(p['_id']) for p in catequizando.get('progresos', [])}

    for key, value in request.form.items():
        if '_' in key and key.rsplit('_', 1)[1] in ids_progresos_existentes:
            campo, prog_id_str = key.rsplit('_', 1)
            progresos_data[prog_id_str][campo] = value
    for prog_id_str in ids_progresos_existentes:
        progresos_data[prog_id_str]['aprobado'] = f'aprobado_{prog_id_str}' in request.form

    for prog_id_str, datos in progresos_data.items():
        actualizar_progreso(id_catequizando, int(prog_id_str), datos)

    flash("Progresos actualizados.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-progreso/<int:id_progreso>', methods=['POST'])
def eliminar_progreso_route(id_catequizando, id_progreso):
    eliminar_progreso(id_catequizando, id_progreso)
    flash("Progreso eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# ===============================================
# === 5. GESTIÓN DE ASISTENCIAS
# ===============================================

@catequizando_bp.route('/<int:id_catequizando>/registrar-asistencia', methods=['POST'])
def registrar_asistencia_route(id_catequizando):
    registrar_asistencia(
        id_catequizando, 
        request.form.get("fecha_asistencia"), 
        request.form.get("estado_asistencia"),
        request.form.get("id_nivel_asistencia"),
        request.form.get("id_grupo_asistencia"),
        request.form.get("id_catequista") 
    )
    flash("Asistencia registrada.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/actualizar-asistencias', methods=['POST'])
def actualizar_multiples_asistencias(id_catequizando):
    asistencias_data = defaultdict(dict)
    for key, value in request.form.items():
        if '_' in key and key.rsplit('_', 1)[1].isdigit():
            campo, asis_id_str = key.rsplit('_', 1)
            asistencias_data[int(asis_id_str)][campo] = value

    for asis_id, datos in asistencias_data.items():
        actualizar_asistencia(id_catequizando, asis_id, datos)
    
    flash("Asistencias actualizadas.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-asistencia/<int:id_asistencia>', methods=['POST'])
def eliminar_asistencia_route(id_catequizando, id_asistencia):
    eliminar_asistencia(id_catequizando, id_asistencia)
    flash("Asistencia eliminada.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# ===============================================
# === 6. GESTIÓN DE SESIONES ESPECIALES
# ===============================================

@catequizando_bp.route('/<int:id_catequizando>/agregar-sesion', methods=['POST'])
def agregar_sesion_route(id_catequizando):
    # ¡CAMBIO! Recogemos los nuevos campos del formulario
    agregar_sesion_especial(
        id_catequizando, 
        request.form.get("tipo_sesion"), 
        request.form.get("observaciones_sesion"), 
        request.form.get("id_autorizador"), # El ID del catequista
        request.form.get("fecha_sesion")   # La nueva fecha
    )
    flash("Sesión especial añadida.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/actualizar-sesiones', methods=['POST'])
def actualizar_multiples_sesiones(id_catequizando):
    sesiones_data = defaultdict(dict)
    for key, value in request.form.items():
        if '_' in key and key.rsplit('_', 1)[1].isdigit():
            campo, sesion_id_str = key.rsplit('_', 1)
            sesiones_data[int(sesion_id_str)][campo] = value

    for sesion_id, datos in sesiones_data.items():
        actualizar_sesion_especial(id_catequizando, sesion_id, datos)
    
    flash("Sesiones especiales actualizadas.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-sesion/<int:id_sesion>', methods=['POST'])
def eliminar_sesion_route(id_catequizando, id_sesion):
    eliminar_sesion_especial(id_catequizando, id_sesion)
    flash("Sesión especial eliminada.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# ===============================================
# === 7. GESTIÓN DE SACRAMENTOS
# ===============================================

@catequizando_bp.route('/<int:id_catequizando>/registrar-sacramento', methods=['POST'])
def registrar_sacramento_route(id_catequizando):
    datos_sacramento = {k: v for k, v in request.form.items()}
    registrar_sacramento(id_catequizando, datos_sacramento)
    flash("Sacramento registrado.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/actualizar-sacramentos', methods=['POST'])
def actualizar_multiples_sacramentos(id_catequizando):
    sacramentos_data = defaultdict(dict)
    for key, value in request.form.items():
        if '_' in key and key.rsplit('_', 1)[1].isdigit():
            campo, sac_id_str = key.rsplit('_', 1)
            sacramentos_data[int(sac_id_str)][campo] = value

    for sac_id, datos in sacramentos_data.items():
        actualizar_sacramento(id_catequizando, sac_id, datos)
    
    flash("Sacramentos actualizados.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-sacramento/<int:id_sacramento>', methods=['POST'])
def eliminar_sacramento_route(id_catequizando, id_sacramento):
    eliminar_sacramento(id_catequizando, id_sacramento)
    flash("Sacramento eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/progreso/<int:id_progreso>/certificado')
def ver_certificado_progreso(id_catequizando, id_progreso):
    datos_certificado = obtener_datos_para_certificado(id_catequizando, id_progreso)
    
    if not datos_certificado:
        flash("No se pudo generar el certificado. Asegúrese de que el progreso esté aprobado.", "danger")
        return redirect(url_for('catequizando.detalles', id=id_catequizando))
    
    return render_template('certificado/progreso.html', datos=datos_certificado)