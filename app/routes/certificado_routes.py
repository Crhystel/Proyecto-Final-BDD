from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.certificado_service import *

certificado_bp = Blueprint('certificado', __name__, url_prefix='/certificados')

@certificado_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@certificado_bp.route('/')
def index():
    certificados = obtener_certificados()
    return render_template('certificado/index.html', certificados=certificados)

@certificado_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_certificado(
            request.form['contenido'],
            request.form['fecha_emision'],
            request.form['id_inscripcion']
        )
        return redirect(url_for('certificado.index'))

    inscripciones = obtener_inscripciones()
    return render_template('certificado/insertar.html', inscripciones=inscripciones)

@certificado_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_certificado(
            id,
            request.form['contenido'],
            request.form['fecha_emision'],
            request.form['id_inscripcion']
        )
        return redirect(url_for('certificado.index'))

    certificado = obtener_certificado_por_id(id)
    inscripciones = obtener_inscripciones()
    return render_template('certificado/actualizar.html', certificado=certificado, inscripciones=inscripciones)

@certificado_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_certificado(id)
        return redirect(url_for('certificado.index'))

    return render_template('certificado/eliminar.html', id=id)
