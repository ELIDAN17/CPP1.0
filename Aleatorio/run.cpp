#include <iostream>
using namespace std;


/*
class Matriz {
private:
    int** datos;
    int nFilas;
    int nColumnas;

public:
    // Constructor
    Matriz(int nF, int nC) : nFilas(nF), nColumnas(nC) {
        datos = new int*[nFilas];
        for (int i = 0; i < nFilas; ++i) {
            datos[i] = new int[nColumnas];
        }
    }

    // Destructor
    ~Matriz() {
        for (int i = 0; i < nFilas; ++i) {
            delete[] datos[i];
        }
        delete[] datos;
    }

    // Sobrecarga del operador +
    friend Matriz operator+(const Matriz& m1, const Matriz& m2);

    // Método para asignar valores a la matriz
    void asignarValores() {
        //cout << "Ingrese los valores de la matriz:" << endl;
        for (int i = 0; i < nFilas; ++i) {
            for (int j = 0; j < nColumnas; ++j) {
                datos[i][j]=1+rand()%(49);
                cout << datos[i][j]<<" ";
            }
        }
        cout << endl;
    }

    // Método para mostrar la matriz
    void mostrar() const { cout<<endl;
        for (int i = 0; i < nFilas; ++i) {
            for (int j = 0; j < nColumnas; ++j) {
                cout << datos[i][j] << " ";
            }
            cout << endl;
        }
    }
};
Matriz operator+(const Matriz& m1, const Matriz& m2) {
    if (m1.nFilas!= m2.nFilas || m1.nColumnas!= m2.nColumnas) {
        cerr << "Las matrices tienen dimensiones diferentes, no pueden sumarse." << endl;
        exit(1); // Termina el programa con error
    }

    Matriz resultado(m1.nFilas, m1.nColumnas);
    for (int i = 0; i < m1.nFilas; ++i) {
        for (int j = 0; j < m1.nColumnas; ++j) {
            resultado.datos[i][j] = m1.datos[i][j] + m2.datos[i][j];
        }
    }

    return resultado;
}
int main() {
    int nFilas = 3, nColumnas = 3;

    Matriz m1(nFilas, nColumnas);
    m1.asignarValores();

    Matriz m2(nFilas, nColumnas);
    m2.asignarValores();

    Matriz suma = m1 + m2;
    suma.mostrar();

    return 0;
}
*/