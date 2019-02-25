#include "iRRAM.h"

iRRAM::REAL irram_2cbrt(iRRAM::REAL x)
{
    iRRAM::REAL n = iRRAM::REAL(1) / iRRAM::REAL(3);
    iRRAM::REAL a = iRRAM::power(x + 1, n);
    iRRAM::REAL b = iRRAM::power(x, n);
    iRRAM::REAL r = a - b;
    return r;
}
