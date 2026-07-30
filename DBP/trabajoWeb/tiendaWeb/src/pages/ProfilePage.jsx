// src/frontend/src/pages/ProfilePage.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext'; 

const ProfilePage = () => {
    // información usuario 
    const { user, token, logout, updateAuthUser } = useAuth();
    const userId = user?.id_usuario;

    // perfil y direcciones
    const [profileData, setProfileData] = useState({
        nombre: '',
        apellido: '',
        correo: '',
        telefono: '',
        rol: '' 
    });
    const [addresses, setAddresses] = useState([]);

    // Estados para UI (carga, errores, mensajes)
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [message, setMessage] = useState(null);

    // Estado para edición de perfil
    const [isEditingProfile, setIsEditingProfile] = useState(false);
    const [newPassword, setNewPassword] = useState('');

    // Estado dirección (añadir/editar)
    const [showAddressForm, setShowAddressForm] = useState(false);
    const [currentAddress, setCurrentAddress] = useState(null);
    const [addressFormData, setAddressFormData] = useState({
        ciudad: '',
        calle: '',
        numero: '',
        referencia: ''
    });

    // Cargar datos al usuario/token
    useEffect(() => {
        if (!userId || !token) {
            setError('No autenticado. Por favor, inicia sesión.');
            setLoading(false);
            return;
        }

        const fetchProfileAndAddresses = async () => {
            try {
                const profileRes = await axios.get(`http://localhost:3001/api/usuarios/${userId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setProfileData(profileRes.data);

                const addressesRes = await axios.get(`http://localhost:3001/api/direcciones/usuario/${userId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setAddresses(addressesRes.data);

            } catch (err) {
                console.error('Error al cargar datos:', err);
                setError(err.response?.data?.message || 'Error al cargar el perfil o las direcciones.');
                if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                    logout();
                }
            } finally {
                setLoading(false);
            }
        };

        fetchProfileAndAddresses();
    }, [userId, token, logout]);

    const handleProfileChange = (e) => {
        const { name, value } = e.target;
        setProfileData(prevData => ({ ...prevData, [name]: value }));
    };

    const handleAddressFormChange = (e) => {
        const { name, value } = e.target;
        setAddressFormData(prevData => ({ ...prevData, [name]: value }));
    };

    // Guardar cambios del perfil
    const handleSaveProfile = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setMessage(null);

        try {
            const updateData = { ...profileData };
            if (newPassword) {
                updateData.contraseña = newPassword;
            }

            await axios.put(`http://localhost:3001/api/usuarios/${userId}`, updateData, {
                headers: { Authorization: `Bearer ${token}` }
            });

            setMessage('Perfil actualizado con éxito!');
            setIsEditingProfile(false);
            setNewPassword('');
            updateAuthUser({
                nombre: profileData.nombre,
                apellido: profileData.apellido,
                correo: profileData.correo,
                telefono: profileData.telefono,
                rol: profileData.rol 
            }); 

        } catch (err) {
            console.error('Error al actualizar perfil:', err);
            setError(err.response?.data?.message || 'Error al actualizar el perfil.');
        } finally {
            setLoading(false);
        }
    };

    // Añadir o Editar una Dirección
    const handleSaveAddress = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setMessage(null);

        try {
            if (currentAddress) {
                await axios.put(`http://localhost:3001/api/direcciones/${currentAddress.id_direccion}`, {
                    ...addressFormData,
                    id_usuario: userId
                }, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setMessage('Dirección actualizada con éxito!');
            } else {
                await axios.post('http://localhost:3001/api/direcciones', {
                    ...addressFormData,
                    id_usuario: userId
                }, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setMessage('Dirección añadida con éxito!');
            }

            // Recargar direcciones despues de añadir/editar
            const addressesRes = await axios.get(`http://localhost:3001/api/direcciones/usuario/${userId}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setAddresses(addressesRes.data);
            setShowAddressForm(false);
            setCurrentAddress(null);
            setAddressFormData({ ciudad: '', calle: '', numero: '', referencia: '' });

        } catch (err) {
            console.error('Error al guardar dirección:', err);
            setError(err.response?.data?.message || 'Error al guardar la dirección.');
        } finally {
            setLoading(false);
        }
    };

    // Eliminar una Dirección
    const handleDeleteAddress = async (id_direccion) => {
        if (!window.confirm('¿Estás seguro de que quieres eliminar esta dirección?')) {
            return;
        }

        setLoading(true);
        setError(null);
        setMessage(null);

        try {
            await axios.delete(`http://localhost:3001/api/direcciones/${id_direccion}`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            setMessage('Dirección eliminada con éxito!');
            setAddresses(prevAddresses => prevAddresses.filter(addr => addr.id_direccion !== id_direccion));
        } catch (err) {
            console.error('Error al eliminar dirección:', err);
            setError(err.response?.data?.message || 'Error al eliminar la dirección.');
        } finally {
            setLoading(false);
        }
    };

    // Funciones visibilidad dirección
    const handleAddAddressClick = () => {
        setCurrentAddress(null);
        setAddressFormData({ ciudad: '', calle: '', numero: '', referencia: '' });
        setShowAddressForm(true);
    };

    const handleEditAddressClick = (address) => {
        setCurrentAddress(address);
        setAddressFormData({
            ciudad: address.ciudad,
            calle: address.calle,
            numero: address.numero,
            referencia: address.referencia
        });
        setShowAddressForm(true);
    };

    const handleCancelAddressForm = () => {
        setShowAddressForm(false);
        setCurrentAddress(null);
        setAddressFormData({ ciudad: '', calle: '', numero: '', referencia: '' });
    };
    if (loading && !profileData.correo && addresses.length === 0) {
        return <div className="flex justify-center items-center min-h-screen bg-gray-100"><p className="text-xl text-gray-700">Cargando perfil y direcciones...</p></div>;
    }

    if (error) {
        return <div className="flex justify-center items-center min-h-screen bg-gray-100"><p className="text-xl text-red-600 font-semibold">Error: {error}</p></div>;
    }

    if (!userId) {
        return <div className="flex justify-center items-center min-h-screen bg-gray-100"><p className="text-xl text-red-600 font-semibold">Por favor, inicia sesión para ver tu perfil.</p></div>;
    }

    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4 sm:px-6 lg:px-8 font-inter">
            <div className="max-w-5xl mx-auto">
                {message && (
                    <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-md relative mb-6 text-center shadow-sm" role="alert">
                        {message}
                    </div>
                )}
                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md relative mb-6 text-center shadow-sm" role="alert">
                        {error}
                    </div>
                )}
                <div className="bg-white shadow-xl rounded-xl p-6 sm:p-8 mb-8 flex flex-col items-center text-center relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-32 bg-gradient-to-r from-blue-500 to-purple-600 rounded-t-xl"></div>
                    
                    <div className="relative mt-16 mb-4">
                        <img 
                            src={`https://placehold.co/120x120/a78bfa/ffffff?text=${profileData.nombre ? profileData.nombre[0].toUpperCase() : 'U'}`} 
                            alt="Profile Avatar" 
                            className="w-32 h-32 rounded-full border-4 border-white shadow-lg object-cover bg-purple-200"
                        />
                    </div>

                    <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900 mb-2">
                        {profileData.nombre} {profileData.apellido}
                    </h1>
                    <p className="text-lg text-gray-600 mb-4">
                        {profileData.rol ? profileData.rol.charAt(0).toUpperCase() + profileData.rol.slice(1) : 'Usuario'}
                    </p>
                    <p className="text-gray-700 mb-4 max-w-lg">
                        Bienvenido a tu perfil en MinimarketShop. Aquí puedes gestionar tu información personal y tus direcciones.
                    </p>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 border border-gray-200">
                        <h2 className="text-2xl font-bold mb-5 pb-2 border-b-2 border-gray-200 text-gray-700">Datos Personales</h2>
                        {!isEditingProfile ? (
                            <div className="space-y-3">
                                <p className="text-lg"><strong className="text-gray-700">Correo:</strong> {profileData.correo}</p>
                                <p className="text-lg"><strong className="text-gray-700">Teléfono:</strong> {profileData.telefono || 'No especificado'}</p>
                                <p className="text-lg"><strong className="text-gray-700">Fecha de Creación:</strong> {new Date(profileData.fecha_creacion).toLocaleDateString()}</p>
                                {profileData.fecha_actualizacion && (
                                    <p className="text-lg"><strong className="text-gray-700">Última Actualización:</strong> {new Date(profileData.fecha_actualizacion).toLocaleDateString()}</p>
                                )}
                                <div className="pt-4">
                                    <button
                                        onClick={() => setIsEditingProfile(true)}
                                        className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded-lg transition duration-300 ease-in-out transform hover:scale-105 shadow-md w-full"
                                    >
                                        Editar Perfil
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <form onSubmit={handleSaveProfile} className="space-y-4">
                                <div>
                                    <label htmlFor="nombre" className="block text-gray-700 text-base font-semibold mb-2">Nombre:</label>
                                    <input
                                        type="text"
                                        id="nombre"
                                        name="nombre"
                                        value={profileData.nombre}
                                        onChange={handleProfileChange}
                                        className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    />
                                </div>
                                <div>
                                    <label htmlFor="apellido" className="block text-gray-700 text-base font-semibold mb-2">Apellido:</label>
                                    <input
                                        type="text"
                                        id="apellido"
                                        name="apellido"
                                        value={profileData.apellido}
                                        onChange={handleProfileChange}
                                        className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    />
                                </div>
                                <div>
                                    <label htmlFor="correo" className="block text-gray-700 text-base font-semibold mb-2">Correo Electrónico:</label>
                                    <input
                                        type="email"
                                        id="correo"
                                        name="correo"
                                        value={profileData.correo}
                                        onChange={handleProfileChange}
                                        className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                                        required
                                    />
                                </div>
                                <div>
                                    <label htmlFor="telefono" className="block text-gray-700 text-base font-semibold mb-2">Teléfono:</label>
                                    <input
                                        type="text"
                                        id="telefono"
                                        name="telefono"
                                        value={profileData.telefono}
                                        onChange={handleProfileChange}
                                        className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                                <div className="mb-6">
                                    <label htmlFor="newPassword" className="block text-gray-700 text-base font-semibold mb-2">Nueva Contraseña (dejar en blanco si no cambias):</label>
                                    <input
                                        type="password"
                                        id="newPassword"
                                        name="newPassword"
                                        value={newPassword}
                                        onChange={(e) => setNewPassword(e.target.value)}
                                        className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    />
                                </div>
                                <div className="flex flex-col sm:flex-row items-center justify-end space-y-3 sm:space-y-0 sm:space-x-3">
                                    <button
                                        type="submit"
                                        className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition duration-300 ease-in-out transform hover:scale-105 shadow-md w-full sm:w-auto"
                                        disabled={loading}
                                    >
                                        {loading ? 'Guardando...' : 'Guardar Cambios'}
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => { setIsEditingProfile(false); setNewPassword(''); setError(null); }}
                                        className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 transition duration-300 ease-in-out transform hover:scale-105 shadow-md w-full sm:w-auto"
                                    >
                                        Cancelar
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>

                    {/* Sección de Direcciones */}
                    <div className="bg-white shadow-lg rounded-xl p-6 sm:p-8 border border-gray-200">
                        <h2 className="text-2xl font-bold mb-5 pb-2 border-b-2 border-gray-200 text-gray-700">Mis Direcciones</h2>

                        {!showAddressForm && (
                            <button
                                onClick={handleAddAddressClick}
                                className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-5 rounded-lg mb-6 transition duration-300 ease-in-out transform hover:scale-105 shadow-md w-full"
                            >
                                Añadir Nueva Dirección
                            </button>
                        )}

                        {showAddressForm && (
                            <div className="mb-8 border border-gray-200 p-6 rounded-xl bg-gray-50 shadow-inner">
                                <h3 className="text-xl font-bold mb-4 text-gray-700">{currentAddress ? 'Editar Dirección' : 'Añadir Nueva Dirección'}</h3>
                                <form onSubmit={handleSaveAddress} className="space-y-4">
                                    <div>
                                        <label htmlFor="ciudad" className="block text-gray-700 text-base font-semibold mb-2">Ciudad:</label>
                                        <input
                                            type="text"
                                            id="ciudad"
                                            name="ciudad"
                                            value={addressFormData.ciudad}
                                            onChange={handleAddressFormChange}
                                            className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="calle" className="block text-gray-700 text-base font-semibold mb-2">Calle:</label>
                                        <input
                                            type="text"
                                            id="calle"
                                            name="calle"
                                            value={addressFormData.calle}
                                            onChange={handleAddressFormChange}
                                            className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="numero" className="block text-gray-700 text-base font-semibold mb-2">Número:</label>
                                        <input
                                            type="text"
                                            id="numero"
                                            name="numero"
                                            value={addressFormData.numero}
                                            onChange={handleAddressFormChange}
                                            className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500"
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="referencia" className="block text-gray-700 text-base font-semibold mb-2">Referencia (Opcional):</label>
                                        <textarea
                                            id="referencia"
                                            name="referencia"
                                            value={addressFormData.referencia}
                                            onChange={handleAddressFormChange}
                                            className="shadow-sm appearance-none border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 h-24"
                                        ></textarea>
                                    </div>
                                    <div className="flex flex-col sm:flex-row items-center justify-end space-y-3 sm:space-y-0 sm:space-x-3">
                                        <button
                                            type="submit"
                                            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 transition duration-300 ease-in-out transform hover:scale-105 shadow-md w-full sm:w-auto"
                                            disabled={loading}
                                        >
                                            {loading ? 'Guardando...' : 'Guardar Dirección'}
                                        </button>
                                        <button
                                            type="button"
                                            onClick={handleCancelAddressForm}
                                            className="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-5 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 transition duration-300 ease-in-out transform hover:scale-105 shadow-md w-full sm:w-auto"
                                        >
                                            Cancelar
                                        </button>
                                    </div>
                                </form>
                            </div>
                        )}

                        {addresses.length === 0 ? (
                            !showAddressForm && <p className="text-gray-600 text-lg">No tienes direcciones registradas.</p>
                        ) : (
                            <div className="grid grid-cols-1 gap-6"> 
                                {addresses.map(address => (
                                    <div key={address.id_direccion} className="border border-gray-200 p-5 rounded-xl shadow-sm bg-gray-50 flex flex-col justify-between">
                                        <div>
                                            <p className="font-bold text-xl mb-1 text-gray-800">{address.calle} {address.numero}</p>
                                            <p className="text-gray-700 mb-1">{address.ciudad}</p>
                                            {address.referencia && <p className="text-gray-600 text-sm italic">Referencia: {address.referencia}</p>}
                                        </div>
                                        <div className="mt-4 flex gap-3">
                                            <button
                                                onClick={() => handleEditAddressClick(address)}
                                                className="bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-lg text-sm transition duration-300 ease-in-out transform hover:scale-105 shadow"
                                            >
                                                Editar
                                            </button>
                                            <button
                                                onClick={() => handleDeleteAddress(address.id_direccion)}
                                                className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-lg text-sm transition duration-300 ease-in-out transform hover:scale-105 shadow"
                                            >
                                                Eliminar
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
