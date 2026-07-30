const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
app.use(cors({
    origin: ['http://localhost:5173', 'http://localhost:4173'], // URL de tu frontend
    credentials: true,
    exposedHeaders: ['Content-Disposition'] 
}));

app.use(express.json()); 

// Importar Rutas
const authRoutes = require('./src/routes/authRoutes');
const perfilRoutes = require('./src/routes/perfilRoutes');
const practicaRoutes = require('./src/routes/practicaRoutes');
const bitacoraRoutes = require('./src/routes/bitacoraRoutes');
const documentoRoutes = require('./src/routes/documentoRoutes');
const evaluacionRoutes = require('./src/routes/evaluacionRoutes');
const reporteRoutes = require('./src/routes/reporteRoutes');
const dashboardRoutes = require('./src/routes/dashboardRoutes');
const notificacionRoutes = require('./src/routes/notificacionRoutes');
const tutorRoutes = require('./src/routes/tutorRoutes');
const adminRoutes = require('./src/routes/adminRoutes');
const decanoRoutes = require('./src/routes/decanoRoutes');

// Registrar Rutas globales de la API
app.use('/api/auth', authRoutes);
app.use('/api/perfil', perfilRoutes);
app.use('/api/practicas', practicaRoutes);
app.use('/api/dashboard', dashboardRoutes);
app.use('/api/reportes', reporteRoutes);
app.use('/api/evaluaciones', evaluacionRoutes);
app.use('/api/bitacora', bitacoraRoutes);
app.use('/api/documentos', documentoRoutes);
app.use('/api/notificaciones', notificacionRoutes);
app.use('/api/tutores', tutorRoutes);
app.use('/api/tutor', tutorRoutes);
app.use('/api/admin', adminRoutes);
app.use('/api/decano', decanoRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Servidor SMCPP corriendo en http://localhost:${PORT}`);
}); 