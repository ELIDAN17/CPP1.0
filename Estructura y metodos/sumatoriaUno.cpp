

#include <iostream>
using namespace std;
int main()
{
    int n, i, sum = 0;
    cout << "Ingresa un número natural para la sumatoria (n): ";
    cin >> n;
    cout << "Ingrese el valor para (i): ";
    cin >> n;
    if (n < 0 && i < 0)
    {
        cout << "Número no válido, ingresa solo números naturales." << endl;
        return 1;
    }
    cout << "La sumatoria es: ";

    for (i; i < n; ++i)
    {
        cout << "1";
        if (i < n - 1)
        {
            cout << " + ";
        }
        sum += 1;
    }
    cout << endl;
    cout << "El resultado de la sumatoria es: " << sum << endl;
    return 0;
}
