import os
import re
import logging
import subprocess

from config import iRRAM_HOME, PROJECT_HOME

# report_dir = '/Users/whj/Desktop/HerbieCases'  # Herbie 跑benchmark得到的report文件夹
# report_dir = '/home/whj/experiment/2/HerbieCases'
report_dir = PROJECT_HOME + 'Binary/HerbieOutputs'
# case_parent_dir = os.path.join(PROJECT_HOME, '1/case/herbie')
src_dir = os.path.join(PROJECT_HOME, 'Source/backend')
herbieoptdir = '../../Subject/herbie/herbieopt/' #where herbie.cc and irram.cc in
HerbieOptimizeddir ='../../Binary/HerbieOptimized/herbie/'
obj_dir = '../../Binary/obj/herbie/'
result_dir = '../../Result/herbie/'

# 每个herbie实验用例生成输入的范围
case_input_range = {
    '2log': {'begin': '0.0', 'end': 'INF'},
    'exp2': {'begin': '-700', 'end': '700'},
    'expax': {'begin': '-26', 'end': '26'},
    'expm1': {'begin': '-700', 'end': '700'},
    '2nthrt': {'begin': '1.0', 'end': 'INF'},
    '2cbrt': {'begin': '0.0', 'end': 'INF'},
    '2sqrt': {'begin': '0.0', 'end': 'INF'},
    '2isqrt': {'begin': '0.0', 'end': 'INF'},
    'sqrtexp': {'begin': '-1.0', 'end': '1.0'},
    'qlog': {'begin': '-1.0', 'end': '1.0'},
    'logq': {'begin': '-1.0', 'end': '1.0'},
    'logs': {'begin': '0.0', 'end': 'INF'},
    'expq2': {'begin': '-700', 'end': '700'},
    'expq3': {'begin': '-1.0', 'end': '1.0'},
    'midarc': {'begin': '-1.0', 'end': '1.0'},
}

# 每个herbie实验用例输入的维度
case_input_dimension = {
    'expax': 2,
    '2cos': 2,
    '2sin': 2,
    '2tan': 2,
    '2nthrt': 2,
    'quad2m': 3,
    'quad2p': 3,
    'quadp': 3,
    'quadm': 3,
    'expq3': 3,
    'midarc': 4,
}


# 找到所有的compiled.c文件，也就是包含了Herbie优化后程序代码的文件，将其中优化后程序组成一个C++文件
def summary_compile_c():

    compiled_files = list()
    for root, dirs, files in os.walk(report_dir):
        for file in files:
            if file == "compiled.c":
                compiled_files.append(os.path.join(root, file))

    compiled_files.sort()

    herbie_file = open("herbie.cc", "w")

    for compiled_file in compiled_files:

        [report_num, case_name] = compiled_file.split('/')[-3:-1]
        funcname = '_'.join(["herbie", report_num, case_name.replace('-', '_')])
        with open(compiled_file) as file:
            lines = file.readlines()
            start = next(i for i in range(len(lines)) if lines[i].startswith("double f_od"))
            end = next(i for i in range(len(lines)) if lines[i].startswith("}") and i > start) + 1
            lines[start] = lines[start].replace('f_od', funcname)
            for i in range(start, end):
                herbie_file.write(lines[i])
        herbie_file.write('\n')

    herbie_file.close()


def save_herbie_cc(execname, herbie_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = herbie_code.split('\n')[0]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]


    header = '''#include <cmath>
#include <iostream>
#include <string>
#include <iomanip>
#include <cfenv>
#include "../../../../Source/backend/points.h"
#include "iRRAM/lib.h"

int iRRAM::MAXiterationnum = 30;
bool iRRAM::enableReiterate  = true;
bool iRRAM::alwaysenableReiterate  = true;

'''

    main = "int main() {\n"
    main += "\tstd::fesetround(FE_DOWNWARD);\n"
    main += "\tstd::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tstd::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    main += "\tdouble r_double = " + execname + "(" + ", ".join([x+"_double" for x in vars]) + ");\n"
    main += "\tstd::cout << double2binary(r_double) << std::endl;\n"
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(herbie_code)
        f.write("\n")
        f.write(main)


