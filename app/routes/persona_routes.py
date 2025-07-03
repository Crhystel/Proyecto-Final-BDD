from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.persona_service import *

persona_bp = Blueprint('persona', __name__, url_prefix='/personas')

@persona_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado.", "warning")
        return redirect('/')

@persona_bp.route('/')
def index():
    personas = obtener_personas()
    tipos_map = {'P': 'Padre', 'M': 'Madre', 'D': 'Padrino', 'N': 'Madrina'}
    return render_template('persona/index.html', personas=personas, tipos_map=tipos_map)

@persona_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_persona(
            request.form['nombre'], request.form['apellido'],
            request.form['tipo_persona'], request.form.get('telefono'),
            request.form.get('correo')
        )
        flash("Persona creada exitosamente.", "success")
        return redirect(url_for('persona.index'))
    return render_template('persona/insertar.html')

@persona_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    persona = obtener_persona_por_id(id)
    if not persona:
        flash("Persona no encontrada.", "danger")
        return redirect(url_for('persona.index'))

    if request.method == 'POST':
        actualizar_persona(
            id, request.form['nombre'], request.form['apellido'],
            request.form['tipo_persona'], request.form.get('telefono'),
            request.form.get('correo')
        )
        flash("Datos de la persona actualizados.", "success")
        return redirect(url_for('persona.index'))

    return render_template('persona/actualizar.html', persona=persona)

@persona_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    persona = obtener_persona_por_id(id)
    if not persona:
        flash("Persona no encontrada.", "danger")
        return redirect(url_for('persona.index'))
    return render_template('persona/eliminar.html', persona=persona)

@persona_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_persona(id)
    flash("Persona eliminada permanentemente.", "info")
    return redirect(url_for('persona.index'))