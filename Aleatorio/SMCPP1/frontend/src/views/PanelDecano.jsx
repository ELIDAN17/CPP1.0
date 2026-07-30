import { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { GraduationCap, Clock, Award, CheckCircle, RefreshCw, BarChart2, Briefcase, FileClock } from 'lucide-react';

export default function PanelDecano() {
    const { token, usuario } = useContext(AuthContext);

    const [metricas, setMetricas] = useState(null);
    const [practicas, setPracticas] = useState([]);
    const [cargando, setCargando] = useState(true);

    const cargarDatos = async () => {
        try {
            setCargando(true);
            const res = await fetch('http://localhost:3000/api/decano/reportes-macro', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const datos = await res.json();
                setMetricas(datos.desempeno);
                setPracticas(datos.practicas || []);
            }
        } catch (error) {
            console.error("Error al cargar reportes de decanato:", error);
        } finally {
            setCargando(false);
        }
    };

    useEffect(() => {
        if (token) cargarDatos();
    }, [token]);

    return (
        <div className="space-y-6">

            {/* CABECERA INFORMATIVA */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-6 bg-slate-950/40 border border-slate-850 rounded-2xl gap-4">
                <div className="space-y-1">
                    <h3 className="text-lg font-bold text-white">¡Bienvenido, Dr. {usuario?.nombre_completo}!</h3>
                    <p className="text-xs text-slate-400">Consolidado general de estadísticas, KPIs e indicadores macro de prácticas preprofesionales.</p>
                </div>
                <span className="px-3 py-1 bg-purple-500/10 text-purple-400 border border-purple-500/20 text-xs font-bold rounded-xl flex items-center gap-2 shrink-0">
                    <Award className="w-4 h-4" /> Decano de Facultad
                </span>
            </div>

            {cargando ? (
                <div className="flex justify-center items-center h-48 gap-2">
                    <RefreshCw className="w-5 h-5 text-cyan-400 animate-spin" />
                    <p className="text-slate-400 text-xs">Cargando reporte ejecutivo macro...</p>
                </div>
            ) : (
                <>
                    {/* 📊 SECCIÓN DE TARJETAS KPIs */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-5">

                        {/* KPI 1: Total Alumnos */}
                        <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl relative overflow-hidden group shadow-lg">
                            <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                <GraduationCap className="w-20 h-20 text-white" />
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-purple-600/10 rounded-xl border border-purple-500/20 text-purple-400">
                                    <GraduationCap className="w-6 h-6" />
                                </div>
                                <div>
                                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Alumnos Registrados</p>
                                    <h3 className="text-2xl font-black text-white mt-0.5">{metricas?.total_estudiantes || 0}</h3>
                                </div>
                            </div>
                            <p className="text-[10px] text-slate-500 mt-2">Total de alumnos mapeados en sistema académico EPIS.</p>
                        </div>

                        {/* KPI 2: Total Horas Validadas */}
                        <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl relative overflow-hidden group shadow-lg">
                            <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                <Clock className="w-20 h-20 text-white" />
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-cyan-600/10 rounded-xl border border-cyan-500/20 text-cyan-400">
                                    <Clock className="w-6 h-6" />
                                </div>
                                <div>
                                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Horas Validadas Totales</p>
                                    <h3 className="text-2xl font-black text-white mt-0.5">{metricas?.total_horas_validadas || 0} hrs</h3>
                                </div>
                            </div>
                            <p className="text-[10px] text-slate-500 mt-2">Suma de horas firmadas por tutores en bitácoras.</p>
                        </div>

                        {/* KPI 3: Practicas Activas */}
                        <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl relative overflow-hidden group shadow-lg">
                            <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                <Briefcase className="w-20 h-20 text-white" />
                            </div>
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-blue-600/10 rounded-xl border border-blue-500/20 text-blue-400">
                                    <Briefcase className="w-6 h-6" />
                                </div>
                                <div>
                                    <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Procesos de Prácticas</p>
                                    <h3 className="text-2xl font-black text-white mt-0.5">
                                        {metricas?.distribucion_estados?.reduce((a, c) => a + c.cantidad, 0) || 0}
                                    </h3>
                                </div>
                            </div>
                            <div className="flex gap-2.5 mt-2.5 text-[9px] uppercase tracking-wide font-extrabold">
                                {metricas?.distribucion_estados?.map((dist) => (
                                    <span key={dist.estado} className="px-1.5 py-0.5 bg-slate-950/80 border border-slate-850 rounded text-slate-400">
                                        {dist.estado}: <strong className="text-cyan-400">{dist.cantidad}</strong>
                                    </span>
                                ))}
                            </div>
                        </div>

                    </div>

                    {/* 📊 CUADRO DE LISTADO GLOBAL DE AVANCE */}
                    <div className="bg-slate-950/40 border border-slate-850 rounded-2xl overflow-hidden shadow-lg">
                        <div className="p-5 border-b border-slate-850/80 bg-slate-900/10 flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <BarChart2 className="w-4 h-4 text-cyan-400" />
                                <h4 className="text-xs font-extrabold uppercase tracking-wider text-white">Seguimiento Consolidado de Avance de Alumnos</h4>
                            </div>
                            <button
                                onClick={cargarDatos}
                                title="Actualizar Datos"
                                className="p-1 px-2.5 bg-slate-800 hover:bg-slate-750 text-[10px] font-bold text-slate-300 hover:text-white rounded-lg flex items-center gap-1 transition-all"
                            >
                                <RefreshCw className="w-3.5 h-3.5" /> Refrescar
                            </button>
                        </div>

                        {practicas.length === 0 ? (
                            <p className="text-slate-500 text-xs text-center py-12">No hay registros de carpetas de prácticas en la facultad.</p>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full text-left border-collapse text-xs text-slate-300">
                                    <thead>
                                        <tr className="border-b border-slate-850 bg-slate-900/20 text-[10px] font-bold text-slate-400 tracking-wider uppercase">
                                            <th className="p-4">Estudiante</th>
                                            <th className="p-4">Empresa / Entidad</th>
                                            <th className="p-4">Modalidad</th>
                                            <th className="p-4">Progreso de Horas</th>
                                            <th className="p-4">Estado General</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-850/40">
                                        {practicas.map((p) => {
                                            const pct = Math.min(((p.horas_acumuladas / (p.horas_requeridas || 1)) * 100).toFixed(1), 100);
                                            return (
                                                <tr key={p.id_practica} className="hover:bg-slate-900/10 transition-colors">
                                                    <td className="p-4 font-normal">
                                                        <div className="font-semibold text-white">{p.estudiante}</div>
                                                        <div className="text-[10px] text-slate-500 font-mono">{p.codigo_estudiante}</div>
                                                    </td>
                                                    <td className="p-4 font-medium text-slate-350">{p.empresa}</td>
                                                    <td className="p-4 text-slate-400 font-medium">{p.tipo_practica}</td>
                                                    <td className="p-4">
                                                        <div className="flex items-center gap-3">
                                                            <div className="w-24 bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-805/50">
                                                                <div className="bg-gradient-to-r from-blue-600 to-cyan-400 h-full rounded-full" style={{ width: `${pct}%` }}></div>
                                                            </div>
                                                            <span className="font-bold text-cyan-400 text-[10px]">{pct}% ({p.horas_acumuladas}/{p.horas_requeridas}h)</span>
                                                        </div>
                                                    </td>
                                                    <td className="p-4">
                                                        <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${p.estado_general === 'Aceptado' || p.estado_general === 'Finalizado' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                                                                p.estado_general === 'Rechazado' ? 'bg-rose-500/10 text-rose-455 border-rose-500/20' :
                                                                    p.estado_general === 'En Proceso' ? 'bg-blue-500/10 text-blue-450 border-blue-500/20' :
                                                                        'bg-amber-500/10 text-amber-440 border-amber-500/20'
                                                            }`}>
                                                            {p.estado_general}
                                                        </span>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                </>
            )}

        </div>
    );
}
