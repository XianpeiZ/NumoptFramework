
import random
import codecs
import copy
import antlr4
import itertools
import time
import json
import signal
import pickle
import sympy

from rule import TransformRule, SympyRule, LoopRule, RULES
from path import Path

from expr_parser.rulesParser import rulesParser #expr -> rules
from expr_parser.rulesLexer import rulesLexer   #expr -> rules

from sympy import *
from sympy.parsing.sympy_parser import *

from expr import *
from path import Procedure, Loop
from config import *


# 对路径进行随机代数变换，生成等价路径
def generate_equal_paths(path, num=10):

    # 等价路径集合
    equal_paths = set()
    equal_paths.add(path)

    # 规则集合
    rules = list()
    rules.append(RULES['LoopReduce'])
    rules.append(RULES['LoopReverse'])
    rules.append(RULES['TaylorCos'])
    rules.append(RULES['Taylor'])
    rules.append(RULES['Simplify'])
    rules.append(RULES['Horner'])
    rules.append(RULES['SinSinR'])
    rules.append(RULES['CosPlus'])
    rules.append(RULES['ExpReduction'])
    rules.append(RULES['FracPartial'])
    rules.append(RULES['TaylorExp'])

    # 记录待应用的规则与已经应用的规则
    to_transform = set()
    done_transform = set()
    for rule in rules:
        to_transform.add(rule.rule_name + '@' + json.dumps(path.to_json()))

    start_ticks = time.time()
    run_ticks = 0
    while len(equal_paths) < num and not run_ticks > 10:  # 设置30秒的超时时间

        # to_transform为空，说明已经全部应用完成
        if not to_transform:
            break

        run_ticks = time.time() - start_ticks

        # 随机选取待应用规则与表达式 TODO: 按概率选取
        rp = random.sample(to_transform, 1)[0]
        to_transform.remove(rp)
        done_transform.add(rp)

        print(rp)
        rp = rp.split("@", 1)

        rule = RULES[rp[0]]
        path = Path(json.loads(rp[1]))

        print("chosen rule:\t" + rule.rule_name)
        print("chosen path:")
        print(path.to_json())
        epath = apply_rule_path(path, rule)
        if epath:
            print("After transform:")
            print(epath.to_json())
        print("")

        if not epath:
            continue

        equal_paths.add(epath)

        # 将新产生的路径与规则组合加入到to_transform
        for rule in rules:
            rp = rule.rule_name + '@' + json.dumps(epath.to_json())
            if rp in done_transform:
                continue
            to_transform.add(rp)

    equal_paths.remove(path)

    return equal_paths


