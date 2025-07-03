from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.tipo_sacramento_service import (
    crear_tipo_sacramento,
    obtener_tipos_sacramento,
    obtener_tipo_sacramento_por_id,
    actualizar_tipo_sacramento,
    eliminar_tipo_sacramento
)

tiposacramento_bp = Blueprint('tiposacramento', __name__, url_prefix='/tipos_sacramento')

@tiposacramento_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado.", "warning")
        return redirect(url_for('home'))


@tiposacramento_bp.route('/')
def index():
    lista_tipos = obtener_tipos_sacramento()
    return render_template('tipo_sacramento/index.html', tipos=lista_tipos)

@tiposacramento_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            crear_tipo_sacramento(nombre)
            flash("Tipo de sacramento creado exitosamente.", "success")
        else:
            flash("El nombre es un campo requerido.", "danger")
        return redirect(url_for('tiposacramento.index'))
    
    return render_template('tipo_sacramento/insertar.html')

@tiposacramento_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    tipo = obtener_tipo_sacramento_por_id(id)
    if not tipo:
        flash("Tipo de sacramento no encontrado.", "danger")
        return redirect(url_for('tiposacramento.index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        if nombre:
            actualizar_tipo_sacramento(id, nombre)
            flash("Tipo de sacramento actualizado exitosamente.", "success")
        else:
            flash("El nombre no puede estar vacío.", "danger")
        return redirect(url_for('tiposacramento.index'))

    return render_template('tipo_sacramento/actualizar.html', tipo=tipo)

@tiposacramento_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    tipo = obtener_tipo_sacramento_por_id(id)
    if not tipo:
        flash("Tipo de sacramento no encontrado.", "danger")
        return redirect(url_for('tiposacramento.index'))
    return render_template('tipo_sacramento/eliminar.html', tipo=tipo)

@tiposacramento_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    exito = eliminar_tipo_sacramento(id)
    if exito:
        flash("Tipo de sacramento eliminado permanentemente.", "info")
    else:
        flash("Error al eliminar el tipo de sacramento.", "danger")
    return redirect(url_for('tiposacramento.index'))