# en app/models.py

from . import db  # La instancia de la BD creada en __init__.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    # Añadimos 'admin' a las opciones de rol
    ROL_CHOICES = (
        ('paciente', 'Paciente'),
        ('medico', 'Medico'),
        ('admin', 'Admin'), # <-- AÑADIDO
    )
    rol = db.Column(db.String(10), nullable=False)

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    estado_verificacion = db.Column(db.String(10), nullable=False, default='aprobado')
    
    # --- NUEVOS MÉTODOS PARA EL TOKEN ---
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)
    
    # Nuevo método para establecer la contraseña
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Nuevo método para verificar la contraseña
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f'<Usuario {self.username}>'
    
    

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidad = db.Column(db.String(100), nullable=False)
    licencia_medica = db.Column(db.String(50))
    
    # Relación con Usuario
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    biografia = db.Column(db.Text, nullable=True)
    foto_perfil = db.Column(db.String(200), nullable=True)
    usuario = db.relationship('Usuario', backref=db.backref('medico', uselist=False))

    def __repr__(self):
        return f'<Medico {self.usuario.username}>'

class Cita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo_consulta = db.Column(db.Text)
    estado = db.Column(db.String(12), default='programada')
    
    # Relaciones
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    
    paciente = db.relationship('Usuario', backref='citas')
    medico = db.relationship('Medico', backref='citas')

    def __repr__(self):
        return f'<Cita {self.id}>'


class Disponibilidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Relación con el médico
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    medico = db.relationship('Medico', backref='disponibilidades')

    # Días de la semana (0=Lunes, 1=Martes, ..., 6=Domingo)
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    def __repr__(self):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return f'{self.medico.usuario.username} - {dias[self.dia_semana]}: {self.hora_inicio} a {self.hora_fin}'    
    