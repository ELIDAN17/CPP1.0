// src/controllers/reporteController.js
const pool = require('../config/db');

const obtenerDashboardEstudiante = async (req, res) => {
    try {
        const idUsuarioUUID = req.usuario.idUsuario || req.usuario.id_usuario;

        // Consulta unificada para extraer la información del alumno, su práctica activa y la empresa
        const queryPrincipal = `
            SELECT 
                e.nombres,
                e.apellidos,
                e.codigo_estudiante,
                p.id_practica,
                p.horas_requeridas,
                p.tipo_practica,
                emp.razon_social AS empresa
            FROM estudiantes e
            INNER JOIN usuarios u ON u.id_usuario = e.id_usuario
            LEFT JOIN practicas p ON e.id_estudiante = p.id_estudiante AND p.estado_general = 'En Proceso'
            LEFT JOIN empresas emp ON p.id_empresa = emp.id_empresa
            WHERE u.id_usuario = $1
            LIMIT 1
        `;
        const resPrincipal = await pool.query(queryPrincipal, [idUsuarioUUID]);

        if (resPrincipal.rows.length === 0) {
            return res.status(444).json({ error: 'No se encontraron registros para el estudiante autenticado.' });
        }

        const info = resPrincipal.rows[0];
        const idPractica = info.id_practica;

        // Valores por defecto en caso de no registrar una práctica activa aún
        let horasAcumuladas = 0;
        let totalActividades = 0;
        let documentosAprobados = 0;

        if (idPractica) {
            // 1. Sumar horas de la bitácora (puedes decidir si sumas solo aprobadas o totales según tu lógica)
            const queryHoras = `
                SELECT 
                    COALESCE(SUM(cantidad_horas), 0) AS horas_acumuladas,
                    COUNT(*) AS total_actividades
                FROM bitacora_actividades
                WHERE id_practica = $1
            `;
            const resHoras = await pool.query(queryHoras, [idPractica]);
            horasAcumuladas = resHoras.rows[0].horas_acumuladas;
            totalActividades = resHoras.rows[0].total_actividades;

            // 2. Contar cuántos entregables del expediente ya fueron aprobados
            const queryDocs = `
                SELECT COUNT(*) AS aprobados
                FROM documentos_practica
                WHERE id_practica = $1 AND estado_aprobacion = 'Aprobado'
            `;
            const resDocs = await pool.query(queryDocs, [idPractica]);
            documentosAprobados = resDocs.rows[0].aprobados;
        }

        // RETORNAMOS EL OBJETO CON LAS LLAVES EXACTAS QUE BUSCA TU FRONTEND
        return res.status(200).json({
            nombres: info.nombres,
            apellidos: info.apellidos,
            codigo_estudiante: info.codigo_estudiante,
            empresa: info.empresa || 'No Asignado',
            total_actividades: parseInt(totalActividades),
            documentos_aprobados: parseInt(documentosAprobados),
            horas_acumuladas: parseFloat(horasAcumuladas),
            horas_requeridas: parseInt(info.horas_requeridas) || 0,
            tipo_practica: info.tipo_practica || 'No Definido'
        });

    } catch (error) {
        console.error("❌ Error en el reporte del dashboard:", error);
        return res.status(500).json({ error: 'Error interno del servidor al compilar el panel de control.' });
    }
};

// RUTA DEL ARCHIVO: backend/controllers/reporteController.js

const verPanelCoordinador = async (req, res) => {
    try {
        const id_usuario_coordinador = req.usuario?.id_usuario;

        const query = `
            SELECT 
                p.id_practica,
                p.estado_general,
                p.horas_requeridas,
                p.tipo_practica,
                e.codigo_estudiante,
                (e.nombres || ' ' || e.apellidos) AS estudiante_nombre,
                emp.razon_social,
                
                -- Suma de horas aprobadas
                COALESCE((
                    SELECT SUM(ba.cantidad_horas) 
                    FROM bitacora_actividades ba 
                    WHERE ba.id_practica = p.id_practica 
                      AND ba.estado_validacion = 'Aprobado'
                ), 0) AS horas_acumuladas,
                
                -- 🎯 CORREGIDO: Retorna el endpoint de descarga con la barra / al inicio
                COALESCE((
                    SELECT '/api/documentos/descargar/' || id_documento
                    FROM documentos_practica 
                    WHERE id_practica = p.id_practica 
                      AND id_tipo_doc = 2 
                    ORDER BY id_documento DESC LIMIT 1
                ), '') AS url_plan_trabajo,
                
                -- 🎯 CORREGIDO: Retorna el endpoint de descarga con la barra / al inicio
                COALESCE((
                    SELECT '/api/documentos/descargar/' || id_documento
                    FROM documentos_practica 
                    WHERE id_practica = p.id_practica 
                      AND id_tipo_doc = 4 
                    ORDER BY id_documento DESC LIMIT 1
                ), '') AS url_informe_final,
                
                COALESCE((
                    SELECT comentarios_revision 
                    FROM documentos_practica 
                    WHERE id_practica = p.id_practica 
                      AND id_tipo_doc = 4 
                    ORDER BY id_documento DESC LIMIT 1
                ), '') AS observaciones_documento
                
            FROM practicas p
            INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
            LEFT JOIN empresas emp ON p.id_empresa = emp.id_empresa
            INNER JOIN autoridades_academicas aut ON p.id_coordinador = aut.id_autoridad
            WHERE aut.id_usuario = $1
            ORDER BY p.id_practica DESC;
        `;

        const resultado = await pool.query(query, [id_usuario_coordinador]);
        return res.json(resultado.rows);

    } catch (error) {
        console.error("❌ Error en el servidor PostgreSQL:", error.message);
        return res.status(500).json({
            error: "Error interno al procesar el panel del coordinador.",
            detalles: error.message
        });
    }
};

const descargarDocumento = async (req, res) => {
    try {
        const { id } = req.params;

        // Buscamos el archivo binario y su nombre en la BD oficial
        const query = `
            SELECT nombre_archivo, archivo_binario 
            FROM documentos_practica 
            WHERE id_documento = $1
        `;
        const resultado = await pool.query(query, [id]);

        if (resultado.rows.length === 0) {
            return res.status(404).send('Archivo no encontrado');
        }

        const { nombre_archivo, archivo_binario } = resultado.rows[0];

        // Configuramos las cabeceras para que el navegador entienda que es un archivo
        res.setHeader('Content-Type', 'application/pdf'); // Cambia si usas Word (.docx)
        res.setHeader('Content-Disposition', `inline; filename="${nombre_archivo}"`);

        // Enviamos el buffer binario directamente
        return res.send(archivo_binario);
    } catch (error) {
        console.error("❌ Error al descargar archivo:", error.message);
        return res.status(500).send('Error al descargar el archivo');
    }
};

module.exports = {
    obtenerDashboardEstudiante,
    verPanelCoordinador,
    descargarDocumento
};