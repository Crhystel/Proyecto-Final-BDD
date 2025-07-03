from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# Importamos todas las funciones del servicio
from app.services.tipo_documento_service import (
    crear_tipo_documento,
    obtener_tipos_documento,
    obtener_tipo_documento_por_id,
    actualizar_tipo_documento,
    eliminar_tipo_documento
)

tipo_documento_bp = Blueprint('tipo_documento', __name__, url_prefix='/tipos-documento')

@tipo_documento_bp.before_request
def verificar_admin():
    # Asegúrate de que solo los administradores puedan acceder
    if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado.", "warning")
        return redirect(url_for('auth.login')) # Redirigir al login es más seguro

@tipo_documento_bp.route('/')
def index():
    tipos = obtener_tipos_documento()
    return render_template('tipo_documento/index.html', tipos=tipos)

@tipo_documento_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        # Recogemos los datos del formulario
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')

        # Validación básica para que no estén vacíos
        if not tipo or not descripcion:
            flash("Ambos campos, tipo y descripción, son obligatorios.", "warning")
            return render_template('tipo_documento/insertar.html')

        crear_tipo_documento(tipo, descripcion)
        flash("Tipo de documento creado exitosamente.", "success")
        return redirect(url_for('tipo_documento.index'))
    
    return render_template('tipo_documento/insertar.html')

@tipo_documento_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        descripcion = request.form.get('descripcion')

        if not tipo or not descripcion:
            flash("Ambos campos son obligatorios.", "warning")
            # Obtenemos los datos de nuevo para no perder el contexto al recargar
            tipo_doc = obtener_tipo_documento_por_id(id)
            return render_template('tipo_documento/actualizar.html', tipo_doc=tipo_doc)
            
        actualizar_tipo_documento(id, tipo, descripcion)
        flash("Tipo de documento actualizado exitosamente.", "success")
        return redirect(url_for('tipo_documento.index'))

    # Para el método GET, obtenemos el documento y lo pasamos a la plantilla
    tipo_doc = obtener_tipo_documento_por_id(id)
    if not tipo_doc:
        flash("Tipo de documento no encontrado.", "danger")
        return redirect(url_for('tipo_documento.index'))
        
    return render_template('tipo_documento/actualizar.html', tipo_doc=tipo_doc)

@tipo_documento_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    tipo_doc = obtener_tipo_documento_por_id(id)
    if not tipo_doc:
        flash("Tipo de documento no encontrado.", "danger")
        return redirect(url_for('tipo_documento.index'))
    return render_template('tipo_documento/eliminar.html', tipo_doc=tipo_doc)

@tipo_documento_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_tipo_documento(id)
    flash("Tipo de documento eliminado.", "info")
    return redirect(url_for('tipo_documento.index'))