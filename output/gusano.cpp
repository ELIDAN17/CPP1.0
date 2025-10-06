#include <iostream>
#include <conio.h>
#include <windows.h>
#include <vector>

using namespace std;

bool gameOver;
const int width = 20;
const int height = 17;
int x, y, fruitX, fruitY, score;
enum eDirection { STOP = 0, LEFT, RIGHT, UP, DOWN };
eDirection dir;
vector<pair<int, int>> tail; // Vector para almacenar las posiciones de la cola

void Setup() {
    gameOver = false;
    dir = STOP;
    x = width / 2;
    y = height / 2;
    fruitX = rand() % width;
    fruitY = rand() % height;
    score = 0;
    tail.clear();
}

void Draw() {
    HANDLE hConsole = GetStdHandle(STD_OUTPUT_HANDLE);
COORD position;
position.X=0;
position.Y=0;
SetConsoleCursorPosition(hConsole,position);
    for (int i = 0; i < width + 2; i++)
        cout << "#";
    cout << endl;

    for (int i = 0; i < height; i++) {
        for (int j = 0; j < width; j++) {
            if (j == 0)
                cout << "#"; // Borde izquierdo

            if (i == y && j == x)
                cout << "O"; // Cabeza del gusano
            else if (i == fruitY && j == fruitX)
                cout << "F"; // Fruta
            else {
                bool print = false;
                for (auto &segment : tail) {
                    if (segment.first == j && segment.second == i) {
                        cout << "o";
                        print = true;
                    }
                }
                if (!print)
                    cout << " ";
            }

            if (j == width - 1)
                cout << "#"; // Borde derecho
        }
        cout << endl;
    }

    for (int i = 0; i < width + 2; i++)
        cout << "#";
    cout << endl;

    cout << "Score: " << score << endl;
}

void Input() {
    if (_kbhit()) {
        switch (_getch()) {
        case 'a':
            if (dir != RIGHT) dir = LEFT;
            break;
        case 'd':
            if (dir != LEFT) dir = RIGHT;
            break;
        case 'w':
            if (dir != DOWN) dir = UP;
            break;
        case 's':
            if (dir != UP) dir = DOWN;
            break;
        case 'x':
            gameOver = true;
            break;
        }
    }
}

void Logic() {
    pair<int, int> prev = {x, y}; // Guardar la posición previa de la cabeza
    pair<int, int> prev2;
    if (!tail.empty()) {
        prev2 = tail[0];
        tail[0] = prev;
    }

    for (int i = 1; i < tail.size(); i++) {
        prev = tail[i];
        tail[i] = prev2;
        prev2 = prev;
    }

    switch (dir) {
    case LEFT:
        x--;
        break;
    case RIGHT:
        x++;
        break;
    case UP:
        y--;
        break;
    case DOWN:
        y++;
        break;
    default:
        break;
    }

    if (x >= width) x = 0; else if (x < 0) x = width - 1;
    if (y >= height) y = 0; else if (y < 0) y = height - 1;

    for (auto &segment : tail) {
        if (segment.first == x && segment.second == y)
            gameOver = true;
    }

    if (x == fruitX && y == fruitY) {
        score += 10;
        fruitX = rand() % width;
        fruitY = rand() % height;
        tail.push_back({x, y});
    }
}

int main() {
    Setup();
    while (!gameOver) {
        Draw();
        Input();
        Logic();
        Sleep(100); // Controla la velocidad del juego
    }

    cout << "Game Over! Your score: " << score << endl;
    return 0;
}
