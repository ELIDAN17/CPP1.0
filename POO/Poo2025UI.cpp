#include <iostream>
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;
#include <cmath>
#include <stdexcept>
#include <vector>
#include <memory>
#include <numeric>
#include <algorithm>

// 1. Receptor (Receiver): El objeto que realiza la acción real
class EditorDeTexto
{
private:
    string contenido;

public:
    EditorDeTexto() : contenido("") {}
    void guardar(const string &nuevo_contenido)
    {
        contenido = nuevo_contenido;
        // Muestra solo los primeros 20 caracteres
        cout << "Editor: Contenido guardado: '" << contenido.substr(0, 20) << (contenido.length() > 20 ? "..." : "") << "'" << endl;
    }
    void cargar(const string &contenido_anterior)
    {
        contenido = contenido_anterior;
        cout << "Editor: Contenido deshecho. Estado actual: '" << contenido.substr(0, 20) << (contenido.length() > 20 ? "..." : "") << "'" << endl;
    }
    string getContenido() const
    {
        return contenido;
    }
};
// 2. Interfaz Command
class Comando
{
public:
    virtual void ejecutar() = 0;
    virtual void deshacer() = 0;
    virtual ~Comando() = default;
};
// 3. Comando Concreto: Guardar
class GuardarCommand : public Comando
{
private:
    EditorDeTexto *editor;
    string nuevo_contenido;
    string contenido_anterior; // Almacena el estado para el Deshacer
public:
    GuardarCommand(EditorDeTexto *e, const string &nuevo)
        : editor(e), nuevo_contenido(nuevo), contenido_anterior(e->getContenido()) {}
    void ejecutar() override
    {
        editor->guardar(nuevo_contenido);
    }
    void deshacer() override
    {
        editor->cargar(contenido_anterior);
    }
};
// 4. Invocador: Almacena el historial de comandos
class Invocador
{
private:
    // Usa unique_ptr para gestionar la memoria de los comandos ejecutados
    vector<unique_ptr<Comando>> historial;

public:
    void ejecutarComando(Comando *comando)
    {
        cout << "\nEjecutando comando..." << endl;
        comando->ejecutar();
        historial.push_back(unique_ptr<Comando>(comando));
    }
    void deshacerUltimo()
    {
        if (!historial.empty())
        {
            cout << "\nDeshaciendo comando..." << endl;
            historial.back()->deshacer(); // Deshace la última acción
            historial.pop_back();         // Quita el comando del historial
        }
        else
        {
            cout << "\nHistorial vacío. Nada que deshacer." << endl;
        }
    }
};
int main()
{
    cout << "\n--- DEMOSTRACIÓN DEL PATRÓN COMMAND ---" << endl;
    EditorDeTexto editor;
    Invocador invocador;
    // Comando 1: Guardar primer texto
    Comando *cmd1 = new GuardarCommand(&editor, "Este es el primer texto guardado en el editor.");
    invocador.ejecutarComando(cmd1);
    // Comando 2: Guardar segundo texto
    Comando *cmd2 = new GuardarCommand(&editor, "Ahora cambiamos el texto por una nueva versión.");
    invocador.ejecutarComando(cmd2);
    // Deshacer (vuelve al estado del cmd1)
    invocador.deshacerUltimo();
    // Deshacer (vuelve al estado inicial, vacío)
    invocador.deshacerUltimo();
    // Intento de deshacer con historial vacío
    invocador.deshacerUltimo();
    return 0;
}

