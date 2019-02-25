#include "iRRAM.h"

iRRAM::REAL irram_quadm(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL c)
{
    iRRAM::REAL d = -b - iRRAM::sqrt(b * b - 4 * a * c);
    iRRAM::REAL r = d / (2 * a);
    return r;
}
