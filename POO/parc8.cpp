

/* // ejercicio 8.4
#include <iostream>
using namespace std;
struct monomio
{
    char car;
    float coef;
    float exp;
    monomio() {}
    monomio(char c, float ce, float ex)
    {
        car = c;
        coef = ce;
        exp = ex;
    }
};
class Polinomio
{
private:
    monomio *mon;
    int n;
    int size;

public:
    Polinomio()
    {
        size = 10;
        mon = new monomio[size];
        n = 0;
    }
    void add(char c, float ce, float ex)
    {
        if (n < size)
        {
            mon[n++] = monomio(c, ce, ex);
        }
    }
    Polinomio(const Polinomio &p)
    {
        size = p.size;
        n = p.n;
        mon = new monomio[size];
        for (int i = 0; i < n; i++)
        {
            mon[i] = p.mon[i];
        }
    }
    Polinomio operator=(const Polinomio &p)
    {
        if (this != &p)
        {
            delete[] mon;
            size = p.size;
            n = p.n;
            mon = new monomio[size];
            for (int i = 0; i < n; i++)
            {
                mon[i] = p.mon[i];
            }
        }
        return *this;
    }
    Polinomio operator+(const Polinomio &p)
    {
        Polinomio res;
        for (int i = 0; i < n; i++)
            res.add(mon[i].car, mon[i].coef, mon[i].exp);
        for (int i = 0; i < p.n; i++)
            res.add(p.mon[i].car, p.mon[i].coef, p.mon[i].exp);
        return res;
    }
    Polinomio operator-(const Polinomio &p)
    {
        Polinomio res;
        for (int i = 0; i < n; i++)
            res.add(mon[i].car, mon[i].coef, mon[i].exp);
        for (int i = 0; i < p.n; i++)
            res.add(p.mon[i].car, -p.mon[i].coef, p.mon[i].exp);
        return res;
    }
    Polinomio operator*(const Polinomio &p)
    {
        Polinomio res;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < p.n; j++)
            {
                char c = mon[i].car;
                float ce = mon[i].coef * p.mon[j].coef;
                float ex = mon[i].exp + p.mon[j].exp;
                res.add(c, ce, ex);
            }
        }
        return res;
    }
    Polinomio operator/(const Polinomio &p)
    {
        Polinomio res;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < p.n; j++)
            {
                char c = mon[i].car;
                float ce = mon[i].coef / p.mon[j].coef;
                float ex = mon[i].exp - p.mon[j].exp;
                res.add(c, ce, ex);
            }
        }
        return res;
    }
    bool operator==(const Polinomio &p)
    {
        if (n != p.n)
            return false;
        for (int i = 0; i < n; i++)
        {
            if (mon[i].coef != p.mon[i].coef || mon[i].exp != p.mon[i].exp)
                return false;
        }
        return true;
    }
    bool operator!=(const Polinomio &p)
    {
        return !(*this == p);
    }
    void print()
    {
        for (int i = 0; i < n; i++)
        {
            cout << mon[i].coef << mon[i].car << "^" << mon[i].exp;
            if (i < n - 1)
                cout << " + ";
        }
        cout << endl;
    }
    friend void print(const Polinomio &p)
    {
        for (int i = 0; i < p.n; i++)
        {
            cout << p.mon[i].coef << p.mon[i].car << "^" << p.mon[i].exp;
            if (i < p.n - 1)
                cout << " + ";
        }
        cout << endl;
    }
    ~Polinomio()
    {
        delete[] mon;
    }
};
int main()
{
    Polinomio p1, p2;
    p1.add('x', 2, 3);
    p1.add('x', 1, 1);
    p2.add('x', 3, 2);
    p2.add('x', 4, 0);
    Polinomio suma = p1 + p2;
    Polinomio resta = p1 - p2;
    Polinomio producto = p1 * p2;
    Polinomio division = p1 / p2;
    cout << "P1: ";
    p1.print();
    cout << "P2: ";
    p2.print();
    cout << "Suma: ";
    suma.print();
    cout << "Resta: ";
    resta.print();
    cout << "Producto: ";
    producto.print();
    cout << "Division: ";
    division.print();
    cout << "¿P1 y P2 son iguales? " << (p1 == p2 ? "Sí" : "No") << endl;
    return 0;
}*/

