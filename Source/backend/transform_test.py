import unittest

from rule import RULES
from transform import *


class TestTransform(unittest.TestCase):

    def test_apply_rule_node(self):

        str_expr = "a+b"
        root = build_parse_tree(str_expr).root
        tranfromed_node = apply_rule_node(root, RULES['CommutationPlus'])
        print(tranfromed_node.getText())
        self.assertTrue(tranfromed_node.getText() == 'b+a')

        str_expr = "sqrt(x+1)-sqrt(x)"
        root = build_parse_tree(str_expr).root
        tranfromed_node = apply_rule_node(root, RULES['Minus3'])
        print(tranfromed_node.getText())
        self.assertTrue(tranfromed_node.getText() == '1/(sqrt(x)+sqrt(x+1))')

        str_expr = "a+b+c"
        root = build_parse_tree(str_expr).root
        tranfromed_node = apply_rule_node(root, RULES['AssociationPlus'])
        print(tranfromed_node.getText())
        self.assertTrue(tranfromed_node.getText() == 'a+(b+c)')