def apply_rule_path(path, rule):

    epath = copy.deepcopy(path)

    if isinstance(rule, LoopRule):

        # 循环规约规则
        if rule.rule_name == "LoopReduce":

            pl = epath.get_path_list()

            # 可运用规则的候选循环下标
            candidate_index = list()
            for i in range(len(pl) - 1):
                if isinstance(pl[i], Loop) and isinstance(pl[i+1], Loop) and reduce_loop(pl[i], pl[i+1]):
                    candidate_index.append(i)

            # 无法运用该条规则
            if not candidate_index:
                return None

            index = random.choice(candidate_index)
            p = reduce_loop(pl[index], pl[index+1])

            # 删除原有循环
            del pl[index+1]
            del pl[index]

            # 添加规约后的procedure
            pl.insert(index, p)

        # 循环逆序规则
        if rule.rule_name == "LoopReverse":

            pl = epath.get_path_list()

            # 可运用规则的候选循环下标
            candidate_index = list()
            for i in range(len(pl)):
                if isinstance(pl[i], Loop) and generate_equal_loop(pl[i]):
                    candidate_index.append(i)

            # 无法运用该条规则
            if not candidate_index:
                return None

            index = random.choice(candidate_index)
            l = generate_equal_loop(pl[index])

            # 删除原有循环
            del pl[index]

            # 添加规约后的procedure
            pl.insert(index, l)

    if isinstance(rule, SympyRule):

        # 首先收集所有可用规则的计算式，广度优先遍历路径上所有procedure的update_expr
        candidates = list()

        stk = list()
        stk.extend(epath.get_path_list())

        while stk:

            t = stk.pop()

            if isinstance(t, Procedure):
                candidates.extend(t.get_procedure())

            if isinstance(t, Loop):
                lb = t.get_loop_body()
                for p in lb:
                    stk.extend(p.get_path_list())

        chosen = random.choice(candidates)

        str_expr = chosen[1]

        transformations = standard_transformations + (convert_xor,)
        sympy_expr = parse_expr(str_expr, transformations=transformations)

        if rule.rule_name == 'Simplify':
            str_expr = str(simplify(sympy_expr))
        if rule.rule_name == 'Expand':
            str_expr = str(expand(sympy_expr))
        if rule.rule_name == 'Horner':
            try:
                str_expr = str(horner(sympy_expr))
            except sympy.polys.polyerrors.PolynomialError:
                return None  # 应用horner规则报错，返回None
        if rule.rule_name == 'Taylor':

            # sympy泰勒展开可能超时，设置一个10秒的时限
            # def handler(signum, frame):
            #     print("Taylor expand timeout!")
            #     raise Exception("timeout")
            #
            # signal.signal(signal.SIGALRM, handler)
            # signal.alarm(10)

            try:
                str_expr = str(series(sympy_expr, n=8))
            except Exception:
                return None  # 泰勒展开报错，返回None

            # signal.alarm(0)

            # 泰勒展开失败，返回原计算式
            if 'Derivative' in str_expr:
                str_expr = chosen[1]

            # sympy泰勒展开式会附带大O标记，这里要做一次字符串处理
            Opos = str_expr.rfind('O')
            if Opos > 0:
                str_expr = str_expr[:Opos-2]
        chosen[1] = str_expr

    if isinstance(rule, TransformRule):

        # 在路径中随机选取一个可运用规则的计算过程进行规则的运用

        # 首先收集所有可用规则的计算式，广度优先遍历路径上所有procedure的update_expr
        candidates = list()

        stk = list()
        stk.extend(epath.get_path_list())

        while stk:

            t = stk.pop()

            if isinstance(t, Procedure):
                candidates.extend(t.get_procedure())

            if isinstance(t, Loop):
                lb = t.get_loop_body()
                for p in lb:
                    stk.extend(p.get_path_list())

        # 筛选掉无法应用规则的表达式
        candidates = [x for x in candidates if apply_rule_expr(x[1], rule)]

        if candidates:
            chosen = random.choice(candidates)
            chosen[1] = apply_rule_expr(chosen[1], rule)
        else:
            return None

    return epath


# 根据表达式字符串构建表达式的解析树
def build_parse_tree(expr_str):
    data = codecs.decode(bytes(expr_str, 'utf-8'), 'ascii', 'strict')
    input = antlr4.InputStream(data)
    lexer = rulesLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = rulesParser(stream)
    return ParseTree(parser.expression())


