#include <iostream>

using namespace std;

// --- Funciones Matemáticas Auxiliares ---

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
    return (val < 0) ? -val : val;
}

// --- Estructura para la Función y su Derivada (Hasta Grado 4) ---
struct FuncionRaphson
{
    // Coeficientes para la forma a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
    double a4, a3, a2, a1, a0;
    int grado_n;

    // Calcula la función original F(x)
    double calcularFx(double x)
    {
        double resultado = 0.0;

        resultado += a0; // i=0
        if (grado_n >= 1)
            resultado += a1 * x; // i=1
        if (grado_n >= 2)
            resultado += a2 * x * x; // i=2
        if (grado_n >= 3)
            resultado += a3 * x * x * x; // i=3
        if (grado_n >= 4)
            resultado += a4 * x * x * x * x; // i=4

        return resultado;
    }

    // Calcula la derivada F'(x) = 4a4*x^3 + 3a3*x^2 + 2a2*x + a1
    double calcularFPrimaX(double x)
    {
        double resultado = 0.0;

        // Derivada del término x^1
        if (grado_n >= 1)
            resultado += a1;

        // Derivada del término x^2 -> 2*a2*x
        if (grado_n >= 2)
            resultado += 2.0 * a2 * x;

        // Derivada del término x^3 -> 3*a3*x^2
        if (grado_n >= 3)
            resultado += 3.0 * a3 * x * x;

        // Derivada del término x^4 -> 4*a4*x^3
        if (grado_n >= 4)
            resultado += 4.0 * a4 * potencia(x, 3);

        return resultado;
    }
};

// --- Implementación del Método de Newton-Raphson ---
void metodoNewtonRaphson()
{
    double x0, epsilon;
    FuncionRaphson funcion = {0.0, 0.0, 0.0, 0.0, 0.0, 0}; // Inicializar a cero
    int k = 0;
    double x_anterior;
    double x_actual;

    cout << "--- Metodo de Newton-Raphson (Polinomios de Grado 2, 3 o 4) ---" << endl;

    // 1. Entrada del Grado y Coeficientes
    do
    {
        cout << "Ingrese el GRADO N del polinomio (solo 2, 3 o 4): ";
        cin >> funcion.grado_n;
    } while (funcion.grado_n < 2 || funcion.grado_n > 4);

    if (funcion.grado_n == 4)
    {
        cout << "Ingrese a4 (x^4): ";
        cin >> funcion.a4;
    }
    if (funcion.grado_n >= 3)
    {
        cout << "Ingrese a3 (x^3): ";
        cin >> funcion.a3;
    }
    if (funcion.grado_n >= 2)
    {
        cout << "Ingrese a2 (x^2): ";
        cin >> funcion.a2;
    }
    cout << "Ingrese a1 (x^1): ";
    cin >> funcion.a1;
    cout << "Ingrese a0 (cte): ";
    cin >> funcion.a0;

    // Impresión de la Ecuación (para verificación)
    cout << "\nEcuacion F(x): ";
    if (funcion.a4 != 0)
        cout << funcion.a4 << "x^4 + ";
    if (funcion.a3 != 0)
        cout << funcion.a3 << "x^3 + ";
    if (funcion.a2 != 0)
        cout << funcion.a2 << "x^2 + ";
    if (funcion.a1 != 0)
        cout << funcion.a1 << "x + ";
    cout << funcion.a0 << " = 0" << endl;

    // 2. Entrada de la aproximación inicial y precisión
    cout << "\nIngrese la aproximacion inicial (x0): ";
    cin >> x0;
    cout << "Ingrese la precision epsilon (error absoluto en |x_k - x_{k-1}|): ";
    cin >> epsilon;

    x_anterior = x0;
    k = 1;

    // Primer chequeo: Si la derivada es cero en x0, salimos inmediatamente.
    if (funcion.calcularFPrimaX(x0) == 0)
    {
        cout << "\n--- ERROR: La derivada f'(x) es cero en x0 = " << x0 << ". El metodo fallara. ---" << endl;
        return;
    }

    cout << "\nIteraciones:" << endl;
    cout << "k\t X_k\t\t f(X_k)\t\t f'(X_k)\t\t |Error Aproximado|" << endl;

    // Bucle de Iteraciones
    while (true)
    {
        double fx = funcion.calcularFx(x_anterior);
        double f_prima_x = funcion.calcularFPrimaX(x_anterior);

        // Chequeo de la derivada nula dentro del bucle
        if (f_prima_x == 0)
        {
            cout << "\n--- ERROR: La derivada f'(x) es cero en x = " << x_anterior << ". El metodo fallara. ---" << endl;
            return;
        }

        // Formula de Newton-Raphson: x_{k+1} = x_k - f(x_k) / f'(x_k)
        x_actual = x_anterior - (fx / f_prima_x);
        double error_aproximacion = valorAbsoluto(x_actual - x_anterior);

        // SALIDA DE LAS ITERACIONES (Tabla)
        cout << k << "\t " << x_actual << "\t\t " << fx << "\t\t " << f_prima_x << "\t\t " << error_aproximacion << endl;
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