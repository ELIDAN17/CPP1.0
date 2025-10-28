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
        email = request.form.get('email').strip().lower()  # 🔥 Normalizar email
        password = request.form.get('password')
        rol = request.form.get('rol')

        # 🔥🔥🔥 VALIDACIÓN GMAIL COMPLETA - REEMPLAZA TU CÓDIGO ACTUAL
        if not email.endswith('@gmail.com'):
            flash('Solo se permiten correos de Gmail (@gmail.com) para las notificaciones.', 'danger')
            return redirect(url_for('main.registro'))

        # 🔥 NUEVO: Validación estricta del usuario Gmail
        usuario_gmail = email.split('@')[0]
        
        # Validar longitud
        if len(usuario_gmail) < 6:
            flash('El usuario de Gmail debe tener al menos 6 caracteres.', 'danger')
            return redirect(url_for('main.registro'))
        
        if len(usuario_gmail) > 30:
            flash('El usuario de Gmail no puede tener más de 30 caracteres.', 'danger')
            return redirect(url_for('main.registro'))
        
        # Validar caracteres permitidos
        if not re.match(r'^[a-z0-9.]+$', usuario_gmail):
            flash('Solo se permiten letras, números y puntos en el usuario Gmail.', 'danger')
            return redirect(url_for('main.registro'))
        
        # Validar puntos
        if usuario_gmail.startswith('.') or usuario_gmail.endswith('.'):
            flash('El usuario Gmail no puede empezar ni terminar con punto.', 'danger')
            return redirect(url_for('main.registro'))
        
        if '..' in usuario_gmail:
            flash('No se permiten puntos consecutivos en el usuario Gmail.', 'danger')
            return redirect(url_for('main.registro'))

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

        # 🔥 VERIFICAR SI EMAIL YA EXISTE - AGREGAR ESTO TAMBIÉN
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este correo electrónico ya está registrado.', 'danger')
            return redirect(url_for('main.registro'))

        # Crear usuario con teléfono
        nuevo_usuario = Usuario(
            username=username,
            email=email,
            telefono=telefono_completo, 
            rol=rol
        )

        # Creamos una nueva instancia del usuario
       #nuevo_usuario = Usuario(username=username, email=email, rol=rol)
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

@main.route('/verificar_usuarios')
@login_required  
def verificar_usuarios():
    if current_user.rol != 'admin':
        return "Solo para admin"
    
    usuarios = Usuario.query.all()
    html = "<h1>USUARIOS EN BASE DE DATOS</h1>"
    
    for usuario in usuarios:
        html += f"""
        <div style='border: 2px solid #333; margin: 10px; padding: 10px;'>
            <h3>ID: {usuario.id} - {usuario.username}</h3>
            <p>Email: {usuario.email}</p>
            <p>Rol: <strong>{usuario.rol}</strong></p>
            <p>Estado: <strong>{usuario.estado_verificacion}</strong></p>
            <p>Teléfono: {usuario.telefono}</p>
        </div>
        """
    
    return html


