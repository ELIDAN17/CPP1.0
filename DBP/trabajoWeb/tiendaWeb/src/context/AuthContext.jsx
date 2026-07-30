// src/frontend/src/context/AuthContext.jsx
import React, { createContext, useState, useEffect, useContext } from 'react';
// import { useNavigate } from 'react-router-dom'; // ¡ELIMINA ESTA LÍNEA!

// Crea el contexto de autenticación
const AuthContext = createContext(null);

// Hook personalizado para usar el contexto de autenticación
export const useAuth = () => {
  return useContext(AuthContext);
};

// Proveedor de autenticación que envuelve la aplicación
export const AuthProvider = ({ children }) => {
  // Estado para el usuario (contendrá id, nombre, email, rol, etc.)
  const [user, setUser] = useState(null);
  // Estado para el token JWT
  const [token, setToken] = useState(null);
  // Estado booleano para saber si el usuario está logeado
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // const navigate = useNavigate(); // ¡ELIMINA ESTA LÍNEA! useNavigate NO va aquí.

  // Efecto para cargar el estado de autenticación desde el almacenamiento local al iniciar
  // Esto permite que el usuario permanezca logeado al recargar la página
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('token');

    if (storedUser && storedToken) {
      try {
        const parsedUser = JSON.parse(storedUser);
        setUser(parsedUser);
        setToken(storedToken);
        setIsLoggedIn(true); // Marca como logeado si hay datos válidos en localStorage
        console.log('AuthContext: Usuario y token restaurados desde localStorage.');
      } catch (e) {
        console.error('AuthContext: Error al parsear usuario desde localStorage:', e);
        // Si hay un error al parsear (ej. datos corruptos), limpia el almacenamiento
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        setUser(null);
        setToken(null);
        setIsLoggedIn(false);
      }
    }
  }, []); // Se ejecuta solo una vez al montar el componente

  // Función para iniciar sesión
  const login = (userData, userToken) => {
    setUser(userData);
    setToken(userToken);
    setIsLoggedIn(true); // Marca como logeado
    localStorage.setItem('user', JSON.stringify(userData)); // Guarda usuario en localStorage
    localStorage.setItem('token', userToken); // Guarda token en localStorage
    console.log('AuthContext: Login exitoso. Estado actualizado y guardado en localStorage.', userData);
  };

  // Función para cerrar sesión
  const logout = () => {
    setUser(null);
    setToken(null);
    setIsLoggedIn(false); // Marca como no logeado
    localStorage.removeItem('user'); // Elimina usuario de localStorage
    localStorage.removeItem('token'); // Elimina token de localStorage
    console.log('AuthContext: Sesión cerrada. Datos eliminados de localStorage.');
    // La redirección (navigate('/login')) debe hacerse en el componente que LLAMA a logout,
    // por ejemplo, en el Navbar o en la página de Login/Profile.
  };

  // Valor que se proporcionará a los componentes que consuman este contexto
  const authContextValue = {
    user,
    token,
    isLoggedIn, // Puedes usar isLoggedIn si lo necesitas, aunque 'user' ya indica si está logeado
    login,
    logout,
    // Si necesitas una función para actualizar solo el usuario sin cambiar el token, puedes añadirla aquí
    // Por ejemplo: updateAuthUser: (newUserData) => { setUser(newUserData); localStorage.setItem('user', JSON.stringify(newUserData)); }
  };

  return (
    <AuthContext.Provider value={authContextValue}>
      {children}
    </AuthContext.Provider>
  );
};
