#ifndef TIME5_H
#define TIME5_H
class Time
{
public:
    Time(int = 0, int = 0, int = 0); // default constructor
    void setTime(int, int, int);     // set time
    void setHour(int);               // set hour
    void setMinute(int);             // set minute
    void setSecond(int);             // set second
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
// #include "time5.h"
Time::Time(int hr, int min, int sec)
{
    setTime(hr, min, sec);
}
void Time::setTime(int h, int m, int s)
{
    setHour(h);
    setMinute(m);
    setSecond(s);
}
void Time::setHour(int h)
{
    hour = (h >= 0 && h < 24) ? h : 0;
}
void Time::setMinute(int m)
{
    minute = (m >= 0 && m < 60) ? m : 0;
}
void Time::setSecond(int s)
{
    second = (s >= 0 && s < 60) ? s : 0;
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
    cout << "    " << std::endl;
    cout << ((hour == 12) ? 12 : hour % 12) << ":"
         << (minute < 10 ? "0" : "") << minute << ":"
         << (second < 10 ? "0" : "") << second
         << (hour < 12 ? " AM" : " PM");
}
int main()
{
    Time wakeUp(6, 45, 0);     // non-constant object
    const Time noon(12, 0, 0); // constant object
    wakeUp.setHour(18);        // non-const         non-const
    //    noon.setHour(12);          // non-const         const
    wakeUp.getHour();     // const             non-const
    noon.getMinute();     // const             const
    noon.printMilitary(); // const             const
    noon.printStandard(); // non-const         const
    return 0;
}
