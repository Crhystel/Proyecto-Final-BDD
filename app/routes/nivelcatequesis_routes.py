from flask import Blueprint, render_template, request, redirect, url_for, session
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
    niveles = obtener_niveles()
    return render_template('nivel/index.html', niveles=niveles)

@nivel_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_nivel(
            request.form['orden'],
            request.form['nombre_nivel'],
            request.form['descripcion'],
            request.form['id_libro'] or None,
            request.form['id_tipo_sacramento'] or None
        )
        return redirect(url_for('nivel.index'))
    
    libros = obtener_libros()
    tipos_sacramento = obtener_tipos_sacramento()
    return render_template('nivel/insertar.html', libros=libros, tipos=tipos_sacramento)

@nivel_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_nivel(
            id,
            request.form['orden'],
            request.form['nombre_nivel'],
            request.form['descripcion'],
            request.form['id_libro'] or None,
            request.form['id_tipo_sacramento'] or None
        )
        return redirect(url_for('nivel.index'))

    nivel = obtener_nivel_por_id(id)
    libros = obtener_libros()
    tipos_sacramento = obtener_tipos_sacramento()
    return render_template('nivel/actualizar.html', nivel=nivel, libros=libros, tipos=tipos_sacramento)

@nivel_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_nivel(id)
        return redirect(url_for('nivel.index'))
    return render_template('nivel/eliminar.html', id=id)
