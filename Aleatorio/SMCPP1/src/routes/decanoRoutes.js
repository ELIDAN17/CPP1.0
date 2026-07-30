const express = require('express');
const router = express.Router();
const decanoController = require('../controllers/decanoController');
const { verificarToken } = require('../middlewares/authMiddleware');

// Middleware para restringir acceso solo a Decano
const verificarRolDecano = (req, res, next) => {
    const idRol = req.usuario.idRol || req.usuario.id_rol;
    if (Number(idRol) !== 5 && Number(idRol) !== 1) {
        return res.status(403).json({ error: "Acceso denegado: Se requiere rol de Decano." });
    }
    next();
};

// Rutas de Decanato
router.get('/reportes-macro', verificarToken, verificarRolDecano, decanoController.obtenerReportesMacro);

module.exports = router;
