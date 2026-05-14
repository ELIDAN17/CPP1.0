#include <iostream>
#define MAX 100
using namespace std;
class Pila
{
private:
    int arr[MAX], tope;

public:
    Pila() { tope = -1; }
    void push(int valor)
    {
        if (tope >= MAX - 1)
        {
            cout << "Error: Pila llena" << endl;
            return;
        }
        arr[++tope] = valor;
        cout << "Insertado: " << valor << endl;
    }
    void pop()
    {
        if (tope < 0)
        {
            cout << "Error: Pila vacia" << endl;
            return;
        }
        cout << "Eliminado: " << arr[tope--] << endl;
    }
    void mostrar()
    {
        if (tope < 0)
        {
            cout << "Pila vacia" << endl;
            return;
        }
        cout << "Pila final (de tope a base):" << endl;
        for (int i = tope; i >= 0; i--)
        {
            cout << arr[i] << endl;
        }
    }
};
int main()
{
    Pila p;
    cout << "=== Insertando elementos ===" << endl;
    p.push(5);
    p.push(10);
    p.push(15);
    p.push(20);
    p.push(25);
    cout << "\n=== Eliminando dos elementos ===" << endl;
    p.pop();
    p.pop();
    cout << "\n=== Estado final ===" << endl;
    p.mostrar();
    return 0;
}
