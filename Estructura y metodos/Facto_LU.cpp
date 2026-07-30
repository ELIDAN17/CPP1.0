#include <iostream>

using namespace std;

// Definición del tamaño de la matriz (N x N)
const int N = 3;

// Función auxiliar para imprimir la matriz
void imprimirMatriz(double M[N][N])
{
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            cout << M[i][j] << "\t";
        }
        cout << endl;
    }
    cout << "----------------------------------" << endl;
}

// --- Método de Factorización LU ---
void factorizacionLU()
{
    // Matriz de ejemplo A (3x3).
    double A[N][N] = {
        {2, 1, 1},
        {4, 1, 0},
        {-2, 2, 1}};

    // Matriz U: Inicialmente A. Al final, Matriz Triangular Superior.
    double U[N][N];
    // Matriz L: Inicialmente con ceros, llenaremos los multiplicadores.
    double L[N][N];

    // Inicializar U con A y L con la identidad (unos en la diagonal, ceros en el resto)
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            U[i][j] = A[i][j];
            L[i][j] = (i == j) ? 1.0 : 0.0;
        }
    }

    cout << "--- Metodo de Factorizacion LU (3x3) ---" << endl;
    cout << "Matriz A inicial:" << endl;
    imprimirMatriz(A);

    // 1. Fase de Eliminación (Construye U y L simultáneamente)
    for (int k = 0; k < N - 1; k++)
    { // k es el pivote (fila actual)

        // Verificación de Pivote
        if (U[k][k] == 0)
        {
            cout << "Error: Pivote cero. La factorizacion LU sin pivoteo falla." << endl;
            return;
        }

        // Eliminar elementos debajo del pivote U[k][k]
        for (int i = k + 1; i < N; i++)
        { // Filas debajo del pivote

            // Calculo del multiplicador m_ik
            double multiplicador = U[i][k] / U[k][k];

            // Guardar el multiplicador en L[i][k]
            L[i][k] = multiplicador;

            // Operación: U[i] = U[i] - multiplicador * U[k]
            for (int j = k; j < N; j++)
            {
                U[i][j] -= multiplicador * U[k][j];
            }
        }
    }

    cout << "\n--- Resultado ---" << endl;

    cout << "Matriz L (Triangular Inferior):" << endl;
    imprimirMatriz(L);

    cout << "Matriz U (Triangular Superior):" << endl;
    imprimirMatriz(U);

    // Nota: Para una verificación completa, se podría multiplicar L*U y compararla con A.
}

int main()
{
    char continuar_programa;
    do
    {
        factorizacionLU();
        cout << "\n¿Deseas realizar otra operacion? (S/N): ";
        cin >> continuar_programa;
    } while (continuar_programa == 'S' || continuar_programa == 's');

    cout << "Programa terminado." << endl;
    return 0;
}
