#include <iostream>
using namespace std;
const int N = 3; // Tamaño de la matriz 3x3
double valorAbsoluto(double n) { return (n < 0) ? -n : n; }
double raizCuadrada(double n) // Método de Newton-Raphson para cholesky
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
void mostrarMatriz(double m[N][N], const char *t)
{
    cout << "\n--- " << t << " ---" << endl;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
            cout << m[i][j] << "\t";
        cout << endl;
    }
}

void mostrarSistema(double m[N][N], double b[N], const char *t)
{
    cout << "\n--- " << t << " ---" << endl;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
            cout << m[i][j] << "\t";
        cout << "| " << b[i] << endl;
    }
}

void leerM(double m[N][N], const char *n)
{
    cout << "Ingrese matriz " << n << " (3x3):" << endl;
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            cin >> m[i][j];
}

void leerV(double v[N])
{
    cout << "Ingrese vector b (3 elementos):" << endl;
    for (int i = 0; i < N; i++)
        cin >> v[i];
}

double det3x3(double m[N][N])
{
    return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
           m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
           m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]);
}

// --- METODOS DE RESOLUCION ---

void mGauss(double A[N][N], double b[N])
{
    mostrarSistema(A, b, "MATRIZ INICIAL (A|b)");
    double m[N][N + 1];
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
            m[i][j] = A[i][j];
        m[i][N] = b[i];
    }
    for (int i = 0; i < N; i++)
    {
        for (int k = i + 1; k < N; k++)
        {
            double f = m[k][i] / m[i][i];
            for (int j = i; j <= N; j++)
                m[k][j] -= f * m[i][j];
        }
    }
    double x[N];
    for (int i = N - 1; i >= 0; i--)
    {
        x[i] = m[i][N];
        for (int j = i + 1; j < N; j++)
            x[i] -= m[i][j] * x[j];
        x[i] /= m[i][i];
    }
    cout << "\nRESULTADO (Gauss): x1=" << x[0] << ", x2=" << x[1] << ", x3=" << x[2] << endl;
}

void mGaussJordan(double A[N][N], double b[N])
{
    mostrarSistema(A, b, "MATRIZ INICIAL (A|b)");
    double m[N][N + 1];
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
            m[i][j] = A[i][j];
        m[i][N] = b[i];
    }
    for (int i = 0; i < N; i++)
    {
        double p = m[i][i];
        for (int j = i; j <= N; j++)
            m[i][j] /= p;
        for (int k = 0; k < N; k++)
        {
            if (k != i)
            {
                double f = m[k][i];
                for (int j = i; j <= N; j++)
                    m[k][j] -= f * m[i][j];
            }
        }
    }
    cout << "\nRESULTADO (Gauss-Jordan): x1=" << m[0][N] << ", x2=" << m[1][N] << ", x3=" << m[2][N] << endl;
}

void mLU(double A[N][N], double b[N])
{
    mostrarMatriz(A, "MATRIZ INICIAL");
    double L[N][N] = {0}, U[N][N] = {0};

    for (int i = 0; i < N; i++)
    {
        for (int k = i; k < N; k++)
        {
            double s = 0;
            for (int j = 0; j < i; j++)
                s += L[i][j] * U[j][k];
            U[i][k] = A[i][k] - s;
        }
        for (int k = i; k < N; k++)
        {
            if (i == k)
                L[i][i] = 1;
            else
            {
                double s = 0;
                for (int j = 0; j < i; j++)
                    s += L[k][j] * U[j][i];
                L[k][i] = (A[k][i] - s) / U[i][i];
            }
        }
    }
    mostrarMatriz(L, "RESULTADO L");
    mostrarMatriz(U, "RESULTADO U");

    double y[N];
    for (int i = 0; i < N; i++)
    {
        double s = 0;
        for (int j = 0; j < i; j++)
            s += L[i][j] * y[j];
        y[i] = b[i] - s;
    }

    cout << "\n--- RESULTADOS INTERMEDIOS (De Matriz L: Ly = b) ---" << endl;
    cout << "y1 = " << y[0] << endl;
    cout << "y2 = " << y[1] << endl;
    cout << "y3 = " << y[2] << endl;

    double x[N];
    for (int i = N - 1; i >= 0; i--)
    {
        double s = 0;
        for (int j = i + 1; j < N; j++)
            s += U[i][j] * x[j];
        x[i] = (y[i] - s) / U[i][i];
    }

    cout << "\n--- RESULTADOS FINALES (De Matriz U: Ux = y) ---" << endl;
    cout << "x1 (a) = " << x[0] << endl;
    cout << "x2 (b) = " << x[1] << endl;
    cout << "x3 (c) = " << x[2] << endl;
}

void mInversa(double A[N][N])
{
    mostrarMatriz(A, "MATRIZ INICIAL");
    double det = det3x3(A);
    if (valorAbsoluto(det) < 0.000001)
    {
        cout << "No tiene inversa." << endl;
        return;
    }
    double inv[N][N], adj[N][N];
    adj[0][0] = (A[1][1] * A[2][2] - A[1][2] * A[2][1]);
    adj[0][1] = -(A[0][1] * A[2][2] - A[0][2] * A[2][1]);
    adj[0][2] = (A[0][1] * A[1][2] - A[0][2] * A[1][1]);
    adj[1][0] = -(A[1][0] * A[2][2] - A[1][2] * A[2][0]);
    adj[1][1] = (A[0][0] * A[2][2] - A[0][2] * A[2][0]);
    adj[1][2] = -(A[0][0] * A[1][2] - A[0][2] * A[1][0]);
    adj[2][0] = (A[1][0] * A[2][1] - A[1][1] * A[2][0]);
    adj[2][1] = -(A[0][0] * A[2][1] - A[0][1] * A[2][0]);
    adj[2][2] = (A[0][0] * A[1][1] - A[0][1] * A[1][0]);
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            inv[i][j] = adj[j][i] / det; // Transpuesta de adjunta
    mostrarMatriz(inv, "MATRIZ INVERSA");
}

