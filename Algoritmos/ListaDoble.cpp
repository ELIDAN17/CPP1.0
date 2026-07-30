#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <filesystem> // para verificar existencia de archivos
#include <cstdlib>    // para system("cls") o "clear"
using namespace std;
namespace fs = filesystem;
// ------------------------- CLASE NODO -------------------------
class Nodo
{
public:
    int id;
    string nombre;
    string correo;
    string carrera;
    int anio;
    Nodo *siguiente;
    Nodo *anterior;

    Nodo(int _id, string _nombre, string _correo, string _carrera, int _anio)
    {
        id = _id;
        nombre = _nombre;
        correo = _correo;
        carrera = _carrera;
        anio = _anio;
        siguiente = nullptr;
        anterior = nullptr;
    }
};

// ------------------------- CLASE LISTA DOBLE -------------------------
class ListaDoble
{
private:
    Nodo *cabeza;
    int idActual;

    void guardarEnArchivo()
    {
        ofstream archivo("registros.txt");
        if (!archivo.is_open())
        {
            cout << "Error: No se pudo abrir el archivo para guardar.\n";
            return;
        }
        Nodo *actual = cabeza;
        while (actual != nullptr)
        {
            archivo << actual->id << ";"
                    << actual->nombre << ";"
                    << actual->correo << ";"
                    << actual->carrera << ";"
                    << actual->anio << endl;
            actual = actual->siguiente;
        }
        archivo.close();
    }

    void cargarDesdeArchivo()
    {
        ifstream archivo("registros.txt");
        if (!archivo.is_open())
        {
            // No hay archivo aún, no es error
            return;
        }
        string linea;
        while (getline(archivo, linea))
        {
            stringstream ss(linea);
            string campo;
            int id, anio;
            string nombre, correo, carrera;

            getline(ss, campo, ';');
            id = stoi(campo);
            getline(ss, nombre, ';');
            getline(ss, correo, ';');
            getline(ss, carrera, ';');
            getline(ss, campo, ';');
            anio = stoi(campo);

            Nodo *nuevo = new Nodo(id, nombre, correo, carrera, anio);
            if (cabeza == nullptr)
            {
                cabeza = nuevo;
            }
            else
            {
                Nodo *actual = cabeza;
                while (actual->siguiente != nullptr)
                {
                    actual = actual->siguiente;
                }
                actual->siguiente = nuevo;
                nuevo->anterior = actual;
            }
            if (id >= idActual)
                idActual = id + 1;
        }
        archivo.close();
    }

public:
    ListaDoble()
    {
        cabeza = nullptr;
        idActual = 1;
        cargarDesdeArchivo();
    }

    ~ListaDoble()
    {
        Nodo *actual = cabeza;
        while (actual != nullptr)
        {
            Nodo *temp = actual;
            actual = actual->siguiente;
            delete temp;
        }
    }

    // 1. AGREGAR estudiante (ID automático)
    void agregar(string nombre, string correo, string carrera, int anio)
    {
        Nodo *nuevo = new Nodo(idActual++, nombre, correo, carrera, anio);

        if (cabeza == nullptr)
        {
            cabeza = nuevo;
        }
        else
        {
            Nodo *actual = cabeza;
            while (actual->siguiente != nullptr)
            {
                actual = actual->siguiente;
            }
            actual->siguiente = nuevo;
            nuevo->anterior = actual;
        }
        guardarEnArchivo();
        cout << "\n✅ Estudiante agregado con ID: " << nuevo->id << endl;
    }