/*
// 1. Interfaz de Estrategia
class EstrategiaOrdenamiento
{
public:
    virtual void ordenar(vector<int> &data) = 0;
    virtual ~EstrategiaOrdenamiento() = default;
};
// 2. Estrategia Concreta: Ordenamiento Burbuja
class OrdenamientoBurbuja : public EstrategiaOrdenamiento
{
public:
    void ordenar(vector<int> &data) override
    {
        int n = data.size();
        for (int i = 0; i < n - 1; ++i)
        {
            for (int j = 0; j < n - i - 1; ++j)
            {
                if (data[j] > data[j + 1])
                {
                    swap(data[j], data[j + 1]);
                }
            }
        }
        cout << " -> Ordenado con Burbuja." << endl;
    }
};
// 2. Estrategia Concreta: Ordenamiento Quicksort
class OrdenamientoQuicksort : public EstrategiaOrdenamiento
{
public:
    void ordenar(vector<int> &data) override
    {
        // Usa la implementación optimizada de la STL (típicamente Quicksort o Introsort)
        sort(data.begin(), data.end());
        cout << " -> Ordenado con Quicksort (std::sort)." << endl;
    }
};
// 3. Contexto
class Contexto
{
private:
    // Puntero a la estrategia actual
    unique_ptr<EstrategiaOrdenamiento> estrategia;

public:
    // El Contexto ahora gestiona la memoria de la Estrategia (opcional pero más seguro)
    Contexto(unique_ptr<EstrategiaOrdenamiento> e) : estrategia(move(e)) {}
    void setEstrategia(unique_ptr<EstrategiaOrdenamiento> e)
    {
        estrategia = move(e);
    }
    void ejecutarOrdenamiento(vector<int> data)
    { // Pasa una copia de los datos
        cout << "Datos iniciales: ";
        for (int val : data)
            cout << val << " ";
        estrategia->ordenar(data);
        cout << "Resultado final: ";
        for (int val : data)
            cout << val << " ";
        cout << endl;
    }
};
int main()
{
    cout << "\n--- DEMOSTRACIÓN DEL PATRÓN STRATEGY ---" << endl;
    vector<int> datos_1 = {5, 1, 4, 2, 8};
    vector<int> datos_2 = {9, 3, 7, 6, 0};
    // 1. Crear Contexto con Estrategia Burbuja
    Contexto ctx(make_unique<OrdenamientoBurbuja>());
    ctx.ejecutarOrdenamiento(datos_1);
    // 2. Cambiar a Estrategia Quicksort en tiempo de ejecución
    ctx.setEstrategia(make_unique<OrdenamientoQuicksort>());
    ctx.ejecutarOrdenamiento(datos_2);
    return 0;
}*/

/*
// Patron Observer notChat
// Declaración anticipada
class Observador;
// 1. Interfaz Sujeto (Observable)
class Sujeto
{
public:
    virtual void adjuntar(Observador *observador) = 0;
    virtual void notificar(const string &mensaje) = 0;
    virtual ~Sujeto() = default;
};
// 2. Interfaz Observador
class Observador
{
public:
    virtual void actualizar(const string &mensaje) = 0;
    virtual ~Observador() = default;
};
// 3. Sujeto Concreto: Sala de Chat
class SalaDeChat : public Sujeto
{
private:
    // Almacena punteros a los observadores
    vector<Observador *> observadores;

public:
    void adjuntar(Observador *observador) override
    {
        observadores.push_back(observador);
        cout << "Sistema: Nuevo usuario registrado." << endl;
    }
    void notificar(const string &mensaje) override
    {
        cout << "\n--- SALA DE CHAT - Nuevo Mensaje: '" << mensaje << "' ---" << endl;
        for (Observador *obs : observadores)
        {
            obs->actualizar(mensaje);
        }
    }
};
// 4. Observador Concreto: Usuario
class Usuario : public Observador
{
private:
    string nombre;

public:
    Usuario(const string &n) : nombre(n) {}
    void actualizar(const string &mensaje) override
    {
        cout << "[" << nombre << "]: Nuevo mensaje recibido: '" << mensaje << "'" << endl;
    }
};
int main()
{
    cout << "--- DEMOSTRACIÓN DEL PATRÓN OBSERVER ---" << endl;
    // 1. Crear Sala (Sujeto)
    SalaDeChat *sala = new SalaDeChat();
    // 2. Crear Usuarios (Observadores)
    Usuario *alice = new Usuario("Alice");
    Usuario *bob = new Usuario("Bob");
    // 3. Adjuntar
    sala->adjuntar(alice);
    sala->adjuntar(bob);
    // 4. Notificar a todos los usuarios registrados
    sala->notificar("¡Hola a todos! Mañana hay clases.");
    sala->notificar("¿Hay práctica de POO?");
    // Limpieza de memoria
    delete sala;
    delete alice;
    delete bob;
    return 0;
}*/

