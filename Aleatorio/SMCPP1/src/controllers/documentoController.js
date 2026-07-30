const pool = require('../config/db');
const fs = require('fs');
const documentoModel = require('../models/documentoModel');

const verDocumentosEstudiante = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;

        const resEstudiante = await pool.query(
            'SELECT id_estudiante FROM estudiantes WHERE id_usuario = $1',
            [idUsuarioUUID]
        );

        if (resEstudiante.rows.length === 0) {
            return res.status(404).json({ error: 'Perfil no encontrado.' });
        }

        const idEstudiante = resEstudiante.rows[0].id_estudiante;

        // 🎯 IMPORTANTE: No cargamos 'archivo_binario' en el listado para optimizar rendimiento de red
        const queryDocs = `
            SELECT 
                d.id_documento,
                d.id_practica,
                d.id_tipo_doc,
                d.version,
                d.estado_aprobacion,
                d.comentarios_revision,
                d.fecha_subida,
                d.nombre_archivo,
                t.nombre_documento 
            FROM documentos_practica d
            INNER JOIN practicas p ON d.id_practica = p.id_practica
            INNER JOIN tipos_documento t ON d.id_tipo_doc = t.id_tipo_doc
            WHERE p.id_estudiante = $1
        `;
        const resDocs = await pool.query(queryDocs, [idEstudiante]);

        res.json(resDocs.rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

const subirDocumentoEstudiante = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;
        const { id_tipo_doc } = req.body; // El frontend enviará qué tipo de documento es (ej: 2 para Plan de Trabajo, 4 para Informe Final)

        // 1. Validar que Multer haya interceptado y guardado el archivo físico
        if (!req.file) {
            return res.status(400).json({ error: 'No se ha seleccionado ningún archivo o el formato no es PDF.' });
        }

        if (!id_tipo_doc) {
            // Eliminar archivo temporal en caso de error
            fs.unlink(req.file.path, () => { });
            return res.status(400).json({ error: 'El tipo de documento es requerido.' });
        }

        // 2. Buscar la práctica activa ('En Proceso') del estudiante mediante su UUID de usuario
        const queryPractica = `
            SELECT p.id_practica 
            FROM practicas p
            INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
            WHERE e.id_usuario = $1 AND p.estado_general = 'En Proceso'
            LIMIT 1
        `;
        const resPractica = await pool.query(queryPractica, [idUsuarioUUID]);

        if (resPractica.rows.length === 0) {
            // Eliminar archivo temporal en caso de error
            fs.unlink(req.file.path, () => { });
            return res.status(404).json({ error: 'No tienes una práctica activa para subir este documento.' });
        }

        const idPractica = resPractica.rows[0].id_practica;

        // 🎯 LECTURA BINARIA DEL ARCHIVO FÍSICO TEMPORAL
        const archivoBinario = fs.readFileSync(req.file.path);
        const nombreArchivo = req.file.originalname;

        // 3. Insertar/Actualizar el documento en la tabla 'documentos_practica' usando el Modelo unificado
        const nuevoDocumento = await documentoModel.subirDocumento(
            idPractica,
            id_tipo_doc,
            nombreArchivo,
            archivoBinario
        );

        // 🎯 ELIMINACIÓN DEL ARCHIVO TEMPORAL EN DISCO (YA ESTÁ EN LA BD COMO BYTEA)
        fs.unlink(req.file.path, (err) => {
            if (err) {
                console.error(`⚠️ Error al eliminar archivo temporal ${req.file.path}:`, err);
            }
        });

        return res.status(201).json({
            mensaje: 'Documento en formato PDF subido y registrado con éxito.',
            documento: nuevoDocumento
        });

    } catch (error) {
        console.error("❌ Error al subir documento:", error);
        if (req.file && req.file.path) {
            fs.unlink(req.file.path, () => { });
        }
        return res.status(500).json({ error: 'Error interno del servidor al procesar el archivo.' });
    }
};

module.exports = {
    verDocumentosEstudiante,
    subirDocumentoEstudiante
};