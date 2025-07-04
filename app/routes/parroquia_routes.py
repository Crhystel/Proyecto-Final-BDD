from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.parroquia_service import *
from app.services.ciclo_catequistico_service import obtener_ciclos
parroquia_bp = Blueprint('parroquia', __name__, url_prefix='/parroquias')

@parroquia_bp.before_request
def solo_admin():
    if 'rol' not in session or session['rol'] != 'A':
        flash("Acceso no autorizado", "warning")
        return redirect(url_for('bienvenidageneral'))

@parroquia_bp.route('/')
def index():
    parroquias = obtener_parroquias()
    return render_template('parroquia/index.html', parroquias=parroquias)

@parroquia_bp.route('/insertar', methods=['GET', 'POST'])
def insertar():
    if request.method == 'POST':
        crear_parroquia_grupo(
            nombre=request.form['nombre'],
            direccion=request.form['direccion'],
            ciudad=request.form['ciudad'],
            telefono=request.form.get('telefono'),
            correo=request.form.get('correo_electronico'), 
            id_principal_seleccionado=request.form.get('id_parroquia_principal') or None,
            nombre_grupo=request.form.get("nombre_grupo"),
            id_ciclo=request.form.get("id_ciclo")
        )
        flash("Parroquia creada exitosamente.", "success")
        return redirect(url_for('parroquia.index'))
    
    parroquias_principales = obtener_parroquias_principales()
    lista_de_ciclos=obtener_ciclos()
    return render_template('parroquia/insertar.html', parroquias_principales=parroquias_principales, ciclos=lista_de_ciclos)

@parroquia_bp.route('/actualizar/<string:id>', methods=['GET', 'POST'])
def actualizar(id):
    if request.method == 'POST':
        # Llamamos a la función de actualizar
        resultado = actualizar_parroquia(
            id_parroquia=id,
            nombre=request.form['nombre'],
            direccion=request.form['direccion'],
            ciudad=request.form['ciudad'],
            telefono=request.form.get('telefono'),
            correo=request.form.get('correo_electronico'), 
            id_parroquia_principal=request.form.get('id_parroquia_principal') or None
        )
        
        if resultado == -1:
            flash("Error: Una parroquia no puede ser su propia parroquia principal.", "danger")
            return redirect(url_for('parroquia.actualizar', id=id))
        elif resultado:
            flash("Parroquia actualizada exitosamente.", "success")
        else:
            flash("No se realizaron cambios o ocurrió un error.", "info")
            
        return redirect(url_for('parroquia.index'))

    parroquia = obtener_parroquia_por_id(id)
    if not parroquia:
        flash("Parroquia no encontrada.", "danger")
        return redirect(url_for('parroquia.index'))
        
    parroquias_principales_raw = obtener_parroquias_principales()
    parroquias_principales_filtradas = [p for p in parroquias_principales_raw if p['_id'] != int(id)]
    
    return render_template('parroquia/actualizar.html', 
                           parroquia=parroquia, 
                           parroquias_principales=parroquias_principales_filtradas)
    
@parroquia_bp.route('/eliminar/<string:id>', methods=['POST'])
def eliminar(id):
    eliminar_parroquia(id)
    flash("Parroquia eliminada.", "info")
    return redirect(url_for('parroquia.index'))

@parroquia_bp.route('/confirmar-eliminar/<string:id>')
def confirmar_eliminar(id):
    parroquia = obtener_parroquia_por_id(id)
    if not parroquia:
        flash("Parroquia no encontrada.", "danger")
        return redirect(url_for('parroquia.index'))
    return render_template('parroquia/eliminar.html', parroquia=parroquia)

@parroquia_bp.route('/<int:id>/detalles')
def detalles_parroquia(id):
    parroquia = obtener_detalles_completos_parroquia(id)
    
    if not parroquia:
        flash("Parroquia no encontrada.", "danger")
        return redirect(url_for('parroquia.index'))
    
    if 'parroquia_principal' not in parroquia:
        flash("Las parroquias principales no gestionan grupos directamente", "info")
        return redirect(url_for('parroquia.index'))
    return render_template('parroquia/detalles.html', parroquia=parroquia)

@parroquia_bp.route('/<string:id>/agregar_grupo', methods=['GET', 'POST'])
def agregar_grupo(id):
    parroquia = obtener_parroquia_por_id(id)
    if not parroquia:
        flash("Parroquia no encontrada.", "danger")
        return redirect(url_for('parroquia.index'))
    if 'parroquia_principal' not in parroquia:
        flash("No se pueden añadir grupos a una parroquia principal","warning")
        return redirect(url_for('parroquia.index'))

    if request.method == 'POST':
        nombre_grupo = request.form.get('nombre_grupo')
        id_ciclo = request.form.get('id_ciclo')
        
        exito = agregar_grupo_a_parroquia(id, nombre_grupo, id_ciclo)
        
        if exito:
            flash("Grupo añadido exitosamente.", "success")
        else:
            flash("No se pudo añadir el grupo.", "danger")
            
        return redirect(url_for('parroquia.detalles_parroquia', id=id))
    
    lista_ciclos = obtener_ciclos()
    return render_template('parroquia/agregar_grupo.html', parroquia=parroquia, ciclos=lista_ciclos)