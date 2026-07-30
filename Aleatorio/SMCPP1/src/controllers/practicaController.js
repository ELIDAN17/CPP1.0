const pool = require('../config/db');
const practicaModel = require('../models/practicaModel');

const registrarNuevaPractica = async (req, res) => {
    try {
        const { idEstudiante } = req.body;

        // Regla de negocio: Un estudiante no puede tener dos prácticas activas simultáneamente
        const practicaActiva = await practicaModel.obtenerPracticaPorEstudiante(idEstudiante);
        if (practicaActiva) {
            return res.status(400).json({
                error: 'El estudiante ya cuenta con un proceso de prácticas activo en el sistema.'
            });
        }

        // Si no tiene prácticas activas, procedemos con el registro
        const nuevaPractica = await practicaModel.crearPractica(req.body);

        res.status(201).json({
            mensaje: "Proceso de práctica preprofesional iniciado con éxito.",
            practica: nuevaPractica
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

// 🎯 CONTROLADOR PRINCIPAL: Dictaminar el estado de la práctica (Aceptado, Rechazado, En Proceso)
const dictaminarPractica = async (req, res) => {
    try {
        const { id_practica } = req.params;
        const { estado_general, observaciones } = req.body;
        const idRol = req.usuario.idRol || req.usuario.id_rol;

        // 🛡️ REGLA DE SEGURIDAD: Solo Coordinador Académico (2) o Administrador (1)
        if (Number(idRol) !== 2 && Number(idRol) !== 1) {
            return res.status(403).json({ error: "Acceso denegado: Se requiere rol de Coordinador Académico o Administrador." });
        }

        if (!estado_general) {
            return res.status(400).json({ error: "El estado del dictamen es obligatorio." });
        }

        // 1. Actualizar el estado general de la práctica
        const queryPractica = `
            UPDATE practicas 
            SET estado_general = $1 
            WHERE id_practica = $2 
            RETURNING *
        `;
        const resPractica = await pool.query(queryPractica, [estado_general, id_practica]);

        if (resPractica.rows.length === 0) {
            return res.status(404).json({ error: "No se encontró la práctica especificada para dictaminar." });
        }

        // 2. Mapear estado_general de la práctica a estado_aprobacion del documento
        let estadoAprobacionDoc = 'Pendiente';
        if (estado_general === 'Aceptado' || estado_general === 'Finalizado') {
            estadoAprobacionDoc = 'Aprobado';
        } else if (estado_general === 'Rechazado') {
            estadoAprobacionDoc = 'Rechazado';
        } else if (estado_general === 'En Proceso' && observaciones) {
            estadoAprobacionDoc = 'Observado';
        }

        // 3. Sincronizar con el último documento cargado (usualmente el Plan de Trabajo o Informe Final)
        const queryUltimoDoc = `
            SELECT id_documento 
            FROM documentos_practica 
            WHERE id_practica = $1 
            ORDER BY id_documento DESC 
            LIMIT 1
        `;
        const resDoc = await pool.query(queryUltimoDoc, [id_practica]);

        if (resDoc.rows.length > 0) {
            const id_documento = resDoc.rows[0].id_documento;
            const queryActualizarDoc = `
                UPDATE documentos_practica 
                SET estado_aprobacion = $1, comentarios_revision = $2 
                WHERE id_documento = $3 
                RETURNING id_documento, estado_aprobacion, comentarios_revision
            `;
            await pool.query(queryActualizarDoc, [estadoAprobacionDoc, observaciones || null, id_documento]);
        }

        console.log(`👨‍🏫 [COORD] Práctica #${id_practica} dictaminada como '${estado_general}'`);

        return res.status(200).json({
            mensaje: "Dictamen sobre el proceso de práctica registrado con éxito.",
            practica: resPractica.rows[0]
        });

    } catch (error) {
        console.error("❌ Error al dictaminar la práctica:", error.message);
        return res.status(500).json({ error: "Error interno del servidor al registrar el dictamen." });
    }
};

module.exports = {
    registrarNuevaPractica,
    dictaminarPractica
};