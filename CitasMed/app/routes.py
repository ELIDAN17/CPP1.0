# en app/routes.py
from datetime import datetime, time, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from .models import Usuario, Cita, Disponibilidad, Medico, Mensaje, HistorialMedico, Notificacion, SolicitudMedico
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import current_user
from flask_mail import Message
from . import mail
import re

def validar_telefono(numero_completo):
    """Valida formato internacional: +51987654321"""
    patron = r'^\+\d{10,15}$'  # + seguido de 10-15 dígitos
    return bool(re.match(patron, numero_completo))

def formatear_telefono(codigo_pais, numero):
    """Combina código de país y número"""
    # Remover espacios y caracteres especiales
    numero_limpio = re.sub(r'[^\d]', '', numero)
    return f"+{codigo_pais}{numero_limpio}"

# Creamos un "Blueprint" para organizar nuestras rutas
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        rol = request.form.get('rol')

        # NUEVO: Obtener datos de teléfono
        codigo_pais = request.form.get('codigo_pais', '+51')  # Perú por defecto
        numero_telefono = request.form.get('telefono', '').strip()

        # Validar y formatear teléfono
        if numero_telefono:
            telefono_completo = formatear_telefono(codigo_pais, numero_telefono)
            if not validar_telefono(telefono_completo):
                flash('Formato de teléfono inválido. Use el formato internacional.')
                return redirect(url_for('main.registro'))
        else:
            telefono_completo = None

        # Crear usuario con teléfono
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            telefono=telefono_completo, 
            rol=rol
        )

        # Creamos una nueva instancia del usuario
        nuevo_usuario = Usuario(username=username, email=email, rol=rol)
        nuevo_usuario.set_password(password) # Usamos el método seguro

        # --- LÓGICA DE VERIFICACIÓN ---
        if rol == 'medico':
            nuevo_usuario.estado_verificacion = 'pendiente'
        else:
            # Los pacientes se aprueban automáticamente
            nuevo_usuario.estado_verificacion = 'aprobado'
        # --- FIN DE LA LÓGICA ---
        
        # Guardamos en la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Por favor, inicia sesión.')
        
        # Redirigimos a la página de inicio (o a una de login en el futuro)
        return redirect(url_for('main.index'))

    # Si es GET, solo mostramos el formulario
    return render_template('registro.html')

# --- NUEVA RUTA DE LOGIN ---
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()

        # Verificamos si el usuario existe y la contraseña es correcta
        if user and user.check_password(password):
            # Verificamos si la cuenta está aprobada
            if user.estado_verificacion != 'aprobado':
                flash('Tu cuenta está pendiente de aprobación.')
                return redirect(url_for('main.login'))
            
            login_user(user)
            # Redirigimos al dashboard después de un login exitoso
            return redirect(url_for('main.dashboard'))
        else:
            flash('Usuario o contraseña incorrectos.')
            return redirect(url_for('main.login'))
    return render_template('login.html')

# --- NUEVA RUTA DE LOGOUT ---
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# --- PANEL DE ADMINISTRADOR ---
@main.route('/admin')
@login_required
def admin_panel():
    # 1. Proteger la ruta: solo los admins pueden entrar
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))

    # 2. Obtener la lista de médicos pendientes
    medicos_pendientes = Usuario.query.filter_by(rol='medico', estado_verificacion='pendiente').all()
    
    from datetime import datetime, date
    
    total_usuarios = Usuario.query.count()
    total_medicos = Usuario.query.filter_by(rol='medico', estado_verificacion='aprobado').count()
    
    # Citas de hoy
    hoy = date.today()
    citas_hoy = Cita.query.filter(
        db.func.date(Cita.fecha_hora) == hoy,
        Cita.estado == 'programada'
    ).count()
    
    # Solicitudes pendientes (médicos pendientes)
    solicitudes_pendientes = len(medicos_pendientes)
    
    return render_template('admin.html', 
                         medicos_pendientes=medicos_pendientes,
                         total_usuarios=total_usuarios,
                         total_medicos=total_medicos,
                         citas_hoy=citas_hoy,
                         solicitudes_pendientes=solicitudes_pendientes)
  

