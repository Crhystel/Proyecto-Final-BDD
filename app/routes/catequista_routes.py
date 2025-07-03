from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.catequista_service import *

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

@catequista_bp.route('/actualizar/<int:id>/', methods=['GET', 'POST'])
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

@catequista_bp.route('/confirmar-eliminar/<int:id>/')
def confirmar_eliminar(id):
    catequista = obtener_catequista_por_id(id)
    if not catequista:
        flash("Catequista no encontrado.", "danger")
        return redirect(url_for('catequista.index'))
    return render_template('catequista/eliminar.html', catequista=catequista)

@catequista_bp.route('/<int:id>/asignar-grupos')
def asignar_grupos(id):
    catequista = obtener_catequista_por_id(id)
    if not catequista:
        flash("Catequista no encontrado.", "danger")
        return redirect(url_for('catequista.index'))

    todos_los_grupos = obtener_todos_los_grupos()
    grupos_p = catequista.get('grupos_como_principal') or []
    grupos_s = catequista.get('grupos_como_secundario') or []
    grupos_asignados_ids = [g['_id'] for g in grupos_p] + [g['_id'] for g in grupos_s]

    return render_template('catequista/asignar_grupos.html', 
                           catequista=catequista, 
                           todos_los_grupos=todos_los_grupos,
                           grupos_asignados_ids=grupos_asignados_ids)

@catequista_bp.route('/<int:id>/procesar-asignacion', methods=['POST'])
def procesar_asignacion(id):
    id_grupo = request.form.get('id_grupo')
    if not id_grupo:
        flash("Error: Debes seleccionar un grupo para asignar.", "warning")
        return redirect(url_for('catequista.asignar_grupos', id=id))
    
    catequista = obtener_catequista_por_id(id)
    if not catequista:
        flash("Catequista no encontrado.", "danger")
        return redirect(url_for('catequista.index'))
    
    rol_catequista = catequista.get('rol') 
    grupo_info = obtener_grupo_por_id(id_grupo) 

    if grupo_info and rol_catequista:
        exito=asignar_grupo_a_catequista(
            id_catequista=id, 
            id_grupo=id_grupo, 
            nombre_grupo=grupo_info['nombre_grupo'], 
            rol_catequista=rol_catequista
        )
        if exito:
            flash("Grupo asignado correctamente.", "success")
        else:
            flash("Error: No se pudo asignar el grupo. La operación en la base de datos falló.", "danger")

    else:
        flash("Error al asignar el grupo. El grupo o el rol del catequista no son válidos.", "danger")

    return redirect(url_for('catequista.asignar_grupos', id=id))

@catequista_bp.route('/<int:id_catequista>/eliminar-grupo/<int:id_grupo>', methods=['POST'])
def eliminar_grupo(id_catequista, id_grupo):
    eliminar_grupo_de_catequista(id_catequista, id_grupo)
    flash("Grupo eliminado correctamente.", "success")
    return redirect(url_for('catequista.asignar_grupos', id=id_catequista))