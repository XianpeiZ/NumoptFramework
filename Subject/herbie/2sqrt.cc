#include "iRRAM.h"

iRRAM::REAL irram_2sqrt(iRRAM::REAL x)
{
    iRRAM::REAL r = iRRAM::sqrt(x + 1) - iRRAM::sqrt(x);
    return r;
}
