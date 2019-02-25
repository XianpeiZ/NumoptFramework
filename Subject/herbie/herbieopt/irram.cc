#include "iRRAM.h"

// Herbie Case: 2log
iRRAM::REAL irram_2log(iRRAM::REAL N) {
    return iRRAM::log(N+1) - iRRAM::log(N);
}

// Herbie Case: cos2
iRRAM::REAL irram_cos2(iRRAM::REAL x) {
    return (1-iRRAM::cos(x))/(x*x);
}

// Herbie case: exp2
iRRAM::REAL irram_exp2(iRRAM::REAL x) {
    return (iRRAM::exp(x) - 2 ) + iRRAM::exp(-x);
}

// Herbie case: expax
iRRAM::REAL irram_expax(iRRAM::REAL a, iRRAM::REAL x) {
    return iRRAM::exp(a*x) - 1;
}

// Herbie case: expm1
iRRAM::REAL irram_expm1(iRRAM::REAL x) {
    return iRRAM::exp(x) - 1;
}

// Herbie case: expq2
iRRAM::REAL irram_expq2(iRRAM::REAL x) {
    return iRRAM::exp(x)/(iRRAM::exp(x)-1);
}

// Herbie case: invcot
iRRAM::REAL irram_invcot(iRRAM::REAL x) {
    return 1/x-1/iRRAM::tan(x);
}

// Herbie case: quad2m
iRRAM::REAL irram_quad2m(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL c) {
    return ((-b/2)-iRRAM::sqrt(b*b/4-a*c))/a;
}

// Herbie case: quadp
iRRAM::REAL irram_quadp(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL c) {
    iRRAM::REAL d = -b + iRRAM::sqrt(b*b-4*a*c);
    return d/(2*a);
}

// Herbie case: quadm
iRRAM::REAL irram_quadm(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL c) {
    iRRAM::REAL d = -b - iRRAM::sqrt(b*b-4*a*c);
    return d/(2*a);
}

// Herbie case: sintan
iRRAM::REAL irram_sintan(iRRAM::REAL x) {
    iRRAM::REAL a = x - iRRAM::sin(x);
    iRRAM::REAL b = x - iRRAM::tan(x);
    return a/b;
}

// Herbie case: sqrtexp
iRRAM::REAL irram_sqrtexp(iRRAM::REAL x) {
    return iRRAM::sqrt(iRRAM::exp(x)+1);
}

// Herbie case: quad2p
iRRAM::REAL irram_quad2p(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL c) {
    return ((-b/2)+iRRAM::sqrt(b*b/4-a*c))/a;
}

// Herbie case: 2nthrt 
iRRAM::REAL irram_2nthrt(iRRAM::REAL x, iRRAM::REAL n) {
    iRRAM::REAL a = iRRAM::power(x+1, 1/n);
    iRRAM::REAL b = iRRAM::power(x, 1/n);
    return a - b;
}

// Herbie case: 2frac
iRRAM::REAL irram_2frac(iRRAM::REAL x) {
    iRRAM::REAL a = 1/(x+1);
    iRRAM::REAL b = 1/x;
    return a - b;
}

// Herbie case: 2cos
iRRAM::REAL irram_2cos(iRRAM::REAL e, iRRAM::REAL x) {
    return iRRAM::cos(x+e) - iRRAM::cos(x);
}

// Herbie case: 2cbrt
iRRAM::REAL irram_2cbrt(iRRAM::REAL x) {
    iRRAM::REAL n = iRRAM::REAL(1)/iRRAM::REAL(3);
    iRRAM::REAL a = iRRAM::power(x+1, n);
    iRRAM::REAL b = iRRAM::power(x, n);
    return a - b;
}

// Herbie case: tanhf
iRRAM::REAL irram_tanhf(iRRAM::REAL x) {
    return (1-iRRAM::cos(x))/iRRAM::sin(x);
}

// Herbie case: qlog
iRRAM::REAL irram_qlog(iRRAM::REAL x) {
    iRRAM::REAL a = iRRAM::log(1-x);
    iRRAM::REAL b = iRRAM::log(1+x);
    return a/b;
}

// Herbie case: logq
iRRAM::REAL irram_logq(iRRAM::REAL eps) {
    iRRAM::REAL a = 1 - eps;
    iRRAM::REAL b = 1 + eps;
    return iRRAM::log(a/b);
    
}

// Herbie case: logs
iRRAM::REAL irram_logs(iRRAM::REAL n) {
    return (n+1)*iRRAM::log(n+1) - n*iRRAM::log(n) - 1;
}

// Herbie case: expq3
iRRAM::REAL irram_expq3(iRRAM::REAL a, iRRAM::REAL b, iRRAM::REAL eps) {
    iRRAM::REAL abe = eps*(iRRAM::exp((a+b)*eps)-1);
    iRRAM::REAL ae = iRRAM::exp(a*eps) - 1;
    iRRAM::REAL be = iRRAM::exp(b*eps) - 1;
    return abe/(ae*be);
}

// Herbie case: 3frac
iRRAM::REAL irram_3frac(iRRAM::REAL x) {
    return 1/(x+1) - 2/x + 1/(x-1);
}

// Herbie case: 2tan
iRRAM::REAL irram_2tan(iRRAM::REAL e, iRRAM::REAL x) {
    return iRRAM::tan(x+e) - iRRAM::tan(x);
}

// Herbie case: 2sqrt
iRRAM::REAL irram_2sqrt(iRRAM::REAL x) {
    return iRRAM::sqrt(x+1) - iRRAM::sqrt(x);
}

// Herbie case: 2sin
iRRAM::REAL irram_2sin(iRRAM::REAL e, iRRAM::REAL x) {
    return iRRAM::sin(x+e) - iRRAM::sin(x);
}

// Herbie case: 2isqrt
iRRAM::REAL irram_2isqrt(iRRAM::REAL x) {
    return 1/iRRAM::sqrt(x) - 1/iRRAM::sqrt(x+1);
}

// Herbie case: 2atan
iRRAM::REAL irram_2atan(iRRAM::REAL N) {
    return iRRAM::atan(N+1) - iRRAM::atan(N);
}


// Herbie case: midarc
iRRAM::REAL irram//此处干扰herbie_report中case名字的查找且无用，注释掉，下同_midarc(iRRAM::REAL z1image, iRRAM::REAL z1real, iRRAM::REAL z2image, iRRAM::REAL z2real)
{
    iRRAM::REAL r = z1real + z2real;
    iRRAM::REAL i = z1image + z2image;
    return r / iRRAM::sqrt((r * r) + (i * i));
}

// Herbie case: float_extension
iRRAM::REAL irram//_float_extension(int n) {
    iRRAM::REAL r = 0;
    for (int i=1;i<n;i++) r=r+iRRAM::REAL(1)/sqrt(iRRAM::REAL(i));
    return r;
}