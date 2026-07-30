import { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Users, FileCheck, AlertTriangle, GraduationCap, ChevronDown, ChevronUp, Eye, X, Save, MessageSquare, ExternalLink } from 'lucide-react';

export default function PanelCoordinador() {
  const { token, usuario } = useContext(AuthContext);
  
  const [listaAlumnos, setListaAlumnos] = useState([]);
  const [tarjetaExpandida, setTarjetaExpandida] = useState(null);
  
  // Estados para el Modal del "Ojito" (Ver archivos y Dictaminar Estado)
  const [alumnoSeleccionado, setAlumnoSeleccionado] = useState(null);
  const [mostrarModalCalificar, setMostrarModalCalificar] = useState(false);

  // Estados para el Modal de Rechazo (Motivo del rechazo)
  const [alumnoARechazar, setAlumnoARechazar] = useState(null);
  const [mostrarModalRechazo, setMostrarModalRechazo] = useState(false);
  
  // Estados para persistir cambios reales en la BD
  const [estadoDictamen, setEstadoDictamen] = useState('Aceptado');
  const [observaciones, setObservaciones] = useState('');

  // Cargar datos reales vinculados a la estructura relacional
  useEffect(() => {
    const cargarDatosReales = async () => {
      try {
        const respuesta = await fetch('http://localhost:3000/api/reportes/panel/coordinador', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (respuesta.ok) {
          const datos = await respuesta.json();
          setListaAlumnos(datos);
        }
      } catch (error) {
        console.error("Error al sincronizar el panel del coordinador:", error);
      }
    };
    if (token) cargarDatosReales();
  }, [token]);

  // Abrir visor de archivos reales (Ojito)
  const abrirVisorExpediente = (alumno) => {
    setAlumnoSeleccionado(alumno);
    setObservaciones(alumno.observaciones_documento || '');
    setEstadoDictamen(alumno.estado_general || 'Aceptado');
    setMostrarModalCalificar(true);
  };

  // Guardar Dictamen Final / Evaluación en la BD
  const manejarGuardarDictamen = async (e) => {
    e.preventDefault();
    try {
      const respuesta = await fetch(`http://localhost:3000/api/practicas/${alumnoSeleccionado.id_practica}/dictaminar`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({
          estado_general: estadoDictamen,
          observaciones: observaciones
        })
      });
      if (respuesta.ok) {
        alert("Evaluación registrada con éxito en la base de datos.");
        setMostrarModalCalificar(false);
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
    }
  };

  // Abrir Modal para ingresar motivo de Rechazo con texto obligatorio
  const abrirModalRechazo = (alumno) => {
    setAlumnoARechazar(alumno);
    setObservaciones('');
    setMostrarModalRechazo(true);
  };

  // Enviar el Rechazo con su respectivo motivo actualizando la tabla
  const manejarEnviarRechazo = async (e) => {
    e.preventDefault();
    try {
      const respuesta = await fetch(`http://localhost:3000/api/practicas/${alumnoARechazar.id_practica}/dictaminar`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify({
          estado_general: 'Rechazado',
          observaciones: observaciones
        })
      });
      if (respuesta.ok) {
        alert("Práctica rechazada. Registro actualizado.");
        setMostrarModalRechazo(false);
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
    }
  };

  // Clasificación estricta de datos basándose en los strings exactos del Seed
  const datosTarjeta1 = listaAlumnos; 
  const datosTarjeta2 = listaAlumnos.filter(p => p.estado_general?.trim() === 'En Proceso');
  const datosTarjeta3 = listaAlumnos.filter(p => p.estado_general?.trim() === 'Pendiente');

  return (
    <div className="space-y-6 relative">
      {/* Encabezado */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-6 bg-slate-950/40 border border-slate-850 rounded-2xl gap-4">
        <div className="space-y-1">
          <h3 className="text-lg font-bold text-white">¡Bienvenido, Ing. {usuario?.nombre_completo}!</h3>
          <p className="text-xs text-slate-400">Panel administrativo de control y decisiones de la EPIS.</p>
        </div>
        <span className="px-3 py-1 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs font-bold rounded-xl flex items-center gap-2 shrink-0">
          <GraduationCap className="w-4 h-4" /> Docente: {usuario?.codigo}
        </span>
      </div>

      {/* 📊 SECCIÓN DE TARJETAS */}
      <div className="flex flex-col gap-4">
        
        {/* ================= TARJETA 1: TOTAL ESTUDIANTES ================= */}
        <div className={`border rounded-2xl overflow-hidden transition-all ${tarjetaExpandida === 1 ? 'border-blue-500/40 bg-slate-900/30' : 'bg-slate-950/40 border-slate-850/60'}`}>
          <div onClick={() => setTarjetaExpandida(tarjetaExpandida === 1 ? null : 1)} className="p-5 flex items-center justify-between cursor-pointer select-none">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-blue-500/10 text-blue-400"><Users className="w-5 h-5" /></div>
              <div>
                <p className="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Número de Estudiantes Asignados</p>
                <p className="text-2xl font-black text-white mt-0.5">{datosTarjeta1.length}</p>
              </div>
            </div>
            <div className="text-slate-500">{tarjetaExpandida === 1 ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}</div>
          </div>
          {tarjetaExpandida === 1 && (
            <div className="border-t border-slate-850/40 bg-slate-950/50 p-4">
              <table className="w-full text-left text-xs text-slate-300">
                <thead>
                  <tr className="border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-900/20">
                    <th className="p-3">Código</th>
                    <th className="p-3">Nombre Completo del Alumno</th>
                    <th className="p-3 text-center">Estado General</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-850/40">
                  {datosTarjeta1.map((alumno) => (
                    <tr key={alumno.id_practica} className="hover:bg-slate-900/30">
                      <td className="p-3 font-mono text-cyan-400 font-bold">{alumno.codigo_estudiante}</td>
                      <td className="p-3 text-white font-medium">{alumno.estudiante_nombre}</td>
                      <td className="p-3 text-center">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${alumno.estado_general === 'Aceptado' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : alumno.estado_general === 'Rechazado' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 'bg-slate-850 text-slate-400'}`}>
                          {alumno.estado_general}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* ================= TARJETA 2: PRÁCTICAS EN PROCESO (OJITO + RECHAZAR) ================= */}
        <div className={`border rounded-2xl overflow-hidden transition-all ${tarjetaExpandida === 2 ? 'border-emerald-500/40 bg-slate-900/30' : 'bg-slate-950/40 border-slate-850/60'}`}>
          <div onClick={() => setTarjetaExpandida(tarjetaExpandida === 2 ? null : 2)} className="p-5 flex items-center justify-between cursor-pointer select-none">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-emerald-500/10 text-emerald-400"><FileCheck className="w-5 h-5" /></div>
              <div>
                <p className="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Prácticas en Proceso / Enviadas</p>
                <p className="text-2xl font-black text-white mt-0.5">{datosTarjeta2.length}</p>
              </div>
            </div>
            <div className="text-slate-500">{tarjetaExpandida === 2 ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}</div>
          </div>
          {tarjetaExpandida === 2 && (
            <div className="border-t border-slate-850/40 bg-slate-950/50 p-4">
              {datosTarjeta2.length === 0 ? (
                <p className="text-xs text-slate-500 italic text-center p-2">No hay expedientes pendientes de inspección.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead>
                      <tr className="border-b border-slate-800 text-[10px] font-bold text-slate-400 uppercase tracking-wider bg-slate-900/20">
                        <th className="p-3">Alumno</th>
                        <th className="p-3">Empresa / Tipo</th>
                        <th className="p-3 text-center">Horas Validadas</th>
                        <th className="p-3 text-center">Acciones</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-850/40">
                      {datosTarjeta2.map((p) => (
                        <tr key={p.id_practica} className="hover:bg-slate-900/30">
                          <td className="p-3">
                            <div className="font-semibold text-white">{p.estudiante_nombre}</div>
                            <div className="text-[10px] text-slate-500">{p.codigo_estudiante}</div>
                          </td>
                          <td className="p-3">
                            <div className="text-white font-medium truncate max-w-[150px]">{p.razon_social}</div>
                            <div className="text-[10px] text-slate-400">{p.tipo_practica}</div>
                          </td>
                          <td className="p-3 text-center">
                            <span className="font-bold text-cyan-400">{p.horas_acumuladas}</span>
                            <span className="text-slate-500">/{p.horas_requeridas}h</span>
                          </td>
                          <td className="p-3 text-center">
                            <div className="flex items-center justify-center gap-1.5">
                              {/* Ojito para ver archivos en la BD y evaluar */}
                              <button onClick={() => abrirVisorExpediente(p)} title="Ver archivos reales y evaluar" className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors">
                                <Eye className="w-4 h-4" />
                              </button>
                              {/* Botón directo de rechazo con justificación */}
                              <button onClick={() => abrirModalRechazo(p)} title="Rechazar y Enviar Observación" className="p-1.5 bg-red-500/10 text-red-400 hover:bg-red-500/20 border border-red-500/20 rounded-lg transition-colors">
                                <X className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Tarjeta 3: Pendientes */}
        <div className={`border rounded-2xl overflow-hidden transition-all ${tarjetaExpandida === 3 ? 'border-amber-500/40 bg-slate-900/30' : 'bg-slate-950/40 border-slate-850/60'}`}>
          <div onClick={() => setTarjetaExpandida(tarjetaExpandida === 3 ? null : 3)} className="p-5 flex items-center justify-between cursor-pointer select-none">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-xl bg-amber-500/10 text-amber-400"><AlertTriangle className="w-5 h-5" /></div>
              <div>
                <p className="text-[11px] font-bold text-slate-400 tracking-wider uppercase">Pendientes (Convenio y Registro Inicial)</p>
                <p className="text-2xl font-black text-white mt-0.5">{datosTarjeta3.length}</p>
              </div>
            </div>
            <div className="text-slate-500">{tarjetaExpandida === 3 ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}</div>
          </div>
          {tarjetaExpandida === 3 && (
            <div className="border-t border-slate-850/40 bg-slate-950/50 p-4">
              <table className="w-full text-left text-xs text-slate-300">
                <tbody className="divide-y divide-slate-850/40">
                  {datosTarjeta3.map((p) => (
                    <tr key={p.id_practica} className="hover:bg-slate-900/30">
                      <td className="p-3"><div className="font-semibold text-white">{p.estudiante_nombre}</div></td>
                      <td className="p-3 text-white">{p.razon_social || 'Convenio sin Empresa Mapeada'}</td>
                      <td className="p-3"><span className="px-2 py-0.5 bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full text-[10px] font-bold">{p.estado_general}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* ================= 🪟 MODAL 1: VISOR DE DOCUMENTACIÓN REAL (OJITO) ================= */}
      {mostrarModalCalificar && alumnoSeleccionado && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <form onSubmit={manejarGuardarDictamen} className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 space-y-4">
            <div className="flex justify-between items-start border-b border-slate-800 pb-2">
              <div>
                <h4 className="text-sm font-bold text-white">Documentos de la Práctica (PostgreSQL)</h4>
                <p className="text-[11px] text-slate-400">Archivos extraídos dinámicamente de la tabla `documentos_practica`.</p>
              </div>
              <button type="button" onClick={() => setMostrarModalCalificar(false)} className="text-slate-400 hover:text-white text-xs bg-slate-800 px-2.5 py-1 rounded-lg">Cerrar</button>
            </div>

            {/* Mapeo de Enlaces Reales obtenidos del backend */}
            <div className="space-y-1.5">
              <label className="block text-[10px] font-bold text-slate-400 uppercase">Archivos Registrados:</label>
              <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-850 space-y-2 text-xs">
                {alumnoSeleccionado.url_plan_trabajo ? (
                  <button 
        type="button"
        onClick={() => {
          // Aseguramos que empiece con barra '/' para evitar errores de concatenación
          const path = alumnoSeleccionado.url_plan_trabajo.startsWith('/') 
            ? alumnoSeleccionado.url_plan_trabajo 
            : `/${alumnoSeleccionado.url_plan_trabajo}`;
          
          window.open(`http://localhost:3000${path}`, '_blank');
        }}
        className="flex items-center gap-1.5 text-cyan-400 hover:underline font-medium bg-transparent border-none cursor-pointer"
      >
        📄 Plan de Trabajo Inicial (Tipo Doc: 2) <ExternalLink className="w-3 h-3" />
      </button>
    ) : (
      <span className="block text-slate-600 italic">No cargó archivo de Plan de Trabajo</span>
    )}

    {alumnoSeleccionado.url_informe_final ? (
      <button 
        type="button"
        onClick={() => {
          // Aseguramos que empiece con barra '/' para evitar errores de concatenación
          const path = alumnoSeleccionado.url_informe_final.startsWith('/') 
            ? alumnoSeleccionado.url_informe_final 
            : `/${alumnoSeleccionado.url_informe_final}`;
          
          window.open(`http://localhost:3000${path}`, '_blank');
        }}
        className="flex items-center gap-1.5 text-cyan-400 hover:underline font-medium bg-transparent border-none cursor-pointer"
      >
        📄 Informe Final de Prácticas (Tipo Doc: 4) <ExternalLink className="w-3 h-3" />
      </button>
                ) : (
                  <span className="block text-slate-600 italic">No cargó archivo de Informe Final</span>
                )}
              </div>
            </div>

            {/* Configuración de Dictamen conforme al Seed de la BD */}
            <div className="grid grid-cols-1 gap-3">
              <div>
                <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Cambiar Estado General</label>
                <select value={estadoDictamen} onChange={(e) => setEstadoDictamen(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500/50">
                  <option value="Aceptado">Aceptado / Conforme</option>
                  <option value="En Proceso">Mantener En Proceso</option>
                  <option value="Rechazado">Rechazado</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Comentarios de Revisión Académica</label>
              <textarea rows="3" placeholder="Añada observaciones sobre el estado o el cumplimiento de horas del expediente..." value={observaciones} onChange={(e) => setObservaciones(e.target.value)} className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-cyan-500/50 resize-none" />
            </div>

            <button type="submit" className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-2">
              <Save className="w-4 h-4" /> Registrar Dictamen Real
            </button>
          </form>
        </div>
      )}

      {/* ================= 🪟 MODAL 2: CUADRO DE MENSAJE POR RECHAZO (MOTIVO OBLIGATORIO) ================= */}
      {mostrarModalRechazo && alumnoARechazar && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <form onSubmit={manejarEnviarRechazo} className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 space-y-4">
            <div className="flex items-center gap-2 text-red-400 border-b border-slate-800 pb-2">
              <MessageSquare className="w-5 h-5" />
              <div>
                <h4 className="text-sm font-bold text-white">Especificar Observación de Rechazo</h4>
                <p className="text-[10px] text-slate-400">Actualizará el estado del expediente a Rechazado en la BD.</p>
              </div>
            </div>

            <div className="text-xs bg-slate-950/50 p-3 rounded-xl border border-slate-850">
              <p className="text-slate-400">Estudiante: <span className="text-white font-bold">{alumnoARechazar.estudiante_nombre}</span></p>
            </div>

            <div>
              <label className="block text-[10px] font-bold text-slate-400 uppercase mb-1">Comentarios / Correcciones Requeridas</label>
              <textarea 
                rows="4" 
                required
                placeholder="Ej. Faltan firmas en el Plan de Trabajo Inicial o las horas de la bitácora registran inconsistencias..."
                value={observaciones} 
                onChange={(e) => setObservaciones(e.target.value)} 
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-red-500/50 resize-none" 
              />
            </div>

            <div className="flex gap-2.5 pt-1">
              <button type="button" onClick={() => setMostrarModalRechazo(false)} className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs rounded-xl">Cancelar</button>
              <button type="submit" className="flex-1 py-2 bg-red-600 hover:bg-red-500 text-white font-bold text-xs rounded-xl">Procesar Rechazo</button>
            </div>
          </form>
        </div>
      )}

    </div>
  );
}