/* // ejercicio 8.3
#include <iostream>
using namespace std;
class Ascensor
{
private:
    int pisoActual;
    int numPisos;
    int capacidad;

public:
    Ascensor(int piso = 0, int pisos = 5, int cap = 4)
        : pisoActual(piso), numPisos(pisos), capacidad(cap) {}
    void mostrar() const
    {
        cout << "Piso actual: " << pisoActual
             << ", Pisos totales: " << numPisos
             << ", Capacidad: " << capacidad << endl;
    }
    // Operador ++ para subir un piso
    Ascensor &operator++()
    {
        if (pisoActual < numPisos)
            pisoActual++;
        return *this;
    }
    // Operador -- para bajar un piso
    Ascensor &operator--()
    {
        if (pisoActual > 0)
            pisoActual--;
        return *this;
    }
    // Operador ==
    bool operator==(const Ascensor &otro) const
    {
        return (numPisos == otro.numPisos && capacidad == otro.capacidad);
    }
    // Operador !=
    bool operator!=(const Ascensor &otro) const
    {
        return !(*this == otro);
    }
};
int main()
{
    Ascensor a(2, 5, 4);
    Ascensor b(3, 5, 4);
    Ascensor c(1, 6, 3);
    ++a;
    --b;
    cout << "Ascensor A: ";
    a.mostrar();
    cout << "Ascensor B: ";
    b.mostrar();
    cout << "¿A y B son iguales? " << (a == b ? "Sí" : "No") << endl;
    cout << "¿A y C son diferentes? " << (a != c ? "Sí" : "No") << endl;
    return 0;
}*/

/* // ejercicio 8.2
#include <iostream>
using namespace std;
class Complex
{
private:
    double real;
    double imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}
    void mostrar() const
    {
        cout << real << " + " << imag << "i" << endl;
    }
    // Operadores amigos
    friend Complex operator-(const Complex &a, const Complex &b);
    friend Complex operator*(const Complex &a, const Complex &b);
    friend Complex operator/(const Complex &a, const Complex &b);
};
// Resta
Complex operator-(const Complex &a, const Complex &b)
{
    return Complex(a.real - b.real, a.imag - b.imag);
}
// Producto
Complex operator*(const Complex &a, const Complex &b)
{
    return Complex(a.real * b.real - a.imag * b.imag,
                   a.real * b.imag + a.imag * b.real);
}
// División
Complex operator/(const Complex &a, const Complex &b)
{
    double denom = b.real * b.real + b.imag * b.imag;
    return Complex((a.real * b.real + a.imag * b.imag) / denom,
                   (a.imag * b.real - a.real * b.imag) / denom);
}
int main()
{
    Complex x(5, 3);
    Complex y(2, -1);
    Complex r1 = x - y;
    Complex r2 = x * y;
    Complex r3 = x / y;
    cout << "Resta: ";
    r1.mostrar();
    cout << "Producto: ";
    r2.mostrar();
    cout << "Division: ";
    r3.mostrar();
    return 0;
}*/

/* // ejercicio 8.1
#include <iostream>
using namespace std;
class Complex
{
private:
    double real;
    double imag;

public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}
    // Mostrar el número complejo
    void mostrar() const
    {
        cout << real << " + " << imag << "i" << endl;
    }
    // Operador resta
    Complex operator-(const Complex &c) const
    {
        return Complex(real - c.real, imag - c.imag);
    }
    // Operador producto
    Complex operator*(const Complex &c) const
    {
        return Complex(real * c.real - imag * c.imag,
                       real * c.imag + imag * c.real);
    }
    // Operador división
    Complex operator/(const Complex &c) const
    {
        double denom = c.real * c.real + c.imag * c.imag;
        return Complex((real * c.real + imag * c.imag) / denom,
                       (imag * c.real - real * c.imag) / denom);
    }
};
int main()
{
    Complex a(4, 2);
    Complex b(1, -1);
    Complex r1 = a - b;
    Complex r2 = a * b;
    Complex r3 = a / b;
    cout << "Resta: ";
    r1.mostrar();
    cout << "Producto: ";
    r2.mostrar();
    cout << "Division: ";
    r3.mostrar();
    return 0;
}*/

