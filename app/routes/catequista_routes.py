from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.catequista_service import *

catequista_bp = Blueprint('catequista', __name__, url_prefix='/catequistas')

@catequista_bp.before_request
def solo_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@catequista_bp.route('/')
def index():
    lista = obtener_catequistas()
    return render_template('catequista/index.html', catequistas=lista)

@catequista_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_catequista(
            request.form['telefono'],
            request.form['apellido'],
            request.form['nombre'],
            request.form['correo'],
            request.form['rol']
        )
        return redirect(url_for('catequista.index'))
    return render_template('catequista/insertar.html')

@catequista_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_catequista(
            id,
            request.form['telefono'],
            request.form['apellido'],
            request.form['nombre'],
            request.form['correo'],
            request.form['rol']
        )
        return redirect(url_for('catequista.index'))
    catequista = obtener_catequista_por_id(id)
    return render_template('catequista/actualizar.html', catequista=catequista)

@catequista_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_catequista(id)
        return redirect(url_for('catequista.index'))
    return render_template('catequista/eliminar.html', id=id)
