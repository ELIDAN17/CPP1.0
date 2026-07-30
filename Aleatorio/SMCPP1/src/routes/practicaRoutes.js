const express = require('express');
const router = express.Router();
const practicaController = require('../controllers/practicaController');
const { verificarToken } = require('../middlewares/authMiddleware');

// Registrar una práctica (Ruta protegida por Token JWT)
router.post('/registrar', verificarToken, practicaController.registrarNuevaPractica);

// 🎯 Registrar Dictamen / Evaluación de Práctica (Ruta protegida para Coordinador/Admin)
router.put('/:id_practica/dictaminar', verificarToken, practicaController.dictaminarPractica);

module.exports = router;