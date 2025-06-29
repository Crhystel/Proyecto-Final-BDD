from flask import Flask, render_template, session, redirect
from app.routes.auth_routes import auth_bp
from app.routes.usuario_routes import usuario_bp
from app.routes.parroquia_routes import parroquia_bp
from app.routes.parroquia_principal_routes import parroquia_principal_bp
from app.routes.catequista_routes import catequista_bp
from app.routes.catequizando_routes import catequizando_bp
from app.routes.ficha_routes import ficha_bp
from app.routes.libro_routes import libro_bp
from app.routes.tipo_sacramento_routes import tipo_sacramento_bp
from app.routes.nivelcatequesis_routes import nivel_bp
from app.routes.ciclo_catequistico_routes import ciclo_bp
from app.routes.grupo_catequesis_routes import grupo_bp
from app.routes.grupo_catequista_routes import grupo_catequista_bp
from app.routes.persona_routes import persona_bp
from app.routes.inscripcion_routes import inscripcion_bp
from app.routes.certificado_routes import certificado_bp
import os

app = Flask(__name__, template_folder=os.path.join('app', 'templates'))
app = Flask(__name__, static_folder="static", template_folder=os.path.join("app", "templates"))
app.secret_key = 'clave-super-secreta'

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(parroquia_bp)
app.register_blueprint(parroquia_principal_bp)
app.register_blueprint(catequista_bp)
app.register_blueprint(catequizando_bp)
app.register_blueprint(ficha_bp)
app.register_blueprint(libro_bp)
app.register_blueprint(tipo_sacramento_bp)
app.register_blueprint(nivel_bp)
app.register_blueprint(ciclo_bp)
app.register_blueprint(grupo_bp)
app.register_blueprint(grupo_catequista_bp)
app.register_blueprint(persona_bp)
app.register_blueprint(inscripcion_bp)
app.register_blueprint(certificado_bp)

@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect('/')
    return render_template('bienvenida.html', usuario=session['usuario'], rol=session['rol'])

@app.route('/bienvenida_general')
def bienvenida_general():
    if 'usuario' not in session:
        return redirect('/')
    return render_template('bienvenidageneral.html', usuario=session['usuario'], rol=session['rol'])


if __name__ == '__main__':
    app.run(debug=True)
