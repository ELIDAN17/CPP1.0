// src/frontend/src/pages/RegisterPage.jsx
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'; 
import axios from 'axios'; 
import { useAuth } from '../context/AuthContext'; 

function RegisterPage() {
    const [formData, setFormData] = useState({
        nombre: '',
        apellido: '',
        correo: '',
        contraseña: '',
        confirmarContraseña: '',
        telefono: '',
        rol: 'cliente', 
    });
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null); 
    const [loading, setLoading] = useState(false); 

    const navigate = useNavigate();
    const { login } = useAuth(); 

    const handleChange = (e) => {
        const { id, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [id]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccessMessage(null);
        setLoading(true); 

        if (formData.contraseña !== formData.confirmarContraseña) {
            setError('Las contraseñas no coinciden.');
            setLoading(false); 
            return;
        }

        try {
            const { confirmarContraseña, ...dataToSend } = formData;
            const response = await axios.post('http://localhost:3001/api/auth/register', dataToSend);
            if (response.data.token && response.data.user) {
                login(response.data.user, response.data.token);
                setSuccessMessage(response.data.message || 'Registro exitoso. ¡Iniciando sesión automáticamente!');
                console.log('Usuario registrado y logueado automáticamente:', response.data.user);
                
                navigate('/profile');
            } else {
                setSuccessMessage(response.data.message || 'Registro exitoso. Por favor, inicia sesión.');
                navigate('/login'); 
            }
        } catch (err) {
            console.error('Error durante el registro:', err);
            setError(err.response?.data?.message || 'Error en el registro. Inténtalo de nuevo.');
        } finally {
            setLoading(false); 
        }
    };

    return (
        <div className="auth-container">
            <h2>Registrarse</h2>
            <form onSubmit={handleSubmit} className="auth-form">
                <div className="form-group">
                    <label htmlFor="nombre">Nombre:</label>
                    <input type="text" id="nombre" name="nombre" value={formData.nombre} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="apellido">Apellido:</label>
                    <input type="text" id="apellido" name="apellido" value={formData.apellido} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="correo">Correo Electrónico:</label>
                    <input type="email" id="correo" name="correo" value={formData.correo} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="contraseña">Contraseña:</label>
                    <input type="password" id="contraseña" name="contraseña" value={formData.contraseña} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="confirmarContraseña">Confirmar Contraseña:</label>
                    <input type="password" id="confirmarContraseña" name="confirmarContraseña" value={formData.confirmarContraseña} onChange={handleChange} required />
                </div>
                <div className="form-group">
                    <label htmlFor="telefono">Teléfono (Opcional):</label>
                    <input type="text" id="telefono" name="telefono" value={formData.telefono} onChange={handleChange} />
                </div>
                
                {/* Rol */}
                <div className="form-group">
                    <label htmlFor="rol">Quiero registrarme como:</label>
                    <select id="rol" name="rol" value={formData.rol} onChange={handleChange}>
                        <option value="cliente">Cliente</option>
                        <option value="vendedor">Vendedor</option>
                    </select>
                </div>

                {error && <p className="error-message">{error}</p>}
                {successMessage && <p className="success-message">{successMessage}</p>}
                <button type="submit" className="auth-button" disabled={loading}>
                    {loading ? 'Registrando...' : 'Registrarse'}
                </button>
            </form>
            <p className="login-link">
                ¿Ya tienes una cuenta? <Link to="/login">Inicia Sesión</Link>
            </p>
        </div>
    );
}

export default RegisterPage;