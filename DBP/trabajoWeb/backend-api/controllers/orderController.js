// backend-api/controllers/orderController.js
const connection = require('../config/db'); // Tu conexión a la base de datos (asumimos que es un pool de mysql2/promise)

// Función para crear una nueva compra y sus detalles
exports.createPurchase = async (req, res) => {
    // Los datos del frontend que esperamos recibir en el cuerpo de la petición (req.body)
    const {
        id_usuario,
        id_direccion,
        metodo_pago,
        items // Un array de objetos { id_producto, cantidad, precio_unitario, id_vendedor, nombre_vendedor }
    } = req.body;

    // --- Validaciones iniciales ---
    if (!id_usuario || !id_direccion || !metodo_pago || !items || items.length === 0) {
        return res.status(400).json({ message: 'Faltan datos requeridos para la compra o el carrito está vacío.' });
    }

    let connectionInstance; // Declaramos la conexión aquí para que esté disponible en el bloque 'finally'
    let purchaseId; // Variable para almacenar el ID de la compra principal

    try {
        connectionInstance = await connection.getConnection(); // Obtener una conexión del pool (¡Importante para transacciones!)
        await connectionInstance.beginTransaction(); // --- INICIAR TRANSACCIÓN ---

        // 1. VALIDAR PRODUCTOS, CALCULAR TOTAL Y VERIFICAR STOCK desde la DB
        let total_compra = 0;
        const productIds = items.map(item => item.id_producto);

        // Obtenemos los productos con sus precios y stock reales de la base de datos
        const [productsInDb] = await connectionInstance.execute(
            `SELECT id_producto, precio, stock, id_vendedor_creador, nombre_vendedor FROM Producto WHERE id_producto IN (${productIds.map(() => '?').join(',')})`,
            productIds
        );

        // Crear un mapa para acceder rápidamente a los datos de los productos por su ID
        const productDataMap = new Map(productsInDb.map(p => [
            p.id_producto,
            {
                precio: parseFloat(p.precio), // Aseguramos que sea número
                stock: p.stock,
                id_vendedor: p.id_vendedor_creador, // Asegúrate de que tu tabla Producto tenga esta columna
                nombre_vendedor: p.nombre_vendedor // Asegúrate de que tu tabla Producto tenga esta columna
            }
        ]));

        // Recorremos los ítems del carrito para calcular el total y validar el stock
        for (const item of items) {
            const productInfo = productDataMap.get(item.id_producto);

            if (!productInfo) {
                throw new Error(`Producto con ID ${item.id_producto} no encontrado en la base de datos.`);
            }
            if (item.cantidad <= 0) {
                throw new Error(`La cantidad para el producto ${item.id_producto} debe ser mayor a 0.`);
            }
            if (productInfo.stock < item.cantidad) {
                throw new Error(`Stock insuficiente para el producto ID: ${item.id_producto}. Disponible: ${productInfo.stock}, Solicitado: ${item.cantidad}.`);
            }
            
            // Verificación adicional para asegurar que el precio es un número válido
            if (isNaN(productInfo.precio)) {
                throw new Error(`El precio del producto ID ${item.id_producto} no es un número válido en la base de datos.`);
            }

            // Usamos el precio del producto de la base de datos
            total_compra += productInfo.precio * item.cantidad;
        }

        // --- CORRECCIÓN CLAVE: Verificar si total_compra es NaN antes de insertar ---
        if (isNaN(total_compra)) {
            throw new Error('El total de la compra no pudo ser calculado correctamente. Verifique los precios de los productos.');
        }

        // 2. Insertar en la tabla Compra
        // Usamos 'estado_envio' para que coincida con tu esquema de DB
        const [compraResult] = await connectionInstance.execute(
            `INSERT INTO Compra (id_usuario, id_direccion, total_compra, metodo_pago, estado_envio)
             VALUES (?, ?, ?, ?, ?)`,
            [id_usuario, id_direccion, total_compra, metodo_pago, 'pendiente'] // Estado inicial de la compra
        );
        purchaseId = compraResult.insertId; // Obtener el ID de la compra recién creada

        // 3. Insertar en la tabla DetalleCompra por cada item del carrito y actualizar stock
        for (const item of items) {
            const productInfo = productDataMap.get(item.id_producto); // Obtenemos la info ya validada
            const subtotal = productInfo.precio * item.cantidad; // Usamos el precio real de la DB

            // Asegúrate de que tu tabla DetalleCompra tenga las columnas id_vendedor y nombre_vendedor
            await connectionInstance.execute(
                `INSERT INTO DetalleCompra (id_compra, id_producto, cantidad, precio_unitario, subtotal, id_vendedor, nombre_vendedor)
                 VALUES (?, ?, ?, ?, ?, ?, ?)`,
                [
                    purchaseId,
                    item.id_producto,
                    item.cantidad,
                    productInfo.precio,
                    subtotal,
                    productInfo.id_vendedor || null, // Pasa null si es undefined
                    productInfo.nombre_vendedor || null // Pasa null si es undefined
                ]
            );

            // Actualizar el stock del producto
            await connectionInstance.execute(
                `UPDATE Producto SET stock = stock - ? WHERE id_producto = ?`,
                [item.cantidad, item.id_producto]
            );
        }

        // 4. Insertar en la tabla Historial para registrar el estado de la compra/pago
        // `NOW()` inserta la fecha y hora actual de la base de datos
        await connectionInstance.execute(
            `INSERT INTO Historial (id_usuario, id_compra, fecha_pago, estado, boleta_emitida)
             VALUES (?, ?, NOW(), ?, ?)`,
            [id_usuario, purchaseId, 'pagado', false] // Asumimos 'pagado' ya que la operación fue exitosa
        );

        await connectionInstance.commit(); // --- COMMIT TRANSACCIÓN ---

        res.status(201).json({ message: 'Compra realizada y registrada en historial con éxito!', purchaseId: purchaseId });

    } catch (error) {
        // --- ROLLBACK TRANSACCIÓN ---
        if (connectionInstance) {
            await connectionInstance.rollback(); 
        }
        console.error('Error al realizar la compra, rollback ejecutado:', error);
        // Devolver un mensaje de error más específico al frontend si es un error de validación
        const statusCode = error.message.includes('Producto con ID') || error.message.includes('Stock insuficiente') || error.message.includes('cantidad debe ser') || error.message.includes('total de la compra') || error.message.includes('precio del producto') ? 400 : 500;
        res.status(statusCode).json({ message: 'Error al procesar la compra.', error: error.message });
    } finally {
        if (connectionInstance) {
            connectionInstance.release(); // Liberar la conexión al pool
        }
    }
};

