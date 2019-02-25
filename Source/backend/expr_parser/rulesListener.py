# Generated from rules.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .rulesParser import rulesParser
else:
    from rulesParser import rulesParser

# This class defines a complete listener for a parse tree produced by rulesParser.
class rulesListener(ParseTreeListener):

    # Enter a parse tree produced by rulesParser#rules.
    def enterRules(self, ctx:rulesParser.RulesContext):
        pass

    # Exit a parse tree produced by rulesParser#rules.
    def exitRules(self, ctx:rulesParser.RulesContext):
        pass


    # Enter a parse tree produced by rulesParser#singleRule.
    def enterSingleRule(self, ctx:rulesParser.SingleRuleContext):
        pass

    # Exit a parse tree produced by rulesParser#singleRule.
    def exitSingleRule(self, ctx:rulesParser.SingleRuleContext):
        pass


    # Enter a parse tree produced by rulesParser#constraint.
    def enterConstraint(self, ctx:rulesParser.ConstraintContext):
        pass

    # Exit a parse tree produced by rulesParser#constraint.
    def exitConstraint(self, ctx:rulesParser.ConstraintContext):
        pass


    # Enter a parse tree produced by rulesParser#equation.
    def enterEquation(self, ctx:rulesParser.EquationContext):
        pass

    # Exit a parse tree produced by rulesParser#equation.
    def exitEquation(self, ctx:rulesParser.EquationContext):
        pass


    # Enter a parse tree produced by rulesParser#expression.
    def enterExpression(self, ctx:rulesParser.ExpressionContext):
        pass

    # Exit a parse tree produced by rulesParser#expression.
    def exitExpression(self, ctx:rulesParser.ExpressionContext):
        pass


    # Enter a parse tree produced by rulesParser#multiplyingExpression.
    def enterMultiplyingExpression(self, ctx:rulesParser.MultiplyingExpressionContext):
        pass

    # Exit a parse tree produced by rulesParser#multiplyingExpression.
    def exitMultiplyingExpression(self, ctx:rulesParser.MultiplyingExpressionContext):
        pass


    # Enter a parse tree produced by rulesParser#powExpression.
    def enterPowExpression(self, ctx:rulesParser.PowExpressionContext):
        pass

    # Exit a parse tree produced by rulesParser#powExpression.
    def exitPowExpression(self, ctx:rulesParser.PowExpressionContext):
        pass


    # Enter a parse tree produced by rulesParser#signedAtom.
    def enterSignedAtom(self, ctx:rulesParser.SignedAtomContext):
        pass

    # Exit a parse tree produced by rulesParser#signedAtom.
    def exitSignedAtom(self, ctx:rulesParser.SignedAtomContext):
        pass


    # Enter a parse tree produced by rulesParser#atom.
    def enterAtom(self, ctx:rulesParser.AtomContext):
        pass

    # Exit a parse tree produced by rulesParser#atom.
    def exitAtom(self, ctx:rulesParser.AtomContext):
        pass


    # Enter a parse tree produced by rulesParser#scientific.
    def enterScientific(self, ctx:rulesParser.ScientificContext):
        pass

    # Exit a parse tree produced by rulesParser#scientific.
    def exitScientific(self, ctx:rulesParser.ScientificContext):
        pass


    # Enter a parse tree produced by rulesParser#constant.
    def enterConstant(self, ctx:rulesParser.ConstantContext):
        pass

    # Exit a parse tree produced by rulesParser#constant.
    def exitConstant(self, ctx:rulesParser.ConstantContext):
        pass


    # Enter a parse tree produced by rulesParser#variable.
    def enterVariable(self, ctx:rulesParser.VariableContext):
        pass

    # Exit a parse tree produced by rulesParser#variable.
    def exitVariable(self, ctx:rulesParser.VariableContext):
        pass


    # Enter a parse tree produced by rulesParser#func.
    def enterFunc(self, ctx:rulesParser.FuncContext):
        pass

    # Exit a parse tree produced by rulesParser#func.
    def exitFunc(self, ctx:rulesParser.FuncContext):
        pass


    # Enter a parse tree produced by rulesParser#funcname.
    def enterFuncname(self, ctx:rulesParser.FuncnameContext):
        pass

    # Exit a parse tree produced by rulesParser#funcname.
    def exitFuncname(self, ctx:rulesParser.FuncnameContext):
        pass


    # Enter a parse tree produced by rulesParser#relop.
    def enterRelop(self, ctx:rulesParser.RelopContext):
        pass

    # Exit a parse tree produced by rulesParser#relop.
    def exitRelop(self, ctx:rulesParser.RelopContext):
        pass


