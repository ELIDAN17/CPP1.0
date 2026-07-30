// src/backend/controllers/productController.js
const connection = require('../config/db'); // Tu pool de conexiones (mysql2/promise)

// Obtener todos los productos
exports.getAllProducts = async (req, res) => {
    try {
        const [rows] = await connection.execute('SELECT * FROM Producto');
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al obtener todos los productos:', error);
        res.status(500).json({ message: 'Error interno del servidor.' });
    }
};

// Obtener productos por ID de categoría
exports.getProductsByCategory = async (req, res) => {
    const { categoryId } = req.params;

    if (!categoryId) {
        return res.status(400).json({ message: 'Se requiere un ID de categoría.' });
    }

    try {
        const [rows] = await connection.execute('SELECT * FROM Producto WHERE id_categoria = ?', [categoryId]);
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al obtener productos por categoría:', error);
        res.status(500).json({ message: 'Error interno del servidor al filtrar por categoría.' });
    }
};

// Buscar productos (búsqueda básica con LIKE para "fuzzy matching")
exports.searchProducts = async (req, res) => {
    const { query } = req.query;

    if (!query) {
        return res.status(400).json({ message: 'Se requiere un término de búsqueda.' });
    }

    const searchTerm = `%${query}%`;
    const sqlQuery = `
        SELECT * FROM Producto
        WHERE nombre LIKE ? OR descripcion LIKE ?
    `;

    try {
        const [rows] = await connection.execute(sqlQuery, [searchTerm, searchTerm]);
        res.status(200).json(rows);
    } catch (error) {
        console.error('Error al buscar productos:', error);
        res.status(500).json({ message: 'Error interno del servidor al realizar la búsqueda.' });
    }
};

// --- FUNCIONES PARA VENDEDOR ---

// Función para añadir un nuevo producto
exports.addProduct = async (req, res) => {
    const { nombre, descripcion, precio, stock, id_categoria, imagen_url } = req.body;
    // El ID del vendedor viene del token JWT, inyectado por authMiddleware en req.user
    const id_vendedor_creador = req.user.id_usuario;

    // Validaciones básicas de entrada
    if (!nombre || !precio || !stock || !id_categoria || !id_vendedor_creador) {
        return res.status(400).json({ message: 'Faltan campos obligatorios para el producto (nombre, precio, stock, categoría, id_vendedor_creador).' });
    }
    if (isNaN(precio) || parseFloat(precio) <= 0) {
        return res.status(400).json({ message: 'El precio debe ser un número positivo.' });
    }
    if (isNaN(stock) || parseInt(stock) < 0) {
        return res.status(400).json({ message: 'El stock debe ser un número entero no negativo.' });
    }

    try {
        // Inserta el nuevo producto en la tabla 'Producto'
        const [result] = await connection.execute(
            'INSERT INTO Producto (nombre, descripcion, precio, stock, id_categoria, id_vendedor_creador, imagen_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
            [nombre, descripcion, precio, stock, id_categoria, id_vendedor_creador, imagen_url || null]
        );
        res.status(201).json({ message: 'Producto añadido con éxito!', productId: result.insertId });
    } catch (error) {
        console.error('Error al añadir producto:', error);
        res.status(500).json({ message: 'Error interno del servidor al añadir el producto.' });
    }
};

// Función para obtener todos los productos de un vendedor específico
exports.getProductsBySeller = async (req, res) => {
    const { idVendedor } = req.params;
    const authenticatedUserId = req.user?.id_usuario;
    const authenticatedUserRole = req.user?.rol;

    // --- LOGS DE DEPURACIÓN EN EL SERVIDOR (Mantener temporalmente para verificar) ---
    console.log('--- Depuración getProductsBySeller ---');
    console.log('ID del vendedor solicitado (idVendedor de URL):', idVendedor);
    console.log('ID del usuario autenticado (req.user.id_usuario):', authenticatedUserId);
    console.log('Rol del usuario autenticado (req.user.rol):', authenticatedUserRole);
    // --- FIN LOGS DE DEPURACIÓN ---

    // Autorización: Permitir solo al vendedor ver sus propios productos o a un administrador
    if (authenticatedUserRole !== 'administrador' && authenticatedUserId?.toString() !== idVendedor.toString()) {
        console.warn(`Acceso denegado para usuario ${authenticatedUserId} (rol: ${authenticatedUserRole}) intentando ver productos de vendedor ${idVendedor}.`);
        return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para ver estos productos.' });
    }

    try {
        const [rows] = await connection.execute(
            'SELECT * FROM Producto WHERE id_vendedor_creador = ?',
            [idVendedor]
        );
        console.log('Productos encontrados para el vendedor:', rows.length);
        res.json(rows);
    } catch (error) {
        console.error('!!! ERROR EN getProductsBySeller (SERVER):', error);
        if (error.sqlMessage) {
            console.error('SQL Error Message:', error.sqlMessage);
        }
        res.status(500).json({ message: 'Error interno del servidor al obtener productos del vendedor.' });
    }
};

