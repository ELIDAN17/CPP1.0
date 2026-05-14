#include <iostream>
#define MAX 100
using namespace std;
class Cola
{
private:
    int arr[MAX], frente, final, cantidad;

public:
    Cola()
    {
        frente = 0;
        final = -1;
        cantidad = 0;
    }
    void enqueue(int valor)
    {
        if (cantidad >= MAX)
        {
            cout << "Error: Cola llena" << endl;
            return;
        }
        final = (final + 1) % MAX;
        arr[final] = valor;
        cantidad++;
        cout << "Encolado: " << valor << endl;
    }
    void dequeue()
    {
        if (cantidad <= 0)
        {
            cout << "Error: Cola vacia" << endl;
            return;
        }
        cout << "Desencolado: " << arr[frente] << endl;
        frente = (frente + 1) % MAX;
        cantidad--;
    }
    void mostrar()
    {
        if (cantidad <= 0)
        {
            cout << "Cola vacia" << endl;
            return;
        }
        cout << "Cola final (de frente a final):" << endl;
        for (int i = 0; i < cantidad; i++)
        {
            int idx = (frente + i) % MAX;
            cout << arr[idx] << endl;
        }
    }
};
int main()
{
    Cola c;
    cout << "=== Encolando elementos ===" << endl;
    c.enqueue(3);
    c.enqueue(6);
    c.enqueue(9);
    c.enqueue(12);
    cout << "\n=== Desencolando un elemento ===" << endl;
    c.dequeue();
    cout << "\n=== Estado final ===" << endl;
    c.mostrar();
    return 0;
}
