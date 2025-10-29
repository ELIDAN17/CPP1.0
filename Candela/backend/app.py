# app.py - Servidor Backend para la Candelaria
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import func, event
#import mysql.connector
import hashlib

app = Flask(__name__)
CORS(app)

# Configuración de XAMPP
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_NAME = "candelaria_db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

# Configuracion de postgreSQL
#DB_USER = "ingeniero_adminJMP"
#DB_PASSWORD = "Admin123FULLcandela#"
#DB_HOST = "localhost"
#DB_PORT = "5432"
#DB_NAME = "ingeniero_candelaJMP_db"
#app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS DE BASE DE DATOS ---

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Enum('admin', 'juez', 'publico'))

class Festividad(db.Model):
    __tablename__ = 'Festividades'
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(255), nullable=False)

class Concurso(db.Model):
    __tablename__ = 'Concursos'
    id = db.Column(db.Integer, primary_key=True)
    festividad_id = db.Column(db.Integer, db.ForeignKey('Festividades.id'))
    nombre_concurso = db.Column(db.String(255), nullable=False)
    fecha_hora_inicio = db.Column(db.DateTime, nullable=False)

class Conjunto(db.Model):
    __tablename__ = 'Conjuntos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    clasificacion = db.Column(db.Enum('Originaria', 'Traje de Luces', 'Indefinido'))

class CriterioCalificacion(db.Model):
    __tablename__ = 'Criterios_Calificacion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    
