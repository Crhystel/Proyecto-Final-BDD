from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.usuario_service import *

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@usuario_bp.route('/')
def index():
    usuarios = obtener_usuarios()
    return render_template('usuario/index.html', usuarios=usuarios)

@usuario_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        rol = request.form['rol']
        crear_usuario(contrasena, nombre, rol)
        return redirect(url_for('usuario.index'))
    return render_template('usuario/insertar.html')

@usuario_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_usuario(id, request.form['contrasena'], request.form['nombre'], request.form['rol'])
        return redirect(url_for('usuario.index'))

    usuario = obtener_usuario_por_id(id)
    return render_template('usuario/actualizar.html', usuario=usuario)

@usuario_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_usuario(id)
        return redirect(url_for('usuario.index'))
    return render_template('usuario/eliminar.html', id=id)
