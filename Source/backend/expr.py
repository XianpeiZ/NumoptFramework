import expr_parser.rulesParser as parser


PRIORITY = {"+":0, "-":0, "*":1, "/":1, "^":2, "**":2}

# 王协自己的树的树节点
class ParseTreeNode(object):

    def __init__(self):
        self.children = []
        return

    def getText(self):
        return ''

# 继承自ParseTreeNode, 操作符节点
class OperatorNode(ParseTreeNode):

    def __init__(self, operator, children):
        self.operator = operator
        self.children = children

    def getText(self):

        if len(self.children) < 2:
            return
        else:
            res = ''
            left_child = self.children[0]
            if isinstance(left_child, OperatorNode) and PRIORITY[self.operator] > PRIORITY[left_child.operator]:
                res += '(' + left_child.getText() + ')'
            else:
                res += left_child.getText()
            res += self.operator

            right_child = self.children[1]
            if isinstance(right_child, OperatorNode) and PRIORITY[self.operator] >= PRIORITY[right_child.operator]:
                res += '(' + right_child.getText() + ')'
            else:
                res += right_child.getText()
        return res

# 继承自ParseTreeNode, 变量节点
class VariableNode(ParseTreeNode):

    def __init__(self, variable):
        self.variable = variable
        self.children = []

    def getText(self):
        return self.variable

# 继承自ParseTreeNode, 函数节点
class FunctionNode(ParseTreeNode):

    def __init__(self, funcname, children):
        self.funcname = funcname
        self.children = children

    def getText(self):
        return self.funcname + '(' + ','.join([x.getText() for x in self.children]) + ')'

# 继承自ParseTreeNode, 对应antlr里的Atom节点
class AtomNode(ParseTreeNode):

    def __init__(self, children):
        self.children = children

    def getText(self):

        if isinstance(self.children[1], OperatorNode) and PRIORITY[self.children[0].getText()] >= PRIORITY[self.children[1].operator]:
            return self.children[0].getText() + '(' + self.children[1].getText() + ')'
        else:
            return self.children[0].getText() + self.children[1].getText()

# 继承自ParseTreeNode, 符号节点
class SymbolNode(ParseTreeNode):

    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

    def getText(self):
        return self.symbol


class ParseTree:

    def __init__(self, tree):

        self.root = self.build(tree)

        '''
        Create a self defined parser tree by an ANTLR parser tree
        :param tree: ANTLR parser tree
        '''

    def build(self, node):

        if isinstance(node, parser.rulesParser.VariableContext):
            return VariableNode(node.getChild(0).getText())

        if isinstance(node, parser.rulesParser.FuncContext):
            funcname = node.getChild(0).getText()
            children = list()
            for i in range(2, node.getChildCount(), 2):
                children.append(self.build(node.getChild(i)))
            return FunctionNode(funcname, children)

        if isinstance(node, parser.rulesParser.ExpressionContext) or isinstance(node, parser.rulesParser.MultiplyingExpressionContext) or isinstance(node, parser.rulesParser.EquationContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 3:
                operator = node.getChild(1).getText()
                children = list()
                children.append(self.build(node.getChild(0)))
                children.append(self.build(node.getChild(2)))
                return OperatorNode(operator, children)

        if isinstance(node, parser.rulesParser.PowExpressionContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 3:
                operator = node.getChild(1).getText()
                children = list()
                children.append(self.build(node.getChild(0)))
                children.append(self.build(node.getChild(2)))
                return OperatorNode(operator, children)

        if isinstance(node, parser.rulesParser.SignedAtomContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 2:
                children = list()
                children.append(SymbolNode(node.getChild(0).getText()))
                children.append(self.build(node.getChild(1)))
                return AtomNode(children)

        if isinstance(node, parser.rulesParser.AtomContext):
            if node.getChildCount() == 1:
                return self.build(node.getChild(0))
            if node.getChildCount() == 3:
                return self.build(node.getChild(1))

        if isinstance(node, parser.rulesParser.ScientificContext) or isinstance(node, parser.rulesParser.ConstantContext):
            if node.getChildCount() == 1:
                return SymbolNode(node.getChild(0).getText())

        return None

    def getText(self):
        return self.root.getText()



