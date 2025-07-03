from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.nivelcatequesis_service import *
from app.services.libro_service import obtener_libros
from app.services.tipo_sacramento_service import obtener_tipos_sacramento

nivel_bp = Blueprint('nivel', __name__, url_prefix='/niveles')
@nivel_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@nivel_bp.route('/')
def index():
    lista_niveles = obtener_niveles()
    return render_template('nivel/index.html', niveles=lista_niveles)

@nivel_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_nivel(
            orden=request.form['orden'],
            nombre_nivel=request.form['nombre_nivel'],
            descripcion=request.form['descripcion'],
            id_libro=request.form.get('id_libro') or None,
            id_tipo_sacramento=request.form.get('id_tipo_sacramento') or None
        )
        flash("Nivel creado exitosamente.", "success")
        return redirect(url_for('nivel.index'))
    
    lista_libros = obtener_libros()
    lista_tipos_sacramento = obtener_tipos_sacramento()
    return render_template('nivel/insertar.html', libros=lista_libros, tipos=lista_tipos_sacramento)

@nivel_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_nivel(
            id_nivel=id,
            orden=request.form['orden'],
            nombre_nivel=request.form['nombre_nivel'],
            descripcion=request.form['descripcion'],
            id_libro=request.form.get('id_libro') or None,
            id_tipo_sacramento=request.form.get('id_tipo_sacramento') or None
        )
        flash("Nivel actualizado exitosamente.", "success")
        return redirect(url_for('nivel.index'))

    nivel = obtener_nivel_por_id(id)
    if not nivel:
        flash("Nivel no encontrado.", "danger")
        return redirect(url_for('nivel.index'))

    lista_libros = obtener_libros()
    lista_tipos_sacramento = obtener_tipos_sacramento()
    return render_template('nivel/actualizar.html', nivel=nivel, libros=lista_libros, tipos=lista_tipos_sacramento)

@nivel_bp.route('/confirmar-eliminar/<string:id>')
def confirmar_eliminar(id):
    nivel=obtener_nivel_por_id(id)
    if not nivel:
        flash("Nivel no encontrado", "danger")
        return redirect(url_for("nivel.index"))
    return render_template('nivel/eliminar.html',nivel=nivel)

@nivel_bp.route('/eliminar/<int:id>', methods=['POST']) 
def eliminar(id):
    exito = eliminar_nivel(id)
    if exito:
        flash("Nivel eliminado", "info")
    else:
        flash("Error al eliminar el nivel.", "danger")
    return redirect(url_for('nivel.index'))