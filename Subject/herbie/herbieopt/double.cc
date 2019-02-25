
// Herbie Case: 2log
double double_2log(double N) {
    return std::log(N+1) - std::log(N);
}

// Herbie Case: cos2
double double_cos2(double x) {
    return (1-std::cos(x))/(x*x);
}

// Herbie case: exp2
double double_exp2(double x) {
    return (std::exp(x) - 2 ) + std::exp(-x);
}

// Herbie case: expax
double double_expax(double a, double x) {
    return std::exp(a*x) - 1;
}

// Herbie case: expm1
double double_expm1(double x) {
    return std::exp(x) - 1;
}

// Herbie case: expq2
double double_expq2(double x) {
    return std::exp(x)/(std::exp(x)-1);
}

// Herbie case: invcot
double double_invcot(double x) {
    return 1/x-1/std::tan(x);
}

// Herbie case: quad2m
double double_quad2m(double a, double b, double c) {
    return ((-b/2)-std::sqrt(b*b/4-a*c))/a;
}

// Herbie case: quadp
double double_quadp(double a, double b, double c) {
    double d = -b + std::sqrt(b*b-4*a*c);
    return d/(2*a);
}

// Herbie case: quadm
double double_quadm(double a, double b, double c) {
    double d = -b - std::sqrt(b*b-4*a*c);
    return d/(2*a);
}

// Herbie case: sintan
double double_sintan(double x) {
    double a = x - std::sin(x);
    double b = x - std::tan(x);
    return a/b;
}

// Herbie case: sqrtexp
double double_sqrtexp(double x) {
    return std::sqrt((std::exp(2*x)-1)/(std::exp(x)-1));
}

// Herbie case: quad2p
double double_quad2p(double a, double b, double c) {
    return ((-b/2)+std::sqrt(b*b/4-a*c))/a;
}

// Herbie case: 2nthrt 
double double_2nthrt(double x, double n) {
    double a = std::pow(x+1, 1/n);
    double b = std::pow(x, 1/n);
    return a - b;
}

// Herbie case: 2frac
double double_2frac(double x) {
    double a = 1/(x+1);
    double b = 1/x;
    return a - b;
}

// Herbie case: 2cos
double double_2cos(double e, double x) {
    return std::cos(x+e) - std::cos(x);
}

// Herbie case: 2cbrt
double double_2cbrt(double x) {
    double n = double(1)/double(3);
    double a = std::pow(x+1, n);
    double b = std::pow(x, n);
    return a - b;
}

// Herbie case: tanhf
double double_tanhf(double x) {
    return (1-std::cos(x))/std::sin(x);
}

// Herbie case: qlog
double double_qlog(double x) {
    double a = std::log(1-x);
    double b = std::log(1+x);
    return a/b;
}

// Herbie case: logq
double double_logq(double eps) {
    double a = 1 - eps;
    double b = 1 + eps;
    return std::log(a/b);
    
}

// Herbie case: logs
double double_logs(double n) {
    return (n+1)*std::log(n+1) - n*std::log(n) - 1;
}

// Herbie case: expq3
double double_expq3(double a, double b, double eps) {
    double abe = eps*(std::exp((a+b)*eps)-1);
    double ae = std::exp(a*eps) - 1;
    double be = std::exp(b*eps) - 1;
    return abe/(ae*be);
}

// Herbie case: 3frac
double double_3frac(double x) {
    return 1/(x+1) - 2/x + 1/(x-1);
}

// Herbie case: 2tan
double double_2tan(double e, double x) {
    return std::tan(x+e) - std::tan(x);
}

// Herbie case: 2sqrt
double double_2sqrt(double x) {
    return std::sqrt(x+1) - std::sqrt(x);
}

// Herbie case: 2sin
double double_2sin(double e, double x) {
    return std::sin(x+e) - std::sin(x);
}

// Herbie case: 2isqrt
double double_2isqrt(double x) {
    return 1/std::sqrt(x) - 1/std::sqrt(x+1);
}

// Herbie case: 2atan
double double_2atan(double N) {
    return std::atan(N+1) - std::atan(N);
}

// Herbie case: midarc
double double_midarc(double z1image, double z1real, double z2image, double z2real)
{
    double r = z1real + z2real;
    double i = z1image + z2image;
    return r / std::sqrt((r * r) + (i * i));
}