/* // ejemplo 7
// Clase Arreglo que almacena objetos enteros
#ifndef ARREGLO_1_H
#define ARREGLO_1_H
#include <iostream>
using namespace std;
class Arreglo1
{
    friend ostream &operator<<(ostream &, const Arreglo1 &);
    friend istream &operator>>(istream &, Arreglo1 &);

public:
    Arreglo1(int = 10);         // constructor predeterminado
    Arreglo1(const Arreglo1 &); // constructor de copia
    ~Arreglo1();                // destructor
    int obtenerTamano() const;  // devuelve tamaño del arreglo
    const Arreglo1 &operator=(const Arreglo1 &);
    // Operador de igualdad
    bool operator==(const Arreglo1 &) const;
    // Operador de desigualdad (lo opuesto al operador de igualdad)
    bool operator!=(const Arreglo1 &derecha) const
    {
        return !(*this == derecha); // invoca a Arreglo1::operator==
    } // fin de la funcion operator!=
    // El Operador de subindice[] para objetos no constantes devuelve un lvalue
    int &operator[](int);
    // El Operador de subindice[] para objetos constantes devuelve un rvalue
    const int &operator[](int) const;

private:
    int tamano; // tamaño del arreglo
    int *ptr;   // puntero al primer elemento del arreglo
};
#endif // ARREGLO1_H
#include <iomanip>
#include <cstdlib> // para la funcion exit
#include <conio.h>
// Constructor predeterminado para la clase Arreglo: tamaño predeterminado
Arreglo1::Arreglo1(int tam)
{
    // Valida tamaño del Arreglo
    tamano = (tam > 0 ? tam : 10);
    ptr = new int[tamano]; // crea espacio para el arreglo
    for (int i = 0; i < tamano; i++)
        ptr[i] = 0; // inicializa el arreglo
}
// Constructor de copia para la clase Arreglo: Debe recibir una referencia para
// evitar la llamada repetida al constructor de copia
Arreglo1::Arreglo1(const Arreglo1 &array) : tamano(array.tamano)
{
    ptr = new int[tamano]; // crear espacio para el arreglo
    for (int i = 0; i < tamano; i++)
        ptr[i] = array.ptr[i]; // copiar dentro del objeto
}
// Destructor de la clase Arreglo
Arreglo1::~Arreglo1()
{
    delete[] ptr; // quita o libera el espacio del arreglo
}
int Arreglo1::obtenerTamano() const
{
    return tamano; // fin de la funcion obtenerTamano
}
// Sobrecarga del operador de asignacion
// La devolucion de const evita: (a1 = a3) = a3
const Arreglo1 &Arreglo1::operator=(const Arreglo1 &derecha)
{
    if (&derecha != this)
    { // verifica la autoasignacion
        // si los arreglos de diferentes tamaños, liberar el arreglo original
        // y asignar espacio para el nuevo arreglo por la izquierda
        if (tamano != derecha.tamano)
        {
            delete[] ptr; // libera el espacio
            tamano = derecha.tamano;
            ptr = new int[tamano]; // reinicializa este objeto
        }
        for (int i = 0; i < tamano; i++) // copia el arreglo
            ptr[i] = derecha.ptr[i];
    }
    return *this; // permite la habilita x = y = z
}
// Determina si dos arreglos son iguales o si son devuelve verdadero, de lo
// contrario se devuelve falso
bool Arreglo1::operator==(const Arreglo1 &derecha) const
{
    if (tamano != derecha.tamano) // arreglos de tamaños diferentes
        return false;
    for (int i = 0; i < tamano; i++)
        if (ptr[i] != derecha.ptr[i]) // los arreglos no son iguales
            return false;
    return true; // los arreglos son iguales
}
// Sobrecarga del operador subindice [] para el retorno de referencias a
// arreglos no constantes, crea un lvalue
int &Arreglo1::operator[](int subindice)
{
    // Verifica si existe error en los indices del arreglo
    if (subindice < 0 || subindice >= tamano)
    {
        cout << "\nError: Subindice " << subindice << " fuera de rango!" << endl;
        getch();
        exit(1); // terminar el programa: subindice fuera de rango
    } // fin del if
    return ptr[subindice]; // retorno de la referencia
} // fin de la funcion operator[]
// Sobrecarga del operador subindice [] para el retorno de referencias a
// arreglos constantes, crea un rvalue
const int &Arreglo1::operator[](int subindice) const
{
    // Verifica si existe error en los limites del arreglo
    if (subindice < 0 || subindice >= tamano)
    {
        cout << "\nError: Subindice " << subindice << " fuera de rango!" << endl;
        getch();
        exit(1); // terminar el programa: subindice fuera de rango
    } // fin del if
    return ptr[subindice]; // retorno de una referencia constante
} // fin de la funcion operator[]
// Sobrecarga del operador de entrada >> para la clase Arreglo; introduce
// valores para todo el arreglo
istream &operator>>(istream &entrada, Arreglo1 &a)
{
    for (int i = 0; i < a.tamano; i++)
        entrada >> a.ptr[i];
    return entrada; // habilita cin >> x >> y;
} // fin de la funcion operator>>
// Sobrecarga del operador de salida << para la clase Arreglo; extrae valores
// para todo el arreglo
ostream &operator<<(ostream &salida, const Arreglo1 &a)
{
    int i;
    // Muestra el arreglo privado basado en apuntadores
    for (i = 0; i < a.tamano; i++)
    {
        salida << setw(10) << a.ptr[i];
        if ((i + 1) % 7 == 0) // 4 numeros por fila de salida
            salida << endl;
    } // fin de for
    if (i % 4 != 0)
        salida << endl;
    return salida; // habilita cout << x << y;
} // fin de la funcion operator<<
// Archivo principal.cpp donde se define la funcion main()
// Programa de prueba para la clase Arreglo
int main()
{
    Arreglo1 enteros1(7); // Instanciar arreglo de 7 elementos
    Arreglo1 enteros2;    // Arreglo predeterminado de 10 elementos
    // Imprime el tamaño de enteros1 y su contenido
    cout << "Tamaño de enteros1 es " << enteros1.obtenerTamano()
         << "\nEl arreglo despues de la inicializacion:\n"
         << enteros1;
    // Imprime el tamaño de enteros2 y su contenido
    cout << "\nTamaño de enteros2 es " << enteros2.obtenerTamano()
         << "\nEl arreglo despues de la inicializacion:\n"
         << enteros2;

    // Introduce e imprime enteros1 y enteros2
    cout << "\nIntroduzca 17 enteros:\n";
    cin >> enteros1 >> enteros2;
    cout << "enteros1:\n"
         << enteros1
         << "enteros2:\n"
         << enteros2;
    // Utiliza el operador de desigualdad (!=) sobrecargado
    cout << "Evaluando: enteros1 != enteros2\n";
    if (enteros1 != enteros2)
        cout << "Enteros1 y enteros2 no son iguales\n";
    // Crea el arreglo enteros3 utilizando enteros1 como un inicializador;
    // imprime su tamaño y su contenido
    Arreglo1 enteros3(enteros1); // llama al constructor de copia
    cout << "\nTamaño de enteros3: " << enteros3.obtenerTamano()
         << "\nArreglo después de la inicialización:\n"
         << enteros3;
    // Uso del operador de asignación sobrecargado
    cout << "\nAsignando enteros2 a enteros1:\n";
    enteros1 = enteros2;
    cout << "enteros1:\n"
         << enteros1
         << "enteros2:\n"
         << enteros2;
    // Utiliza el operador de igualdad (==) sobrecargado
    if (enteros1 == enteros2)
        cout << "enteros1 y enteros2 son iguales\n";
    cout << "\nenteros1[5] es " << enteros1[5];
    // uso del operador de subíndice [] sobrecargado
    cout << "\nAsignando 1000 a enteros1[5]\n";
    enteros1[5] = 1000;
    cout << "enteros1:\n"
         << enteros1;
    // intento de usar un subíndice fuera de rango
    cout << "\nIntentando asignar 1000 a enteros1[15]" << endl;
    enteros1[15] = 1000;
    return 0;
}*/

