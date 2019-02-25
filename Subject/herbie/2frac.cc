#include "iRRAM.h"

iRRAM::REAL irram_2frac(iRRAM::REAL x)
{
    iRRAM::REAL r = 1 / (x + 1) - 1 / x;
    return r;
}
