// src/frontend/src/pages/PaymentMethodsPage.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; // Para obtener el usuario y token

const PaymentMethodsPage = () => {
    const { user, token, logout } = useAuth();
    const userId = user?.id_usuario;

    const [paymentMethods, setPaymentMethods] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);

    // Estados para el formulario de añadir método de pago
    const [showAddForm, setShowAddForm] = useState(false);
    const [formData, setFormData] = useState({
        tipo_tarjeta: '',
        ultimos_4_digitos: '',
        fecha_expiracion: '',
        nombre_titular: '',
        es_predeterminado: false
    });

    // Función para cargar los métodos de pago
    const fetchPaymentMethods = async () => {
        if (!userId || !token) {
            setError('No autenticado. Por favor, inicia sesión.');
            setLoading(false);
            return;
        }
        setLoading(true);
        setError(null);
        setMessage(null);
        try {
            const response = await axios.get(`http://localhost:3001/api/metodos-pago/usuario/${userId}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setPaymentMethods(response.data);
        } catch (err) {
            console.error('Error al cargar métodos de pago:', err);
            setError(err.response?.data?.message || 'Error al cargar métodos de pago.');
            if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                logout();
            }
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchPaymentMethods();
    }, [userId, token, logout]); // Dependencias para recargar

    // Manejador de cambios en el formulario
    const handleFormChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    // Manejador para añadir un método de pago
    const handleAddPaymentMethod = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setMessage(null);

        // Validaciones del formulario
        if (!formData.tipo_tarjeta || !formData.ultimos_4_digitos || !formData.fecha_expiracion || !formData.nombre_titular) {
            setError('Por favor, completa todos los campos obligatorios.');
            setLoading(false);
            return;
        }
        if (formData.ultimos_4_digitos.length !== 4 || !/^\d{4}$/.test(formData.ultimos_4_digitos)) {
            setError('Los últimos 4 dígitos deben ser exactamente 4 números.');
            setLoading(false);
            return;
        }
        if (!/^\d{2}\/\d{4}$/.test(formData.fecha_expiracion)) {
            setError('El formato de la fecha de expiración debe ser MM/AAAA (ej. 12/2025).');
            setLoading(false);
            return;
        }

        try {
            await axios.post('http://localhost:3001/api/metodos-pago', formData, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMessage('Método de pago añadido con éxito!');
            setShowAddForm(false); // Cerrar formulario
            setFormData({ // Limpiar formulario
                tipo_tarjeta: '', ultimos_4_digitos: '', fecha_expiracion: '', nombre_titular: '', es_predeterminado: false
            });
            fetchPaymentMethods(); // Recargar la lista
        } catch (err) {
            console.error('Error al añadir método de pago:', err);
            setError(err.response?.data?.message || 'Error al añadir el método de pago.');
        } finally {
            setLoading(false);
        }
    };

    // Manejador para eliminar un método de pago
    const handleDeletePaymentMethod = async (idMetodoPago) => {
        if (!window.confirm('¿Estás seguro de que quieres eliminar este método de pago?')) {
            return;
        }
        setLoading(true);
        setError(null);
        setMessage(null);
        try {
            await axios.delete(`http://localhost:3001/api/metodos-pago/${idMetodoPago}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMessage('Método de pago eliminado con éxito!');
            fetchPaymentMethods(); // Recargar la lista
        } catch (err) {
            console.error('Error al eliminar método de pago:', err);
            setError(err.response?.data?.message || 'Error al eliminar el método de pago.');
        } finally {
            setLoading(false);
        }
    };

    // Manejador para establecer como predeterminado
    const handleSetDefault = async (idMetodoPago) => {
        setLoading(true);
        setError(null);
        setMessage(null);
        try {
            await axios.put(`http://localhost:3001/api/metodos-pago/${idMetodoPago}/predeterminado`, {}, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMessage('Método de pago establecido como predeterminado.');
            fetchPaymentMethods(); // Recargar para ver el cambio
        } catch (err) {
            console.error('Error al establecer como predeterminado:', err);
            setError(err.response?.data?.message || 'Error al establecer como predeterminado.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="payment-methods-container loading-state">
                <p className="loading-message">Cargando métodos de pago...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="payment-methods-container error-state">
                <p className="error-message">Error: {error}</p>
                {error.includes('No autenticado') || error.includes('token inválido') || error.includes('Acceso denegado') ? (
                    <button onClick={logout} className="main-button">Volver a Iniciar Sesión</button>
                ) : null}
            </div>
        );
    }

    if (!userId) {
        return (
            <div className="payment-methods-container not-authenticated-state">
                <p className="error-message">Por favor, inicia sesión para gestionar tus métodos de pago.</p>
            </div>
        );
    }

    return (
        <div className="payment-methods-container">
            <h1 className="page-title">Mis Métodos de Pago</h1>

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

            {/* Formulario para añadir nuevo método de pago */}
            {!showAddForm ? (
                <button onClick={() => setShowAddForm(true)} className="main-button add-payment-method-button">
                    Añadir Nuevo Método de Pago
                </button>
            ) : (
                <div className="add-payment-method-card">
                    <h2 className="section-title">Añadir Nuevo Método</h2>
                    <form onSubmit={handleAddPaymentMethod} className="payment-method-form">
                        <div className="form-group">
                            <label htmlFor="tipo_tarjeta">Tipo de Tarjeta:</label>
                            <select
                                id="tipo_tarjeta"
                                name="tipo_tarjeta"
                                value={formData.tipo_tarjeta}
                                onChange={handleFormChange}
                                required
                                className="form-select"
                            >
                                <option value="">Selecciona un tipo</option>
                                <option value="Visa">Visa</option>
                                <option value="Mastercard">Mastercard</option>
                                <option value="American Express">American Express</option>
                                <option value="Discover">Discover</option>
                                {/* Puedes añadir más tipos aquí */}
                            </select>
                        </div>
                        <div className="form-group">
                            <label htmlFor="ultimos_4_digitos">Últimos 4 Dígitos:</label>
                            <input
                                type="text"
                                id="ultimos_4_digitos"
                                name="ultimos_4_digitos"
                                value={formData.ultimos_4_digitos}
                                onChange={handleFormChange}
                                maxLength="4"
                                pattern="\d{4}"
                                title="Debe contener exactamente 4 dígitos numéricos."
                                required
                                className="form-input"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="fecha_expiracion">Fecha de Expiración (MM/AAAA):</label>
                            <input
                                type="text"
                                id="fecha_expiracion"
                                name="fecha_expiracion"
                                value={formData.fecha_expiracion}
                                onChange={handleFormChange}
                                placeholder="MM/AAAA"
                                pattern="\d{2}/\d{4}"
                                title="Formato MM/AAAA (ej. 12/2025)"
                                required
                                className="form-input"
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="nombre_titular">Nombre del Titular:</label>
                            <input
                                type="text"
                                id="nombre_titular"
                                name="nombre_titular"
                                value={formData.nombre_titular}
                                onChange={handleFormChange}
                                required
                                className="form-input"
                            />
                        </div>
                        <div className="form-group form-checkbox">
                            <input
                                type="checkbox"
                                id="es_predeterminado"
                                name="es_predeterminado"
                                checked={formData.es_predeterminado}
                                onChange={handleFormChange}
                                className="form-checkbox-input"
                            />
                            <label htmlFor="es_predeterminado">Establecer como predeterminado</label>
                        </div>
                        <div className="form-actions">
                            <button type="submit" className="main-button" disabled={loading}>
                                {loading ? 'Añadiendo...' : 'Añadir Método'}
                            </button>
                            <button type="button" onClick={() => setShowAddForm(false)} className="cancel-button" disabled={loading}>
                                Cancelar
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Lista de Métodos de Pago existentes */}
            <div className="payment-methods-list-section">
                <h2 className="section-title">Tus Métodos Guardados</h2>
                {paymentMethods.length === 0 ? (
                    <p className="no-methods-message">No tienes métodos de pago guardados.</p>
                ) : (
                    <div className="payment-methods-grid">
                        {paymentMethods.map(method => (
                            <div key={method.id_metodo_pago} className={`payment-method-card ${method.es_predeterminado ? 'default-method' : ''}`}>
                                <p className="method-type">
                                    {method.tipo_tarjeta} **** {method.ultimos_4_digitos}
                                </p>
                                <p className="method-details">Titular: {method.nombre_titular}</p>
                                <p className="method-details">Expira: {method.fecha_expiracion}</p>
                                {method.es_predeterminado && <span className="default-badge">Predeterminado</span>}
                                <div className="method-actions">
                                    {!method.es_predeterminado && (
                                        <button
                                            onClick={() => handleSetDefault(method.id_metodo_pago)}
                                            className="set-default-button"
                                            disabled={loading}
                                        >
                                            Establecer Predeterminado
                                        </button>
                                    )}
                                    <button
                                        onClick={() => handleDeletePaymentMethod(method.id_metodo_pago)}
                                        className="delete-button"
                                        disabled={loading}
                                    >
                                        Eliminar
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PaymentMethodsPage;
