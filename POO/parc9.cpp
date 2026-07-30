#include <iostream>
#include <cstring>
#include <ctime>
using namespace std;
class Nacimiento
{
private:
    int dia, mes, anual;

public:
    void PedirFecha();
    void Salvafech(int, int, int);
    bool VerificarFecha(int, int, int);
    void Mostrar();
    bool Bisiesto();
    int LoadAnual();
    int GetAnual() { return anual; }
};
class Persona : public Nacimiento
{
private:
    char Ape[25], Nom[20];
    int Edad;

public:
    void PedirDatos();
    void Mostrar();
    char *NombreCompleto();
};
void Nacimiento::PedirFecha()
{
    int d, m, a;
    cout << "Ingrese día de nacimiento: ";
    cin >> d;
    cout << "Ingrese mes de nacimiento: ";
    cin >> m;
    cout << "Ingrese año de nacimiento: ";
    cin >> a;
    if (VerificarFecha(d, m, a))
    {
        Salvafech(d, m, a);
    }
    else
    {
        cout << "Fecha inválida. Se asignará 0/0/0.\n";
        LoadAnual();
    }
}
void Nacimiento::Salvafech(int d, int m, int a)
{
    dia = d;
    mes = m;
    anual = a;
}
bool Nacimiento::VerificarFecha(int d, int m, int a)
{
    if (a < 1900 || a > 2100)
        return false;
    if (m < 1 || m > 12)
        return false;
    if (d < 1 || d > 31)
        return false;
    // Validación básica de días por mes
    if (m == 2)
    {
        if (a % 4 == 0 && (a % 100 != 0 || a % 400 == 0))
        {
            return d <= 29;
        }
        else
        {
            return d <= 28;
        }
    }
    if (m == 4 || m == 6 || m == 9 || m == 11)
    {
        return d <= 30;
    }
    return true;
}
void Nacimiento::Mostrar()
{
    cout << "Fecha de nacimiento: " << dia << "/" << mes << "/" << anual << endl;
}

bool Nacimiento::Bisiesto()
{
    if (anual == 0)
        return false;
    return (anual % 4 == 0 && (anual % 100 != 0 || anual % 400 == 0));
}
int Nacimiento::LoadAnual()
{
    dia = mes = anual = 0;
    return anual;
}
void Persona::PedirDatos()
{
    cout << "Ingrese apellido: ";
    cin.ignore();
    cin.getline(Ape, 25);
    cout << "Ingrese nombre: ";
    cin.getline(Nom, 20);
    PedirFecha();
    time_t t = time(nullptr);
    tm *now = localtime(&t);
    Edad = now->tm_year + 1900 - GetAnual();
}
void Persona::Mostrar()
{
    cout << "Nombre completo: " << Ape << " " << Nom << endl;
    Nacimiento::Mostrar();
    cout << "Edad: " << Edad << " años" << endl;
    cout << "¿Año bisiesto?: " << (Bisiesto() ? "Sí" : "No") << endl;
}
char *Persona::NombreCompleto()
{
    static char completo[50];
    strcpy(completo, Ape);
    strcat(completo, " ");
    strcat(completo, Nom);
    return completo;
}
int main()
{
    Persona p;
    p.PedirDatos();
    cout << "\n--- Datos de la Persona ---\n";
    p.Mostrar();
    cout << "\nNombre completo: " << p.NombreCompleto() << endl;
    return 0;
}