/*
// Archivo Racional.h
#ifndef RACIONAL_H
#define RACIONAL_H
#include <iostream>
#include <assert.h>
using namespace std;
int mcd(int, int); // para el maximo comun divisor
class Racional{
public:
    // constructores
    Racional(int num = 0, int denom = 1);
    Racional(const Racional &);
    // atributos
    int getnum() const { return num; }
    int getdemon() const { return demon; }
    // operadores aritméticos
    Racional operator-(); // menos unario
    friend Racional operator+(const Racional &, const Racional &);
    friend Racional operator-(const Racional &, const Racional &);
    friend Racional operator*(const Racional &, const Racional &);
    friend Racional operator/(const Racional &, const Racional &);
    // operadores de comparación
    friend bool operator==(const Racional &, const Racional &);
    friend bool operator!=(const Racional &, const Racional &);
    friend bool operator<(const Racional &, const Racional &);
    friend bool operator<=(const Racional &, const Racional &);
    friend bool operator>(const Racional &, const Racional &);
    friend bool operator>=(const Racional &, const Racional &);
    // operadores unarios
    Racional &operator++(); // incremento prefijo
    Racional &operator--(); // disminucion prefijo
    // operadores de asignacion
    Racional &operator=(const Racional &);
    Racional &operator+=(const Racional &);
    Racional &operator-=(const Racional &);
    Racional &operator*=(const Racional &);
    Racional &operator/=(const Racional &);
    // entrada salida
    void print();
    friend ostream &operator<<(ostream &, const Racional &);
    friend istream &operator>>(istream &, Racional &);
private:
    int num, demon;
    void simplificar();
};
#endif // RACIONAL_H
Racional Racional::operator-(){
    return Racional(-num, demon);
}
Racional operator+(const Racional &r1, const Racional &r2){
    int dd = r1.demon * r2.demon;
    int nn = r1.num * r2.demon + r1.demon * r2.num;
    return Racional(nn, dd);
}
Racional operator-(const Racional &r1, const Racional &r2){
    int dd = r1.demon * r2.demon;
    int nn = r1.num * r2.demon - r1.demon * r2.num;
    return Racional(nn, dd);
}
Racional operator*(const Racional &r1, const Racional &r2){
    int dd = r1.demon * r2.demon;
    int nn = r1.num * r2.num;
    return Racional(nn, dd);
}
Racional operator/(const Racional &r1, const Racional &r2){
    int dd = r2.num * r1.demon;
    int nn = r1.num * r2.demon;
    return Racional(nn, dd);
}
bool operator==(const Racional &r1, const Racional &r2){
    return (r1.num * r2.demon == r1.demon * r2.num) ? true : false;
}
bool operator!=(const Racional &r1, const Racional &r2){
    return (r1.num * r2.demon != r1.demon * r2.num) ? true : false;
}
bool operator<(const Racional &r1, const Racional &r2){
    return (r1.num * r2.demon < r1.demon * r2.num) ? true : false;
}
bool operator<=(const Racional &r1, const Racional &r2){
    return (r1.num * r2.demon <= r1.demon * r2.num) ? true : false;
}
bool operator>(const Racional &r1, const Racional &r2){
    return (r1.num * r2.demon > r1.demon * r2.num) ? true : false;
}
bool operator>=(const Racional &r1, const Racional &r2){
    return (r1.num * r2.demon >= r1.demon * r2.num) ? true : false;
}
Racional &Racional::operator++(){ // prefijo
    num = num + demon;
    return *this;
}
Racional &Racional::operator--(){ // prefijo
    num = num - demon;
    return *this;
}
Racional &Racional::operator=(const Racional &p){
    if (*this != p){
        num = p.num;
        demon = p.demon;
    }
    return *this;
}
Racional &Racional::operator+=(const Racional &p){
    *this = *this + p;
    return *this;
}
Racional &Racional::operator-=(const Racional &p){
    *this = *this - p;
    return *this;
}
Racional &Racional::operator*=(const Racional &p){
    *this = *this * p;
    return *this;
}
Racional::Racional(int nu, int den){
    assert(den != 0);
    num = nu;
    demon = den;
    simplificar();
}
Racional::Racional(const Racional &r){
    num = r.num;
    demon = r.demon;
}
void Racional::print(){
    cout << *this;
}
ostream &operator<<(ostream &os, const Racional &r){
    os << r.num << "/" << r.demon;
    return os;
}
istream &operator>>(istream &is, Racional &r){
    is >> r.num >> r.demon;
    return is;
}
void Racional::simplificar(){
    if (!num) return;
    if (demon < 0){
        num = -num;
        demon = -demon;
    }
    int d = mcd(num, demon);
    if (d > 1){
        num = num / d;
        demon = demon / d;
    }
}
int mcd(int x, int y){
    if (x < y) return mcd(y, x);
    if (x % y == 0) return y;
    else return mcd(y, x % y);
}
int main(){
    Racional r1(2, 3), r2(2, 3), r3(2, 3), r4;
    cout << "\nNumeros racionales" << endl;
    cout << "r1 -> " << r1 << endl;
    cout << "r2 -> " << r2 << endl;
    cout << "r3 -> " << r3 << endl;
    r4 = r1 + r2;
    cout << "\nSuma de r1 y r2 = r4 -> " << r4 << endl;
    if (r1 == r3) cout << "\nr1 es igual a r3" << endl;
    else cout << "\nr1 no es igual a r3" << endl;
    r4 += r1;
    cout << "\nr4 += r1 -> " << r4 << endl;
    r4 *= r2;
    cout << "\nr4 *= r2 -> " << r4 << endl;
    ++r3;
    cout << "\n1 + r3 -> " << r3 << endl;
    r1 = r4;
    cout << "\nAsignando r4 a r1 -> " << r1 << endl;
    cout << "\nPresione una tecla para finalizar...!";
    return 0;
}*/

