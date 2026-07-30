// src/frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function LoginPage() {
    const [datosFormulario, setDatosFormulario] = useState({
        correo: '',
        contraseña: ''
    });
    const [error, setError] = useState(null);
    const [cargando, setCargando] = useState(false);

    const navigate = useNavigate();
    const location = useLocation();
    const { login } = useAuth();
    const fromCheckout = location.state?.fromCheckout;

    const handleChange = (e) => {
        const { id, value } = e.target;
        setDatosFormulario(prevData => ({
            ...prevData,
            [id]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setCargando(true);

        try {
            const response = await axios.post('http://localhost:3001/api/auth/login', datosFormulario);
            if (response.data.token && response.data.user) {
                login(response.data.user, response.data.token);
                console.log('LoginPage: Inicio de sesión exitoso. Redirigiendo...');

                if (response.data.user.rol === 'vendedor') {
                    navigate(`/dashboard-vendedor/${response.data.user.id_usuario}`); // Ruta dinámica
                } else if (response.data.user.rol === 'administrador') {
                    navigate('/dashboard-admin');
                } else {
                    if (fromCheckout) {
                        navigate('/checkout');
                    } else {
                        navigate('/profile');
                    }
                }
            } else {
                setError('Respuesta de inicio de sesión inesperada.');
            }
        } catch (err) {
            console.error('LoginPage: Error durante el inicio de sesión:', err);
            setError(err.response?.data?.message || 'Error al iniciar sesión. Verifica tus credenciales.');
        } finally {
            setCargando(false);
        }
    };

    return (
        <div className="auth-form-container"> 
            <div className="auth-form"> 
                <h2 className="auth-title">Iniciar Sesión</h2> 
                <form onSubmit={handleSubmit}>
                    <div className="form-group"> 
                        <label htmlFor="correo">Correo Electrónico:</label>
                        <input
                            type="email"
                            id="correo"
                            name="correo"
                            value={datosFormulario.correo}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className="form-group"> 
                        <label htmlFor="contraseña">Contraseña:</label>
                        <input
                            type="password"
                            id="contraseña"
                            name="contraseña"
                            value={datosFormulario.contraseña}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    {error && <p className="message-error">{error}</p>} 
                    <button
                        type="submit"
                        className="auth-button" 
                        disabled={cargando}
                    >
                        {cargando ? 'Iniciando Sesión...' : 'Entrar'}
                    </button>

                    <p className="auth-link-text"> 
                        ¿No tienes una cuenta? <Link to="/register" className="auth-link">Regístrate aquí.</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}

export default LoginPage;
