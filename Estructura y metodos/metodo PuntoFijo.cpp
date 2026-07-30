// Juan Mamani Pari
// Metodo Punto Fijo
// Los epsilon son error de aproximacion (ejemplo: 0.0001)
#include <iostream>
using namespace std;
double raizCuadrada(double n)
{
    if (n < 0)
        return 1.0 / 0.0;
    if (n == 0)
        return 0.0;
    double x = n, y = 1.0, epsilon_local = 0.00000001;
    while (x - y > epsilon_local)
    {
        x = (x + y) / 2;
        y = n / x;
    }
    return x;
}
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
double valorAbsoluto(double val)
{
    return (val < 0) ? -val : val;
}
double raizN(double n, int indice)
{
    if (n < 0 && indice % 2 == 0)
        return 1.0 / 0.0;
    if (n == 0)
        return 0.0;
    double x = n;
    for (int i = 0; i < 100; ++i)
    {
        double x_anterior = x;
        x = (1.0 / indice) * ((indice - 1) * x + n / potencia(x, indice - 1));
        if (valorAbsoluto(x - x_anterior) < 0.00000001)
            break;
    }
    return x;
}

// Funcion para representar la función de iteración (Despeje)
struct FuncionPhi
{
    double a4, a3, a2, a1, a0;
    int grado_n;
    int opcion_phi;
    // F(x) = a4*x^4 + a3*x^3 + a2*x^2 + a1*x + a0
    double calcularFx(double x)
    {
        double resultado = 0.0;
        resultado += a0;
        if (grado_n >= 1)
            resultado += a1 * x;
        if (grado_n >= 2)
            resultado += a2 * x * x;
        if (grado_n >= 3)
            resultado += a3 * x * x * x;
        if (grado_n >= 4)
            resultado += a4 * x * x * x * x;
        return resultado;
    }
    double operator()(double x)
    {
        // Despejes ESPECÍFICOS (x^2 + x - 6 = 0)
        if (opcion_phi >= 1 && opcion_phi <= 4)
        {
            switch (opcion_phi)
            {
            case 1:
                // return raizCuadrada(((-1.2 * x * x * x) - (2.1 * x) + 0.7) / -3.5);
                return 6.0 - x * x;
            case 2:
                // return raizCuadrada(((3.5 * x * x) - (2.1 * x) + 0.7) / (1.2 * x));
                return raizCuadrada(6.0 - x);
            case 3:
                if (x == 0)
                    return 1.0 / 0.0;
                return (6.0 / x) - 1.0;
            case 4:
                if (x + 1.0 == 0)
                    return 1.0 / 0.0;
                return 6.0 / (x + 1.0);
            }
        }
        // Despejes GENÉRICOS
        else if (opcion_phi >= 5 && opcion_phi <= 6)
        {
            switch (opcion_phi)
            {
            // Caso 5: Despejar el término lineal (a1*x) -> x = x - f(x)/a1 (Si a1 es el más grande)
            case 5:
                if (a1 == 0)
                    return 1.0 / 0.0;
                return x - (calcularFx(x) / a1);

            // Caso 6: Despejar la constante (a0/...) - x = -a0 / (a4*x^3 + a3*x^2 + a2*x + a1)
            case 6:
            {
                double denominador = 0.0;
                if (grado_n >= 4)
                    denominador += a4 * potencia(x, 3);
                if (grado_n >= 3)
                    denominador += a3 * potencia(x, 2);
                if (grado_n >= 2)
                    denominador += a2 * x;
                denominador += a1;
                if (denominador == 0)
                    return 1.0 / 0.0;
                return -a0 / denominador;
            }
            }
        }
        return 1.0 / 0.0;
    }
};
// Verificación de Raíces Cuadráticas Exactas
void verificarRaicesCuadraticas(double a2, double a1, double a0, double x_aprox)
{
    if (a2 == 0)
        return;
    cout << "\n=============================================" << endl;
    cout << "VERIFICACION DE RAICES EXACTAS (SOLO PARA GRADO 2)" << endl;
    double discriminante = a1 * a1 - 4 * a2 * a0;
    if (discriminante >= 0)
    {
        double raiz_d = raizCuadrada(discriminante);
        if (raiz_d == 1.0 / 0.0)
        {
            cout << "La ecuacion tiene raices complejas. No se realiza verificacion simple." << endl;
            return;
        }
        double x1_exacta = (-a1 + raiz_d) / (2 * a2);
        double x2_exacta = (-a1 - raiz_d) / (2 * a2);
        cout << "Raiz 1 (x1) = " << x1_exacta << endl;
        cout << "Raiz 2 (x2) = " << x2_exacta << endl;
        double error1 = valorAbsoluto(x_aprox - x1_exacta);
        double error2 = valorAbsoluto(x_aprox - x2_exacta);
        cout << "\nEl valor aproximado se acerca ";
        if (error1 < error2)
        {
            cout << "a la Raiz 1 (Error: " << error1 << ")" << endl;
        }
        else
        {
            cout << "a la Raiz 2 (Error: " << error2 << ")" << endl;
        }
    }
    else
    {
        cout << "La ecuacion tiene raices complejas. No se realiza verificacion simple." << endl;
    }
    cout << "=============================================" << endl;
}
void metodoPuntoFijo()
{
    double x0, x1;
    double epsilon1, epsilon2;
    FuncionPhi phi = {0.0, 0.0, 0.0, 0.0, 0.0, 0, 0};
    int k = 0;
    cout << "--- Metodo del Punto Fijo (Polinomios de Grado 2, 3 o 4) ---" << endl;
    // 1. Entrada del Grado y Coeficientes
    do
    {
        cout << "Ingrese el GRADO N del polinomio (solo 2, 3 o 4): ";
        cin >> phi.grado_n;
    } while (phi.grado_n < 2 || phi.grado_n > 4);

    if (phi.grado_n == 4)
    {
        cout << "Ingrese a4 (x^4): ";
        cin >> phi.a4;
    }
    if (phi.grado_n >= 3)
    {
        cout << "Ingrese a3 (x^3): ";
        cin >> phi.a3;
    }
    if (phi.grado_n >= 2)
    {
        cout << "Ingrese a2 (x^2): ";
        cin >> phi.a2;
    }
    cout << "Ingrese a1 (x^1): ";
    cin >> phi.a1;
    cout << "Ingrese a0 (cte): ";
    cin >> phi.a0;
    // Impresión de la Ecuación (para verificación)
    cout << "\nEcuacion F(x): ";
    if (phi.a4 != 0)
        cout << phi.a4 << "x^4 + ";
    if (phi.a3 != 0)
        cout << phi.a3 << "x^3 + ";
    if (phi.a2 != 0)
        cout << phi.a2 << "x^2 + ";
    if (phi.a1 != 0)
        cout << phi.a1 << "x + ";
    cout << phi.a0 << " = 0" << endl;

    // 2. Selección de funciones extraidas del principal
    cout << "\nSeleccione el despeje phi(x) a usar:" << endl;
    cout << "Despejes ESPECIFICOS (Solo para F(x) = x^2 + x - 6 = 0)" << endl;
    cout << "1. x = 6 - x^2" << endl;
    cout << "2. x = sqrt(6 - x)" << endl;
    cout << "3. x = (6/x) - 1" << endl;
    cout << "4. x = 6 / (x + 1)" << endl;
    cout << "------------------------------------------------------------" << endl;
    cout << "5. Despeje GENERICO 1 (x = x - F(x)/a1)" << endl;
    cout << "6. Despeje GENERICO 2 (x = -a0 / (aN*x^(N-1) + ... + a1))" << endl;
    cout << "Opcion: ";
    cin >> phi.opcion_phi;
    // 3. Entrada de la aproximación inicial y error
    cout << "\nIngrese la aproximacion inicial (x0): ";
    cin >> x0;
    cout << "Ingrese la precision epsilon1 (|f(x)|): ";
    cin >> epsilon1;
    cout << "Ingrese la precision epsilon2 (|x_k - x_{k-1}|): ";
    cin >> epsilon2;
    if (valorAbsoluto(phi.calcularFx(x0)) < epsilon1)
    {
        cout << "\n--- Convergencia inmediata en x0. Raiz aproximada (x_bar): " << x0 << " ---" << endl;
        if (phi.grado_n == 2)
            verificarRaicesCuadraticas(phi.a2, phi.a1, phi.a0, x0);
        return;
    }
    // Paso 3. k = 1
    k = 1;
    cout << "\nIteraciones:" << endl;
    cout << "K\t X_k\t\t f(X_k)\t\t |Error Aproximacion|" << endl;

    // Bucle de Iteraciones
    while (true)
    {
        // Paso 4. x1 = phi(x0)
        x1 = phi(x0);
        double fx1 = phi.calcularFx(x1);
        double error_aproximacion = valorAbsoluto(x1 - x0);

        // Manejo de divergencias
        if (x1 == 1.0 / 0.0 || x1 == -1.0 / 0.0)
        {
            cout << "\n--- ERROR: El metodo diverge (posiblemente mala elección de phi) ---" << endl;
            return;
        }
        // SALIDA DE LAS ITERACIONES (Tabla)
        cout << k << "\t " << x1 << "\t\t " << valorAbsoluto(fx1) << "\t\t " << error_aproximacion << endl;

        // Paso 5. Condición de Parada
        if (valorAbsoluto(fx1) < epsilon1 || error_aproximacion < epsilon2)
        {
            cout << "\n--- Convergencia alcanzada y verificada ---" << endl;
            cout << "Raiz aproximada (x_bar): " << x1 << endl;
            cout << "Numero de iteraciones: " << k << endl;

            if (valorAbsoluto(fx1) < epsilon1)
            {
                cout << "Condicion cumplida: |f(x1)| < Epsilon1." << endl;
            }
            if (error_aproximacion < epsilon2)
            {
                cout << "Condicion cumplida: |x1 - x0| < Epsilon2." << endl;
            }
            break;
        }

        // Paso 6. x0 = x1
        x0 = x1;
        // Paso 7. k = k + 1, vuelva al paso 4
        k++;
    }

    if (phi.grado_n == 2)
    {
        verificarRaicesCuadraticas(phi.a2, phi.a1, phi.a0, x1);
    }
}
int main()
{
    char continuar_programa;
    do
    {
        metodoPuntoFijo();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}