/*
// Composite carpeta y archivos
// 1. Componente Base
class ComponenteSistema
{
protected:
    string nombre;
    int tamano; // Tamaño en KB
public:
    ComponenteSistema(const string &n, int t) : nombre(n), tamano(t) {}
    virtual ~ComponenteSistema() = default;
    virtual void mostrar(int nivel_indentacion = 0) const = 0;
    virtual int obtenerTamanoTotal() const = 0;
    // Método para Composite (si es una hoja, no hace nada)
    virtual void agregar(ComponenteSistema *componente) {}
};
// 2. Hoja (Archivos)
class Archivo : public ComponenteSistema
{
public:
    Archivo(const string &n, int t) : ComponenteSistema(n, t) {}
    void mostrar(int nivel_indentacion) const override
    {
        cout << string(nivel_indentacion * 2, ' ') << "📄 " << nombre << " (" << tamano << "KB)" << endl;
    }
    int obtenerTamanoTotal() const override
    {
        return tamano;
    }
};
// 3. Compuesto (Carpeta)
class Carpeta : public ComponenteSistema
{
private:
    vector<unique_ptr<ComponenteSistema>> hijos;

public:
    Carpeta(const string &n) : ComponenteSistema(n, 0) {}
    void agregar(ComponenteSistema *componente) override
    {
        hijos.push_back(unique_ptr<ComponenteSistema>(componente));
    }
    void mostrar(int nivel_indentacion) const override
    {
        cout << string(nivel_indentacion * 2, ' ') << "📁 " << nombre << " (" << obtenerTamanoTotal() << "KB total)" << endl;
        for (const auto &hijo : hijos)
        {
            hijo->mostrar(nivel_indentacion + 1);
        }
    }
    int obtenerTamanoTotal() const override
    {
        int tamano_hijos = 0;
        for (const auto &hijo : hijos)
        {
            tamano_hijos += hijo->obtenerTamanoTotal();
        }
        return tamano_hijos;
    }
};
int main()
{
    cout << "--- Prueba de Patrón Composite (C++) ---" << endl;
    // Crear el nodo raíz
    Carpeta *raiz = new Carpeta("ProyectoPOO");
    // Crear subcarpetas
    Carpeta *src = new Carpeta("src");
    Carpeta *docs = new Carpeta("docs");
    // Crear archivos
    Archivo *readme = new Archivo("README.md", 5);
    Archivo *main = new Archivo("main.cpp", 20);
    Archivo *config = new Archivo("config.ini", 3);
    Archivo *informe = new Archivo("informe.pdf", 50);
    // Ensamblar la estructura:
    // Raiz -> README, src, docs
    raiz->agregar(readme);
    raiz->agregar(src);
    raiz->agregar(docs);
    // src -> main.cpp, config.ini
    src->agregar(main);
    src->agregar(config);
    // docs -> informe.pdf
    docs->agregar(informe);
    // Mostrar y calcular el tamaño total
    raiz->mostrar(0);
    // La memoria es gestionada por unique_ptr en la Carpeta, pero la raíz debe ser eliminada
    delete raiz;
    return 0;
}*/

