// src/middlewares/uploadMiddleware.js
const multer = require('multer');
const path = require('path');
const fs = require('fs');

// Asegurar que la carpeta de destino exista
const dir = './uploads/documentos';
if (!fs.existsSync(dir)){
    fs.mkdirSync(dir, { recursive: true });
}

// Configuración de almacenamiento
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, dir); // Los archivos se guardarán en la carpeta root /uploads/documentos
    },
    filename: (req, file, cb) => {
        // Renombrar el archivo para evitar duplicados: idUsuario-timestamp.pdf
        const idUsuario = req.usuario?.idUsuario || 'anonimo';
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, `doc-${idUsuario}-${uniqueSuffix}${path.extname(file.originalname)}`);
    }
});

// Filtro de validación estricta (Solo PDFs) según el requerimiento del proyecto
const fileFilter = (req, file, cb) => {
    if (file.mimetype === 'application/pdf') {
        cb(null, true);
    } else {
        cb(new Error('Formato no soportado. Únicamente se permiten archivos en formato PDF.'), false);
    }
};

const upload = multer({ 
    storage: storage,
    fileFilter: fileFilter,
    limits: { fileSize: 5 * 1024 * 1024 } // Límite opcional de 5MB por archivo
});

module.exports = upload;