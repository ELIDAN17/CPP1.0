from pathlib import Path
import os
import sys  # 👉 ESTAS LÍNEAS SON LAS QUE FALTABAN PARA QUE LEA TUS CARPETAS

# Ruta base
BASE_DIR = Path(__file__).resolve().parent.parent

# 🚀 ESTAS DOS LÍNEAS SON LA SOLUCIÓN PRINCIPAL: LE DICES A PYTHON "OYE, AQUÍ ESTÁN LOS CÓDIGOS"
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))


# Seguridad
SECRET_KEY = 'django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
DEBUG = True
ALLOWED_HOSTS = []


# 📱 LISTA DE APPS: AHORA SIMPLE, SENCILLA Y FUNCIONANDO
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ✅ NOMBRES SIMPLES, TAL COMO LOS CREAMOS
    'users',
    'students',
    'companies',
    'agreements',
    'hours_records',
    'evaluations',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

# 🎨 PLANTILLAS (CORREGIDO PARA TU UBICACIÓN)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mysite' / 'templates'],  # 👅 APUNTA DONDE TÚ LOS TIENES
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# 🗄️ BASE DE DATOS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 🔐 CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# 🌐 IDIOMA
LANGUAGE_CODE = 'es-PE'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True


# 📂 ESTÁTICOS (CORREGIDO PARA TU UBICACIÓN)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'mysite' / 'static', # 👅 APUNTA DONDE TÚ LOS TIENES
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ⚠️ USUARIO: AHORA SIMPLE
AUTH_USER_MODEL = 'users.User'