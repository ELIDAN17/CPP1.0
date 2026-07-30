// ==========================================
// RUTA DE TU ARCHIVO: src/views/DashboardEstudiante.jsx
// ==========================================
import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Clock, Building2, CheckCircle2, FileUp, AlertCircle, RefreshCw } from 'lucide-react';

export default function DashboardEstudiante() {
  // Extraemos el token y la función cerrarSesion de tu AuthContext corregido
  const { token, cerrarSesion } = useContext(AuthContext);
  const [datos, setDatos] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');

  // ESCUCHADOR DE RED: Si vuelve el internet, reintenta sincronizar automáticamente
  useEffect(() => {
    const manejarRegresoRed = () => {
      console.log("Se detectó el restablecimiento de red. Re-sincronizando Dashboard...");
      setError('');
      setCargando(true);
      // Al cambiar el estado de cargando a true, gatillamos indirectamente una recarga limpia
    };

    const manejarCaidaRed = () => {
      alert("Se ha perdido la conexión a internet. Los datos en pantalla podrían estar desactualizados.");
    };

    window.addEventListener('online', manejarRegresoRed);
    window.addEventListener('offline', manejarCaidaRed);

    return () => {
      window.removeEventListener('online', manejarRegresoRed);
      window.removeEventListener('offline', manejarCaidaRed);
    };
  }, []);

  useEffect(() => {
    if (!token) return;

    let activo = true;

    const cargarDatosDashboard = async () => {
      try {
        // SEGURIDAD BLINDADA: Quitamos el idEstudiante de la URL. 
        const respuesta = await fetch(`http://localhost:3000/api/reportes/dashboard/estudiante`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });

        // CONTROL DE EXPIRACIÓN: Si el servidor rebota el token (Expirado o Manipulado)
        if (respuesta.status === 401 || respuesta.status === 403) {
          alert("Tu sesión ha caducado por inactividad o seguridad. Serás redirigido al inicio.");
          cerrarSesion(); // Te expulsa al login y limpia el almacenamiento
          return;
        }

        const resultado = await respuesta.json();
        console.log("DATOS REALES DEL BACKEND:", resultado);

        if (!respuesta.ok) {
          throw new Error(resultado.error || 'No se pudo conectar con el servidor.');
        }

        if (activo) {
          setDatos(resultado);
          setCargando(false);
        }
      } catch (err) {
        if (activo) {
          // Si el fetch falla porque literalmente no hay internet, damos un mensaje claro
          if (!navigator.onLine) {
            setError('Sin conexión a internet. Restablece tu red para actualizar el panel.');
          } else {
            setError(err.message);
          }
          setCargando(false);
        }
      }
    };

    if (cargando) {
      cargarDatosDashboard();
    }

    return () => {
      activo = false;
    };
  }, [token, cargando, cerrarSesion]);

  if (cargando) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[300px] gap-3">
        <RefreshCw className="w-8 h-8 text-cyan-400 animate-spin" />
        <p className="text-slate-400 text-sm animate-pulse">Sincronizando con la base de datos de la facultad...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-6 rounded-2xl flex items-center gap-4 max-w-xl mx-auto">
        <AlertCircle className="w-8 h-8 shrink-0" />
        <div>
          <h4 className="font-bold text-white">Error de sincronización</h4>
          <p className="text-sm text-slate-400 mt-1">{error}</p>
          <button
            onClick={() => setCargando(true)} // Reintento controlado reactivamente
            className="mt-3 px-4 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700 transition-all"
          >
            Reintentar Conexión
          </button>
        </div>
      </div>
    );
  }

  const totalHoras = datos?.horas_acumuladas || 0;
  const horasReq = datos?.horas_requeridas || 1;
  const porcentajeHoras = Math.min(((totalHoras / horasReq) * 100).toFixed(1), 100);
  const nombreCompleto = datos?.nombres && datos.apellidos ? `${datos.nombres} ${datos.apellidos}` : 'Estudiante';
  const codigoEstudiante = datos?.codigo_estudiante ?? 'S/C';

  return (
    <div className="space-y-6">

      {/* CABECERA CON DATOS DEL ALUMNO */}
      <div className="bg-slate-900/20 border border-slate-800/60 p-6 rounded-2xl flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 shadow-md">
        <div>
          <h2 className="text-xl font-black text-white tracking-tight">Bienvenido, {nombreCompleto}</h2>
          <p className="text-sm text-slate-400 mt-0.5">Panel de control de Prácticas Preprofesionales</p>
        </div>
        <div className="bg-slate-950/60 border border-slate-800 px-4 py-2 rounded-xl text-center sm:text-right shrink-0">
          <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Código Universitario</p>
          <p className="text-sm font-mono font-bold text-cyan-400 mt-0.5">{codigoEstudiante}</p>
        </div>
      </div>

      {/* SECCIÓN 1: Tarjetas Métricas Principales */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

        {/* Tarjeta 1: Empresa Activa */}
        <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl relative overflow-hidden group shadow-lg">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <Building2 className="w-24 h-24 text-white" />
          </div>
          <div className="flex items-center gap-4 mb-4">
            <div className="p-3 bg-blue-600/10 rounded-xl border border-blue-500/20 text-blue-400 shadow-[0_0_15px_rgba(30,64,175,0.1)]">
              <Building2 className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Centro de Prácticas</p>
              <h3 className="text-lg font-bold text-white mt-0.5 truncate max-w-[180px]">{datos?.empresa || 'No Asignado'}</h3>
            </div>
          </div>
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            Convenio Vigente
          </span>
        </div>

        {/* Tarjeta 2: Actividades Reportadas */}
        <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl relative overflow-hidden group shadow-lg">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <CheckCircle2 className="w-24 h-24 text-white" />
          </div>
          <div className="flex items-center gap-4 mb-4">
            <div className="p-3 bg-cyan-600/10 rounded-xl border border-cyan-500/20 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.1)]">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Hitos de Bitácora</p>
              <h3 className="text-2xl font-black text-white mt-0.5">{datos?.total_actividades || 0}</h3>
            </div>
          </div>
          <p className="text-xs text-slate-400">Entradas del diario pendientes de firma por el tutor.</p>
        </div>

        {/* Tarjeta 3: Documentación Aprobada */}
        <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl relative overflow-hidden group shadow-lg">
          <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
            <FileUp className="w-24 h-24 text-white" />
          </div>
          <div className="flex items-center gap-4 mb-4">
            <div className="p-3 bg-purple-600/10 rounded-xl border border-purple-500/20 text-purple-400 shadow-[0_0_15px_rgba(147,51,234,0.1)]">
              <FileUp className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Entregables Validados</p>
              <h3 className="text-2xl font-black text-white mt-0.5">{datos?.documentos_aprobados || 0} / 4</h3>
            </div>
          </div>
          <p className="text-xs text-slate-400">Documentos oficiales validados por coordinación.</p>
        </div>
      </div>

      {/* SECCIÓN 2: Panel de Progreso de Horas */}
      <div className="bg-gradient-to-br from-slate-900/60 to-slate-950/40 border border-slate-800 p-6 rounded-2xl shadow-xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Clock className="w-5 h-5 text-cyan-400" />
            <h4 className="text-sm font-bold text-white uppercase tracking-wider">Progreso Cronológico Total</h4>
          </div>
          <span className="text-xl font-black text-cyan-400 tracking-tight">{porcentajeHoras}%</span>
        </div>

        <div className="w-full bg-slate-950 rounded-full h-3 border border-slate-800/50 p-0.5 overflow-hidden mb-4">
          <div
            className="bg-gradient-to-r from-blue-600 to-cyan-400 h-full rounded-full transition-all duration-1000 shadow-[0_0_12px_rgba(6,182,212,0.4)]"
            style={{ width: `${porcentajeHoras}%` }}
          ></div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 text-center sm:text-left">
          <div className="border-r border-slate-800/50 pr-4">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Horas Registradas</p>
            <p className="text-lg font-extrabold text-white mt-0.5">{totalHoras} hrs</p>
          </div>
          <div className="sm:border-r border-slate-800/50 pr-4">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Meta Académica</p>
            <p className="text-lg font-extrabold text-slate-400 mt-0.5">{datos?.horas_requeridas || 0} hrs</p>
          </div>
          <div className="col-span-2 sm:col-span-1 pt-2 sm:pt-0">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Modalidad Evaluada</p>
            <p className="text-sm font-bold text-cyan-400 mt-1 truncate">{datos?.tipo_practica || 'No Definido'}</p>
          </div>
        </div>
      </div>

    </div>
  );
}