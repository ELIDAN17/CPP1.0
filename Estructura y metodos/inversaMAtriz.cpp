#include <iostream>

using namespace std;

// Definición de las constantes GLOBALES (N=filas, M=columnas de la matriz aumentada)
const int N = 3;
const int M = 2 * N; // M = 6 (3 de A + 3 de I)

// --- Función auxiliar para imprimir la matriz AUMENTADA ---
// IMPORTANTE: Los corchetes deben usar las constantes globales (N y M)
void imprimirMatriz(double Mtx[N][M])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            cout << Mtx[i][j] << "\t";
            // Separador visual entre A y I
            if (j == N - 1)
            {
                cout << "| \t";
            }
        }
        cout << endl;
    }
    cout << "--------------------------------------" << endl;
}

// --- Método de la Inversa (Usando Gauss-Jordan Aumentado) ---
void inversaMatrices()
{
    // Matriz Aumentada [A | I]
    double A_Aumentada[N][M];

    // Matriz de ejemplo A (Debe ser invertible)
    double A_ejemplo[N][N] = {
        {1, 2, 3},
        {0, 1, 4},
        {5, 6, 0}};

    // 1. Inicializar la Matriz Aumentada (A | I)
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < M; j++)
        {
            if (j < N)
            {
                // Copiar la matriz A al lado izquierdo
                A_Aumentada[i][j] = A_ejemplo[i][j];
            }
            else
            {
                // Colocar la Matriz Identidad I al lado derecho
                A_Aumentada[i][j] = (j == i + N) ? 1.0 : 0.0;
            }
        }
    }

    cout << "--- Calculo de la Inversa (Gauss-Jordan Aumentado 3x6) ---" << endl;
    cout << "Matriz Aumentada inicial [A | I]:" << endl;
    imprimirMatriz(A_Aumentada);

    // 2. Fase de Eliminación (Aplicar Gauss-Jordan a la matriz N x M)
    for (int k = 0; k < N; k++)
    { // k es el pivote (columna/fila)

        // **A. Normalización del Pivote**
        double pivotValue = A_Aumentada[k][k];
        if (pivotValue == 0)
        {
            cout << "\n--- ERROR: Pivote cero. La matriz no es invertible o requiere pivoteo de filas. ---" << endl;
            return;
        }
        for (int j = k; j < M; j++)
        {
            A_Aumentada[k][j] /= pivotValue;
        }

        // **B. Eliminación de Elementos** (Hacer ceros por encima y por debajo)
        for (int i = 0; i < N; i++)
        {
            if (i != k)
            { // Saltar la fila del pivote
                double factor = A_Aumentada[i][k];
                for (int j = k; j < M; j++)
                {
                    A_Aumentada[i][j] -= factor * A_Aumentada[k][j];
                }
            }
        }
    }

    cout << "\nMatriz Final en forma [I | A^-1]:" << endl;
    imprimirMatriz(A_Aumentada);

    // 3. Extracción de la Inversa (El lado derecho)
    cout << "--- Matriz Inversa (A^-1) ---" << endl;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            // La inversa está en las columnas N, N+1, N+2...
            cout << A_Aumentada[i][j + N] << "\t";
        }
        cout << endl;
    }
}

int main()
{
    char continuar_programa;
    do
    {
        inversaMatrices();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}