#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import *

import json
import re

none_variable_chars = " ~`!@#$%^&*()-+={[}]|\\:;\"\'<,>.?/"
# variables substitution in expr. e.g x+y --> a+b
def convert_expr(expr, origin_vars, new_vars):

    m = {}
    for i in range(len(origin_vars)):
        m[origin_vars[i]] = new_vars[i]

    new_expr = ''
    i = 0
    var_start = -1
    reading_ref = False
    while i < len(expr):
        if reading_ref and expr[i] in none_variable_chars:
            # end a variable reference
            var = expr[var_start:i]
            if var in m.keys():
                new_expr += m[var]
            else:
                # is a function reference
                new_expr += var
            new_expr += expr[i]
            reading_ref = False
        elif reading_ref and (expr[i].isalpha() or expr[i] == '_' or expr[i].isdigit()):
            # still reading a variable
            pass
        elif not reading_ref and (expr[i].isalpha() or expr[i] == '_'):
            # start a variable reference
            var_start = i
            reading_ref = True
        else:
            new_expr += expr[i]
        i += 1
    if reading_ref:
        var = expr[var_start:]
        new_expr += m[var]
        reading_ref = False
    # while i < len(expr):
    #     if not expr[i].isalpha():
    #         new_expr += expr[i]
    #         i += 1
    #     else:
    #         j = i
    #         while j < len(expr) and expr[j].isalpha():
    #             j += 1
    #         var = expr[i:j]
    #         if var in m:
    #             new_expr += m[var]
    #         else:
    #             new_expr += var
    #         i = j

    return new_expr


class PathData:

    """path文件封装类"""

    def __init__(self, path_file):

        with open(path_file) as f:
            data = json.load(f)

        self.data = data

        self.program_name = data['program_name']
        self.function_name = data['function_name']

        self.variables = data['variables']
        self.input_variables = data['input_variables']

        self.return_expr = data['return']

        # initialize paths
        # must initialize loops and procedures first as when initialize paths we need loops and procedures information
        self.paths = None
        self.init_paths()

    def init_paths(self):
        self.paths = list()
        for path in self.data['paths']:
            self.paths.append(Path(path))

    def get_program_name(self):
        return self.program_name
    def get_function_name(self):
        return self.function_name

    def get_variables(self):
        return list(self.variables.keys())

    def get_variable_type(self, var):
        return self.variables[var]

    def get_input_variables(self):
        return self.input_variables

    def get_paths(self):
        return self.paths

    def get_return_expr(self):
        return self.return_expr

    def clear_paths(self):
        self.paths = list()

    def add_path(self, path):
        self.paths.append(path)

    def to_json(self):

        data = dict()
        data['program_name'] = self.get_program_name()
        data['function_name'] = self.get_function_name()
        data['variables'] = self.variables
        data['input_variables'] = self.input_variables
        data['return'] = self.return_expr

        data['paths'] = [path.to_json() for path in self.paths]

        return data

    def output_json(self, path_file):
        data = self.to_json()
        with open(path_file, 'w') as f:
            json.dump(data, f, indent=4)


