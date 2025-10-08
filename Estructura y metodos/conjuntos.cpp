/*Conjuntos: solo se acpta numeros enaturales, el usuario asigar la cantidad de elementos para cada conjunto
depues debe ingresar los elemtos del conjunto, en ves de comas utilizar el espacio*/
#include <iostream>
using namespace std;
int main() {
    int A[20], B[20];
    int tamA, tamB;
    cout << "Cantidad de elementos para el conjunto A: ";
    cin >> tamA;
    cout << "Elementos del conjunto A (separados por espacio): ";
    for (int i = 0; i < tamA; i++) {
        cin >> A[i];
    }
    cout << "Cantidad de elementos para el conjunto B: ";
    cin >> tamB;
    cout << "Elementos del conjunto B (separados por espacio): ";
    for (int i = 0; i < tamB; i++) {
        cin >> B[i];
    }
    int A_limpio[20], tam_A_limpio = 0;
    for (int i = 0; i < tamA; i++) {
        bool duplicado = false;
        for (int j = 0; j < tam_A_limpio; j++) {
            if (A[i] == A_limpio[j]) {
                duplicado = true;
                break;
            }
        }
        if (!duplicado) {
            A_limpio[tam_A_limpio] = A[i];
            tam_A_limpio++;
        }
    }
    for (int i = 0; i < tam_A_limpio - 1; i++) {//Orden Bubble Sort A
        for (int j = 0; j < tam_A_limpio - i - 1; j++) {
            if (A_limpio[j] > A_limpio[j + 1]) {
                int temp = A_limpio[j];
                A_limpio[j] = A_limpio[j + 1];
                A_limpio[j + 1] = temp;
            }
        }
    }
    int B_limpio[20], tam_B_limpio = 0;
    for (int i = 0; i < tamB; i++) {
        bool duplicado = false;
        for (int j = 0; j < tam_B_limpio; j++) {
            if (B[i] == B_limpio[j]) {
                duplicado = true;
                break;
            }
        }
        if (!duplicado) {
            B_limpio[tam_B_limpio] = B[i];
            tam_B_limpio++;
        }
    }
    for (int i = 0; i < tam_B_limpio - 1; i++) {//Orden Bubble Sort B
        for (int j = 0; j < tam_B_limpio - i - 1; j++) {
            if (B_limpio[j] > B_limpio[j + 1]) {
                int temp = B_limpio[j];
                B_limpio[j] = B_limpio[j + 1];
                B_limpio[j + 1] = temp;
            }
        }
    }
    cout << "\nConjuntos limpios y ordenados:\n";
    cout << "A = {";
    for (int i = 0; i < tam_A_limpio; i++) {
        cout << A_limpio[i];
        if (i < tam_A_limpio - 1) {
            cout << ", ";
        }
    }
    cout << "}\n";
    cout << "B = {";
    for (int i = 0; i < tam_B_limpio; i++) {
        cout << B_limpio[i];
        if (i < tam_B_limpio - 1) { 
            cout << ", ";
        }
    }
    cout << "}\n";
    cout << "Union (A U B): {";
    int union_conjunto[40]; 
    int tam_union = 0;
    bool primero_union = true;
    for (int i = 0; i < tam_A_limpio; i++) {
        union_conjunto[tam_union++] = A_limpio[i];
    }
    for (int i = 0; i < tam_B_limpio; i++) {
        bool existe_en_A = false;
        for (int j = 0; j < tam_A_limpio; j++) {
            if (B_limpio[i] == A_limpio[j]) {
                existe_en_A = true;
                break;
            }
        }
        if (!existe_en_A) {
            union_conjunto[tam_union++] = B_limpio[i];
        }
    }
    for (int i = 0; i < tam_union - 1; i++) {//Orden Bubble Sort
        for (int j = 0; j < tam_union - i - 1; j++) {
            if (union_conjunto[j] > union_conjunto[j + 1]) {
                int temp = union_conjunto[j];
                union_conjunto[j] = union_conjunto[j + 1];
                union_conjunto[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < tam_union; i++) {
        cout << union_conjunto[i];
        if (i < tam_union - 1) {
            cout << ", ";
        }
    }
    cout << "}\n";
    cout << "Interseccion (A n B): {";
    bool primer_elemento_interseccion = true;
    for (int i = 0; i < tam_A_limpio; i++) {
        for (int j = 0; j < tam_B_limpio; j++) {
            if (A_limpio[i] == B_limpio[j]) {
                if (!primer_elemento_interseccion) {
                    cout << ", ";
                }
                cout << A_limpio[i];
                primer_elemento_interseccion = false;
                break;
            }
        }
    }
    cout << "}\n";
    cout << "Diferencia (A - B): {";
    bool primer_elemento_diferencia_AB = true;
    for (int i = 0; i < tam_A_limpio; i++) {
        bool existe_en_B = false;
        for (int j = 0; j < tam_B_limpio; j++) {
            if (A_limpio[i] == B_limpio[j]) {
                existe_en_B = true;
                break;
            }
        }
        if (!existe_en_B) {
            if (!primer_elemento_diferencia_AB) {
                cout << ", ";
            }
            cout << A_limpio[i];
            primer_elemento_diferencia_AB = false;
        }
    }
    cout << "}\n";
    cout << "Diferencia (B - A): {";
    bool primer_elemento_diferencia_BA = true;
    for (int i = 0; i < tam_B_limpio; i++) {
        bool existe_en_A = false;
        for (int j = 0; j < tam_A_limpio; j++) {
            if (B_limpio[i] == A_limpio[j]) {
                existe_en_A = true;
                break;
            }
        }
        if (!existe_en_A) {
            if (!primer_elemento_diferencia_BA) {
                cout << ", ";
            }
            cout << B_limpio[i];
            primer_elemento_diferencia_BA = false;
        }
    }
    cout << "}\n";
    cout << "Diferencia Simetrica (A-B) U (B-A): {";
    int diferencia_simetrica[40]; 
    int tam_diferencia_simetrica = 0;
    for (int i = 0; i < tam_A_limpio; i++) {
        bool existe_en_B = false;
        for (int j = 0; j < tam_B_limpio; j++) {
            if (A_limpio[i] == B_limpio[j]) {
                existe_en_B = true;
                break;
            }
        }
        if (!existe_en_B) {
            diferencia_simetrica[tam_diferencia_simetrica++] = A_limpio[i];
        }
    }
    for (int i = 0; i < tam_B_limpio; i++) {
        bool existe_en_A = false;
        for (int j = 0; j < tam_A_limpio; j++) {
            if (B_limpio[i] == A_limpio[j]) {
                existe_en_A = true;
                break;
            }
        }
        if (!existe_en_A) {
            diferencia_simetrica[tam_diferencia_simetrica++] = B_limpio[i];
        }
    }
    for (int i = 0; i < tam_diferencia_simetrica - 1; i++) {
        for (int j = 0; j < tam_diferencia_simetrica - i - 1; j++) {
            if (diferencia_simetrica[j] > diferencia_simetrica[j + 1]) {
                int temp = diferencia_simetrica[j];
                diferencia_simetrica[j] = diferencia_simetrica[j + 1];
                diferencia_simetrica[j + 1] = temp;
            }
        }
    }
    for (int i = 0; i < tam_diferencia_simetrica; i++) {
        cout << diferencia_simetrica[i];
        if (i < tam_diferencia_simetrica - 1) {
            cout << ", ";
        }
    }
    cout << "}\n";

    return 0;
}
