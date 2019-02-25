#include "iRRAM.h"

iRRAM::REAL irram_expq3(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL e)
{
    iRRAM::REAL abe = e * (iRRAM::exp((a + b) * e) - 1);
    iRRAM::REAL ae = iRRAM::exp(a * e) - 1;
    iRRAM::REAL be = iRRAM::exp(b * e) - 1;
    iRRAM::REAL r = abe / (ae * be);
    return r;
}
