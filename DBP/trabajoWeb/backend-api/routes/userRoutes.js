// backend-api/routes/userRoutes.js
const express = require('express');
const router = express.Router();
// CORRECCIÓN CLAVE: Importamos las funciones específicas del controlador de usuario
// Asegúrate de que los nombres aquí coincidan con los 'exports.nombreFuncion' en userController.js
const { 
    getAllUsers, 
    getUserById, 
    updateUser, 
    deleteUser 
} = require('../controllers/userController');
// Importamos authMiddleware y authorizeRoles desestructurando el objeto
const { authMiddleware, authorizeRoles } = require('../middleware/authMiddleware'); 

// Rutas protegidas para la gestión de usuarios
// GET /api/usuarios/
// Obtener todos los usuarios (solo para administradores)
router.get('/', authMiddleware, authorizeRoles('administrador'), getAllUsers);

// GET /api/usuarios/:id
// Obtener un usuario por ID
// Cualquier usuario autenticado puede ver su propio perfil, un administrador puede ver cualquiera.
router.get('/:id', authMiddleware, getUserById); // Usamos ':id' para consistencia con otros IDs

// PUT /api/usuarios/:id
// Actualizar un usuario por ID
// Cualquier usuario autenticado puede actualizar su propio perfil.
router.put('/:id', authMiddleware, updateUser);

// DELETE /api/usuarios/:id
// Eliminar un usuario por ID (solo para administradores)
router.delete('/:id', authMiddleware, authorizeRoles('administrador'), deleteUser);

module.exports = router;