class PuntajeDetalle(db.Model):
    __tablename__ = 'Puntajes_Detalle'
    id = db.Column(db.Integer, primary_key=True)
    participacion_id = db.Column(db.Integer, db.ForeignKey('Participaciones.id'))
    criterio_id = db.Column(db.Integer, db.ForeignKey('Criterios_Calificacion.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))
    puntaje = db.Column(db.Numeric(5, 2), nullable=False)

class Participacion(db.Model):
    __tablename__ = 'Participaciones'
    id = db.Column(db.Integer, primary_key=True)
    concurso_id = db.Column(db.Integer, db.ForeignKey('Concursos.id'), nullable=False)
    conjunto_id = db.Column(db.Integer, db.ForeignKey('Conjuntos.id'), nullable=False)
    orden_presentacion = db.Column(db.Integer, nullable=False)
    tipo_danza = db.Column(db.String(100), nullable=False)
    votos_publico = db.Column(db.Integer, default=0)
    
    # Relaciones
    conjunto = db.relationship('Conjunto')
    puntajes = db.relationship('PuntajeDetalle', backref='participacion', lazy='dynamic')
    
    @property
    def puntaje_total(self):
        total = db.session.query(func.sum(PuntajeDetalle.puntaje)).filter(
            PuntajeDetalle.participacion_id == self.id
        ).scalar()
        return round(float(total or 0.00), 2)

# Tabla temporal para control de votos por IP
class VotoTemporal(db.Model):
    __tablename__ = 'Votos_Temporal'
    id = db.Column(db.Integer, primary_key=True)
    ip_hash = db.Column(db.String(32), nullable=False, unique=True)
    participation_id = db.Column(db.Integer, db.ForeignKey('Participaciones.id'))
    nombre_votante = db.Column(db.String(255), nullable=False)
    fecha_voto = db.Column(db.DateTime, default=datetime.utcnow)
    participacion = db.relationship('Participacion', foreign_keys=[participation_id])
# --- FUNCIONES DE UTILIDAD ---

def serialize_participacion(p, criterios_map):
    """Serializa la participación, incluyendo puntajes dinámicos por criterio."""
    puntajes_criterio = {}
    for detalle in p.puntajes.all():
        criterio_nombre = criterios_map.get(detalle.criterio_id, 'Desconocido')
        puntajes_criterio[criterio_nombre.lower()] = str(detalle.puntaje)

    # ✅ CORRECCIÓN: Incluir tipo_danza directamente en el nivel principal
    return {
        'id_participacion': p.id,
        'orden_concurso': p.orden_presentacion,
        'puntaje_coreografia': puntajes_criterio.get('coreografía', None),
        'puntaje_traje': puntajes_criterio.get('traje', None),
        'puntaje_musica': puntajes_criterio.get('música', None),
        'puntaje_total': str(p.puntaje_total),
        'votos_publico': p.votos_publico,
        'tipo_danza': p.tipo_danza,  # ✅ ESTA LÍNEA ES CLAVE
        'conjunto': {
            'nombre': p.conjunto.nombre,
            'clasificacion': p.conjunto.clasificacion
        }
    }
    
# --- NUEVA FUNCIÓN PARA CALCULAR TIEMPO HASTA FECHA ---
def calcular_tiempo_hasta_fecha(fecha_objetivo):
    """Calcula días, horas, minutos hasta una fecha específica"""
    ahora = datetime.now()
    
    if ahora >= fecha_objetivo:
        return "EN CURSO 🎭"
    
    diferencia = fecha_objetivo - ahora
    dias = diferencia.days
    segundos_restantes = diferencia.seconds
    horas = segundos_restantes // 3600
    minutos = (segundos_restantes % 3600) // 60
    
    if dias > 30:
        meses = dias // 30
        dias_restantes = dias % 30
        if meses > 1:
            return f"Faltan {meses} meses y {dias_restantes} días"
        else:
            return f"Falta 1 mes y {dias_restantes} días"
    elif dias > 0:
        if dias == 1:
            return f"Mañana en {horas}h {minutos}m"
        else:
            return f"Faltan {dias} días, {horas}h {minutos}m"
    elif horas > 0:
        return f"Faltan {horas}h {minutos}m"
    else:
        return f"Faltan {minutos} minutos"

def predict_schedule(participaciones, hora_inicio=None):
    """Calcula el horario estimado de presentación considerando múltiples días."""
    horarios = {}
    
    # Obtener la fecha de inicio del concurso
    concurso = Concurso.query.first()
    fecha_inicio_concurso = concurso.fecha_hora_inicio if concurso else None
    
    if not hora_inicio and fecha_inicio_concurso:
        hora_inicio = fecha_inicio_concurso
    elif not hora_inicio:
        hora_inicio = datetime(2025, 2, 1, 8, 0, 0)
    
    # ✅ CORRECCIÓN: Configurar horarios diferentes por día
    hora_inicio_dia1 = hora_inicio  # Día 1 usa la hora del concurso (ej: 17:00)
    hora_inicio_dias_siguientes = hora_inicio.replace(hour=8, minute=0, second=0)  # Días 2+ a las 08:00
    
    tiempo_presentacion_min = 15
    max_presentaciones_por_dia = 40
    
    tiempo_acumulado = timedelta(minutes=0)
    dia_actual = 0
    presentaciones_hoy = 0
    
    for p in sorted(participaciones, key=lambda x: x.orden_presentacion):
        # Usar hora de inicio correcta según el día
        if dia_actual == 0:
            # Día 1: Usar hora exacta del concurso
            hora_base = hora_inicio_dia1
        else:
            # Días 2, 3, etc.: Usar 08:00 AM
            hora_base = hora_inicio_dias_siguientes + timedelta(days=dia_actual)
        
        # Calcular hora estimada
        hora_estimada = hora_base + tiempo_acumulado
        
        #  Verificar límites del día
        hora_fin_jornada = hora_base.replace(hour=23, minute=59, second=59)
        
        if hora_estimada > hora_fin_jornada or presentaciones_hoy >= max_presentaciones_por_dia:
            # Pasar al siguiente día
            dia_actual += 1
            presentaciones_hoy = 0
            tiempo_acumulado = timedelta(minutes=0)
            
            # Actualizar hora base para nuevo día
            if dia_actual == 0:
                hora_base = hora_inicio_dia1
            else:
                hora_base = hora_inicio_dias_siguientes + timedelta(days=dia_actual)
            
            hora_estimada = hora_base + tiempo_acumulado
        
        horarios[p.id] = {
            'hora': hora_estimada.strftime('%H:%M'),
            'fecha_completa': hora_estimada,
            'dia': dia_actual + 1,
            'estado': calcular_estado_participacion(p, hora_estimada, participaciones, fecha_inicio_concurso)
        }
        
        tiempo_acumulado += timedelta(minutes=tiempo_presentacion_min)
        presentaciones_hoy += 1
        
        # ✅ DEBUG: Verificar horarios calculados
        #print(f"🎭 {p.conjunto.nombre} - Día {dia_actual + 1} - Hora: {hora_estimada.strftime('%H:%M')}")
        
    return horarios

def calcular_estado_participacion(participacion_actual, hora_estimada, todas_participaciones, fecha_inicio_concurso=None):
    """Calcula el estado correcto considerando múltiples días y fecha de inicio"""
    ahora = datetime.now()
    
    # Si hay fecha de inicio del concurso, verificar si ya comenzó
    if fecha_inicio_concurso:
        if ahora < fecha_inicio_concurso:
            return calcular_tiempo_hasta_fecha(fecha_inicio_concurso)
    
    # Ordenar todas las participaciones por orden
    participaciones_ordenadas = sorted(todas_participaciones, key=lambda x: x.orden_presentacion)
    
    # Encontrar el índice de la participación actual
    indice_actual = None
    for i, p in enumerate(participaciones_ordenadas):
        if p.id == participacion_actual.id:
            indice_actual = i
            break
    
    if indice_actual is None:
        return "Por Definir"
    
    # ✅ CORRECCIÓN: Si la hora estimada YA PASÓ (considerando el día completo) → FINALIZADO
    if ahora >= hora_estimada:
        return "FINALIZADO ✅"
    
    # Si es la primera participación → calcular tiempo hasta su inicio
    if indice_actual == 0:
        tiempo_restante = hora_estimada - ahora
        return formatear_tiempo_espera(tiempo_restante)
    
    # Para participaciones que NO son la primera
    participacion_anterior = participaciones_ordenadas[indice_actual - 1]
    
    # Buscar la hora estimada de la participación anterior
    hora_anterior_estimada = None
    for p in participaciones_ordenadas:
        if p.id == participacion_anterior.id:
            # Aproximar hora anterior (15 minutos antes)
            hora_anterior_estimada = hora_estimada - timedelta(minutes=15)
            break
    
    if not hora_anterior_estimada:
        return "Por Definir"
    
    # ✅ CORRECCIÓN: Si la participación anterior YA TERMINÓ → esta es la próxima
    if ahora >= hora_anterior_estimada:
        tiempo_restante = hora_estimada - ahora
        if tiempo_restante.total_seconds() <= 300:  # 5 minutos
            return "¡PRONTO! 🏃‍♂️"
        return formatear_tiempo_espera(tiempo_restante)
    else:
        # La anterior todavía no termina → mostrar tiempo entre turnos
        tiempo_entre_turnos = hora_estimada - hora_anterior_estimada
        return f"En {formatear_tiempo_espera(tiempo_entre_turnos)}"
    
       
def formatear_tiempo_espera(timedelta_obj):
    """Formatea el tiempo de espera en días, horas y minutos"""
    if timedelta_obj.total_seconds() <= 0:
        return "0m"
    
    total_segundos = int(timedelta_obj.total_seconds())
    dias = total_segundos // (24 * 3600)
    horas = (total_segundos % (24 * 3600)) // 3600
    minutos = (total_segundos % 3600) // 60
    
    if dias > 0:
        return f"{dias}d {horas}h {minutos}m"
    elif horas > 0:
        return f"{horas}h {minutos}m"
    else:
        return f"{minutos}m" 

# --- FUNCIONES HELPER NUEVAS ---

def es_admin():
    """Verifica si el usuario actual es admin"""
    username = request.json.get('username') if request.json else request.args.get('username')
    if not username:
        return False
    user = Usuario.query.filter_by(username=username).first()
    return user and user.rol == 'admin'

def get_user_from_request():
    """Obtiene usuario del request"""
    username = request.json.get('username') if request.json else request.args.get('username')
    if username:
        return Usuario.query.filter_by(username=username).first()
    return None

# --- ENDPOINTS ---

@app.route('/api/login', methods=['POST'])
def login():
    """Autentica usuarios admin/jueces."""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        print(f"🔐 Intento de login: usuario='{username}', contraseña='{password}'")
        
        # Buscar usuario en la base de datos
        user = Usuario.query.filter_by(username=username).first()
        
        if user:
            print(f"✅ Usuario encontrado: {user.username}")
            print(f"📝 Contraseña en BD: '{user.password_hash}'")
            print(f"🎭 Rol: {user.rol}")
            print(f"🔍 Comparando: '{password}' == '{user.password_hash}' -> {password == user.password_hash}")
            
            # Verificación directa
            if user.password_hash == password and user.rol in ['admin', 'juez']:
                print("🎉 LOGIN EXITOSO")
                return jsonify({
                    'success': True,
                    'username': user.username,
                    'rol': user.rol
                })
            else:
                print(f"❌ FALLÓ: Contraseña coincide: {password == user.password_hash}, Rol válido: {user.rol in ['admin', 'juez']}")
        
        else:
            print(f"❌ Usuario '{username}' NO encontrado en la BD")
            
        # Listar todos los usuarios para debug
        print("👥 TODOS LOS USUARIOS EN BD:")
        todos_usuarios = Usuario.query.all()
        for u in todos_usuarios:
            print(f"   - {u.username} (rol: {u.rol}) -> contraseña: '{u.password_hash}'")
        
        return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'}), 401
        
    except Exception as e:
        print(f"💥 Error en login: {e}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.route('/api/participaciones/<int:concurso_id>', methods=['GET'])
def get_participaciones(concurso_id):
    """Obtiene todas las participaciones para un concurso - CORREGIDO"""
    try:
        # ✅ Cargar las relaciones necesarias
        participaciones = Participacion.query.filter_by(concurso_id=concurso_id)\
            .join(Conjunto)\
            .order_by(Participacion.orden_presentacion)\
            .all()
        
        criterios = CriterioCalificacion.query.all()
        criterios_map = {c.id: c.nombre for c in criterios}

        data = []
        for p in participaciones:
            participacion_data = serialize_participacion(p, criterios_map)
            data.append(participacion_data)
            
        # ✅ DEBUG: Verificar que las danzas se envían correctamente
        print(f"🎭 Enviando {len(data)} participaciones con danzas:")
        for item in data[:3]:  # Mostrar primeras 3 para debug
            print(f"   #{item['orden_concurso']} - Danza: '{item.get('tipo_danza')}'")
            
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error al obtener participaciones: {e}")
        return jsonify({'error': f'Error interno del servidor: {e}'}), 500
    
    

@app.route('/api/concurso/fecha-inicio', methods=['GET'])
def get_fecha_inicio():
    """Obtiene la fecha de inicio del concurso"""
    try:
        concurso = Concurso.query.first()
        if concurso and concurso.fecha_hora_inicio:
            return jsonify({
                'fecha_inicio': concurso.fecha_hora_inicio.isoformat(),
                'success': True
            })
        return jsonify({'fecha_inicio': None, 'success': False})
    except Exception as e:
        print(f"Error obteniendo fecha inicio: {e}")
        return jsonify({'error': 'Error al obtener fecha'}), 500

@app.route('/api/predecir-horarios/<int:concurso_id>', methods=['GET'])
def get_horarios(concurso_id):
    """Obtiene el horario estimado para cada participación."""
    try:
        participaciones = Participacion.query.filter_by(concurso_id=concurso_id).all()
        
        # Obtener la hora de inicio del concurso
        concurso = Concurso.query.get(concurso_id)
        hora_inicio = concurso.fecha_hora_inicio if concurso else None
        
        horarios = predict_schedule(participaciones, hora_inicio)
        horarios_json = {}
        for part_pid, horario_data in horarios.items():
            horarios_json[part_pid] = {
                'hora': horario_data['hora'],
                'fecha_completa': horario_data['fecha_completa'].isoformat() if 'fecha completa' in horario_data else None,
                'dia': horario_data['dia']
            }

        return jsonify(horarios_json)
    except Exception as e:
        app.logger.error(f"Error al predecir horarios: {e}")
        return jsonify({'error': 'Error al calcular horarios'}), 500

# --- SISTEMA DE VOTOS POR IP CON NOMBRE ---

@app.route('/api/voto/verificar-ip/<int:participacion_id>', methods=['GET'])
def verificar_voto_ip(participacion_id):
    """Verificar si la IP ya votó por esta participación"""
    try:
        user_ip = request.remote_addr
        # Crear un hash único de IP + participación
        ip_hash = hashlib.md5(f"{user_ip}_{participacion_id}".encode()).hexdigest()
        
        # Verificar en la base de datos si ya existe este voto
        voto_existente = VotoTemporal.query.filter_by(ip_hash=ip_hash).first()
        
        return jsonify({'ya_voto': bool(voto_existente)})
    except Exception as e:
        print(f"Error verificando voto: {e}")
        return jsonify({'ya_voto': False})

@app.route('/api/votar-con-nombre/<int:participacion_id>', methods=['POST'])
def votar_con_nombre(participacion_id):
    """Votar con nombre pero controlar por IP"""
    data = request.json
    nombre_votante = data.get('nombre_votante', '').strip()
    
    if not nombre_votante:
        return jsonify({'error': 'Nombre requerido'}), 400
    
    if len(nombre_votante) < 2:
        return jsonify({'error': 'El nombre debe tener al menos 2 caracteres'}), 400

    try:
        user_ip = request.remote_addr
        # Crear hash único
        ip_hash = hashlib.md5(f"{user_ip}_{participacion_id}".encode()).hexdigest()
        
        # Verificar si ya votó desde esta IP
        voto_existente = VotoTemporal.query.filter_by(ip_hash=ip_hash).first()
        
        if voto_existente:
            return jsonify({'error': 'Ya has votado por esta participación desde este dispositivo'}), 400
        
        # Realizar el voto
        participacion = Participacion.query.get(participacion_id)
        if not participacion:
            return jsonify({'error': 'Participación no encontrada'}), 404
        
        participacion.votos_publico += 1
        
        # Guardar el voto en tabla temporal
        nuevo_voto = VotoTemporal(
            ip_hash=ip_hash,
            participacion_id=participacion_id,
            nombre_votante=nombre_votante
        )
        
        db.session.add(nuevo_voto)
        db.session.commit()
        
        criterios = CriterioCalificacion.query.all()
        criterios_map = {c.id: c.nombre for c in criterios}
        
        return jsonify(serialize_participacion(participacion, criterios_map))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al votar: {e}")
        return jsonify({'error': 'Error al procesar el voto'}), 500

@app.route('/api/admin/votos-participacion/<int:participacion_id>', methods=['GET'])
def get_votos_participacion(participacion_id):
    """Obtener lista de votantes para una participación (solo admin)"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    try:
        votos = VotoTemporal.query.filter_by(participacion_id=participacion_id).order_by(VotoTemporal.fecha_voto.desc()).all()
        
        return jsonify([{
            'nombre': voto.nombre_votante,
            'fecha': voto.fecha_voto.isoformat() if voto.fecha_voto else None
        } for voto in votos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/votar/<int:id_participacion>', methods=['POST'])
def votar(id_participacion):
    """Incrementa el contador de votos públicos para una participación."""
    try:
        participacion = Participacion.query.get(id_participacion)
        if not participacion:
            return jsonify({'error': 'Participación no encontrada'}), 404
        
        participacion.votos_publico += 1
        db.session.commit()
        
        criterios = CriterioCalificacion.query.all()
        criterios_map = {c.id: c.nombre for c in criterios}
        
        return jsonify(serialize_participacion(participacion, criterios_map))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al votar: {e}")
        return jsonify({'error': 'Error al procesar el voto'}), 500

@app.route('/api/puntaje/<int:id_participacion>', methods=['POST'])
def actualizar_puntaje(id_participacion):
    """Actualiza o inserta puntajes en Puntajes_Detalle (MODO ADMIN)."""
    data = request.json
    
    username = data.get('username')
    if not username:
        return jsonify({'error': 'No autorizado. Usuario requerido.'}), 401
    
    user = Usuario.query.filter_by(username=username).first()
    if not user or user.rol not in ['admin', 'juez']:
        return jsonify({'error': 'No tiene permisos para editar puntajes'}), 403

    try:
        participacion = Participacion.query.get(id_participacion)
        if not participacion:
            return jsonify({'error': 'Participación no encontrada'}), 404

        updated_count = 0
        
        criterio_map_nombre_a_id = {
            'coreografia': 1,  # Coreografía
            'traje': 2,        # Traje
            'musica': 3        # Música
        }
        
        for key, criterio_id in criterio_map_nombre_a_id.items():
            if key in data and data[key] is not None:
                puntaje_float = float(data[key])
                
                detalle = PuntajeDetalle.query.filter_by(
                    participacion_id=id_participacion, 
                    criterio_id=criterio_id, 
                    usuario_id=user.id
                ).first()
                
                if detalle:
                    detalle.puntaje = puntaje_float
                else:
                    nuevo_detalle = PuntajeDetalle(
                        participacion_id=id_participacion, 
                        criterio_id=criterio_id, 
                        usuario_id=user.id,
                        puntaje=puntaje_float
                    )
                    db.session.add(nuevo_detalle)
                
                updated_count += 1
        
        if updated_count > 0:
            db.session.commit()
            
            criterios = CriterioCalificacion.query.all()
            criterios_map = {c.id: c.nombre for c in criterios}
            
            return jsonify(serialize_participacion(participacion, criterios_map))
        else:
            return jsonify({'error': 'Ningún campo de puntaje válido proporcionado'}), 400

    except ValueError:
        db.session.rollback()
        return jsonify({'error': 'Puntaje inválido. Debe ser un número.'}), 400
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error al actualizar puntaje: {e}")
        return jsonify({'error': 'Error interno del servidor al actualizar el puntaje'}), 500

# --- ENDPOINTS DE ADMINISTRACIÓN NUEVOS ---

@app.route('/api/admin/conjuntos', methods=['GET'])
def get_all_conjuntos():
    """Obtener todos los conjuntos para gestión admin"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    conjuntos = Conjunto.query.all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre,
        'clasificacion': c.clasificacion
    } for c in conjuntos])

