// src/frontend/src/components/PrivateRoute.jsx
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // Importa tu hook de autenticación

/**
 * Componente PrivateRoute para proteger rutas basadas en la autenticación y el rol del usuario.
 *
 * @param {object} props - Propiedades del componente.
 * @param {string[]} [props.allowedRoles] - Un array de roles permitidos (ej. ['cliente', 'vendedor', 'administrador']).
 * Si no se proporciona, solo verifica si el usuario está logeado.
 */
const PrivateRoute = ({ allowedRoles }) => {
    const { user, isLoggedIn, loading } = useAuth(); // Obtiene el estado de autenticación y el usuario

    // Si todavía estamos cargando el estado de autenticación, no renderizamos nada
    // para evitar redirecciones prematuras.
    if (loading) {
        return (
            <div className="private-route-loading">
                <p>Verificando autenticación...</p>
                {/* Puedes añadir un spinner o un mensaje de carga más elaborado aquí */}
            </div>
        );
    }

    // 1. Verificar si el usuario está logeado
    if (!isLoggedIn) {
        // Si no está logeado, redirige a la página de login.
        // Se usa `replace` para que el usuario no pueda volver a la página protegida con el botón de atrás.
        return <Navigate to="/login" replace />;
    }

    // 2. Si está logeado, verificar si tiene un rol permitido (si se especificaron roles)
    if (allowedRoles && allowedRoles.length > 0) {
        // Asegurarse de que el usuario y su rol existen
        if (!user || !user.rol) {
            // Si el usuario no tiene un rol definido o el objeto user es nulo,
            // lo redirigimos al login o a una página de error/acceso denegado.
            console.warn("PrivateRoute: Usuario logeado pero sin rol definido. Redirigiendo a login.");
            return <Navigate to="/login" replace />;
        }

        // Convertir el rol del usuario a minúsculas para una comparación sin distinción de mayúsculas/minúsculas
        const userRole = user.rol.toLowerCase();

        // Verificar si el rol del usuario está en la lista de roles permitidos
        if (!allowedRoles.map(role => role.toLowerCase()).includes(userRole)) {
            // Si el rol no está permitido, redirige a una página de acceso denegado o a la home
            console.warn(`Acceso denegado: Usuario con rol '${user.rol}' intentó acceder a una ruta protegida para roles: ${allowedRoles.join(', ')}`);
            // Puedes redirigir a una página 403 (Acceso Denegado) si la tienes
            return <Navigate to="/" replace />; // Redirige a la página de inicio por defecto
        }
    }

    // Si el usuario está logeado y su rol es permitido (o no se especificaron roles),
    // renderiza el componente hijo de la ruta.
    return <Outlet />;
};

export default PrivateRoute;