# 在表达式的解析树节点上运用规则，返回应用规则后的解析树节点
def apply_rule_node(node, rule):

    if isinstance(rule, SympyRule):

        str_expr = node.getText()
        transformations = standard_transformations + (convert_xor, )
        try:
            sympy_expr = parse_expr(str_expr, transformations=transformations)
        except Exception:
            return node

        if rule.rule_name == 'Simplify':
            str_expr = str(simplify(sympy_expr))
        if rule.rule_name == 'Expand':
            str_expr = str(expand(sympy_expr))
        if rule.rule_name == 'Horner':
            str_expr = str(horner(sympy_expr))
        if rule.rule_name == 'Taylor':

            # sympy泰勒展开可能超时，设置一个10秒的时限
            def handler(signum, frame):
                print("Taylor expand timeout!")
                raise Exception("timeout")

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(5)

            try:
                str_expr = str(series(sympy_expr, n=8))
            except Exception:
                str_expr = node.getText()  # 泰勒展开报错，返回原表达式

            signal.alarm(0)

            # 泰勒展开失败，返回原计算式
            if 'Derivative' in str_expr:
                str_expr = node.getText()

            # sympy泰勒展开式会附带大O标记，这里要做一次字符串处理
            Opos = str_expr.rfind('O')
            if Opos > 0:
                str_expr = str_expr[:Opos-2]
                print(str_expr)

        parse_tree = build_parse_tree(str_expr)
        return parse_tree.root

    if isinstance(rule, TransformRule):

        candidate_nodes = find_matched_nodes(rule.origin_parse_tree.root, node)

        if not candidate_nodes:
            return node

        # 采取随机的策略，在所有匹配的节点中随机选取一个节点，做对应的转换操作
        chosen_node = random.choice(candidate_nodes)

        # 下面首先要找到转换规则中变量在表达式解析树中对应的节点，方法是对两个树结构平行的做DFS
        rule_stack = [rule.origin_parse_tree.root]
        expr_stack = [chosen_node]

        # 节点对应关系的字典
        rule2expr = dict()
        while rule_stack:
            rule_node = rule_stack.pop()
            expr_node = expr_stack.pop()
            if isinstance(rule_node, VariableNode):
                rule2expr[rule_node.getText()] = expr_node
                continue
            rule_stack.extend(rule_node.children)
            expr_stack.extend(expr_node.children)

        # 生成转换后的节点
        transformed_node = copy.deepcopy(rule.transformed_parse_tree.root)
        rule_stack = [transformed_node]
        while rule_stack:
            rule_node = rule_stack.pop()
            for i in range(len(rule_node.children)):
                if isinstance(rule_node.children[i], VariableNode) and rule_node.children[i].getText() in rule2expr:
                    rule_node.children[i] = rule2expr[rule_node.children[i].getText()]
                else:
                    rule_stack.append(rule_node.children[i])

        # 在转换后节点的最顶端做一次simplify操作，去掉一些多余的括号
        for i in range(len(transformed_node.children)):
            transformed_node.children[i] = apply_rule_node(transformed_node.children[i], RULES['Simplify'])


        # 在原计算式中做对应的替换
        if node == chosen_node:
            return transformed_node
        else:
            expr_stack = [node]
            while expr_stack:
                expr_node = expr_stack.pop()
                for i in range(len(expr_node.children)):
                    if expr_node.children[i] == chosen_node:
                        expr_node.children[i] = transformed_node
                    else:
                        expr_stack.append(expr_node.children[i])
        return node


# 在表达式上使用规则进行等价转换，返回一个新的表达式
def apply_rule_expr(expr_str, rule):

    if isinstance(rule, TransformRule):

        expr_parse_tree = build_parse_tree(expr_str)

        candidates = find_match(rule.origin_parse_tree, expr_parse_tree)
        if not candidates:
            return None

        candidate = random.choice(candidates)

        s_rule = [rule.origin_parse_tree.root]
        s_expr = [candidate]

        # 找到匹配规则中变量所对应的节点
        m = dict()
        while s_rule:
            n_rule = s_rule.pop()
            n_expr = s_expr.pop()
            if isinstance(n_rule, VariableNode):
                m[n_rule.getText()] = n_expr
                continue
            s_rule.extend(n_rule.children)
            s_expr.extend(n_expr.children)

        # 生成转换后的节点
        transformed_node = copy.deepcopy(rule.transformed_parse_tree.root)
        s_rule = [transformed_node]
        while s_rule:
            n_rule = s_rule.pop()
            for i in range(len(n_rule.children)):
                if isinstance(n_rule.children[i], VariableNode) and n_rule.children[i].getText() in m:
                    n_rule.children[i] = m[n_rule.children[i].getText()]
                else:
                    s_rule.append(n_rule.children[i])

        # 在原计算式中做对应的替换
        if expr_parse_tree.root == candidate:
            expr_parse_tree.root = transformed_node
        else:
            s_expr = [expr_parse_tree.root]
            while s_expr:
                n_expr = s_expr.pop()
                for i in range(len(n_expr.children)):
                    if n_expr.children[i] == candidate:
                        n_expr.children[i] = transformed_node
                    else:
                        s_expr.append(n_expr.children[i])

        return expr_parse_tree.getText()

    if isinstance(rule, SympyRule):
        return expr


