import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Eye, CheckCircle, XCircle, Clock, Search } from 'lucide-react';

export default function ControlPracticas() {
  const { token } = useContext(AuthContext);
  const [practicas, setPracticas] = useState([]);
  const [busqueda, setBusqueda] = useState('');

  // Cargar la lista real de prácticas asignadas al coordinador
  useEffect(() => {
    const cargarPracticas = async () => {
      try {
        const res = await fetch('http://localhost:3000/api/reportes/panel/coordinador', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const datos = await res.json();
          setPracticas(datos);
        }
      } catch (error) {
        console.error("Error al cargar la lista de prácticas:", error);
      }
    };
    if (token) cargarPracticas();
  }, [token]);

  // Filtro de búsqueda por alumno o empresa
  const practicasFiltradas = practicas.filter(p => 
    p.estudiante_nombre?.toLowerCase().includes(busqueda.toLowerCase()) ||
    p.razon_social?.toLowerCase().includes(busqueda.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-white">Control de Prácticas Preprofesionales</h3>
          <p className="text-xs text-slate-400">Listado oficial de expedientes y estados de carpetas en la EPIS.</p>
        </div>

        {/* Barra de Búsqueda */}
        <div className="relative max-w-xs w-full">
          <span className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-slate-500">
            <Search className="w-4 h-4" />
          </span>
          <input
            type="text"
            placeholder="Buscar alumno o empresa..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
            className="w-full text-xs pl-9 pr-4 py-2 bg-slate-950/40 border border-slate-850 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors"
          />
        </div>
      </div>

      {/* Tabla de Expedientes Reales */}
      <div className="bg-slate-950/40 border border-slate-850 rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-850 bg-slate-900/20 text-[11px] font-bold text-slate-400 tracking-wider uppercase">
                <th className="p-4">Estudiante</th>
                <th className="p-4">Empresa / Tipo</th>
                <th className="p-4 text-center">Horas</th>
                <th className="p-4">Estado</th>
                <th className="p-4 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850/60 text-xs text-slate-300">
              {practicasFiltradas.length === 0 ? (
                <tr>
                  <td colSpan="5" className="p-8 text-center text-slate-500">
                    No se encontraron registros de prácticas asignadas en este momento.
                  </td>
                </tr>
              ) : (
                practicasFiltradas.map((p) => (
                  <tr key={p.id_practica} className="hover:bg-slate-900/20 transition-colors">
                    <td className="p-4">
                      <div className="font-semibold text-white">{p.estudiante_nombre}</div>
                      <div className="text-[10px] text-slate-500">{p.codigo_estudiante}</div>
                    </td>
                    <td className="p-4">
                      <div className="text-white">{p.razon_social}</div>
                      <div className="text-[10px] text-slate-400">{p.tipo_practica}</div>
                    </td>
                    <td className="p-4 text-center">
                      <span className="font-bold text-cyan-400">{p.horas_acumuladas}</span>
                      <span className="text-slate-500"> / {p.horas_requeridas} hrs</span>
                    </td>
                    <td className="p-4">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                        p.estado_general === 'Finalizado' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                        p.estado_general === 'En Proceso' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' :
                        'bg-amber-500/10 text-amber-400 border-amber-500/20'
                      }`}>
                        {p.estado_general === 'Finalizado' ? <CheckCircle className="w-3 h-3" /> :
                         p.estado_general === 'En Proceso' ? <Clock className="w-3 h-3" /> : 
                         <XCircle className="w-3 h-3" />}
                        {p.estado_general}
                      </span>
                    </td>
                    <td className="p-4 text-center">
                      <button 
                        title="Revisar Expediente"
                        className="p-1.5 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors inline-flex items-center"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}