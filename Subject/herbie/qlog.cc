#include "iRRAM.h"

iRRAM::REAL irram_qlog(iRRAM::REAL x)
{
    iRRAM::REAL a = iRRAM::log(1 - x);
    iRRAM::REAL b = iRRAM::log(1 + x);
    return a / b;
}