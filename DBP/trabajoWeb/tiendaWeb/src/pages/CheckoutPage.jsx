// src/frontend/src/pages/CheckoutPage.jsx
import React, { useState, useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom'; // Asegúrate de que Link esté aquí si lo usas en el JSX
import axios from 'axios';

const CheckoutPage = () => {
    // Desestructuramos calculateTotal del useCart hook
    const { cartItems, clearCart, calculateTotal } = useCart(); 
    const { user, token, logout } = useAuth();
    const navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);
    const [isProcessingOrder, setIsProcessingOrder] = useState(false);

    // Estados para direcciones y métodos de pago del usuario
    const [addresses, setAddresses] = useState([]);
    const [paymentMethods, setPaymentMethods] = useState([]);

    // Estados para la dirección y método de pago seleccionados para esta compra
    const [selectedAddressId, setSelectedAddressId] = useState('');
    const [selectedPaymentMethodId, setSelectedPaymentMethodId] = useState('');

    // Effect para cargar direcciones y métodos de pago al montar
    useEffect(() => {
        if (!user || !token) {
            // Si no hay user, redirige al login, pasando el estado para volver aquí después
            navigate('/login', { state: { fromCheckout: true } });
            return;
        }

        const fetchUserData = async () => {
            setLoading(true);
            setError(null);
            try {
                // 1. Obtener direcciones del usuario
                const addressesRes = await axios.get(`http://localhost:3001/api/direcciones/usuario/${user.id_usuario}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setAddresses(addressesRes.data);

                // Intentar precargar la dirección predeterminada
                const defaultAddress = addressesRes.data.find(addr => addr.es_predeterminado);
                if (defaultAddress) {
                    setSelectedAddressId(defaultAddress.id_direccion);
                } else if (addressesRes.data.length > 0) {
                    // Si no hay predeterminada, selecciona la primera
                    setSelectedAddressId(addressesRes.data[0].id_direccion);
                }

                // 2. Obtener métodos de pago del usuario
                const paymentMethodsRes = await axios.get(`http://localhost:3001/api/metodos-pago/usuario/${user.id_usuario}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setPaymentMethods(paymentMethodsRes.data);

                // Intentar precargar el método de pago predeterminado
                const defaultPaymentMethod = paymentMethodsRes.data.find(pm => pm.es_predeterminado);
                if (defaultPaymentMethod) {
                    setSelectedPaymentMethodId(defaultPaymentMethod.id_metodo_pago);
                } else if (paymentMethodsRes.data.length > 0) {
                    // Si no hay predeterminada, selecciona la primera
                    setSelectedPaymentMethodId(paymentMethodsRes.data[0].id_metodo_pago);
                }

            } catch (err) {
                console.error('Error al cargar datos del usuario para checkout:', err);
                setError(err.response?.data?.message || 'Error al cargar tus direcciones o métodos de pago.');
                if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                    logout(); // Cerrar sesión si el token es inválido
                }
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [user, token, logout, navigate]); // Dependencias

    // Calcular el total de la compra usando la función del contexto
    const totalCompra = calculateTotal(); // <--- ¡Esta línea usa la función correctamente!

    // Manejar la colocación de la orden
    const handlePlaceOrder = async () => {
        if (cartItems.length === 0) {
            setError('Tu carrito está vacío. Añade productos antes de proceder al pago.');
            return;
        }
        if (!selectedAddressId) {
            setError('Por favor, selecciona una dirección de envío.');
            return;
        }
        if (!selectedPaymentMethodId) {
            setError('Por favor, selecciona un método de pago.');
            return;
        }

        setIsProcessingOrder(true);
        setError(null);
        setMessage(null);

        try {
            // Obtener el objeto del método de pago seleccionado para obtener el tipo_tarjeta
            const selectedPaymentMethod = paymentMethods.find(pm => pm.id_metodo_pago === selectedPaymentMethodId);
            if (!selectedPaymentMethod) {
                throw new Error('Método de pago seleccionado no válido.');
            }

            const orderData = {
                id_usuario: user.id_usuario,
                id_direccion: selectedAddressId,
                metodo_pago: selectedPaymentMethod.tipo_tarjeta, // Usar el tipo de tarjeta como método de pago
                items: cartItems.map(item => ({
                    id_producto: item.id_producto,
                    cantidad: item.cantidad
                }))
            };

            const response = await axios.post('http://localhost:3001/api/ordenes', orderData, {
                headers: { Authorization: `Bearer ${token}` }
            });

            setMessage(response.data.message || 'Orden realizada con éxito!');
            clearCart(); // Limpiar el carrito después de la compra exitosa
            navigate(`/confirmacion-orden/${response.data.purchaseId}`); // Redirigir a la página de confirmación

        } catch (err) {
            console.error('Error al realizar la orden:', err);
            setError(err.response?.data?.message || 'Error al procesar tu orden. Inténtalo de nuevo.');
            if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                logout();
            }
        } finally {
            setIsProcessingOrder(false);
        }
    };

    if (loading) {
        return (
            <div className="checkout-page-container loading-state">
                <p className="loading-message">Cargando datos para el checkout...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="checkout-page-container error-state">
                <p className="error-message">Error: {error}</p>
                {error.includes('No autenticado') || error.includes('token inválido') || error.includes('Acceso denegado') ? (
                    <button onClick={logout} className="main-button">Volver a Iniciar Sesión</button>
                ) : null}
            </div>
        );
    }

    if (!user) {
        return (
            <div className="checkout-page-container not-authenticated-state">
                <p className="error-message">Debes iniciar sesión para proceder al pago.</p>
                <button onClick={() => navigate('/login', { state: { fromCheckout: true } })} className="main-button">Iniciar Sesión</button>
            </div>
        );
    }

    if (cartItems.length === 0) {
        return (
            <div className="checkout-page-container empty-cart-state">
                <p className="info-message">Tu carrito está vacío. No puedes proceder al checkout.</p>
                <button onClick={() => navigate('/')} className="main-button">Volver a la Tienda</button>
            </div>
        );
    }

    return (
        <div className="checkout-page-container">
            <h1 className="page-title">Finalizar Compra</h1>

            {message && (
                <div className="success-message-banner" role="alert">
                    {message}
                </div>
            )}
            {error && (
                <div className="error-message-banner" role="alert">
                    {error}
                </div>
            )}

            <div className="checkout-content-grid">
                {/* Sección de Resumen del Carrito */}
                <div className="checkout-section-card cart-summary-card">
                    <h2 className="section-title">Resumen del Pedido</h2>
                    <ul className="cart-items-list">
                        {cartItems.map(item => (
                            <li key={item.id_producto} className="cart-item-summary">
                                <span className="item-name">{item.nombre}</span>
                                <span className="item-quantity">x{item.cantidad}</span>
                                <span className="item-price">${(parseFloat(item.precio) * item.cantidad).toFixed(2)}</span>
                            </li>
                        ))}
                    </ul>
                    <div className="order-total">
                        <strong>Total:</strong> <span>${totalCompra.toFixed(2)}</span>
                    </div>
                </div>

                {/* Sección de Dirección de Envío */}
                <div className="checkout-section-card shipping-address-card">
                    <h2 className="section-title">Dirección de Envío</h2>
                    {addresses.length === 0 ? (
                        <p className="info-message">No tienes direcciones guardadas. Por favor, añádelas en tu <Link to="/profile" className="text-blue-600 hover:underline">perfil</Link>.</p>
                    ) : (
                        <div className="form-group">
                            <label htmlFor="address-select" className="form-label">Selecciona una dirección:</label>
                            <select
                                id="address-select"
                                value={selectedAddressId}
                                onChange={(e) => setSelectedAddressId(parseInt(e.target.value))}
                                className="form-select"
                            >
                                <option value="">-- Selecciona una dirección --</option>
                                {addresses.map(addr => (
                                    <option key={addr.id_direccion} value={addr.id_direccion}>
                                        {addr.calle} {addr.numero}, {addr.ciudad} {addr.es_predeterminado ? ' (Predeterminada)' : ''}
                                    </option>
                                ))}
                            </select>
                            {selectedAddressId && (
                                <div className="selected-address-details">
                                    <p><strong>Detalles:</strong></p>
                                    {addresses.find(addr => addr.id_direccion === selectedAddressId) && (
                                        <>
                                            <p>{addresses.find(addr => addr.id_direccion === selectedAddressId).calle} {addresses.find(addr => addr.id_direccion === selectedAddressId).numero}</p>
                                            <p>{addresses.find(addr => addr.id_direccion === selectedAddressId).ciudad}</p>
                                            {addresses.find(addr => addr.id_direccion === selectedAddressId).referencia && (
                                                <p>Ref: {addresses.find(addr => addr.id_direccion === selectedAddressId).referencia}</p>
                                            )}
                                        </>
                                    )}
                                </div>
                            )}
                        </div>
                    )}
                </div>

                {/* Sección de Método de Pago */}
                <div className="checkout-section-card payment-method-card">
                    <h2 className="section-title">Método de Pago</h2>
                    {paymentMethods.length === 0 ? (
                        <p className="info-message">No tienes métodos de pago guardados. Por favor, añádelos en tu <Link to="/metodos-pago" className="text-blue-600 hover:underline">perfil</Link>.</p>
                    ) : (
                        <div className="form-group">
                            <label htmlFor="payment-method-select" className="form-label">Selecciona un método de pago:</label>
                            <select
                                id="payment-method-select"
                                value={selectedPaymentMethodId}
                                onChange={(e) => setSelectedPaymentMethodId(parseInt(e.target.value))}
                                className="form-select"
                            >
                                <option value="">-- Selecciona un método --</option>
                                {paymentMethods.map(pm => (
                                    <option key={pm.id_metodo_pago} value={pm.id_metodo_pago}>
                                        {pm.tipo_tarjeta} **** {pm.ultimos_4_digitos} {pm.es_predeterminado ? ' (Predeterminado)' : ''}
                                    </option>
                                ))}
                            </select>
                            {selectedPaymentMethodId && (
                                <div className="selected-payment-details">
                                    <p><strong>Detalles:</strong></p>
                                    {paymentMethods.find(pm => pm.id_metodo_pago === selectedPaymentMethodId) && (
                                        <>
                                            <p>Tipo: {paymentMethods.find(pm => pm.id_metodo_pago === selectedPaymentMethodId).tipo_tarjeta}</p>
                                            <p>Últimos 4 dígitos: {paymentMethods.find(pm => pm.id_metodo_pago === selectedPaymentMethodId).ultimos_4_digitos}</p>
                                            <p>Titular: {paymentMethods.find(pm => pm.id_metodo_pago === selectedPaymentMethodId).nombre_titular}</p>
                                            <p>Expira: {paymentMethods.find(pm => pm.id_metodo_pago === selectedPaymentMethodId).fecha_expiracion}</p>
                                        </>
                                    )}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>

            <div className="checkout-actions">
                <button
                    onClick={handlePlaceOrder}
                    className="main-button place-order-button"
                    disabled={isProcessingOrder || cartItems.length === 0 || !selectedAddressId || !selectedPaymentMethodId}
                >
                    {isProcessingOrder ? 'Procesando Orden...' : `Pagar $${totalCompra.toFixed(2)}`}
                </button>
            </div>
        </div>
    );
};

export default CheckoutPage;