/* // Ejercicio 9.2
#include <iostream>
#include <cstring>
using namespace std;
struct fecha
{
    int dia, mes, anio;
};
class artista
{
private:
    char nombre[30];
    fecha nacimiento;
    char sexo[2], pais[15];

public:
    artista(char n[30], fecha f, char s[2], char p[15]);
    ~artista() {}
    void ingresar();
    void imprimir();
};
class cantante : public artista
{
private:
    char genero[15], canciones[200][40];
    int num_canciones;

public:
    cantante(char n[30], fecha f, char s[2], char p[15]);
    ~cantante() {}
    void ingresar();
    void imprimir();
    void getgenero(char g[15]);
    void repertorio();
};
artista::artista(char n[30], fecha f, char s[2], char p[15])
{
    strcpy(nombre, n);
    nacimiento = f;
    strcpy(sexo, s);
    strcpy(pais, p);
}
void artista::ingresar()
{
    cout << "Nombre: " << nombre << endl;
    cout << "Fecha de nacimiento: " << nacimiento.dia << "/" << nacimiento.mes << "/" << nacimiento.anio << endl;
    cout << "Sexo: " << sexo << endl;
    cout << "País: " << pais << endl;
}
void artista::imprimir()
{
    ingresar();
}
cantante::cantante(char n[30], fecha f, char s[2], char p[15]) : artista(n, f, s, p)
{
    num_canciones = 0;
    strcpy(genero, "");
}
void cantante::ingresar()
{
    cout << "Ingrese género musical: ";
    cin.getline(genero, 15);
    cout << "Ingrese número de canciones: ";
    cin >> num_canciones;
    cin.ignore();
    for (int i = 0; i < num_canciones; i++)
    {
        cout << "Canción " << i + 1 << ": ";
        cin.getline(canciones[i], 40);
    }
}
void cantante::imprimir()
{
    artista::imprimir();
    cout << "Género musical: " << genero << endl;
    cout << "Repertorio:" << endl;
    for (int i = 0; i < num_canciones; i++)
    {
        cout << "- " << canciones[i] << endl;
    }
}
void cantante::getgenero(char g[15])
{
    strcpy(g, genero);
}
void cantante::repertorio()
{
    cout << "Listado de canciones:" << endl;
    for (int i = 0; i < num_canciones; i++)
    {
        cout << canciones[i] << endl;
    }
}
int main()
{
    char nombre[30], sexo[2], pais[15];
    fecha nac;
    cout << "Ingrese nombre del artista: ";
    cin.getline(nombre, 30);
    cout << "Ingrese fecha de nacimiento (día mes año): ";
    cin >> nac.dia >> nac.mes >> nac.anio;
    cin.ignore();
    cout << "Ingrese sexo (M/F): ";
    cin.getline(sexo, 2);
    cout << "Ingrese país: ";
    cin.getline(pais, 15);
    cantante c(nombre, nac, sexo, pais);
    c.ingresar();
    cout << "\n--- Datos del Cantante ---\n";
    c.imprimir();
    return 0;
}*/

/* // Ejercicio 9.1
#include <iostream>
#include <string>
using namespace std;
class persona{
private:
    string nombre, estado_civil;
    int edad;
    char sexo;
public:
    persona() {}
    persona(string n, int e) : nombre(n), edad(e) {}
    persona(string n, int e, char s, string ec) : nombre(n), edad(e), sexo(s), estado_civil(ec) {}
    void setNombre(string n) { nombre = n; }
    void setEdad(int e) { edad = e; }
    void setSexo(char s) { sexo = s; }
    void setEstadoCivil(string ec) { estado_civil = ec; }
    string getNombre() { return nombre; }
    int getEdad() { return edad; }
    char getSexo() { return sexo; }
    string getEstadoCivil() { return estado_civil; }
    void print() {
        cout << "Nombre: " << nombre << endl;
        cout << "Edad: " << edad << endl;
        cout << "Sexo: " << sexo << endl;
        cout << "Estado Civil: " << estado_civil << endl;
    }
};
class alumno_unmsm : public persona{
private:
    string codigo, curso[5];
    float notas[5];
    int peso[5];
public:
    alumno_unmsm() {}
    void setCodigo(string c) { codigo = c; }
    void setCurso(int i, string nombre){
        if (i >= 0 && i < 5)
            curso[i] = nombre;
    }
    void setNota(int i, float nota){
        if (i >= 0 && i < 5)
            notas[i] = nota;
    }
    void setPeso(int i, int p){
        if (i >= 0 && i < 5)
            peso[i] = p;
    }
    string getCodigo() { return codigo; }
    string getCurso(int i) { return (i >= 0 && i < 5) ? curso[i] : ""; }
    float getNota(int i) { return (i >= 0 && i < 5) ? notas[i] : 0; }
    int getPeso(int i) { return (i >= 0 && i < 5) ? peso[i] : 0; }
    float promedioPonderado(){
        float suma = 0;
        int total_peso = 0;
        for (int i = 0; i < 5; i++){
            suma += notas[i] * peso[i];
            total_peso += peso[i];
        }
        return (total_peso > 0) ? suma / total_peso : 0;
    }
    void printAlumno(){
        print();
        cout << "Código: " << codigo << endl;
        for (int i = 0; i < 5; i++){
            cout << "Curso " << i + 1 << ": " << curso[i]
                 << " | Nota: " << notas[i]
                 << " | Peso: " << peso[i] << endl;
        }
        cout << "Promedio Ponderado: " << promedioPonderado() << endl;
    }
};
int main(){
    alumno_unmsm alumno;
    string nombre, estado_civil, codigo, curso;
    int edad, peso;
    char sexo;
    float nota;
    cout << "Ingrese nombre: ";
    getline(cin, nombre);
    alumno.setNombre(nombre);
    cout << "Ingrese edad: ";
    cin >> edad;
    alumno.setEdad(edad);
    cout << "Ingrese sexo (M/F): ";
    cin >> sexo;
    alumno.setSexo(sexo);
    cin.ignore();
    cout << "Ingrese estado civil: ";
    getline(cin, estado_civil);
    alumno.setEstadoCivil(estado_civil);
    cout << "Ingrese código de alumno: ";
    getline(cin, codigo);
    alumno.setCodigo(codigo);
    for (int i = 0; i < 5; i++){
        cout << "\nCurso " << i + 1 << ": ";
        getline(cin, curso);
        alumno.setCurso(i, curso);
        cout << "Nota: ";
        cin >> nota;
        alumno.setNota(i, nota);
        cout << "Peso (creditaje): ";
        cin >> peso;
        alumno.setPeso(i, peso);
        cin.ignore();
    }
    cout << "\n--- Datos del Alumno ---\n";
    alumno.printAlumno();
    return 0;
}*/