@app.route('/api/admin/conjuntos', methods=['POST'])
def crear_conjunto():
    """Crear nuevo conjunto"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    nombre = data.get('nombre')
    clasificacion = data.get('clasificacion')
    
    if not nombre:
        return jsonify({'error': 'Nombre del conjunto requerido'}), 400
    
    if clasificacion not in ['Originaria', 'Traje de Luces', 'Indefinido']:
        return jsonify({'error': 'Clasificación inválida'}), 400
    
    try:
        # Verificar si el conjunto ya existe
        conjunto_existente = Conjunto.query.filter_by(nombre=nombre).first()
        if conjunto_existente:
            return jsonify({'error': 'Ya existe un conjunto con ese nombre'}), 400
        
        nuevo_conjunto = Conjunto(
            nombre=nombre,
            clasificacion=clasificacion
        )
        
        db.session.add(nuevo_conjunto)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'mensaje': 'Conjunto creado exitosamente',
            'conjunto': {
                'id': nuevo_conjunto.id,
                'nombre': nuevo_conjunto.nombre,
                'clasificacion': nuevo_conjunto.clasificacion
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al crear conjunto: {str(e)}'}), 500

@app.route('/api/admin/conjuntos/<int:conjunto_id>', methods=['PUT'])
def editar_conjunto(conjunto_id):
    """Editar conjunto existente"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    nombre = data.get('nombre')
    clasificacion = data.get('clasificacion')
    
    conjunto = Conjunto.query.get(conjunto_id)
    if not conjunto:
        return jsonify({'error': 'Conjunto no encontrado'}), 404
    
    try:
        if nombre:
            conjunto.nombre = nombre
        if clasificacion:
            if clasificacion not in ['Originaria', 'Traje de Luces', 'Indefinido']:
                return jsonify({'error': 'Clasificación inválida'}), 400
            conjunto.clasificacion = clasificacion
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'mensaje': 'Conjunto actualizado exitosamente',
            'conjunto': {
                'id': conjunto.id,
                'nombre': conjunto.nombre,
                'clasificacion': conjunto.clasificacion
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar conjunto: {str(e)}'}), 500

@app.route('/api/admin/concurso/hora-inicio', methods=['PUT'])
def actualizar_hora_inicio():
    """Actualizar hora de inicio del concurso"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    nueva_hora_str = data.get('hora_inicio')
    concurso_id = data.get('concurso_id', 1)
    
    if not nueva_hora_str:
        return jsonify({'error': 'Hora de inicio requerida'}), 400
    
    try:
        # Convertir string a datetime
        nueva_hora = datetime.strptime(nueva_hora_str, '%Y-%m-%d %H:%M:%S')
        
        concurso = Concurso.query.get(concurso_id)
        if not concurso:
            return jsonify({'error': 'Concurso no encontrado'}), 404
        
        concurso.fecha_hora_inicio = nueva_hora
        db.session.commit()
        
        return jsonify({
            'success': True,
            'mensaje': f'Hora de inicio actualizada a: {nueva_hora_str}',
            'nueva_hora': nueva_hora_str
        })
    except ValueError:
        return jsonify({'error': 'Formato de hora inválido. Use: YYYY-MM-DD HH:MM:SS'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar hora: {str(e)}'}), 500

@app.route('/api/admin/participaciones/<int:participacion_id>/danza', methods=['PUT'])
def editar_danza_participacion(participacion_id):
    """Cambiar el tipo de danza de una participación específica"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    nueva_danza = data.get('tipo_danza')
    
    if not nueva_danza:
        return jsonify({'error': 'Tipo de danza requerido'}), 400
    
    participacion = Participacion.query.get(participacion_id)
    if not participacion:
        return jsonify({'error': 'Participación no encontrada'}), 404
    
    participacion.tipo_danza = nueva_danza
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': f'Danza actualizada a: {nueva_danza}',
        'participacion': {
            'id': participacion.id,
            'conjunto_nombre': participacion.conjunto.nombre,
            'tipo_danza': participacion.tipo_danza,
            'orden': participacion.orden_presentacion
        }
    })

