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

// --- Estructura para la Función Polinómica (Generalizada hasta Grado 4) ---
struct FuncionSecante
{
    // Coeficientes para la forma a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
    double a4, a3, a2, a1, a0;
    int grado_n;

    // Calcula la función F(x)
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
            resultado += a4 * potencia(x, 4); // i=4

        return resultado;
    }
};

// --- Implementación del Método de la Secante ---
void metodoSecante()
{
    double x_anterior, x_actual, x_siguiente;
    double epsilon1, epsilon2;
    // Inicialización generalizada
    FuncionSecante funcion = {0.0, 0.0, 0.0, 0.0, 0.0, 0};
    int k = 0;
    double fx_anterior, fx_actual;

    cout << "--- Metodo de la Secante (Polinomios de Grado 2, 3 o 4) ---" << endl;

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

    // 2. Entrada de las aproximaciones iniciales y precisiones
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

    // 3. Verificación de convergencia inmediata en x0
    if (valorAbsoluto(fx_anterior) < epsilon1)
    {
        cout << "\n--- Convergencia inmediata en x0 ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_anterior << endl;
        return;
    }

    // 4. Verificación de convergencia en x1
    double error_x1_x0 = valorAbsoluto(x_actual - x_anterior);
    if (valorAbsoluto(fx_actual) < epsilon1 || error_x1_x0 < epsilon2)
    {
        cout << "\n--- Convergencia en x1 ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_actual << endl;
        return;
    }

    // Inicio de las iteraciones
    k = 1;

    cout << "\nIteraciones:" << endl;
    cout << "k\t x_k\t\t f(x_k)\t\t |x_k - x_{k-1}|" << endl;

    // Mostrar la segunda aproximación como el inicio de la tabla (k=1)
    cout << "1\t " << x_actual << "\t " << fx_actual << "\t " << error_x1_x0 << endl;

    // Bucle para k=2, 3, 4...
    while (true)
    {

        // 5. Manejo del denominador (f(x_actual) - f(x_anterior)) = 0
        if (fx_actual == fx_anterior)
        {
            cout << "\n--- ERROR: f(x_k) es igual a f(x_{k-1}). La secante es horizontal y el metodo fallara. ---" << endl;
            return;
        }

        // 6. Formula de la Secante
        // x_siguiente = x_actual - f(x_actual) * (x_actual - x_anterior) / (f(x_actual) - f(x_anterior))
        x_siguiente = x_actual - (fx_actual * (x_actual - x_anterior)) / (fx_actual - fx_anterior);

        double fx_siguiente = funcion.calcularFx(x_siguiente);
        double error_aproximacion = valorAbsoluto(x_siguiente - x_actual);

        // SALIDA DE LA ITERACIÓN ACTUAL (k+1)
        cout << k + 1 << "\t " << x_siguiente << "\t " << fx_siguiente << "\t " << error_aproximacion << endl;

        // 7. Condición de Parada
        if (valorAbsoluto(fx_siguiente) < epsilon1 || error_aproximacion < epsilon2)
        {

            cout << "\n--- Convergencia alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x_siguiente << endl;
            cout << "Numero de iteraciones: " << k + 1 << endl;

            if (valorAbsoluto(fx_siguiente) < epsilon1)
            {
                cout << "Condicion cumplida: |f(x_k)| < " << epsilon1 << " (Epsilon1)." << endl;
            }
            if (error_aproximacion < epsilon2)
            {
                cout << "Condicion cumplida: |x_k - x_{k-1}| < " << epsilon2 << " (Epsilon2)." << endl;
            }
            break;
        }

        // 8. Actualización de las variables para la próxima iteración (x_{k-1} = x_k, x_k = x_{k+1})
        x_anterior = x_actual;
        fx_anterior = fx_actual;
        x_actual = x_siguiente;
        fx_actual = fx_siguiente;

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