/*
// Logger monitoreo de excepciones en cpp
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <ctime>
#include <vector>
#include <thread>
#include <chrono>
using namespace std;

// Excepción personalizada
class DivisionPorCero : public runtime_error
{
public:
    DivisionPorCero() : runtime_error("Error: División entre cero detectada.") {}
};

class Registro
{
private:
    ofstream archivo;

public:
    Registro(const string &nombreArchivo)
    {
        archivo.open(nombreArchivo, ios::app);
    }

    ~Registro()
    {
        if (archivo.is_open())
            archivo.close();
    }

    void registrar(const string &mensaje)
    {
        time_t ahora = time(0);
        archivo << "[" << ctime(&ahora) << "] " << mensaje << endl;
    }
};

// Función que lanza excepción si hay división por cero
double dividir(double a, double b)
{
    if (b == 0)
        throw DivisionPorCero();
    return a / b;
}

int main()
{
    Registro log("sistema.log");
    vector<pair<double, double>> operaciones = {{10, 2}, {5, 0}, {-8, 4}, {9, 3}};

    for (auto [a, b] : operaciones)
    {
        try
        {
            double resultado = dividir(a, b);
            cout << "Resultado de " << a << " / " << b << " = " << resultado << endl;
            log.registrar("División exitosa: " + to_string(a) + "/" + to_string(b) + " = " + to_string(resultado));
        }
        catch (const DivisionPorCero &ex)
        {
            cerr << ex.what() << endl;
            log.registrar("Error: " + string(ex.what()));
        }
        catch (const exception &ex)
        {
            cerr << "Excepción genérica: " << ex.what() << endl;
            log.registrar("Excepción genérica: " + string(ex.what()));
        }

        // Simula monitoreo en tiempo real
        this_thread::sleep_for(chrono::seconds(1));
    }

    log.registrar("Monitoreo finalizado correctamente.");
    cout << "Consulta el archivo sistema.log para ver los registros." << endl;
    return 0;
}*/

