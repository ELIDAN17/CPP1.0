/*
#include <iostream>
using namespace std;

const int N = 100; // tamaño máximo de la memoria

class Calculadora
{
public:
    Calculadora()
    {
        n1 = n2 = res = 0;
        op = '+';
        nmem = 0;
    }

    Calculadora(float a, float b, char o)
    {
        n1 = a;
        n2 = b;
        op = o;
        calcular();
        memoria[nmem++] = res;
    }

    ~Calculadora()
    {
        cout << "Destruyendo objeto Calculadora..." << endl;
    }

    void asignaN1(float a) { n1 = a; }
    void asignaN2(float b) { n2 = b; }
    void setOp(char o) { op = o; }

    float getN1() { return n1; }
    float getN2() { return n2; }
    char getOp() { return op; }
    float getRes() { return res; }

    void calcular()
    {
        switch (op)
        {
        case '+':
            res = n1 + n2;
            break;
        case '-':
            res = n1 - n2;
            break;
        case '*':
            res = n1 * n2;
            break;
        case '/':
            if (n2 != 0)
                res = n1 / n2;
            else
            {
                cout << "Error: división por cero." << endl;
                res = 0;
            }
            break;
        default:
            cout << "Operador inválido." << endl;
            res = 0;
        }
        if (nmem < N)
            memoria[nmem++] = res;
    }

    void imprime()
    {
        cout << "Operación: " << n1 << " " << op << " " << n2 << " = " << res << endl;
    }

    void imprimeTipo()
    {
        switch (op)
        {
        case '+':
            cout << "Suma" << endl;
            break;
        case '-':
            cout << "Resta" << endl;
            break;
        case '*':
            cout << "Multiplicación" << endl;
            break;
        case '/':
            cout << "División" << endl;
            break;
        default:
            cout << "Operación desconocida" << endl;
        }
    }

    void imprimeMem()
    {
        cout << "Memoria de resultados:" << endl;
        for (int i = 0; i < nmem; i++)
            cout << i + 1 << ") " << memoria[i] << endl;
    }

    void limpiarmemoria()
    {
        nmem = 0;
        cout << "Memoria borrada." << endl;
    }

private:
    float n1, n2, res;
    char op;
    float memoria[N];
    int nmem;
};
int main()
{
    Calculadora calc;
    float a, b;
    char operador;
    int opcion;

    do
    {
        cout << "\n--- Menú Calculadora ---" << endl;
        cout << "1) Nueva operación" << endl;
        cout << "2) Ver tipo de operación" << endl;
        cout << "3) Ver memoria" << endl;
        cout << "4) Limpiar memoria" << endl;
        cout << "5) Salir" << endl;
        cout << "Seleccione una opción: ";
        cin >> opcion;

        switch (opcion)
        {
        case 1:
            cout << "Ingrese primer número: ";
            cin >> a;
            cout << "Ingrese segundo número: ";
            cin >> b;
            cout << "Ingrese operador (+, -, *, /): ";
            cin >> operador;

            calc.asignaN1(a);
            calc.asignaN2(b);
            calc.setOp(operador);
            calc.calcular();
            calc.imprime();
            break;

        case 2:
            calc.imprimeTipo();
            break;

        case 3:
            calc.imprimeMem();
            break;

        case 4:
            calc.limpiarmemoria();
            break;

        case 5:
            cout << "Fin del programa." << endl;
            break;

        default:
            cout << "Opción inválida." << endl;
        }
    } while (opcion != 5);

    return 0;
}*/