@main.route('/validar-email', methods=['POST'])
def validar_email_tiempo_real():
    """Valida email en tiempo real SIN dependencias externas"""
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    # 1. Validar que no esté vacío
    if not email:
        return jsonify({
            'valido': False,
            'mensaje': '📧 Ingresa tu correo Gmail'
        })
    
    # 2. Validar formato Gmail básico
    if not email.endswith('@gmail.com'):
        return jsonify({
            'valido': False,
            'mensaje': '❌ Solo se permiten correos Gmail (@gmail.com)'
        })
    
    # 3. 🔥 VALIDACIÓN ESTRICTA del usuario Gmail
    usuario = email.split('@')[0]
    
    # Reglas de Gmail oficiales:
    # - Mínimo 6 caracteres, máximo 30
    # - Solo letras, números y puntos
    # - No puede empezar o terminar con punto
    # - No puede tener puntos consecutivos
    
    if len(usuario) < 6:
        return jsonify({
            'valido': False,
            'mensaje': '❌ El usuario debe tener al menos 6 caracteres'
        })
    
    if len(usuario) > 30:
        return jsonify({
            'valido': False, 
            'mensaje': '❌ El usuario no puede tener más de 30 caracteres'
        })
    
    # Solo caracteres permitidos
    if not re.match(r'^[a-z0-9.]+$', usuario):
        return jsonify({
            'valido': False,
            'mensaje': '❌ Solo letras, números y puntos (sin espacios ni símbolos)'
        })
    
    # No puede empezar/terminar con punto
    if usuario.startswith('.') or usuario.endswith('.'):
        return jsonify({
            'valido': False,
            'mensaje': '❌ El usuario no puede empezar ni terminar con punto'
        })
    
    # No puntos consecutivos
    if '..' in usuario:
        return jsonify({
            'valido': False,
            'mensaje': '❌ No se permiten puntos consecutivos'
        })
    
    # 4. Validar si ya existe en NUESTRA base de datos
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        return jsonify({
            'valido': False, 
            'mensaje': '❌ Este correo ya está registrado en nuestro sistema'
        })
    
    # 5. ✅ CORREO VÁLIDO
    return jsonify({
        'valido': True,
        'mensaje': '✅ Correo Gmail válido y disponible'
    })
    
@main.route('/validar-email-editar', methods=['POST'])
@login_required
def validar_email_editar():
    """Valida email al editar perfil (considera email original)"""
    data = request.get_json()
    nuevo_email = data.get('email', '').strip().lower()
    email_original = data.get('email_original', '').strip().lower()
    
    # 1. Si es el mismo email, es válido
    if nuevo_email == email_original:
        return jsonify({
            'valido': True,
            'mensaje': '✅ Correo actual (sin cambios)'
        })
    
    # 2. Validar que no esté vacío
    if not nuevo_email:
        return jsonify({
            'valido': False,
            'mensaje': '📧 Ingresa tu correo Gmail'
        })
    
    # 3. Validar formato Gmail básico
    if not nuevo_email.endswith('@gmail.com'):
        return jsonify({
            'valido': False,
            'mensaje': '❌ Solo se permiten correos Gmail (@gmail.com)'
        })
    
    # 4. Validación estricta del usuario Gmail
    usuario = nuevo_email.split('@')[0]
    
    if len(usuario) < 6:
        return jsonify({
            'valido': False,
            'mensaje': '❌ El usuario debe tener al menos 6 caracteres'
        })
    
    if len(usuario) > 30:
        return jsonify({
            'valido': False, 
            'mensaje': '❌ El usuario no puede tener más de 30 caracteres'
        })
    
    if not re.match(r'^[a-z0-9.]+$', usuario):
        return jsonify({
            'valido': False,
            'mensaje': '❌ Solo letras, números y puntos'
        })
    
    if usuario.startswith('.') or usuario.endswith('.'):
        return jsonify({
            'valido': False,
            'mensaje': '❌ No puede empezar ni terminar con punto'
        })
    
    if '..' in usuario:
        return jsonify({
            'valido': False,
            'mensaje': '❌ No se permiten puntos consecutivos'
        })
    
    # 5. Validar si ya existe en nuestra BD (excluyendo el usuario actual)
    usuario_existente = Usuario.query.filter(
        Usuario.email == nuevo_email,
        Usuario.id != current_user.id
    ).first()
    
    if usuario_existente:
        return jsonify({
            'valido': False, 
            'mensaje': '❌ Este correo ya está registrado por otro usuario'
        })
    
    # 6. ✅ CORREO VÁLIDO
    return jsonify({
        'valido': True,
        'mensaje': '✅ Nuevo correo Gmail válido y disponible'
    })

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
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))

    # Buscar al médico por su ID
    medico = Usuario.query.get(medico_id)
    if medico and medico.rol == 'medico' and medico.estado_verificacion == 'pendiente':
        # Cambiar su estado a aprobado
        medico.estado_verificacion = 'aprobado'
        
        # ✅ VERIFICAR y crear el perfil médico
        perfil_existente = Medico.query.filter_by(usuario_id=medico.id).first()
        if not perfil_existente:
            # Buscar datos de la solicitud
            solicitud = SolicitudMedico.query.filter_by(usuario_id=medico.id).first()
            
            perfil_medico = Medico(
                usuario_id=medico.id,
                especialidad=solicitud.especialidad if solicitud else 'General',
                biografia=solicitud.biografia if solicitud else '',
                licencia_medica=solicitud.licencia_medica if solicitud else ''
            )
            db.session.add(perfil_medico)
        
        db.session.commit()
        flash(f'El médico {medico.username} ha sido aprobado.')
    else:
        flash('Médico no encontrado o ya está aprobado.')

    return redirect(url_for('main.admin_panel'))

