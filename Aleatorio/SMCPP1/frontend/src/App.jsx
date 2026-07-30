// ==========================================
// RUTA DE TU ARCHIVO: src/App.jsx
// ==========================================
import { useState, useContext } from 'react';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Login from './views/Login';
import Sidebar from './components/Sidebar';
import DashboardEstudiante from './views/DashboardEstudiante';
import BitacoraEstudiante from './views/BitacoraEstudiante';
import DocumentosEstudiante from './views/DocumentosEstudiante';
import NotificacionesEstudiante from './views/NotificacionesEstudiante';
import PanelTutor from './views/PanelTutor';
import PanelCoordinador from './views/PanelCoordinador';
import ControlPracticas from './views/ControlPracticas';
import PanelAdmin from './views/PanelAdmin';
import PanelDecano from './views/PanelDecano';

function ContenidoApp() {
  const { token, usuario } = useContext(AuthContext);

  // 🎯 Controlamos la navegación manual mediante clics en el Sidebar
  const [vistaManual, setVistaManual] = useState(null);

  // Si no hay sesión iniciada, mostramos el login de inmediato
  if (!token || !usuario) {
    return <Login />;
  }

  // 🎯 VISTA ACTIVA DINÁMICA: Si el usuario no ha hecho clic en el menú (vistaManual es null),
  // calculamos la vista de arranque directamente del id_rol en tiempo de ejecución.
  const vistaActiva = vistaManual || (() => {
    switch (Number(usuario.id_rol)) {
      case 1: return 'admin_panel';
      case 2: return 'coordinador_panel';
      case 3: return 'dashboard';
      case 4: return 'tutor_panel';
      case 5: return 'decano_panel';
      default: return 'dashboard';
    }
  })();

  return (
    <div className="min-h-screen flex bg-[#070a13] text-white">
      {/* El Sidebar actualiza vistaManual de forma limpia */}
      <Sidebar vistaActiva={vistaActiva} setVistaActiva={setVistaManual} />

      {/* Área de Contenido Principal Dinámico */}
      <main className="flex-1 p-8 overflow-y-auto">
        <header className="mb-8">
          <h2 className="text-2xl font-bold capitalize text-white tracking-tight">
            {vistaActiva === 'dashboard' ? 'Panel de Control General'
              : vistaActiva === 'bitacora' ? 'Mi Bitácora de Prácticas'
                : vistaActiva === 'documentos' ? 'Repositorio de Entregables'
                  : vistaActiva === 'notificaciones' ? 'Centro de Notificaciones'
                    : vistaActiva === 'tutor_panel' ? 'Supervisión de Estudiantes asignados'
                      : vistaActiva === 'admin_panel' ? 'Panel de Administración Global'
                        : vistaActiva === 'coordinador_panel' ? 'Panel de Coordinación Académica'
                          : vistaActiva === 'decano_panel' ? 'Panel de Decanato'
                            : vistaActiva === 'control_practicas' ? 'Control de Prácticas Preprofesionales'
                              : vistaActiva}
          </h2>
          <p className="text-slate-400 text-sm mt-0.5">Gestión en tiempo real de tu proceso académico.</p>
        </header>

        {/* Renderizado condicional síncrono óptimo basado en la vista calculada */}
        <div className="bg-slate-900/20 border border-slate-850 p-6 rounded-3xl backdrop-blur-md min-h-[400px]">
          {vistaActiva === 'dashboard' && <DashboardEstudiante />}
          {vistaActiva === 'bitacora' && <BitacoraEstudiante />}
          {vistaActiva === 'documentos' && <DocumentosEstudiante />}
          {vistaActiva === 'notificaciones' && <NotificacionesEstudiante />}
          {vistaActiva === 'tutor_panel' && <PanelTutor />}
          {vistaActiva === 'coordinador_panel' && <PanelCoordinador />}
          {vistaActiva === 'admin_panel' && <PanelAdmin />}
          {vistaActiva === 'decano_panel' && <PanelDecano />}

          {vistaActiva === 'control_practicas' && <ControlPracticas />}
        </div>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <ContenidoApp />
    </AuthProvider>
  );
}