@app.route('/api/admin/participaciones/<int:participacion_id>/orden', methods=['PUT'])
def editar_orden_participacion(participacion_id):
    """Cambiar el orden de presentación"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    nuevo_orden = data.get('orden_presentacion')
    
    if nuevo_orden is None or nuevo_orden < 1:
        return jsonify({'error': 'Orden válido requerido'}), 400
    
    participacion = Participacion.query.get(participacion_id)
    if not participacion:
        return jsonify({'error': 'Participación no encontrada'}), 404
    
    # Verificar si el orden ya está ocupado
    orden_existente = Participacion.query.filter_by(
        concurso_id=participacion.concurso_id,
        orden_presentacion=nuevo_orden
    ).first()
    
    if orden_existente and orden_existente.id != participacion_id:
        return jsonify({'error': 'El orden ya está ocupado por otro conjunto'}), 400
    
    participacion.orden_presentacion = nuevo_orden
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': f'Orden actualizado a: {nuevo_orden}',
        'participacion': {
            'id': participacion.id,
            'conjunto_nombre': participacion.conjunto.nombre,
            'orden': participacion.orden_presentacion
        }
    })

@app.route('/api/admin/participaciones', methods=['POST'])
def agregar_participacion():
    """Agregar nueva participación (conjunto al concurso)"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    conjunto_id = data.get('conjunto_id')
    concurso_id = data.get('concurso_id', 1)  # Por defecto concurso 1
    tipo_danza = data.get('tipo_danza', 'Por definir')
    
    if not conjunto_id:
        return jsonify({'error': 'ID de conjunto requerido'}), 400
    
    # Verificar si el conjunto ya participa
    participacion_existente = Participacion.query.filter_by(
        concurso_id=concurso_id,
        conjunto_id=conjunto_id
    ).first()
    
    if participacion_existente:
        return jsonify({'error': 'El conjunto ya está participando'}), 400
    
    # Obtener el último orden para ponerlo al final
    ultima_participacion = Participacion.query.filter_by(concurso_id=concurso_id).order_by(
        Participacion.orden_presentacion.desc()
    ).first()
    
    nuevo_orden = (ultima_participacion.orden_presentacion + 1) if ultima_participacion else 1
    
    nueva_participacion = Participacion(
        concurso_id=concurso_id,
        conjunto_id=conjunto_id,
        orden_presentacion=nuevo_orden,
        tipo_danza=tipo_danza,
        votos_publico=0
    )
    
    db.session.add(nueva_participacion)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': 'Participación agregada exitosamente',
        'participacion': {
            'id': nueva_participacion.id,
            'conjunto_nombre': nueva_participacion.conjunto.nombre,
            'tipo_danza': nueva_participacion.tipo_danza,
            'orden': nueva_participacion.orden_presentacion
        }
    })