# --- RUTA PARA APROBAR MÉDICOS ---
@main.route('/admin/aprobar/<int:medico_id>')
@login_required
def aprobar_medico(medico_id):
    # Proteger la ruta de nuevo
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))

    # Buscar al médico por su ID
    medico = Usuario.query.get(medico_id)
    if medico:
        # Cambiar su estado y guardar en la BD
        medico.estado_verificacion = 'aprobado'
        db.session.commit()
        flash(f'El médico {medico.username} ha sido aprobado.')
    else:
        flash('Médico no encontrado.')

    # Redirigir de vuelta al panel de admin
    return redirect(url_for('main.admin_panel'))

@main.route('/admin/usuarios')
@login_required
def gestionar_usuarios():
    # Verificamos que sea un admin
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))
    
    # Obtenemos todos los usuarios, ordenados por ID
    usuarios = Usuario.query.order_by(Usuario.id.asc()).all()
    return render_template('gestionar_usuarios.html', usuarios=usuarios)

@main.route('/admin/usuario/editar/<int:usuario_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    # Verificar que el usuario actual es un administrador
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))

    usuario_a_editar = Usuario.query.get_or_404(usuario_id)

    if request.method == 'POST':
        # Actualizamos los datos del usuario con la información del formulario
        usuario_a_editar.username = request.form.get('username')
        usuario_a_editar.email = request.form.get('email')
        usuario_a_editar.rol = request.form.get('rol')
        
        db.session.commit()
        flash('Usuario actualizado con éxito.')
        return redirect(url_for('main.gestionar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario_a_editar)

@main.route('/admin/usuario/eliminar/<int:usuario_id>', methods=['POST'])
@login_required
def eliminar_usuario(usuario_id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('main.dashboard'))

    usuario_a_eliminar = Usuario.query.get_or_404(usuario_id)

    if usuario_a_eliminar.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta.', 'danger')
        return redirect(url_for('main.gestionar_usuarios'))

    try:
        username = usuario_a_eliminar.username
        
        # VERIFICAR si tiene citas futuras como médico
        if usuario_a_eliminar.medico:
            citas_futuras = Cita.query.filter(
                Cita.medico_id == usuario_a_eliminar.medico.id,
                Cita.fecha_hora > datetime.now(),
                Cita.estado == 'programada'
            ).count()
            
            if citas_futuras > 0:
                flash(f'No se puede eliminar: tiene {citas_futuras} citas futuras programadas.', 'warning')
                return redirect(url_for('main.gestionar_usuarios'))
        
        # ELIMINACIÓN (tu código actual)
        Cita.query.filter_by(paciente_id=usuario_id).delete()
        
        if usuario_a_eliminar.medico:
            Cita.query.filter_by(medico_id=usuario_a_eliminar.medico.id).delete()
            db.session.delete(usuario_a_eliminar.medico)
        
        db.session.delete(usuario_a_eliminar)
        db.session.commit()
        flash(f'Usuario "{username}" eliminado correctamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar: {str(e)}', 'danger')

    return redirect(url_for('main.gestionar_usuarios'))

@main.route('/dashboard')
@login_required # Este decorador protege la página
def dashboard():
    # Si el usuario es un admin, lo redirigimos a su panel especial
    if current_user.rol == 'admin':
        return redirect(url_for('main.admin_panel'))
    
    citas = []
    if current_user.rol == 'paciente':
        # Buscamos las citas del paciente
        citas = Cita.query.filter_by(paciente_id=current_user.id).order_by(Cita.fecha_hora.asc()).all()
    
    # Si es médico, lo llevamos a su dashboard (que por ahora solo tiene un enlace)
    elif current_user.rol == 'medico':
        citas = Cita.query.filter_by(medico_id=current_user.medico.id).order_by(Cita.fecha_hora.asc()).all()
    
    if current_user.rol == 'paciente':
        citas = Cita.query.filter_by(paciente_id=current_user.id).order_by(Cita.fecha_hora.asc()).all()
    
    # Pasamos información sobre si puede solicitar ser médico
    puede_solicitar_medico = (
        current_user.rol == 'paciente' and 
        current_user.estado_verificacion == 'aprobado'
    )
    
    # Pasamos las citas a la nueva plantilla del dashboard
    return render_template('dashboard.html', citas=citas, puede_solicitar_medico=puede_solicitar_medico)



@main.route('/medico/horario', methods=['GET', 'POST'])
@login_required
def gestionar_horario():
    # Proteger la ruta para que solo entren médicos
    if current_user.rol != 'medico':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))
    
    # Lógica para añadir un nuevo horario (POST)
    if request.method == 'POST':
        dia_semana = request.form.get('dia_semana')
        hora_inicio_str = request.form.get('hora_inicio')
        hora_fin_str = request.form.get('hora_fin')

        # Convertimos el texto a objetos de tiempo
        hora_inicio = time.fromisoformat(hora_inicio_str)
        hora_fin = time.fromisoformat(hora_fin_str)

        # Creamos la nueva disponibilidad
        nueva_disponibilidad = Disponibilidad(
            medico_id=current_user.medico.id,
            dia_semana=int(dia_semana),
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )
        db.session.add(nueva_disponibilidad)
        db.session.commit()
        flash('Nuevo horario añadido con éxito.')
        return redirect(url_for('main.gestionar_horario'))

    # Lógica para mostrar los horarios existentes (GET)
    horarios = Disponibilidad.query.filter_by(medico_id=current_user.medico.id).order_by(Disponibilidad.dia_semana).all()
    return render_template('horario_medico.html', horarios=horarios)

