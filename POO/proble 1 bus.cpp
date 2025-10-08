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

    void agregarFrente(int v) {
        Nodo* nuevo = new Nodo(v);
        if (final == nullptr) {
            inicio = final = nuevo;
            final->conectar(inicio);
        } else {
            nuevo->conectar(inicio);
            final->conectar(nuevo);
            inicio = nuevo;
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

    bool eliminarFinal() {
        if (final != nullptr) {
            if (inicio == final) {
                delete inicio;
                inicio = final = nullptr;
            } else {
                Nodo* temp = inicio;
                while (temp->obtenerSiguiente() != final) {
                    temp = temp->obtenerSiguiente();
                }
                delete final;
                final = temp;
                final->conectar(inicio);
            }
            return true;
        }
        return false;
    }

    int Top() {
        if (inicio == nullptr) {
            return -1; 
        }
        return inicio->obtenerDato();
    }

    int Size() {
        if (inicio == nullptr) return 0;
        int tam = 1;
        Nodo* temp = inicio;
        while (temp->obtenerSiguiente() != inicio) {
            tam++;
            temp = temp->obtenerSiguiente();
        }
        return tam;
    }

    int obtenerIDEnPos(int pos) {
        Nodo* actual = inicio;
        for (int i = 1; i < pos; ++i) {
            actual = actual->obtenerSiguiente();
        }
        return actual->obtenerDato();
    }

    int obtenerPosEnCola(int id) {
        Nodo* actual = inicio;
        int pos = 1;
        do {
            if (actual->obtenerDato() == id) {
                return pos;
            }
            actual = actual->obtenerSiguiente();
            pos++;
        } while (actual != inicio);
        return -1; // No debería llegar aquí
    }
};

void procesarCasos() {
    int T; 
    cin >> T;
    for (int caso = 1; caso <= T; ++caso) {
        int N;
        cin >> N;
        Colacir cola;
        cout << "Caso " << caso << ":\n";
        
        for (int i = 0; i < N; ++i) {
            int tipo;
            char x; // operacion
            int y; // ID 
            cin >> tipo;
            if (tipo == 1) {
                cin >> x >> y;
                if (x == 'B') {
                    cola.agregar(y); 
                } else {
                    cola.agregarFrente(y); 
                }
            } else if (tipo == 2) {
                cin >> x;
                if (x == 'B') {
                    cola.eliminarFinal(); 
                } else {
                    cola.eliminar(); 
                }
            } else if (tipo == 3) {
                cin >> x >> y;
                if (x == 'D') {
                    cout << cola.obtenerIDEnPos(y) << endl; 
                } else {
                    cout << cola.obtenerPosEnCola(y) << endl; 
                }
            }
        }
    }
}

int main() {
    procesarCasos(); 
    return 0;
}
