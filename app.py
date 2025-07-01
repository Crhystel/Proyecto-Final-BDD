# app.py (VERSIÓN CORREGIDA Y ESTRUCTURADA)

from flask import Flask, render_template, session, redirect, url_for, flash
from extensions import bcrypt
import os
from app.routes.auth_routes import auth_bp
from app.routes.catequizando_routes import catequizando_bp
from app.routes.usuario_routes import usuario_bp

app = Flask(__name__, 
            static_folder="static", 
            template_folder=os.path.join("app", "templates"))

# Configura la clave secreta para las sesiones
app.secret_key = 'e9cd3e16efd30433a17ab00a1432daa1be5eb5f4760f8a38'

bcrypt.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(catequizando_bp, url_prefiz='/catequizando')
app.register_blueprint(usuario_bp,url_prefix='/usuarios')


@app.route('/')
def index_route():
    if 'usuario_nombre' in session:
        return redirect(url_for('home'))
    return redirect(url_for('auth.login'))

@app.route('/home')
def home():
    if 'usuario_nombre' not in session:
        flash("Por favor, iniciar sesión para continuar.", "info")
        return redirect(url_for('auth.login'))
    
    return render_template('home.html', 
                           usuario=session['usuario_nombre'], 
                           rol=session['rol'])

@app.route('/bienvenida_general')
def bienvenida_general():
    if 'usuario_nombre' not in session:
        flash("Por favor, inicia sesión para continuar.", "info")
        return redirect(url_for('auth.login'))
        
    return render_template('bienvenidageneral.html', 
                           usuario=session['usuario_nombre'], 
                           rol=session['rol'])

# --- 4. EJECUCIÓN DE LA APLICACIÓN ---
if __name__ == '__main__':
    # Asegúrate de que tu base de datos está disponible antes de correr
    app.run(debug=True)