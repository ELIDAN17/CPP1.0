#include <iostream>
using namespace std;

char* convertBase(int num, int base) {
    static char result[100]; // Almacenar el resultado máximo de 99 dígitos
    int index = 0;
    
    if (num == 0) {
        result[index++] = '0';
    } else {
        convertBase(num / base, base);
        switch(base) {
            case 2:
                result[index] = (num % 2 ? '1' : '0');
                break;
            case 8:
                result[index] = (num % 8 + '0');
                break;
            case 10:
                result[index] = (num % 10 + '0');
                break;
            case 16:
                result[index] = (num % 16 > 9 ? "ABCDEF"[num % 16 - 10] : num % 16 + '0');
                break;
            default:
                result[index] = "0123456789ABCDEF"[num % base];
        }
        index++;
    }
    
    return &result[index - 1];
}

int main() {
    int num, base;
    cout << "Ingrese un número entero: ";
    cin >> num;
    cout << "Ingrese la base de destino (2-16): ";
    cin >> base;
    
    if (base >= 2 && base <= 16) {
        char* result = convertBase(num, base);
        cout << "El número " << num << " en base " << base << " es: " << result << endl;
    } else {
        cout << "Base inválida. Por favor, ingrese una base entre 2 y 16." << endl;
    }
    
    return 0;
}




/*
// Función principal
int main() {
    int num, baseOriginal, baseNueva;
    
    cout << "Ingrese un número entero positivo: ";
    cin >> num;
    
    cout << "Ingrese la base original del número (2-16): ";
    cin >> baseOriginal;
    
    cout << "Ingrese la nueva base de destino (2-16): ";
    cin >> baseNueva;
    
    // Verificar si las bases son válidas
    if (baseOriginal >= 2 && baseOriginal <= 16 && baseNueva >= 2 && baseNueva <= 16) {
        // Convertir al sistema decimal
        int decimal = convertirBaseADecimal(num, baseOriginal);
        
        // Convertir de decimal a la nueva base
        string resultado = convertirDecimalABase(decimal, baseNueva);
        
        cout << "El número " << num << " en base " << baseOriginal << " es igual a " << resultado << " en base " << baseNueva << endl;
    } else {
        cout << "Base inválida. Por favor, ingrese bases entre 2 y 16." << endl;
    }
    
    return 0;
}

// Función recursiva para convertir de cualquier base a decimal
int convertirBaseADecimal(int num, int base) {
    if (num == 0)
        return 0;
    else if (num < base)
        return num;
    else
        return convertirBaseADecimal(num / base, base) * base + (num % base);
}

// Función recursiva para convertir de decimal a cualquier base
string convertirDecimalABase(int decimal, int base) {
    if (decimal == 0)
        return "0";
    else if (decimal < base)
        return char('0' + decimal);
    else
        return convertirDecimalABase(decimal / base, base) + char('0' + decimal % base);
}
*/