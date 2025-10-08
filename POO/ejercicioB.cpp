#include <iostream> // Para entrada y salida estándar.
#include <vector>   // Para usar vector, un contenedor de datos dinamico.
#include <memory>   // Para punteros inteligentes, como unique_ptr.
#include <cmath>    // Para funciones matematias.
using namespace std;

struct Shape // Define una clase base abstracta llamada 'Shape'.
{
    // Destructor virtual. Es CRUCIAL para el polimorfismo.
    virtual ~Shape() = default;
    // Metodo virtual puro. Obliga a cualquier clase que herede de 'Shape' a proporcionar una
    // implementacion para el calculo del area. El '= 0' lo hace puro.
    virtual double area() const = 0;

    virtual double perimeter() const = 0; // metodo virtual para el perimetro.
};
// Define la clase 'Rectangle' que hereda publicamente de 'Shape'.
class Rectangle : public Shape
{
    double w_, h_; // Atributos privados para el ancho y la altura del rectangulo.
public:
    // Constructor que inicializa el ancho (w) y el alto (h).
    Rectangle(double w, double h) : w_(w), h_(h) {}
    // Implementacion del metodo 'area()'. La palabra clave 'override' garantiza
    // que estamos sobrescribiendo un metodo virtual de la clase base.
    double area() const override { return w_ * h_; }
    // Implementacion del metodo 'perimeter()'.
    double perimeter() const override { return 2 * (w_ + h_); }
};
// Define la clase 'Circle' que tambien hereda publicamente de 'Shape'.
class Circle : public Shape
{
    double r_; // Atributo privado para el radio del circulo.
    // 'static' significa que solo hay una copia para todos los objetos de la clase.
    // 'constexpr' asegura que se calcula en tiempo de compilacion.
    static constexpr double PI = 3.14159265358979323846;

public:
    // Constructor para el circulo. 'explicit' evita conversiones implicitas no deseadas.
    explicit Circle(double r) : r_(r) {}
    // Implementacion del metodo 'area()' para el circulo.
    double area() const override { return PI * r_ * r_; }
    double perimeter() const override { return 2 * PI * r_; }
};

int main() // La funcion principal
{
    // Crea un vector de punteros unicos (unique_ptr) a objetos 'Shape'.
    vector<unique_ptr<Shape>> shapes;
    // Crea un objeto 'Rectangle' en la memoria dinamica y lo añade al vector.
    shapes.emplace_back(make_unique<Rectangle>(4.0, 3.0));
    // Crea un objeto 'Circle' y lo añade al vector.
    shapes.emplace_back(make_unique<Circle>(2.5));
    // Bucle para iterar sobre cada puntero en el vector.
    for (const auto &s : shapes)
    {
        // el programa determina en tiempo de ejecucion si el objeto real es un 'Rectangle' o un
        // 'Circle' y llama al metodo 'area()' o 'perimeter()' correcto.
        cout << "A=" << s->area() << " | P=" << s->perimeter() << '\n';
    }
    return 0; // El programa termina con exito.
}

/*
// practica01_shape.cpp
#include <iostream>
#include <vector> //array
#include <memory> // pointers intel
#include <cmath>
using namespace std;
struct Shape
{
    virtual ~Shape() = default;
    virtual double area() const = 0;
    virtual double perimeter() const = 0;
};
class Rectangle : public Shape
{
    double w_, h_;

public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; } // override sobre
    double perimeter() const override { return 2 * (w_ + h_); }
};
class Circle : public Shape
{
    double r_;
    static constexpr double PI = 3.14159265358979323846; // constexpr tiempo de compilacion

public:
    explicit Circle(double r) : r_(r) {}
    double area() const override { return PI * r_ * r_; }
    double perimeter() const override { return 2 * PI * r_; }
};
int main()
{
    vector<unique_ptr<Shape>> shapes;
    shapes.emplace_back(make_unique<Rectangle>(4.0, 3.0));
    shapes.emplace_back(make_unique<Circle>(2.5));
    for (const auto &s : shapes)
    {
        cout << "A=" << s->area() << " | P=" << s->perimeter() << '\n';
    }
    return 0;
}*/
