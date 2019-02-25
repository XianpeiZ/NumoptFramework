#!/usr/bin/env sage
# -*- coding: utf-8 -*-

from __future__ import print_function

# from transform import convert_expr
from path import *
from config import *

import os

# merge paths in pth file to a C program
def merge_path(path_file):

    path_data = PathData(path_file)

    code_header = \
'''
#include <iostream>
#include <iomanip>
#include <limits>
#include <cmath>
#include <cfenv>

#include "iRRAM.h"
#include "../../../../Source/backend/points.h"
#include "../../../../Source/backend/self_math.h"
#include "../../../../Source/backend/gamma.h"
#include "iRRAM/lib.h"

int iRRAM::MAXiterationnum = 30;
bool iRRAM::enableReiterate  = true;
bool iRRAM::alwaysenableReiterate  = true;

using namespace std;
using namespace iRRAM;

'''

    code_body = ''

    # 函数声明
    param_list = ', '.join([FLOAT[path_data.get_variable_type(x)] + ' ' + x for x in path_data.get_input_variables()])
    code_body += FLOAT['decimal'] + ' ' + path_data.get_function_name() + '(' + param_list + ')\n'
    code_body += '{\n'

    # 变量声明，每个变量分别声明其浮点精度类型变量以及任意精度类型变量
    for v in path_data.get_variables():
        if v not in path_data.get_input_variables():
            code_body += '\t' + FLOAT[path_data.get_variable_type(v)] + ' ' + v + ';\n'
            code_body += '\t' + REAL[path_data.get_variable_type(v)] + ' ' + v + '_real;\n'
        else:
            code_body += '\t' + REAL[path_data.get_variable_type(v)] + ' ' + v + '_real(' + v + ');\n'

    code_body += '\n'

    # 优化后的浮点精度实现
    for p in path_data.get_paths():
        if p.get_implement() == FLOATTYPE:
            code_body += '\t' + 'if(' + p.constrain + ') {\n'
            for m in p.path_list:
                code_body += m.to_cpp_code(FLOATTYPE, 2)
            code_body += '\t\treturn ' + path_data.get_return_expr() + ';\n'
            code_body += '\t}\n'
            code_body += '\n'

    # 原任意精度实现
    float_vars = path_data.get_variables()
    real_vars = [fv + '_real' for fv in float_vars]
    for p in path_data.get_paths():
        if p.get_implement() == REALTYPE:
            code_body += '\t' + 'if(' + p.constrain + ') {\n'
            for m in p.path_list:
                code_body += convert_expr(m.to_cpp_code(REALTYPE, 2), float_vars, real_vars)
            code_body += '\t\treturn ' + path_data.get_return_expr() + '_real.as_double();\n'
            code_body += '\t}\n'
            code_body += '\n'

    # return语句
    code_body += '\treturn ' + path_data.get_return_expr() + ';\n'
    code_body += '}\n\n'

    # main函数
    code_body += "void compute() {\n"
    code_body += "\tstd::fesetround(FE_DOWNWARD);\n"
    code_body += "\tstd::string " + ",".join([x + "_str" for x in path_data.get_input_variables()]) + ";\n"
    code_body += "\tiRRAM::cin >> " + " >> ".join([x + "_str" for x in path_data.get_input_variables()]) + ";\n"
    for var in path_data.get_input_variables():
        if path_data.get_variable_type(var) == 'decimal':
            code_body += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
        else:
            code_body += "\tdouble " + var + "_double = binary2int(" + var + "_str);\n"
    code_body += "\tdouble r_double = " + path_data.get_function_name() + "(" + ", ".join([x + "_double" for x in path_data.get_input_variables()]) + ");\n"
    code_body += '\tiRRAM::cout << double2binary(r_double) << "\\n";\n'
    code_body += "}\n"

    # output to file
    if path_file.rfind('/') != -1:
        output_directory = path_file[:path_file.rfind('/')+1]

    output_file = open(os.path.join(output_directory, 'opt.cc'), 'w')

    print(code_header, file=output_file)
    print(code_body, file=output_file)




