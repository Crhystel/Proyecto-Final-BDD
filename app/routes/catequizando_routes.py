from flask import Blueprint, render_template,request,redirect,url_for,session,flash
from app.services.catequizando_service import (
    crear_catequizando,
    obtener_catequizando_por_id,
    actualizar_catequizando,
    eliminar_catequizando,
    obtener_catequizandos
)
from app.services.parroquia_service import obtener_parroquias

catequizando_bp=Blueprint("catequizando",__name__)

@catequizando_bp.before_request
def solo_admin():
    if 'rol' not in session or session["rol"]!="A":
        flash("Acceso no autorizado","warning")
        return redirect("/")
    
@catequizando_bp.route("/")
def index():
    lista_catequizandos=obtener_catequizandos()
    return render_template("catequizando/index.html",
                           catequizandos=lista_catequizandos)
    
@catequizando_bp.route('/insertar',methods=["GET","POST"])
def insertar():
    if request.method=="POST":
        es_bautizado="bautizado" in request.form
        crear_catequizando(
            apellido=request.form["apellido"],
            nombre=request.form["nombre"],
            fecha_nacimiento=request.form["fecha_nacimiento"],
            doc_identidad=request.form["documento_identidad"],
            fecha_registro=request.form["fecha_registro"],
            bautizado=es_bautizado,
            id_parroquia=request.form.get("id_parroquia") or None
        )
        flash("Catequizando creado exitosamente", "success")
        return redirect(url_for("catequizando.index"))
    parroquias=obtener_parroquias()
    return render_template("catequizando/insertar.html", parroquias=parroquias)

@catequizando_bp.route("/actualizar/<id>",methods=["GET","POST"])
def actualizar(id):
    if request.method=="POST":
        es_bautizado="bautizado" in request.form
        actualizar_catequizando(
            id_catequizando=id,
            apellido=request.form["apellido"],
            nombre=request.form["nombre"],
            fecha_nac=request.form["fecha_nacimiento"],
            doc_id=request.form["documentos_identidad"],
            fecha_reg=request.form["fecha_registro"],
            bautizado=es_bautizado,
            id_parroquia=request.form.get("id_parroquia") or None
        )
        flash("Catequizando actualizado exitosamente.", "success")
        return redirect(url_for('catequizando.index'))
    
    catequizando = obtener_catequizando_por_id(id)
    parroquias = obtener_parroquias()
    
    if not catequizando:
        flash("Catequizando no encontrado.", "danger")
        return redirect(url_for('catequizando.index'))
        
    return render_template('catequizando/actualizar.html', catequizando=catequizando, parroquias=parroquias)

@catequizando_bp.route('/eliminar/<id>', methods=['POST']) 
def eliminar(id):
    eliminar_catequizando(id)
    flash("Catequizando eliminado.", "info")
    return redirect(url_for('catequizando.index'))

@catequizando_bp.route('/confirmar-eliminar/<id>')
def confirmar_eliminar(id):
    catequizando = obtener_catequizando_por_id(id)
    return render_template('catequizando/eliminar.html', catequizando=catequizando)