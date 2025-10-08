// JUAM MAMANI PARI
// Calculo de la distancia entre dos puntos en el plano cartesiano
// Metodo de biseccion
// guias de implementacion: https://youtu.be/yeinln1Nt_U
// https://www.youtube.com/watch?v=9fGsN33nEng
#include <iostream>
using namespace std;
double raizCuadradaBiseccion(double n)
{
    if (n < 0)
    {
        return -1.0;
    }
    if (n == 0)
    {
        return 0.0;
    }
    double bajo = 0.0;
    double alto = n;
    double medio = (bajo + alto) / 2.0;
    double epsilon = 0.000001;
    if (n < 1.0)
    {
        alto = 1.0;
    }
    while ((alto - bajo) > epsilon)
    {
        medio = (bajo + alto) / 2.0;
        if ((medio * medio) > n)
        {
            alto = medio;
        }
        else
        {
            bajo = medio;
        }
    }
    return medio;
}
int main()
{
    char continuar;
    do
    {
        double x1, y1, x2, y2;
        double distancia;
        cout << "Ingrese las coordenadas del primer punto (x1, y1):" << endl;
        cout << "x1: ";
        cin >> x1;
        cout << "y1: ";
        cin >> y1;
        cout << "Ingrese las coordenadas del segundo punto (x2, y2):" << endl;
        cout << "x2: ";
        cin >> x2;
        cout << "y2: ";
        cin >> y2;
        double dx_cuadrado = (x2 - x1) * (x2 - x1);
        double dy_cuadrado = (y2 - y1) * (y2 - y1);
        distancia = raizCuadradaBiseccion(dx_cuadrado + dy_cuadrado);
        cout << "La distancia entre los puntos es: " << distancia << endl;
        cout << "¿Deseas calcular la distancia para otros puntos? (S/N): ";
        cin >> continuar;
    } while (continuar == 'S' || continuar == 's');
    cout << "Programa terminado." << endl;
    return 0;
}