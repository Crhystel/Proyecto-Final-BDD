from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.grupo_catequesis_service import *
from app.services.parroquia_service import obtener_parroquias
from app.services.ciclo_catequistico_service import obtener_ciclos

grupo_bp = Blueprint('grupo', __name__, url_prefix='/grupos')

@grupo_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@grupo_bp.route('/')
def index():
    grupos = obtener_grupos()
    return render_template('grupo_catequesis/index.html', grupos=grupos)

@grupo_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_grupo(
            request.form['nombre'],
            request.form['id_parroquia'],
            request.form['id_ciclo']
        )
        return redirect(url_for('grupo.index'))

    parroquias = obtener_parroquias()
    ciclos = obtener_ciclos()
    return render_template('grupo_catequesis/insertar.html', parroquias=parroquias, ciclos=ciclos)

@grupo_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_grupo(
            id,
            request.form['nombre'],
            request.form['id_parroquia'],
            request.form['id_ciclo']
        )
        return redirect(url_for('grupo.index'))

    grupo = obtener_grupo_por_id(id)
    parroquias = obtener_parroquias()
    ciclos = obtener_ciclos()
    return render_template('grupo_catequesis/actualizar.html', grupo=grupo, parroquias=parroquias, ciclos=ciclos)

@grupo_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_grupo(id)
        return redirect(url_for('grupo.index'))
    return render_template('grupo_catequesis/eliminar.html', id=id)
