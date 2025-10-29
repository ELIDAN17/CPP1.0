#include <iostream>  // Para operaciones de entrada y salida (cout)
#include <string>    // Para usar cadenas
#include <sstream>   // Para construir cadenas de texto con datos formateados
#include <iomanip>   // Para formatear la salida numérica (setprecision)
using namespace std; // Usar el espacio de nombres estándar para evitar escribir std::
#include <stdexcept> // Importa la biblioteca para usar excepciones estándar
#include <vector>    // Para usar std::vector (contenedor de hijos)
#include <memory>    // Para usar std::unique_ptr (gestión de memoria segura)
#include <algorithm>
#include <memory> // Para usar unique_ptr

class Observador;
class Sujeto
{
public:
    virtual void registrar(Observador *o) = 0;
    virtual void notificar(const string &mensaje) = 0;
    virtual ~Sujeto() = default;
};

class Observador
{
public:
    virtual void actualizar(const string &mensaje) = 0;
    virtual ~Observador() = default;
};
class SujetoConcreto : public Sujeto
{
private:
    vector<Observador *> obs;

public:
    void registrar(Observador *o) override
    {
        obs.push_back(o);
        cout << "Sistema: Observador registrado." << endl;
    }
    void notificar(const string &mensaje) override
    {
        cout << "\n--- Sujeto Notificando: " << mensaje << " ---" << endl;
        for (Observador *o : obs)
        {
            o->actualizar(mensaje);
        }
    }
};
class ObservadorConcreto : public Observador
{
public:
    void actualizar(const string &mensaje) override
    {
        cout << "Notificado: " << mensaje << endl;
    }
};

int main()
{
    SujetoConcreto *s = new SujetoConcreto();
    ObservadorConcreto *o1 = new ObservadorConcreto();
    ObservadorConcreto *o2 = new ObservadorConcreto();
    s->registrar(o1);
    s->registrar(o2);
    s->notificar("Se actualizó el sistema.");
    delete s;
    delete o1;
    delete o2;
    return 0;
}

/*
// Patron  command  editor de texto
// 1. (Receiver): Objeto que realiza la acción real
class EditorDeTexto
{
private:
    string contenido;
public:
    EditorDeTexto() : contenido("") {}
    void guardar(const string &nuevo_contenido)
    {
        contenido = nuevo_contenido;
        cout << "Editor: Contenido guardado." << endl;
    }
    void cargar(const string &contenido_anterior)
    {
        contenido = contenido_anterior; // Carga el estado anterior (función de Deshacer)
        cout << "Editor: Contenido deshecho..." << endl;
    }

    string getContenido() const
    {
        return contenido; // Devuelve el estado actual (usado para capturar el estado anterior)
    }
};

// 2. Interfaz Command
class Comando
{
public:
    virtual void ejecutar() = 0; // Ejecuta la acción
    virtual void deshacer() = 0; // Revierte la acción
    virtual ~Comando() = default;
};

// 3. Comando Concreto: Guardar
class GuardarCommand : public Comando
{
private:
    EditorDeTexto *editor;
    string nuevo_contenido;
    string contenido_anterior; // Estado necesario para el Deshacer

public:
    GuardarCommand(EditorDeTexto *e, const string &nuevo)
        : editor(e), nuevo_contenido(nuevo), contenido_anterior(e->getContenido()) {} // Captura el estado ANTES de ejecutar

    void ejecutar() override
    {
        editor->guardar(nuevo_contenido); // Llama a la acción en el Receptor
    }

    void deshacer() override
    {
        editor->cargar(contenido_anterior); // Revierte usando el estado guardado
    }
};

// 4. Invocador: Almacena el historial y gestiona la ejecución
class Invocador
{
private:
    vector<unique_ptr<Comando>> historial; // Lista de comandos ejecutados (historial)

public:
    void ejecutarComando(Comando *comando)
    {
        cout << "\nEjecutando comando..." << endl;
        comando->ejecutar();
        historial.push_back(unique_ptr<Comando>(comando)); // Añade el comando al historial para posible deshacer
    }

    void deshacerUltimo()
    {
        if (!historial.empty())
        {
            cout << "\nDeshaciendo comando..." << endl;
            historial.back()->deshacer();
            historial.pop_back(); // Elimina el comando que acaba de ser deshecho
        }
        else
        {
            cout << "\nHistorial vacío. Nada que deshacer." << endl;
        }
    }
};
// Función de demostración para el patrón Command
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
}*/

