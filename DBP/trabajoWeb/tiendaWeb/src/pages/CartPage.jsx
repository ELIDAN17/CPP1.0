// src/frontend/src/pages/CartPage.jsx
import React, { useState } from 'react'; 
import { useCart } from '../context/CartContext';
import { Link, useNavigate } from 'react-router-dom';

function CartPage() {
    const { cartItems, removeFromCart, updateQuantity, clearCart, calculateTotal } = useCart(); // Asegúrate de desestructurar calculateTotal
    const navigate = useNavigate(); 

    const [message, setMessage] = useState(null); 
    const [errorMessage, setErrorMessage] = useState(null); 

    const subtotal = calculateTotal();

    const handleRemoveItem = (id_producto, nombre_producto) => {
        if (window.confirm(`¿Estás seguro de que quieres eliminar "${nombre_producto}" del carrito?`)) {
            removeFromCart(id_producto);
            setMessage(`"${nombre_producto}" ha sido eliminado del carrito.`);
            setErrorMessage(null); 
        }
    };

    const handleClearCart = () => {
        if (window.confirm('¿Estás seguro de que quieres vaciar todo el carrito?')) {
            clearCart();
            setMessage('El carrito ha sido vaciado.');
            setErrorMessage(null); // Limpiar cualquier error previo
        }
    };

    const handleProceedToCheckout = () => {
        if (cartItems.length === 0) {
            setErrorMessage('Tu carrito está vacío. No puedes proceder al pago.');
            setMessage(null); 
            return;
        }
        setErrorMessage(null); 
        setMessage(null); 
        navigate('/checkout');
    };

    return (
        <div className="main-content cart-page-container">
            <h1 className="page-title">Tu Carrito de Compras</h1>
            {message && <div className="success-message-banner">{message}</div>}
            {errorMessage && <div className="error-message-banner">{errorMessage}</div>}

            {cartItems.length === 0 ? (
                <div className="text-center no-products-found">
                    <p>Tu carrito está vacío. ¡Explora nuestros productos y añade algo!</p>
                    <Link to="/" className="add-to-cart-button mt-4">Volver a la tienda</Link>
                </div>
            ) : (
                <div className="cart-content">
                    <div className="cart-items-list">
                        {cartItems.map(item => (
                            <div key={item.id_producto} className="cart-item-card">
                                <img
                                    src={item.imagen_url || 'https://via.placeholder.com/100x100'}
                                    alt={item.nombre}
                                    className="cart-item-image"
                                    onError={(e) => {
                                        e.target.onerror = null;
                                        e.target.src = 'https://via.placeholder.com/100x100?text=No+Image'; // Fallback
                                    }}
                                />
                                <div className="cart-item-details">
                                    <h3>{item.nombre}</h3>
                                    <p>Precio Unitario: ${item.precio.toFixed(2)}</p>
                                    <div className="cart-item-quantity-controls">
                                        <button onClick={() => updateQuantity(item.id_producto, item.cantidad - 1)} disabled={item.cantidad <= 1}>-</button>
                                        <span>{item.cantidad}</span>
                                        <button onClick={() => updateQuantity(item.id_producto, item.cantidad + 1)}>+</button>
                                        <button className="remove-item-button" onClick={() => handleRemoveItem(item.id_producto, item.nombre)}>Eliminar</button>
                                    </div>
                                    <p className="cart-item-subtotal">Subtotal: ${(item.precio * item.cantidad).toFixed(2)}</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="cart-summary-box">
                        <h2>Resumen del Pedido</h2>
                        <div className="summary-row">
                            <span>Subtotal:</span>
                            <span>${subtotal.toFixed(2)}</span>
                        </div>
                        <div className="summary-row total-row">
                            <h3>Total:</h3>
                            <h3>${subtotal.toFixed(2)}</h3>
                        </div>
                        
                        <div className="cart-actions-buttons">
                            <button 
                                className="clear-cart-button"
                                onClick={handleClearCart}
                                disabled={cartItems.length === 0}
                            >
                                Vaciar Carrito
                            </button>

                            <button 
                                className="proceed-to-checkout-button" 
                                onClick={handleProceedToCheckout}
                                disabled={cartItems.length === 0}
                            >
                                Proceder al Pago
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CartPage;