def find_matched_nodes(rule_node, expr_node):
    '''

    在expr_node对应的树结构中匹配rule_node的形式，返回所有匹配中的节点，用 DFS + 递归 实现

    :param rule_node:
    :param expr_node:
    :return:

    '''

    matched_nodes = list()

    s = [expr_node]
    while s:
        n = s.pop()
        if match(rule_node, n):
            matched_nodes.append(n)
        s.extend(n.children)

    return matched_nodes


def find_match(origin_parse_tree, expr_parse_tree):
    '''
    :param origin_parse_tree: 等价转换规则原计算形式对应的解析树
    :param expr_parse_tree: 欲进行转换的表达式对应的解析树
    :return: 返回表达式解析树中的与原计算形式相同的子树节点
    '''

    matched_nodes = list()

    s = [expr_parse_tree.root]
    while s:
        n = s.pop()
        if match(origin_parse_tree.root, n):
            matched_nodes.append(n)
        s.extend(n.children)

    return matched_nodes


def match(rule_tree_node, expr_tree_node):
    '''
    判断两棵解析树是否match
    :param rule_tree_node:
    :param expr_tree_node:
    :return:
    '''
    vdict = dict()
    return match_recursive(rule_tree_node, expr_tree_node, vdict)


def match_recursive(rule_tree_node, expr_tree_node, vdict):

    if isinstance(rule_tree_node, OperatorNode):
        if not isinstance(expr_tree_node, OperatorNode):
            return False
        if not rule_tree_node.operator == expr_tree_node.operator:
            return False
        if not len(rule_tree_node.children) == len(expr_tree_node.children):
            return False
        return all(match_recursive(rule_tree_node.children[i], expr_tree_node.children[i], vdict) for i in range(len(rule_tree_node.children)))

    if isinstance(rule_tree_node, VariableNode):
        if rule_tree_node.getText() in vdict and vdict[rule_tree_node.getText()] != expr_tree_node.getText():
            return False
        vdict[rule_tree_node.getText()] = expr_tree_node.getText()
        return True

    if isinstance(rule_tree_node, FunctionNode):
        if not isinstance(expr_tree_node, FunctionNode):
            return False
        if not rule_tree_node.funcname == expr_tree_node.funcname:
            return False
        if not len(rule_tree_node.children) == len(expr_tree_node.children):
            return False
        return all(match_recursive(rule_tree_node.children[i], expr_tree_node.children[i], vdict) for i in range(len(rule_tree_node.children)))

    if isinstance(rule_tree_node, AtomNode):
        if not isinstance(expr_tree_node, AtomNode):
            return False
        if not len(rule_tree_node.children) == len(expr_tree_node.children):
            return False
        return all(match_recursive(rule_tree_node.children[i], expr_tree_node.children[i], vdict) for i in range(len(rule_tree_node.children)))

    if isinstance(rule_tree_node, SymbolNode):
        if not isinstance(expr_tree_node, SymbolNode):
            return False
        if not rule_tree_node.symbol == expr_tree_node.symbol:
            return False
        return True


# 使用给定的规则生成等价表达式集合
def generate_equivalent_expressions(expr, rules):

    expr_set = {expr}

    # 以 rule@expr 为关键字存储待的规则与表达式，每次随机选取一个进行等价变换，形成新的表达式后与规则列表作笛卡尔乘积然后加入进去

    rule_expr_set = set()
    for rule in rules:
        rule_expr_set.add(rule.rule_name+'@'+expr)

    i = 0
    while rule_expr_set and i <= 200:
        i += 1
        rule_expr = random.sample(rule_expr_set, 1)[0]
        rule_expr_set.remove(rule_expr)
        rule_name, expr = rule_expr.split('@')
        parse_tree = build_parse_tree(expr)
        transformed_expr = apply_rule_node(parse_tree.root, RULES[rule_name]).getText()
        if transformed_expr and transformed_expr not in expr_set:
            print('# Apply rule [ %s ] tranform [ %s ] -> [ %s ]' % (rule_name, expr, transformed_expr))
            for rule in rules:
                rule_expr_set.add(rule.rule_name+'@'+transformed_expr)
            expr_set.add(transformed_expr)

    print("------------------- Remaining Todo ---------------------")
    rule_expr_set= list(rule_expr_set)
    rule_expr_set.sort(key=len)
    for re in rule_expr_set:
        print(re)

    return expr_set







