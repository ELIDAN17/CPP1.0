// src/controllers/dashboardController.js
const pool = require('../config/db');

const obtenerMetricasEstudiante = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;

        // 1. Obtener los datos de la práctica activa y las horas requeridas
        const queryPractica = `
            SELECT p.id_practica, p.horas_requeridas, p.estado_general, p.fecha_inicio
            FROM practicas p
            INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
            WHERE e.id_usuario = $1 AND p.estado_general = 'En Proceso'
            LIMIT 1
        `;
        const resPractica = await pool.query(queryPractica, [idUsuarioUUID]);

        if (resPractica.rows.length === 0) {
            return res.status(200).json({
                tienePracticaActiva: false,
                mensaje: "No se encontró ninguna práctica activa 'En Proceso'."
            });
        }

        const { id_practica, horas_requeridas, estado_general, fecha_inicio } = resPractica.rows[0];

        // 2. Calcular total de horas aprobadas y pendientes en la bitácora
        const queryHoras = `
            SELECT 
                COALESCE(SUM(CASE WHEN estado_validacion = 'Aprobado' THEN cantidad_horas ELSE 0 END), 0) AS horas_aprobadas,
                COALESCE(SUM(CASE WHEN estado_validacion = 'Pendiente' THEN cantidad_horas ELSE 0 END), 0) AS horas_pendientes
            FROM bitacora_actividades
            WHERE id_practica = $1
        `;
        const resHoras = await pool.query(queryHoras, [id_practica]);
        const { horas_aprobadas, horas_pendientes } = resHoras.rows[0];

        // 3. Contar estado de los documentos del expediente
        const queryDocumentos = `
            SELECT 
                COUNT(*) AS total_documentos,
                COALESCE(SUM(CASE WHEN estado_aprobacion = 'Aprobado' THEN 1 ELSE 0 END), 0) AS documentos_aprobados,
                COALESCE(SUM(CASE WHEN estado_aprobacion = 'Pendiente' THEN 1 ELSE 0 END), 0) AS documentos_pendientes
            FROM documentos_practica
            WHERE id_practica = $1
        `;
        const resDocs = await pool.query(queryDocumentos, [id_practica]);
        const { total_documentos, documentos_aprobados, documentos_pendientes } = resDocs.rows[0];

        // 4. Calcular porcentajes de progreso de forma segura
        const totalHorasAbonadas = parseFloat(horas_aprobadas);
        const totalHorasRequeridas = parseInt(horas_requeridas) || 1; // Evitar división por cero
        const porcentajeHoras = Math.min(Math.round((totalHorasAbonadas / totalHorasRequeridas) * 100), 100);

        return res.status(200).json({
            tienePracticaActiva: true,
            id_practica,
            fecha_inicio,
            estado_general,
            horas_requeridas: totalHorasRequeridas,
            horas_aprobadas: totalHorasAbonadas,
            horas_pendientes: parseFloat(horas_pendientes),
            porcentaje_progreso: porcentajeHoras,
            documentos: {
                total: parseInt(total_documentos),
                aprobados: parseInt(documentos_aprobados),
                pendientes: parseInt(documentos_pendientes)
            }
        });

    } catch (error) {
        console.error("❌ Error al obtener métricas del dashboard:", error);
        return res.status(500).json({ error: 'Error interno del servidor al procesar las métricas.' });
    }
};

module.exports = {
    obtenerMetricasEstudiante
};