/*
// reales
#include <iostream>
#include <cmath>
using namespace std;
class CReal
{
public:
    // Constructores
    CReal() { num = 0.0; }
    CReal(double n) { num = n; }
    CReal(const CReal &r) { num = r.num; }
    // Métodos de impresión
    void imprimir()
    {
        cout << "Número real: " << num << endl;
    }
    // Método para obtener el signo
    char getSigno()
    {
        return (num < 0) ? '-' : '+';
    }
    // Operaciones aritméticas
    CReal sumar(CReal a, CReal b)
    {
        return CReal(a.num + b.num);
    }
    CReal restar(CReal a, CReal b)
    {
        return CReal(a.num - b.num);
    }
    CReal multiplicar(CReal a, CReal b)
    {
        return CReal(a.num * b.num);
    }
    CReal dividir(CReal a, CReal b)
    {
        if (b.num == 0)
        {
            cout << "Error: división por cero." << endl;
            return CReal(0);
        }
        return CReal(a.num / b.num);
    }

private:
    double num;
};
int main()
{
    CReal r1(5.75), r2(-2.25), resultado;
    cout << "r1: ";
    r1.imprimir();
    cout << "r2: ";
    r2.imprimir();
    cout << "\nSigno de r1: " << r1.getSigno() << endl;
    cout << "Signo de r2: " << r2.getSigno() << endl;
    resultado = resultado.sumar(r1, r2);
    cout << "\nr1 + r2 = ";
    resultado.imprimir();
    resultado = resultado.restar(r1, r2);
    cout << "r1 - r2 = ";
    resultado.imprimir();
    resultado = resultado.multiplicar(r1, r2);
    cout << "r1 * r2 = ";
    resultado.imprimir();
    resultado = resultado.dividir(r1, r2);
    cout << "r1 / r2 = ";
    resultado.imprimir();
    return 0;
}*/

/*
// 3D
#include <iostream>
#include <cmath>
using namespace std;
class Punto3D
{
public:
    // Constructores
    Punto3D()
    {
        x = y = z = 0;
    }
    Punto3D(float a, float b, float c)
    {
        x = a;
        y = b;
        z = c;
    }
    Punto3D(const Punto3D &p)
    {
        x = p.x;
        y = p.y;
        z = p.z;
    }
    // Métodos set
    void setX(float a) { x = a; }
    void setY(float b) { y = b; }
    void setZ(float c) { z = c; }
    // Métodos get
    float getX() const { return x; }
    float getY() const { return y; }
    float getZ() const { return z; }
    // Método para imprimir el punto
    void imprimir() const
    {
        cout << "(" << x << ", " << y << ", " << z << ")" << endl;
    }
    // Método para calcular la distancia entre dos puntos
    float distancia(const Punto3D &otro) const
    {
        return sqrt(pow(x - otro.x, 2) + pow(y - otro.y, 2) + pow(z - otro.z, 2));
    }
    // Método para trasladar el punto
    void trasladar(float dx, float dy, float dz)
    {
        x += dx;
        y += dy;
        z += dz;
    }

private:
    float x, y, z;
};
int main()
{
    Punto3D p1(1.0, 2.0, 3.0);
    Punto3D p2(4.0, 6.0, 9.0);
    cout << "Punto 1: ";
    p1.imprimir();
    cout << "Punto 2: ";
    p2.imprimir();
    cout << "\nDistancia entre puntos: " << p1.distancia(p2) << endl;
    cout << "\nTrasladando Punto 1 por (1, -2, 3)..." << endl;
    p1.trasladar(1, -2, 3);
    cout << "Nuevo Punto 1: ";
    p1.imprimir();
    return 0;
}*/

/*
// combinado
#include <iostream>
using namespace std;

// Clase Rectangulo
class Rectangulo
{
private:
    float base;
    float altura;

public:
    void setLados(float b, float h)
    {
        base = b;
        altura = h;
    }

    float getBase() { return base; }
    float getAltura() { return altura; }

    float area() { return base * altura; }
    float perimetro() { return 2 * (base + altura); }

    void print()
    {
        cout << "\nRectángulo:" << endl;
        cout << "Base = " << base << ", Altura = " << altura << endl;
        cout << "Área = " << area() << endl;
        cout << "Perímetro = " << perimetro() << endl;
    }
};

// Clase Triangulo
class Triangulo
{
private:
    float base;
    float altura;

public:
    void setDatos(float b, float h)
    {
        base = b;
        altura = h;
    }

    float getBase() { return base; }
    float getAltura() { return altura; }

    float area() { return (base * altura) / 2; }

    float perimetro()
    {
        // Asumiendo triángulo equilátero para simplificar
        return 3 * base;
    }

    void print()
    {
        cout << "\nTriángulo:" << endl;
        cout << "Base = " << base << ", Altura = " << altura << endl;
        cout << "Área = " << area() << endl;
        cout << "Perímetro (aproximado) = " << perimetro() << endl;
    }
};

// Función principal con menú
int main()
{
    int opcion;
    float b, h;

    do
    {
        cout << "\n--- Menú de Figuras ---" << endl;
        cout << "1) Rectángulo" << endl;
        cout << "2) Triángulo" << endl;
        cout << "3) Salir" << endl;
        cout << "Seleccione una opción: ";
        cin >> opcion;

        switch (opcion)
        {
        case 1:
        {
            cout << "Ingrese base: ";
            cin >> b;
            cout << "Ingrese altura: ";
            cin >> h;
            Rectangulo r;
            r.setLados(b, h);
            r.print();
            break;
        }
        case 2:
        {
            cout << "Ingrese base: ";
            cin >> b;
            cout << "Ingrese altura: ";
            cin >> h;
            Triangulo t;
            t.setDatos(b, h);
            t.print();
            break;
        }
        case 3:
            cout << "Fin del programa." << endl;
            break;
        default:
            cout << "Opción inválida." << endl;
        }
    } while (opcion != 3);

    return 0;
}*/

