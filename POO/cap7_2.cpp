#include <iostream>
using std::cout;
using std::endl;
class Increment
{
public:
    Increment(int c = 0, int i = 1);
    void addIncrement() { count += increment; }
    void print() const;

private:
    int count;
    const int increment; // const data member
};
Increment::Increment(int c, int i)
    : increment(i) // initializer for const member
{
    count = c;
}
void Increment::print() const
{
    cout << "count = " << count
         << ", increment = " << increment << endl;
}
int main()
{
    Increment value(10, 5);
    cout << "Before incrementing: ";
    value.print();
    for (int j = 0; j < 3; j++)
    {
        value.addIncrement();
        cout << "After increment " << j + 1 << ": ";
        value.print();
    }
    return 0;
}
