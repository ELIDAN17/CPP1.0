// src/frontend/src/pages/SellerDashboardPage.jsx
import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Navigate } from 'react-router-dom'; // Importa Navigate para la redirección

const SellerDashboardPage = () => {
    const { user } = useAuth();

    // Lógica de protección de ruta:
    // Si no hay usuario logueado O el rol del usuario NO es 'vendedor',
    // redirige a la página de inicio o a donde consideres apropiado.
    if (!user || user.rol !== 'vendedor') {
        return <Navigate to="/" replace />; // Redirige a la página de inicio
    }

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-6 text-center">
                Dashboard del Vendedor {user?.nombre ? `(${user.nombre})` : ''}
            </h1>
            <p className="text-center text-lg text-gray-700">
                ¡Bienvenido al panel de control de tu tienda!
            </p>
            <div className="mt-8 p-6 bg-white rounded-lg shadow-md">
                <h2 className="text-2xl font-semibold mb-4">Funciones de Vendedor:</h2>
                <ul className="list-disc list-inside space-y-2">
                    <li>Gestionar productos (añadir, editar, eliminar)</li>
                    <li>Ver pedidos de tus productos</li>
                    <li>Ver estadísticas de ventas</li>
                    <li>Configurar tu perfil de vendedor</li>
                </ul>
                <p className="mt-4 text-gray-600">
                    (Estas funcionalidades se construirán en el futuro)
                </p>
            </div>
        </div>
    );
};

export default SellerDashboardPage;
