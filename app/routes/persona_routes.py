from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.persona_service import *

persona_bp = Blueprint('persona', __name__, url_prefix='/personas')

@persona_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@persona_bp.route('/')
def index():
    personas = obtener_personas()
    return render_template('persona/index.html', personas=personas)

@persona_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_persona(
            request.form['nombre'],
            request.form['apellido'],
            request.form['tipo_persona'],
            request.form['telefono'],
            request.form['correo']
        )
        return redirect(url_for('persona.index'))
    return render_template('persona/insertar.html')

@persona_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_persona(
            id,
            request.form['nombre'],
            request.form['apellido'],
            request.form['tipo_persona'],
            request.form['telefono'],
            request.form['correo']
        )
        return redirect(url_for('persona.index'))

    persona = obtener_persona_por_id(id)
    return render_template('persona/actualizar.html', persona=persona)

@persona_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_persona(id)
        return redirect(url_for('persona.index'))
    return render_template('persona/eliminar.html', id=id)
