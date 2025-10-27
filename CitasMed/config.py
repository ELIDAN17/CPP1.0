# en config.py

import os

class Config:
    # Clave secreta para proteger los formularios y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil'
    
    # Configuración de la base de datos con SQLAlchemy
    # Usamos el driver pymysql para conectarnos a XAMPP
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@127.0.0.1:3306/citas_medicas_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'citasmed20@gmail.com') # <-- TU CORREO DE GMAIL
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'citasMED123+') # <-- TU CONTRASEÑA DE APLICACIÓN
    SCHEDULER_API_ENABLED = True