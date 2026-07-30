#include <iostream>
using namespace std;

class Nodo {
    int valor;
    Nodo* sig;
public:
    Nodo(int v) : valor(v), sig(nullptr) {}
    int obtenerDato() {
        return valor;
    }

    Nodo* obtenerSiguiente() {
        return sig;
    }

    void conectar(Nodo* nodo) {
        sig = nodo;
    }
};

class Colacir {
private:
    Nodo* inicio;
    Nodo* final;

public:
    Colacir() : inicio(nullptr), final(nullptr) {}

    void agregar(int v) {
        Nodo* nuevo = new Nodo(v);
        if (final == nullptr) {
            inicio = final = nuevo;
            final->conectar(inicio);  
        } else {
            final->conectar(nuevo);
            final = nuevo;
            final->conectar(inicio);  
        }
    }

    bool eliminar() {
        if (inicio != nullptr) {
            Nodo* temp = inicio;
            if (inicio == final) { 
                inicio = final = nullptr;
            } else {
                inicio = inicio->obtenerSiguiente();
                final->conectar(inicio); 
            }
            delete temp;
            return true;
        }
        return false;
    }

    void mostrarElementos() {
        if (inicio == nullptr) return;
        Nodo* temp = inicio;
        do {
            cout << temp->obtenerDato() << endl;
            temp = temp->obtenerSiguiente();
        } while (temp != inicio);
    }
    int ultimoElemento() {
        if (final != nullptr) {
            return final->obtenerDato();
        }
        return -1;
    }
     int Top() {
        if (inicio == NULL) {
            return -1; 
        }
        return inicio->obtenerDato();
    }
    int Size() {
        if (!inicio) return 0;
        int tam = 1;
        Nodo* temp = inicio;
        while (temp->obtenerSiguiente() != inicio) {
            tam++;
            temp = temp->obtenerSiguiente();
        }
        return tam;
    }
};
int josefo(int n, int k) {
    Colacir* cola = new Colacir();
    for (int i = 1; i <= n; ++i) cola->agregar(i);
    while (cola->Size() > 1) {
        for (int i = 0; i < k - 1; ++i) {
            cola->agregar(cola->Top());  
            cola->eliminar();
        }
        cola->eliminar();  
    }

    int sobr = cola->Top();
    delete cola; 
    return sobr;
}

int main() {
    int n, k;
    cout << "Ingrese n: ";
    cin >> n;
    cout << "Ingrese k: ";
    cin >> k;

    int sobr = josefo(n, k);
    cout << "El sobreviviente es: " <<sobr<< endl;

    return 0;
}