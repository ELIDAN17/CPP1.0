#include <iostream>
#include <iomanip>

using namespace std;

class Point
{
    friend ostream &operator<<(ostream &, const Point &);

public:
    Point(int = 0, int = 0);
    void setPoint(int, int);
    int getX() const { return x; }
    int getY() const { return y; }

protected:
    int x, y;
};

Point::Point(int a, int b)
{
    setPoint(a, b);
}

void Point::setPoint(int a, int b)
{
    x = a;
    y = b;
}

ostream &operator<<(ostream &output, const Point &p)
{
    output << '[' << p.x << ", " << p.y << ']';
    return output;
}

class Circle : public Point
{
    friend ostream &operator<<(ostream &, const Circle &);

public:
    Circle(double r = 0.0, int x = 0, int y = 0);
    void setRadius(double);
    double getRadius() const;
    double area() const;

protected:
    double radius;
};

Circle::Circle(double r, int a, int b)
    : Point(a, b)
{
    setRadius(r);
}

void Circle::setRadius(double r)
{
    radius = (r >= 0 ? r : 0);
}

double Circle::getRadius() const
{
    return radius;
}

double Circle::area() const
{
    return 3.14159 * radius * radius;
}

ostream &operator<<(ostream &output, const Circle &c)
{
    output << "Center = " << static_cast<Point>(c)
           << "; Radius = "
           << setiosflags(ios::fixed | ios::showpoint)
           << setprecision(2) << c.radius;
    return output;
}

int main()
{
    Point *pointPtr = 0, p(30, 50);
    Circle *circlePtr = 0, c(2.7, 120, 89);

    cout << "Point p: " << p << "\nCircle c: " << c << '\n';

    pointPtr = &c;
    cout << "\nCircle c (via *pointPtr): "
         << *pointPtr << '\n';

    circlePtr = static_cast<Circle *>(pointPtr);
    cout << "\nCircle c (via *circlePtr):\n"
         << *circlePtr
         << "\nArea of c (via circlePtr): "
         << circlePtr->area() << '\n';
    pointPtr = &p;
    circlePtr = static_cast<Circle *>(pointPtr);
    cout << "\nPoint p (via *circlePtr):\n"
         << *circlePtr
         << "\nArea of object circlePtr points to: "
         << circlePtr->area() << endl;

    return 0;
}