/*
// clase triangulo
#include <iostream>
#include <cmath>
using namespace std;

class Triangulo
{
private:
    float base;
    float altura;

public:
    void setDatos()
    {
        cout << "Ingrese base del triángulo: ";
        cin >> base;
        cout << "Ingrese altura del triángulo: ";
        cin >> altura;
    }

    void getDatos()
    {
        cout << "Base: " << base << ", Altura: " << altura << endl;
    }

    float area()
    {
        return (base * altura) / 2;
    }

    float perimetro()
    {
        // Asumiendo triángulo equilátero para ejemplo simple
        return 3 * base;
    }

    void print()
    {
        cout << "Área: " << area() << endl;
        cout << "Perímetro (aproximado): " << perimetro() << endl;
    }
};

int main()
{
    Triangulo t;
    t.setDatos();
    t.getDatos();
    t.print();

    return 0;
}*/

// clase rectangulo
#include <iostream>
using namespace std;
class Rectangulo
{
public:
    void setLados(float b, float h)
    {
        base = b;
        altura = h;
    }
    float getBase() { return base; }
    float getAltura() { return altura; }
    float area() { return base * altura; }
    float perimetro() { return 2 * (base + altura); }
    void print()
    {
        cout << "Área: " << area() << endl;
        cout << "Perímetro: " << perimetro() << endl;
    }

private:
    float base;
    float altura;
};
int main()
{
    Rectangulo r;
    float b, h;
    cout << "Ingrese base del rectángulo: ";
    cin >> b;
    cout << "Ingrese altura del rectángulo: ";
    cin >> h;
    r.setLados(b, h);
    cout << "\nBase = " << r.getBase() << ", Altura = " << r.getAltura() << endl;
    r.print();
    return 0;
}

/* codigo 11
#ifndef TIME1_H // si no está definido TIME1_H
#define TIME1_H // definir TIME1_H
class Time
{ // Declaración del tipo de dato abstracto Time
public:
    Time();                      // constructor
    void setTime(int, int, int); // establecer hora, minuto, segundo
    void printUniversal();       // imprimir hora en formato universal
    void printStandard();        // imprimir hora en formato estándar
private:
    int hour;   // 0 - 23
    int minute; // 0 - 59
    int second; // 0 - 59
}; // fin de la clase Time
#endif // TIME1_H
#include <iostream>
using namespace std;
// Inicializa los datos miembro en un estado consistente
Time::Time() { hour = minute = second = 0; } // Constructor de la clase Time
// Establece nuevos valores de hora
void Time::setTime(int h, int m, int s)
{
    hour = (h >= 0 && h < 24) ? h : 0;
    minute = (m >= 0 && m < 60) ? m : 0;
    second = (s >= 0 && s < 60) ? s : 0;
}
// Imprime Time en formato universal (HH:MM:SS)
void Time::printUniversal()
{
    cout << (hour < 10 ? "0" : "") << hour << ":"
         << (minute < 10 ? "0" : "") << minute;
}
// Imprime Time en formato estándar (HH:MM:SS AM/PM)
void Time::printStandard()
{
    cout << ((hour == 0 || hour == 12) ? 12 : hour % 12) << ":"
         << (minute < 10 ? "0" : "") << minute << ":"
         << (second < 10 ? "0" : "") << second
         << (hour < 12 ? " AM" : " PM");
}
int main()
{
    Time t; // crea objeto Time
    cout << "\nLa hora universal inicial es: ";
    t.printUniversal();
    cout << "\nLa hora estándar inicial es: ";
    t.printStandard();
    // Utilizando setTime
    t.setTime(15, 27, 16);
    cout << "\n\nLa hora universal después de setTime es: ";
    t.printUniversal();
    cout << "\nLa hora estándar después de setTime es: ";
    t.printStandard();
    // Intentando valores no válidos para el objeto t
    t.setTime(99, 99, 99);
    cout << "\n\nDespués de intentar ingresar valores no válidos:\n\nHora universal: ";
    t.printUniversal();
    cout << "\nHora estándar: ";
    t.printStandard();
    cout << endl;
    return 0;
}*/

