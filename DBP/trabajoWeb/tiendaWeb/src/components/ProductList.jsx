import React from 'react';
import ProductCard from './ProductCard'; // Asegúrate de que la ruta sea correcta

const ProductList = ({ products }) => { // Cambiado 'productos' a 'products' para consistencia con HomePage
  if (!products || products.length === 0) {
    return <p className="main-content no-products-found">No hay productos para mostrar.</p>; // Usamos clases de CSS tradicional
  }

  return (
    // Cuadrícula principal de productos (usaremos una clase CSS tradicional para esto)
    <div className="productos-grid"> 
      {products.map(product => ( // Iteramos sobre 'products'
        // Pasamos cada 'product' al componente ProductCard
        <ProductCard 
          key={product.id_producto} // Clave única es esencial para React
          product={product} // Pasamos el objeto 'product' completo como prop
        />
      ))}
    </div>
  );
};

export default ProductList;