#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
int main()
{
    double A[N][N + 1]; // Matriz aumentada para el sistema Ax = b
    double L[N][N] = {0}, U[N][N] = {0};
    double y[N], x[N];
    char continuar;
    do
    {
        cout << "\n--- METODO LU (SISTEMA 3x3) ---" << endl;
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
        for (int i = 0; i < N; i++)
        {
            // Matriz U
            for (int k = i; k < N; k++)
            {
                double suma = 0;
                for (int j = 0; j < i; j++)
                    suma += (L[i][j] * U[j][k]);
                U[i][k] = A[i][k] - suma;
            }
            // Matriz L
            for (int k = i; k < N; k++)
            {
                if (i == k)
                    L[i][i] = 1;
                else
                {
                    double suma = 0;
                    for (int j = 0; j < i; j++)
                        suma += (L[k][j] * U[j][i]);
                    L[k][i] = (A[k][i] - suma) / U[i][i];
                }
            }
        }
        cout << "\n--- MATRIZ L ---" << endl;
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
                cout << L[i][j] << "\t";
            cout << endl;
        }
        for (int i = 0; i < N; i++)
        {
            double suma = 0;
            for (int j = 0; j < i; j++)
                suma += L[i][j] * y[j];
            y[i] = A[i][N] - suma;
        }
        cout << "\nValores hallados con L (Sustitucion hacia adelante):" << endl;
        cout << "y1 = " << y[0] << endl;
        cout << "y2 = " << y[1] << endl;
        cout << "y3 = " << y[2] << endl;
        cout << "\n--- MATRIZ U ---" << endl;
        for (int i = 0; i < N; i++)
        {
            for (int j = 0; j < N; j++)
                cout << U[i][j] << "\t";
            cout << endl;
        }
        for (int i = N - 1; i >= 0; i--)
        {
            double suma = 0;
            for (int j = i + 1; j < N; j++)
                suma += U[i][j] * x[j];
            x[i] = (y[i] - suma) / U[i][i];
        }
        cout << "\nValores hallados con U (Sustitucion hacia atras):" << endl;
        cout << "x1 = " << x[0] << endl;
        cout << "x2 = " << x[1] << endl;
        cout << "x3 = " << x[2] << endl;
        cout << "\n¿Desea resolver otro sistema? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}