@main.route('/medicos')
@login_required
def listar_medicos():
    # Buscamos los perfiles de médico cuyos usuarios asociados estén aprobados
    medicos_aprobados = Medico.query.join(Usuario).filter(Usuario.estado_verificacion == 'aprobado').all()
    return render_template('medicos.html', medicos=medicos_aprobados)

# --- RUTA PARA VER PERFIL Y HORARIOS DE UN MÉDICO ---
@main.route('/medico/<int:medico_id>')
@login_required
def perfil_medico(medico_id):
    medico = Medico.query.get_or_404(medico_id)
    
    # --- LÓGICA PARA CALCULAR HORARIOS DISPONIBLES ---
    
    # 1. Definir el intervalo de las citas (ej. 30 minutos)
    intervalo_cita = timedelta(minutes=30)
    
    # 2. Obtener la disponibilidad base del médico y las citas ya agendadas
    disponibilidades = medico.disponibilidades
    citas_agendadas = Cita.query.filter(Cita.medico_id == medico_id, Cita.fecha_hora >= datetime.now()).all()
    
    # Crear un set con las horas ya ocupadas para una búsqueda rápida
    horas_ocupadas = {cita.fecha_hora for cita in citas_agendadas}
    
    horarios_libres = []
    
    # 3. Generar turnos para los próximos 14 días
    hoy = datetime.now().date()
    for i in range(14):
        dia_actual = hoy + timedelta(days=i)
        dia_semana_actual = dia_actual.weekday() # Lunes=0, Martes=1, ...
        
        for d in disponibilidades:
            if d.dia_semana == dia_semana_actual:
                # Generamos los posibles turnos para este día
                hora_turno = datetime.combine(dia_actual, d.hora_inicio)
                hora_fin = datetime.combine(dia_actual, d.hora_fin)
                
                while hora_turno < hora_fin:
                    # Si el turno es en el futuro y no está en las horas ocupadas, lo añadimos
                    if hora_turno > datetime.now() and hora_turno not in horas_ocupadas:
                        horarios_libres.append(hora_turno)
                    
                    hora_turno += intervalo_cita
    
    # --- FIN DE LA LÓGICA ---
    
    return render_template('perfil_medico.html', medico=medico, horarios_libres=horarios_libres)