/* // ejemplo 6
#include <iostream>
#include <cmath>
using namespace std;
class entero
{
private:
    int num;

public:
    entero() { num = 0; }
    entero(int x) { num = x; }
    entero(entero &e) { num = e.num; }
    void asignar(int x) { num = x; }
    void cambiar_signo() { num = -num; }
    void imprimir() { cout << num << endl; }
    char getSigno()
    {
        if (num > 0)
            return '+';
        else if (num < 0)
            return '-';
        else
            return ' ';
    }
    entero operator+(entero y)
    {
        num = num + y.num;
        return *this;
    }
    entero operator-(entero y)
    {
        num = num - y.num;
        return *this;
    }
    entero operator*(entero y)
    {
        num = num * y.num;
        return *this;
    }
    entero operator/(entero y)
    {
        num = num / y.num;
        return *this;
    }
    entero operator%(entero y)
    {
        num = num % y.num;
        return *this;
    }
    // Operadores de relación
    bool operator==(entero y) { return num == y.num; }
    bool operator!=(entero y) { return num != y.num; }
    bool operator>(entero y) { return num > y.num; }
    bool operator<(entero y) { return num < y.num; }
    bool operator>=(entero y) { return num >= y.num; }
    bool operator<=(entero y) { return num <= y.num; }
    // Operador de asignación
    entero operator=(entero y)
    {
        num = y.num;
        return *this;
    }
    // Operador ! para mostrar divisores
    void operator!()
    {
        int absNum = abs(num);
        for (int i = 1; i <= absNum; ++i)
            if (absNum % i == 0)
                cout << i << endl;
    }
};
int main()
{
    cout << "Clase entero:" << endl;
    entero a(7), b(10), c, d, e;
    cout << "a = ";
    a.imprimir();
    cout << "b = ";
    b.imprimir();
    cout << "c = ";
    c.imprimir();
    cout << "d = ";
    d.imprimir();
    cout << "e = ";
    e.imprimir();
    cout << "\na + b = ";
    a = a + b;
    a.imprimir();
    cout << "a - b = ";
    a = a - b;
    a.imprimir();
    cout << "a * b = ";
    a = a * b;
    a.imprimir();
    cout << "a / b = ";
    a = a / b;
    a.imprimir();
    // Módulo
    cout << "a % b = ";
    a = a % b;
    a.imprimir();
    // Comparaciones
    cout << "\na == b: " << (a == b) << endl;
    cout << "a != b: " << (a != b) << endl;
    cout << "a > b: " << (a > b) << endl;
    cout << "a < b: " << (a < b) << endl;
    cout << "a >= b: " << (a >= b) << endl;
    cout << "a <= b: " << (a <= b) << endl;
    // Divisores
    entero f(30);
    cout << "\nDivisores de ";
    f.imprimir();
    !f;
    return 0;
}*/

