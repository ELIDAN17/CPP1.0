#include <iostream>

using namespace std;

int main()
{
    int mejorX1 = 0;
    int mejorX2 = 0;
    double maxZ = 0;

    cout << "Calculando optimizacion para Funco..." << endl;
    cout << "---------------------------------------" << endl;

    // Recorremos posibles valores de x1 y x2 (limitados por la madera disponible)
    for (int x1 = 0; x1 <= 5; x1++)
    { // x1 maximo es 5 (20/4)
        for (int x2 = 0; x2 <= 7; x2++)
        { // x2 maximo es 6.67 (20/3)

            // Verificamos las restricciones
            bool maderaOk = (4 * x1 + 3 * x2 <= 20);
            bool mercadoOk = (x2 >= 2 * x1);

            if (maderaOk && mercadoOk)
            {
                double utilidadActual = 40 * x1 + 25 * x2;

                // Si encontramos una mejor utilidad, la guardamos
                if (utilidadActual > maxZ)
                {
                    maxZ = utilidadActual;
                    mejorX1 = x1;
                    mejorX2 = x2;
                }
            }
        }
    }

    cout << "RESULTADOS OPTIMOS:" << endl;
    cout << "Escritorios a fabricar: " << mejorX1 << endl;
    cout << "Sillas a fabricar: " << mejorX2 << endl;
    cout << "Utilidad Maxima: $" << maxZ << endl;

    return 0;
}