/* codigo 10
// OBJETIVO: Una clase que utiliza un arreglo de objetos 2009-0
// La clase CAlumno gestiona objetos individuales. Si se quiere gestionar un
// conjunto de objetos CAlumno, es mejor que una clase que utilice un array de
// objetos CAlumno. Una nueva clase debe permitir agregar un nuevo alumno, buscar un
// alumno y eliminar un alumno según su código.
// El programa presenta un MENU DE OPCIONES al usuario
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const int N = 50;
using namespace std;
struct alumno
{
    int codigo;
    char nombre[40];
    int notas[4];
};
class CAlumno
{
public:
    void setCodigo(int cod);
    void setNombre(char nom[]);
    void setNotas();
    int getCodigo();
    char *getNombre();
    void getNotas();
    double promedio();
    const char *estado();

private:
    alumno a;
};
void CAlumno::setCodigo(int cod) { a.codigo = cod; }
void CAlumno::setNombre(char nom[]) { strcpy(a.nombre, nom); }
void CAlumno::setNotas()
{
    cout << "\nIngrese cuatro notas: ";
    for (int i = 0; i < 4; i++)
    {
        cin >> a.notas[i];
    }
}
int CAlumno::getCodigo() { return a.codigo; }
char *CAlumno::getNombre() { return a.nombre; }
void CAlumno::getNotas()
{
    cout << "Notas: ";
    for (int i = 0; i < 4; i++)
    {
        cout << a.notas[i] << " ";
    }
    cout << endl;
}
double CAlumno::promedio()
{
    int suma = 0;
    for (int i = 0; i < 4; i++)
    {
        suma += a.notas[i];
    }
    return suma / 4.0;
}
const char *CAlumno::estado()
{
    if (promedio() >= 10.5)
        return "Aprobado";
    else
        return "Desaprobado";
}
void listar(CAlumno a)
{
    cout << "\nDatos del alumno: " << endl;
    cout << "Código: " << a.getCodigo() << endl;
    cout << "Nombre: " << a.getNombre() << endl;
    a.getNotas();
    cout << "Promedio: " << a.promedio() << endl;
    cout << "Estado: " << a.estado() << endl;
}
class CAlumnos
{
public:
    CAlumnos() { indice = 0; }
    void setAlumno(int p, CAlumno actual) { array[p] = actual; }
    CAlumno getAlumno(int p) { return array[p]; }
    int getIndice() { return indice; }
    void agrega(CAlumno uno);
    void elimina(int P);
    int busca(int cod);

private:
    CAlumno array[N];
    int indice;
};
void CAlumnos::agrega(CAlumno uno)
{
    if (indice < N)
    {
        array[indice] = uno;
        indice++;
    }
}
void CAlumnos::elimina(int P)
{
    for (int i = P; i < indice; i++)
        array[i] = array[i + 1];
    indice--;
}
int CAlumnos::busca(int cod)
{ // Busca alumno por su código
    for (int i = 0; i < indice; i++)
    {
        if (array[i].getCodigo() == cod)
            return i;
    }
    return -1; // No se encuentra
}
CAlumnos Industrial; // Declaro objeto CAlumnos de Industrial
void agregar();
void eliminar();
void imprimir();
void menu();
int main()
{
    menu();
    return 0;
}
// Desarrollo de las funciones adicionales
void agregar()
{
    int cod;
    char nom[40];
    fflush(stdin);
    cout << "\nIngrese código del alumno : ";
    cin >> cod;
    fflush(stdin);
    cout << "\nIngrese nombre del alumno : ";
    gets(nom);
    fflush(stdin);
    CAlumno alumno; // declaro el objeto
    // Colocar datos en el objeto
    alumno.setCodigo(cod);
    alumno.setNombre(nom);
    alumno.setNotas();
    int p = Industrial.busca(cod);
    if (p >= 0)
        cout << "¡Código repetido!..." << endl;
    else
    {
        // Agregar alumno al array
        if (Industrial.getIndice() == N)
            cout << "¡Arreglo de alumnos de Industrial lleno!..." << endl;
        else
        {
            Industrial.agrega(alumno);
            imprimir();
        }
    }
}
void eliminar()
{
    int cod;
    cout << "Codigo: ";
    cin >> cod;
    cin.ignore();
    int p = Industrial.busca(cod);
    cout << "Índice a eliminar: " << p << endl;
    if (p < 0)
    {
        cout << "¡Código no existe!" << endl;
    }
    else
    {
        Industrial.elimina(p);
        imprimir();
    }
}
void imprimir()
{
    if (Industrial.getIndice() == 0)
        cout << "No hay alumnos en Industrial..." << endl;
    else
    {
        for (int i = 0; i < Industrial.getIndice(); i++)
        {
            CAlumno ca = Industrial.getAlumno(i);
            cout << "\nCódigo: " << ca.getCodigo() << endl;
            cout << "Nombre: " << ca.getNombre() << endl;
            cout << "Promedio: " << ca.promedio() << endl;
            cout << "Estado: " << ca.estado() << endl;
        }
    }
}
void menu()
{
    int opc;
    do
    {
        cout << "\n[1] Agregar" << endl;
        cout << "[2] Eliminar" << endl;
        cout << "[3] Imprimir" << endl;
        cout << "[0] Salir" << endl;
        cout << "Opción: ";
        cin >> opc;
        switch (opc)
        {
        case 1:
            agregar();
            break;
        case 2:
            eliminar();
            break;
        case 3:
            imprimir();
            break;
        }
    } while (opc != 0);
    cout << "¡Fin del programa!..." << endl;
}*/

