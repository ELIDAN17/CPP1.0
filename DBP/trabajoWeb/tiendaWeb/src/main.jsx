import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css'; // Tu archivo CSS global
import { AuthProvider } from './context/AuthContext'; 
import { CartProvider } from './context/CartContext';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <CartProvider> {/* Envuelve App también con el proveedor del carrito */}
        <App />
      </CartProvider>
    </AuthProvider>
  </React.StrictMode>,
);