const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');

// Definimos las rutas de autenticación
router.post('/registro', authController.registrarUsuario);
router.post('/login', authController.loginUsuario);

module.exports = router;