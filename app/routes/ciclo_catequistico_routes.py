from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.ciclo_catequistico_service import *
from app.services.nivelcatequesis_service import obtener_niveles

ciclo_bp = Blueprint('ciclo', __name__, url_prefix='/ciclos')

@ciclo_bp.before_request
def verificar_admin():
    if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado", "warning")
        return redirect(url_for('home'))

@ciclo_bp.route('/')
def index():
    lista_ciclos = obtener_ciclos()
    return render_template('ciclo_catequistico/index.html', ciclos=lista_ciclos)

@ciclo_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_ciclo(
            nombre=request.form['nombre'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            id_nivel=request.form.get('id_nivel')
        )
        flash("Ciclo creado exitosamente.", "success")
        return redirect(url_for('ciclo.index'))
    
    lista_niveles = obtener_niveles() 
    return render_template('ciclo_catequistico/insertar.html', niveles=lista_niveles)

@ciclo_bp.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        actualizar_ciclo(
            id_ciclo=id,
            nombre=request.form['nombre'],
            fecha_inicio=request.form['fecha_inicio'],
            fecha_fin=request.form['fecha_fin'],
            id_nivel=request.form.get('id_nivel')
        )
        flash("Ciclo actualizado exitosamente.", "success")
        return redirect(url_for('ciclo.index'))
    
    ciclo = obtener_ciclo_por_id(id)
    if not ciclo:
        flash("Ciclo no encontrado.", "danger")
        return redirect(url_for('ciclo.index'))
    
    lista_niveles = obtener_niveles()
    return render_template('ciclo_catequistico/actualizar.html', ciclo=ciclo, niveles=lista_niveles)

@ciclo_bp.route('/confirmar-eliminar/<int:id>')
def confirmar_eliminar(id):
    ciclo = obtener_ciclo_por_id(id)
    if not ciclo:
        flash("Ciclo no encontrado.", "danger")
        return redirect(url_for('ciclo.index'))
    return render_template('ciclo_catequistico/eliminar.html', ciclo=ciclo)

@ciclo_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    exito = eliminar_ciclo(id)
    if exito:
        flash("Ciclo eliminado.", "info")
    else:
        flash("Error al eliminar el ciclo.", "danger")
    return redirect(url_for('ciclo.index'))