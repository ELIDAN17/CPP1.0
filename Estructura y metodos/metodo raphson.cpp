#include <iostream>

using namespace std;

// Función para elevar un número a una potencia entera
double potencia(double base, int exponente)
{
    if (exponente == 0)
        return 1.0;
    if (exponente < 0)
        return 1.0 / potencia(base, -exponente);
    double resultado = 1.0;
    for (int i = 0; i < exponente; ++i)
    {
        resultado *= base;
    }
    return resultado;
}

// Función para el valor absoluto
double valorAbsoluto(double val)
{
    if (val < 0)
    {
        return -val;
    }
    return val;
}

// --- Estructura para la Función y su Derivada ---
struct FuncionGeneral
{
    double a, b, c;
    int n;

    // Calcula la función f(x) = a*x^n + b*x + c
    double calcularFx(double x)
    {
        return a * potencia(x, n) + b * x + c;
    }

    // Calcula la derivada f'(x) = a*n*x^(n-1) + b
    double calcularDerivada(double x)
    {
        // Si n=1, el exponente de x es 0 (potencia(x, 0)=1), la derivada es a*1 + b. Correcto.
        // Si n=0, la derivada es 0 + b. Correcto (c*x^0 + b*x + c).
        return a * n * potencia(x, n - 1) + b;
    }
};

// --- Implementación del Método de Newton-Raphson ---
void metodoNewtonRaphson()
{
    double x0, epsilon;
    FuncionGeneral funcion;
    int k = 1;
    double x_anterior;
    double x_actual;

    cout << "--- Metodo de Newton-Raphson (para f(x) = a*x^n + b*x + c) ---" << endl;

    // 1. Entrada de la función polinómica
    cout << "Ingrese el exponente n (ej: 3 para cubica): ";
    cin >> funcion.n;
    cout << "Ingrese el coeficiente a: ";
    cin >> funcion.a;
    cout << "Ingrese el coeficiente b: ";
    cin >> funcion.b;
    cout << "Ingrese el coeficiente c: ";
    cin >> funcion.c;
    cout << "Ecuacion: " << funcion.a << "x^" << funcion.n << " + " << funcion.b << "x + " << funcion.c << " = 0" << endl;

    // 2. Entrada de la aproximación inicial y precisión
    cout << "\nIngrese la aproximacion inicial (x0): ";
    cin >> x0;
    cout << "Ingrese la precision epsilon (error absoluto en |x_k - x_{k-1}|): ";
    cin >> epsilon;

    x_anterior = x0;

    cout << "\nIteraciones:" << endl;
    cout << "k\t x_k\t\t f(x_k)\t\t f'(x_k)\t |x_k - x_{k-1}|" << endl;

    // Bucle de Iteraciones
    while (true)
    {
        double fx = funcion.calcularFx(x_anterior);
        double f_prima_x = funcion.calcularDerivada(x_anterior);

        // Manejo de la derivada nula (posible punto de inflexión)
        if (f_prima_x == 0)
        {
            cout << "\n--- ERROR: La derivada f'(x) es cero en x = " << x_anterior << ". El metodo fallara. ---" << endl;
            return;
        }

        // Formula de Newton-Raphson: x_{k+1} = x_k - f(x_k) / f'(x_k)
        x_actual = x_anterior - (fx / f_prima_x);

        double error_aproximacion = valorAbsoluto(x_actual - x_anterior);

        // SALIDA DE LAS ITERACIONES (Tabla)
        cout << k << "\t " << x_actual << "\t " << fx << "\t " << f_prima_x << "\t ";
        if (k > 0)
        {
            cout << error_aproximacion;
        }
        cout << endl;
        // -----------------------------

        // Condición de Parada: |x_k - x_{k-1}| < epsilon
        if (error_aproximacion < epsilon)
        {
            cout << "\n--- Convergencia alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x_actual << endl;
            cout << "Numero de iteraciones: " << k << endl;
            cout << "Condicion cumplida: |x_k - x_{k-1}| = " << error_aproximacion << " < " << epsilon << " (Epsilon)." << endl;
            break;
        }

        x_anterior = x_actual;
        k++;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoNewtonRaphson();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}