// --- FUNCIÓN: Obtener detalles de una orden específica por ID de compra ---
exports.getOrderDetailsById = async (req, res) => {
    const { orderId } = req.params;
    const authenticatedUserId = req.user?.id_usuario; // Usar optional chaining
    const authenticatedUserRole = req.user?.rol; // Usar optional chaining

    // Validar que el usuario autenticado exista
    if (!authenticatedUserId) {
        return res.status(401).json({ message: 'No autenticado. Inicie sesión para ver los detalles de la orden.' });
    }

    try {
        // Obtener los detalles de la compra principal
        const [orderRows] = await connection.execute(
            `SELECT 
                c.id_compra, 
                c.id_usuario, 
                c.fecha_compra, 
                c.total_compra, 
                c.metodo_pago, 
                c.estado_envio AS estado_pedido, -- Usar estado_envio de la DB y renombrar a estado_pedido
                d.calle, d.numero, d.ciudad, d.referencia
             FROM Compra c
             JOIN Direccion d ON c.id_direccion = d.id_direccion
             WHERE c.id_compra = ?`,
            [orderId]
        );

        if (orderRows.length === 0) {
            return res.status(404).json({ message: 'Orden no encontrada.' });
        }

        const order = orderRows[0];

        // Autorización: Solo el usuario que hizo la compra o un administrador puede ver la orden
        if (authenticatedUserRole !== 'administrador' && authenticatedUserId.toString() !== order.id_usuario.toString()) {
            return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para ver esta orden.' });
        }

        // Obtener los detalles de los productos dentro de esa compra
        const [itemRows] = await connection.execute(
            `SELECT 
                dc.id_producto, 
                p.nombre AS nombre_producto, 
                dc.cantidad, 
                dc.precio_unitario, 
                dc.subtotal,
                dc.id_vendedor,
                dc.nombre_vendedor
             FROM DetalleCompra dc
             JOIN Producto p ON dc.id_producto = p.id_producto
             WHERE dc.id_compra = ?`,
            [orderId]
        );

        // Construir el objeto de respuesta final
        const responseData = {
            id_pedido: order.id_compra,
            id_usuario: order.id_usuario,
            fecha_pedido: order.fecha_compra,
            total_pedido: parseFloat(order.total_compra),
            metodo_pago: order.metodo_pago,
            estado_pedido: order.estado_pedido, // Ya renombrado en la consulta SQL
            direccion_envio: {
                calle: order.calle,
                numero: order.numero,
                ciudad: order.ciudad,
                referencia: order.referencia || null
            },
            items: itemRows.map(item => ({
                id_producto: item.id_producto,
                nombre_producto: item.nombre_producto,
                cantidad: item.cantidad,
                precio_unitario: parseFloat(item.precio_unitario),
                subtotal: parseFloat(item.subtotal),
                id_vendedor: item.id_vendedor,
                nombre_vendedor: item.nombre_vendedor
            }))
        };

        res.json(responseData);

    } catch (error) {
        console.error('Error al obtener detalles de la orden por ID:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener detalles de la orden.', error: error.message });
    }
};


