#include "iRRAM.h"

iRRAM::REAL irram_quad2m(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL c)
{
    iRRAM::REAL r = ((-b / 2) - iRRAM::sqrt(b * b / 4 - a * c)) / a;
    return r;
}
