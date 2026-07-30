const express = require('express');
const router = express.Router();
const reporteController = require('../controllers/reporteController');
const { verificarToken } = require('../middlewares/authMiddleware');
const reporteModel = require('../models/reporteModel'); // 🎯 Unificado sin la 'o' al final

// Rutas protegidas para los paneles de control
router.get('/dashboard/estudiante', verificarToken, reporteController.obtenerDashboardEstudiante);
router.get('/panel/coordinador', verificarToken, reporteController.verPanelCoordinador);

// 🎯 CORREGIDO: Se añade 'reporteController.' antes de la función y se quita el prefijo '/api'
// Nota: La ruta queda como /documentos/descargar/:id para que no se duplique con el app.use('/api', ...)
router.get('/documentos/descargar/:id', reporteController.descargarDocumento); 

router.get('/coordinador/estadisticas', verificarToken, async (req, res) => {
    try {
        // 🎯 Usamos idUsuario que es como viene en tu payload según tu controlador
        const idUsuario = req.usuario.idUsuario || req.usuario.id_usuario;
        const idRol = req.usuario.idRol || req.usuario.id_rol;

        if (!idUsuario) {
            return res.status(400).json({ error: "No se encontró el ID de usuario en el token de sesión." });
        } 

        if (Number(idRol) !== 2) {
            return res.status(403).json({ error: "Acceso denegado: Se requiere rol de Coordinador." });
        }

        // 🎯 Corregido: Ahora coincide exactamente con la importación de arriba
        const metricas = await reporteModel.obtenerMetricasCoordinador(idUsuario);
        return res.status(200).json(metricas);

    } catch (error) {
        console.error("❌ ERROR EN ENDPOINT ESTADÍSTICAS:", error);
        return res.status(500).json({ error: error.message });
    }
});

module.exports = router;