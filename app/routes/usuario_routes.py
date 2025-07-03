from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.usuario_service import *

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
        
        if not all([nombre, contrasena, rol]):
            flash("Todos los campos son obligatorios.", "danger")
            return render_template('usuario/insertar.html')

        resultado = crear_usuario_service(nombre, contrasena, rol)
        
        if resultado:
            flash(f"Usuario '{nombre}' creado exitosamente.", "success")
            return redirect(url_for('usuario.index'))
        else:
            flash(f"El nombre de usuario '{nombre}' ya existe. Por favor, elige otro.", "danger")
            return render_template('usuario/insertar.html', nombre=nombre, rol=rol)
            
    return render_template('usuario/insertar.html')

@usuario_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if session.get('usuario_id') == id:
        flash("Para editar tu propia cuenta, usa la página de 'Perfil'.", "info")

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        rol = request.form.get('rol')
        nueva_contrasena = request.form.get('contrasena') or None
        actualizar_usuario(id, nombre, rol, nueva_contrasena)
        
        flash("Usuario actualizado exitosamente.", "success")
        return redirect(url_for('usuario.index'))
    usuario = obtener_usuario_por_id_service(id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('usuario.index'))
        
    return render_template('usuario/actualizar.html', usuario=usuario)

@usuario_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_usuario(id)
    flash("Usuario eliminado exitosamente.", "info")
    return redirect(url_for('usuario.index'))


@usuario_bp.route('/confirmar-eliminar/<int:id>/')
def confirmar_eliminar(id):
    if session.get('usuario_id')==id:
        flash("No puedes eliminar tu propia cuenta de administrador.", "danger")
        return redirect(url_for('usuario.index'))

    usuario = obtener_usuario_por_id_service(id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('usuario.index'))
    return render_template('usuario/eliminar.html', usuario=usuario)

@usuario_bp.route('/<int:id>/notificaciones')
def ver_notificaciones(id):
    usuario = obtener_usuario_por_id_service(id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for('usuario.index'))
    
    notificaciones = sorted(
        usuario.get('notificaciones', []), 
        key=lambda n: n['fecha_recepcion'], 
        reverse=True
    )
    
    return render_template('usuario/notificaciones.html', usuario=usuario, notificaciones=notificaciones)

@usuario_bp.route('/<int:id>/agregar_notificacion', methods=['POST'])
def agregar_notificacion(id):
    tipo = request.form.get('tipo_notificacion')
    mensaje = request.form.get('mensaje')

    if not tipo or not mensaje:
        flash("El tipo y el mensaje de la notificación son obligatorios.", "warning")
        return redirect(url_for('usuario.ver_notificaciones', id=id))

    agregar_notificacion_a_usuario(id, tipo, mensaje)
    flash("Notificación enviada exitosamente.", "success")
    return redirect(url_for('usuario.ver_notificaciones', id=id))

@usuario_bp.route('/<int:id_usuario>/eliminar_notificacion/<int:id_notificacion>', methods=['POST'])
def eliminar_notificacion(id_usuario, id_notificacion):
    eliminar_notificacion_de_usuario(id_usuario, id_notificacion)
    flash("Notificación eliminada.", "info")
    return redirect(url_for('usuario.ver_notificaciones', id=id_usuario))