class Loop:

    """Loop封装类, 一个Loop指代一段循环的代码，包括了所涉及到的临时变量和它们的初始化，循环体等内容"""

    def __init__(self, loop_json):

        self.variables = loop_json['variables']  # 变量列表，字典结构{var:var_type;}，包含了循环涉及到的所有变量以及类型信息
        self.initialize = loop_json['initialize']  # 变量初始化列表，字典结构{var: init_expr;}
        self.loop_body = list()  # 循环体，为一个Path列表

        for lb in loop_json['loop_body']:
            self.loop_body.append(Path(lb))

    def __hash__(self):
        return hash(json.dumps(self.to_json()))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if not self.get_variables() == other.get_variables():
            return False
        if not self.get_initialize_list() == other.get_initialize_list():
            return False
        if not self.get_loop_body() == other.get_loop_body():
            return False
        return True

    def get_variables(self):
        return list(self.variables.keys())

    def get_variable_type(self, var):
        return self.variables[var]

    def get_initialize_expr(self, var):
        return self.initialize[var]

    def set_initialize_expr(self, var, expr):
        self.initialize[var] = expr

    def get_initialize_list(self):
        return self.initialize

    def get_loop_body(self):
        return self.loop_body

    @staticmethod
    def get_type():
        return 'loop'

    def to_json(self):
        data = dict()
        data["type"] = "loop"
        data["content"] = dict()
        data["content"]['variables'] = self.variables
        data["content"]['initialize'] = self.initialize
        data["content"]['loop_body'] = [p.to_json() for p in self.get_loop_body()]
        return data

    def to_cpp_code(self, implement_type, indent=0):

        code = indent*'\t'+'{\n'

        if implement_type == 'float':
            implement = FLOAT
        elif implement_type == 'real':
            implement = REAL

        # temporary variables declaration and initialize
        for var in self.get_variables():
            code += (indent+1)*'\t' + implement[self.get_variable_type(var)] + ' ' + var + ';\n'

        for var, update_expr in self.get_initialize_list().items():
            update_expr = compatible2cpp(update_expr)
            code += (indent+1)*'\t' + var + ' = ' + update_expr + ';\n'

        code += (indent+1)*'\t'+'while(true) {\n'

        # loop body
        for lb in self.get_loop_body():
            code += lb.to_cpp_code(implement_type, indent+2)

        code += (indent+1)*'\t'+'}\n'
        code += indent*'\t'+'}\n'
        return code

    def to_mixed_code(self, path_data, indent=0):

        code = indent*'\t' + '{\n'

        origin_vars = path_data.get_variables()
        real_vars = [x+'_real' for x in origin_vars]

        # temporary variables declaration and initialize
        for var in self.get_variables():
            code += (indent+1)*'\t' + REAL[self.get_variable_type(var)] + ' ' + var + ';\n'

        for var, update_expr in self.get_initialize_list().items():
            update_expr = compatible2cpp(update_expr)
            code += (indent+1)*'\t' + var + ' = ' + convert_expr(update_expr, origin_vars, real_vars) + ';\n'

        code += (indent+1)*'\t'+'while(true) {\n'

        # loop body
        for lb in self.get_loop_body():
            code += lb.to_mixed_code(path_data, indent+2)

        code += (indent+1)*'\t'+'}\n'

        code += indent*'\t'+'}\n'

        return code


