const express = require('express');
const router = express.Router();
const bitacoraController = require('../controllers/bitacoraController');
const { verificarToken } = require('../middlewares/authMiddleware');

// SOLO pones '/estudiante' porque '/api/bitacora' ya viene heredado de server.js
router.get('/estudiante', verificarToken, bitacoraController.verBitacoraEstudiante);
router.post('/registrar', verificarToken, bitacoraController.registrarActividadDiaria);

module.exports = router;