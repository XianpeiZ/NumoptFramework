#!/usr/bin/python
# -*- coding:utf-8 -*-

# Configuration file

PROJECT_HOME = '../../'
#iRRAM_HOME = '/home/whj/iRRAM'
iRRAM_HOME = PROJECT_HOME + 'Binary/iRRAM'

# 优化后程序两种不同的实现类型：浮点数实现、高精度实现
FLOATTYPE = 'float'
REALTYPE = 'real'


# 浮点精度与高精度程序的容许的比特误差，容许误差范围内认为是稳定的
TOLERANCE = 4

# 不同实现对应的不同类型的名称以及需要引入的头文件等
FLOAT = dict()
REAL = dict()

FLOAT['decimal'] = 'double'
FLOAT['integer'] = 'int'
FLOAT['cin'] = 'std::cin'
FLOAT['cout'] = 'std::cout'
FLOAT['header'] = '''
#include "points.h"
#include "self_math.h"
#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>
#include <string>
#include <cfenv>

#define euler_gamma 0.577215664901532860606512090082402431042159335
#define pi 3.1415926535897932384626433832795

using namespace std;
'''

REAL['decimal'] = 'REAL'
REAL['integer'] = 'int'
REAL['cin'] = 'iRRAM::cin'
REAL['cout'] = 'iRRAM::cout'
REAL['header'] = '''
#include "points.h"
#include "self_math.h"
#include "iRRAM.h"
#include "gamma.h"
#include <string>
#include <cfenv>

#undef euler_gamma
#define euler_gamma REAL("0.57721566490153286060651209008240243104215933593992")
#define pi REAL(3.1415926535897932384626433832795)

using namespace iRRAM;

'''

REAL['convert_func'] = {'decimal': 'as_double(53)', 'integer': ''}

# 二进制表示转换数值表示的函数名
TRANSFUNC = dict()
TRANSFUNC['decimal'] = 'binary2double'
TRANSFUNC['integer'] = 'binary2int'

FLOATCPP = 'float.cpp'
REALCPP = 'real.cpp'

LOGFILE = open('LOG', 'a')

