// backend-api/routes/orderRoutes.js
const express = require('express');
const router = express.Router();
// Importamos las funciones específicas del controlador de órdenes
const { 
    createPurchase, 
    getOrderDetailsById, 
    getOrdersByUserId, 
    getOrdersForSeller 
} = require('../controllers/orderController');
// Importamos authMiddleware y authorizeRoles desestructurando el objeto
const { authMiddleware, authorizeRoles } = require('../middleware/authMiddleware'); 

// Ruta para crear una nueva compra (protegida por autenticación)
// POST /api/ordenes
router.post('/', authMiddleware, createPurchase);

// Ruta para obtener los detalles de una orden específica por su ID (protegida por autenticación)
// GET /api/ordenes/:orderId
router.get('/:orderId', authMiddleware, getOrderDetailsById);

// Ruta para obtener órdenes que contienen productos de un vendedor específico (protegida por autenticación y autorización)
// GET /api/ordenes/vendedor/:idVendedor
router.get('/vendedor/:idVendedor', authMiddleware, authorizeRoles('vendedor', 'administrador'), getOrdersForSeller);

// Ruta para obtener órdenes de un usuario específico (protegida por autenticación y autorización)
// GET /api/ordenes/usuario/:idUsuario
router.get('/usuario/:idUsuario', authMiddleware, getOrdersByUserId);

module.exports = router;
