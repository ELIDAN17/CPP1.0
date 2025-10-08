import React, { useState, useEffect } from 'react';
import { useParams, useLocation } from 'react-router-dom';
import ProductList from '../components/ProductList';

function HomePage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pageTitle, setPageTitle] = useState('Nuestros Productos'); 

  const { categoryId } = useParams(); 
  const location = useLocation(); 

  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      setError(null);
      let url = 'http://localhost:3001/api/productos'; 
      let title = 'Nuestros Productos'; 

      const queryParams = new URLSearchParams(location.search);
      const searchQuery = queryParams.get('query');

      if (categoryId) {
        url = `http://localhost:3001/api/productos/categoria/${categoryId}`;
        title = `Productos de Categoría`; 
      } else if (location.pathname === '/productos/buscar' && searchQuery) {
        url = `http://localhost:3001/api/productos/buscar?query=${encodeURIComponent(searchQuery)}`;
        title = `Resultados para "${searchQuery}"`;
      } else if (location.pathname === '/') {
        url = 'http://localhost:3001/api/productos?destacados=true'; 
        title = 'Productos Destacados';
      }

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setProducts(data);
        setPageTitle(title); 
      } catch (err) {
        console.error("Error al cargar productos:", err);
        setError("Error al cargar productos. Intenta de nuevo.");
        setPageTitle("Error");
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [categoryId, location.search, location.pathname]); 

  if (loading) return <div className="main-content text-center">Cargando productos...</div>;
  if (error) return <div className="main-content error-message">{error}</div>; 
  if (products.length === 0) return <div className="main-content text-center no-products-found">No se encontraron productos.</div>; // Añadimos una clase para esto

  return (
    <div className="main-content">
      <h1 className="page-title">{pageTitle}</h1> 
      <ProductList products={products} />
    </div>
  );
}

export default HomePage;