# --- RUTA PARA AGENDAR Y CONFIRMAR LA CITA ---
@main.route('/agendar/<int:medico_id>', methods=['GET', 'POST'])
@login_required
def agendar(medico_id):
    # Asegurarnos de que solo los pacientes puedan agendar
    if current_user.rol != 'paciente':
        flash('Solo los pacientes pueden agendar citas.')
        return redirect(url_for('main.listar_medicos'))

    medico = Medico.query.get_or_404(medico_id)
    slot_str = request.args.get('slot')
    
    if not slot_str:
        flash('Error: No se ha seleccionado un horario.')
        return redirect(url_for('main.perfil_medico', medico_id=medico_id))

    # Convertimos el texto del slot a un objeto datetime
    slot_dt = datetime.fromisoformat(slot_str)

    if request.method == 'POST':
        # Lógica para crear la cita
        motivo = request.form.get('motivo_consulta', 'Consulta general')
        if not motivo: motivo = 'Consulta General'
        nueva_cita = Cita(
            paciente_id=current_user.id,
            medico_id=medico.id,
            fecha_hora=slot_dt,
            estado='programada',
            motivo_consulta=motivo # Puedes añadir un campo para esto en el futuro
        )
        db.session.add(nueva_cita)
        db.session.commit()
        
        try:
            msg = Message(
                'Confirmación de Cita Médica',
                sender='tu_correo@gmail.com', # <-- El mismo correo que en config.py
                recipients=[current_user.email] # <-- Se envía al email del paciente
            )
            msg.html = render_template(
                'email/confirmacion_cita.html',
                paciente=current_user,
                medico=medico,
                cita=nueva_cita
            )
            mail.send(msg)
            flash('¡Tu cita ha sido agendada con éxito! Se ha enviado una confirmación a tu correo.')
        except Exception as e:
            # Si el correo falla, la cita ya está guardada. Solo informamos del error del correo.
            flash(f'¡Tu cita ha sido agendada con éxito! Sin embargo, no se pudo enviar el correo de confirmación. Error: {e}')
        # --- FIN DE LA LÓGICA DEL CORREO ---
        
        return redirect(url_for('main.dashboard'))

    # Si es GET, mostramos la página de confirmación
    return render_template('confirmar_cita.html', medico=medico, slot=slot_dt)


# --- RUTA PARA CANCELAR UNA CITA ---
@main.route('/cita/cancelar/<int:cita_id>')
@login_required
def cancelar_cita(cita_id):
    # Buscamos la cita por su ID
    cita = Cita.query.get_or_404(cita_id)

    # Verificamos que el usuario que intenta cancelar sea el dueño de la cita
    if cita.paciente_id != current_user.id:
        flash('No tienes permiso para cancelar esta cita.')
        return redirect(url_for('main.dashboard'))
    
    # Cambiamos el estado y guardamos
    cita.estado = 'cancelada'
    db.session.commit()
    
    flash('La cita ha sido cancelada con éxito.')
    return redirect(url_for('main.dashboard'))


@main.route('/medico/perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil_medico():
    if current_user.rol != 'medico':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))
    
    medico = current_user.medico # Obtenemos el perfil del médico logueado
    if request.method == 'POST':
        medico.biografia = request.form.get('biografia')
        medico.foto_perfil = request.form.get('foto_perfil')
        db.session.commit()
        flash('Tu perfil ha sido actualizado con éxito.')
        return redirect(url_for('main.dashboard'))

    return render_template('editar_perfil_medico.html', medico=medico)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Solicitud de Reseteo de Contraseña',
                  sender='tu_correo@gmail.com', # El correo configurado en config.py
                  recipients=[user.email])
    msg.body = f'''Para resetear tu contraseña, visita el siguiente enlace:
{url_for('main.reset_password', token=token, _external=True)}

Si no solicitaste este cambio, por favor ignora este correo.
'''
    mail.send(msg)