@main.route('/admin/rechazar/<int:medico_id>')
@login_required
def rechazar_medico(medico_id):
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))

    # Buscar al médico por su ID
    medico = Usuario.query.get(medico_id)
    if medico and medico.rol == 'medico' and medico.estado_verificacion == 'pendiente':
        # Cambiar el rol de vuelta a paciente y estado a aprobado
        medico.rol = 'paciente'
        medico.estado_verificacion = 'aprobado'
        
        # Marcar la solicitud como rechazada si existe
        if hasattr(medico, 'solicitud_medico') and medico.solicitud_medico:
            medico.solicitud_medico.estado = 'rechazada'
            medico.solicitud_medico.fecha_revision = datetime.now()
            medico.solicitud_medico.admin_revisor_id = current_user.id
        
        db.session.commit()
        flash(f'La solicitud de {medico.username} ha sido rechazada.')
    else:
        flash('Médico no encontrado o ya fue procesado.')

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
    # 1. Definir el intervalo de las citas a 1 HORA
    intervalo_cita = timedelta(minutes=60)
    
    # 2. Obtener la disponibilidad base del médico y las citas ya agendadas
    disponibilidades = medico.disponibilidades
    citas_agendadas = Cita.query.filter(Cita.medico_id == medico_id, Cita.fecha_hora >= datetime.now()).all()
    
    # Crear un set con las horas ya ocupadas para una búsqueda rápida
    horas_ocupadas = {cita.fecha_hora for cita in citas_agendadas}
    
    horarios_libres = []
    
    # 3. Solo usar los días específicos que el médico configuró
    hoy = datetime.now().date()
    
    # Crear un conjunto de días únicos que el médico tiene configurados
    dias_configurados = set()
    for disponibilidad in disponibilidades:
        dias_configurados.add(disponibilidad.dia_semana)
    
    # Para cada día de la semana configurado, generar horarios para los próximos 7 días
    for i in range(7):  # Reducido a 7 días para mayor precisión
        dia_actual = hoy + timedelta(days=i)
        dia_semana_actual = dia_actual.weekday()
        
        # ✅ SOLO procesar si el médico configuró este día de la semana
        if dia_semana_actual in dias_configurados:
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
    
    # Ordenar los horarios por fecha y hora
    horarios_libres.sort()
    
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

