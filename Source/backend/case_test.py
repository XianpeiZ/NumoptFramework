import unittest

from rule import RULES
from transform import generate_equivalent_expressions


class TestTransform(unittest.TestCase):

    def setUp(self):
        return

    def test_midarc(self):

        expr = '((A1+B1*I)/sqrt(A1**2+B1**2)+(A2+B2*I)/sqrt(A2**2+B2**2))/abs((A1+B1*I)/sqrt(A1**2+B1**2)+(A2+B2*I)/sqrt(A2**2+B2**2))'

        #expr = '(e**(I*atan(B1/A1))+e**(I*atan(B2/A2)))/abs(e**(I*atan(B1/A1))+e**(I*atan(B2/A2)))'

        target = ['e**(I*(atan(B1/A1)+atan(B2/A2))/2)']

        rules = list()
        rules.append(RULES['PolarRepresentation'])
        rules.append(RULES['CommutationMultiply'])
        rules.append(RULES['Midarc'])

        rules.append(RULES['Simplify'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)

        for te in target:
            self.assertTrue(te in equivalent_expr)


    def test_logq(self):

        expr = 'log((1-eps)/(1+eps))'

        target = '-2*eps*(3*eps**4+5*eps**2+15)/15'

        rules = list()
        rules.append(RULES['Simplify'])
        #rules.append(RULES['TaylorLnPlusReverse'])
        #rules.append(RULES['TaylorLnMinusReverse'])
        #rules.append(RULES['LnDivide'])
        rules.append(RULES['Taylor'])
        rules.append(RULES['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)

        self.assertTrue(target in equivalent_expr)

    def test_expq3(self):

        expr = 'eps*(exp((a+b)*eps)-1)/((exp(a*eps)-1)*(exp(b*eps)-1))'
        target = ''

        rules = list()

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        self.assertTrue(target in equivalent_expr)

    def test_2cos(self):

        expr = 'cos(x+e)-cos(x)'

        target = ['cos(e)*cos(x)-sin(e)*sin(x)-cos(x)', '-2*sin(e/2+x)*sin(e/2)']

        rules = list()
        rules.append(RULES['SinSinR'])
        rules.append(RULES['CosPlus'])
        rules.append(RULES['Simplify'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_sqrtexp(self):

        expr = 'sqrt((exp(2*eps)-1)/(exp(eps)-1))'
        target = 'sqrt(exp(eps)+1)'

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['ExpReduction'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)

        self.assertTrue(target in equivalent_expr)

    def test_expq2(self):

        expr = 'exp(x)/(exp(x)-1)'
        target = '1+1/(x+pow(x,2)/2+pow(x,3)/6+pow(x,4)/24)'

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['FracPartial'])
        rules.append(RULES['TaylorExp'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        self.assertTrue(target in equivalent_expr)

    def test_2sin(self):

        expr = 'sin(x+e)-sin(x)'
        target = ['sin(x)*cos(e)+cos(x)*sin(e)-sin(x)',
                  '(-e^7/322560+e^5/1920-e^3/24+e)*cos(e/2+x)',
                  '-e*(e^6-168*e^4+13440*e^2-322560)*cos(e/2+x)/322560']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['SinPlus'])
        rules.append(RULES['CosSinR'])
        # rules.append(RULES['TaylorSin'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_2tan(self):

        expr = 'tan(x+e)-tan(x)'
        target = ['sin(e)/(cos(x)*(cos(e)*cos(x)-sin(e)*sin(x)))']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['TanPlus'])
        rules.append(RULES['CosPlus'])
        rules.append(RULES['CommDenominator2'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_cos2(self):

        expr = '(1-cos(x))/(x*x)'
        target = ['x**4/720-x**2/24+1/2']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['TaylorCos'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_sintan(self):

        expr = '(x-sin(x))/(x-tan(x))'
        target =['(-x**4+42*x**2-840)/(16*(17*x**4+42*x**2+105))']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['TaylorSin'])
        rules.append(RULES['TaylorTan'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_tanhf(self):

        expr = '(1-cos(x))/sin(x)'
        expr = '(-cos(x)+1)/sin(x)'
        target = ['sin(x)/(cos(x)+1)']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['NumeratorFrom1'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)


    def test_quadm(self):

        expr = '(-b+sqrt(b*b-4*a*c))/(2*a)'
        target = ['4*a*c/(-2*a*(b+sqrt(-4*a*c+b**2)))']


        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['NumeratorFrom1'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_invcot(self):

        expr = '1/x-1/tan(x)'
        target = ['x/3+x**3/45+2*x**5/945']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['Taylor'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

        for te in target:
            self.assertTrue(te in equivalent_expr)




    def test_logs(self):

        expr = '(n+1)*ln(n+1)-n*ln(n)-1'
        target = ['']



    def test_expax(self):

        expr = 'exp(x)-1'
        target = ['x*(x*(x*(x*(x/120+1/24)+1/6)+1/2)+1)']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['Taylor'])
        rules.append(RULES['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_exp2(self):

        expr = 'exp(x)-2+exp(-x)'
        target = ['x**2*(x**2*(x**2/360+1/12)+1)']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['Taylor'])
        rules.append(RULES['Horner'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_2sqrt(self):

        expr = 'sqrt(x+1)-sqrt(x)'
        target = ['1/(sqrt(x)+sqrt(x+1))']

        rules = list()
        rules.append(RULES['Simplify'])
        #rules.append(RULES['Taylor'])
        rules.append(RULES['NumeratorFrom3'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_2log(self):

        expr = 'log(n+1)-log(n))'
        target = ['']

        rules = list()
        rules.append(RULES['Simplify'])
        #rules.append(RULES['Taylor'])
        rules.append(RULES['Distribution3'])
        rules.append(RULES['TaylorLog'])
        rules.append(RULES['LogMinus'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_logs(self):

        expr = '(n+1)*log(n+1)-n*log(n)-1'
        target = ['']

        rules = list()
        rules.append(RULES['Simplify'])
        # rules.append(RULES['Taylor'])
        rules.append(RULES['Distribution2'])
        rules.append(RULES['CommutationPlus'])
        # rules.append(RULES['TaylorLog'])
        rules.append(RULES['LogMinus'])
        rules.append(RULES['LogDivideReverse'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_atan2(self):

        expr = 'atan(n+1)-atan(n)'
        target = ['']

        rules = list()
        rules.append(RULES['Simplify'])
        # rules.append(RULES['Taylor'])
        rules.append(RULES['AtanMinus'])
        # rules.append(RULES['TaylorLog'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)


    def test_gamma(self):

        expr = 'gamma((2-euler_gamma+x)/(euler_gamma-1-x)-1)'
        target = ['']

        rules = list()
        rules.append(RULES['Simplify'])
        # rules.append(RULES['Taylor'])
        rules.append(RULES['Gamma_1'])
        # rules.append(RULES['TaylorLog'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)


    def test_quadp(self):

        expr = '((-b)-sqrt(b*b-4*a*c))/(2*a)'
        target = ['']

        rules = list()
        rules.append(RULES['Simplify'])
        rules.append(RULES['NumeratorFrom2'])
        # rules.append(RULES['Taylor'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        for ee in equivalent_expr:
            print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_midarc(self):
        expr = '((z1real+z2real)/sqrt((((z1real+z2real)*(z1real+z2real))+((z1image+z2image)*(z1image+z2image)))))'
        target = ['cos(atan(z1image/z1real)/2+atan(z2image/z2real)/2)']
        rules = list()
        rules.append(RULES['Minus1'])
        rules.append(RULES['Minus2'])
        rules.append(RULES['Minus3'])
        rules.append(RULES['CommutationPlus'])
        rules.append(RULES['Midarc'])

        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        print('------------------------------------------------')
        for ee in equivalent_expr:
            if ee.startswith('cos'):
                print(ee)
        for te in target:
            self.assertTrue(te in equivalent_expr)

    def test_gamma(self):
        expr = "(8.0-4.0*euler_gamma+3.0*((2*euler_gamma-2*x-3.0)/(-euler_gamma+x+1.0))-2.0*euler_gamma*((2*euler_gamma-2*x-3.0)/(-euler_gamma+x+1.0)))/(4.0*((2*euler_gamma-2*x-3.0)/(-euler_gamma+x+1.0))+8.0)"
        rules = []
        rules.append(RULES['Simplify'])
        equivalent_expr = generate_equivalent_expressions(expr, rules)
        equivalent_expr = list(equivalent_expr)
        equivalent_expr.sort(key=len)
        print('------------------------------------------------')
        for ee in equivalent_expr:
            print(ee)


if __name__ == '__main__':
    unittest.main()
