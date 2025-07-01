# app/routes/usuario_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.usuario_service import (
    crear_usuario_service,
    obtener_usuarios_service,
    obtener_usuario_por_id_service,
    actualizar_usuario_service,
    eliminar_usuario_service
)

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuarios')


@usuario_bp.route('/')
def index():
    usuarios = obtener_usuarios_service()
    return render_template('usuario/index.html', usuarios=usuarios)

@usuario_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol')
        
        # Validaciones básicas
        if not all([nombre, contrasena, rol]):
            flash("Todos los campos son obligatorios.", "danger")
            return render_template('usuario/insertar.html')

        resultado = crear_usuario_service(nombre, contrasena, rol)
        
        if resultado:
            flash(f"Usuario '{nombre}' creado exitosamente.", "success")
            return redirect(url_for('usuario.index'))
        else:
            flash(f"El nombre de usuario '{nombre}' ya existe. Por favor, elige otro.", "danger")
            # Volvemos a renderizar el formulario para que el usuario pueda corregir
            return render_template('usuario/insertar.html', nombre=nombre, rol=rol)
            
    return render_template('usuario/insertar.html')

@usuario_bp.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    if session.get('usuario_id')==id:
        flash("No puedes eliminar tu propia cuenta de administrador.", "danger")
        return redirect(url_for('usuario.index'))

    eliminado = eliminar_usuario_service(id)
    if eliminado:
        flash("Usuario eliminado exitosamente.", "info")
    else:
        flash("No se pudo eliminar al usuario.", "danger")

    return redirect(url_for('usuario.index'))


@usuario_bp.route('/confirmar-eliminar/<id>')
def confirmar_eliminar(id):
    if session.get('usuario_id')==id:
        flash("No puedes eliminar tu propia cuenta de administrador.", "danger")
        return redirect(url_for('usuario.index'))

    usuario = obtener_usuario_por_id_service(id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('usuario.index'))
    return render_template('usuario/eliminar.html', usuario=usuario)