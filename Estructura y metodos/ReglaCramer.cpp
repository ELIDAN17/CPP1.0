#include <iostream>

using namespace std;

// Definición del tamaño de la matriz (N x N)
const int N = 3;

// --- Funcion Auxiliar: Determinante 3x3 ---
double calcularDeterminante(double M[N][N])
{
    // a11 * (a22*a33 - a23*a32)
    double det_a11 = M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]);

    // - a12 * (a21*a33 - a23*a31)
    double det_a12 = M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]);

    // + a13 * (a21*a32 - a22*a31)
    double det_a13 = M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]);

    return det_a11 - det_a12 + det_a13;
}

// --- Metodo de la Regla de Cramer ---
void metodoCramer()
{
    // Matriz de coeficientes A (3x3).
    double A[N][N] = {
        {2, 1, 1},
        {1, 3, 2},
        {3, 2, 4}};
    // Vector de términos constantes b.
    double b[N] = {12, 19, 30};

    double det_A;
    double soluciones[N];

    cout << "--- Metodo de la Regla de Cramer (Sistema 3x3) ---" << endl;

    // 1. Calcular el Determinante de la Matriz de Coeficientes A
    det_A = calcularDeterminante(A);

    cout << "Determinante principal (Det(A)): " << det_A << endl;

    if (det_A == 0)
    {
        cout << "\n--- ERROR: Det(A) es cero. El sistema no tiene solucion unica. ---" << endl;
        return;
    }

    // 2. Calcular los Determinantes A_i y las Soluciones x_i
    for (int i = 0; i < N; i++)
    { // i = 0 para x1, i = 1 para x2, i = 2 para x3

        // Crear la matriz A_i (Copia de A)
        double A_i[N][N];
        for (int r = 0; r < N; r++)
        {
            for (int c = 0; c < N; c++)
            {
                A_i[r][c] = A[r][c];
            }
        }

        // Reemplazar la columna i de A_i por el vector de constantes b
        for (int r = 0; r < N; r++)
        {
            A_i[r][i] = b[r];
        }

        // Calcular el determinante de la matriz modificada
        double det_A_i = calcularDeterminante(A_i);

        // Calcular la solucion x_i = Det(A_i) / Det(A)
        soluciones[i] = det_A_i / det_A;

        cout << "Determinante de A" << i + 1 << ": " << det_A_i << endl;
    }

    // 3. Mostrar la Solución Final
    cout << "\n--- Solucion Final ---" << endl;
    for (int i = 0; i < N; i++)
    {
        cout << "x" << i + 1 << " = " << soluciones[i] << endl;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        metodoCramer();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}