@main.route('/cita/<int:cita_id>/reprogramar', methods=['GET', 'POST'])
@login_required
def reprogramar_cita(cita_id):
    """Permite al médico reprogramar una cita - VERSIÓN CORREGIDA"""
    # Verificar que sea médico
    if current_user.rol != 'medico' or not current_user.medico:
        flash('Acceso no autorizado. Solo para médicos.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    cita = Cita.query.get_or_404(cita_id)
    
    # Verificar que el médico es dueño de esta cita
    if cita.medico_id != current_user.medico.id:
        flash('No tienes permiso para esta acción.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            # Obtener la nueva fecha y hora
            nueva_fecha_str = request.form.get('nueva_fecha')
            nueva_hora_str = request.form.get('nueva_hora')
            
            if not nueva_fecha_str or not nueva_hora_str:
                flash('Debes seleccionar una fecha y hora válidas.', 'danger')
                return redirect(url_for('main.reprogramar_cita', cita_id=cita_id))
            
            # Combinar fecha y hora
            nueva_fecha_hora = datetime.strptime(f"{nueva_fecha_str} {nueva_hora_str}", '%Y-%m-%d %H:%M')
            
            # Verificar que la nueva fecha sea en el futuro
            if nueva_fecha_hora <= datetime.now():
                flash('La nueva fecha debe ser en el futuro.', 'danger')
                return redirect(url_for('main.reprogramar_cita', cita_id=cita_id))
            
            # Guardar fecha original
            fecha_original = cita.fecha_hora
            
            # Actualizar cita
            cita.fecha_hora = nueva_fecha_hora
            cita.estado = 'reprogramada'
            db.session.commit()
            
            flash('✅ Cita reprogramada exitosamente.', 'success')
            return redirect(url_for('main.dashboard'))
            
        except ValueError as e:
            flash('Formato de fecha/hora inválido.', 'danger')
            return redirect(url_for('main.reprogramar_cita', cita_id=cita_id))
        except Exception as e:
            flash('Error al reprogramar la cita.', 'danger')
            return redirect(url_for('main.reprogramar_cita', cita_id=cita_id))
    
    # Si es GET, mostrar formulario de reprogramación
    # Generar horarios disponibles simples para los próximos 7 días
    horarios_disponibles = []
    hoy = datetime.now().date()
    
    for i in range(1, 8):  # Próximos 7 días
        dia_actual = hoy + timedelta(days=i)
        
        # Horarios fijos: 9:00, 11:00, 15:00, 17:00
        horarios_del_dia = [
            datetime.combine(dia_actual, time(9, 0)),
            datetime.combine(dia_actual, time(11, 0)),
            datetime.combine(dia_actual, time(15, 0)),
            datetime.combine(dia_actual, time(17, 0))
        ]
        
        for horario in horarios_del_dia:
            # Verificar que no haya citas en ese horario
            cita_existente = Cita.query.filter(
                Cita.medico_id == current_user.medico.id,
                Cita.fecha_hora == horario,
                Cita.estado.in_(['programada', 'reprogramada'])
            ).first()
            
            if not cita_existente and horario > datetime.now():
                horarios_disponibles.append(horario)
    
    return render_template('reprogramar_cita.html', 
                         cita=cita, 
                         horarios_disponibles=horarios_disponibles)
    
    
@main.route('/cita/<int:cita_id>/marcar_no_show', methods=['POST'])
@login_required
def marcar_no_show(cita_id):
    """Marca que el paciente no llegó a la cita - VERSIÓN CORREGIDA"""
    # Verificar que sea médico
    if current_user.rol != 'medico' or not current_user.medico:
        flash('Acceso no autorizado. Solo para médicos.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    cita = Cita.query.get_or_404(cita_id)
    
    # Verificar que el médico es dueño de esta cita
    if cita.medico_id != current_user.medico.id:
        flash('No tienes permiso para esta acción.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    try:
        # Marcar como "no show" (paciente no llegó)
        cita.estado = 'no_show'
        db.session.commit()
        flash('✅ Cita marcada como "paciente no llegó".', 'warning')
    except Exception as e:
        flash('Error al actualizar la cita.', 'danger')
    
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

@main.route('/cita/<int:cita_id>/completar')
@login_required
def completar_cita(cita_id):
    """Marca una cita como completada - VERSIÓN MEJORADA"""
    try:
        # Verificar que sea médico
        if current_user.rol != 'medico' or not current_user.medico:
            flash('Acceso no autorizado. Solo para médicos.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Buscar la cita
        cita = Cita.query.get_or_404(cita_id)
        
        # Verificar permisos
        if cita.medico_id != current_user.medico.id:
            flash('No tienes permiso para esta acción.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Validar estado actual
        if cita.estado not in ['programada', 'reprogramada']:
            flash(f'No se puede completar una cita en estado: {cita.estado}', 'warning')
            return redirect(url_for('main.dashboard'))
        
        # Verificar que la cita ya pasó (opcional)
        if cita.fecha_hora > datetime.now():
            flash('⚠️ Esta cita aún no ha llegado. ¿Estás seguro de completarla?', 'warning')
            # Podrías agregar confirmación adicional aquí
        
        # Cambiar estado
        cita.estado = 'completada'
        db.session.commit()
        
        flash('✅ Cita marcada como completada correctamente.', 'success')
        
    except Exception as e:
        db.session.rollback()
        print(f"Error completando cita: {e}")
        flash('❌ Error al completar la cita.', 'danger')
    
    return redirect(url_for('main.dashboard'))


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
        # Obtener el nuevo email del formulario
        nuevo_email = request.form.get('email').strip().lower()
        
        # 🔥 SOLO validar si el email CAMBIÓ
        if nuevo_email != current_user.email:
            # Validar que sea Gmail
            if not nuevo_email.endswith('@gmail.com'):
                flash('Solo se permiten correos de Gmail (@gmail.com) para las notificaciones.', 'danger')
                return redirect(url_for('main.editar_perfil'))
            
            # 🔥 Validación estricta del usuario Gmail (solo si cambió)
            usuario_gmail = nuevo_email.split('@')[0]
            
            if len(usuario_gmail) < 6:
                flash('El usuario de Gmail debe tener al menos 6 caracteres.', 'danger')
                return redirect(url_for('main.editar_perfil'))
            
            if len(usuario_gmail) > 30:
                flash('El usuario de Gmail no puede tener más de 30 caracteres.', 'danger')
                return redirect(url_for('main.editar_perfil'))
            
            if not re.match(r'^[a-z0-9.]+$', usuario_gmail):
                flash('Solo se permiten letras, números y puntos en el usuario Gmail.', 'danger')
                return redirect(url_for('main.editar_perfil'))
            
            if usuario_gmail.startswith('.') or usuario_gmail.endswith('.'):
                flash('El usuario Gmail no puede empezar ni terminar con punto.', 'danger')
                return redirect(url_for('main.editar_perfil'))
            
            if '..' in usuario_gmail:
                flash('No se permiten puntos consecutivos en el usuario Gmail.', 'danger')
                return redirect(url_for('main.editar_perfil'))
            
            # 🔥 Validar si el NUEVO email ya existe (excluyendo el usuario actual)
            usuario_existente = Usuario.query.filter(
                Usuario.email == nuevo_email,
                Usuario.id != current_user.id  # Excluir al usuario actual
            ).first()
            
            if usuario_existente:
                flash('Este correo electrónico ya está registrado por otro usuario.', 'danger')
                return redirect(url_for('main.editar_perfil'))

        # Campos para TODOS los usuarios
        current_user.username = request.form.get('username')
        current_user.email = nuevo_email  # Usar el email validado
        current_user.metodo_contacto_preferido = request.form.get('metodo_contacto', 'email')
        current_user.fecha_nacimiento = request.form.get('fecha_nacimiento') or None
        current_user.genero = request.form.get('genero') or None
        
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
    solicitud_existente = SolicitudMedico.query.filter_by(usuario_id=current_user.id, estado='pendiente').first()
    if solicitud_existente:
        flash('Ya tienes una solicitud médica pendiente de revisión.', 'info')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            especialidad = request.form.get('especialidad')
            licencia_medica = request.form.get('licencia_medica')
            institucion = request.form.get('institucion')
            experiencia_anos = request.form.get('experiencia_anos')
            biografia = request.form.get('biografia')
            url_licencia = request.form.get('url_licencia')
            url_identidad = request.form.get('url_identidad')
            url_cv = request.form.get('url_cv')
            
            # ✅ SOLUCIÓN: Obtener el objeto REAL de la base de datos
            usuario_db = Usuario.query.get(current_user.id)
            
            # ✅ CAMBIAR ROL en la base de datos
            usuario_db.rol = 'medico'
            usuario_db.estado_verificacion = 'pendiente'
            
            # Crear solicitud
            nueva_solicitud = SolicitudMedico(
                usuario_id=usuario_db.id,
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
            
            # ✅ ACTUALIZAR la sesión del usuario
            login_user(usuario_db)
            
            flash('¡Solicitud enviada correctamente! Será revisada por nuestro equipo.', 'success')
            return redirect(url_for('main.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al enviar solicitud: {str(e)}', 'danger')
            return redirect(url_for('main.solicitar_medico'))
    
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
    