def save_irram_cc(irram_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = irram_code.split('\n')[1]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]

    funcname = function_definition.split('(')[0].split(' ')[1]

    header = '''#include <string>
#include <iostream>
#include "iRRAM.h"
#include <cfenv>
#include "../../../../Source/backend/points.h"
#include "iRRAM/lib.h"

int iRRAM::MAXiterationnum = 30;
bool iRRAM::enableReiterate  = true;
bool iRRAM::alwaysenableReiterate  = true;
'''

    main = "void compute() {\n"
    main += "\tstd::fesetround(FE_DOWNWARD);\n"
    main += "\tstd::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);\n"
    main += "\tiRRAM::cout << iRRAM::setRwidth(30);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tiRRAM::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    for var in vars:
        main += "\tiRRAM::REAL " + var + "_irram(" + var + "_double);\n"
    main += "\tiRRAM::REAL r_irram = " + funcname + "(" + ", ".join([x+"_irram" for x in vars]) + ");\n"
    main += "\tdouble r_double = r_irram.as_double();\n"
    main += '\tiRRAM::cout << double2binary(r_double) << "\\n";\n'
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(irram_code)
        f.write("\n")
        f.write(main)


def save_double_cc(double_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = double_code.split('\n')[1]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]

    funcname = function_definition.split('(')[0].split(' ')[1]

    header = '''#include <string>
#include <iostream>
#include <cfenv>
#include "../../../../Source/backend/points.h"
#include "iRRAM/lib.h"

int iRRAM::MAXiterationnum = 30;
bool iRRAM::enableReiterate  = true;
bool iRRAM::alwaysenableReiterate  = true;

'''

    main = "int main() {\n"
    main += "\tstd::cout << std::scientific << std::setprecision(std::numeric_limits<double>::digits10);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tstd::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    main += "\tdouble r = " + funcname + "(" + ", ".join([x+"_double" for x in vars]) + ");\n"
    main += '\tstd::cout << double2binary(r) << "\\n";\n'
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(double_code)
        f.write("\n")
        f.write(main)


def save_opt_cc(opt_code, file):

    pattern = re.compile(r'\((.*)\)')
    function_definition = opt_code.split('\n')[1]
    params = pattern.search(function_definition).group()
    vars = [x.strip().split(' ')[1] for x in params[1:-1].split(',')]

    funcname = function_definition.split('(')[0].split(' ')[1]

    header = '''#include <string>
#include <iostream>
#include <iomanip>
#include <limits>
#include "iRRAM.h" 
#include <cfenv>
#include "../../../../Source/backend/points.h"

using namespace std;
using namespace iRRAM;

'''

    main = "void compute() {\n"
    main += "\tstd::fesetround(FE_DOWNWARD);\n"
    main += "\tstd::string " + ",".join([x+"_str" for x in vars]) + ";\n"
    main += "\tiRRAM::cin >> " + " >> ".join([x+"_str" for x in vars]) + ";\n"
    for var in vars:
        main += "\tdouble " + var + "_double = binary2double(" + var + "_str);\n"
    main += "\tdouble r_double = " + funcname + "(" + ", ".join([x+"_double" for x in vars]) + ");\n"
    main += '\tiRRAM::cout << double2binary(r_double) << "\\n";\n'
    main += "}\n"

    with open(file, 'w') as f:
        f.write(header)
        f.write("\n")
        f.write(opt_code)
        f.write("\n\n")
        f.write(main)


