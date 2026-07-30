const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const { verificarToken } = require('../middlewares/authMiddleware');

// Middleware para restringir acceso solo a Administradores
const verificarRolAdmin = (req, res, next) => {
    const idRol = req.usuario.idRol || req.usuario.id_rol;
    if (Number(idRol) !== 1) {
        return res.status(403).json({ error: "Acceso denegado: Se requiere rol de Administrador." });
    }
    next();
};

// Rutas administrativas protegidas
router.get('/usuarios', verificarToken, verificarRolAdmin, adminController.listarUsuarios);
router.post('/usuarios', verificarToken, verificarRolAdmin, adminController.crearUsuario);
router.delete('/usuarios/:id_usuario', verificarToken, verificarRolAdmin, adminController.eliminarUsuario);

module.exports = router;
