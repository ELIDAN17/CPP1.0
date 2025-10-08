// src/frontend/src/pages/OrderConfirmationPage.jsx
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useCart } from '../context/CartContext'; 

function OrderConfirmationPage() {
    const { orderId } = useParams(); 
    const { clearCart } = useCart(); 

    const [showConfetti, setShowConfetti] = useState(false);

    useEffect(() => {
        clearCart();
        setShowConfetti(true);
        const timer = setTimeout(() => setShowConfetti(false), 5000); 
        return () => clearTimeout(timer); 
    }, [clearCart]);

    return (
        <div className="order-confirmation-container">
            {showConfetti && (
                <div className="confetti-animation">🎉 ¡Felicidades! 🎉</div>
            )}
            <h1 className="confirmation-title">¡Tu Compra ha sido Exitosa!</h1>
            <p className="confirmation-message">
                Gracias por tu pedido. Tu compra ha sido procesada correctamente.
            </p>
            {orderId && (
                <p className="order-id-display">
                    <strong>ID de Tu Orden:</strong> <span className="order-id-value">{orderId}</span>
                </p>
            )}
            <p className="next-steps-message">
                Recibirás un correo electrónico de confirmación con los detalles de tu pedido.
            </p>
            <div className="confirmation-actions">
                <Link to="/" className="main-button back-to-home-button">
                    Volver a la Tienda
                </Link>
            </div>
        </div>
    );
}

export default OrderConfirmationPage;
