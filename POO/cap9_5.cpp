#include <iostream>

using namespace std;

class Base1
{
public:
    Base1(int x) { value = x; }
    int getData() const { return value; }

protected:
    int value;
};

class Base2
{
public:
    Base2(char c) { letter = c; }
    char getData() const { return letter; }

protected:
    char letter;
};

class Derived : public Base1, public Base2
{
    friend ostream &operator<<(ostream &, const Derived &);

public:
    Derived(int, char, double);
    double getReal() const;

private:
    double real;
};

Derived::Derived(int i, char c, double f)
    : Base1(i), Base2(c), real(f) {}

double Derived::getReal() const
{
    return real;
}

ostream &operator<<(ostream &output, const Derived &d)
{
    output << "    Integer: " << d.value
           << "\n  Character: " << d.letter
           << "\nReal number: " << d.real;
    return output;
}

int main()
{
    Base1 b1(10);
    Base2 b2('Z');
    Derived d(7, 'A', 3.5);

    cout << "Object b1 contains integer " << b1.getData()
         << "\nObject b2 contains character " << b2.getData()
         << "\nObject d contains:\n"
         << d << "\n\n";

    cout << "Data members of Derived can be"
         << " accessed individually:"
         << "\n    Integer: " << d.Base1::getData()
         << "\n  Character: " << d.Base2::getData()
         << "\nReal number: " << d.getReal() << "\n\n";

    cout << "Derived can be treated as an "
         << "object of either base class:\n";

    Base1 *base1Ptr = &d;
    cout << "base1Ptr->getData() yields "
         << base1Ptr->getData() << '\n';

    Base2 *base2Ptr = &d;
    cout << "base2Ptr->getData() yields "
         << base2Ptr->getData() << endl;

    return 0;
}