/* //ejemplo 5
#include <iostream>
using namespace std;
//*******************************************
// TAD Complejo: Sobrecarga de operadores +, -, - unario, ! unario,
// y operador de extracción de flujo << con funciones amigas.
//*******************************************
class Complejo
{
private:
    float real;
    float imag;

public:
    Complejo() : real(0), imag(0) {}
    Complejo(float r, float i) : real(r), imag(i) {}

    // Método para imprimir usando cout
    void print();

    // Operadores sobrecargados como funciones amigas
    friend Complejo operator+(const Complejo &, const Complejo &);
    friend Complejo operator-(const Complejo &, const Complejo &);
    friend Complejo operator-(const Complejo &); // unario
    friend Complejo operator!(const Complejo &); // opuesto
    friend ostream &operator<<(ostream &, const Complejo &);
};
void Complejo::print()
{
    cout << (*this); // usa operador <<
}
Complejo operator+(const Complejo &x, const Complejo &y)
{
    return Complejo(x.real + y.real, x.imag + y.imag);
}
Complejo operator-(const Complejo &x, const Complejo &y)
{
    return Complejo(x.real - y.real, x.imag - y.imag);
}
Complejo operator-(const Complejo &x)
{
    return Complejo(x.real, -x.imag); // conjugado
}
Complejo operator!(const Complejo &x)
{
    return Complejo(-x.real, -x.imag); // opuesto
}
ostream &operator<<(ostream &os, const Complejo &x)
{
    os << x.real << ((x.imag < 0) ? "" : "+") << x.imag << "i";
    return os;
}
int main()
{
    Complejo x(4.0, 3.0), y(2.0, -1.0);
    Complejo z, w, t;
    cout << "Sumando dos complejos:" << endl;
    x.print();
    cout << " + " << endl;
    y.print();
    cout << " = " << endl;
    z = x + y;
    z.print();
    cout << endl;
    cout << "Restando dos complejos:" << endl;
    x.print();
    cout << " - " << endl;
    y.print();
    cout << " = " << endl;
    z = x - y;
    z.print();
    cout << endl;
    // Unario -
    cout << "Usando operador - unario para el primer complejo:" << endl;
    t = -x;
    t.print();
    cout << endl;
    // Unario !
    cout << "Usando operador ! unario para el opuesto de un complejo:" << endl;
    t = !y;
    t.print();
    cout << endl;
    return 0;
}*/

