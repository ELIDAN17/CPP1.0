import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Loader, AlertTriangle, Settings, Users, BarChart3, Edit3, Trash2, Plus, Clock, UserCheck } from 'lucide-react'; 
import './App.css';

function App() {
    
    // --- Estados de la Aplicación ---
    const [participaciones, setParticipaciones] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filtroBusqueda, setFiltroBusqueda] = useState("");
    const [isAdmin, setIsAdmin] = useState(false);
    const [horarios, setHorarios] = useState({});
    const [loadingHorarios, setLoadingHorarios] = useState(true);
    const [fechaConcurso, setFechaConcurso] = useState(null);

    // --- NUEVOS ESTADOS PARA ADMIN ---
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showLogin, setShowLogin] = useState(false);
    const [loginData, setLoginData] = useState({ username: '', password: '' });
    const [showAdminPanel, setShowAdminPanel] = useState(false);
    const [conjuntosDisponibles, setConjuntosDisponibles] = useState([]);
    const [usuarios, setUsuarios] = useState([]);
    const [estadisticas, setEstadisticas] = useState(null);
    
    // --- NUEVOS ESTADOS PARA VOTOS Y ADMIN ---
    const [votanteNombre, setVotanteNombre] = useState('');
    const [showVotoModal, setShowVotoModal] = useState(false);
    const [participacionAVotar, setParticipacionAVotar] = useState(null);
    const [listaVotantes, setListaVotantes] = useState({});
    const [showCrearConjunto, setShowCrearConjunto] = useState(false);
    const [nuevoConjunto, setNuevoConjunto] = useState({ nombre: '', clasificacion: 'Traje de Luces', tipo_danza: 'Morenada' });
    
    const anoAConsultar = 2025;
    const BACKEND_URL = "http://localhost:5000/api"; 
    const ID_CONCURSO = 1; 
     // Lista de danzas disponibles
    const danzas = [
        'Morenada', 'Diablada', 'Caporal', 'Tinkus', 'Sikuris', 
        'Llamerada', 'Kullawada', 'Waca Waca', 'Suri Sikuris', 
        'Auqui Auqui', 'Pujllay', 'Tobas', 'Saya', 'Tuntuna',
        'Tundiques', 'Chacareros', 'Wifalas', 'Kajelos', 'Unucajas',
        'Unkakus', 'Wititi', 'Qashway Soltero', 'Pinquilladas', 
        'Ayarachis'
    ];

    // --- 1. CARGAR DATOS Y HORARIOS ---
    // --- 1. CARGAR DATOS Y HORARIOS ---
useEffect(() => {
    const cargarDatosYHorarios = async () => {
        setLoading(true);
        setLoadingHorarios(true);
        setError(null);
        
        try {
            console.log('🔄 Cargando datos principales...');
            
            // Cargar fecha del concurso PRIMERO
            try {
                const fechaResponse = await axios.get(`${BACKEND_URL}/concurso/fecha-inicio`);
                if (fechaResponse.data.success && fechaResponse.data.fecha_inicio) {
                    setFechaConcurso(new Date(fechaResponse.data.fecha_inicio));
                    console.log('📅 Fecha del concurso cargada:', fechaResponse.data.fecha_inicio);
                }
            } catch (fechaError) {
                console.log('⚠️ No se pudo cargar fecha del concurso:', fechaError);
            }

            // Cargar participaciones
            const resParticipaciones = await axios.get(`${BACKEND_URL}/participaciones/${ID_CONCURSO}`);
            const participacionesCargadas = resParticipaciones.data;
            console.log('📊 Participaciones cargadas:', participacionesCargadas.length);
            
            if (participacionesCargadas.length === 0) {
                setError("No se encontraron participaciones.");
                setLoading(false);
                return;
            }
            
            setParticipaciones(participacionesCargadas.sort((a, b) => a.orden_concurso - b.orden_concurso));
            
            // Cargar horarios
            console.log('🕒 Cargando horarios...');
            const resHorarios = await axios.get(`${BACKEND_URL}/predecir-horarios/${ID_CONCURSO}`);
            console.log('⏰ Horarios cargados:', Object.keys(resHorarios.data).length);
            setHorarios(resHorarios.data);
            
            setLoading(false);
            setLoadingHorarios(false);

        } catch (err) {
            console.error("Error al cargar datos:", err);
            setError("Error al conectar con el servidor");
            setLoading(false);
            setLoadingHorarios(false);
        }
    };
    
    cargarDatosYHorarios();
    
    // Cargar sesión guardada
    const savedUser = localStorage.getItem('adminUser');
    if (savedUser) {
        setIsLoggedIn(true);
        setIsAdmin(true);
        setLoginData(prev => ({ ...prev, username: savedUser }));
        console.log('🔑 Sesión cargada:', savedUser)
    }
}, []); // ✅ SOLO se ejecuta una vez al montar el componente

    // --- FUNCIÓN DE DEBUG PARA VERIFICAR USUARIOS ---
