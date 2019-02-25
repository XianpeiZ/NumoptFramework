#include "iRRAM.h"

iRRAM::REAL irram_2isqrt(iRRAM::REAL x)
{
    iRRAM::REAL r = 1 / iRRAM::sqrt(x) - 1 / iRRAM::sqrt(x + 1);
    return r;
}
