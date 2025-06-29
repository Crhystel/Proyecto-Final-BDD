from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.ciclo_catequistico_service import *
from app.services.nivelcatequesis_service import obtener_niveles

ciclo_bp = Blueprint('ciclo', __name__, url_prefix='/ciclos')

@ciclo_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@ciclo_bp.route('/')
def index():
    ciclos = obtener_ciclos()
    return render_template('ciclo_catequistico/index.html', ciclos=ciclos)

@ciclo_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_ciclo(
            request.form['nombre'],
            request.form['fecha_inicio'],
            request.form['fecha_fin'],
            request.form['id_nivel']
        )
        return redirect(url_for('ciclo.index'))
    
    niveles = obtener_niveles()
    return render_template('ciclo_catequistico/insertar.html', niveles=niveles)

@ciclo_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_ciclo(
            id,
            request.form['nombre'],
            request.form['fecha_inicio'],
            request.form['fecha_fin'],
            request.form['id_nivel']
        )
        return redirect(url_for('ciclo.index'))
    
    ciclo = obtener_ciclo_por_id(id)
    niveles = obtener_niveles()
    return render_template('ciclo_catequistico/actualizar.html', ciclo=ciclo, niveles=niveles)

@ciclo_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_ciclo(id)
        return redirect(url_for('ciclo.index'))
    return render_template('ciclo_catequistico/eliminar.html', id=id)