def save_makefile(bins, file, casename):


     content = ""
     content += "iRRAM_HOME=../../" + iRRAM_HOME + "\n"
     content += "CPPFLAGS = -I$(iRRAM_HOME)/include\n"
     content += "CXX = clang++ -std=c++11\n"
     content += "CXXCPP = clang++ -E -std=c++11\n"
     content += "CXXFLAGS = -g -O2\n"
     content += "LDFLAGS = -Xlinker -rpath -Xlinker $(iRRAM_HOME)/lib\n"
     content += "LDLIBS =  -L$(iRRAM_HOME)/lib -liRRAM -lmpfr -lgmp -lm -lpthread\n"
     content += "all: " + " ".join(bins) + " rules"+"\n"
     for bin in bins:
         content += bin + ": " + bin + ".cc points.o\n"
     content += "points.o: ../../../../Source/backend/points.cc ../../../../Source/backend/points.h\n"
     content += "\t$(CXX) -c -o $@ $< $(CXXFLAGS)\n"
     content += "rules: \n"
     for bin in bins:
         content += "\tmv "+ bin+" ../../../obj/herbie/"+casename+"/"+bin+";\n"
     content += "\tmv points.o ../../../obj/herbie/"+casename+"/points.o;\n"
     content += "clean:\n"
     content += "\trm -rf " + " ".join(bins) + " points.o *.dSYM\n"
     content += "deepclean: clean\n"
     content += "\trm -rf *.cc *.txt result.csv Makefile *_o.pth.json\n"





     with open(file, 'w') as f:
         f.write(content)


# 生成Herbie优化后代码，其实现从当前目录的herbie.cc中获取
def generate_herbie_cc(casename):

    # 新建case文件夹
    case_dir = os.path.join(HerbieOptimizeddir, casename)
    os.makedirs(case_dir, exist_ok=True)

    # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    herbie_bin = list()

    # Herbie实现文件，可调用summary_compile_c函数生成
    herbie_code_file = os.path.join(herbieoptdir, "herbie.cc")

    # 获取herbie函数名称以及相应代码
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

        pattern = re.compile(r'^double .*?' + casename + r'(?:.|\n)*?\}', re.M)
        herbie_code = pattern.findall(content)

    # 生成herbie的C++实现
    for hb in herbie_bin:
        hb_cc = os.path.join(case_dir, hb + '.cc')
        content = [x for x in herbie_code if hb in x][0]
        save_herbie_cc(hb, content, hb_cc)


# 生成irram任意精度代码，其实现从当前目录的irram.cc中获取
def generate_irram_cc(casename):

    case_dir = os.path.join(HerbieOptimizeddir, casename) # HerbieOptimized/casename

    # irram实现文件，直接按照数学公式纯手工编写
    irram_code_file = os.path.join(herbieoptdir, "irram.cc")

    # 获取irram实现文件中的代码实现
    with open(irram_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^.*?' + casename + r'(?:.|\n)*?\}', re.M)
        irram_code = pattern.findall(content)

    # 生成irram的C++实现
    irram_cc = os.path.join(case_dir, 'irram.cc')
    content = irram_code[0]
    save_irram_cc(content, irram_cc)


# 生成double精度代码，其实现从当前目录的double.cc中获取
def generate_double_cc(casename):

    case_dir = os.path.join(HerbieOptimizeddir, casename)

    # irram实现文件，直接按照数学公式纯手工编写
    double_code_file = os.path.join(herbieoptdir, "double.cc")

    # 获取irram实现文件中的代码实现
    with open(double_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^.*?' + casename + r'(?:.|\n)*?\}', re.M)
        irram_code = pattern.findall(content)

    # 生成irram的C++实现
    irram_cc = os.path.join(case_dir, 'double.cc')
    content = irram_code[0]
    save_double_cc(content, irram_cc)


# 生成opt代码，其实现从当前目录的opt.cc中获取
def generate_opt_cc(casename):

    os.chdir(src_dir)
    case_dir = os.path.join(HerbieOptimizeddir, casename)

    # 优化后实现文件，暂时通过手工编写，后续需要自动化实现
    opt_code_file = os.path.join(src_dir, "opt.cc")

    # 获取优化后文件中代码实现
    with open(opt_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^.*?' + casename + r'(?:.|\n)*?\n\}', re.M)
        opt_code = pattern.findall(content)

    # 生成优化后文件的C++实现
    opt_cc = os.path.join(case_dir, 'opt.cc')
    content = opt_code[0]
    save_opt_cc(content, opt_cc)


