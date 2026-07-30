#include <iostream>
using namespace std;
void minimosCuadrados()
{
    int n;
    cout << "\n--- METODO DE MINIMOS CUADRADOS (REGRESION LINEAL) ---" << endl;
    cout << "¿Cuantos puntos desea ingresar?: ";
    cin >> n;
    double x[100], y[100];
    double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
    for (int i = 0; i < n; i++)
    {
        cout << "Punto " << i + 1 << " (Ingresa x [espacio] y): ";
        cin >> x[i] >> y[i];
        sumX += x[i];
        sumY += y[i];
        sumXY += x[i] * y[i];
        sumX2 += x[i] * x[i];
    }
    double a1 = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    double a0 = (sumY / n) - a1 * (sumX / n);
    cout << "\n--- RESULTADOS ---" << endl;
    cout << "Suma de X  : " << sumX << endl;
    cout << "Suma de Y  : " << sumY << endl;
    cout << "Suma de X*Y: " << sumXY << endl;
    cout << "Suma de X^2: " << sumX2 << endl;
    cout << "----------------------------" << endl;
    cout << "Coeficiente a0 (Interseccion): " << a0 << endl;
    cout << "Coeficiente a1 (Pendiente)   : " << a1 << endl;
    cout << "Ecuacion de la recta: y = " << a0 << " + " << a1 << "x" << endl;
}
int main()
{
    char continuar;
    do
    {
        minimosCuadrados();
        cout << "\n¿Deseas realizar otro ajuste? (s/n): ";
        cin >> continuar;
    } while (continuar == 's' || continuar == 'S');
    cout << "Programa terminado." << endl;
    return 0;
}