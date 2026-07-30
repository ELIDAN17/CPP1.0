const bitacoraModel = require('../models/bitacoraModel');
const practicaModel = require('../models/practicaModel');

const validarActividadDiaria = async (req, res) => {
    try {
        const { idBitacora, estado, observaciones } = req.body;

        // 1. Validar que el estado sea un valor permitido
        if (estado !== 'Aprobado' && estado !== 'Rechazado') {
            return res.status(400).json({ error: 'El estado enviado debe ser estricto: "Aprobado" o "Rechazado".' });
        }

        // 2. Actualizar el estado de la actividad en la bitácora
        const actividadActualizada = await bitacoraModel.revisarActividad(idBitacora, estado, observaciones);
        if (!actividadActualizada) {
            return res.status(404).json({ error: 'No se encontró el registro de bitácora especificado.' });
        }

        // 3. Regla de negocio: Si el tutor la aprueba, sumamos las horas a la práctica global
        let progresoPractica = null;
        if (estado === 'Aprobado') {
            progresoPractica = await practicaModel.acumularHoras(
                actividadActualizada.id_practica, 
                actividadActualizada.cantidad_horas
            );
        }

        res.json({
            mensaje: `Actividad evaluada con éxito como: ${estado}.`,
            actividad: actividadActualizada,
            progresoHoras: progresoPractica // Devuelve cuántas horas va acumulando el alumno en total
        });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

module.exports = {
    validarActividadDiaria
};