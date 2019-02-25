#include "iRRAM.h"


iRRAM::REAL irram_cos2(iRRAM::REAL x)
{
    return (1 - iRRAM::cos(x)) / (x * x);
}