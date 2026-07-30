#include <iostream>
#include <conio.h>
#include <windows.h>

using namespace std;

bool finJuego; //bool gameOver;
const int ancho = 40;    //const int width = 20;
const int altura = 10;   //const int height = 10;
int x, y, obstaculo, puntaje;  // int x, y, obstacleX, score;
bool saltar;   //bool jump;

void configuracion(){  //void Setup() {
    finJuego = false;
    x = 2; 
    y = altura -2;  //y = height - 2;
    obstaculo = ancho -2;  //obstacleX = width - 1;
    puntaje = 0;   //score = 0;
    saltar = false;  //jump = false;
}

void mapa(){    //void Draw() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position); // Borra la pantalla

    for (int i = 0; i < ancho + 2; i++)
        cout << "#";
    cout << endl;

    for (int i = 0; i < altura; i++) {
        for (int j = 0; j < ancho; j++) {
            if (j == 0)
                cout << "||"; // Borde izquierdo
            if (i == y && j == x)
                cout << "¬O°"; // Jugador
            else if (i == altura - 1)
                cout << "="; // Suelo
            else if (i == altura - 2 && j == obstaculo)
                cout << "T"; // Obstáculo
            else
                cout << " ";
        }
        cout << "||" << endl; // Borde derecho
    }

    for (int i = 0; i < ancho + 2; i++)
        cout << "#";
    cout << endl;

    cout << "Puntaje: " << puntaje << endl;
}

void entrada() {
    if (_kbhit()) {
        switch (_getch()) {
        case ' ':
            if (!saltar) {
                saltar = true;
            }
            break;
        case 'x':
            finJuego = true;
            break;
        }
    }
}

void Logica() {
    if (saltar) {
        y -= 1;
        if (y < altura - 4) {
            saltar = false;
        }
    } else if (y < altura - 2) {
        y += 1;
    }

    obstaculo--;
    if (obstaculo < 0) {
        obstaculo = ancho - 1;
        puntaje++;
    }

    if (obstaculo == x && y == altura - 2) {
        finJuego = true;
    }
}

int main() {
    configuracion();
    while (!finJuego) {
        mapa();
        entrada();
        Logica();
        Sleep(50); // Controla la velocidad del juego
    }

    cout << "Fin del Juego! su Puntaje es: " << puntaje << endl;
    return 0;
}
