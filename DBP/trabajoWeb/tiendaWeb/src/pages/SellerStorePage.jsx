// src/frontend/src/pages/SellerDashboardPage.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; // Para obtener el usuario y token del vendedor

const SellerDashboardPage = () => {
    const { user, token, logout } = useAuth();
    const idVendedor = user?.id_usuario;

    // Estados para los datos del formulario de nuevo producto
    const [datosProducto, setDatosProducto] = useState({
        nombre: '',
        descripcion: '',
        precio: '',
        stock: '',
        id_categoria: '',
        imagen_url: ''
    });
    // Estado para la lista de categorías (se cargará desde el backend)
    const [categorias, setCategorias] = useState([]);
    // Estado para las órdenes/compras de los productos del vendedor
    const [sellerOrders, setSellerOrders] = useState([]);

    // Estados para la UI (carga, errores, mensajes de éxito)
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);
    const [mensajeExito, setMensajeExito] = useState(null);
    const [enviandoProducto, setEnviandoProducto] = useState(false);

    // Efecto para cargar categorías y órdenes del vendedor al montar el componente
    useEffect(() => {
        console.log('SellerDashboardPage: useEffect iniciado.');
        console.log('SellerDashboardPage: user:', user);
        console.log('SellerDashboardPage: token:', token ? 'presente' : 'ausente');
        console.log('SellerDashboardPage: idVendedor:', idVendedor);

        if (!idVendedor || !token) {
            console.log('SellerDashboardPage: No idVendedor o token. Estableciendo error y cargando=false.');
            setError('No autenticado. Por favor, inicia sesión como vendedor.');
            setCargando(false);
            return;
        }

        if (user.rol !== 'vendedor') {
            console.log('SellerDashboardPage: Rol no es vendedor. Estableciendo error y cargando=false.');
            setError('Acceso denegado. Debes iniciar sesión como vendedor para ver este contenido.');
            setCargando(false);
            return;
        }

        const fetchData = async () => {
            console.log('SellerDashboardPage: fetchData iniciado.');
            try {
                // 1. Cargar categorías para el formulario de añadir producto
                console.log('SellerDashboardPage: Intentando cargar categorías...');
                const categoriasRes = await axios.get('http://localhost:3001/api/categorias');
                setCategorias(categoriasRes.data);
                console.log('SellerDashboardPage: Categorías cargadas:', categoriasRes.data.length);

                // 2. Cargar órdenes/compras de los productos de este vendedor
                console.log(`SellerDashboardPage: Intentando cargar órdenes para vendedor ID: ${idVendedor}...`);
                const ordersRes = await axios.get(`http://localhost:3001/api/ordenes/vendedor/${idVendedor}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setSellerOrders(ordersRes.data);
                console.log('SellerDashboardPage: Órdenes de vendedor cargadas:', ordersRes.data.length);

            } catch (err) {
                console.error('SellerDashboardPage: Error en fetchData:', err);
                setError(err.response?.data?.message || 'Error al cargar las categorías o las órdenes.');
                if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                    console.log('SellerDashboardPage: Error 401/403 detectado, cerrando sesión.');
                    logout();
                }
            } finally {
                console.log('SellerDashboardPage: fetchData finalizado. Estableciendo cargando=false.');
                setCargando(false);
            }
        };

        fetchData();
    }, [idVendedor, token, logout, user]); // Dependencias para recargar si cambian

    // Maneja los cambios en los campos del formulario de producto
    const handleProductoChange = (e) => {
        const { name, value } = e.target;
        setDatosProducto(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    // Maneja el envío del formulario para añadir un nuevo producto
    const handleAddProductSubmit = async (e) => {
        e.preventDefault();
        setEnviandoProducto(true);
        setError(null);
        setMensajeExito(null);

        if (!datosProducto.nombre || !datosProducto.precio || !datosProducto.stock || !datosProducto.id_categoria) {
            setError('Por favor, completa todos los campos obligatorios (nombre, precio, stock, categoría).');
            setEnviandoProducto(false);
            return;
        }
        if (isNaN(datosProducto.precio) || parseFloat(datosProducto.precio) <= 0) {
            setError('El precio debe ser un número positivo.');
            setEnviandoProducto(false);
            return;
        }
        if (isNaN(datosProducto.stock) || parseInt(datosProducto.stock) < 0) {
            setError('El stock debe ser un número entero no negativo.');
            setEnviandoProducto(false);
            return;
        }

        try {
            const productoAEnviar = {
                ...datosProducto,
                precio: parseFloat(datosProducto.precio),
                stock: parseInt(datosProducto.stock),
                id_vendedor_creador: idVendedor // Asegura que se envíe el ID del vendedor creador
            };

            const response = await axios.post('http://localhost:3001/api/productos', productoAEnviar, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            setMensajeExito(response.data.message || 'Producto añadido con éxito!');
            setDatosProducto({
                nombre: '',
                descripcion: '',
                precio: '',
                stock: '',
                id_categoria: '',
                imagen_url: ''
            });

        } catch (err) {
            console.error('Error al añadir producto:', err);
            setError(err.response?.data?.message || 'Error al añadir el producto. Inténtalo de nuevo.');
            if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                logout();
            }
        } finally {
            setEnviandoProducto(false);
        }
    };

    // Renderizado condicional para estados iniciales
    if (cargando) {
        return (
            <div className="seller-dashboard-container loading-state">
                <p className="loading-message">Cargando dashboard del vendedor...</p>
            </div>
        );
    }

    if (error) { // Si hay un error, lo mostramos
        return (
            <div className="seller-dashboard-container error-state">
                <p className="error-message">Error: {error}</p>
                {(error.includes('No autenticado') || error.includes('Acceso denegado')) ? (
                    <p className="error-message">Por favor, inicia sesión como vendedor para acceder a este panel.</p>
                ) : null}
            </div>
        );
    }

    // Si no está cargando y no hay error, pero el usuario no es vendedor o no hay idVendedor
    if (!idVendedor || user.rol !== 'vendedor') {
        return (
            <div className="seller-dashboard-container not-authenticated-state">
                <p className="error-message">Acceso denegado. Debes iniciar sesión como vendedor para ver este contenido.</p>
            </div>
        );
    }

    return (
        <div className="seller-dashboard-container">
            <h1 className="page-title">Dashboard del Vendedor</h1>
            <p className="dashboard-welcome-message">Bienvenido, {user.nombre || user.email}. Aquí puedes gestionar tus productos y ventas.</p>

            {/* Mensajes de éxito o error */}
            {mensajeExito && (
                <div className="success-message-banner" role="alert">
                    {mensajeExito}
                </div>
            )}
            {error && ( // Mostrar error aquí también si no se capturó en el renderizado inicial
                <div className="error-message-banner" role="alert">
                    {error}
                </div>
            )}

            {/* Sección para Añadir Nuevo Producto */}
            <div className="add-product-section-card">
                <h2 className="section-title">Añadir Nuevo Producto</h2>
                <form onSubmit={handleAddProductSubmit} className="product-form">
                    <div className="form-group">
                        <label htmlFor="nombre">Nombre del Producto:</label>
                        <input
                            type="text"
                            id="nombre"
                            name="nombre"
                            value={datosProducto.nombre}
                            onChange={handleProductoChange}
                            required
                            className="form-input"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="descripcion">Descripción:</label>
                        <textarea
                            id="descripcion"
                            name="descripcion"
                            value={datosProducto.descripcion}
                            onChange={handleProductoChange}
                            className="form-input form-textarea"
                        ></textarea>
                    </div>
                    <div className="form-group">
                        <label htmlFor="precio">Precio:</label>
                        <input
                            type="number"
                            id="precio"
                            name="precio"
                            value={datosProducto.precio}
                            onChange={handleProductoChange}
                            required
                            min="0.01"
                            step="0.01"
                            className="form-input"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="stock">Stock:</label>
                        <input
                            type="number"
                            id="stock"
                            name="stock"
                            value={datosProducto.stock}
                            onChange={handleProductoChange}
                            required
                            min="0"
                            step="1"
                            className="form-input"
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="id_categoria">Categoría:</label>
                        <select
                            id="id_categoria"
                            name="id_categoria"
                            value={datosProducto.id_categoria}
                            onChange={handleProductoChange}
                            required
                            className="form-select"
                        >
                            <option value="">Selecciona una categoría</option>
                            {categorias.map(categoria => (
                                <option key={categoria.id_categoria} value={categoria.id_categoria}>
                                    {categoria.nombre}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="form-group">
                        <label htmlFor="imagen_url">URL de Imagen (Opcional):</label>
                        <input
                            type="text"
                            id="imagen_url"
                            name="imagen_url"
                            value={datosProducto.imagen_url}
                            onChange={handleProductoChange}
                            className="form-input"
                        />
                    </div>

                    <button
                        type="submit"
                        className="main-button"
                        disabled={enviandoProducto}
                    >
                        {enviandoProducto ? 'Añadiendo Producto...' : 'Añadir Producto'}
                    </button>
                </form>
            </div>

            {/* Sección de Compras de Clientes (Órdenes de mis productos) */}
            <div className="seller-orders-section-card">
                <h2 className="section-title">Compras de Mis Productos</h2>
                {sellerOrders.length === 0 ? (
                    <p className="no-orders-message">Aún no hay compras de tus productos.</p>
                ) : (
                    <div className="table-responsive">
                        <table className="orders-table">
                            <thead>
                                <tr>
                                    <th>ID Compra</th>
                                    <th>Fecha</th>
                                    <th>Cliente</th>
                                    <th>Producto</th>
                                    <th>Cantidad</th>
                                    <th>Subtotal</th>
                                    <th>Estado Envío</th>
                                    <th>Contacto Cliente</th>
                                </tr>
                            </thead>
                            <tbody>
                                {sellerOrders.map(order => (
                                    order.productos.map((item, index) => (
                                        <tr key={`${order.id_compra}-${item.nombre_producto}-${index}`}>
                                            <td>{order.id_compra}</td>
                                            <td>{new Date(order.fecha_compra).toLocaleDateString()}</td>
                                            <td>{order.cliente.nombre} {order.cliente.apellido}</td>
                                            <td>{item.nombre_producto}</td>
                                            <td>{item.cantidad}</td>
                                            <td>${parseFloat(item.subtotal).toFixed(2)}</td>
                                            <td>{order.estado_pedido}</td>
                                            <td>
                                                Email: {order.cliente.correo}<br />
                                                Tel: {order.cliente.telefono || 'N/A'}
                                            </td>
                                        </tr>
                                    ))
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default SellerDashboardPage;
