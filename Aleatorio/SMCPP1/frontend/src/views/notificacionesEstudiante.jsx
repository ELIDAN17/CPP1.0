// src/views/NotificacionesEstudiante.jsx
import { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { Bell, BellOff, Check, CheckCircle2, AlertTriangle, Info, ShieldAlert, RefreshCw } from 'lucide-react';

export default function NotificacionesEstudiante() {
  const { token } = useContext(AuthContext);
  const [notificaciones, setNotificaciones] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    if (!token) return;

    let activo = true; // Control de limpieza del efecto

    const cargarNotificaciones = async () => {
      try {
        const respuesta = await fetch('http://localhost:3000/api/notificaciones', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (respuesta.ok) {
          const datos = await respuesta.json();
          if (activo) {
            setNotificaciones(datos);
            setCargando(false);
          }
        }
      } catch (err) {
        console.error("Error al traer alertas:", err);
        if (activo) {
          setCargando(false);
        }
      }
    };

    if (cargando) {
      cargarNotificaciones();
    }

    return () => {
      activo = false; // Cancela la actualización si el componente se desmonta
    };
  }, [token, cargando]); // Dependencias limpias

  const marcarLeida = async (id) => {
    try {
      const respuesta = await fetch(`http://localhost:3000/api/notificaciones/${id}/leer`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (respuesta.ok) {
        // En lugar de mutar, actualizamos el estado y forzamos una recarga limpia
        setNotificaciones(prev => 
          prev.map(n => n.id_notificacion === id ? { ...n, leido: true } : n)
        );
      }
    } catch (err) {
      console.error("Error al actualizar alerta:", err);
    }
  };

  const obtenerIcono = (tipo) => {
    switch (tipo) {
      case 'exito': return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
      case 'alerta': return <AlertTriangle className="w-5 h-5 text-amber-400" />;
      case 'error': return <ShieldAlert className="w-5 h-5 text-rose-400" />;
      default: return <Info className="w-5 h-5 text-cyan-400" />;
    }
  };

  if (cargando) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[300px] gap-2">
        <RefreshCw className="w-7 h-7 text-cyan-400 animate-spin" />
        <p className="text-xs text-slate-500 font-medium">Buscando alertas del sistema...</p>
      </div>
    );
  }

  const noLeidas = notificaciones.filter(n => !n.leido).length;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      
      {/* Encabezado */}
      <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl flex items-center justify-between backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 rounded-xl text-cyan-400 border border-cyan-500/20 relative">
            <Bell className="w-5 h-5" />
            {noLeidas > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-rose-500 rounded-full animate-pulse" />
            )}
          </div>
          <div>
            <h2 className="text-base font-bold text-white tracking-wide">Centro de Notificaciones</h2>
            <p className="text-xs text-slate-400">Tienes {noLeidas} alertas sin leer actualmente.</p>
          </div>
        </div>
        <button 
          onClick={() => setCargando(true)}
          className="p-2 hover:bg-slate-800/80 rounded-xl border border-slate-800 text-slate-400 hover:text-white transition-all"
          title="Sincronizar alertas"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      {/* Lista de Alertas */}
      {notificaciones.length === 0 ? (
        <div className="bg-slate-900/20 border border-slate-850 p-12 rounded-2xl text-center">
          <BellOff className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h4 className="text-sm font-bold text-slate-400">Buzón completamente limpio</h4>
          <p className="text-xs text-slate-500 mt-1">Te avisaremos por aquí cuando tu tutor evalúe tus entregables.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {notificaciones.map((n) => (
            <div 
              key={n.id_notificacion}
              className={`p-4 rounded-xl border flex items-start justify-between gap-4 transition-all duration-300 backdrop-blur-sm ${
                n.leido 
                  ? 'bg-slate-900/20 border-slate-850/60 opacity-65' 
                  : 'bg-slate-900/60 border-slate-800/80 shadow-md shadow-slate-950/20'
              }`}
            >
              <div className="flex gap-3.5">
                <div className="mt-0.5 shrink-0">{obtenerIcono(n.tipo)}</div>
                <div>
                  <h4 className={`text-xs font-bold tracking-wide ${n.leido ? 'text-slate-400' : 'text-white'}`}>
                    {n.titulo}
                  </h4>
                  <p className="text-xs text-slate-400 mt-1 leading-relaxed">{n.mensaje}</p>
                  <span className="block text-[10px] text-slate-500 mt-2 font-medium">
                    {new Date(n.fecha_creacion).toLocaleString()}
                  </span>
                </div>
              </div>

              {!n.leido && (
                <button
                  onClick={() => marcarLeida(n.id_notificacion)}
                  className="p-1.5 bg-slate-950 border border-slate-800 hover:border-cyan-500/40 hover:text-cyan-400 text-slate-400 rounded-lg transition-all shrink-0"
                  title="Marcar como leída"
                >
                  <Check className="w-3.5 h-3.5" />
                </button>
              )}
            </div>
          ))}
        </div>
      )}

    </div>
  );
}