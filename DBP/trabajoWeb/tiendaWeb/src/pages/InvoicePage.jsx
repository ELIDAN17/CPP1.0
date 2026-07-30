// src/frontend/src/pages/InvoicePage.jsx
import React, { useContext, useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext'; // Importa el hook useAuth para el contexto de autenticación
import { useCart } from '../context/CartContext'; // Importa el hook useCart para el contexto del carrito
import { useNavigate } from 'react-router-dom'; // Hook para la navegación programática

const InvoicePage = () => {
  const { user } = useAuth(); // Obtiene el objeto de usuario logeado del contexto de autenticación
  const { cartItems, clearCart } = useCart(); // Obtiene los ítems actuales del carrito y la función para limpiarlo
  const navigate = useNavigate(); // Inicializa el hook de navegación
  const [detallesPedido, setDetallesPedido] = useState(null); // Estado para almacenar los detalles del pedido a mostrar

  useEffect(() => {
    if (!user || !user.id || cartItems.length === 0) {
      navigate('/checkout'); // Redirige de vuelta a la página de checkout
      return; // Detiene la ejecución del efecto
    }

    const totalCalculado = cartItems.reduce((sum, item) => sum + (item.precio * item.quantity), 0);

    // Establece los detalles del pedido en el estado local
    setDetallesPedido({
      id: `ORD-${Date.now()}-${user.id}`, // ID de orden simulado, combina fecha y ID de usuario
      fecha: new Date().toLocaleDateString(), // Fecha actual del pedido
      cliente: user.nombre || user.email || `Usuario ID: ${user.id}`, // Nombre o email del cliente
      items: cartItems, // Los ítems que estaban en el carrito
      total: totalCalculado, // El monto total calculado
    });

    // Limpia el carrito después de mostrar la factura (simula una compra exitosa)
    clearCart();

  }, [user, cartItems, navigate, clearCart]); // Dependencias del useEffect para que se ejecute cuando cambien

  // Muestra un mensaje de carga mientras se preparan los detalles del pedido
  if (!detallesPedido) {
    return (
      <div className="invoice-page-container loading-state">
        <p className="loading-message">Cargando detalles de la factura...</p>
      </div>
    );
  }

  return (
    <div className="invoice-page-container"> {/* Contenedor principal de la página de factura */}
      <div className="invoice-card"> {/* Tarjeta que contiene los detalles de la factura */}
        <h2 className="invoice-title">
          ¡Pedido Realizado con Éxito!
        </h2>
        <h3 className="invoice-subtitle">
          Factura / Boleta
        </h3>

        <div className="invoice-header-info"> {/* Información del encabezado de la factura */}
          <div>
            <p><strong>Número de Pedido:</strong> <span className="info-value">{detallesPedido.id}</span></p>
            <p><strong>Fecha:</strong> <span className="info-value">{detallesPedido.fecha}</span></p>
          </div>
          <div className="invoice-customer-info">
            <p><strong>Cliente:</strong> <span className="info-value">{detallesPedido.cliente}</span></p>
            {/* Aquí podrías añadir más detalles del cliente si los tienes en el objeto user */}
          </div>
        </div>

        <div className="invoice-items-section"> {/* Sección de detalles de los ítems del pedido */}
          <h4 className="section-title">Detalles del Pedido:</h4>
          <div className="table-responsive"> {/* Contenedor para tabla responsiva */}
            <table className="invoice-table">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th className="text-center">Cantidad</th>
                  <th className="text-right">Precio Unitario</th>
                  <th className="text-right">Subtotal</th>
                </tr>
              </thead>
              <tbody>
                {detallesPedido.items.map((item) => (
                  <tr key={item.id_producto}>
                    <td>{item.nombre}</td>
                    <td className="text-center">{item.quantity}</td>
                    <td className="text-right">${item.precio.toFixed(2)}</td>
                    <td className="text-right">${(item.precio * item.quantity).toFixed(2)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="invoice-total-section"> {/* Sección del total de la factura */}
          Total: ${detallesPedido.total.toFixed(2)}
        </div>

        <div className="invoice-actions"> {/* Acciones al final de la factura */}
          <button
            onClick={() => navigate('/')}
            className="main-button"
          >
            Volver al Inicio
          </button>
        </div>
      </div>
    </div>
  );
};

export default InvoicePage;
