// src/frontend/src/components/Navbar.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

function Navbar() {
    const { cartItems } = useCart();
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const [searchTerm, setSearchTerm] = useState('');
    const [categories, setCategories] = useState([]);
    const [isCategoriesDropdownOpen, setIsCategoriesDropdownOpen] = useState(false);

    const totalItemsInCart = cartItems.reduce((acc, item) => acc + (parseInt(item.cantidad) || 0), 0);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const response = await axios.get('http://localhost:3001/api/categorias');
                setCategories(response.data);
            } catch (error) {
                console.error("Error al cargar categorías en Navbar:", error);
            }
        };
        fetchCategories();
    }, []);

    const handleSearch = (e) => {
        e.preventDefault();
        if (searchTerm.trim()) {
            navigate(`/productos/buscar?query=${encodeURIComponent(searchTerm)}`);
        } else {
            navigate('/');
        }
        setSearchTerm('');
    };

    const toggleCategoriesDropdown = () => {
        setIsCategoriesDropdownOpen(!isCategoriesDropdownOpen);
    };

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (isCategoriesDropdownOpen && !event.target.closest('.categories-dropdown-container')) {
                setIsCategoriesDropdownOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isCategoriesDropdownOpen]);

    return (
        <nav className="navbar"> {/* Clase personalizada */}
            <div className="navbar-brand"> {/* Clase personalizada */}
                <Link to="/">MinimarketShop</Link>
            </div>

            <form onSubmit={handleSearch} className="search-form"> {/* Clase personalizada */}
                <input
                    type="text"
                    placeholder="Buscar productos..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <button type="submit">
                    Buscar
                </button>
            </form>

            <ul className="navbar-links"> {/* Clase personalizada */}
                <li><Link to="/">Inicio</Link></li>
                
                <li className="categories-dropdown-container"> {/* Clase personalizada */}
                    <span className="navbar-link categories-dropdown-toggle" onClick={toggleCategoriesDropdown}>Categorías ▼</span>
                    {isCategoriesDropdownOpen && (
                        <ul className="categories-dropdown-menu"> {/* Clase personalizada */}
                            {categories.map(cat => (
                                <li key={cat.id_categoria}>
                                    <Link
                                        to={`/productos/categoria/${cat.id_categoria}`}
                                        onClick={() => setIsCategoriesDropdownOpen(false)}
                                    >
                                        {cat.nombre}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    )}
                </li>

                <li>
                    <Link to="/carrito" className="navbar-link">
                        🛒 Carrito ({totalItemsInCart})
                    </Link>
                </li>

                {user ? (
                    <>
                        {user.rol === 'vendedor' && (
                            <>
                                <li>
                                    <Link to={`/dashboard-vendedor/${user.id_usuario}`} className="navbar-link">Dashboard</Link>
                                </li>
                                {/* Si tienes una página de "Mi Tienda" para el vendedor, descomenta y ajusta */}
                                {/* <li>
                                    <Link to={`/mi-tienda/${user.id_usuario}`} className="navbar-link">Mi Tienda</Link>
                                </li> */}
                            </>
                        )}
                        {user.rol === 'cliente' && (
                            <li>
                                <Link to={`/mis-ordenes/${user.id_usuario}`} className="navbar-link">Mis Órdenes</Link>
                            </li>
                        )}
                        <li>
                            <Link to="/profile" className="navbar-link">Perfil</Link>
                        </li>
                        <li>
                            <button onClick={handleLogout} className="auth-button logout"> {/* Clases personalizadas */}
                                Cerrar Sesión
                            </button>
                        </li>
                    </>
                ) : (
                    <>
                        <li>
                            <Link to="/login" className="auth-button">Login</Link> {/* Clase personalizada */}
                        </li>
                        <li>
                            <Link to="/register" className="auth-button register">Registro</Link> {/* Clase personalizada */}
                        </li>
                    </>
                )}
            </ul>
        </nav>
    );
}

export default Navbar;
