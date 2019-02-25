#include "iRRAM.h"

iRRAM::REAL irram_expm1(iRRAM::REAL x)
{
    iRRAM::REAL r = iRRAM::exp(x) - 1;
    return r;
}
