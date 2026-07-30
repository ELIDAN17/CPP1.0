// src/backend/controllers/paymentMethodController.js
const connection = require('../config/db'); // Tu pool de conexiones (mysql2/promise)

// Obtener todos los métodos de pago de un usuario específico
exports.getPaymentMethodsByUserId = async (req, res) => {
    const { idUsuario } = req.params;
    const authenticatedUserId = req.user?.id_usuario; // ID del usuario autenticado desde el token
    const authenticatedUserRole = req.user?.rol; // Rol del usuario autenticado

    // Autorización: Un usuario solo puede ver sus propios métodos de pago, o un administrador puede ver cualquiera.
    if (authenticatedUserRole !== 'administrador' && authenticatedUserId?.toString() !== idUsuario.toString()) {
        return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para ver estos métodos de pago.' });
    }

    try {
        const [rows] = await connection.execute('SELECT id_metodo_pago, tipo_tarjeta, ultimos_4_digitos, fecha_expiracion, nombre_titular, es_predeterminado FROM MetodoPago WHERE id_usuario = ? ORDER BY es_predeterminado DESC, fecha_creacion DESC', [idUsuario]);
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al obtener métodos de pago:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener métodos de pago.' });
    }
};

// Añadir un nuevo método de pago
exports.addPaymentMethod = async (req, res) => {
    const { tipo_tarjeta, ultimos_4_digitos, fecha_expiracion, nombre_titular, es_predeterminado } = req.body;
    const id_usuario = req.user.id_usuario; // El ID del usuario viene del token JWT

    // Validaciones básicas
    if (!tipo_tarjeta || !ultimos_4_digitos || !fecha_expiracion || !nombre_titular) {
        return res.status(400).json({ message: 'Faltan campos obligatorios para el método de pago.' });
    }
    if (ultimos_4_digitos.length !== 4 || !/^\d{4}$/.test(ultimos_4_digitos)) {
        return res.status(400).json({ message: 'Los últimos 4 dígitos deben ser exactamente 4 números.' });
    }
    // Validación básica de fecha de expiración (MM/AAAA)
    if (!/^\d{2}\/\d{4}$/.test(fecha_expiracion)) {
        return res.status(400).json({ message: 'El formato de la fecha de expiración debe ser MM/AAAA.' });
    }

    let connectionInstance;
    try {
        connectionInstance = await connection.getConnection();
        await connectionInstance.beginTransaction();

        // Si se establece como predeterminado, desmarcar todos los demás métodos de pago de este usuario
        if (es_predeterminado) {
            await connectionInstance.execute('UPDATE MetodoPago SET es_predeterminado = FALSE WHERE id_usuario = ?', [id_usuario]);
        }

        const [result] = await connectionInstance.execute(
            'INSERT INTO MetodoPago (id_usuario, tipo_tarjeta, ultimos_4_digitos, fecha_expiracion, nombre_titular, es_predeterminado) VALUES (?, ?, ?, ?, ?, ?)',
            [id_usuario, tipo_tarjeta, ultimos_4_digitos, fecha_expiracion, nombre_titular, es_predeterminado || false]
        );

        await connectionInstance.commit();
        res.status(201).json({ message: 'Método de pago añadido con éxito!', paymentMethodId: result.insertId });

    } catch (error) {
        if (connectionInstance) {
            await connectionInstance.rollback();
        }
        console.error('Error al añadir método de pago:', error);
        res.status(500).json({ message: 'Error interno del servidor al añadir método de pago.' });
    } finally {
        if (connectionInstance) {
            connectionInstance.release();
        }
    }
};

// Eliminar un método de pago
exports.deletePaymentMethod = async (req, res) => {
    const { idMetodoPago } = req.params;
    const authenticatedUserId = req.user.id_usuario;
    const authenticatedUserRole = req.user.rol;

    try {
        // Primero, verifica si el método de pago existe y si pertenece al usuario autenticado (o si es admin)
        const [methodRows] = await connection.execute('SELECT id_usuario FROM MetodoPago WHERE id_metodo_pago = ?', [idMetodoPago]);

        if (methodRows.length === 0) {
            return res.status(404).json({ message: 'Método de pago no encontrado.' });
        }

        const methodOwnerId = methodRows[0].id_usuario;

        // Autorización
        if (authenticatedUserRole !== 'administrador' && methodOwnerId.toString() !== authenticatedUserId.toString()) {
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para eliminar este método de pago.' });
        }

        const [deleteResult] = await connection.execute('DELETE FROM MetodoPago WHERE id_metodo_pago = ?', [idMetodoPago]);

        if (deleteResult.affectedRows === 0) {
            return res.status(404).json({ message: 'Método de pago no encontrado para eliminar.' });
        }

        res.status(200).json({ message: 'Método de pago eliminado con éxito.' });

    } catch (error) {
        console.error('Error al eliminar método de pago:', error);
        res.status(500).json({ message: 'Error interno del servidor al eliminar método de pago.' });
    }
};

// Establecer un método de pago como predeterminado
exports.setDefaultPaymentMethod = async (req, res) => {
    const { idMetodoPago } = req.params;
    const authenticatedUserId = req.user.id_usuario;
    const authenticatedUserRole = req.user.rol;

    let connectionInstance;
    try {
        connectionInstance = await connection.getConnection();
        await connectionInstance.beginTransaction();

        // 1. Verificar que el método de pago existe y pertenece al usuario
        const [methodRows] = await connectionInstance.execute('SELECT id_usuario FROM MetodoPago WHERE id_metodo_pago = ?', [idMetodoPago]);

        if (methodRows.length === 0) {
            await connectionInstance.rollback();
            return res.status(404).json({ message: 'Método de pago no encontrado.' });
        }

        const methodOwnerId = methodRows[0].id_usuario;

        // Autorización
        if (authenticatedUserRole !== 'administrador' && methodOwnerId.toString() !== authenticatedUserId.toString()) {
            await connectionInstance.rollback();
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para modificar este método de pago.' });
        }

        // 2. Desmarcar todos los demás métodos de pago del usuario como predeterminados
        await connectionInstance.execute('UPDATE MetodoPago SET es_predeterminado = FALSE WHERE id_usuario = ?', [methodOwnerId]);

        // 3. Marcar el método de pago seleccionado como predeterminado
        const [updateResult] = await connectionInstance.execute('UPDATE MetodoPago SET es_predeterminado = TRUE WHERE id_metodo_pago = ?', [idMetodoPago]);

        if (updateResult.affectedRows === 0) {
            await connectionInstance.rollback();
            return res.status(404).json({ message: 'Método de pago no encontrado para establecer como predeterminado.' });
        }

        await connectionInstance.commit();
        res.status(200).json({ message: 'Método de pago establecido como predeterminado con éxito.' });

    } catch (error) {
        if (connectionInstance) {
            await connectionInstance.rollback();
        }
        console.error('Error al establecer método de pago predeterminado:', error);
        res.status(500).json({ message: 'Error interno del servidor al establecer método de pago predeterminado.' });
    } finally {
        if (connectionInstance) {
            connectionInstance.release();
        }
    }
};
