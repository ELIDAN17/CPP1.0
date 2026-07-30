// ==========================================
// RUTA DE TU ARCHIVO: src/context/AuthContext.jsx
// ==========================================
/* eslint-disable react-refresh/only-export-components */
import { createContext, useState } from 'react';

// 1. Creamos el contexto maestro
export const AuthContext = createContext();

// 2. Creamos el proveedor del estado
export const AuthProvider = ({ children }) => {
  
  // Inicializamos el token de forma segura
  const [token, setToken] = useState(() => localStorage.getItem('token') || null);
  
  // Inicializamos el objeto usuario con un bloque protector anti-errores
  const [usuario, setUsuario] = useState(() => {
    try {
      const usuarioGuardado = localStorage.getItem('usuario');
      if (usuarioGuardado && usuarioGuardado !== 'undefined') {
        return JSON.parse(usuarioGuardado);
      }
    } catch (error) {
      console.error("Error al parsear el usuario del localStorage:", error);
    }
    return null;
  });

  const [cargando] = useState(false);

  // 🎯 NUEVO: Determinar la vista inicial por defecto basada en el rol del usuario recuperado
  const [vistaInicial, setVistaInicial] = useState(() => {
    try {
      const usuarioGuardado = localStorage.getItem('usuario');
      if (usuarioGuardado && usuarioGuardado !== 'undefined') {
        const user = JSON.parse(usuarioGuardado);
        
        // Evaluamos el id_rol (según tu DDL original)
        switch (Number(user.id_rol)) {
          case 1: return 'admin_panel';       // Administrador
          case 2: return 'coordinador_panel'; // Coordinador EPIS
          case 3: return 'dashboard';         // Estudiante (Por defecto)
          case 4: return 'tutor_panel';       // Tutor Externo (Empresa)
          case 5: return 'decano_panel';      // Decano de Facultad
          default: return 'dashboard';
        }
      }
    } catch (e) {
      console.error("Error al calcular vista inicial:", e);
    }
    return 'dashboard';
  });

  // Guarda de forma segura tanto el token como los datos del perfil
  const iniciarSesion = (nuevoToken, datosUsuario) => {
    localStorage.setItem('token', nuevoToken);
    
    // Si datosUsuario es válido lo guardamos, si no, dejamos el genérico antiguo
    const usuarioAAsignar = datosUsuario || { id_rol: 3, nombres: 'Estudiante', apellidos: 'UNA', codigo_estudiante: '000000' };
    localStorage.setItem('usuario', JSON.stringify(usuarioAAsignar));
    
    setToken(nuevoToken);
    setUsuario(usuarioAAsignar);

    // 🔀 DERIVACIÓN DINÁMICA DE ROLES AL INICIAR SESIÓN
    // Esto evita que un rol vea pantallas rotas de otro rol
    switch (Number(usuarioAAsignar.id_rol)) {
      case 1: // Administrador
        setVistaInicial('admin_panel');
        break;
      case 2: // Coordinador
        setVistaInicial('coordinador_panel');
        break;
      case 3: // Estudiante
        setVistaInicial('dashboard');
        break;
      case 4: // Tutor (Empresa)
        setVistaInicial('tutor_panel');
        break;
      case 5: // Decano
        setVistaInicial('decano_panel');
        break;
      default:
        setVistaInicial('dashboard');
    }
  };

  const cerrarSesion = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('usuario');
    
    setToken(null);
    setUsuario(null);
    setVistaInicial('dashboard');
    
    window.location.href = '/login'; 
  };

  return (
    <AuthContext.Provider value={{ usuario, token, iniciarSesion, cerrarSesion, cargando, vistaInicial }}>
      {children}
    </AuthContext.Provider>
  );
};