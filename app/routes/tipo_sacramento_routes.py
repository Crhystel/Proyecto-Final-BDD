from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.tipo_sacramento_service import *

tipo_sacramento_bp = Blueprint('tipo_sacramento', __name__, url_prefix='/tipos_sacramento')

@tipo_sacramento_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@tipo_sacramento_bp.route('/')
def index():
    tipos = obtener_tipos_sacramento()
    return render_template('tipo_sacramento/index.html', tipos=tipos)

@tipo_sacramento_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_tipo_sacramento(request.form['nombre'])
        return redirect(url_for('tipo_sacramento.index'))
    return render_template('tipo_sacramento/insertar.html')

@tipo_sacramento_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_tipo_sacramento(id, request.form['nombre'])
        return redirect(url_for('tipo_sacramento.index'))

    tipo = obtener_tipo_sacramento_por_id(id)
    return render_template('tipo_sacramento/actualizar.html', tipo=tipo)

@tipo_sacramento_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_tipo_sacramento(id)
        return redirect(url_for('tipo_sacramento.index'))
    return render_template('tipo_sacramento/eliminar.html', id=id)
