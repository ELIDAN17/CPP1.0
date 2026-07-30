    // src/frontend/src/App.jsx
    import React from 'react';
    import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';

    import HomePage from './pages/HomePage';
    import ProductDetailPage from './pages/ProductDetailPage';
    import CheckoutPage from './pages/CheckoutPage';
    import LoginPage from './pages/LoginPage';
    import RegisterPage from './pages/RegisterPage';
    import CartPage from './pages/CartPage';
    import ProfilePage from './pages/ProfilePage';
    import SellerDashboardPage from './pages/SellerDashboardPage';
    // import InvoicePage from './pages/InvoicePage'; // Si lo usas, descomenta
    // import SellerStorePage from './pages/SellerStorePage'; // Si lo usas, descomenta
    // import OrderConfirmationPage from './pages/OrderConfirmationPage'; // Si lo usas, descomenta
    import MyOrdersPage from './pages/MyOrdersPage';
    import PaymentMethodsPage from './pages/PaymentMethodsPage';

    import Navbar from './components/Navbar';
    import Footer from './components/Footer'; 
    import { CartProvider } from './context/CartContext';
    import { AuthProvider, useAuth } from './context/AuthContext';

    import './index.css'; 

    // --- Componente PrivateRoute ---
    const PrivateRoute = ({ allowedRoles }) => {
      const { user, loading } = useAuth();
      if (loading) {
        return <div className="text-center py-10 text-xl text-blue-600">Cargando...</div>;
      }
      if (!user) {
        return <Navigate to="/login" replace />;
      }
      if (allowedRoles && !allowedRoles.includes(user.rol)) {
        return <Navigate to="/" replace />;
      }
      return <Outlet />;
    };

    function App() {
      return (
        <Router>
          <AuthProvider>
            <CartProvider>
              <div className="min-h-screen flex flex-col bg-gray-100"> 
                <Navbar />
                <main className="flex-grow container mx-auto p-4"> 
                  <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/productos/categoria/:categoryId" element={<HomePage />} />
                    <Route path="/productos/buscar" element={<HomePage />} />
                    <Route path="/product/:id" element={<ProductDetailPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/carrito" element={<CartPage />} />
                    <Route element={<PrivateRoute allowedRoles={['cliente', 'vendedor', 'administrador']} />}>
                      <Route path="/profile" element={<ProfilePage />} />
                      <Route path="/checkout" element={<CheckoutPage />} />
                      <Route path="/metodos-pago" element={<PaymentMethodsPage />} />
                      <Route path="/mis-ordenes/:id_usuario" element={<MyOrdersPage />} />
                    </Route>
                    <Route element={<PrivateRoute allowedRoles={['vendedor', 'administrador']} />}>
                      <Route path="/dashboard-vendedor/:id" element={<SellerDashboardPage />} />
                    </Route>
                    <Route path="*" element={<h1 className="text-center text-4xl font-bold text-red-600 mt-20">404 - Página No Encontrada</h1>} />
                    <Route path="/politica-privacidad" element={<div className="bg-white p-6 rounded-lg shadow-md mt-4"><h1>Política de Privacidad</h1><p>Contenido de la política de privacidad.</p></div>} />
                    <Route path="/terminos-servicio" element={<div className="bg-white p-6 rounded-lg shadow-md mt-4"><h1>Términos de Servicio</h1><p>Contenido de los términos de servicio.</p></div>} />
                    <Route path="/contacto" element={<div className="bg-white p-6 rounded-lg shadow-md mt-4"><h1>Contacto</h1><p>Información de contacto.</p></div>} />
                  </Routes>
                </main>
                <Footer />
              </div>
            </CartProvider>
          </AuthProvider>
        </Router>
      );
    }

    export default App;
    