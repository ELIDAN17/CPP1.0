import React from 'react';
import { useCart } from '../context/CartContext';

function ProductCard({ product }) { // Cambiado 'producto' a 'product' para consistencia
    const { addToCart } = useCart();

    const handleAddToCart = () => { // Nombre correcto de la función
        console.log("Añadiendo producto al carrito:", product);
        addToCart(product); // Pasamos el producto completo
        // Opcional: mostrar una notificación
        alert(`${product.nombre} añadido al carrito!`);
    };

    return (
        <div className="producto-card">
            {/* Usamos product.imagen_url (lo que viene del backend) */}
            <img src={product.imagen_url || 'https://via.placeholder.com/300x200'} alt={product.nombre} className="producto-imagen" />
            
            <div className="producto-info"> {/* Añadimos un div para el contenido si quieres separarlo visualmente */}
                <h3 className="producto-nombre">{product.nombre}</h3>
                <p className="producto-descripcion">{product.descripcion}</p>
                {/* Aseguramos que el precio sea un número y tenga 2 decimales */}
                <p className="producto-precio">${parseFloat(product.precio).toFixed(2)}</p>
                <p className="producto-stock">Stock: {product.stock}</p>
                {/* Corregido el onClick al nombre de función correcto */}
                <button className="add-to-cart-button" onClick={handleAddToCart}>Añadir al Carrito</button>
            </div>
        </div>
    );
}

export default ProductCard;