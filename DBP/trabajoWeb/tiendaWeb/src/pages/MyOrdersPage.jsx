    // src/frontend/src/pages/MyOrdersPage.jsx
    import React from 'react';
    import { useParams } from 'react-router-dom';
    import { useAuth } from '../context/AuthContext'; // Asumiendo que necesitas el usuario logeado

    const MyOrdersPage = () => {
      const { id_usuario } = useParams(); // Para obtener el ID del usuario de la URL
      const { user } = useAuth(); // Para obtener el usuario logeado

      // Opcional: Puedes verificar si el id_usuario de la URL coincide con el usuario logeado
      // if (user && user.id_usuario !== parseInt(id_usuario)) {
      //   return <div className="text-center py-10">Acceso denegado o usuario no coincide.</div>;
      // }

      return (
        <div className="container mx-auto p-4">
          <h1 className="text-3xl font-bold mb-6 text-center">Mis Órdenes</h1>
          {user ? (
            <p className="text-lg text-center mb-4">Bienvenido, {user.nombre}. Aquí verás tus órdenes.</p>
          ) : (
            <p className="text-lg text-center mb-4">Inicia sesión para ver tus órdenes.</p>
          )}
          {/* Aquí iría la lógica para cargar y mostrar las órdenes del usuario */}
          <div className="bg-white shadow-md rounded-lg p-6">
            <p>Contenido de la página de Mis Órdenes para el usuario con ID: {id_usuario}</p>
            {/* Ejemplo: Lista de órdenes */}
            <ul className="list-disc pl-5 mt-4">
              <li>Orden #12345 - Fecha: 2025-07-24 - Total: $150.00 - Estado: Entregado</li>
              <li>Orden #12346 - Fecha: 2025-07-23 - Total: $75.50 - Estado: Enviado</li>
            </ul>
            <p className="mt-4 text-sm text-gray-600">
              (Esta es una página de ejemplo. La funcionalidad real de carga de órdenes debe implementarse aquí.)
            </p>
          </div>
        </div>
      );
    };

    export default MyOrdersPage;
    