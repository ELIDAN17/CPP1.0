# en app/routes.py
from datetime import datetime, time, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Usuario, Cita, Disponibilidad, Medico
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from flask_login import current_user
from flask_mail import Message
from . import mail

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
    
    # 3. Mostrar la página de admin con la lista
    return render_template('admin.html', medicos_pendientes=medicos_pendientes)

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
    # Paso 1: Verificar que el usuario actual es un administrador
    if current_user.rol != 'admin':
        flash('Acceso no autorizado.')
        return redirect(url_for('main.dashboard'))

    # Paso 2: Encontrar al usuario que se quiere eliminar
    usuario_a_eliminar = Usuario.query.get_or_404(usuario_id)

    # No permitir que el admin se elimine a sí mismo
    if usuario_a_eliminar.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta de administrador.')
        return redirect(url_for('main.gestionar_usuarios'))

    # Paso 3: Lógica de seguridad para médicos
    if usuario_a_eliminar.rol == 'medico':
        # Buscamos si el médico tiene citas asociadas
        citas_existentes = Cita.query.filter_by(medico_id=usuario_a_eliminar.medico.id).first()
        if citas_existentes:
            flash('ERROR: Este médico no puede ser eliminado porque tiene citas agendadas. Por favor, cancela o reasigna sus citas primero.')
            return redirect(url_for('main.gestionar_usuarios'))
        
        # Si no tiene citas, también eliminamos su perfil de médico
        db.session.delete(usuario_a_eliminar.medico)

    # Paso 4: Eliminar al usuario y guardar cambios
    db.session.delete(usuario_a_eliminar)
    db.session.commit()

    flash(f'El usuario "{usuario_a_eliminar.username}" ha sido eliminado con éxito.')
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
    
    # Pasamos las citas a la nueva plantilla del dashboard
    return render_template('dashboard.html', citas=citas)


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