@main.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        user = Usuario.query.filter_by(email=email).first()
        if user:
            send_reset_email(user)
        flash('Si existe una cuenta con ese correo, se ha enviado un enlace para resetear la contraseña.')
        return redirect(url_for('main.login'))
    return render_template('reset_password_request.html')

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = Usuario.verify_reset_token(token)
    if user is None:
        flash('El token es inválido o ha expirado.')
        return redirect(url_for('main.reset_password_request'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        user.set_password(password)
        db.session.commit()
        flash('Tu contraseña ha sido actualizada. Ya puedes iniciar sesión.')
        return redirect(url_for('main.login'))
        
    return render_template('reset_password.html')

# Añadir estas nuevas rutas al archivo existente routes.py

@main.route('/cita/<int:cita_id>/chat')
@login_required
def chat_cita(cita_id):
    # Verificar que el usuario tiene acceso a esta cita
    cita = Cita.query.get_or_404(cita_id)
    
    # Solo el paciente o médico de la cita pueden acceder
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.id:
        flash('No tienes acceso a este chat.')
        return redirect(url_for('main.dashboard'))
    
    if current_user.rol == 'medico' and cita.medico_id != current_user.medico.id:
        flash('No tienes acceso a este chat.')
        return redirect(url_for('main.dashboard'))
    
    # Obtener mensajes existentes
    mensajes = Mensaje.query.filter_by(cita_id=cita_id).order_by(Mensaje.fecha_hora.asc()).all()
    
    return render_template('chat_cita.html', cita=cita, mensajes=mensajes)

@main.route('/cita/<int:cita_id>/enviar_mensaje', methods=['POST'])
@login_required
def enviar_mensaje(cita_id):
    # Verificar acceso similar a la ruta anterior
    cita = Cita.query.get_or_404(cita_id)
    
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    if current_user.rol == 'medico' and cita.medico_id != current_user.medico.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    mensaje_texto = request.form.get('mensaje', '').strip()
    
    if mensaje_texto:
        nuevo_mensaje = Mensaje(
            cita_id=cita_id,
            usuario_id=current_user.id,
            mensaje=mensaje_texto,
            tipo='texto'
        )
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        # Marcar como no leído para el otro usuario
        # (lógica simple: el remitente ve su mensaje como leído, el otro no)
        
        return jsonify({
            'success': True,
            'mensaje_id': nuevo_mensaje.id,
            'fecha_hora': nuevo_mensaje.fecha_hora.strftime('%H:%M'),
            'usuario_nombre': current_user.username
        })
    
    return jsonify({'error': 'Mensaje vacío'}), 400

@main.route('/cita/<int:cita_id>/mensajes')
@login_required
def obtener_mensajes(cita_id):
    # Verificar acceso
    cita = Cita.query.get_or_404(cita_id)
    
    if current_user.rol == 'paciente' and cita.paciente_id != current_user.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    if current_user.rol == 'medico' and cita.medico_id != current_user.medico.id:
        return jsonify({'error': 'No autorizado'}), 403
    
    # Obtener mensajes desde un ID específico (para updates en tiempo real)
    desde_id = request.args.get('desde_id', 0, type=int)
    
    mensajes = Mensaje.query.filter(
        Mensaje.cita_id == cita_id,
        Mensaje.id > desde_id
    ).order_by(Mensaje.fecha_hora.asc()).all()
    
    # Marcar mensajes como leídos si el usuario actual no es el remitente
    for mensaje in mensajes:
        if mensaje.usuario_id != current_user.id and not mensaje.leido:
            mensaje.leido = True
    db.session.commit()
    
    mensajes_data = []
    for msg in mensajes:
        mensajes_data.append({
            'id': msg.id,
            'mensaje': msg.mensaje,
            'fecha_hora': msg.fecha_hora.strftime('%H:%M'),
            'usuario_id': msg.usuario_id,
            'usuario_nombre': msg.remitente.username,
            'es_mio': msg.usuario_id == current_user.id,
            'leido': msg.leido
        })
    
    return jsonify({'mensajes': mensajes_data})

# Agregar en routes.py
@main.route('/cita/<int:cita_id>/completar')
@login_required
def completar_cita(cita_id):
    if current_user.rol != 'medico':
        flash('Solo los médicos pueden completar citas.')
        return redirect(url_for('main.dashboard'))
    
    cita = Cita.query.get_or_404(cita_id)
    
    # Verificar que el médico es el dueño de esta cita
    if cita.medico_id != current_user.medico.id:
        flash('No tienes permiso para esta acción.')
        return redirect(url_for('main.dashboard'))
    
    cita.estado = 'completada'
    db.session.commit()
    
    flash('Cita marcada como completada.')
    return redirect(url_for('main.dashboard'))

# Agregar en routes.py - Funcionalidades médicas avanzadas

@main.route('/cita/<int:cita_id>/historial', methods=['GET', 'POST'])
@login_required
def gestionar_historial(cita_id):
    # Verificar que es médico y tiene acceso
    if current_user.rol != 'medico':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))
    
    cita = Cita.query.get_or_404(cita_id)
    if cita.medico_id != current_user.medico.id:
        flash('No tienes acceso a esta cita.')
        return redirect(url_for('main.dashboard'))
    
    # Buscar historial existente o crear uno nuevo
    historial = HistorialMedico.query.filter_by(cita_id=cita_id).first()
    
    if request.method == 'POST':
        if not historial:
            historial = HistorialMedico(
                paciente_id=cita.paciente_id,
                medico_id=current_user.medico.id,
                cita_id=cita_id
            )
            db.session.add(historial)
        
        # Actualizar campos del historial
        historial.diagnostico = request.form.get('diagnostico', '')
        historial.tratamiento = request.form.get('tratamiento', '')
        historial.medicamentos_recetados = request.form.get('medicamentos', '')
        historial.notas_medicas = request.form.get('notas_medicas', '')
        historial.tipo = request.form.get('tipo', 'consulta')
        
        db.session.commit()
        flash('Historial médico actualizado correctamente.')
        return redirect(url_for('main.dashboard'))
    
    return render_template('historial_medico.html', 
                         cita=cita, 
                         historial=historial,
                         paciente=cita.paciente)

