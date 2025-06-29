from flask import Blueprint, render_template, request, redirect, url_for
from app.services.parroquia_principal_service import (
    obtener_parroquias,
    crear_parroquia,
    actualizar_parroquia,
    eliminar_parroquia
)

parroquia_principal_bp = Blueprint('parroquia', __name__, url_prefix='/parroquias')

@parroquia_principal_bp.route('/')
def index():
    parroquias = obtener_parroquias()
    return render_template('parroquia_principal/index.html', parroquias=parroquias)

@parroquia_principal_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        crear_parroquia(nombre, direccion, ciudad, telefono, correo)
        return redirect(url_for('parroquia.index'))
    return render_template('parroquia_principal/insertar.html')

@parroquia_principal_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_parroquia(id, request.form['nombre'], request.form['direccion'],
                             request.form['ciudad'], request.form['telefono'], request.form['correo'])
        return redirect(url_for('parroquia.index'))

    from app.database import get_connection
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM PARROQUIA_PRINCIPAL WHERE id_parroquia_principal = ?", id)
        parroquia = cursor.fetchone()
    return render_template('parroquia_principal/actualizar.html', parroquia=parroquia)

@parroquia_principal_bp.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if request.method == 'POST':
        eliminar_parroquia(id)
        return redirect(url_for('parroquia.index'))
    return render_template('parroquia_principal/eliminar.html', id=id)

