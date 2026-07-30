// backend-api/controllers/addressController.js
const db = require('../config/db'); // Asumimos que es un pool de mysql2/promise

// Obtener todas las direcciones de un usuario
exports.getAddressesByUser = async (req, res) => {
    const { id_usuario } = req.params;

    try {
        // CAMBIO CLAVE: Eliminar 'ORDER BY es_principal DESC'
        const [rows] = await db.execute('SELECT * FROM Direccion WHERE id_usuario = ? ORDER BY id_direccion DESC', [id_usuario]);
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al obtener direcciones del usuario:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener direcciones.' });
    }
};

// Añadir una nueva dirección
exports.addAddress = async (req, res) => {
    const { id_usuario, ciudad, calle, numero, referencia } = req.body;

    if (!id_usuario || !ciudad || !calle) {
        return res.status(400).json({ message: 'ID de usuario, ciudad y calle son campos obligatorios para la dirección.' });
    }

    try {
        const [result] = await db.execute(
            'INSERT INTO Direccion (id_usuario, ciudad, calle, numero, referencia) VALUES (?, ?, ?, ?, ?)',
            [id_usuario, ciudad, calle, numero, referencia]
        );
        res.status(201).json({ message: 'Dirección añadida con éxito.', id_direccion: result.insertId });
    } catch (error) {
        console.error('Error al añadir dirección:', error);
        res.status(500).json({ message: 'Error interno del servidor al añadir dirección.' });
    }
};

// Actualizar una dirección existente
exports.updateAddress = async (req, res) => {
    const { id_direccion } = req.params;
    // CAMBIO CLAVE: Eliminar 'es_principal' de la desestructuración si no se va a usar
    const { id_usuario, ciudad, calle, numero, referencia } = req.body; 

    if (!ciudad || !calle) {
        return res.status(400).json({ message: 'Ciudad y calle son campos obligatorios para la dirección.' });
    }

    // CAMBIO CLAVE: Eliminar 'es_principal = ?' de la consulta UPDATE
    let query = 'UPDATE Direccion SET ciudad = ?, calle = ?, numero = ?, referencia = ? WHERE id_direccion = ?';
    // CAMBIO CLAVE: Eliminar 'es_principal' de queryParams
    let queryParams = [ciudad, calle, numero, referencia, id_direccion];

    try {
        const [result] = await db.execute(query, queryParams);

        if (result.affectedRows === 0) {
            return res.status(404).json({ message: 'Dirección no encontrada o no se realizaron cambios.' });
        }
        res.status(200).json({ message: 'Dirección actualizada con éxito.' });
    } catch (error) {
        console.error('Error al actualizar dirección:', error);
        res.status(500).json({ message: 'Error interno del servidor al actualizar dirección.' });
    }
};

// Eliminar una dirección
exports.deleteAddress = async (req, res) => {
    const { id_direccion } = req.params;

    try {
        const [result] = await db.execute('DELETE FROM Direccion WHERE id_direccion = ?', [id_direccion]);

        if (result.affectedRows === 0) {
            return res.status(404).json({ message: 'Dirección no encontrada.' });
        }
        res.status(200).json({ message: 'Dirección eliminada con éxito.' });
    } catch (error) {
        console.error('Error al eliminar dirección:', error);
        res.status(500).json({ message: 'Error interno del servidor al eliminar dirección.' });
    }
};