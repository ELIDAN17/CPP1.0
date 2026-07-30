// ====== src/models/documentoModel.js ======
const db = require('../config/db');

// Registrar o actualizar el PDF físico del alumno
const subirDocumento = async (idPractica, idTipoDoc, nombreArchivo, archivoBinario) => {
    const query = `
        INSERT INTO documentos_practica (id_practica, id_tipo_doc, nombre_archivo, archivo_binario, estado_aprobacion, fecha_subida)
        VALUES ($1, $2, $3, $4, 'Pendiente', NOW())
        ON CONFLICT (id_practica, id_tipo_doc)
        DO UPDATE SET 
            nombre_archivo = $3, 
            archivo_binario = $4, 
            estado_aprobacion = 'Pendiente', 
            version = documentos_practica.version + 1, -- Incrementa la versión automáticamente si vuelve a subir
            fecha_subida = NOW()
        RETURNING id_documento, id_tipo_doc, nombre_archivo, estado_aprobacion, fecha_subida;
    `;
    const valores = [idPractica, idTipoDoc, nombreArchivo, archivoBinario];
    const resultado = await db.query(query, valores);
    return resultado.rows[0];
};

// Verificar el estado de aprobación actual
const obtenerDocumentoPorTipo = async (idPractica, idTipoDoc) => {
    const query = `
        SELECT id_documento, estado_aprobacion, version 
        FROM documentos_practica 
        WHERE id_practica = $1 AND id_tipo_doc = $2
        LIMIT 1
    `;
    const resultado = await db.query(query, [idPractica, idTipoDoc]);
    return resultado.rows[0];
};

module.exports = {
    subirDocumento,
    obtenerDocumentoPorTipo
};