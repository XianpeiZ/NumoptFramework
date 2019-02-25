#ifndef SELF_MATH_H
#define SELF_MATH_H

#include <cmath>
#include "iRRAM/lib.h"
/**
input (a, b) represents a vector
get the angle between vector (a, b) and vector (1, 0)
the return value is in [-pi/2, 3*pi/2)
**/

//extern bool iRRAM::enableReiterate;
//extern int iRRAM::MAXiterationnum;
//extern bool iRRAM::alwaysenableReiterate;

double get_arc(double a, double b);

double fac(int n);

iRRAM::REAL fac_real(int n);

#endif
