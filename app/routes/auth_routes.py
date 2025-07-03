from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import verificar_credenciales

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está en sesión, redirigirlo
    if 'usuario' in session:
        return redirect(url_for('bienvenida'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        
        # verificar_credenciales ahora devuelve un diccionario o None
        usuario = verificar_credenciales(nombre, contrasena)
        
        if usuario:
            # Almacenamos los datos en la sesión. MongoDB devuelve un diccionario.
            session['usuario_id'] = str(usuario['_id']) # Guardar el ID es buena práctica
            session['usuario_nombre'] = usuario['nombre']
            session['rol'] = usuario['rol']
            
            flash(f"Bienvenido de vuelta, {usuario['nombre']}!", "success")

            if usuario['rol'] == 'A':
                return redirect(url_for('bienvenida')) # Redirige a la página de admin
            else:
                return redirect(url_for('bienvenida_general')) # O a una página general
        
        # Usamos flash para mostrar el error de forma más elegante
        flash('Credenciales inválidas. Por favor, inténtalo de nuevo.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado la sesión exitosamente.', 'info')
    return redirect(url_for('auth.login'))