'''
if __name__ == '__main__':
    expr = 'a = s1/2'
    print(intdiv2floatdiv(expr))
# 生成等价过程模块
def generate_equal_procedure(path_data, procedure):

    equal_procedures = list()

    for v in path_data.get_all_variables():
        var(v)

    # Horner规则
    ep = copy.deepcopy(procedure)
    ep.set_id(ep.get_id() + '_HORNER')  # 设置新id

    for i in range(len(procedure.get_procedure())):
        variable = procedure.get_procedure()[i][0]
        update_expr = procedure.get_procedure()[i][1]
        expr = update_expr
        for v in path_data.get_all_variables():

            # 表达式字符串中指数标记为 '^' 会报错，需替换为'**'
            expr = str(expr)
            if '^' in expr:
                expr = expr.replace('^', '**')

            exec('expr = ' + expr)
            if isinstance(expr, Expression):
                exec('expr = str(expr.horner('+ v + '))')
        ep.set_update_expr(variable, expr)

    path_data.add_procedure(ep)         # 记得将新产生的procedure加入到path_data
    equal_procedures.append(ep)

    # 规则列表匹配规则
    ep = copy.deepcopy(procedure)

    origin_vars = path_data.get_input_variables()
    for i in range(len(procedure.get_procedure())):

        # 这个procedure中被更新的变量
        updated_var = procedure.get_procedure()[i][0]

        # 更新表达式
        update_expr = procedure.get_procedure()[i][1]

        # 规则列表中去匹配是否为等价表达式，若发现匹配到了便转换
        for j in range(len(rules)):
            rule = rules[j]
            if is_expr_equal(origin_vars, update_expr, rule['variables'], rule['origin_expr']):
                update_expr = convert_expr(rule['equal_expr'], rule['variables'], origin_vars)
                ep = copy.deepcopy(ep)
                ep.set_id(ep.get_id() + '_RULE_' + rule['name'])  # 设置新id
                ep.set_update_expr(updated_var, update_expr)
                equal_procedures.append(ep)
                # 记得将生成的等价procedure加入到path_data中
                path_data.add_procedure(ep)

    return equal_procedures
'''


# 生成等价循环模块
def generate_equal_loop(loop):

    # 累加累乘规则，针对类似于for(i=0;i<n;++i)这样的循环判定是否为累加或者累乘，然后逆序操作

    # 单循环变量
    if len(loop.get_variables()) == 1:
        # 循环体中仅两条路径
        if len(loop.get_loop_body()) == 2:
            p1 = loop.get_loop_body()[0]
            p2 = loop.get_loop_body()[1]

            # 两条路径约束互补
            if ('!('+p1.get_constrain()+')' == p2.get_constrain()) or (p1.get_constrain() == '!('+p2.get_constrain()+')'):
                # 循环体中临时变量更新方法为+1
                tv = loop.get_variables()[0]
                loop_body_path = p1 if len(p1.get_path_list()) == 1 else p2
                if len(loop_body_path.get_path_list()) == 1:
                    loop_body_procedure = loop_body_path.get_path_list()[0]
                    if loop_body_procedure.get_update_expr(tv) == tv+'+1' or loop_body_procedure.get_update_expr(tv) == '1+'+tv:

                        # 判断其他变量是否为累加、累乘的更新形式
                        can_transform = True

                        for i in range(len(loop_body_procedure.get_procedure())):
                            v = loop_body_procedure.get_procedure()[i][0]
                            e = loop_body_procedure.get_procedure()[i][1]
                            if v == tv:
                                continue
                            if not e.startswith(v):
                                can_transform = False
                                break
                            if e[len(v)] not in "+*":
                                can_transform = False
                                break
                            if v in e[len(v):]:
                                can_transform = False
                                break

                        if can_transform:
                            el = copy.deepcopy(loop)

                            vstart = el.get_initialize_expr(tv)
                            vend = loop_body_path.get_constrain().split('<')[1]

                            el.set_initialize_expr(tv, vend+'-1')

                            p1 = el.get_loop_body()[0]
                            p2 = el.get_loop_body()[1]
                            loop_body_path = p1 if len(p1.get_path_list()) == 1 else p2
                            loop_body_path.set_constrain(tv+'>='+vstart)
                            loop_body_procedure = loop_body_path.get_path_list()[0]
                            loop_body_procedure.set_update_expr(tv, tv+'-1')

                            loop_body_path = p1 if len(p1.get_path_list()) == 0 else p2
                            loop_body_path.set_constrain("!("+tv+">="+vstart+")")

                            return el

    return None