const debugUsuarios = async () => {
    try {
        console.log('🔍 Debug: Verificando usuarios en el backend...');
        
        // Verificar directamente el endpoint de usuarios
        const response = await axios.get(`${BACKEND_URL}/admin/usuarios`, { 
            params: { username: loginData.username } 
        });
        
        console.log('📊 Respuesta del backend:', response.data);
        console.log('👥 Usuarios recibidos:', response.data);
        console.log('🔑 Usuario logueado:', loginData.username);
        
        if (response.data && response.data.length > 0) {
            alert(`✅ Se encontraron ${response.data.length} usuarios:\n\n${
                response.data.map(u => `• ${u.username} (${u.rol})`).join('\n')
            }`);
        } else {
            alert('❌ No se encontraron usuarios en la base de datos');
        }
        
    } catch (error) {
        console.error('💥 Error en debug:', error);
        if (error.response) {
            console.log('📡 Respuesta del error:', error.response.data);
            alert(`❌ Error del servidor: ${error.response.data.error || error.response.status}`);
        } else {
            alert('❌ Error de conexión con el servidor');
        }
    }
};

    // --- 2. SISTEMA DE VOTOS POR IP CON NOMBRE ---
    const verificarPuedeVotar = async (id_participacion) => {
        try {
            const response = await axios.get(`${BACKEND_URL}/voto/verificar-ip/${id_participacion}`);
            return !response.data.ya_voto;
        } catch (error) {
            console.error("Error verificando voto:", error);
            return true; // En caso de error, permitir votar
        }
    };

    const abrirModalVoto = async (id_participacion) => {
        const puedeVotar = await verificarPuedeVotar(id_participacion);
        
        if (!puedeVotar) {
            alert('❌ Ya has votado por esta participación desde este dispositivo');
            return;
        }
        
        setParticipacionAVotar(id_participacion);
        setShowVotoModal(true);
    };

    const procesarVoto = async () => {
        if (!votanteNombre.trim()) {
            alert('❌ Por favor ingrese su nombre para votar');
            return;
        }

        if (votanteNombre.trim().length < 2) {
            alert('❌ Por favor ingrese un nombre válido (mínimo 2 caracteres)');
            return;
        }

        try {
            const response = await axios.post(`${BACKEND_URL}/votar-con-nombre/${participacionAVotar}`, {
                nombre_votante: votanteNombre.trim()
            });
            
            // Actualizar estado inmediatamente
            actualizarParticipacionEnEstado(response.data);
            
            setShowVotoModal(false);
            setVotanteNombre('');
            alert('✅ ¡Voto registrado correctamente! Gracias por participar.');
        } catch (error) {
            if (error.response?.data?.error) {
                alert(`❌ ${error.response.data.error}`);
            } else {
                alert('❌ Error al registrar el voto');
            }
            console.error("Error al votar:", error);
        }
    };

    // --- 3. FUNCIÓN PARA ACTUALIZAR PUNTAJES (CON LOGIN) ---
    const handleActualizarPuntaje = async (id_participacion, tipoPuntaje) => {
        if (!isAdmin) {
            setShowLogin(true);
            return;
        }
        
        const nuevoPuntaje = window.prompt(`MODO ADMIN:\nIngrese el nuevo puntaje para "${tipoPuntaje}":`);
        if (nuevoPuntaje === null || nuevoPuntaje.trim() === "") return;
        
        const puntajeNumerico = parseFloat(nuevoPuntaje);
        if (isNaN(puntajeNumerico) || puntajeNumerico < 0) {
            window.alert("Error: Ingrese solo números positivos.");
            return;
        }
        
        try {
            const response = await axios.post(`${BACKEND_URL}/puntaje/${id_participacion}`, {
                [tipoPuntaje]: puntajeNumerico,
                username: loginData.username
            });
            
            actualizarParticipacionEnEstado(response.data);
            alert('✅ Puntaje actualizado correctamente');
        } catch (error) {
            if (error.response?.status === 401 || error.response?.status === 403) {
                alert('❌ No autorizado. Por favor, inicie sesión nuevamente.');
                handleLogout();
            } else {
                alert('❌ Error al actualizar puntaje');
                console.error('Error:', error);
            }
        }
    };

    // --- 4. FUNCIONES DE ADMINISTRACIÓN MEJORADAS ---

    // Cargar datos para panel admin
    const cargarDatosAdmin = async () => {
        try {
            console.log('🔧 Cargando datos admin...');
            const [conjuntosRes, usuariosRes, statsRes] = await Promise.all([
                axios.get(`${BACKEND_URL}/admin/conjuntos`, { 
                    params: { username: loginData.username } 
                }),
                axios.get(`${BACKEND_URL}/admin/usuarios`, { 
                    params: { username: loginData.username } 
                }),
                axios.get(`${BACKEND_URL}/admin/estadisticas`, { 
                    params: { username: loginData.username } 
                })
            ]);
             console.log('✅ Datos cargados:', {
                conjuntos: conjuntosRes.data,
                usuarios: usuariosRes.data,
                estadisticas: statsRes.data
            });
            
            setConjuntosDisponibles(conjuntosRes.data);
            setUsuarios(usuariosRes.data);
            setEstadisticas(statsRes.data);
             // ✅ AGREGAR ESTE ALERT DE CONFIRMACIÓN
        alert(`✅ Datos cargados exitosamente:\n• ${conjuntosRes.data.length} conjuntos\n• ${usuariosRes.data.length} usuarios\n• ${statsRes.data?.concurso?.total_participaciones || 0} participaciones`);

        } catch (error) {
            console.error('Error cargando datos admin:', error);
            if (error.response?.status === 403) {
                alert('❌ No tiene permisos de administrador');
                handleLogout();
            } else if(error.response?.data?.error){
              alert(`❌ Error: ${error.response.data.error}`);
            }else{
                alert('Error al cargar datos de administración');
            }
        }
    };

    // Crear nuevo conjunto
    const handleCrearConjunto = async () => {
        if (!nuevoConjunto.nombre.trim()) {
            alert('❌ El nombre del conjunto es requerido');
            return;
        }

        try {
            const response = await axios.post(`${BACKEND_URL}/admin/conjuntos`, {
                nombre: nuevoConjunto.nombre,
                clasificacion: nuevoConjunto.clasificacion,
                tipo_danza: nuevoConjunto.tipo_danza || 'Morenada',
                username: loginData.username
            });

            setShowCrearConjunto(false);
            setNuevoConjunto({ nombre: '', clasificacion: 'Traje de Luces', tipo_danza: 'Morenada' });
            alert('✅ Conjunto creado exitosamente');
            
            // Recargar lista de conjuntos
            await cargarDatosAdmin();
        } catch (error) {
            if (error.response?.data?.error) {
                alert(`❌ ${error.response.data.error}`);
            } else {
                alert('❌ Error al crear conjunto');
            }
        }
    };

    const getPrediccionEstado = (id_participacion) => {
    if (loadingHorarios) return "Cargando...";
    
    const horarioData = horarios[id_participacion];
    if (!horarioData) return "Pendiente";
    
    // ✅ DEBUG DETALLADO
    console.log('🔍 DEBUG HORARIOS:', {
        id_participacion,
        horarioData,
        fechaConcurso: fechaConcurso?.toLocaleString(),
        tipoHorario: typeof horarioData
    });

    // ✅ PRIMERO: Usar el estado que viene del backend si está disponible
    if (horarioData.estado) {
        return horarioData.estado;
    }
    
    const ahora = new Date();
    
    // 1. VERIFICAR SI EL CONCURSO HA INICIADO
    if (fechaConcurso && ahora < fechaConcurso) {
        const diffMs = fechaConcurso - ahora;
        const diffDias = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        const diffHoras = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const diffMin = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        
        if (diffDias > 30) {
            const meses = Math.floor(diffDias / 30);
            const diasRestantes = diffDias % 30;
            if (diasRestantes > 0) {
                return `Concurso inicia en ${meses} ${meses === 1 ? 'mes' : 'meses'} y ${diasRestantes} ${diasRestantes === 1 ? 'día' : 'días'}`;
            } else {
                return `Concurso inicia en ${meses} ${meses === 1 ? 'mes' : 'meses'}`;
            }
        } else if (diffDias > 0) {
            return `Concurso inicia en ${diffDias} ${diffDias === 1 ? 'día' : 'días'} y ${diffHoras}h`;
        } else {
            return `Concurso inicia en ${diffHoras}h ${diffMin}m`;
        }
    }
    
    // 2. SI EL CONCURSO YA INICIÓ, CALCULAR ESTADO NORMAL
    const horaEstimada = typeof horarioData === 'string' ? horarioData : horarioData.hora;
    if (!horaEstimada) return "Pendiente";
    
    // Obtener información del día desde el backend
    const diaBackend = typeof horarioData === 'object' ? horarioData.dia : 1;
    
    // ✅ CALCULAR HORA CORRECTAMENTE - RESPETAR LO QUE VIENE DEL BACKEND
    let horaParticipacion;

    if (fechaConcurso) {
        horaParticipacion = new Date(fechaConcurso);
        
        // ✅ CORRECCIÓN: Siempre respetar la hora que viene del backend
        // Si el backend dice "08:00" para Día 1, es porque el concurso inicia a las 08:00
        const [horas, minutos] = horaEstimada.split(':').map(Number);
        
        if (diaBackend === 1) {
            // Día 1: Usar fecha del concurso con la hora del backend
            horaParticipacion.setHours(horas, minutos, 0, 0);
        } else {
            // Días 2, 3, etc.: Avanzar días y usar hora del backend
            horaParticipacion.setDate(fechaConcurso.getDate() + (diaBackend - 1));
            horaParticipacion.setHours(horas, minutos, 0, 0);
        }
    } else {
        // Fallback sin fecha de concurso
        horaParticipacion = new Date();
        const [horas, minutos] = horaEstimada.split(':').map(Number);
        horaParticipacion.setHours(horas, minutos, 0, 0);
    }

    // ✅ DEBUG FINAL
    console.log('⏰ HORA CALCULADA:', {
        participacion: id_participacion,
        dia: diaBackend,
        horaBackend: horaEstimada,
        horaFinal: horaParticipacion.toLocaleString(),
        diferencia: (horaParticipacion - ahora) / (1000 * 60) + ' minutos'
    });

    const diffMs = horaParticipacion - ahora;
    
    // Lógica de estados
    if (diffMs < -5 * 60 * 1000) {
        return "FINALIZADO ✅";
    } else if (diffMs <= 0) {
        return "EN CURSO 💃";
    } else if (diffMs < 5 * 60 * 1000) {
        return "¡PRONTO! 🏃‍♂️";
    } else {
        const diffDias = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        const diffHoras = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const diffMin = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        
        if (diffDias > 0) {
            return `${diffDias}d ${diffHoras}h ${diffMin}m`;
        } else if (diffHoras > 0) {
            return `En ${diffHoras}h ${diffMin}m`;
        } else {
            return `En ${diffMin}m`;
        }
    }
};

    /// Función para mostrar información del día
