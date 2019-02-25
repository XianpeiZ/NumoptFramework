#include "iRRAM.h"

iRRAM::REAL irram_2tan(iRRAM::REAL x, iRRAM::REAL e)
{
    iRRAM::REAL r = iRRAM::tan(x + e) - iRRAM::tan(x);
    return r;
}
