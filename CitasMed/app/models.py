from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from datetime import datetime

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)  # NUEVO: formato +51987654321
    metodo_contacto_preferido = db.Column(db.Enum('email', 'sms'), default='email') 
    fecha_nacimiento = db.Column(db.Date, nullable=True)  
    genero = db.Column(db.Enum('masculino', 'femenino', 'otro'), nullable=True)  
    password_hash = db.Column(db.String(256))
    
    ROL_CHOICES = (
        ('paciente', 'Paciente'),
        ('medico', 'Medico'),
        ('admin', 'Admin'),
    )
    rol = db.Column(db.String(10), nullable=False)

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    estado_verificacion = db.Column(db.String(10), nullable=False, default='aprobado')
    
    mensajes_enviados = db.relationship('Mensaje', foreign_keys='Mensaje.usuario_id', backref='remitente', lazy='dynamic')
    
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
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<Usuario {self.username}>'

class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    especialidad = db.Column(db.String(100), nullable=False)
    licencia_medica = db.Column(db.String(50))
    
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
    
    recordatorio_enviado = db.Column(db.Boolean, default=False)
    metodo_recordatorio = db.Column(db.Enum('email', 'sms', 'none'), default='none')
    urgencia = db.Column(db.Enum('baja', 'media', 'alta'), default='media')
    canal_consulta = db.Column(db.Enum('presencial', 'virtual'), default='presencial')
    duracion_estimada = db.Column(db.Integer, default=30)  # minutos
    
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    
    paciente = db.relationship('Usuario', backref='citas')
    medico = db.relationship('Medico', backref='citas')
    
    mensajes = db.relationship('Mensaje', backref='cita', lazy='dynamic')
    historiales_medicos = db.relationship('HistorialMedico', backref='cita', lazy='dynamic')
    triage = db.relationship('Triage', backref='cita', uselist=False)

    def __repr__(self):
        return f'<Cita {self.id}>'

class Disponibilidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    medico = db.relationship('Medico', backref='disponibilidades')
    dia_semana = db.Column(db.Integer, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    def __repr__(self):
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        return f'{self.medico.usuario.username} - {dias[self.dia_semana]}: {self.hora_inicio} a {self.hora_fin}'

class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('cita.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow)
    leido = db.Column(db.Boolean, default=False)
    tipo = db.Column(db.Enum('texto', 'archivo', 'sistema'), default='texto')
    archivo_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return f'<Mensaje {self.id} - Cita {self.cita_id}>'

class HistorialMedico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medico.id'), nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('cita.id'), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    tipo = db.Column(db.Enum('consulta', 'seguimiento', 'emergencia'), default='consulta')
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)
    medicamentos_recetados = db.Column(db.Text)
    notas_medicas = db.Column(db.Text)
    archivos_adjuntos = db.Column(db.JSON)

    paciente = db.relationship('Usuario', foreign_keys=[paciente_id])
    medico = db.relationship('Medico', foreign_keys=[medico_id])

    def __repr__(self):
        return f'<HistorialMedico {self.id} - Paciente {self.paciente_id}>'

class Triage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('cita.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cuestionario = db.Column(db.JSON, nullable=False)
    puntuacion_urgencia = db.Column(db.Integer, default=0)
    recomendaciones = db.Column(db.Text)
    fecha_completado = db.Column(db.DateTime, default=datetime.utcnow)

    paciente = db.relationship('Usuario', foreign_keys=[paciente_id])

    def __repr__(self):
        return f'<Triage {self.id} - Cita {self.cita_id}>'

class Notificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo = db.Column(db.Enum('recordatorio_cita', 'confirmacion', 'cancelacion', 'mensaje', 'sistema'))
    titulo = db.Column(db.String(200), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_leido = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.Enum('pendiente', 'enviado', 'leido', 'fallido'), default='pendiente')
    metodo = db.Column(db.Enum('email', 'sms', 'push'), nullable=False)

    usuario = db.relationship('Usuario', foreign_keys=[usuario_id])

    def __repr__(self):
        return f'<Notificacion {self.id} - {self.tipo}>'
    
class SolicitudMedico(db.Model):
    __tablename__ = 'solicitud_medico'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)
    especialidad = db.Column(db.String(100), nullable=False)
    licencia_medica = db.Column(db.String(50), nullable=False)
    institucion = db.Column(db.String(200), nullable=False)
    experiencia_anos = db.Column(db.String(20), nullable=False)
    biografia = db.Column(db.Text, nullable=False)
    url_licencia = db.Column(db.String(500))
    url_identidad = db.Column(db.String(500))
    url_cv = db.Column(db.String(500))
    estado = db.Column(db.Enum('pendiente', 'aprobada', 'rechazada'), default='pendiente')
    notas_admin = db.Column(db.Text)
    
    usuario = db.relationship('Usuario', backref=db.backref('solicitudes_medico', lazy=True))