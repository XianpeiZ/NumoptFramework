#include "iRRAM.h"

iRRAM::REAL irram_2cos(iRRAM::REAL x, iRRAM::REAL e)
{
    iRRAM::REAL r = iRRAM::cos(x + e) - iRRAM::cos(x);
    return r;
}
