import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { BookOpen, Calendar, Clock, FileText, Send, CheckCircle, Clock3, AlertCircle, RefreshCw } from 'lucide-react';

export default function BitacoraEstudiante() {
  const { token } = useContext(AuthContext);
  const [actividades, setActividades] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);

  // Estados del Formulario
  const [fecha, setFecha] = useState('');
  const [horas, setHoras] = useState('');
  const [descripcion, setDescripcion] = useState('');
  const [mensaje, setMensaje] = useState({ tipo: '', texto: '' });

  // 1. Obtener historial inicial de manera segura
  useEffect(() => {
    if (!token) return;

    let activo = true;

    const obtenerActividades = async () => {
      try {
        const respuesta = await fetch(`http://localhost:3000/api/bitacora/estudiante`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const datos = await respuesta.json();

        if (activo && respuesta.ok) {
          setActividades(Array.isArray(datos) ? datos : []);
          setCargando(false);
        }
      } catch (err) {
        console.error("Error al traer bitácora:", err);
        if (activo) setCargando(false);
      }
    };

    obtenerActividades();

    return () => {
      activo = false;
    };
  }, [token]);

  // 2. Refrescar la lista de forma limpia usando la misma ruta del token
  const recargarHistorialSilenciosamente = async () => {
    try {
      const respuesta = await fetch(`http://localhost:3000/api/bitacora/estudiante`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const datos = await respuesta.json();
      if (respuesta.ok) {
        setActividades(Array.isArray(datos) ? datos : []);
      }
    } catch (err) {
      console.error("Error al refrescar:", err);
    }
  };

  // 3. Enviar nueva actividad al Backend alineado con los parámetros de la API
  const handleSubmit = async (e) => {
    e.preventDefault();
    setGuardando(true);
    setMensaje({ tipo: '', texto: '' });

    try {
      const respuesta = await fetch('http://localhost:3000/api/bitacora/registrar', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          fecha,              // Alineado con req.body.fecha
          horas: parseFloat(horas), // Alineado con req.body.horas
          descripcion         // Alineado con req.body.descripcion
        })
      });

      const resultado = await respuesta.json();

      if (!respuesta.ok) throw new Error(resultado.error || 'Error al registrar actividad');

      setMensaje({ tipo: 'exito', texto: '¡Actividad registrada con éxito!' });
      setFecha('');
      setHoras('');
      setDescripcion('');

      // Refrescamos la lista limpiamente sin parámetros extras
      recargarHistorialSilenciosamente();
    } catch (err) {
      setMensaje({ tipo: 'error', texto: err.message });
    } finally {
      setGuardando(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

      {/* COLUMNA 1: Formulario de Registro */}
      <div className="lg:col-span-1 bg-slate-900/40 border border-slate-800 p-6 rounded-2xl h-fit backdrop-blur-md">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2.5 bg-cyan-500/10 rounded-xl text-cyan-400 border border-cyan-500/20">
            <BookOpen className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white tracking-wide">Reportar Jornada</h3>
        </div>

        {mensaje.texto && (
          <div className={`mb-4 p-3 rounded-xl text-xs font-semibold flex items-center gap-2 ${mensaje.tipo === 'exito' ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400' : 'bg-rose-500/10 border border-rose-500/20 text-rose-400'
            }`}>
            {mensaje.tipo === 'exito' ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
            <span>{mensaje.texto}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Fecha de la Actividad</label>
            <div className="relative">
              <Calendar className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
              <input
                type="date"
                required
                value={fecha}
                onChange={(e) => setFecha(e.target.value)}
                className="w-full bg-slate-950/40 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-white text-xs focus:outline-none focus:border-cyan-500/50 transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Horas Invertidas</label>
            <div className="relative">
              <Clock className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
              <input
                type="number"
                required
                min="1"
                max="12"
                step="0.5"
                placeholder="Ej. 4"
                value={horas}
                onChange={(e) => setHoras(e.target.value)}
                className="w-full bg-slate-950/40 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-white text-xs focus:outline-none focus:border-cyan-500/50 transition-all"
              />
            </div>
          </div>

          <div>
            <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1.5">Descripción de Labores</label>
            <div className="relative">
              <FileText className="absolute left-3.5 top-3 w-4 h-4 text-slate-500" />
              <textarea
                required
                rows="4"
                placeholder="Detalla las actividades desarrolladas en la empresa..."
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
                className="w-full bg-slate-950/40 border border-slate-800 rounded-xl py-2.5 pl-10 pr-4 text-white text-xs focus:outline-none focus:border-cyan-500/50 transition-all resize-none"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={guardando}
            className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-semibold py-2.5 px-4 rounded-xl text-xs shadow-lg transition-all disabled:opacity-50"
          >
            {guardando ? 'Guardando...' : 'Subir a Bitácora'}
            {!guardando && <Send className="w-3.5 h-3.5" />}
          </button>
        </form>
      </div>

      {/* COLUMNA 2-3: Historial Tecnológico */}
      <div className="lg:col-span-2 bg-slate-900/40 border border-slate-800 p-6 rounded-2xl backdrop-blur-md">
        <h3 className="text-base font-bold text-white mb-6 tracking-wide">Línea de Tiempo de Actividades</h3>

        {cargando ? (
          <div className="flex justify-center items-center h-48 gap-2">
            <RefreshCw className="w-5 h-5 text-cyan-400 animate-spin" />
            <p className="text-slate-400 text-xs">Cargando registros...</p>
          </div>
        ) : actividades.length === 0 ? (
          <p className="text-slate-500 text-xs text-center py-12">No hay actividades registradas en esta etapa.</p>
        ) : (
          <div className="relative border-l border-slate-800 ml-4 space-y-6">
            {actividades.map((act, index) => (
              // Corregido el warning usando un identificador fallback seguro
              <div key={act.id_bitacora || index} className="relative pl-6 group">
                <span className={`absolute -left-2.5 top-1.5 w-5 h-5 rounded-full border-4 border-[#070a13] flex items-center justify-center ${act.estado_validacion === 'Aprobado' ? 'bg-emerald-500' :
                    act.estado_validacion === 'Observado' ? 'bg-rose-500' : 'bg-amber-500 animate-pulse'
                  }`}></span>

                <div className="bg-slate-950/40 border border-slate-800/60 p-4 rounded-xl hover:border-slate-700 transition-colors">
                  <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                    <div className="flex items-center gap-3 text-xs text-slate-400">
                      <span className="font-semibold text-white">
                        {act.fecha_actividad ? new Date(act.fecha_actividad).toLocaleDateString() : 'Fecha inválida'}
                      </span>
                      <span>•</span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-cyan-400" /> {act.cantidad_horas} hrs
                      </span>
                    </div>

                    <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-wider flex items-center gap-1 border ${act.estado_validacion === 'Aprobado' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' :
                        act.estado_validacion === 'Observado' ? 'bg-rose-500/10 border-rose-500/20 text-rose-400' :
                          'bg-amber-500/10 border-amber-500/20 text-amber-400'
                      }`}>
                      {act.estado_validacion === 'Aprobado' ? <CheckCircle className="w-3 h-3" /> : <Clock3 className="w-3 h-3" />}
                      {act.estado_validacion || 'Pendiente'}
                    </span>
                  </div>
                  <p className="text-slate-300 text-xs leading-relaxed">{act.descripcion_actividad || act.descripcion}</p>

                  {/* Mostrar observaciones del tutor si lo tiene */}
                  {act.observaciones_tutor && (
                    <div className="mt-2 p-2 bg-rose-500/5 border border-rose-500/10 rounded-lg text-rose-450 text-[11px] leading-relaxed">
                      <strong>Observación del Tutor:</strong> {act.observaciones_tutor}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

    </div>
  );
}