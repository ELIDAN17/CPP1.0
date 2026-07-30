// ARCHIVO: backend/routes/tutorRoutes.js
const express = require('express');
const router = express.Router();
const tutorController = require('../controllers/tutorController');
const { verificarToken } = require('../middlewares/authMiddleware');

// Middleware para restringir accesos exclusivamente a tutores y coordinadores
const verificarRolTutor = (req, res, next) => {
    const idRol = req.usuario.idRol || req.usuario.id_rol;
    // Rol 4: Tutor, Rol 1: Administrador
    if (Number(idRol) !== 4 && Number(idRol) !== 1) {
        return res.status(403).json({ error: "Acceso denegado: Se requiere rol de Tutor Externo." });
    }
    next();
};

// 1. Obtener los alumnos asignados al tutor logueado
router.get('/estudiantes', verificarToken, verificarRolTutor, tutorController.obtenerEstudiantesAsignados);

// 2. Obtener la bitácora de un alumno específico
router.get('/estudiante/:id_practica/bitacora', verificarToken, verificarRolTutor, tutorController.obtenerBitacoraEstudiante);

// 3. Evaluar una actividad de la bitácora (Aprobar u Observar)
router.put('/bitacora/validar/:id_actividad', verificarToken, verificarRolTutor, tutorController.validarActividadBitacora);

module.exports = router;