@main.route('/paciente/<int:paciente_id>/historial')
@login_required
def ver_historial_paciente(paciente_id):
    # Verificar que es médico
    if current_user.rol != 'medico':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))
    
    paciente = Usuario.query.get_or_404(paciente_id)
    
    # Obtener todo el historial del paciente
    historiales = HistorialMedico.query.filter_by(paciente_id=paciente_id).order_by(HistorialMedico.fecha_creacion.desc()).all()
    
    return render_template('historial_completo.html', 
                         paciente=paciente, 
                         historiales=historiales)

@main.route('/cita/<int:cita_id>/iniciar_consulta')
@login_required
def iniciar_consulta_virtual(cita_id):
    # Para consultas virtuales - cambiar estado
    if current_user.rol != 'medico':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))
    
    cita = Cita.query.get_or_404(cita_id)
    if cita.medico_id != current_user.medico.id:
        flash('No tienes acceso a esta cita.')
        return redirect(url_for('main.dashboard'))
    
    cita.estado = 'en_consulta'
    cita.canal_consulta = 'virtual'
    db.session.commit()
    
    flash('Consulta virtual iniciada. El paciente puede unirse.')
    return redirect(url_for('main.chat_cita', cita_id=cita_id))

@main.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        # Campos para TODOS los usuarios
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        current_user.metodo_contacto_preferido = request.form.get('metodo_contacto', 'email')
        current_user.fecha_nacimiento = request.form.get('fecha_nacimiento') or None
        current_user.genero = request.form.get('genero') or None
        
        # Biografía y foto para TODOS (nuevos campos que necesitarías agregar al modelo Usuario)
        # current_user.biografia = request.form.get('biografia', '')  # Si decides agregar este campo
        # current_user.foto_perfil = request.form.get('foto_perfil', '')  # Si decides agregar este campo
        
        # Teléfono
        codigo_pais = request.form.get('codigo_pais', '51')
        numero_telefono = request.form.get('telefono', '').strip()
        
        if numero_telefono:
            telefono_completo = formatear_telefono(codigo_pais, numero_telefono)
            if validar_telefono(telefono_completo):
                current_user.telefono = telefono_completo
            else:
                flash('Formato de teléfono inválido. Use solo números.', 'danger')
                return redirect(url_for('main.editar_perfil'))
        else:
            current_user.telefono = None
        
        # Campos ESPECÍFICOS para MÉDICOS
        if current_user.rol == 'medico' and current_user.medico:
            current_user.medico.biografia = request.form.get('biografia', '')
            current_user.medico.foto_perfil = request.form.get('foto_perfil', '')
        
        db.session.commit()
        flash('Perfil actualizado correctamente.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('editar_perfil.html')

@main.route('/solicitar_medico', methods=['GET', 'POST'])
@login_required
def solicitar_medico():
    if current_user.rol != 'paciente':
        flash('Ya tienes un rol asignado.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Verificar si ya tiene solicitud pendiente
    if current_user.solicitud_medico and current_user.solicitud_medico.estado == 'pendiente':
        flash('Ya tienes una solicitud médica pendiente de revisión.', 'info')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        # Obtener datos del formulario
        especialidad = request.form.get('especialidad')
        licencia_medica = request.form.get('licencia_medica')
        institucion = request.form.get('institucion')
        experiencia_anos = request.form.get('experiencia_anos')
        biografia = request.form.get('biografia')
        url_licencia = request.form.get('url_licencia')
        url_identidad = request.form.get('url_identidad')
        url_cv = request.form.get('url_cv')
        
        # Crear nueva solicitud
        nueva_solicitud = SolicitudMedico(
            usuario_id=current_user.id,
            especialidad=especialidad,
            licencia_medica=licencia_medica,
            institucion=institucion,
            experiencia_anos=experiencia_anos,
            biografia=biografia,
            url_licencia=url_licencia,
            url_identidad=url_identidad,
            url_cv=url_cv
        )
        
        db.session.add(nueva_solicitud)
        db.session.commit()
        
        flash('¡Solicitud enviada! Será revisada por nuestro equipo en hasta 48 horas.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('solicitud_medico.html')


# Agregar en routes.py
@main.route('/perfil')
@login_required
def ver_perfil():
    return render_template('ver_perfil.html')


# Agregar en routes.py
from datetime import datetime, timedelta

def enviar_recordatorios_citas():
    """Envía recordatorios automáticos de citas 24h antes"""
    try:
        # Calcular fecha/hora para recordatorios (24h antes)
        ahora = datetime.now()
        recordatorio_min = ahora + timedelta(hours=23)  # 23-25h antes
        recordatorio_max = ahora + timedelta(hours=25)
        
        # Buscar citas que cumplan:
        # - Estén entre 23-25 horas en el futuro
        # - Estado 'programada'
        # - Recordatorio no enviado
        citas_pendientes = Cita.query.filter(
            Cita.fecha_hora.between(recordatorio_min, recordatorio_max),
            Cita.estado == 'programada',
            Cita.recordatorio_enviado == False
        ).all()
        
        recordatorios_enviados = 0
        
        for cita in citas_pendientes:
            try:
                # Enviar email de recordatorio
                msg = Message(
                    'Recordatorio de Cita Médica',
                    sender='tu_correo@gmail.com',
                    recipients=[cita.paciente.email]
                )
                msg.html = render_template(
                    'email/recordatorio_cita.html',
                    paciente=cita.paciente,
                    medico=cita.medico,
                    cita=cita
                )
                mail.send(msg)
                
                # Marcar como enviado
                cita.recordatorio_enviado = True
                cita.metodo_recordatorio = 'email'
                recordatorios_enviados += 1
                
                # Registrar en tabla de notificaciones
                notificacion = Notificacion(
                    usuario_id=cita.paciente.id,
                    tipo='recordatorio_cita',
                    titulo='Recordatorio de Cita',
                    mensaje=f'Recordatorio enviado para cita con Dr. {cita.medico.usuario.username}',
                    metodo='email',
                    estado='enviado'
                )
                db.session.add(notificacion)
                
            except Exception as e:
                print(f"Error enviando recordatorio para cita {cita.id}: {e}")
                # Registrar error en notificaciones
                notificacion = Notificacion(
                    usuario_id=cita.paciente.id,
                    tipo='recordatorio_cita',
                    titulo='Error en Recordatorio',
                    mensaje=f'Error al enviar recordatorio: {str(e)}',
                    metodo='email',
                    estado='fallido'
                )
                db.session.add(notificacion)
        
        db.session.commit()
        return f"Recordatorios enviados: {recordatorios_enviados}"
        
    except Exception as e:
        print(f"Error en sistema de recordatorios: {e}")
        return f"Error: {str(e)}"
    


