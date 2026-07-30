#include <iostream>
using namespace std;
int main()
{
    double decimal;
    double sumatoria = 0.0;
    int i, veces; // veces = 30000;
    cout << "Ingresa un número con decimal (x): ";
    cin >> decimal;
    cout << "Ingrese el valor para (i): ";
    cin >> i;
    cout << "ingrese el valor de (n): ";
    cin >> veces;
    if (decimal < 0)
    {
        cout << "Número no válido, ingresa un número positivo." << endl;
        return 1;
    }
    for (i; i < veces; ++i)
    {
        sumatoria += decimal;
    }
    cout << "El número " << decimal << " sumado" << veces << "veces es: " << sumatoria << endl;
    return 0;
}
