#include "iRRAM.h"

iRRAM::REAL irram_expax(iRRAM::REAL a, iRRAM::REAL x)
{
    iRRAM::REAL r = iRRAM::exp(a * x) - 1;
    return r;
}
