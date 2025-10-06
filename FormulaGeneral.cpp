// JUAN MAMANI PARI
// metodo newton-raphson
// guia de implementacion: https://www.youtube.com/watch?v=JbbY37AAiN0
// Implementacion de la formula general para ecuaciones cuadraticas
// Guia de implementacion para truncar y redondear
// https://www.youtube.com/watch?v=svwNYKFQxUM
#include <iostream>
using namespace std;
double truncar(double valor, int decimales)
{
    long long factor = 1;
    for (int i = 0; i < decimales; ++i)
    {
        factor *= 10;
    }
    long long numeroEntero = static_cast<long long>(valor * factor);
    return static_cast<double>(numeroEntero) / factor;
}
double redondear(double valor, int decimales)
{
    long long factor = 1;
    for (int i = 0; i < decimales; ++i)
    {
        factor *= 10;
    }
    double valor_redondeado = valor * factor;
    if (valor_redondeado >= 0)
    {
        return static_cast<double>(static_cast<long long>(valor_redondeado + 0.5)) / factor;
    }
    else
    {
        return static_cast<double>(static_cast<long long>(valor_redondeado - 0.5)) / factor;
    }
}
double raizCuadrada(double n)
{
    if (n < 0)
    {
        return -1.0;
    }
    if (n == 0)
    {
        return 0.0;
    }
    double x = n;
    double y = 1.0;
    double epsilon = 0.000001; // Precisión deseada
    while (x - y > epsilon)
    {
        x = (x + y) / 2;
        y = n / x;
    }
    return x;
}

int main()
{
    char continuar;
    do
    {
        double a, b, c;
        int digitos;
        cout << "Ingresa los coeficientes de la ecuacion cuadratica (ax^2 + bx + c = 0):" << endl;
        cout << "Coeficiente a: ";
        cin >> a;
        cout << "Coeficiente b: ";
        cin >> b;
        cout << "Coeficiente c: ";
        cin >> c;

        if (a == 0)
        {
            cout << "Error: El coeficiente 'a' no puede ser cero." << endl;
        }
        else
        {
            double discriminante = b * b - 4 * a * c;
            cout << "Ingresa la cantidad de digitos decimales para truncar/redondear: ";
            cin >> digitos;
            if (discriminante > 0)
            {
                double raiz_d = raizCuadrada(discriminante);
                double x1 = (-b + raiz_d) / (2 * a);
                double x2 = (-b - raiz_d) / (2 * a);
                cout << "La ecuacion tiene dos soluciones reales y distintas:" << endl;
                cout << "x1 (truncado) = " << truncar(x1, digitos) << endl;
                cout << "x1 (redondeado) = " << redondear(x1, digitos) << endl;
                cout << "x2 (truncado) = " << truncar(x2, digitos) << endl;
                cout << "x2 (redondeado) = " << redondear(x2, digitos) << endl;
            }
            else if (discriminante == 0)
            {
                double x = -b / (2 * a);
                cout << "La ecuacion tiene una unica solucion real:" << endl;
                cout << "x (truncado) = " << truncar(x, digitos) << endl;
                cout << "x (redondeado) = " << redondear(x, digitos) << endl;
            }
            else
            {
                double parteReal = -b / (2 * a);
                double parteImaginaria = raizCuadrada(-discriminante) / (2 * a);
                cout << "La ecuacion tiene dos soluciones complejas:" << endl;
                cout << "x1 (truncado) = " << truncar(parteReal, digitos) << " + " << truncar(parteImaginaria, digitos) << "i" << endl;
                cout << "x1 (redondeado) = " << redondear(parteReal, digitos) << " + " << redondear(parteImaginaria, digitos) << "i" << endl;
                cout << "x2 (truncado) = " << truncar(parteReal, digitos) << " - " << truncar(parteImaginaria, digitos) << "i" << endl;
                cout << "x2 (redondeado) = " << redondear(parteReal, digitos) << " - " << redondear(parteImaginaria, digitos) << "i" << endl;
            }
        }
        cout << "¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar;
    } while (continuar == 'S' || continuar == 's');
    cout << "Programa terminado." << endl;
    return 0;
}