/* // ejemplo 4
#include <iostream>
using namespace std;
class Complejo
{
private:
    float real;
    float imag;

public:
    Complejo() {}           // Constructor por defecto
    Complejo(float, float); // Constructor con parámetros
    void print();
    // Operadores sobrecargados como funciones miembro
    Complejo operator+(const Complejo &); // Suma binaria
    Complejo operator-(const Complejo &); // Resta binaria
    Complejo operator-();                 // Negación unaria
};
// Implementación de constructores
Complejo::Complejo(float a, float b)
{
    real = a;
    imag = b;
}
void Complejo::print()
{
    cout << real << " + " << imag << "i" << endl;
}
// Operador + binario
Complejo Complejo::operator+(const Complejo &y)
{
    return Complejo(real + y.real, imag + y.imag);
}
// Operador - binario
Complejo Complejo::operator-(const Complejo &y)
{
    return Complejo(real - y.real, imag - y.imag);
}
// Operador - unario (negación del imaginario)
Complejo Complejo::operator-()
{
    return Complejo(real, -imag);
}
int main()
{
    Complejo x(3.0, 1.0), y(2.0, 4.0), z, t;
    cout << "Sumando dos complejos:" << endl;
    x.print();
    cout << " + ";
    y.print();
    cout << endl;
    z = x + y;
    cout << "Resultado: ";
    z.print();
    cout << endl;
    cout << "Restando dos complejos:" << endl;
    x.print();
    cout << " - ";
    y.print();
    cout << endl;
    z = x - y;
    cout << "Resultado: ";
    z.print();
    cout << endl;
    cout << "Usando operador - unario sobre el primer complejo:" << endl;
    cout << " - ";
    x.print();
    cout << endl;
    z = -x;
    cout << "Resultado: ";
    z.print();
    cout << endl;
    return 0;
}*/

