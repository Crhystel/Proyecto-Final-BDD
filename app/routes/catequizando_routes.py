# app/routes/catequizando_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import datetime

# --- Importaciones de Servicios ---
# Servicio principal
from app.services.catequizando_service import *
from app.services.parroquia_service import *
from app.services.catequista_service import *
from app.services.nivelcatequesis_service import obtener_niveles
from app.services.tipo_sacramento_service import obtener_tipos_sacramento
from app.services.persona_service import obtener_personas # Para padres y padrinos
from app.services.tipo_documento_service import obtener_tipos_documento # Para documentos

catequizando_bp = Blueprint("catequizando", __name__, url_prefix='/catequizandos')

@catequizando_bp.before_request
def solo_admin():
    if 'rol' not in session or session["rol"] != "A":
        flash("Acceso no autorizado", "warning")
        return redirect("/")

# ===============================================
# === CRUD BÁSICO DE CATEQUIZANDO
# ===============================================

@catequizando_bp.route("/")
def index():
    lista_catequizandos = obtener_catequizandos()
    return render_template("catequizando/index.html", catequizandos=lista_catequizandos)

@catequizando_bp.route('/insertar', methods=["GET", "POST"])
def insertar():
    if request.method == "POST":
        id_nuevo = crear_catequizando(
            nombre=request.form["nombre"], apellido=request.form["apellido"],
            fecha_nacimiento=request.form["fecha_nacimiento"], doc_identidad=request.form["documento_identidad"],
            fecha_registro=request.form["fecha_registro"], id_parroquia=request.form.get("id_parroquia")
        )
        flash("Catequizando creado. Ahora puede gestionar sus detalles.", "success")
        return redirect(url_for("catequizando.detalles", id=id_nuevo))
    
    parroquias = obtener_parroquias()
    return render_template("catequizando/insertar.html", parroquias=parroquias)

@catequizando_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_catequizando(id)
    flash("Catequizando eliminado permanentemente.", "info")
    return redirect(url_for('catequizando.index'))

@catequizando_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    catequizando = obtener_catequizando_por_id(id)
    if not catequizando:
        flash("Catequizando no encontrado.", "danger")
        return redirect(url_for('catequizando.index'))
    return render_template('catequizando/eliminar.html', catequizando=catequizando)


@catequizando_bp.route('/<int:id>/detalles')
def detalles(id):
    catequizando = obtener_catequizando_por_id(id)
    if not catequizando:
        flash("Catequizando no encontrado.", "danger")
        return redirect(url_for('catequizando.index'))
    
    # Pasamos todos los datos necesarios para los formularios
    context = {
        "catequizando": catequizando,
        "todas_las_parroquias": obtener_parroquias(),
        "todos_los_grupos": obtener_todos_los_grupos(),
        "todos_los_niveles": obtener_niveles(),
        "todos_los_catequistas": obtener_catequistas(),
        "todos_los_sacramentos": obtener_tipos_sacramento(),
        "todos_los_tipos_doc": obtener_tipos_documento(),
        "todas_las_personas": obtener_personas() # Para padres/padrinos
    }
    return render_template('catequizando/detalles.html', **context)



