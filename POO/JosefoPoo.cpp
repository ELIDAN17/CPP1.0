#include <iostream>
using namespace std;

const int MAX_SIZE = 100000; // Máximo tamaño del círculo

// Estructura de un elemento de la cola
typedef struct Node {
    int data;
    Node* next;
} Node;

class Queue {
private:
    Node* front;
    Node* rear;
    int size;
    
public:
    Queue() : front(nullptr), rear(nullptr), size(0) {}
    
    void enqueue(int val) {
        Node* newNode = new Node();
        newNode->data = val;
        newNode->next = nullptr;
        
        if (rear == nullptr) {
            front = rear = newNode;
        } else {
            rear->next = newNode;
            rear = newNode;
        }
        size++;
    }
    
    int dequeue() {
        if (front == nullptr) return -1; // Cola vacía
        
        int temp = front->data;
        Node* tempNode = front;
        front = front->next;
        
        if (front == nullptr) {
            rear = nullptr;
        }
        
        delete tempNode;
        size--;
        return temp;
    }
    
    bool isEmpty() { return (front == nullptr); }
};

int josephusProblem(int n, int k) {
    Queue q;
    
    // Insertar todos los números del 1 al n en la cola
    for (int i = 1; i <= n; i++) {
        q.enqueue(i);
    }
    
    int count = 0;
    while (!q.isEmpty()) {
        count++;
        if (count % k != 0) {
            q.dequeue(); // Eliminar el k-ésimo elemento
        } else {
            return q.front->data; // Devolver el primer elemento de la cola
        }
    }
    
    return -1; // No debería llegar aquí
}

int main() {
    int n, k;
    cout << "Ingrese el número total de personas: ";
    cin >> n;
    cout << "Ingrese el valor de k: ";
    cin >> k;
    
    int result = josephusProblem(n, k);
    
    if (result != -1) {
        cout << "La posición inicial de la persona que escapará es: " << result << endl;
    } else {
        cout << "Error en la solución." << endl;
    }
    
    return 0;
}
