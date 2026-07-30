#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;
//Movimiento Parabolico
int main(){
    float e,vt,ve,g=9.76,a,an,r,pi=3.141592,tv,ae,at,e1;
    cout<<"ingrese el angulo: "; cin>>a;
    cout<<"ingrese velocidad inical experimental: "; cin>>ve;
    cout<<"ingrese tiempo de vuelo: "; cin>>tv;
    an=a*(pi/180); //cout<<"an: "<<an<<endl;
    r=((ve*ve)*sin(2*an))/g; //4.39cout<<"r: "<<r<<endl;
    vt=(tv*g)/(2*sin(an));
    e=((vt-ve)/vt)*100;
    cout<<"valor teorico: "<<vt<<endl;
    cout<<"Error porcentual: "<<fabs(e)<<"%"<<endl;
    cout<<"ingrese alcace max experimental: "; cin>>ae;
    at=((vt*vt)*sin(2*an))/g;
    e1=((at-ae)/at)*100;
    cout<<"alcance teorico: "<<at<<endl;
    cout<<"error porcentual: "<<fabs(e1)<<"%"<<endl;
    return 0;
    
}