/* codigo 9
// OBJETIVO: Una clase CAlumno 2009-0
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;
struct alumno
{
    char codigo[10];
    char nombre[40];
    int notas[4];
};
class CAlumno
{
public:
    void setCodigo();
    void setNombre();
    void setNotas();
    char *getCodigo();
    char *getNombre();
    void getNotas();
    double promedio();
    char *estado();

private:
    alumno a;
};
void CAlumno::setCodigo()
{
    cout << "Ingrese código del alumno: ";
    gets(a.codigo);
}
void CAlumno::setNombre()
{
    cout << "Ingrese nombre del alumno: ";
    gets(a.nombre);
}
void CAlumno::setNotas()
{
    cout << "Ingrese cuatro notas: ";
    for (int i = 0; i < 4; i++)
    {
        cin >> a.notas[i];
    }
}
char *CAlumno::getCodigo()
{
    return a.codigo;
}
char *CAlumno::getNombre()
{
    return a.nombre;
}
void CAlumno::getNotas()
{
    cout << "Notas: ";
    for (int i = 0; i < 4; i++)
    {
        cout << a.notas[i] << " ";
    }
}
double CAlumno::promedio()
{
    int suma = 0;
    for (int i = 0; i < 4; i++)
    {
        suma += a.notas[i];
    }
    return suma / 4.0;
}
char *CAlumno::estado()
{
    if (promedio() >= 10.5)
        return "Aprobado";
    else
        return "Desaprobado";
}
void listar(CAlumno a)
{
    cout << "\nDatos del alumno: " << endl;
    cout << "\nCódigo: " << a.getCodigo() << endl;
    cout << "Nombre: " << a.getNombre() << endl;
    a.getNotas();
    cout << "\nPromedio: " << a.promedio() << endl;
    cout << "Estado: " << a.estado() << endl;
}
int main()
{ // Clase_Alumno_2.cpp
    CAlumno un;
    un.setCodigo();
    un.setNombre();
    un.setNotas();
    listar(un);
    return 0;
}*/

