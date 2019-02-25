#include "iRRAM.h"

iRRAM::REAL irram_logs(iRRAM::REAL n)
{
    iRRAM::REAL r = (n + 1) * iRRAM::log(n + 1) - n * iRRAM::log(n) - 1;
    return r;
}
