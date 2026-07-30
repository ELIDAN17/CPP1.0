const express = require('express');
const router = express.Router();
const categoryController = require('../controllers/categoryController'); // Importa el controlador de categorías

// Ruta para obtener todas las categorías
// GET /api/categorias/
router.get('/', categoryController.getAllCategories);

module.exports = router; // ¡CRÍTICO: Exportar el router!