/*
// ejemplo 3
#include <iostream>
using namespace std;
class Complejo
{
private:
    float real;
    float imag;

public:
    Complejo() {}           // Constructor por defecto
    Complejo(float, float); // Constructor con parámetros
    void print();
    // Sobrecarga del operador + como función miembro
    Complejo operator+(const Complejo &);
};
// Implementación del constructor por defecto
Complejo::Complejo(float a, float b)
{
    real = a;
    imag = b;
}
// Método para imprimir el número complejo
void Complejo::print()
{
    cout << real << " + " << imag << "i" << endl;
}
// Sobrecarga del operador + como función miembro
Complejo Complejo::operator+(const Complejo &y)
{
    return Complejo(real + y.real, imag + y.imag);
}
int main()
{
    Complejo x(1.0, 3.0), y(2.0, 1.0);
    Complejo z;
    cout << "Sobrecarga de Operadores con función miembro:" << endl;
    cout << "Complejo 1: ";
    x.print();
    cout << "Complejo 2: ";
    y.print();
    z = x + y; // usa la función miembro por prioridad
    cout << "\nSuma: ";
    z.print();
    cout << endl;
    return 0;
}*/

/*
// ejemplo 2
#include <iostream>
using namespace std;
class Complejo
{
    // Miembros privados
    float real;
    float imag;

public:
    Complejo();             // Constructor por defecto
    Complejo(float, float); // Constructor con parámetros
    ~Complejo();            // Destructor
    void print();           // Mostrar el número complejo
    // Función amiga para sobrecargar el operador +
    friend Complejo operator+(const Complejo &, const Complejo &);
};
// Implementación de métodos
Complejo::Complejo() : real(0), imag(0) {}
Complejo::Complejo(float r, float i) : real(r), imag(i) {}
void Complejo::print()
{
    cout << real << " + " << imag << "i" << endl;
}
// Sobrecarga del operador +
Complejo operator+(const Complejo &x, const Complejo &y)
{
    // Access to private members requires this function to be a friend of Complejo
    return Complejo(x.real + y.real, x.imag + y.imag);
}
Complejo::~Complejo()
{
    cout << "Destruyendo objeto Complejo..." << endl;
}
// Función principal
int main()
{
    Complejo x(1.0, 3.0), y(2.0, 1.0);
    Complejo z;
    cout << "Sobrecarga de Operadores con friend" << endl;
    cout << "Complejo 1: ";
    x.print();
    cout << "Complejo 2: ";
    y.print();
    z = x + y; // Uso del operador sobrecargado
    cout << "\nSuma: ";
    z.print();
    cout << endl;
    x.~Complejo();
    y.~Complejo();
    z.~Complejo();
    return 0;
}*/

/* //ejemplo 1
#include <iostream>
// Muestra el uso de funciones operadoras amigas; es decir, las funciones de
// sobrecarga de operadores pueden ser declaradas como amigas de la clase
using namespace std;
class Complejo
{
public:
    Complejo() {}               // Constructor por defecto
    Complejo(float a, float b); // Constructor con parámetros
    void print();               // Método para mostrar el número complejo
    // Sobrecargando el operador + para sumar objetos Complejo
    friend Complejo operator+(Complejo x, Complejo y);

private:
    float real;
    float imag;
};
// Implementación del constructor
Complejo::Complejo(float a, float b)
{
    real = a;
    imag = b;
}
// Método para imprimir el número complejo
void Complejo::print()
{
    cout << real << " + " << imag << "i" << endl;
}
// Función amiga para sobrecargar el operador +
Complejo operator+(Complejo x, Complejo y)
{
    Complejo z;
    z.real = x.real + y.real;
    z.imag = x.imag + y.imag;
    return z;
}
int main()
{
    Complejo x(1.0, 3.0), y(2.0, 1.0);
    Complejo z;
    cout << "Sobrecarga de Operadores con friend" << endl;
    cout << "Complejo 1: ";
    x.print();
    cout << "Complejo 2: ";
    y.print();
    z = x + y;
    cout << "Suma = ";
    z.print();
    return 0;
}
*/
