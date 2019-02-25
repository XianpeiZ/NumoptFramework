#include "iRRAM.h"

iRRAM::REAL irram_tanhf(iRRAM::REAL x)
{
    iRRAM::REAL r = (1 - iRRAM::cos(x)) / iRRAM::sin(x);
    return r;
}
