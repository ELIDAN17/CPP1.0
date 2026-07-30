// Carga las variables de entorno del archivo .env al inicio
require('dotenv').config();

const express = require('express');
const cors = require('cors');

// Importar la conexión a la base de datos
const db = require('./config/db');

// Importar archivos de rutas
const productRoutes = require('./routes/productRoutes');
console.log('DEBUG: Valor de productRoutes:', productRoutes); // Nuevo log
const authRoutes = require('./routes/authRoutes');
console.log('DEBUG: Valor de authRoutes:', authRoutes); // Nuevo log
const categoryRoutes = require('./routes/categoryRoutes'); // Asegúrate que estos archivos existan
console.log('DEBUG: Valor de categoryRoutes:', categoryRoutes); // Nuevo log
const userRoutes = require('./routes/userRoutes');
console.log('DEBUG: Valor de userRoutes:', userRoutes); // Nuevo log
const orderRoutes = require('./routes/orderRoutes');
console.log('DEBUG: Valor de orderRoutes:', orderRoutes); // Nuevo log
const addressRoutes = require('./routes/addressRoutes');
console.log('DEBUG: Valor de addressRoutes:', addressRoutes); // Nuevo log
const paymentMethodRoutes = require('./routes/paymentMethodRoutes');
console.log('DEBUG: Valor de paymentMethodRoutes:', paymentMethodRoutes); // Nuevo log
console.log('Valor de productRoutes al inicio de server.js:', productRoutes); // AÑADE ESTA LÍNEA AQUÍ
console.log('Tipo de productRoutes al inicio de server.js:', typeof productRoutes); // Y ESTA TAMBIÉN
console.log('Es productRoutes una función middleware?', typeof productRoutes === 'function' || (productRoutes && typeof productRoutes.stack === 'object')); // Y ESTA


const app = express();
const port = process.env.PORT || 3001; // El backend se ejecutará en el puerto 3001 por defecto

// ====================================================================
// MIDDLEWARES GLOBALES
// ====================================================================

// Middleware para parsear JSON en el cuerpo de las solicitudes (req.body)
app.use(express.json());

// Middleware CORS: Permite que tu frontend de React se conecte a esta API
app.use(cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:5173'
}));

// ====================================================================
// RUTAS DE LA API
// ====================================================================

// Ruta de prueba simple (GET /)
app.get('/', (req, res) => {
    res.send('API de la tienda funcionando correctamente!');
});

// Usar las rutas importadas para cada recurso
app.use('/api/productos', productRoutes);
app.use('/api/auth', authRoutes);
app.use('/api/categorias', categoryRoutes);
app.use('/api/usuarios', userRoutes);
app.use('/api/ordenes', orderRoutes);
app.use('/api/direcciones', addressRoutes);
app.use('/api/metodos-pago', paymentMethodRoutes);

// ====================================================================
// MANEJO DE ERRORES (Middleware para errores 404 y 500)
// ====================================================================

// Middleware para manejar rutas no encontradas (404)
app.use((req, res, next) => {
    res.status(404).json({ message: 'Ruta no encontrada.' });
});

// Middleware centralizado para manejar errores internos del servidor (500)
app.use((err, req, res, next) => {
    console.error(err.stack); // Loggea el error para depuración
    res.status(500).json({ message: 'Algo salió mal en el servidor.' });
});

// ====================================================================
// INICIAR EL SERVIDOR EXPRESS
// ====================================================================

app.listen(port, () => {
    console.log(`--- INICIANDO SERVIDOR ---`); // Para depuración
    console.log(`🚀 Servidor API escuchando en http://localhost:${port}`);
    console.log(`Para probar productos: http://localhost:${port}/api/productos`);
    console.log(`Para registrar usuario (POST): http://localhost:${port}/api/auth/register`);
    console.log(`Para login (POST): http://localhost:${port}/api/auth/login`);
    console.log(`Para probar métodos de pago: http://localhost:${port}/api/metodos-pago`); // Nuevo log
});