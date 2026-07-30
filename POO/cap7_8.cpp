#ifndef TIME6_H
#define TIME6_H
class Time
{
public:
    Time(int = 0, int = 0, int = 0); // default constructor
    Time &setTime(int, int, int);    // set hour, minute, second
    Time &setHour(int);              // set hour
    Time &setMinute(int);            // set minute
    Time &setSecond(int);            // set second
    int getHour() const;             // return hour
    int getMinute() const;           // return minute
    int getSecond() const;           // return second
    void printMilitary() const;      // print military time
    void printStandard() const;      // print standard time
private:
    int hour;   // 0 - 23
    int minute; // 0 - 59
    int second; // 0 - 59
};
#endif
#include <iostream>
using std::cout;
Time::Time(int hr, int min, int sec)
{
    setTime(hr, min, sec);
}
Time &Time::setTime(int h, int m, int s)
{
    setHour(h);
    setMinute(m);
    setSecond(s);
    return *this; // enables cascading
}
Time &Time::setHour(int h)
{
    hour = (h >= 0 && h < 24) ? h : 0;
    return *this; // enables cascading
}
Time &Time::setMinute(int m)
{
    minute = (m >= 0 && m < 60) ? m : 0;
    return *this; // enables cascading
}
Time &Time::setSecond(int s)
{
    second = (s >= 0 && s < 60) ? s : 0;
    return *this; // enables cascading
}
int Time::getHour() const { return hour; }
int Time::getMinute() const { return minute; }
int Time::getSecond() const { return second; }
void Time::printMilitary() const
{
    cout << (hour < 10 ? "0" : "") << hour << ":" << (minute < 10 ? "0" : "") << minute;
}
void Time::printStandard() const
{
    cout << ((hour == 0 || hour == 12) ? 12 : hour % 12)
         << ":" << (minute < 10 ? "0" : "") << minute
         << ":" << (second < 10 ? "0" : "") << second
         << (hour < 12 ? " AM" : " PM");
}
#include <iostream>
using std::cout;
using std::endl;
// #include "time6.h"
int main()
{
    Time t;
    t.setHour(18).setMinute(30).setSecond(22);
    cout << "Military time: ";
    t.printMilitary();
    cout << "\nStandard time: ";
    t.printStandard();
    cout << "\n\nNew standard time: ";
    t.setTime(20, 20, 20).printStandard();
    cout << endl;
    return 0;
}
