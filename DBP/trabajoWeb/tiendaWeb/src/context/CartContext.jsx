// src/frontend/src/context/CartContext.jsx
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

const CartContext = createContext();

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};

export const CartProvider = ({ children }) => {
    const [cartItems, setCartItems] = useState(() => {
        try {
            const localData = localStorage.getItem('cartItems');
            const parsedData = localData ? JSON.parse(localData) : [];
            // Asegura que el precio sea un número al cargar desde localStorage
            return parsedData.map(item => ({
                ...item,
                precio: parseFloat(item.precio),
                cantidad: item.cantidad || 1 // Asegura que 'cantidad' exista y sea un número
            }));
        } catch (error) {
            console.error("Error al cargar el carrito de localStorage:", error);
            return [];
        }
    });

    // Guardar carrito en localStorage cada vez que cambie
    useEffect(() => {
        try {
            localStorage.setItem('cartItems', JSON.stringify(cartItems));
        } catch (error) {
            console.error("Error al guardar el carrito en localStorage:", error);
        }
    }, [cartItems]);

    // Función para añadir un ítem al carrito
    // Ahora acepta 'quantity' como parámetro
    const addToCart = (product, quantityToAdd = 1) => {
        setCartItems(prevItems => {
            const existingItemIndex = prevItems.findIndex(item => item.id_producto === product.id_producto);
            
            // Asegurarse de que el precio sea un número al añadirlo
            const numericPrice = parseFloat(product.precio);
            if (isNaN(numericPrice)) {
                console.error("Error: El precio del producto no es un número válido. Producto:", product);
                return prevItems; // No añadir el producto si el precio es inválido
            }

            if (existingItemIndex > -1) {
                // Si el producto ya existe, actualiza la cantidad
                const updatedItems = [...prevItems];
                updatedItems[existingItemIndex] = {
                    ...updatedItems[existingItemIndex],
                    cantidad: updatedItems[existingItemIndex].cantidad + quantityToAdd // Usar 'cantidad'
                };
                return updatedItems;
            } else {
                // Si es un nuevo producto, añádelo con la cantidad especificada
                return [...prevItems, { ...product, precio: numericPrice, cantidad: quantityToAdd }]; // Usar 'cantidad'
            }
        });
    };

    // Función para eliminar un ítem del carrito
    const removeFromCart = (id_producto) => {
        setCartItems(prevItems => prevItems.filter(item => item.id_producto !== id_producto));
    };

    // Función para actualizar la cantidad de un ítem
    const updateQuantity = (id_producto, newQuantity) => {
        setCartItems(prevItems => {
            if (newQuantity <= 0) {
                return prevItems.filter(item => item.id_producto !== id_producto); // Eliminar si la cantidad es 0 o menos
            }
            return prevItems.map(item =>
                item.id_producto === id_producto
                    ? { ...item, cantidad: newQuantity } // Usar 'cantidad'
                    : item
            );
        });
    };

    // Función para limpiar todo el carrito
    const clearCart = () => {
        setCartItems([]);
    };

    // Función para calcular el total del carrito
    // Usamos useCallback para memoizar la función y evitar re-creaciones innecesarias
    const calculateTotal = useCallback(() => {
        return cartItems.reduce((acc, item) => {
            // Asegurarse de que item.precio sea un número antes de la operación
            const price = parseFloat(item.precio);
            const quantity = item.cantidad; // Usar 'cantidad'
            
            if (isNaN(price) || isNaN(quantity)) {
                console.warn(`Item con id_producto ${item.id_producto} tiene precio o cantidad inválidos. Precio: ${item.precio}, Cantidad: ${item.cantidad}`);
                return acc; // Ignorar este item o manejar el error como prefieras
            }
            return acc + (price * quantity);
        }, 0);
    }, [cartItems]); // Dependencia: recalcular solo si cartItems cambia

    // El valor que se proporcionará a los consumidores del contexto
    const contextValue = {
        cartItems,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        calculateTotal // <--- ¡AHORA SÍ ESTÁ INCLUIDO!
    };

    return (
        <CartContext.Provider value={contextValue}>
            {children}
        </CartContext.Provider>
    );
};
