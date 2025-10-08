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

// --- Estructura para la Función Polinómica ---
struct FuncionGeneral
{
    double a, b, c;
    int n;

    // Calcula la función f(x) = a*x^n + b*x + c
    double calcularFx(double x)
    {
        return a * potencia(x, n) + b * x + c;
    }
};

// --- Implementación del Método de la Secante ---
void metodoSecante()
{
    double x_anterior, x_actual, x_siguiente;
    double epsilon1, epsilon2;
    FuncionGeneral funcion;
    int k = 0; // Se inicializa en 0 para x0, x1 y luego k=1 para x2
    double fx_anterior, fx_actual;

    cout << "--- Metodo de la Secante (para f(x) = a*x^n + b*x + c) ---" << endl;

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

    // 1. Entrada de las aproximaciones iniciales y precisiones
    cout << "\nIngrese la primera aproximacion inicial (x0): ";
    cin >> x_anterior;
    cout << "Ingrese la segunda aproximacion inicial (x1): ";
    cin >> x_actual;
    cout << "Ingrese la precision epsilon1 (|f(x)|): ";
    cin >> epsilon1;
    cout << "Ingrese la precision epsilon2 (|x_k - x_{k-1}|): ";
    cin >> epsilon2;

    // Calculos iniciales
    fx_anterior = funcion.calcularFx(x_anterior);
    fx_actual = funcion.calcularFx(x_actual);

    // 2. Si |f(x0)| < epsilon1, haga x_bar = x0 Fin.
    if (valorAbsoluto(fx_anterior) < epsilon1)
    {
        cout << "\n--- Convergencia inmediata en x0 ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_anterior << endl;
        return;
    }

    // 3. Si |f(x1)| < epsilon1 o |x1 - x0| < epsilon2 entonces haga x_bar = x1 Fin.
    if (valorAbsoluto(fx_actual) < epsilon1 || valorAbsoluto(x_actual - x_anterior) < epsilon2)
    {
        cout << "\n--- Convergencia en x1 ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_actual << endl;
        return;
    }

    // Inicio de las iteraciones
    k = 1;

    cout << "\nIteraciones:" << endl;
    cout << "k\t x_k\t\t f(x_k)\t\t |x_k - x_{k-1}|" << endl;

    // Mostrar la segunda aproximación como el inicio de la tabla
    cout << "1\t " << x_actual << "\t " << fx_actual << "\t " << valorAbsoluto(x_actual - x_anterior) << endl;

    // Bucle para k=2, 3, 4... (donde x_k es el x_siguiente)
    while (true)
    {

        // Manejo del denominador (f(x1) - f(x0)) = 0
        if (fx_actual == fx_anterior)
        {
            cout << "\n--- ERROR: f(x_k) es igual a f(x_{k-1}). El metodo fallara por division por cero. ---" << endl;
            return;
        }

        // 5. Formula de la Secante: x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x_siguiente = x_actual - (fx_actual * (x_actual - x_anterior)) / (fx_actual - fx_anterior);

        double fx_siguiente = funcion.calcularFx(x_siguiente);
        double error_aproximacion = valorAbsoluto(x_siguiente - x_actual);

        // 6. Si |f(x2)| < epsilon1 o |x2 - x1| < epsilon2 entonces haga x_bar = x2 Fin.
        if (valorAbsoluto(fx_siguiente) < epsilon1 || error_aproximacion < epsilon2)
        {

            // SALIDA DE LA ÚLTIMA ITERACIÓN
            cout << k + 1 << "\t " << x_siguiente << "\t " << fx_siguiente << "\t " << error_aproximacion << endl;

            cout << "\n--- Convergencia alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x_siguiente << endl;
            cout << "Numero de iteraciones: " << k + 1 << endl;

            if (valorAbsoluto(fx_siguiente) < epsilon1)
            {
                cout << "Condicion cumplida: |f(x_k)| = " << valorAbsoluto(fx_siguiente) << " < " << epsilon1 << " (Epsilon1)." << endl;
            }
            if (error_aproximacion < epsilon2)
            {
                cout << "Condicion cumplida: |x_k - x_{k-1}| = " << error_aproximacion << " < " << epsilon2 << " (Epsilon2)." << endl;
            }
            break;
        }

        // 7. x0 = x1 y x1 = x2
        // 8. k = k + 1, vuelva al paso 5
        x_anterior = x_actual;
        fx_anterior = fx_actual;
        x_actual = x_siguiente;
        fx_actual = fx_siguiente; // f(x2) se convierte en f(x1) para la próxima iteración

        // Muestra la iteración actual (x2) antes de que se convierta en x1 para el siguiente paso
        cout << k + 1 << "\t " << x_siguiente << "\t " << fx_siguiente << "\t " << error_aproximacion << endl;
        k++;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoSecante();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}