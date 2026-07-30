// src/routes/notificacionRoutes.js
const express = require('express');
const router = express.Router();
const notificacionController = require('../controllers/notificacionController');
const { verificarToken } = require('../middlewares/authMiddleware');

router.get('/', verificarToken, notificacionController.obtenerNotificaciones);
router.put('/:id/leer', verificarToken, notificacionController.marcarComoLeida);

module.exports = router;