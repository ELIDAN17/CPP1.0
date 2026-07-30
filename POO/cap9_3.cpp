#include <iostream>

using namespace std;

class Point
{
public:
    Point(int = 0, int = 0);
    ~Point();

protected:
    int x, y;
};

Point::Point(int a, int b)
{
    x = a;
    y = b;

    cout << "Point  constructor: "
         << '[' << x << ", " << y << ']' << endl;
}

Point::~Point()
{
    cout << "Point  destructor:  "
         << '[' << x << ", " << y << ']' << endl;
}

class Circle : public Point
{
public:
    Circle(double r = 0.0, int x = 0, int y = 0);
    ~Circle();

private:
    double radius;
};

Circle::Circle(double r, int a, int b)
    : Point(a, b)
{
    radius = r;
    cout << "Circle constructor: radius is "
         << radius << " [" << x << ", " << y << ']' << endl;
}

Circle::~Circle()
{
    cout << "Circle destructor:  radius is "
         << radius << " [" << x << ", " << y << ']' << endl;
}

int main()
{
    {
        Point p(11, 22);
    }

    cout << endl;
    Circle circle1(4.5, 72, 29);
    cout << endl;
    Circle circle2(10, 5, 5);
    cout << endl;
    return 0;
}