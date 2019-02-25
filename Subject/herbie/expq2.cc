#include "iRRAM.h"

iRRAM::REAL irram_expq2(iRRAM::REAL x)
{
    iRRAM::REAL r = iRRAM::exp(x) / (iRRAM::exp(x) - 1);
    return r;
}
