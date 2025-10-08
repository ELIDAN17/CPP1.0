#include <iostream>
using namespace std;

int main() {
    double X, Y, Z;
    bool result = false;
    cout<<"Ingrese los valores para X, Y y Z: "<<endl;
    cin>>X>>Y>>Z;
    if((X>Y)&&(Y>Z)){ cout<<"analizis"<<endl;
        bool conXmayorY =(X>Y); cout<<conXmayorY<<" - ";
        bool conYmayorZ =(Y>Z); cout<<conYmayorZ<<endl;
        if(conXmayorY == conYmayorZ){
            result = true; cout<<result<<endl;;
            if(result == true){
                cout << "La condicion es verdadera." << endl;
                cout << "Por lo tanto, x > z es cierto." << endl;
            }
        }
    }else{cout<<"la condicion no se cumple por lo tanto es falsa.";}
    
}



/*
class Proposicion {
private:
    double x;
    double y;
    double z;

public:
    Proposicion(double x, double y, double z);
    bool evaluar();
};

Proposicion::Proposicion(double x, double y, double z) : x(x), y(y), z(z) {}

bool Proposicion::evaluar() {
    bool condicion1 = x > y;
    bool condicion2 = y > z;

    return condicion1 && condicion2;
}

int main() {
    double x, y, z;

    cout << "Ingrese los valores de x, y y z:" << std::endl;
    cin >> x >> y >> z;

    Proposicion prop(x, y, z);

    bool resultado = prop.evaluar();

    if (resultado) {
        cout << "La proposición es verdadera." << std::endl;
    } else {
        cout << "La proposición es falsa." << std::endl;
    }

    return 0;
}
*/