@app.route('/api/admin/participaciones/<int:participacion_id>', methods=['DELETE'])
def eliminar_participacion(participacion_id):
    """Eliminar participación (quitar conjunto del concurso)"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    participacion = Participacion.query.get(participacion_id)
    if not participacion:
        return jsonify({'error': 'Participación no encontrada'}), 404
    
    conjunto_nombre = participacion.conjunto.nombre
    
    # Eliminar también los puntajes asociados
    PuntajeDetalle.query.filter_by(participacion_id=participacion_id).delete()
    # Eliminar votos temporales asociados
    VotoTemporal.query.filter_by(participacion_id=participacion_id).delete()
    
    db.session.delete(participacion)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'mensaje': f'Participación de {conjunto_nombre} eliminada'
    })

@app.route('/api/admin/usuarios', methods=['GET'])
def get_usuarios():
    """Solo admin puede ver todos los usuarios"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    usuarios = Usuario.query.all()
    print(f"👥 Usuarios encontrados en BD: {len(usuarios)}") 
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'rol': u.rol
    } for u in usuarios])

@app.route('/api/admin/usuarios/<int:user_id>/rol', methods=['PUT'])
def cambiar_rol_usuario(user_id):
    """Admin puede cambiar roles de usuarios"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    data = request.json
    nuevo_rol = data.get('rol')
    
    if nuevo_rol not in ['admin', 'juez', 'publico']:
        return jsonify({'error': 'Rol inválido'}), 400
    
    usuario = Usuario.query.get(user_id)
    if not usuario:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    usuario.rol = nuevo_rol
    db.session.commit()
    
    return jsonify({'success': True, 'nuevo_rol': nuevo_rol})

@app.route('/api/admin/estadisticas', methods=['GET'])
def get_estadisticas():
    """Estadísticas para el panel admin"""
    if not es_admin():
        return jsonify({'error': 'No autorizado'}), 403
    
    total_usuarios = Usuario.query.count()
    total_jueces = Usuario.query.filter_by(rol='juez').count()
    total_publico = Usuario.query.filter_by(rol='publico').count()
    total_conjuntos = Conjunto.query.count()
    total_participaciones = Participacion.query.count()
    total_votos = db.session.query(func.sum(Participacion.votos_publico)).scalar() or 0
    
    # Conjuntos más votados
    conjuntos_populares = Participacion.query.order_by(Participacion.votos_publico.desc()).limit(5).all()
    
    return jsonify({
        'usuarios': {
            'total': total_usuarios,
            'jueces': total_jueces,
            'publico': total_publico,
            'admins': total_usuarios - total_jueces - total_publico
        },
        'concurso': {
            'total_conjuntos': total_conjuntos,
            'total_participaciones': total_participaciones,
            'total_votos': int(total_votos)
        },
        'mas_votados': [{
            'nombre': p.conjunto.nombre,
            'votos': p.votos_publico,
            'tipo_danza': p.tipo_danza
        } for p in conjuntos_populares]
    })

# --- Endpoint de prueba ---
@app.route('/api/test', methods=['GET'])
def test():
    """Endpoint de prueba."""
    return jsonify({
        'message': '✅ Servidor Flask funcionando correctamente',
        'status': 'Conectado a la base de datos',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print(f"🚀 Flask corriendo en http://127.0.0.1:5000")
    print(f"📊 Endpoint de prueba: http://127.0.0.1:5000/api/test")
    print(f"👥 Participaciones: http://127.0.0.1:5000/api/participaciones/1")
    print(f"🔧 Endpoints Admin:")
    print(f"   - Gestión conjuntos: GET/POST/PUT /api/admin/conjuntos")
    print(f"   - Editar hora inicio: PUT /api/admin/concurso/hora-inicio")
    print(f"   - Editar danza: PUT /api/admin/participaciones/<id>/danza") 
    print(f"   - Editar orden: PUT /api/admin/participaciones/<id>/orden")
    print(f"   - Agregar participación: POST /api/admin/participaciones")
    print(f"   - Eliminar participación: DELETE /api/admin/participaciones/<id>")
    print(f"   - Gestión usuarios: GET /api/admin/usuarios")
    print(f"   - Cambiar roles: PUT /api/admin/usuarios/<id>/rol")
    print(f"   - Estadísticas: GET /api/admin/estadisticas")
    print(f"   - Ver votantes: GET /api/admin/votos-participacion/<id>")
    app.run(debug=True, port=5000)