/*
// Logger monitoreo de excepciones en cpp
#include <iostream>  // para entrada y salida (cout, cerr)
#include <fstream>   // para el manejo de archivos (ofstream, ifstream)
#include <stdexcept> // para clases de excepciones estándar (runtime_error)
#include <ctime>     // para funciones de tiempo (time, ctime) fecha, hora
#include <vector>    // para el contenedor dinámico
#include <thread>    // para el manejo de hilos (para simular espera)
#include <chrono>    // para operaciones de tiempo en hilos
using namespace std; // para simplificar el código

// --- 1. EXCEPCIÓN PERSONALIZADA ---
// Una clase de excepción que hereda de runtime_error para errores en tiempo de ejecución.
class DivisionPorCero : public runtime_error
{
public:
    // Constructor: llama al constructor de la clase base (runtime_error) la cual es heredada.
    DivisionPorCero() : runtime_error("Error: División entre cero detectada.") {}
    // Al heredar, ya tenemos el método .what() que devolverá el string anterior.
};

// --- 2. CLASE REGISTRO (LOGGER) ---
class Registro
{
private:
    // ofstream es el flujo de salida a archivo, usado para escribir el log.
    ofstream archivo;

public:
    // Constructor: Abre el archivo de log. (adquisición del recurso).
    Registro(const string &nombreArchivo)
    {
        // Abre el archivo. ios::app asegura que los nuevos logs se añadan al final (append).
        archivo.open(nombreArchivo, ios::app);
    }

    // Destructor: Se llama automáticamente cuando el objeto 'log' sale de su ámbito (RAII).
    ~Registro()
    {
        // Cierra el archivo si está abierto, liberando el recurso del sistema.
        if (archivo.is_open())
            archivo.close();
    }

    // Método para escribir un mensaje en el log con fecha y hora.
    void registrar(const string &mensaje)
    {
        // time(0) obtiene la hora actual del sistema.
        time_t ahora = time(0);
        // ctime(&ahora) convierte el tiempo a un string legible.
        // Escribe en el archivo: [timestamp] mensaje \n
        archivo << "[" << ctime(&ahora) << "] " << mensaje << endl;
    }
};

// --- 3. FUNCIÓN PRINCIPAL ---
// Función que realiza una división y verifica la pre-condición de división por cero (excepciones).
double dividir(double a, double b)
{
    // Verificación de la pre-condición: si es cero, se lanza la excepción.
    if (b == 0)
        // Lanza la excepción personalizada. El flujo normal del programa se detiene.
        throw DivisionPorCero();
    // Retorna el resultado si la operación es segura.
    return a / b;
}

// --- 4. FUNCIÓN PRINCIPAL (CLIENTE Y MONITOREO) ---
int main()
{
    // Instancia el Logger. El constructor abre 'sistema.log'.
    Registro log("sistema.log");
   
    // Definición de datos de prueba: pares {numerador, denominador}.
    // La operación {5, 0} generará la excepción.
    vector<pair<double, double>> operaciones = {{10, 2}, {5, 0}, {-8, 4}, {9, 3}};

    // Itera sobre cada operación en el vector.
    for (auto [a, b] : operaciones)
    {
        // Bloque TRY: Contiene el código que podría lanzar una excepción.
        try
        {
            double resultado = dividir(a, b);
           
            // Si es exitosa, imprime y registra la operación.
            cout << "Resultado de " << a << " / " << b << " = " << resultado << endl;
            log.registrar("División exitosa: " + to_string(a) + "/" + to_string(b) + " = " + to_string(resultado));
        }
        // Bloque CATCH específico: Atrapa la excepción personalizada 'DivisionPorCero'.
        catch (const DivisionPorCero &ex)
        {
            // Imprime el mensaje de error en la salida de error estándar (cerr).
            cerr << ex.what() << endl;
            // Registra el error en el archivo de log.
            log.registrar("Error: " + string(ex.what()));
        }
        // Bloque CATCH genérico: Atrapa cualquier otra excepción estándar no capturada antes.
        catch (const exception &ex)
        {
            // Imprime la excepción genérica.
            cerr << "Excepción genérica: " << ex.what() << endl;
            log.registrar("Excepción genérica: " + string(ex.what()));
        }

        // Simula un retraso de 1 segundo para fines de demostración de monitoreo.
        this_thread::sleep_for(chrono::seconds(1));
    }

    // Mensaje final de registro.
    log.registrar("Monitoreo finalizado correctamente.");
    cout << "Consulta el archivo sistema.log para ver los registros." << endl;
    return 0;
}
*/

/*
#include <iostream>
#include <fstream>
#include <stdexcept>
#include <ctime>
using namespace std;

// Excepción personalizada
class DivisionByZeroException : public runtime_error {
public:
    DivisionByZeroException()
        : runtime_error("Error: División entre cero detectada.") {}
};

// Logger simple
class Logger {
private:
    ofstream logfile;

public:
    Logger(const string& filename) {
        logfile.open(filename, ios::app);
    }

    ~Logger() {
        if (logfile.is_open()) logfile.close();
    }

    void log(const string& message) {
        time_t now = time(0);
        logfile << "[" << ctime(&now) << "] " << message << endl;
    }
};

// Función que genera una excepción
double dividir(double a, double b) {
    if (b == 0) throw DivisionByZeroException();
    return a / b;
}

int main() {
    Logger logger("system.log");

    try {
        cout << "Intentando dividir 10 / 0 ..." << endl;
        double resultado = dividir(10, 0);
        cout << "Resultado: " << resultado << endl;
    }
    catch (const DivisionByZeroException& ex) {
        cerr << ex.what() << endl;
        logger.log(ex.what());
    }
    catch (const exception& ex) {
        cerr << "Excepción genérica: " << ex.what() << endl;
        logger.log("Excepción genérica: " + string(ex.what()));
    }

    logger.log("Ejecución finalizada correctamente.");
    cout << "Verifica el archivo system.log para los registros." << endl;

    return 0;
}
*/