// ==========================================
// RUTA DE TU ARCHIVO: src/components/Sidebar.jsx
// ==========================================
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import {
  LayoutDashboard,
  BookOpen,
  FileText,
  LogOut,
  GraduationCap,
  Bell,
  Folder,
  Shield,
  ClipboardList,
  Building
} from 'lucide-react';

export default function Sidebar({ vistaActiva, setVistaActiva }) {
  const { usuario, cerrarSesion } = useContext(AuthContext);
  // 🎯 Definición dinámica de los elementos del menú según el id_rol
  let menuItems;

  switch (Number(usuario?.id_rol)) {
    case 1: // 1. ADMINISTRADOR GLOBAL
      menuItems = [
        { id: 'admin_panel', label: 'Gestión de Usuarios', icon: Shield },
        { id: 'notificaciones', label: 'Alertas Sistema', icon: Bell },
      ];
      break;

    case 2: // 2. COORDINADOR ACADÉMICO (EPIS)
      menuItems = [
        { id: 'coordinador_panel', label: 'Panel General', icon: LayoutDashboard },
        { id: 'control_practicas', label: 'Control de Prácticas', icon: ClipboardList },
        { id: 'notificaciones', label: 'Alertas Académicas', icon: Bell },
      ];
      break;

    case 3: // 3. ESTUDIANTE (Por defecto)
      menuItems = [
        { id: 'dashboard', label: 'Panel General', icon: LayoutDashboard },
        { id: 'bitacora', label: 'Mi Bitácora', icon: BookOpen },
        { id: 'documentos', label: 'Mis Entregables', icon: FileText },
        { id: 'notificaciones', label: 'Notificaciones', icon: Bell },
      ];
      break;

    case 4: // 4. TUTOR EXTERNO (Empresa)
      menuItems = [
        { id: 'tutor_panel', label: 'Monitoreo Alumnos', icon: Folder },
        { id: 'notificaciones', label: 'Mis Alertas', icon: Bell },
      ];
      break;

    case 5: // 5. DECANO DE FACULTAD
      menuItems = [
        { id: 'decano_panel', label: 'Reportes Globales', icon: Building },
        { id: 'notificaciones', label: 'Alertas Institucionales', icon: Bell },
      ];
      break;

    default: // Respaldo por si ocurre un fallo con el rol
      menuItems = [
        { id: 'dashboard', label: 'Panel General', icon: LayoutDashboard },
      ];
  }

  return (
    <aside className="w-64 bg-[#0a0f1d] border-r border-slate-850 flex flex-col justify-between p-6 shrink-0 min-h-screen">
      <div className="space-y-8">
        {/* Identidad de la Institución */}
        <div className="flex items-center gap-3 px-2">
          <div className="p-2 bg-cyan-500/10 rounded-xl border border-cyan-500/20">
            <GraduationCap className="w-5 h-5 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-sm font-black tracking-wider text-white uppercase">PPP - EPIS</h1>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tight">Módulo de Gestión</p>
          </div>
        </div>

        {/* Perfil del Usuario Logueado */}
        <div className="p-4 bg-slate-950/40 border border-slate-900 rounded-2xl space-y-2">
          <div>
            <p className="text-xs font-bold text-white truncate font-sans">
              {usuario?.nombre_completo || (usuario?.nombres ? `${usuario.nombres} ${usuario.apellidos || ''}`.trim() : 'Usuario del Sistema')}
            </p>

            {/* Muestra el código correspondiente según el rol */}
            <p className="text-[10px] text-slate-500 font-medium mt-0.5">
              {Number(usuario?.id_rol) === 3 && usuario?.codigo_estudiante && `Código: ${usuario.codigo_estudiante}`}
              {Number(usuario?.id_rol) === 2 && (usuario?.codigo_docente || usuario?.codigo) && `Reg. Docente: ${usuario.codigo_docente || usuario.codigo}`}
              {Number(usuario?.id_rol) === 4 && usuario?.ruc_empresa && `RUC: ${usuario.ruc_empresa}`}
            </p>
          </div>

          <span className="inline-block px-2 py-0.5 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-[9px] font-extrabold rounded-md uppercase tracking-wide">
            {Number(usuario?.id_rol) === 1 ? 'Administrador'
              : Number(usuario?.id_rol) === 2 ? 'Coordinador EPIS'
                : Number(usuario?.id_rol) === 4 ? 'Tutor Externo'
                  : Number(usuario?.id_rol) === 5 ? 'Decano'
                    : 'Estudiante'}
          </span>
        </div>

        {/* Navegación Dinámica Filtrada */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icono = item.icon;
            const esActivo = vistaActiva === item.id;

            return (
              <button
                key={item.id}
                onClick={() => setVistaActiva(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 text-xs font-bold rounded-xl transition-all duration-200 ${esActivo
                    ? 'bg-gradient-to-r from-blue-600/10 to-cyan-500/5 text-cyan-400 border border-cyan-500/20 shadow-md shadow-cyan-950/10'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/40 border border-transparent'
                  }`}
              >
                <Icono className={`w-4 h-4 ${esActivo ? 'text-cyan-400' : 'text-slate-400'}`} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Botón de Salida */}
      <button
        onClick={cerrarSesion}
        className="w-full flex items-center gap-3 px-4 py-3 text-xs font-bold text-rose-400 hover:text-rose-300 hover:bg-rose-500/5 border border-transparent hover:border-rose-500/10 rounded-xl transition-all duration-200"
      >
        <LogOut className="w-4 h-4" />
        Cerrar Sesión
      </button>
    </aside>
  );
}