/* // Ejemplo 7
#include <iostream>
#include <cmath>
using namespace std;
// Mostrar el uso de funciones virtuales con respecto a la clase base
// Observe que area es una funcion virtual
class Base
{
public:
    virtual void area() = 0;
};
class Derivada1 : public Base
{
public:
    void area();
};
void Derivada1::area()
{ // area de un triangulo
    // puntos del triangulo
    float x1 = 2.0, x2 = 3.2, x3 = 2.8;
    float y1 = 1.5, y2 = 3.5, y3 = 0.5;
    float A = fabs((x1 * (y1 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0);
    cout << "\nEl area del triangulo es: " << A << endl;
}
class Derivada2 : public Base
{
public:
    void area();
};
void Derivada2::area()
{
    // area de un rectangulo
    float x1 = 0.0, x2 = 1.5, x3 = 1.5, x4 = 0.0;
    float y1 = 0.0, y2 = 0.0, y3 = 1.9, y4 = 1.9;
    float dist1, dist2;
    dist1 = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)); // largo
    dist2 = sqrt(pow(x3 - x4, 2) + pow(y3 - y4, 2)); // ancho
    float A = dist1 * dist2;
    cout << "\nEl area del rectangulo es: " << A << endl;
}
class Derivada3 : public Base
{
public:
    void area(); // area de un poligono
};
void Derivada3::area()
{
    int i;
    // puntos del poligono
    float x[6], y[6];
    x[0] = 0.0;
    y[0] = 0.0;
    x[1] = 3.0;
    y[1] = 0.0;
    x[2] = 3.5;
    y[2] = 1.0;
    x[3] = 3.0;
    y[3] = 2.0;
    x[4] = 2.0;
    y[4] = 2.0;
    x[5] = 0.0;
    y[5] = 1.0;
    float A = 0.0;
    for (i = 0; i < 6; i++)
    {
        A += (x[i] * y[i + 1]) - (x[i + 1] * y[i]);
    }
    cout << "El area del poligono es: " << A / 2.0 << endl;
}
int main()
{ // Herencia_Virtual.cpp
    Derivada1 deriv1;
    Derivada2 deriv2;
    Derivada3 deriv3;
    Base *ptr;     // puntero a la clase base
    ptr = &deriv1; // asignar direccion
    ptr->area();   // salida : area del triangulo
    ptr = &deriv2; // asignar direccion
    ptr->area();   // salida : area del rectangulo
    ptr = &deriv3; // asignar direccion
    ptr->area();   // salida : area del poligono
    cout << endl;
    return 0;
}*/

/* // Ejemplo 6
#include <iostream>
#include <conio.h>
using namespace std;
class Empleado
{
    int edad;

public:
    Empleado(int n) : edad(n) {}
    void setedad(int n) { edad = n; }
    int getedad() { return edad; }
};
class Asalariado : public Empleado
{
    float salario;

public:
    Asalariado(float sal = 0, int n = 0);
    void setsalario(float n) { salario = n; }
    float getsalario() { return salario; }
};
Asalariado::Asalariado(float sal, int n) : Empleado(n)
{
    salario = sal;
}
class Estudiante
{
    int ident, grado, edad;

public:
    Estudiante(int n1, int n2, int n3)
    {
        ident = n1;
        grado = n2;
        edad = n3;
    }
    void setident(int n) { ident = n; }
    int getident() { return ident; }
    void setgrado(int n) { grado = n; }
    int getgrado() { return grado; }
    void setedad(int n1) { edad = n1; }
    int getedad() { return edad; }
};
class Practicante : public Estudiante, public Asalariado
{
public:
    Practicante(int n1, int n2, int n3, float sal) : Estudiante(n1, n2, n3), Asalariado(sal) {}
    void print();
};
void Practicante::print()
{
    cout << "ident " << getident() << endl;
    cout << "edad " << Estudiante::getedad() << endl;
    cout << "grado " << getgrado() << endl;
    cout << "salario " << Asalariado::getsalario() << endl;
}
int main()
{ // Eduardo Raffo Lecca
    Practicante Pedro(2001, 5, 25, 1200);
    Pedro.print();
    return 0;
}*/

