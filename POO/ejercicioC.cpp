#include <iostream>
using namespace std;
class Motor
{
public:
    void mover() const
    {
        cout << "El motor se activa y el robot avanza." << endl;
    }
};

class Aspiradora
{
public:
    void aspirar() const
    {
        cout << "La aspiradora comienza a succionar la suciedad." << endl;
    }
};

class RobotLimpiador
{
private:
    Motor motor;
    Aspiradora aspiradora;

public:
    void iniciarLimpieza() const
    {
        cout << "RobotLimpiador: Iniciando ciclo de limpieza." << endl;
        motor.mover();
        aspiradora.aspirar();
        cout << "RobotLimpiador: Ciclo de limpieza completado." << endl;
    }
};

int main()
{
    RobotLimpiador robot;
    robot.iniciarLimpieza();
    return 0;
}

// La composición ofrece varias ventajas significativas para la **mantenibilidad** del código:Flexibilidad, Acoplamiento y Reusabilidad
// herencia

/*
class FiguraGeometrica {
public:
    virtual double area() const = 0;
    virtual double perimetro() const = 0;

};

class Circulo : public FiguraGeometrica {
public:
    double radio;
    double area() const override;
    double perimetro() const override;
};

class Rectangulo : public FiguraGeometrica {
public:
    double ancho, alto;
    double area() const override;
    double perimetro() const override;
};*/
