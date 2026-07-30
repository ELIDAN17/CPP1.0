const express = require('express');
const router = express.Router();
const evaluacionController = require('../controllers/evaluacionController');
const { verificarToken } = require('../middlewares/authMiddleware');

// Ruta privada para que el tutor valide horas
router.put('/validar-bitacora', verificarToken, evaluacionController.validarActividadDiaria);

module.exports = router;