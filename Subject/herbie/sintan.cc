#include "iRRAM.h"

iRRAM::REAL irram_sintan(iRRAM::REAL x)
{
    iRRAM::REAL a = x - iRRAM::sin(x);
    iRRAM::REAL b = x - iRRAM::tan(x);
    iRRAM::REAL r = a / b;
    return r;
}