/* codigo 8
// OBJETIVO: Una clase CAlumno cuyo dato miembro es un objeto del tipo struct
#include <iostream>
#include <stdio.h>
using namespace std;
struct alumno
{
    char codigo[10];
    char nombre[40];
    int notas[4];
};
class CAlumno
{
public:
    void setCodigo()
    {
        cout << "Ingrese código del alumno: ";
        gets(a.codigo);
    }
    void setNombre()
    {
        cout << "Ingrese nombre del alumno: ";
        gets(a.nombre);
    }
    void setNotas()
    {
        cout << "Ingrese cuatro notas: ";
        for (int i = 0; i < 4; i++)
        {
            cin >> a.notas[i];
        }
    }
    char *getCodigo() { return a.codigo; }
    char *getNombre() { return a.nombre; }
    void getNotas()
    {
        for (int i = 0; i < 4; i++)
        {
            cout << a.notas[i] << " ";
            cout << endl;
        }
    }
    double promedio()
    {
        int suma = 0;
        for (int i = 0; i < 4; i++)
        {
            suma += a.notas[i];
        }
        return suma / 4;
    }
    char *estado()
    {
        if (promedio() >= 10.5)
        {
            return "Aprobado";
        }
        else
        {
            return "desaprobado";
        }
    }

private:
    alumno a;
};
int main()
{
    CAlumno ii;
    ii.setCodigo();
    ii.setNombre();
    ii.setNotas();
    cout << "Datos del alumno: " << endl;
    cout << "Código: " << ii.getCodigo() << endl;
    cout << "Nombre: " << ii.getNombre() << endl;
    ii.getNotas();
    double prom = ii.promedio();
    cout << "Promedio = " << prom << endl;
    cout << "Estado = " << ii.estado() << endl;
    return 0;
}*/

/* codigo 7
#include <iostream>
#include <cmath> // para M_PI
using namespace std;
class circulo
{
public:
    circulo();                // constructor por defecto
    circulo(float);           // constructor alternativo
    circulo(const circulo &); // constructor de copia
    double area();
    double perimetro();
    void print();
    ~circulo(); // destructor
private:
    float radio;
};
// usando el operador de resolución o ámbito ::
circulo::circulo()
{
    radio = 0;
}
circulo::circulo(float a)
{
    radio = a;
}
circulo::circulo(const circulo &cl)
{
    radio = cl.radio;
}
double circulo::area()
{
    return M_PI * radio * radio;
}

double circulo::perimetro()
{
    return 2 * M_PI * radio;
}

void circulo::print()
{
    cout << "El radio es: " << radio << endl;
    cout << "El perímetro es: " << perimetro() << endl;
    cout << "El área es: " << area() << endl;
}
circulo::~circulo()
{
    cout << "Objeto destruyéndose..." << endl;
}
int main()
{ // Clase_Circulo_4.cpp
    float r = 1.5;
    circulo cir; // constructor por defecto
    cout << "\nConstructor por defecto" << endl;
    cir.print(); // mostrar datos del círculo por defecto
    // declarando el objeto cir2 y activando el constructor alternativo
    cout << "\nConstructor alternativo" << endl;
    circulo cir2(r);
    cir2.print();
    // activando el constructor de copia
    cout << "\nCopiando un objeto a otro: " << endl;
    circulo cir3 = cir2;
    cir3.print();
    cout << "\nInvocando Destructores" << endl;
    // activando destructores manualmente (esto no es válido en C++)
    cir.~circulo();
    cir2.~circulo();
    cir3.~circulo();
    return 0;
}*/

/* codigo 6
#include <iostream>
#include <cmath> // para M_PI
using namespace std;
class circulo
{
public:
    circulo();        // constructor por defecto
    circulo(float a); // constructor alternativo
    ~circulo();       // destructor
    double area();
    double perimetro();

private:
    float radio;
};
// usando el operador de resolución o ámbito ::
circulo::circulo()
{
    radio = 0;
}
circulo::circulo(float a)
{
    radio = a;
}
double circulo::area()
{
    return M_PI * radio * radio;
}
double circulo::perimetro()
{
    return 2 * M_PI * radio;
}
circulo::~circulo()
{
    cout << "Objeto destruyéndose..." << endl;
}
int main()
{
    float r = 2.5;
    // Declarando el objeto cir y activando su constructor
    circulo cir(r);
    cout << "El área es: " << cir.area() << endl;
    cout << "El perímetro es: " << cir.perimetro() << endl;
    cir.~circulo();
    cout << endl; // activa el destructor
    return 0;
}*/