# 生成Makefile
def generate_makefile(casename):

    case_dir = os.path.join(HerbieOptimizeddir, casename)

    # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    herbie_bin = list()

    # Herbie实现文件，可调用summary_compile_c函数生成
    herbie_code_file = os.path.join(herbieoptdir, "herbie.cc")

    # 获取herbie可执行文件名称
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

    # 生成Makefile
    make_file = os.path.join(case_dir, 'Makefile')
    irram_bin = "irram"
    opt_bin = "opt"
    double_bin = "double"
    save_makefile(herbie_bin + [irram_bin] + [opt_bin] +[double_bin], make_file, casename)# casename for path in makefile


# 生成随机输入，也就是随机采点，默认256个，结果存储在case目录的points.txt中，以二进制表示
def generate_points(casename):

    print("[INFO] Preparing random floating points..")

    case_dir = os.path.join('../../Binary/obj/herbie/', casename)

    points_file = os.path.join(case_dir, 'points.txt')

    if casename in case_input_dimension:
        params_num = case_input_dimension[casename]
    else:
        params_num = 1

    generate_points = './points --dimension=' + str(params_num) + " --file=" + points_file
    if casename in case_input_range:
        generate_points += ' --range=[' + case_input_range[casename]['begin'] + ',' + case_input_range[casename]['end'] + ']'

    print("[INFO] Sample Point Command: " + generate_points)

    os.chdir(src_dir)
    os.system('make 2>/dev/null')
    os.system(generate_points)


# 将之前生成的herbie，irram，opt文件编译成可执行文件
def compile_executables(casename):

    print("[INFO] Compiling herbie executables for " + casename)

    case_dir = os.path.join(HerbieOptimizeddir, casename)
    os.chdir(case_dir)
    os.system('make >/dev/null')
    os.chdir("../../../../Source/backend")


# 每个herbie用例的准备工作
def prepare(casename):

    print("[INFO] Preparing for case :" + casename)
    os.makedirs('../../Binary/HerbieOptimized/herbie/'+casename, exist_ok=True)

    # 生成Herbie优化后代码，其实现从当前目录的herbie.cc中获取
    generate_herbie_cc(casename)

    # 生成irram任意精度代码，其实现从当前目录的irram.cc中获取
    generate_irram_cc(casename)

    # 生成double精度代码，其实现从当前目录double.cc中获取
    generate_double_cc(casename)

    # 生成opt代码，其实现从当前目录的opt.cc中获取
    #generate_opt_cc(casename)
    os.system('cp ../../Binary/OptimizedCode/herbie/'+casename+'/opt.cc ../../Binary/HerbieOptimized/herbie/'+casename+'/opt.cc')

    # 生成Makefile
    generate_makefile(casename)

    # 将之前生成的herbie，irram，opt文件编译成可执行文件
    compile_executables(casename)


