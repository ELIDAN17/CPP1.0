#include <iostream>
#include <string>
using namespace std;
class IFormatoTexto
{ // 1. Target (La interfaz que nuestro cliente espera)
public:
    virtual void guardarTexto(const string &data) = 0;
    virtual ~IFormatoTexto() = default;
};
class FormatoJSON
{ // 2. Adaptee (La clase incompatible, no la podemos modificar)
public:
    void guardarDatosJSON(const string &json_data)
    {
        cout << "Guardando datos en formato JSON: " << json_data << endl;
    }
};
class AdaptadorJSONaTexto : public IFormatoTexto
{ // 3. Adapter (La clase que conecta ambas interfaces)
private:
    FormatoJSON *adaptee;

public:
    AdaptadorJSONaTexto()
    {
        adaptee = new FormatoJSON();
    }
    ~AdaptadorJSONaTexto()
    {
        delete adaptee;
    }
    void guardarTexto(const string &data) override
    {
        string json_format = "{ \"data\": \"" + data + "\" }";
        adaptee->guardarDatosJSON(json_format);
    }
};
void cliente_aplicacion(IFormatoTexto *herramienta)
{ // 4. Cliente (Nuestra aplicación que usa la interfaz Target)
    herramienta->guardarTexto("Este es el texto del reporte.");
}

int main()
{
    IFormatoTexto *adaptador = new AdaptadorJSONaTexto();
    cliente_aplicacion(adaptador);

    delete adaptador;
    return 0;
}

/*
#include <iostream>
#include <string>
using namespace std;
class IFormatoArchivo
{ // target
public:
    virtual void guardar(const string &contenido) = 0;
    virtual ~IFormatoArchivo() = default;
};
class LibreriaAntigua
{ // adaptee
public:
    void registrarDatos(const string &texto, int formato_id)
    {
        cout << "Libreria antigua registrando datos: '" << texto << "' con formato ID " << formato_id << endl;
    }
};
class AdaptadorArchivo : public IFormatoArchivo
{ // adapter
private:
    LibreriaAntigua libreria; // adapter->Adaptee.
public:
    void guardar(const string &contenido) override
    {
        cout << "Adaptador: Traduccion en curso..." << endl;
        libreria.registrarDatos(contenido, 1);
    }
};
int main()
{
    IFormatoArchivo *miHerramienta = new AdaptadorArchivo();
    miHerramienta->guardar("Contenido importante para el archivo.");
    delete miHerramienta;
    return 0;
}*/

/*
#include <iostream>
#include <string>
#include <chrono> // Para obtener la fecha y hora
#include <ctime>  // Para convertir el tiempo

using namespace std;

class Logger
{
private:
    static Logger *instance;
    Logger() {} // Constructor privado

public:
    static Logger *getInstance()
    {
        if (instance == nullptr)
        {
            instance = new Logger();
        }
        return instance;
    }

    void logMessage(const string &msg)
    {
        // Obtener la hora actual
        auto now = chrono::system_clock::now();
        time_t currentTime = chrono::system_clock::to_time_t(now);

        // Convertir a un formato de cadena
        string timeStr = ctime(&currentTime);
        timeStr.pop_back(); // Eliminar el carácter de nueva línea

        cout << "[" << timeStr << "]: " << msg << endl;
    }
};

// inicialización estática
Logger *Logger::instance = nullptr;

int main()
{
    Logger *log1 = Logger::getInstance();
    Logger *log2 = Logger::getInstance();

    log1->logMessage("Iniciando aplicación...");
    log2->logMessage("Usando la misma instancia de Logger");

    if (log1 == log2)
    {
        cout << "Ambos objetos son la misma instancia (Singleton)." << endl;
    }

    return 0;
}*/

/*
#include <iostream>
using namespace std;
class Logger
{
private:
    static Logger *instance; // única instancia
    Logger() {}              // constructor privado
public:
    static Logger *getInstance()
    {
        if (instance == nullptr)
        {
            instance = new Logger();
        }
        return instance;
    }
    void logMessage(const string &msg)
    {
        cout << "[LOG]: " << msg << endl;
    }
};
// inicialización estática
Logger *Logger::instance = nullptr;
int main()
{
    Logger *log1 = Logger::getInstance();
    Logger *log2 = Logger::getInstance();
    log1->logMessage("Iniciando aplicación...");
    log2->logMessage("Usando la misma instancia de Logger");
    // Verificamos si ambas instancias son iguales
    if (log1 == log2)
    {
        cout << "Ambos objetos son la misma instancia (Singleton)." << endl;
    }
    return 0;
}
*/