// src/frontend/src/components/Footer.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-800 text-gray-300 py-8 mt-auto shadow-inner">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center text-center md:text-left">
        {/* Sección de Copyright */}
        <div className="mb-4 md:mb-0">
          <p>&copy; {currentYear} MinimarketShop. Todos los derechos reservados.</p>
        </div>

        {/* Enlaces Legales y de Contacto */}
        <div className="flex flex-wrap justify-center md:justify-end space-x-4 md:space-x-6 text-sm">
          <Link to="/politica-privacidad" className="hover:text-white transition duration-300">
            Política de Privacidad
          </Link>
          <Link to="/terminos-servicio" className="hover:text-white transition duration-300">
            Términos de Servicio
          </Link>
          <Link to="/contacto" className="hover:text-white transition duration-300">
            Contacto
          </Link>
        </div>
      </div>
    </footer>
  );
};

export default Footer;