// ARCHIVO: frontend/src/components/PanelTutor.jsx
import { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Users, BookOpen, CheckCircle, AlertCircle, X, Save } from 'lucide-react';

export default function PanelTutor() {
  const { token, usuario } = useContext(AuthContext);

  const [estudiantes, setEstudiantes] = useState([]);
  const [estudianteSeleccionado, setEstudianteSeleccionado] = useState(null);
  const [bitacora, setBitacora] = useState([]);
  const [mostrarModal, setMostrarModal] = useState(false);

  // Estados para procesar una observación
  const [actividadAObservar, setActividadAObservar] = useState(null);
  const [comentarioObservacion, setComentarioObservacion] = useState('');

  // 1. CARGAR ESTUDIANTES ASIGNADOS (Con useEffect corregido sin efectos colaterales)
  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();

    const cargarEstudiantes = async () => {
      try {
        const respuesta = await fetch('http://localhost:3000/api/tutores/estudiantes', {
          headers: { 'Authorization': `Bearer ${token}` },
          signal: controller.signal
        });
        if (respuesta.ok) {
          const datos = await respuesta.json();
          if (isMounted) {
            setEstudiantes(datos);
          }
        }
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error("Error al cargar estudiantes:", error);
        }
      }
    };

    if (token) {
      cargarEstudiantes();
    }

    return () => {
      isMounted = false;
      controller.abort();
    };
  }, [token]);

  // Función auxiliar para refrescar la lista de estudiantes manualmente tras evaluar actividades
  const refrescarListaEstudiantes = async () => {
    try {
      const respuesta = await fetch('http://localhost:3000/api/tutores/estudiantes', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (respuesta.ok) {
        const datos = await respuesta.json();
        setEstudiantes(datos);
      }
    } catch (error) {
      console.error("Error al refrescar la lista de estudiantes:", error);
    }
  };

  // 2. Abrir y cargar la bitácora de un estudiante
  const abrirBitacora = async (estudiante) => {
    try {
      const respuesta = await fetch(`http://localhost:3000/api/tutores/estudiante/${estudiante.id_practica}/bitacora`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (respuesta.ok) {
        const datos = await respuesta.json();
        setBitacora(datos);
        setEstudianteSeleccionado(estudiante);
        setMostrarModal(true);
      }
    } catch (error) {
      console.error("Error al obtener la bitácora:", error);
    }
  };

  // 3. Procesar Aprobación Directa de una actividad
  const aprobarActividad = async (id_actividad) => {
    try {
      const respuesta = await fetch(`http://localhost:3000/api/tutor/bitacora/validar/${id_actividad}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          estado_validacion: 'Aprobado',
          observaciones_tutor: ''
        })
      });

      if (respuesta.ok) {
        // Refrescar la bitácora abierta actualmente
        setBitacora(bitacora.map(act => 
          act.id_actividad === id_actividad 
            ? { ...act, estado_validacion: 'Aprobado', observaciones_tutor: '' } 
            : act
        ));
        // Recargar los contadores en la lista principal de fondo
        refrescarListaEstudiantes();
      }
    } catch (error) {
      console.error("Error al aprobar actividad:", error);
    }
  };

  // 4. Enviar Observación de una actividad
  const enviarObservacion = async (e) => {
    e.preventDefault();
    if (!comentarioObservacion.trim()) return alert("Debe ingresar un comentario para la observación.");

    try {
      const respuesta = await fetch(`http://localhost:3000/api/tutor/bitacora/validar/${actividadAObservar.id_actividad}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          estado_validacion: 'Observado',
          observaciones_tutor: comentarioObservacion
        })
      });

      if (respuesta.ok) {
        setBitacora(bitacora.map(act => 
          act.id_actividad === actividadAObservar.id_actividad 
            ? { ...act, estado_validacion: 'Observado', observaciones_tutor: comentarioObservacion } 
            : act
        ));
        setActividadAObservar(null);
        setComentarioObservacion('');
        refrescarListaEstudiantes();
      }
    } catch (error) {
      console.error("Error al observar actividad:", error);
    }
  };

  return (
    <div className="space-y-6">
      {/* Encabezado */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-6 bg-slate-950/40 border border-slate-850 rounded-2xl gap-4">
        <div>
          <h3 className="text-lg font-bold text-white">¡Bienvenido, {usuario?.nombre_completo}!</h3>
          <p className="text-xs text-slate-400">Panel de validación de bitácoras de actividades para Tutores de Empresa.</p>
        </div>
        <span className="px-3 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-bold rounded-xl flex items-center gap-2">
          🏢 Tutor Externo
        </span>
      </div>

      {/* 📋 LISTA DE ESTUDIANTES ASIGNADOS */}
      <div className="bg-slate-950/40 border border-slate-850 rounded-2xl p-6">
        <h4 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
          <Users className="w-4 h-4 text-cyan-400" /> Estudiantes Bajo su Supervisión
        </h4>

        {estudiantes.length === 0 ? (
          <p className="text-xs text-slate-500 italic text-center py-4">No tiene estudiantes asignados en este ciclo.</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {estudiantes.map((est) => (
              <div key={est.id_practica} className="p-4 bg-slate-900/50 border border-slate-800 rounded-xl flex flex-col justify-between gap-4">
                <div>
                  <div className="flex justify-between items-start">
                    <div>
                      <h5 className="text-sm font-bold text-white">{est.estudiante_nombre}</h5>
                      <span className="text-[10px] text-cyan-400 font-mono">{est.codigo_estudiante}</span>
                    </div>
                    <span className="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-medium">
                      {est.tipo_practica}
                    </span>
                  </div>

                  {/* Barra de progreso de horas */}
                  <div className="mt-4 space-y-1">
                    <div className="flex justify-between text-[11px]">
                      <span className="text-slate-400">Progreso de Horas:</span>
                      <span className="text-white font-bold">{est.horas_acumuladas} / {est.horas_requeridas} hrs</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div 
                        className="bg-emerald-500 h-full transition-all duration-300"
                        style={{ width: `${Math.min((est.horas_acumuladas / est.horas_requeridas) * 100, 100)}%` }}
                      />
                    </div>
                  </div>
                </div>

                <button 
                  onClick={() => abrirBitacora(est)}
                  className="w-full py-2 bg-cyan-650 hover:bg-cyan-600 text-white font-bold text-xs rounded-lg flex items-center justify-center gap-1.5 transition-colors"
                >
                  <BookOpen className="w-4 h-4" /> Inspeccionar Bitácora
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ================= 🪟 MODAL: BITÁCORA DEL ESTUDIANTE ================= */}
      {mostrarModal && estudianteSeleccionado && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
          <div className="w-full max-w-4xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 flex flex-col max-h-[85vh]">
            
            <div className="flex justify-between items-start border-b border-slate-850 pb-3 mb-4 shrink-0">
              <div>
                <h4 className="text-base font-bold text-white">Bitácora de {estudianteSeleccionado.estudiante_nombre}</h4>
                <p className="text-xs text-slate-400">Revisa, aprueba u observa los registros de horas diarias.</p>
              </div>
              <button 
                onClick={() => setMostrarModal(false)}
                className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Tabla con scroll de la bitácora */}
            <div className="overflow-y-auto flex-1 pr-1">
              {bitacora.length === 0 ? (
                <p className="text-xs text-slate-500 italic text-center py-8">Este estudiante aún no ha registrado actividades en su bitácora.</p>
              ) : (
                <table className="w-full text-left text-xs text-slate-300">
                  <thead>
                    <tr className="border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-950/40 sticky top-0">
                      <th className="p-3">Fecha</th>
                      <th className="p-3 text-center">Horas</th>
                      <th className="p-3">Actividad Reportada</th>
                      <th className="p-3 text-center">Estado</th>
                      <th className="p-3 text-center">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-850/40">
                    {bitacora.map((act) => (
                      <tr key={act.id_actividad} className="hover:bg-slate-950/20">
                        <td className="p-3 whitespace-nowrap text-slate-400">
                          {new Date(act.fecha_actividad).toLocaleDateString()}
                        </td>
                        <td className="p-3 text-center font-bold text-white whitespace-nowrap">
                          {act.cantidad_horas} hrs
                        </td>
                        <td className="p-3 max-w-xs">
                          <p className="text-white font-medium line-clamp-3">{act.descripcion_actividad}</p>
                          {act.observaciones_tutor && (
                            <div className="mt-1.5 p-1.5 bg-red-500/5 border border-red-500/10 rounded text-[10px] text-red-400">
                              <strong>Observación:</strong> {act.observaciones_tutor}
                            </div>
                          )}
                        </td>
                        <td className="p-3 text-center whitespace-nowrap">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                            act.estado_validacion === 'Aprobado' 
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                              : act.estado_validacion === 'Observado'
                              ? 'bg-red-500/10 text-red-400 border border-red-500/20' 
                              : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                          }`}>
                            {act.estado_validacion}
                          </span>
                        </td>
                        <td className="p-3 text-center whitespace-nowrap">
                          {act.estado_validacion === 'Pendiente' ? (
                            <div className="flex items-center justify-center gap-1.5">
                              <button 
                                onClick={() => aprobarActividad(act.id_actividad)}
                                title="Aprobar"
                                className="p-1.5 bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20 border border-emerald-500/20 rounded-lg transition-colors"
                              >
                                <CheckCircle className="w-4 h-4" />
                              </button>
                              <button 
                                onClick={() => setActividadAObservar(act)}
                                title="Observar / Rechazar con comentario"
                                className="p-1.5 bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 rounded-lg transition-colors"
                              >
                                <AlertCircle className="w-4 h-4" />
                              </button>
                            </div>
                          ) : (
                            <span className="text-[10px] text-slate-500">Evaluado</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ================= 📝 MODAL SECUNDARIO: OBSERVAR ACTIVIDAD ================= */}
      {actividadAObservar && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/85 backdrop-blur-sm p-4">
          <form onSubmit={enviarObservacion} className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 shadow-2xl">
            <div className="flex items-center gap-2 text-red-400 border-b border-slate-800 pb-2">
              <AlertCircle className="w-5 h-5" />
              <div>
                <h4 className="text-sm font-bold text-white font-mono">Observar Actividad</h4>
                <p className="text-[10px] text-slate-400">Explique detalladamente qué correcciones requiere el estudiante.</p>
              </div>
            </div>

            <div className="text-xs bg-slate-950 p-3 rounded-lg border border-slate-850">
              <p className="text-slate-400 italic">"{actividadAObservar.descripcion_actividad}"</p>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Motivo de la Observación</label>
              <textarea 
                rows="3" 
                required
                placeholder="Ej. La descripción de la tarea de hoy es muy breve, o las horas reportadas no corresponden con la actividad..."
                value={comentarioObservacion} 
                onChange={(e) => setComentarioObservacion(e.target.value)} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-red-500/50 resize-none" 
              />
            </div>

            <div className="flex gap-3">
              <button 
                type="button" 
                onClick={() => setActividadAObservar(null)} 
                className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-xl"
              >
                Cancelar
              </button>
              <button 
                type="submit" 
                className="flex-1 py-2 bg-red-600 hover:bg-red-500 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-1.5"
              >
                <Save className="w-4 h-4" /> Guardar Observación
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}