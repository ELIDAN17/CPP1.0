#include <iostream>
#include <iomanip>
#include <cmath>

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

ostream &operator<<(ostream &output, const Point &p)
{
    output << '[' << p.x << ", " << p.y << ']';
    return output;
}

Point::Point(int a, int b)
{
    setPoint(a, b);
}

void Point::setPoint(int a, int b)
{
    x = a;
    y = b;
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

class Cylinder : public Circle
{
    friend ostream &operator<<(ostream &, const Cylinder &);

public:
    Cylinder(double h = 0.0, double r = 0.0, int x = 0, int y = 0);
    void setHeight(double);
    double getHeight() const;
    double area() const;
    double volume() const;

protected:
    double height;
};

Cylinder::Cylinder(double h, double r, int x, int y)
    : Circle(r, x, y)
{
    setHeight(h);
}

void Cylinder::setHeight(double h)
{
    height = (h >= 0 ? h : 0);
}

double Cylinder::getHeight() const
{
    return height;
}

double Cylinder::area() const
{
    return 2 * Circle::area() + 2 * 3.14159 * radius * height;
}

double Cylinder::volume() const
{
    return Circle::area() * height;
}

ostream &operator<<(ostream &output, const Cylinder &c)
{
    output << static_cast<Circle>(c)
           << "; Height = " << c.height;
    return output;
}

int main()
{
    Cylinder cyl(5.7, 2.5, 12, 23);

    cout << "X coordinate is " << cyl.getX()
         << "\nY coordinate is " << cyl.getY()
         << "\nRadius is " << cyl.getRadius()
         << "\nHeight is " << cyl.getHeight() << "\n\n";

    cyl.setHeight(10);
    cyl.setRadius(4.25);
    cyl.setPoint(2, 2);

    cout << "The new location, radius, and height of cyl are:\n"
         << cyl << '\n';

    cout << "The area of cyl is:\n"
         << cyl.area() << '\n';

    Point &pRef = cyl;
    cout << "\nCylinder printed as a Point is: "
         << pRef << "\n\n";

    Circle &circleRef = cyl;
    cout << "Cylinder printed as a Circle is:\n"
         << circleRef
         << "\nArea: " << circleRef.area() << endl;

    return 0;
}
