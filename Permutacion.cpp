#include <iostream>
using namespace std;

int main() {
    int n, r, opcion;
    long long factorial_n = 1, factorial_r = 1, factorial_nr = 1;
    long long permutacion, combinacion;
    char continuar = 's';
    
    cout << "===============================================" << endl;
    cout << "    CALCULADORA DE PERMUTACIONES Y COMBINACIONES" << endl;
    cout << "===============================================" << endl;
    cout << endl;
    
    // Mostrar las fórmulas
    cout << "FORMULAS:" << endl;
    cout << "---------" << endl;
    cout << "PERMUTACIONES (el orden SI importa):" << endl;
    cout << "P(n,r) = n! / (n-r)!" << endl;
    cout << "Ejemplo: P(5,3) = 5! / (5-3)! = 120 / 2 = 60" << endl;
    cout << endl;
    cout << "COMBINACIONES (el orden NO importa):" << endl;
    cout << "C(n,r) = n! / (r! * (n-r)!)" << endl;
    cout << "Ejemplo: C(5,3) = 5! / (3! * 2!) = 120 / (6 * 2) = 10" << endl;
    cout << endl;
    cout << "Donde:" << endl;
    cout << "n = número total de elementos" << endl;
    cout << "r = número de elementos a seleccionar/ordenar" << endl;
    cout << "! = factorial (n! = n * (n-1) * (n-2) * ... * 1)" << endl;
    cout << endl;
    
    while(continuar == 's' || continuar == 'S') {
        cout << "===============================================" << endl;
        cout << "Selecciona una opción:" << endl;
        cout << "1. Calcular Permutaciones P(n,r)" << endl;
        cout << "2. Calcular Combinaciones C(n,r)" << endl;
        cout << "3. Calcular ambas" << endl;
        cout << "Opción: ";
        cin >> opcion;
        cout << endl;
        
        if(opcion < 1 || opcion > 3) {
            cout << "Opción inválida. Intenta de nuevo." << endl;
            continue;
        }
        
        cout << "Ingresa el valor de n (total de elementos): ";
        cin >> n;
        cout << "Ingresa el valor de r (elementos a seleccionar): ";
        cin >> r;
        cout << endl;
        
        // Validaciones
        if(n < 0 || r < 0) {
            cout << "Error: Los valores deben ser positivos." << endl;
            continue;
        }
        
        if(r > n) {
            cout << "Error: r no puede ser mayor que n." << endl;
            continue;
        }
        
        // Reiniciar factoriales
        factorial_n = 1;
        factorial_r = 1;
        factorial_nr = 1;
        
        // Calcular factorial de n
        cout << "Calculando " << n << "! = ";
        for(int i = 1; i <= n; i++) {
            factorial_n *= i;
            cout << i;
            if(i < n) cout << " × ";
        }
        cout << " = " << factorial_n << endl;
        
        // Calcular factorial de r
        if(r > 0) {
            cout << "Calculando " << r << "! = ";
            for(int i = 1; i <= r; i++) {
                factorial_r *= i;
                cout << i;
                if(i < r) cout << " × ";
            }
            cout << " = " << factorial_r << endl;
        } else {
            cout << "0! = 1" << endl;
        }
        
        // Calcular factorial de (n-r)
        int nr = n - r;
        if(nr > 0) {
            cout << "Calculando (" << n << "-" << r << ")! = " << nr << "! = ";
            for(int i = 1; i <= nr; i++) {
                factorial_nr *= i;
                cout << i;
                if(i < nr) cout << " × ";
            }
            cout << " = " << factorial_nr << endl;
        } else {
            cout << "(" << n << "-" << r << ")! = 0! = 1" << endl;
        }
        
        cout << endl;
        
        // Calcular según la opción seleccionada
        if(opcion == 1 || opcion == 3) {
            permutacion = factorial_n / factorial_nr;
            cout << "PERMUTACIONES:" << endl;
            cout << "P(" << n << "," << r << ") = " << n << "! / (" << n << "-" << r << ")!" << endl;
            cout << "P(" << n << "," << r << ") = " << factorial_n << " / " << factorial_nr << endl;
            cout << "P(" << n << "," << r << ") = " << permutacion << endl;
            cout << endl;
            cout << "Interpretación: Hay " << permutacion << " maneras diferentes de" << endl;
            cout << "ordenar " << r << " elementos de un total de " << n << " elementos." << endl;
            cout << endl;
        }
        
        if(opcion == 2 || opcion == 3) {
            combinacion = factorial_n / (factorial_r * factorial_nr);
            cout << "COMBINACIONES:" << endl;
            cout << "C(" << n << "," << r << ") = " << n << "! / (" << r << "! × (" << n << "-" << r << ")!)" << endl;
            cout << "C(" << n << "," << r << ") = " << factorial_n << " / (" << factorial_r << " × " << factorial_nr << ")" << endl;
            cout << "C(" << n << "," << r << ") = " << factorial_n << " / " << (factorial_r * factorial_nr) << endl;
            cout << "C(" << n << "," << r << ") = " << combinacion << endl;
            cout << endl;
            cout << "Interpretación: Hay " << combinacion << " maneras diferentes de" << endl;
            cout << "seleccionar " << r << " elementos de un total de " << n << " elementos" << endl;
            cout << "(sin importar el orden)." << endl;
            cout << endl;
        }
        
        if(opcion == 3) {
            cout << "COMPARACIÓN:" << endl;
            cout << "P(" << n << "," << r << ") = " << permutacion << " (con orden)" << endl;
            cout << "C(" << n << "," << r << ") = " << combinacion << " (sin orden)" << endl;
            cout << "Relación: P(" << n << "," << r << ") = C(" << n << "," << r << ") × " << r << "!" << endl;
            cout << "Verificación: " << combinacion << " × " << factorial_r << " = " << (combinacion * factorial_r) << endl;
            cout << endl;
        }
        
        cout << "¿Deseas realizar otro cálculo? (s/n): ";
        cin >> continuar;
        cout << endl;
    }
    
    cout << "===============================================" << endl;
    cout << "           ¡Gracias por usar el programa!" << endl;
    cout << "===============================================" << endl;
    
    return 0;
}