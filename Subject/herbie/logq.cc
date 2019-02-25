#include "iRRAM.h"

iRRAM::REAL irram_logq(iRRAM::REAL e)
{
    iRRAM::REAL a = 1 - e;
    iRRAM::REAL b = 1 + e;
    iRRAM::REAL r = iRRAM::log(a / b);
    return r;
}
