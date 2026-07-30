#include <iostream>
using std::cout;
using std::endl;
class Count
{
public:
    Count() { x = 0; }                         // constructor
    void print() const { cout << x << endl; }  // output
    friend void cannotSetX(Count &c, int val); // declare as friend
private:
    int x; // data member
};
void cannotSetX(Count &c, int val)
{
    c.x = val; // now accessible because it's a friend
}
int main()
{
    Count counter;
    cannotSetX(counter, 3); // cannotSetX is not a friend
    return 0;
}
