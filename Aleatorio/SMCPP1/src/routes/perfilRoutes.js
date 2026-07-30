const express = require('express');
const router = express.Router();
const { verificarToken } = require('../middlewares/authMiddleware');

// Ruta protegida: Retorna los datos que viajan ocultos dentro del Token JWT
router.get('/mi-perfil', verificarToken, (req, res) => {
    res.json({
        mensaje: "Acceso autorizado al perfil privado del SMCPP",
        datosToken: req.usuario // Aquí vienen idUsuario e idRol decodificados de manera segura
    });
});

module.exports = router;