/*
// Patron decorator
// 1. Componente Base (Interfaz de la función matemática)
class ComponenteMatematico
{
public:
    virtual double calcular(double a, double b) = 0;
    virtual ~ComponenteMatematico() = default;
};
// 2. Componente Concreto (Implementación base)
class Division : public ComponenteMatematico
{
public:
    double calcular(double a, double b) override
    {
        if (b == 0)
        {
            throw runtime_error("Error: División por cero.");
        }
        return a / b;
    }
};
// 3. Decorator Base
class DecoradorBase : public ComponenteMatematico
{
protected:
    ComponenteMatematico *componente;

public:
    DecoradorBase(ComponenteMatematico *comp) : componente(comp) {}
    // Delega la operación, manteniendo la interfaz
    double calcular(double a, double b) override
    {
        return componente->calcular(a, b);
    }
};
// 4. Decorator Concreto: Validación de Positivos
class DecoradorValidacionPositivos : public DecoradorBase
{
public:
    DecoradorValidacionPositivos(ComponenteMatematico *comp) : DecoradorBase(comp) {}
    double calcular(double a, double b) override
    {
        if (a <= 0 || b <= 0)
        {
            throw invalid_argument("Error de Decorator: Los argumentos deben ser positivos.");
        }
        // Si la validación es correcta, llama a la operación base
        return DecoradorBase::calcular(a, b);
    }
};
int main()
{
    cout << "--- Prueba de Patrón Decorator (C++) ---" << endl;
    // Componente base: División
    Division division_basica;
    // Decorador: añade la validación de positivos a la división
    DecoradorValidacionPositivos division_decorada(&division_basica);
    try
    {
        // Caso OK
        cout << "Dividir(10.0, 2.0): " << division_decorada.calcular(10.0, 2.0) << endl;
        // Caso Fallo (Validación Decorator)
        cout << "Dividir(10.0, -2.0): ";
        division_decorada.calcular(10.0, -2.0);
    }
    catch (const invalid_argument &e)
    {
        cout << e.what() << endl;
    }
    catch (const runtime_error &e)
    {
        cout << e.what() << endl;
    }
    return 0;
}*/

/*
// Patron adadpter en c++
// 1. Interfaz Target (Lo que el cliente espera)
class Pagos
{
public:
    virtual string pagarEnSoles() = 0;
    virtual ~Pagos() = default;
};
// 2. Clase a Adaptar (Adaptee)
class SistemaPagosDolares
{
private:
    double cantidadDolares;

public:
    SistemaPagosDolares(double dolares) : cantidadDolares(dolares) {}
    double getMontoDolares() const
    {
        return cantidadDolares;
    }
    string procesarDolares() const
    {
        return "Monto original procesado en USD.";
    }
};
// 3. Adaptador
class AdaptadorPagos : public Pagos
{
private:
    SistemaPagosDolares *sistemaDolares;
    const double TIPO_CAMBIO = 3.80; // 1 USD = 3.80 PEN
public:
    AdaptadorPagos(SistemaPagosDolares *adaptee) : sistemaDolares(adaptee) {}
    string pagarEnSoles() override
    {
        double dolares = sistemaDolares->getMontoDolares();
        double soles = dolares * TIPO_CAMBIO;
        // Formateo del resultado
        stringstream ss;
        ss << fixed << setprecision(2) << soles;
        cout << "Convirtiendo: " << fixed << setprecision(2) << dolares << " USD * " << TIPO_CAMBIO << "..." << endl;
        return "Pago procesado: S/. " + ss.str() + " (Moneda Nacional).";
    }
};
int main()
{
    cout << "--- Prueba de Patrón Adapter (C++) ---" << endl;
    double monto_usd = 50.00;
    // Adaptee
    SistemaPagosDolares sistema_dolares(monto_usd);
    // Adaptador (se pasa el puntero del Adaptee)
    AdaptadorPagos adaptador(&sistema_dolares);
    // El cliente llama al método Target (pagarEnSoles)
    cout << adaptador.pagarEnSoles() << endl;
    return 0;
}*/