# 尝试将两个循环进行规约，成功则返回规约后的结果(一个Loop或者Procedure)，否则返回None
def reduce_loop(l1, l2):

    # 两个循环能够规约的必要条件是循环结构相同
    if l1.get_variables() != l2.get_variables():
        return None

    l1_loop_body = l1.get_loop_body()
    l2_loop_body = l2.get_loop_body()
    if len(l1_loop_body) != len(l2_loop_body):
        return None

    for i in range(len(l1_loop_body)):
        if l1_loop_body[i].get_constrain() != l2_loop_body[i].get_constrain():
            return None
        if l1_loop_body[i].get_constrain() != l2_loop_body[i].get_constrain():
            return None

    l1_path_list = list()
    l2_path_list = list()
    for i in range(len(l1_loop_body)):
        l1_path_list = l1_loop_body[i].get_path_list()
        if l1_path_list:
            break

    for i in range(len(l2_loop_body)):
        l2_path_list = l2_loop_body[i].get_path_list()
        if l2_path_list:
            break

    if len(l1_path_list) > 1 or len(l2_path_list) > 1:
        return None

    l1_procedure = l1_path_list[0].get_procedure()
    l2_procedure = l2_path_list[0].get_procedure()

    # 去掉循环临时变量
    l1_procedure = [x for x in l1_procedure if x[0] not in l1.get_variables()]
    l2_procedure = [x for x in l2_procedure if x[0] not in l2.get_variables()]

    variables = list(set([x[0] for x in l1_procedure + l2_procedure]))

    exec_stmts = list()
    exec_stmts.append(",".join(variables) + " = sympy.symbols('" + ' '.join(variables) + "')")
    exec_stmts += [x[0]+'='+x[1] for x in l1_procedure+l2_procedure]

    for x in exec_stmts:
        exec(x)

    exec_res = list()
    for v in variables:
        exec_res.append([v, str(eval(v))])

    # 去除循环过程中不变的变量
    exec_res = [x for x in exec_res if x[0] != x[1]]

    if len(exec_res) == 0:
        # 循环相当于啥都没做，返回一个空的Procedure
        p = Procedure([])
        return p
    elif len(exec_res) == 1 and exec_res[0][1] in variables:
        # 循环在对一个变量不停的赋值，循环n次的效果与一次赋值相同
        p = Procedure(exec_res)
        return p

    return None


