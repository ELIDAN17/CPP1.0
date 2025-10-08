// backend-api/routes/authRoutes.js
const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController'); // Importa tu controlador de autenticación

// Rutas para autenticación (login, register)
router.post('/register', authController.registerUser);
router.post('/login', authController.loginUser);

module.exports = router;