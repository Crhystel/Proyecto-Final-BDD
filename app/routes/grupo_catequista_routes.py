from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.grupo_catequista_service import (
    obtener_grupos_catequistas,
    crear_grupo_catequista,
    actualizar_grupo_catequista,
    eliminar_grupo_catequista,
    obtener_grupos,
    obtener_catequistas_por_rol
)

grupo_catequista_bp = Blueprint('grupo_catequista', __name__, url_prefix='/grupos_catequistas')

@grupo_catequista_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        return redirect('/')

@grupo_catequista_bp.route('/')
def index():
    datos = obtener_grupos_catequistas()
    return render_template('grupo_catequista/index.html', datos=datos)

@grupo_catequista_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_grupo_catequista(
            request.form['id_grupo'],
            request.form['id_catequista_principal'],
            request.form['id_catequista_secundario']
        )
        return redirect(url_for('grupo_catequista.index'))

    grupos = obtener_grupos()
    catequistas_principales = obtener_catequistas_por_rol('P')
    catequistas_ayudantes = obtener_catequistas_por_rol('A')
    return render_template('grupo_catequista/insertar.html', grupos=grupos,
                           catequistas_principales=catequistas_principales,
                           catequistas_ayudantes=catequistas_ayudantes)

@grupo_catequista_bp.route('/actualizar/<int:id_grupo>', methods=['GET', 'POST'])
def actualizar(id_grupo):
    if request.method == 'POST':
        actualizar_grupo_catequista(
            id_grupo,
            request.form['id_catequista_principal'],
            request.form['id_catequista_secundario']
        )
        return redirect(url_for('grupo_catequista.index'))

    # Aquí podrías cargar los datos del grupo si deseas precargar el formulario
    catequistas_principales = obtener_catequistas_por_rol('P')
    catequistas_ayudantes = obtener_catequistas_por_rol('A')
    return render_template('grupo_catequista/actualizar.html', id_grupo=id_grupo,
                           catequistas_principales=catequistas_principales,
                           catequistas_ayudantes=catequistas_ayudantes)

@grupo_catequista_bp.route('/eliminar/<int:id_grupo>/<int:id_catequista>', methods=['GET', 'POST'])
def eliminar(id_grupo, id_catequista):
    if request.method == 'POST':
        eliminar_grupo_catequista(id_grupo, id_catequista)
        return redirect(url_for('grupo_catequista.index'))
    return render_template('grupo_catequista/eliminar.html', id_grupo=id_grupo, id_catequista=id_catequista)