# 生成等价路径
def generate_equal_path(path_data, path):

    equal_paths = list()

    # 循环规约规则，连续的两个相互为逆过程的循环可规约
    path_list = copy.deepcopy(path.get_path_list())
    i = 0
    while i+1 < len(path_list):
        if isinstance(path_list[i], Loop) and isinstance(path_list[i+1], Loop):
            reduce_res = reduce_loop(path_list[i], path_list[i+1])
            if reduce_res:
                del path_list[i:i+2]
                path_list.insert(i, reduce_res)
        i += 1

    ep = copy.deepcopy(path)
    ep.set_path_list(path_list)
    print ('reduce generate path')
    print (ep.to_json())
    equal_paths.append(ep)

    # gamma近似规则
    path_list = copy.deepcopy(path.get_path_list())
    if len(path_list) == 1 and isinstance(path_list[0], Procedure) and len(path_list[0].get_procedure()) == 1:
        update_var = path_list[0].get_procedure()[0][0]
        update_expr = path_list[0].get_procedure()[0][1]
        if update_expr.startswith('gamma(') and update_expr.endswith(')'):
            gamma_input = update_expr[6:-1]
            ep = copy.deepcopy(path)
            ep.add_constrain('abs(('+gamma_input+')+2)<1e-5')
            gamma_procedure = Procedure(path_list[0].get_id()+'_GAMMA_APPROX', [[update_var, generate_gamma_approx_expr(gamma_input)]])
            path_data.add_procedure(gamma_procedure)
            ep.set_path_list([gamma_procedure])
            ep.set_implement(REALTYPE)
            equal_paths.append(ep)

    # 生成等价的Loop以及Procedure后排列组合成新的path
    equal_list = list()
    for t in path.get_path_list():
        if isinstance(t, Procedure):
            equal_list.append(generate_equal_procedure(path_data, t))
        elif isinstance(t, Loop):
            equal_list.append(generate_equal_loop(path_data, t))

    print('product generate path')
    for t in [list(x) for x in itertools.product(*equal_list)]:
        ep = copy.deepcopy(path)
        ep.set_path_list(t)
        print (ep.to_json())
        equal_paths.append(ep)

    return equal_paths


'''
# 使用给定的规则生成等价表达式集合
def generate_equivalent_expressions(expr, rules):

    expr_set = {expr}
    already_choosen = set()
    for i in range(200):
        rule = random.choice(rules)  #随机选取转换规则
        expr = random.sample(expr_set, 1)[0]  #随机选已经生成的等价表达式
        if (rule.rule_name+'@'+expr) in already_choosen:
            # print('#[INFO] Already apply rule { %s } on { %s }' % (rule.rule_name, expr))
            continue
        transformed_expr = apply_rule_expr(expr, rule)
        if transformed_expr:
            print('#[RULE] { %s } tranform { %s } -> { %s }' % (rule.rule_name, expr, transformed_expr))
            already_choosen.add(rule.rule_name+'@'+expr)
            expr_set.add(transformed_expr)

    print(already_choosen)
    return expr_set

rules = load_rules()
rules_dict = dict()
for rule in rules:
    print('name:' + rule.rule_name)
    print('origin:' + rule.origin_parse_tree.getText())
    print('transformed:' + rule.transformed_parse_tree.getText())
    if rule.constrain_parse_tree:
        print('constrain:' + rule.constrain_parse_tree.getText())
    rules_dict[rule.rule_name] = rule

rules_dict['Simplify'] = SympyRule('Simplify')
rules_dict['Horner'] = SympyRule('Horner')

rules = list()

rules.append(rules_dict['LnDivide'])
rules.append(rules_dict['Simplify'])
rules.append(rules_dict['CommutationPlus'])

rules.append(rules_dict['TaylorLnPlusReverse'])
rules.append(rules_dict['TaylorLnMinusReverse'])

rules.append(rules_dict['Simplify'])

rules.append(rules_dict['FracPartial'])
rules.append(rules_dict['TaylorExp'])

cos2_expr = 'exp(x)/(exp(x)-1)'

expr_set = generate_equivalent_expressions(cos2_expr, rules)
print(len(expr_set))
for e in expr_set:
    print(e)


rule = SympyRule('Taylorexp')
rulesimple = SympyRule('Simplify')
expr = 'exp(x*a)'

expr = apply_rule_expr(expr, rule)
print(expr)
expr = (apply_rule_expr(expr, rulesimple))
print(expr)
'''