// Función para obtener órdenes por ID de usuario
exports.getOrdersByUserId = async (req, res) => {
    const { idUsuario } = req.params;
    const authenticatedUserId = req.user?.id_usuario; // Usar optional chaining
    const authenticatedUserRole = req.user?.rol; // Usar optional chaining

    // Validar que el usuario autenticado exista
    if (!authenticatedUserId) {
        return res.status(401).json({ message: 'No autenticado. Inicie sesión para ver sus órdenes.' });
    }

    if (authenticatedUserRole !== 'administrador' && authenticatedUserId.toString() !== idUsuario.toString()) {
        return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para ver estas órdenes.' });
    }

    try {
        const [rows] = await connection.execute(
            'SELECT c.*, d.calle, d.ciudad FROM Compra c JOIN Direccion d ON c.id_direccion = d.id_direccion WHERE c.id_usuario = ? ORDER BY c.fecha_compra DESC',
            [idUsuario]
        );
        res.json(rows);
    } catch (error) {
        console.error('Error al obtener órdenes por usuario:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener órdenes.' });
    }
};

// --- FUNCIÓN: Obtener órdenes que contienen productos de un vendedor específico ---
exports.getOrdersForSeller = async (req, res) => {
    const { idVendedor } = req.params;
    const authenticatedUserId = req.user?.id_usuario; // Usar optional chaining
    const authenticatedUserRole = req.user?.rol; // Usar optional chaining

    // Validar que el usuario autenticado exista
    if (!authenticatedUserId) {
        return res.status(401).json({ message: 'No autenticado. Inicie sesión para ver las órdenes de vendedor.' });
    }

    // Autorización: Solo el vendedor autenticado o un administrador puede ver estas órdenes
    if (authenticatedUserRole !== 'administrador' && authenticatedUserId.toString() !== idVendedor.toString()) {
        return res.status(403).json({ message: 'Acceso denegado. No tienes permiso para ver estas órdenes.' });
    }

    try {
        // Consulta para obtener las compras que incluyen productos de este vendedor
        const [rows] = await connection.execute(
            `SELECT
                C.id_compra,
                C.fecha_compra,
                C.total_compra,
                C.estado_envio AS estado_pedido, -- Usar estado_envio de la DB y renombrar a estado_pedido
                C.metodo_pago,
                U.nombre AS cliente_nombre,
                U.apellido AS cliente_apellido,
                U.correo AS cliente_correo,
                U.telefono AS cliente_telefono,
                P.id_producto, -- Añadido para consistencia en el frontend
                P.nombre AS producto_nombre,
                DC.cantidad,
                DC.precio_unitario,
                DC.subtotal,
                DC.id_vendedor,
                DC.nombre_vendedor
            FROM Compra C
            JOIN DetalleCompra DC ON C.id_compra = DC.id_compra
            JOIN Producto P ON DC.id_producto = P.id_producto
            JOIN Usuario U ON C.id_usuario = U.id_usuario
            WHERE P.id_vendedor_creador = ?
            ORDER BY C.fecha_compra DESC`,
            [idVendedor]
        );

        // Agrupar los resultados por compra para que sea más fácil de manejar en el frontend
        const groupedOrders = {};
        rows.forEach(row => {
            if (!groupedOrders[row.id_compra]) {
                groupedOrders[row.id_compra] = {
                    id_compra: row.id_compra,
                    fecha_compra: row.fecha_compra,
                    total_compra: parseFloat(row.total_compra),
                    estado_pedido: row.estado_pedido, // Ya renombrado en la consulta SQL
                    metodo_pago: row.metodo_pago,
                    cliente: {
                        nombre: row.cliente_nombre,
                        apellido: row.cliente_apellido,
                        correo: row.cliente_correo,
                        telefono: row.telefono
                    },
                    productos: []
                };
            }
            groupedOrders[row.id_compra].productos.push({
                id_producto: row.id_producto,
                nombre_producto: row.producto_nombre,
                cantidad: row.cantidad,
                precio_unitario: parseFloat(row.precio_unitario),
                subtotal: parseFloat(row.subtotal),
                id_vendedor: row.id_vendedor,
                nombre_vendedor: row.nombre_vendedor
            });
        });

        res.json(Object.values(groupedOrders)); // Devuelve un array de objetos de compra agrupados

    } catch (error) {
        console.error('Error al obtener órdenes para el vendedor:', error);
        res.status(500).json({ message: 'Error interno del servidor al obtener órdenes del vendedor.', error: error.message });
    }
};
