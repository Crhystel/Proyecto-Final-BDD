from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.libro_service import *

libro_bp = Blueprint('libro', __name__, url_prefix='/libros')

@libro_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@libro_bp.route('/')
def index():
    libros = obtener_libros()
    return render_template('libro/index.html', libros=libros)

@libro_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_libro(
            request.form['titulo'],
            request.form['autor'],
            request.form['editorial'],
            request.form['anio_edicion']
        )
        return redirect(url_for('libro.index'))
    return render_template('libro/insertar.html')

@libro_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_libro(
            id,
            request.form['titulo'],
            request.form['autor'],
            request.form['editorial'],
            request.form['anio_edicion']
        )
        return redirect(url_for('libro.index'))

    libro = obtener_libro_por_id(id)
    return render_template('libro/actualizar.html', libro=libro)

@libro_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_libro(id)
        return redirect(url_for('libro.index'))
    return render_template('libro/eliminar.html', id=id)
