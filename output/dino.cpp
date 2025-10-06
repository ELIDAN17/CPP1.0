#include <iostream>
#include <conio.h>
#include <windows.h>
#include <vector>
using namespace std;
class objetoJuego {
public:
    int x, y;
    char representation;
    objetoJuego(int x, int y, char rep) : x(x), y(y), representation(rep) {}
    virtual void Mapa() const {
        cout << representation;
    }
};
class Jugador : public objetoJuego {
private:
    bool saltando;
    int saltoAlto;
    int inicioY;
    int contador;
public:
    Jugador(int x, int y) : objetoJuego(x, y, 'm'), saltando(false), saltoAlto(4), contador(0) {
        inicioY = y;
    }
    void Saltar() {
        if (!saltando) {
            saltando = true;
            contador = 0;
        }
    }
    void Actualizar() {
        if (saltando) {
            if (contador < saltoAlto) {
                y--;
                contador++;
            } else if (contador < saltoAlto * 2) {
                y++;
                contador++;
            } else {
                saltando = false;
                y = inicioY;
            }
        }
    }
};
class Obstaculo : public objetoJuego{
public:
    Obstaculo(int x, int y) : objetoJuego(x, y, 'T') {}
    void Mover() {
        x--;
    }
};
class Juego {
private:
    const int ancho; //mapa
    const int altura; //mapa
    Jugador jugador1;
    Obstaculo obstaculo;
    bool finJuego;
    int puntaje;
public:
    Juego(int a, int h) : ancho(a), altura(h), jugador1(2, altura - 2), obstaculo(a - 1, altura - 2), finJuego(false), puntaje(0) {}
    void Mapa() {
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
        cout<<"     + DINO RUN +"<<endl;
        for (int i=0; i<ancho+2; i++)
            cout<<"="; //panel superior
        cout<<endl;
        for (int i=0; i<altura; i++) {
            for (int j=0; j<ancho; j++) {
                if (j == 0)
                    cout << "||"; //panel izquierdo
                if (i == jugador1.y && j == jugador1.x)
                    jugador1.Mapa();
                else if (i == obstaculo.y && j == obstaculo.x)
                    obstaculo.Mapa();
                else if (i == altura - 1)
                    cout << "="; //panel piso
                else
                    cout << " ";
            }
            cout << "||" << endl; // panel derecho
        }
        for (int i=0; i<ancho+2; i++)
            cout << ".";
        cout << endl;
        cout << "Puntaje: " <<puntaje<< endl;
        for (int i=0; i<ancho+2; i++)
            cout << ".";
        cout << endl;
    }
    void Input() {
        if (_kbhit()) {
            switch (_getch()) {
            case ' ':
                jugador1.Saltar();
                break;
            case 'x':
                finJuego = true;
                break;
            }
        }
    }
    void Logica() {
        obstaculo.Mover();
        jugador1.Actualizar();

        if (obstaculo.x < 0) {
            obstaculo.x = ancho - 1;
            puntaje++;
        }

        if (obstaculo.x == jugador1.x && obstaculo.y == jugador1.y) {
            finJuego = true;
        }
    }
    void Ejecutar() {
        int x; cout<<"---------------------------"<<endl;
        cout<<"BIENVENIDO AL JUEGO DINO RUN"<<endl;
        cout<<"Presione 1 para iniciar: ";cin>>x;
        if(x==1){
        while (!finJuego) {
            Mapa();
            Input();
            Logica();
            Sleep(50); // Controla la velocidad del juego
        }
        cout<<"======================="<<endl;
        cout<<"|    FIN DEL JUEGO     |"<<endl;
        cout<<"| Puntaje obtenido: " << puntaje <<" |"<< endl;
        cout<<"======================="<<endl; 
        cout<<endl;
        system("pause");
        HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
        }else{cout<<"valor invalido";HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);}
    }
};
int main() {
    Juego juego(20, 10);
    juego.Ejecutar();
    return 0;
}