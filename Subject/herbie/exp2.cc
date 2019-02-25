#include "iRRAM.h"

iRRAM::REAL irram_exp2(iRRAM::REAL x)
{
    iRRAM::REAL r = (iRRAM::exp(x) - 2) + iRRAM::exp(-x);
    return r;
}
