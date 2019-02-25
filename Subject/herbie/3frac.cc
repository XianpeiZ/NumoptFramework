#include "iRRAM.h"

iRRAM::REAL irram_3frac(iRRAM::REAL x)
{
    iRRAM::REAL r = 1 / (x + 1) - 2 / x + 1 / (x - 1);
    return r;
}
