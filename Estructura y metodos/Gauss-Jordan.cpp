#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3

int main()
{
    double A[N][N + 1]; // Matriz aumentada para el sistema Ax = b
    char continuar;
    do
    {
        cout << "\n--- METODO GAUSS-JORDAN (SISTEMA 3x3) ---" << endl;
        for (int i = 0; i < N; i++)
        {
            cout << "Fila " << i + 1 << ":" << endl;
            for (int j = 0; j < N; j++)
            {
                cout << "  Coeficiente x" << j + 1 << ": ";
                cin >> A[i][j];
            }
            cout << "  Termino independiente (b): ";
            cin >> A[i][N];
        }
        for (int k = 0; k < N; k++)
        {
            if (A[k][k] == 0)
            {
                cout << "Error: Pivote cero. No se puede resolver." << endl;
                return 0;
            }
            double pivote = A[k][k];
            for (int j = k; j < N + 1; j++)
            {
                A[k][j] /= pivote;
            }
            for (int i = 0; i < N; i++)
            {
                if (i != k)
                {
                    double factor = A[i][k];
                    for (int j = k; j < N + 1; j++)
                    {
                        A[i][j] -= factor * A[k][j];
                    }
                }
            }
        }
        cout << "\n--- RESULTADOS FINALES ---" << endl;
        cout << "x1 = " << A[0][N] << endl;
        cout << "x2 = " << A[1][N] << endl;
        cout << "x3 = " << A[2][N] << endl;
        cout << "\n¿Deseas resolver otro sistema? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}