#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
double raizCuadrada(double n)
{
    if (n <= 0)
        return 0;
    double x = n, y = 1;
    for (int i = 0; i < 20; i++)
    {
        x = (x + y) / 2;
        y = n / x;
    }
    return x;
}
void metodoCholesky()
{
    double A[N][N + 1];
    double L[N][N] = {0};
    double y[N], x[N];
    cout << "Nota: La matriz debe ser simetrica y positiva." << endl;
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
    { // Factorizacion de Cholesky (A = L * L^T)
        for (int j = 0; j <= i; j++)
        {
            double suma = 0;
            for (int k = 0; k < j; k++)
            {
                suma += L[i][k] * L[j][k];
            }
            if (i == j)
            {
                double val = A[i][i] - suma;
                if (val < 0)
                {
                    cout << "Error: La matriz no es definida positiva." << endl;
                    return;
                }
                L[i][j] = raizCuadrada(val);
            }
            else
            {
                L[i][j] = (A[i][j] - suma) / L[j][j];
            }
        }
    }
    cout << "\n--- MATRIZ L (Triangular Inferior) ---" << endl;
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
        y[i] = (A[i][N] - suma) / L[i][i];
    }
    for (int i = N - 1; i >= 0; i--)
    {
        double suma = 0;
        for (int j = i + 1; j < N; j++)
            suma += L[j][i] * x[j];
        x[i] = (y[i] - suma) / L[i][i];
    }
    cout << "\n--- SOLUCION FINAL POR CHOLESKY ---" << endl;
    cout << "x1 = " << x[0] << endl;
    cout << "x2 = " << x[1] << endl;
    cout << "x3 = " << x[2] << endl;
}
int main()
{
    char continuar;
    do
    {
        cout << "\n=== METODO DE CHOLESKY (SISTEMA 3x3) ===" << endl;
        metodoCholesky();
        cout << "\n¿Deseas resolver otro sistema? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}