/* codigo 5
#include <iostream>
#include <cmath> // para M_PI
class circulo
{
    // Definimos la parte pública en donde se encuentran las funciones miembro
public:
    void inicio(float a) { radio = a; }
    double area() { return M_PI * radio * radio; }
    double perimetro() { return 2 * M_PI * radio; }
    // Declaramos la parte privada donde se encuentran los datos
private:
    float radio;
};
using namespace std;
int main()
{ // Clase_Circulo_2.cpp
    float r = 2.5;
    circulo cir; // Declaración del objeto cir perteneciente a la clase circulo
    cout << "Circulo de radio " << r << endl;
    // llama a las funciones miembro
    cout << "El area es " << cir.area() << endl;
    cout << "El perimetro es " << cir.perimetro() << endl;
    cout << endl;
    return 0;
}*/

/* codigo 4
#include <iostream>
#include <cmath> // para M_PI

using namespace std;

// Mostrar uso de funciones set y get
class Circulo
{
public:
    void setRadio(float a); // asignar el radio
    float getRadio();       // recuperar el radio
    double area();          // calcular y devolver área
    double perimetro();     // calcular y devolver perímetro
    void print();           // función de utilidad

private:
    float radio;
};
// usando el operador de resolución o ámbito ::
void Circulo::setRadio(float a) // asignar el radio
{
    radio = a;
}

float Circulo::getRadio() // recuperar el radio
{
    return radio;
}

double Circulo::area()
{
    return M_PI * radio * radio;
}

double Circulo::perimetro()
{
    return 2 * M_PI * radio;
}

void Circulo::print()
{
    cout << "El área es: " << area() << endl;
    cout << "El perímetro es: " << perimetro() << endl;
}

// programa principal
int main() // Clase_Circulo_1.cpp
{
    float r;
    Circulo cir;
    cout << "\nIngrese radio: ";
    cin >> r;
    // llamado a setRadio()
    cir.setRadio(r);
    cout << "\nRadio = " << cir.getRadio() << endl;
    cir.print();
    cout << endl;
}*/

/* codigo 3
// Objetivo: Iniciar la introducción a la POO
// Utilizando el operador de resolución de ámbito :: para escribir el código de
// las funciones miembros fuera de la clase.
#include <iostream>
#include <string.h>
#include <stdio.h>
using namespace std;

class persona
{
private:
    char nombre[40];
    short edad;

public:
    void setDatos(); // funciones miembros
    void getDatos(); // funciones miembros
};

void persona::setDatos()
{
    cout << "\nIngrese nombre: ";
    gets(nombre);
    cout << "\nIngrese la edad: ";
    cin >> edad;
}

void persona::getDatos()
{
    cout << "\nNombre: " << nombre << endl;
    cout << "Edad: " << edad << endl;
}

int main()
{                // Clase_Persona_3.cpp
    persona per; // objeto del tipo persona
    per.setDatos();
    per.getDatos();
}*/

/* codigo 2
// Objetivo: Introducción a la POO
// En una clase los miembros se distinguen entre privados, públicos y/o protegidos
// es decir: public, private y protected

#include <iostream>
#include <string.h>

using namespace std;

class persona
{
private: // datos miembros
    char nombre[40];
    short edad;

public: // funciones miembros
    void setDatos(char nom[], short e)
    {
        strcpy(nombre, nom);
        edad = e;
    }

    void getDatos()
    {
        cout << "Nombre: " << nombre << endl;
        cout << "Edad: " << edad << endl;
    }
};

int main() // Clase_Persona_2.cpp
{
    char nom[40];
    short ed;
    cout << "Ingrese nombre: ";
    cin.getline(nom, 40);
    cout << "Ingrese edad: ";
    cin >> ed;
    persona p; // objeto del tipo persona
    p.setDatos(nom, ed);
    p.getDatos();
    cout << endl;
    return 0;
}*/

/* codigo 1
// Objetivo: Introducción a la POO
// En una struct todos los miembros son públicos.
#include <iostream>
#include <string.h>
using namespace std;
struct persona{
    char nombre[40];
    short edad;
    // funciones miembros
    void setDatos(char nom[], short e)
    {
        strcpy(nombre, nom);
        edad = e;
    }
    void getDatos()
    {
        cout << "Nombre: " << nombre << endl;
        cout << "Edad: " << edad << endl;
    }
};
int main(){
    char nom[40];
    short ed;
    cout << "Ingrese nombre: ";
    cin.getline(nom, 40);
    cout << "Ingrese la edad: ";
    cin >> ed;
    persona per; // variable del tipo persona
    per.setDatos(nom, ed);
    per.getDatos();
    cout << endl;
    return 0;
}*/