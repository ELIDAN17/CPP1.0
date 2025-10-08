// backend-api/routes/paymentMethodRoutes.js
const express = require('express');
const router = express.Router();
const paymentMethodController = require('../controllers/paymentMethodController');
// CORRECCIÓN CLAVE: Importamos authMiddleware y authorizeRoles desestructurando el objeto
// Asegúrate de que esta línea sea EXACTAMENTE como se muestra, con las llaves { }
const { authMiddleware, authorizeRoles } = require('../middleware/authMiddleware'); 

// Ruta para obtener todos los métodos de pago de un usuario
// GET /api/metodos-pago/usuario/:idUsuario
router.get('/usuario/:idUsuario', authMiddleware, paymentMethodController.getPaymentMethodsByUserId);

// Ruta para añadir un nuevo método de pago
// POST /api/metodos-pago
router.post('/', authMiddleware, paymentMethodController.addPaymentMethod);

// Ruta para eliminar un método de pago
// DELETE /api/metodos-pago/:idMetodoPago
router.delete('/:idMetodoPago', authMiddleware, paymentMethodController.deletePaymentMethod);

// Ruta para establecer un método de pago como predeterminado
// PUT /api/metodos-pago/:idMetodoPago/predeterminado
router.put('/:idMetodoPago/predeterminado', authMiddleware, paymentMethodController.setDefaultPaymentMethod);

module.exports = router;