/*
// Patron strategy Algor order
// 1. Interfaz de Estrategia
class EstrategiaOrdenamiento
{
public:
    virtual void ordenar(vector<int> &data) = 0; // Interfaz común para todos los algoritmos
    virtual ~EstrategiaOrdenamiento() = default;
};

// 2. Estrategia Concreta: Burbuja
class OrdenamientoBurbuja : public EstrategiaOrdenamiento
{
public:
    void ordenar(vector<int> &data) override
    {
        // ... (Implementación de Burbuja)
        cout << " -> Ordenado con Burbuja." << endl;
    }
};

// 2. Estrategia Concreta: Quicksort
class OrdenamientoQuicksort : public EstrategiaOrdenamiento
{
public:
    void ordenar(vector<int> &data) override
    {
        sort(data.begin(), data.end()); // Uso de std::sort (algoritmo eficiente)
        cout << " -> Ordenado con Quicksort (std::sort)." << endl;
    }
};

// 3. Contexto
class Contexto
{
private:
    unique_ptr<EstrategiaOrdenamiento> estrategia; // Referencia a la estrategia actual (único dueño)

public:
    // Constructor que inicializa el Contexto con una estrategia inicial
    Contexto(unique_ptr<EstrategiaOrdenamiento> e) : estrategia(move(e)) {}

    void setEstrategia(unique_ptr<EstrategiaOrdenamiento> e)
    {
        estrategia = move(e); // Permite cambiar el algoritmo en tiempo de ejecución
    }

    void ejecutarOrdenamiento(vector<int> data)
    {
        cout << "Datos iniciales: ";
        for (int val : data)
            cout << val << " ";

        estrategia->ordenar(data); // El Contexto delega el trabajo a la estrategia actual
    }
};
// Función de demostración para el patrón Strategy
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
// Patron observer notChat
// Declaración anticipada de la clase Observador para evitar errores de referencia circular
class Observador;

// 1. Interfaz Sujeto (Observable)
class Sujeto
{
public:
    virtual void adjuntar(Observador *observador) = 0; // Registrar observador
    virtual void notificar(const string &mensaje) = 0; // Iniciar la notificación
    virtual ~Sujeto() = default;
};

// 2. Interfaz Observador
class Observador
{
public:
    virtual void actualizar(const string &mensaje) = 0; // Recibir la actualización del Sujeto
    virtual ~Observador() = default;
};

// 3. Sujeto Concreto: Sala de Chat
class SalaDeChat : public Sujeto
{
private:
    vector<Observador *> observadores; // Lista de observadores registrados

public:
    void adjuntar(Observador *observador) override
    {
        observadores.push_back(observador); // Agrega el puntero del observador al vector
        cout << "Sistema: Nuevo usuario registrado." << endl;
    }

    void notificar(const string &mensaje) override
    {
        cout << "\n--- SALA DE CHAT - Nuevo Mensaje: '" << mensaje << "' ---" << endl;
        for (Observador *obs : observadores)
        {
            obs->actualizar(mensaje); // Itera y llama al método actualizar() de cada observador
        }
    }
};

// 4. Observador Concreto: Usuario
class Usuario : public Observador
{
private:
    string nombre;

public:
    Usuario(const string &n) : nombre(n) {} // Constructor

    void actualizar(const string &mensaje) override
    {
        cout << "[" << nombre << "]: Nuevo mensaje recibido: '" << mensaje << "'" << endl; // Acción específica al ser notificado
    }
};
// Función de demostración para el patrón Observer
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
// patron composite archivos y carpetas
// 1. Componente Base (Interfaz común para Archivos y Carpetas)
class ComponenteSistema
{
protected:
    string nombre;
    int tamano;

public:
    ComponenteSistema(const string &n, int t) : nombre(n), tamano(t) {}
    virtual ~ComponenteSistema() = default;

    virtual void mostrar(int nivel_indentacion = 0) const = 0; // Muestra el elemento y su contenido
    virtual int obtenerTamanoTotal() const = 0;                // Obtiene el tamaño

    virtual void agregar(ComponenteSistema *componente) {} // Método de gestión de hijos (vacío por defecto, solo Compuesto lo implementa)
};

// 2. Hoja (Archivos)
class Archivo : public ComponenteSistema
{ // Es una hoja, no tiene hijos
public:
    Archivo(const string &n, int t) : ComponenteSistema(n, t) {}

    void mostrar(int nivel_indentacion) const override
    {
        // Muestra el archivo. La función no es recursiva.
        cout << string(nivel_indentacion * 2, ' ') << "📄 " << nombre << " (" << tamano << "KB)" << endl;
    }

    int obtenerTamanoTotal() const override
    {
        return tamano; // Devuelve su propio tamaño
    }
};

// 3. Compuesto (Carpeta)
class Carpeta : public ComponenteSistema
{ // Es un compuesto, puede tener hijos
private:
    vector<unique_ptr<ComponenteSistema>> hijos; // Contenedor para otros Componentes (Archivos o Carpetas)

public:
    Carpeta(const string &n) : ComponenteSistema(n, 0) {}

    void agregar(ComponenteSistema *componente) override
    {
        hijos.push_back(unique_ptr<ComponenteSistema>(componente)); // Añade un Componente a la lista de hijos
    }

    void mostrar(int nivel_indentacion) const override
    {
        // Muestra el nombre de la carpeta
        cout << string(nivel_indentacion * 2, ' ') << "📁 " << nombre << " (" << obtenerTamanoTotal() << "KB total)" << endl;
        for (const auto &hijo : hijos)
        {
            hijo->mostrar(nivel_indentacion + 1); // Llamada recursiva: el Compuesto delega la operación a sus hijos
        }
    }

    int obtenerTamanoTotal() const override
    {
        int tamano_hijos = 0;
        for (const auto &hijo : hijos)
        {
            tamano_hijos += hijo->obtenerTamanoTotal(); // Acumula recursivamente el tamaño de los hijos
        }
        return tamano_hijos;
    }
};
// Función de demostración para el patrón Composite
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
// patron decorator validacion matematica
// 1. Componente Base (Interfaz común para la función matemática)
class ComponenteMatematico
{
public:
    virtual double calcular(double a, double b) = 0; // Método de operación (el mismo para el Decorator)
    virtual ~ComponenteMatematico() = default;
};

// 2. Componente Concreto (Implementación base sin validaciones extra)
class Division : public ComponenteMatematico
{
public:
    double calcular(double a, double b) override
    {
        if (b == 0)
        {
            throw runtime_error("Error: División por cero."); // Verifica el caso de error de la lógica base
        }
        return a / b; // Realiza la operación original
    }
};

// 3. Decorator Base (Mantiene una referencia al Componente)
class DecoradorBase : public ComponenteMatematico
{
protected:
    ComponenteMatematico *componente; // Referencia al objeto envuelto (el Componente que estamos decorando)

public:
    // Constructor que recibe y almacena el objeto a decorar
    DecoradorBase(ComponenteMatematico *comp) : componente(comp) {}

    // Método por defecto: delega la ejecución al objeto envuelto
    double calcular(double a, double b) override
    {
        return componente->calcular(a, b);
    }
};

// 4. Decorator Concreto: Validación de Positivos (Añade funcionalidad)
class DecoradorValidacionPositivos : public DecoradorBase
{
public:
    DecoradorValidacionPositivos(ComponenteMatematico *comp) : DecoradorBase(comp) {} // Constructor que llama al constructor base

    double calcular(double a, double b) override
    {
        if (a <= 0 || b <= 0)
        {
            throw invalid_argument("Error de Decorator: Los argumentos deben ser positivos."); // Lógica añadida por el Decorator (Validación)
        }
        // Si la validación es correcta, llama al cálculo del objeto envuelto (pasando la prueba)
        return DecoradorBase::calcular(a, b);
    }
};
// Función de demostración para el patrón Decorator
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
// Patron Adapter conversion de pagos
// 1. Interfaz Target (Lo que el cliente espera)
class Pagos
{
public:
    virtual string pagarEnSoles() = 0; // Método que el cliente llama (Target)
    virtual ~Pagos() = default;        // Destructor virtual por defecto
};

// 2. Clase a Adaptar (Adaptee)
class SistemaPagosDolares
{
private:
    double cantidadDolares; // El Adaptee solo entiende dólares

public:
    SistemaPagosDolares(double dolares) : cantidadDolares(dolares) {} // Constructor

    double getMontoDolares() const
    {
        return cantidadDolares; // Devuelve el monto original en dólares
    }
};

// 3. Adaptador
class AdaptadorPagos : public Pagos
{ // Hereda de Pagos (Target)
private:
    SistemaPagosDolares *sistemaDolares; // Contiene una referencia al Adaptee
    const double TIPO_CAMBIO = 3.80;     // Constante de conversión

public:
    AdaptadorPagos(SistemaPagosDolares *adaptee) : sistemaDolares(adaptee) {} // Constructor

    string pagarEnSoles() override
    {                                                       // Implementa el método Target
        double dolares = sistemaDolares->getMontoDolares(); // Llama al Adaptee
        double soles = dolares * TIPO_CAMBIO;               // Realiza la conversión (Adaptación)

        // Formatea la salida para mostrar dos decimales
        stringstream ss;
        ss << fixed << setprecision(2) << soles;

        cout << "Convirtiendo: " << fixed << setprecision(2) << dolares << " USD * " << TIPO_CAMBIO << "..." << endl;
        return "Pago procesado: S/. " + ss.str() + " (Moneda Nacional).";
    }
};

int main()
{
    cout << "\n--- DEMOSTRACIÓN DEL PATRÓN ADAPTER ---" << endl;
    double monto_usd = 100.00;

    SistemaPagosDolares sistema_dolares(monto_usd); // Crea el Adaptee
    AdaptadorPagos adaptador(&sistema_dolares);     // Crea el Adaptador

    // El cliente llama a la interfaz Target esperada
    cout << adaptador.pagarEnSoles() << endl;
    return 0;
}*/