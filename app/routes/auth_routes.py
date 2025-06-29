from flask import Blueprint, render_template, request, redirect, url_for, session
from app.services.auth_service import verificar_credenciales

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        usuario = verificar_credenciales(nombre, contrasena)
        if usuario:
            session['usuario'] = usuario.nombre
            session['rol'] = usuario.rol
            if usuario.rol == 'A':
                return redirect(url_for('home'))
            else:
                return redirect(url_for('bienvenida_general'))

        return render_template('auth/login.html', error='Credenciales inválidas')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
