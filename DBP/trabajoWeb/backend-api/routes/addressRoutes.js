const express = require('express');
const router = express.Router();
const addressController = require('../controllers/addressController');
// const { protect } = require('../middleware/authMiddleware'); // Descomentar cuando tengas autenticación

// --- NUEVAS RUTAS PARA GESTIÓN DE DIRECCIONES ---

// Obtener todas las direcciones de un usuario por ID de usuario
// GET /api/direcciones/usuario/:id_usuario
// En producción: router.get('/usuario/:id_usuario', protect, addressController.getAddressesByUser);
router.get('/usuario/:id_usuario', addressController.getAddressesByUser);

// Añadir una nueva dirección para un usuario
// POST /api/direcciones
// En producción: router.post('/', protect, addressController.addAddress);
router.post('/', addressController.addAddress);

// Actualizar una dirección por su ID
// PUT /api/direcciones/:id_direccion
// En producción: router.put('/:id_direccion', protect, addressController.updateAddress);
router.put('/:id_direccion', addressController.updateAddress);

// Eliminar una dirección por su ID
// DELETE /api/direcciones/:id_direccion
// En producción: router.delete('/:id_direccion', protect, addressController.deleteAddress);
router.delete('/:id_direccion', addressController.deleteAddress);

// --- FIN NUEVAS RUTAS ---

module.exports = router;