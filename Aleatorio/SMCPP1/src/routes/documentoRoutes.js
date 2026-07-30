const express = require('express');
const router = express.Router();
const documentosController = require('../controllers/documentoController');
const { verificarToken } = require('../middlewares/authMiddleware');
const upload = require('../middlewares/uploadMiddleware');

// SOLO pones '/estudiante' porque '/api/documentos' ya viene heredado de server.js
router.get('/estudiante', verificarToken, documentosController.verDocumentosEstudiante);
router.post('/subir', verificarToken, upload.single('documento'), documentosController.subirDocumentoEstudiante);

module.exports = router;