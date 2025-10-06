#include <iostream>
using namespace std;
int fibonacci(int n) {
    if (n == 0)
        return 0;
    else if (n == 1)
        return 1;
    else
        return fibonacci(n-1) + fibonacci(n-2);
}

int main() {
    int n;
    cout << "Ingrese el número limite de Fibonacci: "; cin >> n;
    cout << "Secuencia de Fibonacci hasta " << n << ": ";
    int i = 1;
    if ( n<0 ) cout<<"No valido, inrese un valor positivo.";
    while (i <= n) {
        cout << fibonacci(i) << " ";
        i++;
    }
    cout << endl; cout << "El numero Fibonacci en la posicion "<<n<<" es: "<<fibonacci(i-1)<<endl;
    return 0;
}
