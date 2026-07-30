#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
int main()
{
    double A[N][N + 1]; // Matriz aumentada para el sistema Ax = b
    double soluciones[N];
    char continuar;
    do
    {
        cout << "\n--- METODO DE GAUSS (SISTEMA 3x3) ---" << endl;
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
                cout << "Error: Pivote cero detectado. El sistema no se puede resolver." << endl;
                return 0;
            }

            for (int i = k + 1; i < N; i++)
            {
                double factor = A[i][k] / A[k][k];
                for (int j = k; j <= N; j++)
                {
                    A[i][j] -= factor * A[k][j];
                }
            }
        }
        soluciones[N - 1] = A[N - 1][N] / A[N - 1][N - 1];
        for (int i = N - 2; i >= 0; i--)
        {
            double suma = 0;
            for (int j = i + 1; j < N; j++)
            {
                suma += A[i][j] * soluciones[j];
            }
            soluciones[i] = (A[i][N] - suma) / A[i][i];
        }
        cout << "\n--- SOLUCION DEL SISTEMA ---" << endl;
        cout << "x1 = " << soluciones[0] << endl;
        cout << "x2 = " << soluciones[1] << endl;
        cout << "x3 = " << soluciones[2] << endl;
        cout << "\n¿Deseas resolver otro sistema? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    cout << "Programa terminado." << endl;
    return 0;
}