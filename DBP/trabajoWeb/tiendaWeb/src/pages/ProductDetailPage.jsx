// src/frontend/src/pages/ProductDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useCart } from '../context/CartContext'; 

function ProductDetailPage() {
    const { productId } = useParams(); 
    const navigate = useNavigate(); 
    const { addToCart } = useCart(); 

    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [quantity, setQuantity] = useState(1); 

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await axios.get(`http://localhost:3001/api/productos/${productId}`);
                setProduct(response.data);
            } catch (err) {
                console.error('Error al cargar el producto:', err);
                setError('No se pudo cargar los detalles del producto. Inténtalo de nuevo más tarde.');
            } finally {
                setLoading(false);
            }
        };

        fetchProduct();
    }, [productId]); 

    const handleAddToCart = () => {
        if (product && quantity > 0 && quantity <= product.stock) {
            addToCart({
                id_producto: product.id_producto,
                nombre: product.nombre,
                precio: product.precio,
                imagen_url: product.imagen_url,
                cantidad: quantity 
            });
            alert(`${quantity} ${product.nombre}(s) añadido(s) al carrito.`); 
            navigate('/carrito'); 
        } else if (quantity <= 0) {
            alert('La cantidad debe ser al menos 1.');
        } else if (quantity > product.stock) {
            alert(`No hay suficiente stock. Disponible: ${product.stock}`);
        }
    };

    // Manejador para cambiar la cantidad
    const handleQuantityChange = (e) => {
        const value = parseInt(e.target.value);
        if (!isNaN(value) && value >= 1) {
            setQuantity(value);
        } else if (e.target.value === '') {
            setQuantity('');
        }
    };
    if (loading) {
        return (
            <div className="product-detail-container loading-state">
                <p className="loading-message">Cargando detalles del producto...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="product-detail-container error-state">
                <p className="error-message">Error: {error}</p>
                <Link to="/" className="main-button back-button">Volver a la tienda</Link>
            </div>
        );
    }

    if (!product) {
        return (
            <div className="product-detail-container no-data-state">
                <p className="info-message">Producto no encontrado.</p>
                <Link to="/" className="main-button back-button">Volver a la tienda</Link>
            </div>
        );
    }

    return (
        <div className="product-detail-container">
            <div className="product-detail-card">
                <div className="product-image-section">
                    <img
                        src={product.imagen_url || `https://placehold.co/400x400/000000/FFFFFF?text=${encodeURIComponent(product.nombre)}`}
                        alt={product.nombre}
                        className="product-detail-image"
                        onError={(e) => {
                            e.target.onerror = null; // Evita bucles infinitos
                            e.target.src = `https://placehold.co/400x400/cccccc/333333?text=Imagen+No+Disp.`;
                        }}
                    />
                </div>
                <div className="product-info-section">
                    <h1 className="product-title">{product.nombre}</h1>
                    <p className="product-price">${parseFloat(product.precio).toFixed(2)}</p>
                    <p className="product-description">{product.descripcion || 'Sin descripción disponible.'}</p>
                    <p className="product-stock">
                        Stock Disponible: {product.stock > 0 ? product.stock : <span className="text-red-500">Agotado</span>}
                    </p>

                    {product.stock > 0 && (
                        <div className="add-to-cart-controls">
                            <label htmlFor="quantity" className="quantity-label">Cantidad:</label>
                            <input
                                type="number"
                                id="quantity"
                                value={quantity}
                                onChange={handleQuantityChange}
                                min="1"
                                max={product.stock}
                                className="quantity-input"
                            />
                            <button
                                onClick={handleAddToCart}
                                className="add-to-cart-button"
                                disabled={quantity <= 0 || quantity > product.stock}
                            >
                                Añadir al Carrito
                            </button>
                        </div>
                    )}

                    {product.stock === 0 && (
                        <p className="out-of-stock-message">Este producto está agotado.</p>
                    )}

                    <Link to="/" className="back-to-home-link">
                        &larr; Volver a la Tienda
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default ProductDetailPage;
