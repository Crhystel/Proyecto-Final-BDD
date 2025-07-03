from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.libro_service import (
    crear_libro,
    obtener_libros,
    obtener_libro_por_id,
    actualizar_libro,
    eliminar_libro
)

libro_bp = Blueprint('libro', __name__, url_prefix='/libros')

@libro_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado.", "warning")
        return redirect(url_for('home')) 
@libro_bp.route('/')
def index():
    lista_libros = obtener_libros()
    return render_template('libro/index.html', libros=lista_libros)

@libro_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_libro(
            titulo=request.form['titulo'],
            autor=request.form['autor'],
            editorial=request.form['editorial'],
            anio_edicion=request.form.get('anio_edicion')
        )
        flash("Libro creado exitosamente.", "success")
        return redirect(url_for('libro.index'))
    
    return render_template('libro/insertar.html')

@libro_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    libro = obtener_libro_por_id(id)
    if not libro:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('libro.index'))

    if request.method == 'POST':
        actualizar_libro(
            id_libro=id,
            titulo=request.form['titulo'],
            autor=request.form['autor'],
            editorial=request.form['editorial'],
            anio_edicion=request.form.get('anio_edicion')
        )
        flash("Libro actualizado exitosamente.", "success")
        return redirect(url_for('libro.index'))

    return render_template('libro/actualizar.html', libro=libro)

@libro_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    libro = obtener_libro_por_id(id)
    if not libro:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('libro.index'))
    return render_template('libro/eliminar.html', libro=libro)

@libro_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    exito = eliminar_libro(id)
    if exito:
        flash("Libro eliminado permanentemente.", "info")
    else:
        flash("Error al eliminar el libro.", "danger")
    return redirect(url_for('libro.index'))