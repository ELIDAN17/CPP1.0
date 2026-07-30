const pool = require('../config/db');

// Obtener reportes e indicadores macro para el Decanato
const obtenerReportesMacro = async (req, res) => {
    try {
        const idRol = req.usuario.idRol || req.usuario.id_rol;

        // 🛡️ REGLA DE SEGURIDAD: Solo Decano (5) o Administrador (1)
        if (Number(idRol) !== 5 && Number(idRol) !== 1) {
            return res.status(403).json({ error: "Acceso denegado: Se requiere rol de Decano o Administrador." });
        }

        // 1. Contador de estudiantes registrados
        const resEst = await pool.query('SELECT COUNT(*)::int AS total FROM estudiantes');
        const totalEstudiantes = resEst.rows[0].total;

        // 2. Suma total de horas validadas en bitácora
        const resHrs = await pool.query("SELECT COALESCE(SUM(cantidad_horas), 0)::float AS total FROM bitacora_actividades WHERE estado_validacion = 'Aprobado'");
        const totalHorasValidadas = resHrs.rows[0].total;

        // 3. Distribución de estados generales de las prácticas
        const resDist = await pool.query(`
            SELECT 
                COALESCE(estado_general, 'Pendiente') AS estado,
                COUNT(*)::int AS cantidad 
            FROM practicas 
            GROUP BY estado_general
        `);
        const distribucionEstados = resDist.rows;

        // 4. Detalle y supervisión global de todos los procesos de prácticas
        const resPracticas = await pool.query(`
            SELECT 
                p.id_practica,
                e.codigo_estudiante,
                (e.nombres || ' ' || e.apellidos) AS estudiante,
                COALESCE(emp.razon_social, 'Sin Empresa') AS empresa,
                p.tipo_practica,
                p.horas_requeridas,
                COALESCE(p.estado_general, 'Pendiente') AS estado_general,
                COALESCE((
                    SELECT SUM(cantidad_horas) 
                    FROM bitacora_actividades 
                    WHERE id_practica = p.id_practica AND estado_validacion = 'Aprobado'
                ), 0)::float AS horas_acumuladas
            FROM practicas p
            INNER JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
            LEFT JOIN empresas emp ON p.id_empresa = emp.id_empresa
            ORDER BY p.id_practica DESC
        `);

        return res.status(200).json({
            desempeno: {
                total_estudiantes: totalEstudiantes,
                total_horas_validadas: totalHorasValidadas,
                distribucion_estados: distribucionEstados
            },
            practicas: resPracticas.rows
        });

    } catch (error) {
        console.error("❌ Error en reportes macro del Decano:", error.message);
        return res.status(500).json({ error: "Error interno del servidor al compilar las estadísticas macro." });
    }
};

module.exports = {
    obtenerReportesMacro
};
