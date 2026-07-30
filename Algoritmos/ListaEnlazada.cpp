#include <iostream>
using namespace std;
struct Nodo
{
    int dato;
    Nodo *siguiente;
    Nodo(int valor)
    {
        dato = valor;
        siguiente = nullptr;
    }
};
class ListaEnlazada
{
private:
    Nodo *cabeza;

public:
    ListaEnlazada()
    {
        cabeza = nullptr;
    }
    void insertarInicio(int valor)
    {
        Nodo *nuevo = new Nodo(valor);
        nuevo->siguiente = cabeza;
        cabeza = nuevo;
        cout << "Insertado al inicio: " << valor << endl;
    }
    void insertarFinal(int valor)
    {
        Nodo *nuevo = new Nodo(valor);
        if (cabeza == nullptr)
        {
            cabeza = nuevo;
        }
        else
        {
            Nodo *temp = cabeza;
            while (temp->siguiente != nullptr)
            {
                temp = temp->siguiente;
            }
            temp->siguiente = nuevo;
        }
        cout << "Insertado al final: " << valor << endl;
    }
    void eliminarInicio()
    {
        if (cabeza == nullptr)
        {
            cout << "Error: Lista vacia" << endl;
            return;
        }
        Nodo *temp = cabeza;
        cabeza = cabeza->siguiente;
        cout << "Eliminado del inicio: " << temp->dato << endl;
        delete temp;
    }
    void mostrar()
    {
        if (cabeza == nullptr)
        {
            cout << "Lista vacia" << endl;
            return;
        }
        cout << "Lista final:" << endl;
        Nodo *temp = cabeza;
        while (temp != nullptr)
        {
            cout << temp->dato << endl;
            temp = temp->siguiente;
        }
    }
    ~ListaEnlazada()
    {
        while (cabeza != nullptr)
        {
            Nodo *temp = cabeza;
            cabeza = cabeza->siguiente;
            delete temp;
        }
    }
};
int main()
{
    ListaEnlazada lista;
    cout << "=== Insertando al inicio ===" << endl;
    lista.insertarInicio(8);
    lista.insertarInicio(4);
    cout << "\n=== Insertando al final ===" << endl;
    lista.insertarFinal(11);
    cout << "\n=== Eliminando primer nodo ===" << endl;
    lista.eliminarInicio();
    cout << "\n=== Estado final ===" << endl;
    lista.mostrar();
    return 0;
}