class Procedure:

    """Procedure封装类, 一个Procedure指代一段顺序执行的代码，我们用所涉及到的所有变量的更新式来记录这段代码所代表的语义"""

    def __init__(self, procedure_data):

        self.procedure = procedure_data  # 一个 n x 2 大小的列表，对于列表中每一项procedure[i]，procedure[i][0]为更新的变量名，procedure[i][1]为更新式

    def __hash__(self):
        return hash(json.dumps(self.to_json()))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if not self.procedure == other.get_procedure():
            return False
        return True

    def get_update_expr(self, var):
        for i in range(len(self.procedure)):
            if self.procedure[i][0] == var:
                return str(self.procedure[i][1])
        return None

    def set_update_expr(self, var, update_expr):
        for i in range(len(self.procedure)):
            if self.procedure[i][0] == var:
                self.procedure[i][1] = update_expr
                return

    def get_procedure(self):
        return self.procedure

    @staticmethod
    def get_type():
        return 'procedure'

    def to_json(self):

        data = dict()
        data["type"] = "procedure"
        data["content"] = self.procedure

        return data

    # 将常数显示转换到REAL类型
    @staticmethod
    def to_real(matched):
        s = matched.group("number")
        return 'REAL(' + s + ')'

    def to_cpp_code(self, implement_type, indent=0):
        code = ''
        for i in range(len(self.procedure)):
            # 由于iRRAM未实现REAL类型与浮点类型的加减乘除的基本操作，因此需要对表达式中的常数进行类型的显示的转换
            # e.g.   1.0/x -> REAL(1.0)/x
            var = self.procedure[i][0]
            update_expr = self.get_update_expr(var)
            if implement_type == REALTYPE:
                update_expr = re.sub("(?P<number>\d+(?:\.\d+))", Procedure.to_real, update_expr);
                update_expr = compatible2cpp(update_expr)
                # update_expr = re.sub(r'pow', "power", update_expr)
                # update_expr = update_expr.replace('pow(', 'power(')
                # update_expr = update_expr.replace('fac(', 'fac_real(')
                update_expr = function_name_replace(update_expr, 'pow', 'power')
                # update_expr = function_name_replace(update_expr, 'fac', 'fac_real')
                update_expr = addcastreal2functioncall(update_expr)

            # gamma function rename as in c++ gamma is named tgamma
            if implement_type == FLOATTYPE:
                update_expr = compatible2cpp(update_expr)
                # update_expr = update_expr.replace('gamma(', 'tgamma(')
                # update_expr = re.sub('gamma\(', 'tgamma(', update_expr)
                update_expr = function_name_replace(update_expr, 'gamma', 'tgamma')

            code += indent*'\t'+var + ' = ' + str(update_expr) + ';\n'
        return code

    def to_mixed_code(self, path_data, indent=0):
        code = ''
        for i in range(len(self.procedure)):

            # 由于iRRAM未实现REAL类型与浮点类型的加减乘除的基本操作，因此需要对表达式中的常数进行类型的显示的转换
            # e.g.   1.0/x -> REAL(1.0)/x

            origin_vars = path_data.get_variables()
            real_vars = [x+'_real' for x in origin_vars]

            print(self.procedure)
            var = convert_expr(self.procedure[i][0], origin_vars, real_vars)
            update_expr = convert_expr(self.procedure[i][1], origin_vars, real_vars)

            update_expr = re.sub("(?P<number>\d+(?:\.\d+)?)", Procedure.to_real, update_expr);

            code += indent*'\t'+var + ' = ' + str(update_expr) + ';\n'
        return code