const getInfoDia = (id_participacion) => {
    const horarioData = horarios[id_participacion];
    if (!horarioData) return 'Día 1';
    
    // ✅ Usar la información del día que viene del backend
    if (typeof horarioData === 'object' && horarioData.dia) {
        const dias = ['', 'Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5'];
        return dias[horarioData.dia] || `Día ${horarioData.dia}`;
    }
    
    return 'Día 1';
};

    // Función mejorada para calcular hora de fin estimada
    const calcularHoraFinEstimada = () => {
        if (Object.keys(horarios).length === 0 || participaciones.length === 0) return 'No disponible';
        
        // Encontrar la última participación
        const ultimaParticipacion = participaciones.reduce((prev, current) => 
            (prev.orden_concurso > current.orden_concurso) ? prev : current
        );
        
        const ultimoHorario = horarios[ultimaParticipacion.id_participacion];
        if (!ultimoHorario) return 'No disponible';
        
        // Manejar tanto formato string como objeto
        const horaEstimada = typeof ultimoHorario === 'string' ? ultimoHorario : ultimoHorario.hora;
        if (!horaEstimada) return 'No disponible';
        
        // Agregar 8 minutos a la última participación (duración estimada + preparativos)
        const [horas, minutos] = horaEstimada.split(':').map(Number);
        const fecha = new Date();
        fecha.setHours(horas, minutos + 8, 0, 0);
        
        return fecha.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    };

    // CORRECCIÓN: Variable 'ahora' definida correctamente
    const handleActualizarHoraInicio = async () => {
    // Obtener fecha y hora actual para sugerir
    const ahora = new Date();
    const año = ahora.getFullYear() + 1; // Sugerir próximo año
    const mes = String(ahora.getMonth() + 1).padStart(2, '0');
    const dia = String(ahora.getDate()).padStart(2, '0');
    
    // Sugerir fecha del próximo año
    const fechaSugerida = `${año}-${mes}-${dia}`;
    const horaSugerida = '08:00';

    const fechaHoraInput = window.prompt(
        'Ingrese la fecha y hora de INICIO del concurso:\n\n' +
        'Formato: YYYY-MM-DD HH:MM\n' +
        'Ejemplo: 2026-02-23 08:00\n\n' +
        'Fecha actual: ' + ahora.toLocaleDateString('es-ES'),
        `${fechaSugerida} ${horaSugerida}`
    );
    
    if (!fechaHoraInput) return;
    
    // Validar formato de fecha y hora
    const fechaHoraRegex = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
    if (!fechaHoraRegex.test(fechaHoraInput)) {
        alert('❌ Formato inválido. Use: YYYY-MM-DD HH:MM (ej: 2026-02-23 08:00)');
        return;
    }
    
    const nuevaHoraCompleta = `${fechaHoraInput}:00`;
    
    try {
        const response = await axios.put(`${BACKEND_URL}/admin/concurso/hora-inicio`, {
            hora_inicio: nuevaHoraCompleta,
            concurso_id: ID_CONCURSO,
            username: loginData.username
        });
        
        if(response.data.success){
            // Actualizar estado local
            setFechaConcurso(new Date(nuevaHoraCompleta));
            setLoading(true);
            setLoadingHorarios(true);
            const [participacionesRes, horariosRes] = await Promise.all([
                axios.get(`${BACKEND_URL}/participaciones/${ID_CONCURSO}`),
                axios.get(`${BACKEND_URL}/predecir-horarios/${ID_CONCURSO}`)
            ]);

            setParticipaciones(participacionesRes.data.sort((a, b) => a.orden_concurso - b.orden_concurso)  );
            setHorarios(horariosRes.data);
            setLoading(false);
            setLoadingHorarios(false);

            // Mostrar información de la nueva fecha
            const fechaObj = new Date(nuevaHoraCompleta);
            const opciones = { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            const fechaFormateada = fechaObj.toLocaleDateString('es-ES', opciones);
            
            alert(`✅ Fecha de inicio actualizada:\n${fechaFormateada}\n\nLos estados se han actualizado automáticamente.`);
        }
    } catch(error) {
        if (error.response?.data?.error) {
            alert(`✅ Fecha de inicio actualizada:\n${fechaFormateada}\n\n• Día 1: ${fechaObj.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}\n• Día 2: 08:00 AM\n• Los estados se han actualizado automáticamente.`);
        } else {
            alert('❌ Error al actualizar fecha de inicio');
        }
    }
};

// Función para obtener información de la fecha del concurso - MEJORADA
const getInfoFechaConcurso = () => {
    if (!fechaConcurso) {
        return {
            texto: "📅 Fecha del concurso no configurada",
            tipo: 'futuro'
        };
    }
    
    try {
        const ahora = new Date();
        
        // Verificar si la fecha es válida (no 1969)
        if (fechaConcurso.getFullYear() === 1969) {
            return {
                texto: "📅 Fecha del concurso no configurada",
                tipo: 'futuro'
            };
        }
        
        if (ahora >= fechaConcurso) {
            return {
                texto: `🎭 Concurso en curso (inició ${fechaConcurso.toLocaleDateString('es-ES')})`,
                tipo: 'en-curso'
            };
        } else {
            const diffMs = fechaConcurso - ahora;
            const diffDias = Math.floor(diffMs / (1000 * 60 * 60 * 24));
            const diffHoras = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const diffMin = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
            
            if (diffDias > 30) {
                const meses = Math.floor(diffDias / 30);
                const diasRestantes = diffDias % 30;
                if (diasRestantes > 0) {
                    return {
                        texto: `📅 Concurso inicia en ${meses} ${meses === 1 ? 'mes' : 'meses'} y ${diasRestantes} ${diasRestantes === 1 ? 'día' : 'días'}`,
                        tipo: 'futuro'
                    };
                } else {
                    return {
                        texto: `📅 Concurso inicia en ${meses} ${meses === 1 ? 'mes' : 'meses'}`,
                        tipo: 'futuro'
                    };
                }
            } else if (diffDias > 0) {
                return {
                    texto: `📅 Concurso inicia en ${diffDias} ${diffDias === 1 ? 'día' : 'días'} y ${diffHoras}h`,
                    tipo: 'futuro'
                };
            } else {
                return {
                    texto: `📅 Concurso inicia en ${diffHoras}h ${diffMin}m`,
                    tipo: 'futuro'
                };
            }
        }
    } catch (error) {
        console.error('Error en getInfoFechaConcurso:', error);
        return {
            texto: "📅 Error cargando fecha",
            tipo: 'futuro'
        };
    }
};

    // CORRECCIÓN: Función separada correctamente
    const handleConfigurarDias = async () => {
        const presentacionesPorDia = window.prompt(
            'Configurar presentaciones por día:\n\n' +
            'Ingrese el número máximo de presentaciones por día (por defecto: 40)',
            '40'
        );
        
        if (!presentacionesPorDia) return;
        
        const numero = parseInt(presentacionesPorDia);
        if (isNaN(numero) || numero < 1) {
            alert('❌ Número inválido');
            return;
        }
        
        // Aquí podrías enviar esta configuración al backend
        alert(`✅ Configurado: ${numero} presentaciones por día\n\nRecargando horarios...`);
        
        // Recargar horarios
        setLoadingHorarios(true);
        try {
            const resHorarios = await axios.get(`${BACKEND_URL}/predecir-horarios/${ID_CONCURSO}`);
            setHorarios(resHorarios.data);
        } catch (error) {
            console.error('Error recargando horarios:', error);
        }
        setLoadingHorarios(false);
    };

    // Cargar lista de votantes
    const cargarVotantesParticipacion = async (participacionId) => {
        try {
            const response = await axios.get(`${BACKEND_URL}/admin/votos-participacion/${participacionId}`, {
                params: { username: loginData.username }
            });
            setListaVotantes(prev => ({
                ...prev,
                [participacionId]: response.data
            }));
        } catch (error) {
            console.error('Error cargando votantes:', error);
            alert('❌ Error al cargar lista de votantes');
        }
    };

    // Editar danza
    const handleEditarDanza = async (participacionId, danzaActual) => {
        const nuevaDanza = window.prompt('Ingrese el nuevo tipo de danza:', danzaActual);
        if (!nuevaDanza) return;
        
        try {
            await axios.put(`${BACKEND_URL}/admin/participaciones/${participacionId}/danza`, {
                tipo_danza: nuevaDanza,
                username: loginData.username
            });
            
            // Recargar datos
            const res = await axios.get(`${BACKEND_URL}/participaciones/${ID_CONCURSO}`);
            setParticipaciones(res.data.sort((a, b) => a.orden_concurso - b.orden_concurso));
            alert('✅ Danza actualizada correctamente');
        } catch (error) {
            alert('❌ Error al actualizar danza');
        }
    };

    // Editar orden
    const handleEditarOrden = async (participacionId, ordenActual) => {
        const nuevoOrden = window.prompt('Ingrese el nuevo orden de presentación:', ordenActual);
        if (!nuevoOrden) return;
        
        try {
            await axios.put(`${BACKEND_URL}/admin/participaciones/${participacionId}/orden`, {
                orden_presentacion: parseInt(nuevoOrden),
                username: loginData.username
            });
            
            // Recargar datos
            const res = await axios.get(`${BACKEND_URL}/participaciones/${ID_CONCURSO}`);
            setParticipaciones(res.data.sort((a, b) => a.orden_concurso - b.orden_concurso));
            alert('✅ Orden actualizado correctamente');
        } catch (error) {
            alert('❌ Error al actualizar orden');
        }
    };

    // Agregar participación
    const handleAgregarParticipacion = async () => {
        if (conjuntosDisponibles.length === 0) {
            await cargarDatosAdmin();
        }
        
        if (conjuntosDisponibles.length === 0) {
            alert('No hay conjuntos disponibles para agregar');
            return;
        }
        
        // Crear lista más amigable para el usuario
        const listaConjuntos = conjuntosDisponibles.map(c => 
            `${c.id}: ${c.nombre} (${c.clasificacion})`
        ).join('\n');
        
        const conjuntoId = window.prompt(
            'Ingrese el ID del conjunto a agregar:\n\n' + listaConjuntos
        );
        
        if (!conjuntoId) return;
        
        // Verificar que el ID existe
        const conjuntoSeleccionado = conjuntosDisponibles.find(c => c.id === parseInt(conjuntoId));
        if (!conjuntoSeleccionado) {
            alert('❌ ID de conjunto no válido');
            return;
        }
         
        const listaDanzas = danzas.map((danza, index) => `${index + 1}. ${danza}`).join('\n');
    
        const tipoDanzaInput = window.prompt(
            `Ingrese el tipo de danza para "${conjuntoSeleccionado.nombre}":\n\n` +
            listaDanzas +
            `\n\nEscriba el nombre exacto de la danza:`,
            conjuntoSeleccionado.tipo_danza || 'Morenada' // Valor por defecto
        );
        if (!tipoDanzaInput) return;
        
        // Validar que la danza esté en la lista
        const danzaValida = danzas.find(d => d.toLowerCase() === tipoDanzaInput.toLowerCase());
        
        if (!danzaValida){
        if (!window.confirm(`"${tipoDanzaInput}" no está en la lista principal. ¿Desea usarlo de todas formas?`)) {
            return;
        }
    }
    
    const tipoDanza = danzaValida || tipoDanzaInput;
    
    try {
        await axios.post(`${BACKEND_URL}/admin/participaciones`, {
            conjunto_id: parseInt(conjuntoId),
            concurso_id: ID_CONCURSO,
            tipo_danza: tipoDanza,
            username: loginData.username
        });
            
            // Recargar datos
            const res = await axios.get(`${BACKEND_URL}/participaciones/${ID_CONCURSO}`);
            setParticipaciones(res.data.sort((a, b) => a.orden_concurso - b.orden_concurso));
            alert('✅ Participación agregada correctamente');
        } catch (error) {
            if (error.response?.data?.error) {
                alert(`❌ ${error.response.data.error}`);
            } else {
                alert('❌ Error al agregar participación');
            }
        }
    };

    // Eliminar participación
    const handleEliminarParticipacion = async (participacionId, conjuntoNombre) => {
        if (!window.confirm(`¿Está seguro de eliminar la participación de "${conjuntoNombre}"?`)) return;
        
        try {
            await axios.delete(`${BACKEND_URL}/admin/participaciones/${participacionId}`, {
                data: { username: loginData.username }
            });
            
            // Recargar datos
            const res = await axios.get(`${BACKEND_URL}/participaciones/${ID_CONCURSO}`);
            setParticipaciones(res.data.sort((a, b) => a.orden_concurso - b.orden_concurso));
            alert('✅ Participación eliminada correctamente');
        } catch (error) {
            alert('❌ Error al eliminar participación');
        }
    };

    // Cambiar rol de usuario
    const handleCambiarRol = async (userId, usuarioActual, rolActual) => {
        const nuevoRol = window.prompt(
            `Cambiar rol de "${usuarioActual}" (actual: ${rolActual}):\n\nadmin, juez, publico`,
            rolActual
        );
        
        if (!nuevoRol || !['admin', 'juez', 'publico'].includes(nuevoRol)) return;
        
        try {
            await axios.put(`${BACKEND_URL}/admin/usuarios/${userId}/rol`, {
                rol: nuevoRol,
                username: loginData.username
            });
            
            // Recargar usuarios
            const res = await axios.get(`${BACKEND_URL}/admin/usuarios`, { 
                params: { username: loginData.username } 
            });
            setUsuarios(res.data);
            alert('✅ Rol actualizado correctamente');
        } catch (error) {
            alert('❌ Error al actualizar rol');
        }
    };

    // --- 5. FUNCIÓN DE LOGIN MEJORADA ---
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`${BACKEND_URL}/login`, loginData);
            
            if (response.data.success) {
                setIsLoggedIn(true);
                setShowLogin(false);
                setIsAdmin(true);
                setLoginData(prev => ({ ...prev, username: response.data.username }));
                localStorage.setItem('adminUser', response.data.username);
                alert('✅ Login exitoso - Modo Administrador activado');
            }
        } catch (error) {
            alert('❌ Error: Usuario o contraseña incorrectos');
            console.error('Login error:', error);
        }
    };

    // --- 6. FUNCIÓN DE LOGOUT MEJORADA ---
    const handleLogout = () => {
        setIsLoggedIn(false);
        setIsAdmin(false);
        setShowLogin(false);
        setShowAdminPanel(false);
        setLoginData({ username: '', password: '' });
        localStorage.removeItem('adminUser');
        alert('🔒 Sesión cerrada - Modo Administrador desactivado');
    };

    // --- 7. FUNCIÓN AUXILIAR (Actualizar estado) ---
    const actualizarParticipacionEnEstado = (participacionActualizada) => {
        setParticipaciones(participacionesActuales => 
            participacionesActuales.map(p => 
                p.id_participacion === participacionActualizada.id_participacion 
                ? { ...p, ...participacionActualizada }
                : p
            ).sort((a, b) => a.orden_concurso - b.orden_concurso)
        );
    };

    // --- 9. LÓGICA DEL FILTRO ---
    const participacionesFiltradas = participaciones.filter(p => {
        const textoBusqueda = filtroBusqueda.toLowerCase();
        const nombreConjunto = p.conjunto?.nombre?.toLowerCase() || '';
        const tipoDanza = p.tipo_danza?.toLowerCase() || '';
        return nombreConjunto.includes(textoBusqueda) || tipoDanza.includes(textoBusqueda);
    });

    // --- 10. MODALES Y PANELES ---

    const renderLoginModal = () => {
        if (!showLogin) return null;
        
        return (
            <div className="modal-overlay">
                <div className="modal-content">
                    <h3>Login Administrador</h3>
                    <form onSubmit={handleLogin}>
                        <div className="form-group">
                            <label>Usuario:</label>
                            <input
                                type="text"
                                value={loginData.username}
                                onChange={(e) => setLoginData({...loginData, username: e.target.value})}
                                placeholder="Ingrese su usuario"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Contraseña:</label>
                            <input
                                type="password"
                                value={loginData.password}
                                onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                                placeholder="Ingrese su contraseña"
                                required
                            />
                        </div>
                        <div className="modal-buttons">
                            <button type="submit" className="btn-primary">Ingresar</button>
                            <button type="button" onClick={() => setShowLogin(false)} className="btn-secondary">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        );
    };

    const renderVotoModal = () => {
        if (!showVotoModal) return null;
        
        const participacion = participaciones.find(p => p.id_participacion === participacionAVotar);
        
        return (
            <div className="modal-overlay">
                <div className="modal-content">
                    <h3>🎭 Votar por Participación</h3>
                    {participacion && (
                        <div className="voto-info">
                            <p><strong>Conjunto:</strong> {participacion.conjunto.nombre}</p>
                            <p><strong>Danza:</strong> {participacion.tipo_danza}</p>
                            <p><strong>Votos actuales:</strong> {participacion.votos_publico || 0}</p>
                        </div>
                    )}
                    <div className="form-group">
                        <label>¿Cuál es tu nombre? *</label>
                        <input
                            type="text"
                            value={votanteNombre}
                            onChange={(e) => setVotanteNombre(e.target.value)}
                            placeholder="Ej: María, Juan, Carlos..."
                            required
                            maxLength="50"
                        />
                        <small style={{color: '#B0BEC5', fontSize: '0.8rem'}}>
                            * Tu nombre se mostrará públicamente en la lista de votantes
                        </small>
                    </div>
                    <div className="modal-buttons">
                        <button onClick={procesarVoto} className="btn-primary">
                            ✅ Confirmar Mi Voto
                        </button>
                        <button 
                            onClick={() => {
                                setShowVotoModal(false);
                                setVotanteNombre('');
                            }} 
                            className="btn-secondary"
                        >
                            Cancelar
                        </button>
                    </div>
                </div>
            </div>
        );
    };

    const renderCrearConjuntoModal = () => {
        if (!showCrearConjunto) return null;
        
        return (
            <div className="modal-overlay">
                <div className="modal-content">
                    <h3>➕ Crear Nuevo Conjunto</h3>
                    <div className="form-group">
                        <label>Nombre del Conjunto:</label>
                        <input
                            type="text"
                            value={nuevoConjunto.nombre}
                            onChange={(e) => setNuevoConjunto({...nuevoConjunto, nombre: e.target.value})}
                            placeholder="Ej: Morenada Central Puno"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Clasificación:</label>
                        <select
                            value={nuevoConjunto.clasificacion}
                            onChange={(e) => setNuevoConjunto({...nuevoConjunto, clasificacion: e.target.value})}
                            className="form-select"
                        >
                            <option value="Traje de Luces">Traje de Luces</option>
                            <option value="Originaria">Originaria</option>
                            <option value="Indefinido">Indefinido</option>
                        </select>
                    </div>
                    <div className="form-group">
    <label>Tipo de Danza Principal:</label>
    <select
        value={nuevoConjunto.tipo_danza || 'Morenada'}
        onChange={(e) => {
            if (e.target.value === 'manual') {
                // Si selecciona "Otro", abrir input manual
                const danzaManual = window.prompt('Ingrese el nombre de la danza:');
                if (danzaManual) {
                    setNuevoConjunto({...nuevoConjunto, tipo_danza: danzaManual});
                }
            } else {
                setNuevoConjunto({...nuevoConjunto, tipo_danza: e.target.value});
            }
        }}
        className="form-select"
    >
        {danzas.map(danza => (
            <option key={danza} value={danza}>{danza}</option>
        ))}
        {/* ✅ OPCIÓN PARA ESCRIBIR MANUALMENTE */}
        <option value="manual">✏️ Escribir manualmente...</option>
    </select>
    
    {/* ✅ MOSTRAR VALOR ACTUAL SI ES MANUAL */}
    {nuevoConjunto.tipo_danza && !danzas.includes(nuevoConjunto.tipo_danza) && (
        <small style={{color: '#4CAF50', display: 'block', marginTop: '5px'}}>
            Danza personalizada: <strong>{nuevoConjunto.tipo_danza}</strong>
        </small>
    )}

                    </div>
                    <div className="modal-buttons">
                        <button onClick={handleCrearConjunto} className="btn-primary">
                            Crear Conjunto
                        </button>
                        <button 
                            onClick={() => setShowCrearConjunto(false)} 
                            className="btn-secondary"
                        >
                            Cancelar
                        </button>
                    </div>
                </div>
            </div>
        );
    };

    const renderVotantesModal = (participacionId) => {
        const votantes = listaVotantes[participacionId] || [];
        const participacion = participaciones.find(p => p.id_participacion === participacionId);
        
        return (
            <div className="modal-overlay">
                <div className="modal-content">
                    <div className="admin-panel-header">
                        <h3>👥 Votantes - {participacion?.conjunto.nombre}</h3>
                        <button onClick={() => setListaVotantes(prev => ({...prev, [participacionId]: null}))} className="btn-close">
                            ✕
                        </button>
                    </div>
                    
                    <div className="votantes-list">
                        {votantes.length === 0 ? (
                            <p style={{textAlign: 'center', color: '#B0BEC5'}}>No hay votos registrados</p>
                        ) : (
                            <>
                                <p><strong>Total votos:</strong> {votantes.length}</p>
                                <div className="votantes-grid">
                                    {votantes.map((votante, index) => (
                                        <div key={index} className="votante-item">
                                            <span className="votante-nombre">{votante.nombre}</span>
                                            <span className="votante-fecha">
                                                {votante.fecha ? new Date(votante.fecha).toLocaleString() : 'Fecha no disponible'}
                                            </span>
                                        </div>
                                    ))}
                                </div>
                            </>
                        )}
                    </div>
                </div>
            </div>
        );
    };

    const renderAdminPanel = () => {
    if (!showAdminPanel || !isAdmin) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content admin-panel">
                <div className="admin-panel-header">
                    <h3>Panel de Administración</h3>
                    <button onClick={() => setShowAdminPanel(false)} className="btn-close">✕</button>
                </div>
                
                <div className="admin-tabs">
                    {/* Sección de Debug */}
                    <div className="admin-section">
                        <h4>🔧 Estado del Sistema</h4>
                        <div className="debug-info">
                            <p><strong>Usuario:</strong> {loginData.username}</p>
                            <p><strong>Participaciones:</strong> {participaciones.length}</p>
                            <p><strong>Horarios cargados:</strong> {Object.keys(horarios).length}</p>
                            <p><strong>Conjuntos disponibles:</strong> {conjuntosDisponibles.length}</p>
                            <p><strong>Usuarios en sistema:</strong> {usuarios.length}</p>
                        </div>
                        <div className="admin-actions">
                            <button onClick={cargarDatosAdmin} className="btn-primary">
                                🔄 Recargar Todo
                            </button>
                            <button onClick={() => {
                                console.log('🐛 Debug info:', {
                                    participaciones,
                                    horarios,
                                    conjuntosDisponibles,
                                    usuarios,
                                    estadisticas
                                });
                                alert('✅ Información de debug enviada a la consola');
                            }} className="btn-secondary">
                                🐛 Debug Console
                            </button>
                        </div>
                    </div>

                    <div className="admin-section">
                        <h4><Clock size={18} /> Gestión del Concurso</h4>
                        <div className="admin-actions">
                            <button onClick={handleActualizarHoraInicio} className="btn-primary">
                                <Clock size={16} /> Editar Hora Inicio
                            </button>
                            <button onClick={handleConfigurarDias} className="btn-primary">
                                📅 Configurar Días
                            </button>
                            <button onClick={() => {
                                // Forzar recarga de horarios
                                setLoadingHorarios(true);
                                axios.get(`${BACKEND_URL}/predecir-horarios/${ID_CONCURSO}`)
                                    .then(res => {
                                        setHorarios(res.data);
                                        setLoadingHorarios(false);
                                        alert('✅ Horarios recargados');
                                    })
                                    .catch(err => {
                                        console.error('Error recargando horarios:', err);
                                        setLoadingHorarios(false);
                                    });
                            }} className="btn-secondary">
                                🔄 Recargar Horarios
                            </button>
                        </div>
                    </div>

                    <div className="admin-section">
             <h4><Users size={18} /> Gestión de Usuarios</h4>
    <div className="admin-actions">
        <button onClick={debugUsuarios} className="btn-primary">
            🔍 Debug Usuarios
        </button>
        <button onClick={cargarDatosAdmin} className="btn-secondary">
            🔄 Recargar Todo
        </button>
    </div>


    
    {/* ✅ MOSTRAR USUARIOS DIRECTAMENTE - ELIMINAR LA CONDICIÓN */}
        <div className="users-list">
        <p><strong>Total usuarios:</strong> {usuarios.length}</p>
        {usuarios.length === 0 ? (
            <div style={{textAlign: 'center', color: '#B0BEC5', padding: '20px'}}>
                <p>No hay usuarios cargados.</p>
                <p>Haz clic en "Debug Usuarios" para diagnosticar el problema.</p>
            </div>
        ) : (
            usuarios.map(user => (
                <div key={user.id} className="user-item">
                    <div>
                        <strong>{user.username}</strong>
                        <span style={{
                            marginLeft: '10px', 
                            color: user.rol === 'admin' ? '#EF5350' : 
                                   user.rol === 'juez' ? '#FFC107' : '#4CAF50'
                        }}>
                            ({user.rol})
                        </span>
                    </div>
                    <button 
                        onClick={() => handleCambiarRol(user.id, user.username, user.rol)}
                        className="btn-small"
                    >
                        Cambiar Rol
                    </button>
                </div>
            ))
        )}
    </div>

</div>



                    <div className="admin-section">
                            <h4><Users size={18} /> Gestión de Conjuntos</h4>
                            <div className="admin-actions">
                                <button onClick={() => setShowCrearConjunto(true)} className="btn-primary">
                                    <Plus size={16} /> Crear Conjunto
                                </button>
                                <button onClick={handleAgregarParticipacion} className="btn-primary">
                                    <Plus size={16} /> Agregar Participación
                                </button>
                            </div>
                            {conjuntosDisponibles.length > 0 && (
                                <div className="conjuntos-list">
                                    <p><strong>Conjuntos disponibles:</strong> {conjuntosDisponibles.length}</p>
                                </div>
                            )}
                    </div>
                    {estadisticas && (
                            <div className="admin-section">
                                <h4><BarChart3 size={18} /> Estadísticas</h4>
                                <div className="stats-grid">
                                    <div className="stat-item">
                                        <span>Total Usuarios:</span>
                                        <strong>{estadisticas.usuarios.total}</strong>
                                    </div>
                                    <div className="stat-item">
                                        <span>Jueces:</span>
                                        <strong>{estadisticas.usuarios.jueces}</strong>
                                    </div>
                                    <div className="stat-item">
                                        <span>Público:</span>
                                        <strong>{estadisticas.usuarios.publico}</strong>
                                    </div>
                                    <div className="stat-item">
                                        <span>Participaciones:</span>
                                        <strong>{estadisticas.concurso.total_participaciones}</strong>
                                    </div>
                                    <div className="stat-item">
                                        <span>Total Votos:</span>
                                        <strong>{estadisticas.concurso.total_votos}</strong>
                                    </div>
                                    <div className="stat-item">
                                        <span>Conjuntos:</span>
                                        <strong>{estadisticas.concurso.total_conjuntos}</strong>
                                    </div>
                                </div>
                            </div>
                        )}

                    {/* ... resto del panel ... */}
                </div>
            </div>
        </div>
    );
};

    // --- 11. FUNCIÓN PARA RENDERIZAR CONTENIDO ---
    const renderContenido = () => {
        if (loading) return (
            <div className="loading-text">
                <Loader className="loader-icon" size={32} />
                <p>Cargando datos del {anoAConsultar}...</p>
            </div>
        );
        
        if (error) return (
            <div className="error-text">
                <AlertTriangle size={24} />
                <p>{error}</p>
            </div>
        );
        
        if (participacionesFiltradas.length === 0) {
            return <p className="loading-text">No se encontraron resultados para "{filtroBusqueda}"</p>;
        }

        return (
            <>
                {/* VISTA MÓVIL/TABLET - TARJETAS */}
                <div className="card-grid">
                    {participacionesFiltradas.map(p => (
                        <div className="participacion-card" key={p.id_participacion}>
                            <div className="card-header">
                                <span className="card-orden">#{p.orden_concurso}</span>
                                <h3 className="card-nombre">{p.conjunto.nombre}</h3>
                                {isAdmin && (
                                    <div className="card-admin-actions">
                                        <button 
                                            onClick={() => cargarVotantesParticipacion(p.id_participacion)}
                                            className="btn-icon"
                                            title="Ver votantes"
                                        >
                                            <UserCheck size={14} />
                                        </button>
                                        <button 
                                            onClick={() => handleEditarDanza(p.id_participacion, p.tipo_danza)}
                                            className="btn-icon"
                                            title="Editar danza"
                                        >
                                            <Edit3 size={14} />
                                        </button>
                                        <button 
                                            onClick={() => handleEditarOrden(p.id_participacion, p.orden_concurso)}
                                            className="btn-icon"
                                            title="Editar orden"
                                        >
                                            🔢
                                        </button>
                                        <button 
                                            onClick={() => handleEliminarParticipacion(p.id_participacion, p.conjunto.nombre)}
                                            className="btn-icon btn-danger"
                                            title="Eliminar participación"
                                        >
                                            <Trash2 size={14} />
                                        </button>
                                    </div>
                                )}
                            </div>
                            
                            <div className="card-body">
                                <div className="card-info-row info-danza">
                                    <span className="card-info-label">Danza</span>
                                    <span className="card-info-value">{p.tipo_danza || 'Por definir'}</span>
                                </div>
                                
                                <div className="card-info-row info-hora">
                                    <span className="card-info-label">Hora Est. 🕒</span>
                                    <span className="card-info-value prediccion">
                                        {loadingHorarios ? "..." : 
                                            (typeof horarios[p.id_participacion] === 'string' 
                                                ? horarios[p.id_participacion] 
                                                : horarios[p.id_participacion]?.hora || "?")}
                                    </span>
                                </div>
                                {/* -- Información del día (si aplica) --- */}
                                <div className="card-info-row info-dia">
                                    <span className="card-info-label">Día</span>
                                    <span className="card-info-value">{getInfoDia(p.id_participacion)}</span>
                                </div>
                                
                                <div className="card-info-row info-estado">
                                    <span className="card-info-label">Estado Pred.</span>
                                    <span className="card-info-value estado-prediccion">
                                        {getPrediccionEstado(p.id_participacion)}
                                    </span>
                                </div>

                                <div className="card-scores">
                                    <div 
                                        className={isAdmin ? "score-item admin-editable" : "score-item"}
                                        onClick={() => handleActualizarPuntaje(p.id_participacion, 'coreografia')}
                                    >
                                        <span className="score-label">Coreografía</span>
                                        <span className="score-value">{p.puntaje_coreografia || '---'}</span>
                                    </div>
                                    <div 
                                        className={isAdmin ? "score-item admin-editable" : "score-item"}
                                        onClick={() => handleActualizarPuntaje(p.id_participacion, 'traje')}
                                    >
                                        <span className="score-label">Traje</span>
                                        <span className="score-value">{p.puntaje_traje || '---'}</span>
                                    </div>
                                    <div 
                                        className={isAdmin ? "score-item admin-editable" : "score-item"}
                                        onClick={() => handleActualizarPuntaje(p.id_participacion, 'musica')}
                                    >
                                        <span className="score-label">Música</span>
                                        <span className="score-value">{p.puntaje_musica || '---'}</span>
                                    </div>
                                </div>

                                <div className="card-info-row total-score">
                                    <span className="card-info-label">Total Puntaje</span>
                                    <span className="card-info-value">
                                        <strong>{p.puntaje_total || '---'}</strong>
                                    </span>
                                </div>
                            </div>
                            
                            <div className="card-footer">
                                <button 
                                    className="boton-votar"
                                    onClick={() => abrirModalVoto(p.id_participacion)}
                                >
                                    Votar 👍 ({p.votos_publico || 0})
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {/* VISTA ESCRITORIO - TABLA */}
                <div className="table-container">
                    <table className="participaciones-table">
                        <thead>
                            <tr>
                                <th>N°</th>
                                <th>Conjunto</th>
                                <th>Danza</th>
                                <th>Hora Est.</th>
                                <th>Día</th>
                                <th>Estado Pred.</th>
                                <th>Coreografía</th>
                                <th>Traje</th>
                                <th>Música</th>
                                <th>Total</th>
                                <th>Acción</th>
                                {isAdmin && <th>Admin</th>}
                            </tr>
                        </thead>
                        <tbody>
                            {participacionesFiltradas.map(p => (
                                <tr key={p.id_participacion}>
                                    <td className="col-orden">{p.orden_concurso}</td>
                                    <td className="col-conjunto">{p.conjunto.nombre}</td>
                                    <td 
                                        className={`col-danza ${isAdmin ? 'admin-editable' : ''}`}
                                        onClick={() => isAdmin && handleEditarDanza(p.id_participacion, p.tipo_danza)}
                                    >
                                        {p.tipo_danza || 'Por definir'}
                                    </td>
                                    <td className="col-hora prediccion">
                                        {loadingHorarios ? "..." : 
                                            (typeof horarios[p.id_participacion] === 'string' 
                                                ? horarios[p.id_participacion] 
                                                : horarios[p.id_participacion]?.hora || "?")}
                                    </td>
                                    <td className="col-dia">{getInfoDia(p.id_participacion)}</td>
                                    <td className="col-estado estado-prediccion">
                                        {getPrediccionEstado(p.id_participacion)}
                                    </td>
                                    <td 
                                        className={`col-puntaje ${isAdmin ? 'admin-editable' : ''}`}
                                        onClick={() => handleActualizarPuntaje(p.id_participacion, 'coreografia')}
                                    >
                                        {p.puntaje_coreografia || '---'}
                                    </td>
                                    <td 
                                        className={`col-puntaje ${isAdmin ? 'admin-editable' : ''}`}
                                        onClick={() => handleActualizarPuntaje(p.id_participacion, 'traje')}
                                    >
                                        {p.puntaje_traje || '---'}
                                    </td>
                                    <td 
                                        className={`col-puntaje ${isAdmin ? 'admin-editable' : ''}`}
                                        onClick={() => handleActualizarPuntaje(p.id_participacion, 'musica')}
                                    >
                                        {p.puntaje_musica || '---'}
                                    </td>
                                    <td className="col-total">
                                        <strong>{p.puntaje_total || '---'}</strong>
                                    </td>
                                    <td className="col-accion">
                                        <button 
                                            className="boton-votar-table"
                                            onClick={() => abrirModalVoto(p.id_participacion)}
                                        >
                                            Votar 👍 ({p.votos_publico || 0})
                                        </button>
                                    </td>
                                    {isAdmin && (
                                        <td className="col-admin-actions">
                                            <button 
                                                onClick={() => cargarVotantesParticipacion(p.id_participacion)}
                                                className="btn-icon"
                                                title="Ver votantes"
                                            >
                                                <UserCheck size={14} />
                                            </button>
                                            <button 
                                                onClick={() => handleEditarOrden(p.id_participacion, p.orden_concurso)}
                                                className="btn-icon"
                                                title="Editar orden"
                                            >
                                                🔢
                                            </button>
                                            <button 
                                                onClick={() => handleEliminarParticipacion(p.id_participacion, p.conjunto.nombre)}
                                                className="btn-icon btn-danger"
                                                title="Eliminar participación"
                                            >
                                                <Trash2 size={14} />
                                            </button>
                                        </td>
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </>
        );
    };

    // --- 12. RENDER PRINCIPAL ---
    return (
        <div className="App-container"> 
            <header className="App-header">
                <h1>Participaciones para la Festividad {anoAConsultar}</h1>
                <div className="admin-controls">
                    {isAdmin ? (
                        <>
                            <button onClick={() => setShowAdminPanel(true)} className="boton-admin-panel">
                                <Settings size={16} /> Panel Admin
                            </button>
                            <button onClick={handleLogout} className="boton-admin-login logout">
                                🔓 Cerrar Sesión
                            </button>
                            <span className="admin-badge">Modo Administrador</span>
                        </>
                    ) : (
                        <button onClick={() => setShowLogin(true)} className="boton-admin-login">
                            🔑 Login Admin
                        </button>
                    )}
                </div>
            </header>
            
            <main className="App-main">
                <h2>Consulta interactiva Candelaria</h2>
                 {!loadingHorarios && (
    <div className="info-horarios">
        <div className="horario-item">
            <span>🏁 Hora de fin estimada:</span>
            <strong>{calcularHoraFinEstimada()}</strong>
        </div>
        {getInfoFechaConcurso() && (
            <div className={`fecha-concurso ${getInfoFechaConcurso().tipo}`}>
                <span>{getInfoFechaConcurso().texto}</span>
            </div>
        )}
        {isAdmin && (
            <button 
                onClick={handleActualizarHoraInicio}
                className="btn-small"
                style={{marginLeft: '10px'}}
            >
                <Clock size={14} /> Cambiar Fecha Inicio
            </button>
        )}
    </div>
)}

                
                <input 
                    type="text"
                    placeholder="Buscar por nombre o danza (ej. Morenada, Tinkus...)"
                    className="buscador"
                    value={filtroBusqueda}
                    onChange={e => setFiltroBusqueda(e.target.value)}
                />
                
                {renderContenido()}
            </main>

            {renderLoginModal()}
            {renderVotoModal()}
            {renderCrearConjuntoModal()}
            {renderAdminPanel()}
            
            {/* Modales de votantes para cada participación */}
            {Object.keys(listaVotantes).map(participacionId => 
                listaVotantes[participacionId] && renderVotantesModal(parseInt(participacionId))
            )}
        </div>
    );
}

export default App;