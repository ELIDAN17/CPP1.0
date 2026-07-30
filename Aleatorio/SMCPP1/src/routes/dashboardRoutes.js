// src/routes/dashboardRoutes.js
const express = require('express');
const router = express.Router();
const dashboardController = require('../controllers/dashboardController');
const { verificarToken } = require('../middlewares/authMiddleware');

// Ruta protegida para que el alumno consuma sus estadísticas
router.get('/estudiante/metricas', verificarToken, dashboardController.obtenerMetricasEstudiante);

module.exports = router;