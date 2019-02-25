#include "iRRAM.h"

iRRAM::REAL irram_2nthrt(iRRAM::REAL x, iRRAM::REAL n)
{
    iRRAM::REAL a = iRRAM::power(x + 1, 1 / n);
    iRRAM::REAL b = iRRAM::power(x, 1 / n);
    iRRAM::REAL r = a - b;
    return r;
}
