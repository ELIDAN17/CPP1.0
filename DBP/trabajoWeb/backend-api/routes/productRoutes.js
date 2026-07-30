const express = require('express');
const router = express.Router();
const productController = require('../controllers/productController');

// Ruta para obtener todos los productos
// GET /api/productos
router.get('/', productController.getAllProducts);

// --- NUEVAS RUTAS ---

// Ruta para obtener productos por ID de categoría
// GET /api/productos/categoria/:categoryId
router.get('/categoria/:categoryId', productController.getProductsByCategory);

// Ruta para buscar productos
// GET /api/productos/buscar?query=termino
router.get('/buscar', productController.searchProducts);

// --- FIN DE NUEVAS RUTAS ---

module.exports = router;