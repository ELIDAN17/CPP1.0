# config.py

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SSL_CERT_PATH = os.path.join(BASE_DIR, 'certificado', 'DigiCertGlobalRootG2.crt.pem')


class Config:
    # -------------------------------------------------------------------------
    # 1. SEGURIDAD Y CLAVE SECRETA
    # -------------------------------------------------------------------------
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil'
    
    # -------------------------------------------------------------------------
    # 2. CONFIGURACIÓN DE LA BASE DE DATOS (AZURE MySQL con SSL)
    # -------------------------------------------------------------------------
    
    DB_USER = os.environ.get('DB_USER', 'AzureAdmin') 
    DB_PASSWORD = os.environ.get('DB_PASSWORD') 
    DB_HOST = os.environ.get('DB_HOST', 'candela-mysql-server-2025.mysql.database.azure.com')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'citas_medicas_db')
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?ssl_ca={SSL_CERT_PATH}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # -------------------------------------------------------------------------
    # 3. CONFIGURACIÓN DE CORREO Y SCHEDULER
    # -------------------------------------------------------------------------
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    
    # Asegúrate de usar variables de entorno para las credenciales reales
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'citasmed20@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'citasMED123+')
    
    SCHEDULER_API_ENABLED = True