    // 2. MOSTRAR todos los estudiantes
    void mostrar()
    {
        if (cabeza == nullptr)
        {
            cout << "\n📭 No hay estudiantes registrados.\n";
            return;
        }

        cout << "\n📋 LISTA DE ESTUDIANTES:\n";
        cout << "------------------------------------------------------------\n";
        cout << "ID\tNOMBRE\t\tCORREO\t\t\tCARRERA\t\tAÑO\n";
        cout << "------------------------------------------------------------\n";

        Nodo *actual = cabeza;
        while (actual != nullptr)
        {
            cout << actual->id << "\t"
                 << actual->nombre << "\t\t"
                 << actual->correo << "\t\t"
                 << actual->carrera << "\t\t"
                 << actual->anio << endl;
            actual = actual->siguiente;
        }
        cout << "------------------------------------------------------------\n";
    }

    // 3. BUSCAR por nombre (también podría ser por ID)
    void buscarPorNombre(string nombreBuscar)
    {
        if (cabeza == nullptr)
        {
            cout << "\n📭 No hay estudiantes registrados.\n";
            return;
        }

        Nodo *actual = cabeza;
        bool encontrado = false;

        while (actual != nullptr)
        {
            // Búsqueda insensible a mayúsculas/minúsculas (simplificada)
            if (actual->nombre == nombreBuscar)
            {
                cout << "\n🔍 ESTUDIANTE ENCONTRADO:\n";
                cout << "ID: " << actual->id << endl;
                cout << "Nombre: " << actual->nombre << endl;
                cout << "Correo: " << actual->correo << endl;
                cout << "Carrera: " << actual->carrera << endl;
                cout << "Año de ingreso: " << actual->anio << endl;
                encontrado = true;
                break;
            }
            actual = actual->siguiente;
        }

        if (!encontrado)
        {
            cout << "\n❌ No se encontró ningún estudiante con nombre: " << nombreBuscar << endl;
        }
    }

    // 4. MODIFICAR datos de un estudiante por ID
    void modificar(int idBuscar)
    {
        if (cabeza == nullptr)
        {
            cout << "\n📭 No hay estudiantes registrados.\n";
            return;
        }

        Nodo *actual = cabeza;
        while (actual != nullptr)
        {
            if (actual->id == idBuscar)
            {
                cout << "\n✏️ MODIFICANDO ESTUDIANTE ID " << idBuscar << endl;
                cout << "Datos actuales:\n";
                cout << "Nombre: " << actual->nombre << " | Correo: " << actual->correo
                     << " | Carrera: " << actual->carrera << " | Año: " << actual->anio << endl;

                cout << "\nIngrese nuevos datos (deje vacío para mantener):\n";

                string nuevoNombre, nuevoCorreo, nuevaCarrera;
                int nuevoAnio;

                cout << "Nuevo nombre [" << actual->nombre << "]: ";
                getline(cin, nuevoNombre);
                if (!nuevoNombre.empty())
                    actual->nombre = nuevoNombre;

                cout << "Nuevo correo [" << actual->correo << "]: ";
                getline(cin, nuevoCorreo);
                if (!nuevoCorreo.empty())
                    actual->correo = nuevoCorreo;

                cout << "Nueva carrera [" << actual->carrera << "]: ";
                getline(cin, nuevaCarrera);
                if (!nuevaCarrera.empty())
                    actual->carrera = nuevaCarrera;

                cout << "Nuevo año [" << actual->anio << "]: ";
                string anioStr;
                getline(cin, anioStr);
                if (!anioStr.empty())
                    actual->anio = stoi(anioStr);

                guardarEnArchivo();
                cout << "\n✅ Estudiante modificado correctamente.\n";
                return;
            }
            actual = actual->siguiente;
        }

        cout << "\n❌ No se encontró estudiante con ID: " << idBuscar << endl;
    }