/* // Ejemplo 5
#include <iostream>
#include <cmath>
using namespace std;
class Punto
{ // Clase Base: Punto
public:
    Punto() {};
    Punto(int, int);
    ~Punto() {};
    void setx(int);
    void sety(int);
    int getx() const;
    int gety() const;
    friend double distancia(Punto, Punto);

protected:
    int x, y;
};
Punto::Punto(int a, int b)
{
    x = a;
    y = b;
}
int Punto::getx() const { return x; }
void Punto::setx(int a) { x = a; }
void Punto::sety(int b) { y = b; }
int Punto::gety() const { return y; }
double distancia(Punto p1, Punto p2)
{
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2));
}
// Clase Derivada: Punto3D
class Punto3D : public Punto
{
public:
    Punto3D() {}
    Punto3D(int, int, int);
    ~Punto3D() {};
    void setz(int);
    int getz();
    friend double distancia(Punto3D, Punto3D);

private:
    int z;
};
Punto3D::Punto3D(int x0, int y0, int z0) : Punto(x0, y0)
{
    z = z0;
}
int Punto3D::getz() { return z; }
void Punto3D ::setz(int z0) { z = z0; }
double distancia(Punto3D p1, Punto3D p2)
{
    return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2) + pow(p1.z - p2.z, 2));
}
int main()
{ // Herencia_Punto1.cpp
    Punto p1(1, 1), p2(2, 2);
    double dis;
    dis = distancia(p1, p2);
    cout << "Distancia con la Clase Punto:" << endl;
    cout << endl
         << "Punto2D" << endl;
    cout << "Coordenadas de p1: " << p1.getx() << "," << p1.gety() << ";" << endl;
    cout << "Coordenadas de p2: " << p2.getx() << "," << p2.gety() << ";" << endl;
    cout << "Distancia entre p1 y p2: " << dis << endl;
    Punto3D p3(2, 1, 3), p4(0, 0, 0);
    cout << endl
         << "Punto3D" << endl;
    cout << "Coordenadas de p3: " << p3.getx() << "," << p3.gety() << "," << p3.getz() << endl;
    cout << "Coordenadas de p4: " << p4.getx() << "," << p4.gety() << "," << p4.getz() << endl;
    dis = distancia(p3, p4);
    cout << "Distancia entre p3 y p4: " << dis << endl;
    return 0;
}*/

