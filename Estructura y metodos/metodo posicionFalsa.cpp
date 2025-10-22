// Juan Mamani Pari
// Metodo Posicion Falsa
// Los epsilon son error de aproximacion (ejemplo: 0.0001)
#include <iostream>
using namespace std;
// Función para elevar un número a una potencia entera
double potencia(double base, int exponente)
{
    if (exponente == 0)
        return 1.0;
    if (exponente < 0)
        return 1.0 / potencia(base, -exponente);

    // Optimizamos para los grados 2, 3 y 4
    if (exponente == 1)
        return base;
    if (exponente == 2)
        return base * base;
    if (exponente == 3)
        return base * base * base;
    if (exponente == 4)
        return base * base * base * base;

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

// Estructura para la Función Polinómica
struct FuncionPosicionFalsa
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
            resultado += a2 * potencia(x, 2); // i=2
        if (grado_n >= 3)
            resultado += a3 * potencia(x, 3); // i=3
        if (grado_n >= 4)
            resultado += a4 * potencia(x, 4); // i=4

        return resultado;
    }
};

// Implementación del Método de la Posición Falsa
void metodoPosicionFalsa()
{
    double a, b, epsilon1, epsilon2;
    double x_actual;

    FuncionPosicionFalsa funcion = {0.0, 0.0, 0.0, 0.0, 0.0, 0};
    int k = 0;
    double fa, fb;
    double fx_actual;

    cout << "--- Metodo de la Posicion Falsa (Polinomios de Grado 2, 3 o 4) ---" << endl;

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

    // 2. Entrada del intervalo inicial y precisiones
    cout << "\nIngrese el limite inferior del intervalo (a): ";
    cin >> a;
    cout << "Ingrese el limite superior del intervalo (b): ";
    cin >> b;
    cout << "Ingrese la precision epsilon1 (|f(x)|): ";
    cin >> epsilon1;
    cout << "Ingrese la precision epsilon2 (|b - a|): ";
    cin >> epsilon2;
    fa = funcion.calcularFx(a);
    fb = funcion.calcularFx(b);
    // Verificar condición inicial f(a)f(b) < 0
    if (fa * fb >= 0)
    {
        cout << "\n--- ERROR: La funcion debe tener signos opuestos en los limites del intervalo." << endl;
        cout << "f(a)=" << fa << ", f(b)=" << fb << ". Por favor, ingrese otro intervalo. ---" << endl;
        return;
    }
    // 3. Verificaciones iniciales (para usar las nuevas variables epsilon)
    if ((b - a) < epsilon2)
    {
        double x_aprox = (a + b) / 2.0;
        cout << "\n--- El intervalo inicial ya cumple con la precision epsilon2 (|b-a|). ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
        return;
    }
    if (valorAbsoluto(fa) < epsilon1 || valorAbsoluto(fb) < epsilon1)
    {
        double x_aprox = (valorAbsoluto(fa) < epsilon1) ? a : b;
        cout << "\n--- Uno de los limites iniciales ya cumple con la precision epsilon1 (|f(x)|). ---" << endl;
        cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
        return;
    }
    // 4. k = 1
    k = 1;

    cout << "\nIteraciones:" << endl;
    cout << "k\t a\t\t b\t\t x_nuevo\t f(x_nuevo)\t |b - a|" << endl;

    // Bucle de Iteraciones
    while (true)
    {
        double denominador = fb - fa;
        // Manejo del denominador (f(b) - f(a)) = 0
        if (denominador == 0)
        {
            cout << "\n--- ERROR: El denominador f(b) - f(a) es cero. El metodo fallara. ---" << endl;
            return;
        }

        // 5. Formula de la Posición Falsa: x = (a*f(b) - b*f(a)) / (f(b) - f(a))
        // Nota: Fórmula equivalente a x_r = b - (f(b) * (b - a)) / (f(b) - f(a))
        x_actual = (a * fb - b * fa) / denominador;
        fx_actual = funcion.calcularFx(x_actual);

        // SALIDA DE LA ITERACIÓN
        cout << k << "\t " << a << "\t " << b << "\t " << x_actual << "\t " << fx_actual << "\t " << (b - a) << endl;

        // 6. Si |f(x)| < epsilon1, fin.
        if (valorAbsoluto(fx_actual) < epsilon1)
        {

            cout << "\n--- Convergencia por |f(x)| alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x_actual << endl;
            cout << "Numero de iteraciones: " << k << endl;
            cout << "Condicion cumplida: |f(x)| = " << valorAbsoluto(fx_actual) << " < " << epsilon1 << " (Epsilon1)." << endl;
            break;
        }

        // 7. Si f(a) * f(x) > 0, haga a = x y f(a) = f(x)
        if (fa * fx_actual > 0)
        {
            a = x_actual;
            fa = fx_actual;
        }
        // 8. Si f(a) * f(x) <= 0, haga b = x y f(b) = f(x)
        else
        {
            b = x_actual;
            fb = fx_actual;
        }

        // 9. Si b - a < epsilon2, fin.
        if ((b - a) < epsilon2)
        {
            double x_aprox = (a + b) / 2.0;
            cout << "\n--- Convergencia por intervalo |b - a| alcanzada y verificada ---" << endl;
            cout << "El intervalo final es: [" << a << ", " << b << "]" << endl;
            cout << "Raiz aproximada (x_bar): " << x_aprox << endl;
            cout << "Numero de iteraciones: " << k << endl;
            cout << "Condicion cumplida: |b - a| = " << (b - a) << " < " << epsilon2 << " (Epsilon2)." << endl;
            break;
        }

        // 10. k = k + 1
        k++;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoPosicionFalsa();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}