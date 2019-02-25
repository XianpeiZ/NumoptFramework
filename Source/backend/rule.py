#!/usr/bin/env sage
# -*- coding: utf-8 -*-

import antlr4

import expr

from expr_parser.rulesParser import rulesParser
from expr_parser.rulesLexer import rulesLexer


class TransformRule:

    def __init__(self, rule_name, origin_parse_tree, transformed_parse_tree, cp_parse_tree=None, pp_parse_tree=None, weight=100):
        self.rule_name = rule_name
        self.origin_parse_tree = origin_parse_tree
        self.transformed_parse_tree = transformed_parse_tree
        self.constrain_parse_tree = cp_parse_tree
        self.pp_parse_tree = pp_parse_tree
        self.weight = weight


class SympyRule:

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.weight = 0


class LoopRule:

    def __init__(self, rule_name):
        self.rule_name = rule_name
        self.weight = 0

# 解析规则
def initialize_transform_rules():

    # 文件中的自定义转换规则
    rule_file = './rule.txt'

    input = antlr4.FileStream(rule_file)
    lexer = rulesLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = rulesParser(stream)
    tree = parser.rules()

    rules = set()
    for single_rule in tree.getChildren():                              # 这里的child下标和g4文件定义的规则相关
        rule_name = single_rule.getChild(0).getText()                    # 最前面的部分是规则名称
        origin_parse_tree = expr.ParseTree(single_rule.getChild(2))      # input pattern
        transformed_parse_tree = expr.ParseTree(single_rule.getChild(4)) # output pattern
        if single_rule.getChildCount() == 10:
            cp_parse_tree = None
            pp_parse_tree = None
            weight = int(single_rule.getChild(8).getText()[1:])
            
        elif single_rule.getChildCount() == 11 :
            if single_rule.getChild(6).getText() != '@':
                cp_parse_tree = expr.ParseTree(single_rule.getChild(6))
                pp_parse_tree = None
            else :
                cp_parse_tree = None
                pp_parse_tree = expr.ParseTree(single_rule.getChild(7))
            weight = int(single_rule.getChild(9).getText()[1:])

        else:
            cp_parse_tree = expr.ParseTree(single_rule.getChild(6))
            pp_parse_tree = expr.ParseTree(single_rule.getChild(8))
            weight = int(single_rule.getChild(10).getText()[1:])
            
        rules.add(TransformRule(rule_name, origin_parse_tree, transformed_parse_tree,  cp_parse_tree, pp_parse_tree, weight))
    return rules


def initialize_sympy_rules():
    return {SympyRule('Simplify'), SympyRule('Expand'), SympyRule('Horner'), SympyRule('Taylor')}


def initialize_loop_rules():
    return {LoopRule('LoopReduce'), LoopRule('LoopReverse')}

RULES = dict()
for r in initialize_transform_rules() | initialize_sympy_rules() | initialize_loop_rules():
    #r.weight = rule_weight[r.rule_name]
    RULES[r.rule_name] = r
RULES['Simplify'].weight = 1000 #rule.txt中没有simply这条规则，weight在此处加上
RULES['Expand'].weight = 100
RULES['Horner'].weight = 100
RULES['Taylor'].weight = 100
RULES['LoopReduce'].weight = 100
RULES['LoopReverse'].weight = 100

if __name__ == '__main__':

    rule_file = './ruletest.txt'
    input = antlr4.FileStream(rule_file)
    lexer = rulesLexer(input)
    stream = antlr4.CommonTokenStream(lexer)
    parser = rulesParser(stream)

    tree = parser.rules()

    single_rule = tree.getChild(0)                              # 这里的child下标和g4文件定义的规则相关
    rule_name = single_rule.getChild(0).getText()                    # 最前面的部分是规则名称
    origin_parse_tree = expr.ParseTree(single_rule.getChild(2))      # input pattern
    transformed_parse_tree = expr.ParseTree(single_rule.getChild(4)) # output pattern

    print(single_rule.getChildCount())
    print('rule_name, origin_parse_tree, transformed_parse_tree: ',end='')
    print(rule_name, origin_parse_tree, transformed_parse_tree)
    print(single_rule.getChild(8).getText()[1:])
    print(type(single_rule.getChild(5).getText()))



