#include <iostream>  // biblioteca para entrada y salida.
#include <iomanip>   // biblioteca para manipulacion de formato de salida.
#include <sstream>   // biblioteca para flujos de cadenas.
#include <stdexcept> // biblioteca para excepciones estandar, como invalid_argument.
using namespace std; // 'std' para evitar escribir 'std::' repetidamente.
class Time
{
public:
    Time() = default; // Constructor por defecto.
    // Constructor con parametros. Llama al metodo 'set()' para validar e inicializar.
    Time(int hour, int minute, int second) { set(hour, minute, second); }
    // Observadores (getters): metodos para obtener los valores de los atributos.
    int hour() const noexcept { return hour_; }     // 'const' garantiza que no modifica el objeto.
    int minute() const noexcept { return minute_; } //'noexcept' indica que no lanza excepciones.
    int second() const noexcept { return second_; }
    // Modificadores (setters): metodos para cambiar los valores de los atributos.
    void hour(int h)
    {
        validate(h, minute_, second_); // Valida el nuevo valor de la hora junto con los minutos y segundos.
        hour_ = h;                     // Asigna el nuevo valor si la validacion es exitosa.
    }
    void minute(int m)
    {
        validate(hour_, m, second_); // Valida el nuevo valor de los minutos.
        minute_ = m;
    }
    void second(int s)
    {
        validate(hour_, minute_, s); // Valida el nuevo valor de los segundos.
        second_ = s;
    }
    // Metodo 'set()' para modificar los tres atributos a la vez.
    void set(int h, int m, int s)
    {
        validate(h, m, s); // Llama al metodo de validacion con los tres nuevos valores.
        hour_ = h;         // Asigna los nuevos valores solo si la validacion pasa.
        minute_ = m;
        second_ = s;
    }
    // Metodo para convertir la hora a formato militar (HH:MM).
    string toMilitary() const
    {
        ostringstream os;                             // Crea un flujo de cadena en memoria.
        os << setw(2) << setfill('0') << hour_ << ':' // Establece el ancho a 2 y rellena con '0', luego inserta la hora y un ':'.
           << setw(2) << setfill('0') << minute_;     // Realiza lo mismo para los minutos.
        return os.str();                              // Devuelve la cadena final del flujo.
    }
    // Metodo para convertir la hora a formato estandar (h:MM:SS AM/PM).
    string toStandard() const
    {
        // Usa el operador ternario para calcular la hora en formato de 12 horas.
        const int h12 = (hour_ == 0 || hour_ == 12) ? 12 : hour_ % 12;
        // Usa el operador ternario para determinar si es "AM" o "PM".
        const char *ampm = (hour_ < 12) ? "AM" : "PM";
        ostringstream os;
        os << h12 << ':'
           << setw(2) << setfill('0') << minute_ << ':'
           << setw(2) << setfill('0') << second_ << ' ' << ampm;
        return os.str();
    }

private:
    int hour_{0}, minute_{0}, second_{0}; // Atributos de la hora, minuto y segundo en 0.
    // Metodo estatico para validar si los valores estan en el rango correcto.
    static void validate(int h, int m, int s)
    {
        if (h < 0 || h > 23)
            throw invalid_argument("hour out of range[0,23]"); // Lanza una excepcion si la hora es invalida.
        if (m < 0 || m > 59)
            throw invalid_argument("minute out of range [0,59]");
        if (s < 0 || s > 59)
            throw invalid_argument("second out ofrange [0,59]");
    }
};

int main() // La funcion principal
{
    try // Inicia un bloque 'try' para manejar posibles excepciones.
    {
        Time t1(18, 30, 0); // Crea un objeto 'Time' con valores validos.
        // Imprime la hora en formatos militar y estandar.
        cout << t1.toMilitary() << " | " << t1.toStandard() << '\n';
        Time t2;      // Crea un objeto 'Time' usando el constructor por defecto (00:00:00).
        t2.minute(5); // Modifica el minuto. El 'setter' valida el valor.
        t2.second(7); // Modifica el segundo.
        cout << t2.toMilitary() << " | " << t2.toStandard() << '\n';
        // Prueba invalida (descomentar para verificar excepcion):
        // Time bad(29, 73, 0);
    }
    catch (const exception &ex) // Captura cualquier excepcion lanzada en el bloque 'try'.
    {
        cerr << "Error: " << ex.what() << '\n'; // Imprime un mensaje de error en la salida.
        return 1;                               // Retorna 1 para indicar que el programa termino con un error.
    }
    return 0; // Retorna 0 para indicar que el programa termino con exito.
}

/*
#include <iostream>
#include <iomanip>   // manipulacion de formato de salida
#include <sstream>   // flujo de cadena
#include <stdexcept> // excepciones estándar
using namespace std;
class Time
{
public:
    Time() = default;
    Time(int hour, int minute, int second) { set(hour, minute, second); }

    // Observadores get
    int hour() const noexcept { return hour_; }
    int minute() const noexcept { return minute_; }
    int second() const noexcept { return second_; }
    // Modificadores (validación estricta)
    void hour(int h)
    {
        validate(h, minute_, second_);
        hour_ = h;
    }
    void minute(int m)
    {
        validate(hour_, m, second_);
        minute_ = m;
    }
    void second(int s)
    {
        validate(hour_, minute_, s);
        second_ = s;
    }
    void set(int h, int m, int s)
    {
        validate(h, m, s);
        hour_ = h;
        minute_ = m;
        second_ = s;
    }
    string toMilitary() const
    {
        ostringstream os; // object memory
        os << setw(2) << setfill('0') << hour_ << ':'
           << setw(2) << setfill('0') << minute_;
        return os.str();
    }
    string toStandard() const
    {
        const int h12 = (hour_ == 0 || hour_ == 12) ? 12 : hour_ % 12;
        const char *ampm = (hour_ < 12) ? "AM" : "PM";
        ostringstream os;
        os << h12 << ':'
           << setw(2) << setfill('0') << minute_ << ':'
           << setw(2) << setfill('0') << second_ << ' ' << ampm;
        return os.str();
    }

private:
    int hour_{0}, minute_{0}, second_{0};
    static void validate(int h, int m, int s)
    {
        if (h < 0 || h > 23)
            throw invalid_argument("hour out of range[0,23]");
        if (m < 0 || m > 59)
            throw invalid_argument("minute out of range [0,59]");
        if (s < 0 || s > 59)
            throw invalid_argument("second out ofrange [0,59]");
    }
};
int main()
{
    try
    {
        Time t1(18, 30, 0);
        cout << t1.toMilitary() << " | " << t1.toStandard() << '\n';
        Time t2; // 00:00:00
        t2.minute(5);
        t2.second(7);
        cout << t2.toMilitary() << " | " << t2.toStandard() << '\n';
        // Prueba inválida (descomentar para verificar excepción):
        // Time bad(29, 73, 0);
    }
    catch (const exception &ex)
    {
        cerr << "Error: " << ex.what() << '\n';
        return 1;
    }
    return 0;
}
*/