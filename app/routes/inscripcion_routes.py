from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.inscripcion_service import *
from app.services.catequizando_service import obtener_catequizandos
from app.services.grupo_catequesis_service import obtener_grupos

inscripcion_bp = Blueprint('inscripcion', __name__, url_prefix='/inscripciones')

@inscripcion_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@inscripcion_bp.route('/')
def index():
    inscripciones = obtener_inscripciones()
    return render_template('inscripcion/index.html', inscripciones=inscripciones)

@inscripcion_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_inscripcion(
            request.form['observaciones'],
            request.form['estado_pago'],
            request.form['fecha_inscripcion'],
            request.form['id_catequizando'],
            request.form['registrado_por'],
            request.form['id_grupo_catequesis']
        )
        return redirect(url_for('inscripcion.index'))

    catequizandos = obtener_catequizandos()
    grupos = obtener_grupos()
    catequistas = obtener_catequistas()
    return render_template('inscripcion/insertar.html', catequizandos=catequizandos, grupos=grupos, catequistas=catequistas)

@inscripcion_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_inscripcion(
            id,
            request.form['observaciones'],
            request.form['estado_pago'],
            request.form['fecha_inscripcion'],
            request.form['id_catequizando'],
            request.form['registrado_por'],
            request.form['id_grupo_catequesis']
        )
        return redirect(url_for('inscripcion.index'))

    inscripcion = obtener_inscripcion_por_id(id)
    catequizandos = obtener_catequizandos()
    grupos = obtener_grupos()
    catequistas = obtener_catequistas()
    return render_template('inscripcion/actualizar.html', inscripcion=inscripcion, catequizandos=catequizandos, grupos=grupos, catequistas=catequistas)

@inscripcion_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_inscripcion(id)
        return redirect(url_for('inscripcion.index'))
    return render_template('inscripcion/eliminar.html', id=id)
