#include <iostream>
using namespace std;
void interpolacionNewton()
{
    int n;
    cout << "\n--- INTERPOLACION DE NEWTON ---" << endl;
    cout << "¿Cuantos puntos desea ingresar?: ";
    cin >> n;
    double x[10], y[10], f[10][10];
    for (int i = 0; i < n; i++)
    {
        cout << "Punto " << i + 1 << " (Ingresa x [espacio] y): ";
        cin >> x[i] >> y[i];
        f[i][0] = y[i];
    }
    for (int j = 1; j < n; j++)
    {
        for (int i = 0; i < n - j; i++)
        {
            f[i][j] = (f[i + 1][j - 1] - f[i][j - 1]) / (x[i + j] - x[i]);
        }
    }
    cout << "\nCoeficientes b (Diferencias Divididas):" << endl;
    for (int j = 0; j < n; j++)
    {
        cout << "b" << j << " = " << f[0][j] << endl;
    }
    double xi;
    cout << "\nIngrese el valor de x a interpolar: ";
    cin >> xi;
    double resultado = f[0][0];
    double factor = 1.0;
    for (int j = 1; j < n; j++)
    {
        factor *= (xi - x[j - 1]);
        resultado += f[0][j] * factor;
    }
    cout << "El valor aproximado f(" << xi << ") es: " << resultado << endl;
}
int main()
{
    char continuar;
    do
    {
        interpolacionNewton();
        cout << "\n¿Deseas interpolar otros puntos? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    return 0;
}