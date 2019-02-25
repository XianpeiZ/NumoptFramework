#include "iRRAM.h"

iRRAM::REAL irram_sqrtexp(iRRAM::REAL x)
{
    iRRAM::REAL r = iRRAM::sqrt((iRRAM::exp(2 * x) - 1) / (iRRAM::exp(x) - 1));
    return r;
}