/* // Ejemplo 4
#include <iostream>
#include <string>
using namespace std;
// Muestra el concepto de clase base y clase derivada
// un auto es un vehiculo
class Vehiculo
{ // Clase base
private:
    int Peso, MaxVeloc;
    float Precio;

public:
    Vehiculo(int, int, float);
    ~Vehiculo();
    int getPeso();
    int getMaxVeloc();
    float getPrecio();
    void Print();
};
// Definicion de funciones miembro de la clase base
Vehiculo ::Vehiculo(int pe, int maxV, float prec)
{
    Peso = pe;
    MaxVeloc = maxV;
    Precio = prec;
}
// Esta implementación, aunque vacía, resuelve el error "undefined reference"
Vehiculo::~Vehiculo() {}
int Vehiculo ::getPeso() { return Peso; }
int Vehiculo ::getMaxVeloc() { return MaxVeloc; }
float Vehiculo ::getPrecio() { return Precio; }
// Print para la clase base
void Vehiculo ::Print()
{
    // Corrección de la impresión: usar "\n" en lugar de "n"
    cout << "\nPeso: " << Peso << " Kg";
    cout << "\nVelocidad Maxima: " << MaxVeloc << " Km/h";
    cout << "\nPrecio: " << Precio << " Dolares";
}
// Clase derivada Auto
class Auto : public Vehiculo
{
private:
    int NumeroCilindros, PotenciaCaballos, Desplazamiento;

public:
    Auto(int, int, float, int, int, int);
    int getNumeroCilindros();
    int getPotenciaCaballos();
    int getDesplazamiento();
    void Print();
};
// constructor para la clase derivada
Auto::Auto(int pre, int maxV, float prec, int NumCil, int PotCaba, int Despla)
    : Vehiculo(pre, maxV, prec)
{
    NumeroCilindros = NumCil;
    PotenciaCaballos = PotCaba;
    Desplazamiento = Despla;
}
int Auto::getNumeroCilindros() { return NumeroCilindros; }
int Auto::getPotenciaCaballos() { return PotenciaCaballos; }
int Auto::getDesplazamiento() { return Desplazamiento; }
// Print para la clase derivada
void Auto::Print()
{
    // Print para la clase base o padre
    Vehiculo::Print();
    cout << "\nNumero de Cilindros: " << NumeroCilindros;
    cout << "\nCaballos de Potencia: " << PotenciaCaballos;
    cout << "\nDesplazamiento: " << Desplazamiento << " cm cubicos";
}
int main()
{
    Vehiculo unVehiculo(4500, 120, 30000.00);
    cout << "\n--- Un Vehiculo ---";
    unVehiculo.Print();
    cout << endl;
    // ahora con un objeto derivado de vehiculo
    cout << "\n--- Un Auto ---";
    Auto unAuto(3500, 100, 12000.00, 6, 120, 3000);
    unAuto.Print();
    cout << endl
         << endl;
    return 0;
}*/

/* // Ejemplo 3
#include <iostream>
#include <cmath>
#include <iomanip> // para manipular la salida
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
using namespace std;
class angulo
{ // clase base
public:
    void set_ang(int ang) { a = ang; }
    int get_ang() { return a; }

private:
    int a;
};
// clases derivadas
class seno : public angulo
{
public:
    void valor(int ang);
};

class coseno : public angulo
{
public:
    void valor(int ang);
};
void seno::valor(int ang)
{
    set_ang(ang);
    cout << fixed << setprecision(4);
    cout << "Seno(" << get_ang() << ") : ";
    cout << sin(get_ang() * M_PI / 180) << endl;
}
void coseno::valor(int ang)
{
    set_ang(ang);
    cout << fixed << setprecision(4);
    cout << "Coseno(" << get_ang() << ") : ";
    cout << cos(get_ang() * M_PI / 180) << endl;
}
int main() // Herencia_Angulo_3.cpp
{
    seno esta;   // objeto de la clase seno
    coseno beta; // objeto de la clase coseno
    int angulo, n;
    cout << "Cuantos angulos? ";
    cin >> n;
    for (int i = 0; i < n; i++)
    {
        cout << "angulo: ";
        cin >> angulo;
        esta.valor(angulo);
        beta.valor(angulo);
        cout << endl;
    }
    cout << "\nFin del programa!" << endl;
    return 0;
}*/

/* // Ejemplo 2
#include <iostream>
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
using namespace std;
class angulo{ // base clase
public:
    void set_ang(int a){ang = a;}
    int get_ang() const{return ang;}
protected:
    int ang;
};
// clases derivadas seno y coseno
class seno : public angulo{
public:
    void valor(int ang);
};
class coseno : public angulo{
public:
    void valor(int ang);
};
void seno::valor(int ang){
    set_ang(ang);
    cout << "Seno " << get_ang() << " : ";
    cout << sin(get_ang() * M_PI / 180);
}
void coseno::valor(int ang){
    set_ang(ang);
    cout << "Coseno " << get_ang() << " : ";
    cout << cos(get_ang() * M_PI / 180);
}
int main(){
    seno alfa;   // objeto de la clase seno
    coseno beta; // objeto de la clase coseno
    alfa.valor(30);
    cout << endl;
    beta.valor(30);
    cout << endl;
    return 0;
}*/

/* // Ejemplo 1
#include <iostream>
#include <cmath>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
using namespace std;
class angulo{ // clase base
public:
    void set_ang(int ang) { a = ang; }
    int get_ang() { return a; }
private:
    int a;
};
class seno : public angulo{ // clase derivada
public:
    void valor(int ang);
};
void seno::valor(int ang){
    set_ang(ang);
    cout << "\nSeno(" << get_ang() << ") : ";
    cout << sin(get_ang() * M_PI / 180);
}
int main(){      // Herencia_Angulo_1.cpp
    seno x;      // objeto de la clase seno
    x.valor(90); // angulo de 90 grados
    cout << endl
         << endl;
    return 0;
}
*/