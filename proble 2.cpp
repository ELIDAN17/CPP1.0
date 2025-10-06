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
    void eliminar() {
        if (inicio != nullptr) {
            Nodo* temp = inicio;
            if (inicio == final) {
                inicio = final = nullptr;
            } else {
                inicio = inicio->obtenerSiguiente();
                final->conectar(inicio);
            }
            delete temp;
        }
    }
    int Top() {
        if (inicio == nullptr) {
            return -1;
        }
        return inicio->obtenerDato();
    }
    void ordenar() {
        if (inicio == nullptr || inicio->obtenerSiguiente() == inicio) return;
        int tiempos[100000];
        int n = 0;
        Nodo* temp = inicio;
        do {
            tiempos[n++] = temp->obtenerDato();
            temp = temp->obtenerSiguiente();
        } while (temp != inicio);

        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (tiempos[j] > tiempos[j + 1]) {
                    swap(tiempos[j], tiempos[j + 1]);
                }
            }
        }

        inicio = final = nullptr;

        for (int i = 0; i < n; i++) {
            agregar(tiempos[i]);
        }
    }
};
int main() {
    int n;
    cin >> n;
    Colacir cola;

    for (int i = 0; i < n; ++i) {
        int tiempo;
        cin >> tiempo;
        cola.agregar(tiempo);
    }
    cola.ordenar();
    int tiempoEspera = 0;
    int noDecepcionados = 0;

    for (int i = 0; i < n; ++i) {
        if (tiempoEspera <= cola.Top()) {
            noDecepcionados++;
            tiempoEspera += cola.Top();
        }
        cola.eliminar();
    }
    cout << noDecepcionados << endl;
    return 0;
}