#include "iRRAM.h"

iRRAM::REAL irram_2atan(iRRAM::REAL N)
{
    iRRAM::REAL r = iRRAM::atan(N + 1) - iRRAM::atan(N);
    return r;
}