class Path:

    """单条路径的封装类，包含了约束、实现类型以及对应的路径信息"""

    def __init__(self, path_json):

        self.path_list = None  # Path 包含的具体信息，是一个Procedure与Loop的列表
        self.constrain = None  # Path 对应的约束
        self.implement = None  # Path 的实现方式
        self.loop_break = None  # 若Path为循环中的一条路径时，标志其是否为退出循环的路径

        self.constrain = path_json['constrain']

        if 'implement' in path_json.keys():
            self.implement = path_json['implement']
        else:
            self.implement = None

        if 'break' in path_json.keys():
            if path_json['break'] == 'true':
                self.loop_break = True
            else:
                self.loop_break = False

        # path_list为一个Procedure与Loop的列表，代表了一条路径
        self.path_list = []
        for p in path_json['path']:
            if p["type"] == "procedure":
                self.path_list.append(Procedure(p["content"]))
            elif p["type"] == "loop":
                self.path_list.append(Loop(p["content"]))

    def __hash__(self):
        return hash(json.dumps(self.to_json()))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        if not self.path_list == other.get_path_list():
            return False
        if not self.constrain == other.get_constrain():
            return False
        return True

    def set_implement(self, implement):
        self.implement = implement

    def get_implement(self):
        return self.implement

    def add_constrain(self, constrain):
        self.constrain = self.constrain + '&&' + '(' + constrain + ')'

    def get_constrain(self):
        return self.constrain

    def set_constrain(self, cons):
        self.constrain = cons

    def get_path_list(self):
        return self.path_list

    def set_path_list(self, path_list):
        self.path_list = path_list

    def to_json(self):
        data = dict()
        data['constrain'] = self.constrain
        data['path'] = list()
        for p in self.get_path_list():
            data['path'].append(p.to_json())

        if self.implement:
            data['implement'] = self.implement

        if hasattr(self, 'loop_break'):
            if self.loop_break:
                data['break'] = 'true'
            else:
                data['break'] = 'false'

        return data

    def to_cpp_code(self, implement_type, indent=0):
        code = ''
        code += indent*'\t' + 'if(' + self.constrain + ') {\n'
        for m in self.path_list:
            code += m.to_cpp_code(implement_type, indent+1)
        if hasattr(self, 'loop_break') and self.loop_break:
            code += (indent+1)*'\t'+'break;\n'
        code += indent*'\t'+'}\n'
        return code

    # 生成最终优化后代码，可能既包含浮点精度又包含任意精度
    def to_mixed_code(self, path_data, indent=0):

        code = ''

        code += indent*'\t' + 'if(' + self.constrain + ') {\n'

        # 原浮点精度变量转换成为任意精度变量
        origin_vars = path_data.get_variables()

        for v in origin_vars:
            if path_data.get_variable_type(v) != 'integer':
                code += (indent+1)*'\t' + 'iRRAM::' + REAL[path_data.get_variable_type(v)] + ' ' + v + '_real = iRRAM::' + REAL[path_data.get_variable_type(v)] + '(' + v + ');\n'
            else:
                code += (indent + 1) * '\t' + REAL[
                    path_data.get_variable_type(v)] + ' ' + v + '_real = ' + REAL[
                            path_data.get_variable_type(v)] + '(' + v + ');\n'

        # 对Procedure以及Loop进行代码生成，并注意替换其中变量
        for m in self.path_list:
            code += m.to_mixed_code(path_data, indent+1)

        # 计算过程结束后转换回去
        for v in origin_vars:
            if path_data.get_variable_type(v) == 'decimal':
                code += (indent+1)*'\t' + v + ' = ' + v + '_real.' + REAL['convert_func'][path_data.get_variable_type(v)] + ';\n'
            else:
                code += (indent + 1) * '\t' + v + ' = ' + v + '_real;\n'

        if hasattr(self, 'loop_break') and self.loop_break:
            code += (indent+1)*'\t'+'break;\n'

        code += indent*'\t'+'}\n'

        return code


# 将表达式中的**转换为pow函数, 这里通过4次正则表达式替换来完成的. 王协的正则表达式有问题, 经过了多次修复
# 这里'\(' '\)' 匹配到的是真实的括号, 而 () 的作用在于将匹配的结果成组, 成为一个替换变量. 如果不要这个替换变量, 而仅需要成组的时候也是用的小括号, 替换变量的数字以此类推即可.
#  例如 \(([^()]+)\) 的作用是匹配一对括号, 中间不能有右括号, 而匹配成对括号需要嵌套递归进行, 目前做了7层以内的括号匹配
#  其实感觉这里不用正则表达式, 而用程序来替换字符串更好. 语义上即\*\*前后匹配到括号或者变量则进行替换, 替换成pow(a,b)的形式.
def starstar2pow(expr):
    input = expr
    while True:
        output = re.sub(r'\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)\*\*\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)',
                  r'(pow(\1, \8))', input)
        output = re.sub(r'([_a-zA-Z][_a-zA-Z0-9]*)\*\*([0-9|.]+)', r'pow(\1, \2)', output)
        output = re.sub(
            r'([_a-zA-Z][_a-zA-Z0-9]*)\*\*\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)',
            r'pow(\1, \2)', output)
        output = re.sub(r'\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)\*\*([0-9|.]+)', r'(pow(\1, \8))', output)
        if output == input:
            break
        input = output
    #expr = re.sub(r'\(([^()]+)\)\*\*\(([^()]+)\)', r'(pow(\1, \2))', expr)
    #expr = re.sub(r'\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)\*\*\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)',
    #              r'(pow(\1, \8))', expr)
    # expr = re.sub(r'([_a-zA-Z][_a-zA-Z0-9]*)\*\*([0-9|.]+)', r'pow(\1, \2)', expr)
    # expr = re.sub(r'([_a-zA-Z][_a-zA-Z0-9]*)\*\*\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)', r'pow(\1, \2)', expr)
    # expr = re.sub(r'\((([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\(([^()]|\([^()]+\))+\))+\))+\))+\))+\))+)\)\*\*([0-9|.]+)', r'(pow(\1, \8))', expr)
    return output