void mOperaciones(double A[N][N], double B[N][N])
{
    mostrarMatriz(A, "MATRIZ A");
    mostrarMatriz(B, "MATRIZ B");
    double S[N][N], R[N][N], M[N][N] = {0};
    bool ig = true;
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j < N; j++)
        {
            S[i][j] = A[i][j] + B[i][j];
            R[i][j] = A[i][j] - B[i][j];
            if (valorAbsoluto(A[i][j] - B[i][j]) > 0.001)
                ig = false;
            for (int k = 0; k < N; k++)
                M[i][j] += A[i][k] * B[k][j];
        }
    }
    mostrarMatriz(S, "SUMA");
    mostrarMatriz(R, "RESTA");
    mostrarMatriz(M, "MULTIPLICACION");
    cout << "\nComparacion: " << (ig ? "Iguales" : "Diferentes") << endl;
}

void mTranspuesta(double A[N][N])
{
    mostrarMatriz(A, "MATRIZ INICIAL");
    double T[N][N];
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            T[i][j] = A[j][i];
    mostrarMatriz(T, "RESULTADO TRANSPUESTA");
}

void mDeterminante(double A[N][N])
{
    mostrarMatriz(A, "MATRIZ INICIAL");
    cout << "\nRESULTADO DETERMINANTE: " << det3x3(A) << endl;
}

void mCramer(double A[N][N], double b[N])
{
    mostrarSistema(A, b, "MATRIZ INICIAL (A|b)");
    double d = det3x3(A);
    if (valorAbsoluto(d) < 0.000001)
    {
        cout << "Sist. no determinado." << endl;
        return;
    }
    double mX[N][N], mY[N][N], mZ[N][N];
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
        {
            mX[i][j] = (j == 0) ? b[i] : A[i][j];
            mY[i][j] = (j == 1) ? b[i] : A[i][j];
            mZ[i][j] = (j == 2) ? b[i] : A[i][j];
        }
    cout << "\nRESULTADO (Cramer): x1=" << det3x3(mX) / d << ", x2=" << det3x3(mY) / d << ", x3=" << det3x3(mZ) / d << endl;
}

void mCholesky(double A[N][N], double b[N])
{
    mostrarMatriz(A, "MATRIZ INICIAL");
    double L[N][N] = {0};
    for (int i = 0; i < N; i++)
    {
        for (int j = 0; j <= i; j++)
        {
            double s = 0;
            for (int k = 0; k < j; k++)
                s += L[i][k] * L[j][k];
            if (i == j)
                L[i][j] = raizCuadrada(A[i][i] - s);
            else
                L[i][j] = (A[i][j] - s) / L[j][j];
        }
    }
    mostrarMatriz(L, "RESULTADO CHOLESKY (L)");

    // Resolver Ly = b
    double y[N], x[N];
    for (int i = 0; i < N; i++)
    {
        double s = 0;
        for (int j = 0; j < i; j++)
            s += L[i][j] * y[j];
        y[i] = (b[i] - s) / L[i][i];
    }
    // Resolver L^T x = y
    for (int i = N - 1; i >= 0; i--)
    {
        double s = 0;
        for (int j = i + 1; j < N; j++)
            s += L[j][i] * x[j];
        x[i] = (y[i] - s) / L[i][i];
    }
    cout << "\nRESULTADO (Cholesky): x1=" << x[0] << ", x2=" << x[1] << ", x3=" << x[2] << endl;
}

int main()
{
    int op;
    char r;
    double A[N][N], B[N][N], b[N];
    do
    {
        cout << "\n==== MATRIZ ALGEBRAICA (9 METODOS) ====\n";
        cout << "1. Gauss\n2. Gauss-Jordan\n3. LU\n4. Inversa\n5. Operaciones\n6. Transpuesta\n7. Determinante\n8. Cramer\n9. Cholesky\n10. Salir\nOpcion: ";
        cin >> op;

        if (op >= 1 && op <= 10 && op != 5 && op != 10)
            leerM(A, "A");
        // Ahora pedimos b para todos los metodos de resolucion
        if (op == 1 || op == 2 || op == 3 || op == 8 || op == 9)
            leerV(b);
        if (op == 5)
        {
            leerM(A, "A");
            leerM(B, "B");
        }

        switch (op)
        {
        case 1:
            mGauss(A, b);
            break;
        case 2:
            mGaussJordan(A, b);
            break;
        case 3:
            mLU(A, b);
            break;
        case 4:
            mInversa(A);
            break;
        case 5:
            mOperaciones(A, B);
            break;
        case 6:
            mTranspuesta(A);
            break;
        case 7:
            mDeterminante(A);
            break;
        case 8:
            mCramer(A, b);
            break;
        case 9:
            mCholesky(A, b);
            break;
        }
        if (op == 10)
            break;
        cout << "\nOTRO EJERCICIO? (s/n): ";
        cin >> r;
    } while (r == 's' || r == 'S');
    return 0;
}