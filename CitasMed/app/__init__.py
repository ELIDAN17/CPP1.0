# en app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager
from flask_mail import Mail

# Creamos una instancia de la base de datos
db = SQLAlchemy()
login_manager = LoginManager() # Crear instancia
login_manager.login_view = 'main.login' # A qué página redirigir si no se ha logueado

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Inicializamos la base de datos con la app
    db.init_app(app)
    login_manager.init_app(app) 
    mail.init_app(app)# Conectar con la app
    #Migrate(app, db)
    from .models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Importamos y registramos las rutas
    from app.routes import main
    app.register_blueprint(main)

    return app

from app import models