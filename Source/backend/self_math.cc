#include "self_math.h"

bool iRRAM::enableReiterate = true;
int iRRAM::MAXiterationnum = 30;
bool iRRAM::alwaysenableReiterate = true;

double get_arc(double a, double b)
{
    const double pi = 3.14159265358979323846;
//    if(a == 0)
//    {
//        if(b == 0) return 0;
//        else return b < 0 ? -pi/2 : pi/2;
//    }
//    else
//    {
//        if(a > 0)
//        {
//            return atan(b/a);
//        }
//        else
//        {
//            if(b > 0) return atan(b/a) + pi;
//            else return atan(b/a) - pi;
//        }
//    }
    return (a == 0 ? (b == 0 ? 0 : (b < 0 ? -pi/2 : pi/2)) : (a > 0 ? atan(b/a) : (atan(b/a) + pi)));
}

//#include "iRRAM/lib.h"
//
//namespace iRRAM
//{
//    inline REAL get_arc(REAL a, REAL b)
//    {
//    //    if(a == 0)
//    //    {
//    //        if(b == 0) return 0;
//    //        else return b < 0 ? -pi/2 : pi/2;
//    //    }
//    //    else
//    //        return a > 0 ? atan(b/a) : (atan(b/a) + pi);
//        return (a == 0 ? (b == 0 ? REAL(0) : (b < 0 ? -pi()/2 : pi()/2)) : (a > 0 ? atan(b/a) : (atan(b/a) + pi())));
//    }
//}

double fac(int n)
{
    double res = 1;
    for(int i = 2; i <= n; ++i) res *= i;
    return res;
}

iRRAM::REAL fac_real(int n)
{
    iRRAM::REAL res = 1;
    for(int i = 2; i <= n; ++i) res = res * i;
    return res;
}