def function_name_replace(expr, old_func, new_func):
    expr = re.sub(r'^'+old_func + '[\r\n\t ]*\(',
                  new_func + '(', expr)
    expr = re.sub(r'([~`!@#$%^&*()\-+={\[}\]|\\:;\"\'<,>.?/])'+old_func+'[\r\n\t ]*\(',
                  r'\1'+new_func + '(', expr)
    expr = re.sub(r'[ \r\n\t]'+old_func+'[\r\n\t ]*\(',
                  r''+new_func + '(', expr)
    return expr

# 将表达式中的整数除法转换为浮点数除法，1/2 -> 1.0/2
def intdiv2floatdiv(expr):
    return re.sub(r'([^0-9.][0-9]+)/([0-9]+)', r'\1/\2.0', expr)


# 将路径中的表达式转换为c++能够直接使用的计算式
def compatible2cpp(expr):
    expr = starstar2pow(expr)
    expr = intdiv2floatdiv(expr)
    return expr

# add cast to function call parameter, transform function call such as sqrt(x) to sqrt(REAL(x))
def addcastreal2functioncall(expr):
    func_set = {'power', 'exp', 'sin', 'cos', 'cosh', 'tan', 'cot', 'sec', 'csc',
                'acos', 'asin','atan', 'ln', 'log', 'sqrt', 'sum', 'abs', 'max', 'min'}
    # set function's namespace
    for func in func_set:
        new_func = 'iRRAM::'+func
        expr = re.sub(r'([~`!@#$%^&*()\-+={\[}\]|\\:;\"\'<,>.?/])' + func + '[\r\n\t ]*\(',
                      r'\1' + new_func + '((REAL)', expr)
        expr = re.sub(r'^' + func + '[\r\n\t ]*\(',
                      new_func + '((REAL)', expr)
        expr = re.sub(r'[ \r\n\t]' + func + '[\r\n\t ]*\(',
                      r'' + new_func + '((REAL)', expr)
    return expr
    # new_expr = ''
    # i = 0
    # var_start = -1
    # reading_ref = False
    # reading_func_call = False
    # function_call_layer = 0
    # while i < len(expr):
    #     if reading_ref and expr[i] in none_variable_chars:
    #         # end a variable reference
    #         var = expr[var_start:i]
    #         if expr[i] == '(' and var in func_set:
    #             # it is a function call in func_set
    #             new_expr += var
    #             reading_func_call = True
    #         else:
    #             # is a var reference
    #             if reading_func_call:
    #                 new_expr += 'REAL(' + var + ')'
    #             else:
    #                 new_expr += var
    #         new_expr += expr[i]
    #         reading_ref = False
    #     elif reading_ref and (expr[i].isalpha() or expr[i] == '_' or expr[i].isdigit()):
    #         # still reading a variable
    #         pass
    #     elif not reading_ref and (expr[i].isalpha() or expr[i] == '_'):
    #         # start a variable reference
    #         var_start = i
    #         reading_ref = True
    #     else:
    #         new_expr += expr[i]
    #     if reading_func_call:
    #         if expr[i] == '(':
    #             function_call_layer += 1
    #         elif expr[i] == ')':
    #             function_call_layer -= 1
    #             if function_call_layer == 0:
    #                 reading_func_call = False
    #     i += 1
    # if reading_ref:
    #     var = expr[var_start:]
    #     new_expr += var
    # return new_expr

import transform
if __name__ == '__main__':
    path_data = PathData('../case/iRRAM/float_extension/float_extension2.pth')
    paths = path_data.get_paths()
    for p in paths:
        for l in p.path_list:
            tmp = l.to_json()
            if tmp['type'] == 'loop':
                print(l.to_json())
                res = transform.generate_equal_loop(l)
                print(res.to_json())