# 跑irrram,opt,herbie程序，输入为随机采点得到的points.txt文件，输出结果以二进制形式写入到 XXX_result.txt
def run(casename, mode='all'):

    if mode == 'all':
        run(casename, mode='sa')
        run(casename, mode='rd')
        return

    print("[INFO] Running case " + casename + " ...")
    case_dir = os.path.join(obj_dir, casename)#obj_dir

    rst_case_dir = os.path.join(result_dir,casename)
    os.makedirs(rst_case_dir,exist_ok=True)#create result_dir for cases
    print('make dir ' + rst_case_dir)

    herbie_bin = list()  # Herbie可执行文件名称，实验中每个case会选取多个Herbie优化结果进行实验，因此这里是个list
    irram_bin = "irram"  # iRRAM可执行文件名称
    opt_bin = "opt"  # 优化有程序的可执行文件名称
    double_bin = "double"

    herbie_code_file = herbieoptdir+"herbie.cc"

    # 获取herbie可执行文件
    with open(herbie_code_file) as f:
        content = f.read()
        pattern = re.compile(r'^double (.*?' + casename + r'.*?)\(', re.M)
        herbie_bin = pattern.findall(content)

    points_file = "points.txt." + mode

    # 删除旧文件
    os.chdir(rst_case_dir)
    for hb in herbie_bin:
        try:
            os.remove(hb+"_result.txt."+ mode)
        except OSError:
            pass

    try:
        os.remove(irram_bin+"_result.txt." + mode)
    except OSError:
        pass

    try:
        os.remove(opt_bin+"_result.txt." + mode)
    except OSError:
        pass

    try:
        os.remove(double_bin+"_result.txt." + mode)
    except OSError:
        pass

    os.chdir('../../../Source/backend/')
    os.chdir(case_dir)   #obj_dir
    with open(points_file) as f:
        points = f.readlines()

    case_result_dir = '../../../../Result/herbie/'+casename + '/'
    print(os.getcwd())
    for point in points:
        print(point, file=open("point.txt", "w"))
        # print("[INFO] Executing herbie program with input :" + point.replace("\n", ""))
        for hb in herbie_bin:
            os.system("./" + hb + " < point.txt >> " + case_result_dir +hb + "_result.txt." + mode)

    for point in points:
        print(point, file=open("point.txt", "w"))
        # print("[INFO] Executing optimized program with input :" + point.replace("\n", ""))
        os.system("./" + opt_bin + " < point.txt >> " + case_result_dir + opt_bin + "_result.txt." + mode)

    for point in points:
        print(point, file=open("point.txt", "w"))
        # print("[INFO] Executing irram program with input :" + point.replace("\n", ""))
        os.system("./" + irram_bin + " < point.txt >> " + case_result_dir + irram_bin + "_result.txt." + mode)

    for point in points:
        print(point, file=open("point.txt", "w"))
        os.system("./" + double_bin + " < point.txt >> " + case_result_dir + double_bin + "_result.txt." + mode)

    #copy points.txt.mode to result_dir for analysis
    os.system("cp points.txt."+mode+" ../../../../Result/herbie/"+casename+"/points.txt."+mode)
    os.chdir("../../../../Source/backend")


# 分析跑程序得到的result.txt文件，得到每个用例的两种误差，包括herbie所定义的误差以及相对误差，结果输出到result.csv，主要是对analysis的调用
def analysis(case, mode='all'):

    if mode == 'all':
        analysis(case, mode='rd')
        analysis(case, mode='sa')
        return
    print(case)
    case_dir = os.path.join('../../Result/herbie/', case)#result下case的文件夹


    result_files = [f for f in os.listdir(case_dir) if os.path.isfile(os.path.join(case_dir, f)) and "result.txt" in f]

    irram_result_file = None
    herbie_reuslt_files = list()
    opt_result_file = None
    double_result_file = None
    for f in result_files:
        if f.startswith("irram") and f.endswith(mode):
            irram_result_file = f
        if f.startswith("herbie") and f.endswith(mode):
            herbie_reuslt_files.append(f)
        if f.startswith("opt") and f.endswith(mode):
            opt_result_file = f
        if f.startswith("double") and f.endswith(mode):
            double_result_file = f

    if not irram_result_file:
        logging.error("iRRAM result file not found!")
        return

    if len(herbie_reuslt_files)!=10:
        logging.error("Number of Herbie result file is not 10!")
        return

    if not opt_result_file:
        logging.error("Opt result file not found!")
        return

    if not double_result_file:
        logging.error("double result file not found!")
        return

    os.chdir(case_dir)
    analysis_command = "../../../Source/backend/analysis --irram=" + irram_result_file + " --herbie=" + ",".join(herbie_reuslt_files) + " --opt=" + opt_result_file + "  --double=" + double_result_file + " --mode=" + mode + " > error." + mode
    print(analysis_command)
    os.system(analysis_command)
    print("")
    os.chdir('../../../Source/backend')


if __name__ == "__main__":
  
    cases = ['sintan', 'sqrtexp', 'cos2', '2log', '2frac', '2cos', '2cbrt', 'tanhf', 'qlog', 'logs', 'logq', \
             'invcot', 'expq3', 'expq2', 'expm1', 'exp2', '3frac', '2tan', '2sin', '2atan', '2nthrt', \
             'quadp', 'quadm', 'quad2p', 'quad2m', '2sqrt', '2isqrt', 'expax']

    #cases = ['sintan']
    print(cases)

    for case in cases:
        #try:
            prepare(case)
            run(case, mode="rd")
            analysis(case, mode="rd")
        #except:
            #pass







