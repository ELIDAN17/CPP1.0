#include <iostream>
#include <vector>
#include <conio.h>
#include <windows.h>
using namespace std;
const int ANCHO = 40;
const int ALTURA = 10;
const char DINO = 'm';
const char OBSTACULO = 'T';
const char SUELO = '=';
void gotoxy(int x, int y){
        COORD coord;
        coord.X=x;
        coord.Y=y;
        SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
    }
class Dinosaurio {
public:
    int x, y;
    bool saltando;
    int alturaSalto;
    Dinosaurio() : x(3), y(ALTURA-2), saltando(false), alturaSalto(0) {}
    void saltar() {
        if (!saltando) {
            saltando = true;
            alturaSalto = 0;
        }
    }
    void actualizar() {
        if (saltando) {
            y--;
            alturaSalto++;
            if (alturaSalto >=3) {
                saltando = false;
            }
        } else if (y<ALTURA-2) {
            y++;
        }
    }
    void dibujar() const {
        gotoxy(x, y);
        cout<<DINO;
    }
};
class Obstaculo {
public:
    int x, y;
    Obstaculo(int startX) : x(startX), y(ALTURA - 2) {}
    void actualizar() {
        x--;
    }
    void dibujar() const {
        gotoxy(x, y);
        cout << OBSTACULO;
    }
    bool fueraDePantalla() const {
        return x < 0;
    }
};
class Juego {
private:
    Dinosaurio dino;
    vector<Obstaculo> obstaculos;
    bool juegoTerminado;
    int puntaje;
public:
    Juego() : juegoTerminado(false), puntaje(0) {}
    void Mapa() {
        system("cls");
        cout<<"                Dino Run"<<endl;
        cout<<"-----------------------------------------"<<endl;
        dino.dibujar();
        for (const auto &obstaculo : obstaculos) {
            obstaculo.dibujar();
        }
        for (int i = 0; i < ANCHO; i++) {
            gotoxy(i, ALTURA - 1);
            cout << SUELO;
        }
        gotoxy(0, 10);
        cout << "Puntaje: " << puntaje;
    }
    void actualizarJuego() {
        dino.actualizar();
        for (auto &obstaculo : obstaculos) {
            obstaculo.actualizar();
            // colisión
            if (obstaculo.x == dino.x && obstaculo.y == dino.y) {
                juegoTerminado = true;
            }
        }
        if (!obstaculos.empty() && obstaculos.front().fueraDePantalla()) {
            obstaculos.erase(obstaculos.begin());
            puntaje++;
        }
        if (rand() % 20 == 0) {
            obstaculos.emplace_back(ANCHO - 1);
        }
    }
    void manejar() {
        if (_kbhit()) {
            char tecla = _getch();
            if (tecla == ' ') {
                dino.saltar();
            }
        }
    }
    void ejecutar() {
        int x; cout<<"---------------------------"<<endl;
        cout<<"BIENVENIDO AL JUEGO DINO RUN"<<endl;
        cout<<"Presione 1 para iniciar: ";cin>>x;
        if(x==1){
        srand(time(0));
        while (!juegoTerminado) {
            Mapa();
            manejar();
            actualizarJuego();
            Sleep(100);
        }
        gotoxy(0, ALTURA);
        cout<<"\n";
        cout<<"-------------------------------------"<<endl;
        cout<<"|  Fin del juego. Puntaje Final: "<<puntaje<<"  |"<<endl;
        cout<<"-------------------------------------"<<endl;
        cout<<"\n"<<endl;
        system("pause");
        system("cls");
        }else{ cout<<"valor invalido";}
    }
};
int main() {
    Juego juego;
    juego.ejecutar();
    return 0;
}
