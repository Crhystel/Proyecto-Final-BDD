from flask import Blueprint, render_template, request, redirect, url_for
from app.services.ficha_service import *
from app.services.catequizando_service import obtener_catequizandos

ficha_bp = Blueprint('ficha', __name__, url_prefix='/fichas')

@ficha_bp.route('/')
def index():
    fichas = obtener_fichas()
    return render_template('ficha/index.html', fichas=fichas)

@ficha_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_ficha(
            request.form['id_catequizando'],
            request.form.get('tiene_bautismo') == 'on',
            request.form.get('requiere_atencion_especial') == 'on',
            request.form['observaciones'],
            request.form['lugar_bautismo'],
            request.form['fecha_bautismo']
        )
        return redirect(url_for('ficha.index'))

    catequizandos = obtener_catequizandos()
    return render_template('ficha/insertar.html', catequizandos=catequizandos)

@ficha_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_ficha(
            id,
            request.form['id_catequizando'],
            request.form.get('tiene_bautismo') == 'on',
            request.form.get('requiere_atencion_especial') == 'on',
            request.form['observaciones'],
            request.form['lugar_bautismo'],
            request.form['fecha_bautismo']
        )
        return redirect(url_for('ficha.index'))

    ficha = obtener_ficha_por_id(id)
    catequizandos = obtener_catequizandos()
    return render_template('ficha/actualizar.html', ficha=ficha, catequizandos=catequizandos)

@ficha_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_ficha(id)
        return redirect(url_for('ficha.index'))
    return render_template('ficha/eliminar.html', id=id)
