// src/main.jsx o src/index.jsx
import React from 'react';
import ReactDOM from 'react-dom/client'; // Importa desde 'react-dom/client' para React 18
import App from './App.jsx'; // Asegúrate que la ruta y extensión sea correcta para tu App.jsx/js
import 'bootstrap/dist/css/bootstrap.min.css'; // Asegúrate que esta línea esté presente

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);