// Función para actualizar un producto existente
exports.updateProduct = async (req, res) => {
    const { id_producto } = req.params; // ID del producto a actualizar
    const { nombre, descripcion, precio, stock, id_categoria, imagen_url } = req.body;
    const authenticatedUserId = req.user.id_usuario; // ID del usuario autenticado
    const authenticatedUserRole = req.user.rol; // Rol del usuario autenticado

    // Validaciones básicas de entrada
    if (!nombre || !precio || !stock || !id_categoria) {
        return res.status(400).json({ message: 'Faltan campos obligatorios para actualizar el producto.' });
    }
    if (isNaN(precio) || parseFloat(precio) <= 0) {
        return res.status(400).json({ message: 'El precio debe ser un número positivo.' });
    }
    if (isNaN(stock) || parseInt(stock) < 0) {
        return res.status(400).json({ message: 'El stock debe ser un número entero no negativo.' });
    }

    try {
        // Primero, verifica si el producto existe y si pertenece al vendedor autenticado (o si es admin)
        const [productRows] = await connection.execute(
            'SELECT id_vendedor_creador FROM Producto WHERE id_producto = ?',
            [id_producto]
        );

        if (productRows.length === 0) {
            return res.status(404).json({ message: 'Producto no encontrado.' });
        }

        const productOwnerId = productRows[0].id_vendedor_creador;

        // Autorización: Solo el dueño del producto o un administrador puede actualizarlo
        if (authenticatedUserRole !== 'administrador' && productOwnerId.toString() !== authenticatedUserId.toString()) {
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para actualizar este producto.' });
        }

        // Si la autorización es exitosa, procede a actualizar el producto
        const [updateResult] = await connection.execute(
            'UPDATE Producto SET nombre = ?, descripcion = ?, precio = ?, stock = ?, id_categoria = ?, imagen_url = ? WHERE id_producto = ?',
            [nombre, descripcion, precio, stock, id_categoria, imagen_url || null, id_producto]
        );

        if (updateResult.affectedRows === 0) {
            // Esto podría pasar si el producto fue eliminado entre la verificación y la actualización
            return res.status(404).json({ message: 'Producto no encontrado para actualizar.' });
        }

        res.status(200).json({ message: 'Producto actualizado con éxito.' });

    } catch (error) {
        console.error('Error al actualizar producto:', error);
        res.status(500).json({ message: 'Error interno del servidor al actualizar el producto.' });
    }
};

// Función para eliminar un producto
exports.deleteProduct = async (req, res) => {
    const { id_producto } = req.params;
    const authenticatedUserId = req.user.id_usuario;
    const authenticatedUserRole = req.user.rol;

    try {
        // Primero, verifica si el producto existe y si pertenece al vendedor autenticado (o si es admin)
        const [productRows] = await connection.execute(
            'SELECT id_vendedor_creador FROM Producto WHERE id_producto = ?',
            [id_producto]
        );

        if (productRows.length === 0) {
            return res.status(404).json({ message: 'Producto no encontrado.' });
        }

        const productOwnerId = productRows[0].id_vendedor_creador;

        // Autorización: Solo el dueño del producto o un administrador puede eliminarlo
        if (authenticatedUserRole !== 'administrador' && productOwnerId.toString() !== authenticatedUserId.toString()) {
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para eliminar este producto.' });
        }

        // Si la autorización es exitosa, procede a eliminar
        const [deleteResult] = await connection.execute('DELETE FROM Producto WHERE id_producto = ?', [id_producto]);

        if (deleteResult.affectedRows === 0) {
            return res.status(404).json({ message: 'Producto no encontrado para eliminar.' });
        }

        res.status(200).json({ message: 'Producto eliminado con éxito.' });

    } catch (error) {
        console.error('Error al eliminar producto:', error);
        res.status(500).json({ message: 'Error interno del servidor al eliminar el producto.' });
    }
};
