# app.py (VERSIÓN CORREGIDA Y ESTRUCTURADA)

from flask import Flask, render_template, session, redirect, url_for, flash
from extensions import bcrypt
import os
from app.routes.auth_routes import auth_bp
from app.routes.catequizando_routes import catequizando_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.parroquia_routes import parroquia_bp
from app.routes.catequista_routes import catequista_bp
from app.services.catequizando_service import sincronizar_contador

app = Flask(__name__, 
            static_folder="static", 
            template_folder=os.path.join("app", "templates"))

app.secret_key = 'e9cd3e16efd30433a17ab00a1432daa1be5eb5f4760f8a38'

bcrypt.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(catequizando_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(parroquia_bp)
app.register_blueprint(catequista_bp)


@app.route('/')
def index_route():
    if 'usuario_nombre' in session:
        if session.get('rol')=='A':
            return redirect(url_for('bienvenida'))
        else:
            return redirect(url_for('bienvenida_general'))
    return redirect(url_for('auth.login'))

@app.route('/bienvenida')
def bienvenida():
    if 'usuario_nombre' not in session:
        flash("Por favor, iniciar sesión para continuar.", "info")
        return redirect(url_for('auth.login'))
    if session.get('rol')!='A':
        flash("Acceso no autorizado", "warning")
        return redirect(url_for('bienvenida_general'))
    return render_template('bienvenida.html')

@app.route('/bienvenida_general')
def bienvenida_general():
    if 'usuario_nombre' not in session:
        flash("Por favor, inicia sesión para continuar.", "info")
        return redirect(url_for('auth.login'))
        
    return render_template('bienvenidageneral.html')

with app.app_context():
    sincronizar_contador('parroquias')
    sincronizar_contador('catequizandos')
    sincronizar_contador("libros")
    sincronizar_contador("tipo_sacramentos")
    sincronizar_contador("catequistas")
    sincronizar_contador("usuarios")

if __name__ == '__main__':
    app.run(debug=True)