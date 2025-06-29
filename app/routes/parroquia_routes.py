from flask import Blueprint, render_template, request, redirect, url_for
from app.services.parroquia_service import (
    obtener_parroquias,
    crear_parroquia,
    actualizar_parroquia,
    eliminar_parroquia,
    obtener_parroquias_principales
)
from app.database import get_connection

parroquia_bp = Blueprint('parroquia_sec', __name__, url_prefix='/parroquia')

@parroquia_bp.route('/')
def index():
    parroquias = obtener_parroquias()
    return render_template('parroquia/index.html', parroquias=parroquias)

@parroquia_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        id_pp = request.form['id_parroquia_principal']

        crear_parroquia(nombre, direccion, ciudad, telefono, correo, id_pp)
        return redirect(url_for('parroquia_sec.index'))

    parroquias_principales = obtener_parroquias_principales()
    return render_template('parroquia/insertar.html', parroquias_principales=parroquias_principales)

@parroquia_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_parroquia(
            id,
            request.form['nombre'],
            request.form['direccion'],
            request.form['ciudad'],
            request.form['telefono'],
            request.form['correo'],
            request.form['id_parroquia_principal']
        )
        return redirect(url_for('parroquia_sec.index'))

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM PARROQUIA WHERE id_parroquia = ?", id)
        parroquia = cursor.fetchone()
    return render_template('parroquia/actualizar.html', parroquia=parroquia)

@parroquia_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_parroquia(id)
        return redirect(url_for('parroquia_sec.index'))
    return render_template('parroquia/eliminar.html', id=id)

