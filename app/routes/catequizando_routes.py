from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.catequizando_service import *
from app.services.parroquia_service import obtener_parroquias

catequizando_bp = Blueprint('catequizando', __name__, url_prefix='/catequizandos')

@catequizando_bp.before_request
def solo_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@catequizando_bp.route('/')
def index():
    lista = obtener_catequizandos()
    return render_template('catequizando/index.html', catequizandos=lista)

@catequizando_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_catequizando(
            request.form['apellido'],
            request.form['nombre'],
            request.form['fecha_nacimiento'],
            request.form['documento_identidad'],
            request.form['fecha_registro'],
            request.form['bautizado'],
            request.form['id_parroquia'] or None
        )
        return redirect(url_for('catequizando.index'))

    parroquias = obtener_parroquias() 
    return render_template('catequizando/insertar.html', parroquias=parroquias)

@catequizando_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_catequizando(
            id,
            request.form['apellido'],
            request.form['nombre'],
            request.form['fecha_nacimiento'],
            request.form['documento_identidad'],
            request.form['fecha_registro'],
            request.form['bautizado'],
            request.form['id_parroquia'] or None
        )
        return redirect(url_for('catequizando.index'))
    c = obtener_catequizando_por_id(id)
    return render_template('catequizando/actualizar.html', catequizando=c)

@catequizando_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_catequizando(id)
        return redirect(url_for('catequizando.index'))
    return render_template('catequizando/eliminar.html', id=id)