    // 5. ELIMINAR estudiante por ID
    void eliminar(int idEliminar)
    {
        if (cabeza == nullptr)
        {
            cout << "\n📭 No hay estudiantes registrados.\n";
            return;
        }

        Nodo *actual = cabeza;

        while (actual != nullptr)
        {
            if (actual->id == idEliminar)
            {
                // Si no es el primero
                if (actual->anterior != nullptr)
                {
                    actual->anterior->siguiente = actual->siguiente;
                }
                else
                {
                    // Es la cabeza
                    cabeza = actual->siguiente;
                }

                // Si no es el último
                if (actual->siguiente != nullptr)
                {
                    actual->siguiente->anterior = actual->anterior;
                }

                cout << "\n🗑️ Eliminando estudiante: " << actual->nombre << " (ID: " << actual->id << ")" << endl;
                delete actual;
                guardarEnArchivo();
                cout << "✅ Estudiante eliminado correctamente.\n";
                return;
            }
            actual = actual->siguiente;
        }

        cout << "\n❌ No se encontró estudiante con ID: " << idEliminar << endl;
    }

    // Recargar desde archivo (útil si se edita manualmente)
    void recargarDesdeArchivo()
    {
        // Liberar memoria actual
        Nodo *actual = cabeza;
        while (actual != nullptr)
        {
            Nodo *temp = actual;
            actual = actual->siguiente;
            delete temp;
        }
        cabeza = nullptr;
        idActual = 1;
        cargarDesdeArchivo();
        cout << "\n🔄 Registros recargados desde archivo.\n";
    }
};

// ------------------------- MENÚ PRINCIPAL -------------------------
void limpiarPantalla()
{
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

int main()
{
    cout << "📁 El archivo se guarda en: " << filesystem::current_path() << endl;
    ListaDoble lista;
    int opcion;

    cout << "\n🎓 BIENVENIDO AL SISTEMA DE GESTIÓN ACADÉMICA\n";

    while (true)
    {
        cout << "\n============================================\n";
        cout << "   MENÚ PRINCIPAL\n";
        cout << "============================================\n";
        cout << "1. ➕ Agregar nuevo estudiante\n";
        cout << "2. 📋 Mostrar todos los estudiantes\n";
        cout << "3. 🔍 Buscar estudiante por nombre\n";
        cout << "4. ✏️ Modificar estudiante por ID\n";
        cout << "5. 🗑️ Eliminar estudiante por ID\n";
        cout << "6. 🔄 Recargar datos desde archivo\n";
        cout << "7. 🚪 Salir\n";
        cout << "============================================\n";
        cout << "Opción: ";
        cin >> opcion;
        cin.ignore();

        switch (opcion)
        {
        case 1:
        {
            string nombre, correo, carrera;
            int anio;

            cout << "\n--- NUEVO ESTUDIANTE ---\n";
            cout << "Nombre completo: ";
            getline(cin, nombre);
            cout << "Correo electrónico: ";
            getline(cin, correo);
            cout << "Escuela profesional: ";
            getline(cin, carrera);
            cout << "Año de ingreso: ";
            cin >> anio;
            cin.ignore();

            lista.agregar(nombre, correo, carrera, anio);
            break;
        }
        case 2:
            lista.mostrar();
            break;
        case 3:
        {
            string nombre;
            cout << "\n--- BUSCAR POR NOMBRE ---\n";
            cout << "Nombre a buscar: ";
            getline(cin, nombre);
            lista.buscarPorNombre(nombre);
            break;
        }
        case 4:
        {
            int id;
            cout << "\n--- MODIFICAR ESTUDIANTE ---\n";
            cout << "ID del estudiante a modificar: ";
            cin >> id;
            cin.ignore();
            lista.modificar(id);
            break;
        }
        case 5:
        {
            int id;
            cout << "\n--- ELIMINAR ESTUDIANTE ---\n";
            cout << "ID del estudiante a eliminar: ";
            cin >> id;
            cin.ignore();
            lista.eliminar(id);
            break;
        }
        case 6:
            lista.recargarDesdeArchivo();
            break;
        case 7:
            cout << "\n👋 Gracias por usar el sistema. ¡Hasta luego!\n";
            return 0;
        default:
            cout << "\n❌ Opción no válida. Intente nuevamente.\n";
        }
    }

    return 0;
}