# --- 1. Datos Principales y Ficha ---
@catequizando_bp.route('/<int:id>/actualizar-principal', methods=['POST'])
def actualizar_datos_principales(id):
    datos = {
        "nombre": request.form.get("nombre"), "apellido": request.form.get("apellido"),
        "fecha_nacimiento": datetime.datetime.fromisoformat(request.form.get("fecha_nacimiento")),
        "documento_identidad": request.form.get("documento_identidad"),
        "fecha_registro": datetime.datetime.fromisoformat(request.form.get("fecha_registro")),
        "parroquia_ref": int(request.form.get("parroquia_ref")),
        "tiene_bautismo": "tiene_bautismo" in request.form,
        "lugar_bautismo": request.form.get("lugar_bautismo"),
        "fecha_bautismo": datetime.datetime.fromisoformat(request.form.get("fecha_bautismo")) if request.form.get("fecha_bautismo") else None
    }
    actualizar_catequizando_principal(id, datos)
    flash("Datos principales actualizados.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

# --- 2. Documentos ---
@catequizando_bp.route('/<int:id>/agregar-documento', methods=['POST'])
def agregar_un_documento(id):
    ruta_archivo = "ruta/ficticia/al/archivo.pdf" 
    agregar_documento(
        id_catequizando=id, ruta_archivo=ruta_archivo,
        tipo=request.form.get("tipo_documento"),
        descripcion=request.form.get("descripcion_documento")
    )
    flash("Documento añadido.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-documento/<int:id_documento>', methods=['POST'])
def eliminar_un_documento(id_catequizando, id_documento):
    eliminar_documento(id_catequizando, id_documento)
    flash("Documento eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id>/agregar-inscripcion', methods=['POST'])
def agregar_una_inscripcion(id):
    agregar_inscripcion(
        id_catequizando=id, observaciones=request.form.get("observaciones_inscripcion"),
        estado_pago=request.form.get("estado_pago"), id_grupo=request.form.get("id_grupo"),
        id_registrador=session.get('usuario_id')
    )
    flash("Inscripción añadida.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-inscripcion/<int:id_inscripcion>', methods=['POST'])
def eliminar_una_inscripcion(id_catequizando, id_inscripcion):
    eliminar_inscripcion(id_catequizando, id_inscripcion)
    flash("Inscripción eliminada.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/inscripcion/<int:id_inscripcion>/generar-certificado', methods=['POST'])
def generar_un_certificado(id_catequizando, id_inscripcion):
    contenido = request.form.get("contenido_certificado", f"Certificado para la inscripción #{id_inscripcion}")
    generar_certificado_para_inscripcion(id_catequizando, id_inscripcion, contenido)
    flash("Certificado generado.", "success")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/inscripcion/<int:id_inscripcion>/eliminar-certificado', methods=['POST'])
def eliminar_un_certificado(id_catequizando, id_inscripcion):
    eliminar_certificado_de_inscripcion(id_catequizando, id_inscripcion)
    flash("Certificado eliminado de la inscripción.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# --- 4. Progresos ---
@catequizando_bp.route('/<int:id>/agregar-progreso', methods=['POST'])
def agregar_un_progreso(id):
    agregar_progreso(
        id_catequizando=id, id_nivel=request.form.get("id_nivel_progreso"),
        id_catequista=request.form.get("id_catequista_aprobador")
    )
    flash("Progreso de nivel añadido.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-progreso/<int:id_progreso>', methods=['POST'])
def eliminar_un_progreso(id_catequizando, id_progreso):
    eliminar_progreso(id_catequizando, id_progreso)
    flash("Progreso eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

# --- 5. Asistencias ---
@catequizando_bp.route('/<int:id>/registrar-asistencia', methods=['POST'])
def registrar_una_asistencia(id):
    registrar_asistencia(
        id_catequizando=id, fecha=request.form.get("fecha_asistencia"),
        estado=request.form.get("estado_asistencia"), id_nivel=request.form.get("id_nivel_asistencia"),
        id_grupo=request.form.get("id_grupo_asistencia"), id_catequista=session.get('usuario_id') # O un select
    )
    flash("Asistencia registrada.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

# --- 6. Sesiones Especiales ---
@catequizando_bp.route('/<int:id>/agregar-sesion', methods=['POST'])
def agregar_una_sesion(id):
    agregar_sesion_especial(
        id_catequizando=id, tipo_sesion=request.form.get("tipo_sesion"),
        observaciones=request.form.get("observaciones_sesion"),
        id_autorizador=session.get('usuario_id')
    )
    flash("Sesión especial añadida.", "success")
    return redirect(url_for('catequizando.detalles', id=id))

# --- 7. Sacramentos ---
@catequizando_bp.route('/<int:id>/registrar-sacramento', methods=['POST'])
def registrar_un_sacramento(id):
    datos_sacramento = {
        "lugar": request.form.get("lugar_sacramento"),
        "fecha_sacramento": datetime.datetime.fromisoformat(request.form.get("fecha_sacramento")),
        "observaciones": request.form.get("observaciones_sacramento"),
        "tipo_sacramento_ref": request.form.get("id_tipo_sacramento"),
        "padre_ref": request.form.get("id_padre"),
        "madre_ref": request.form.get("id_madre"),
        "padrino_ref": request.form.get("id_padrino"),
        "madrina_ref": request.form.get("id_madrina")
    }
    registrar_sacramento(id, datos_sacramento)
    flash("Sacramento registrado.", "success")
    return redirect(url_for('catequizando.detalles', id=id))
@catequizando_bp.route('/<int:id_catequizando>/eliminar-sacramento/<int:id_sacramento>', methods=['POST'])
def eliminar_un_sacramento(id_catequizando, id_sacramento):
    eliminar_sacramento(id_catequizando, id_sacramento)
    flash("Sacramento eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-asistencia/<int:id_asistencia>', methods=['POST'])
def eliminar_una_asistencia(id_catequizando, id_asistencia):
    eliminar_asistencia(id_catequizando, id_asistencia)
    flash("Registro de asistencia eliminado.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

@catequizando_bp.route('/<int:id_catequizando>/eliminar-sesion/<int:id_sesion>', methods=['POST'])
def eliminar_una_sesion(id_catequizando, id_sesion):
    eliminar_sesion_especial(id_catequizando, id_sesion)
    flash("Sesión especial eliminada.", "info")
    return redirect(url_for('catequizando.detalles', id=id_catequizando))

