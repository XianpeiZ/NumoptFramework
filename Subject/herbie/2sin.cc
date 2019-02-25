#include "iRRAM.h"

iRRAM::REAL irram_2sin(iRRAM::REAL x, iRRAM::REAL e)
{
    iRRAM::REAL r = iRRAM::sin(x + e) - iRRAM::sin(x);
    return r;
}
