from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.catequista_service import (
    crear_catequista,
    obtener_catequistas,
    obtener_catequista_por_id,
    actualizar_catequista,
    eliminar_catequista
)

catequista_bp = Blueprint('catequista', __name__, url_prefix='/catequistas')

@catequista_bp.before_request
def solo_admin():
     if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado", "warning")
        return redirect(url_for('bienvenida'))

@catequista_bp.route('/')
def index():
    lista = obtener_catequistas()
    return render_template('catequista/index.html', catequistas=lista)

@catequista_bp.route('/insertar', methods=['GET','POST'])
def insertar():
    if request.method=='POST':
        crear_catequista(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            correo=request.form['correo'],
            telefono=request.form['telefono'],
            rol=request.form['rol']
        )
        flash("Catequista creado exitosamente.", "success")
        return redirect(url_for('catequista.index'))
    return render_template('catequista/insertar.html')

@catequista_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_catequista(
            id_catequista=id,
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            correo=request.form['correo'],
            telefono=request.form['telefono'],
            rol=request.form['rol']
        )
        flash("Catequista actualizado exitosamente.", "success")
        return redirect(url_for('catequista.index'))
    
    catequista = obtener_catequista_por_id(id)
    if not catequista:
        flash("Catequista no encontrado.", "danger")
        return redirect(url_for('catequista.index'))
    return render_template('catequista/actualizar.html', catequista=catequista)

@catequista_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    eliminar_catequista(id)
    flash("Catequista eliminado.", "info")
    return redirect(url_for('catequista.index'))

@catequista_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    catequista = obtener_catequista_por_id(id)
    if not catequista:
        flash("Catequista no encontrado.", "danger")
        return redirect(url_for('catequista.index'))
    return render_template('catequista/eliminar.html', catequista=catequista)