#include "iRRAM.h"

iRRAM::REAL irram_2log(iRRAM::REAL N)
{
    iRRAM::REAL r;
    r = iRRAM::log(N + 1) - iRRAM::log(N);
    return r;
}
