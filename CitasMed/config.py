# en config.py

import os

class Config:
    # Clave secreta para proteger los formularios y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil'
    
    # Configuración de la base de datos con SQLAlchemy
    # Usamos el driver pymysql para conectarnos a XAMPP
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/citas_medicas_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False