from antlr4 import *
from ANTLR_FEELParser.feelParser import feelParser
from ANTLR_FEELParser.feelLexer import feelLexer
from ANTLR_FEELParser.feelVisitor import feelVisitor


def tree(expression: str) -> ParserRuleContext:
    """
    Create AST from expression and return root node
    :param expression:
    :return:
    """
    input_stream = InputStream(expression)
    lexer = feelLexer(input_stream)
    tree_returned = feelParser(CommonTokenStream(lexer))
    return tree_returned.compilation_unit()


class FEELInputExtractor(feelVisitor):
    def __init__(self):
        super(FEELInputExtractor, self).__init__()
        self.identifiers = set()

    @property
    def result(self):
        return self.identifiers

    def visitR_filterPathExpression(self, ctx:feelParser.R_filterPathExpressionContext):
        lbrack_found = False
        rbrack_found = False
        for c in ctx.getChildren():
            if isinstance(c, TerminalNode) and c.symbol.type == feelParser.LBRACK:
                lbrack_found = True
            elif isinstance(c, TerminalNode) and c.symbol.type == feelParser.RBRACK:
                rbrack_found = True

        if lbrack_found and rbrack_found:
            p = SyntaxTreePrinter()
            p.visit(ctx)
            self.identifiers.add(p.tree_expression)
        else:
            self.visitChildren(ctx)

    def visitTerminal(self, node):
        if node.symbol.type == feelLexer.Identifier and isinstance(node.parentCtx, feelParser.NameRefContext):
            self.identifiers.add(node.getText())


class FEELRuleExtractor(feelVisitor):
    def __init__(self):
        super(FEELRuleExtractor, self).__init__()
        self.rule = []

    @property
    def result(self) -> str:
        return ' '.join(self.rule)

    def visitCompExpression(self, ctx:feelParser.CompExpressionRelContext):
        self.rule.extend(
            (
                ctx.getChild(1).getText(),
                ctx.getChild(2).getText()
            )
        )

    def visitFnInvocation(self, ctx:feelParser.FnInvocationContext):
        self.rule.append(
            ctx.getText()
        )


class SyntaxTreePrinter(feelVisitor):
    def __init__(self):
        super(SyntaxTreePrinter, self).__init__()
        self.result = []

    def visitTerminal(self, node):
        self.result.append(node.getText())

    @property
    def tree_expression(self):
        return ' '.join(self.result)

