from ANTLR_FEELParser.feelParser import feelParser
from ANTLR_FEELParser.feelVisitor import feelVisitor


class FEELInputExtractor(feelVisitor):
    def __init__(self):
        super(FEELInputExtractor, self).__init__()
        self.identifiers = set()

    @property
    def result(self):
        to_return = set()
        for r in self.identifiers:
            to_return.add(r.replace(' . ', '_').replace('(', '_').replace(')', '').replace(' ', ''))
        return to_return

    # def visitQualifiedName(self, ctx:feelParser.QualifiedNameContext):
    #     p = FEELTreePrinter()
    #     p.visit(ctx.parentCtx)
    #     self.identifiers.add(p.tree_expression)

    def visitTerminal(self, node):
        if node.symbol.type == feelParser.Identifier:
            self.identifiers.add(node.getText())

    # def visitFnInvocation(self, ctx:feelParser.FnInvocationContext):
    #     p = FEELTreePrinter()
    #     p.visit(ctx.parentCtx)
    #     self.identifiers.add(p.tree_expression)


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
            'boolean'
        )


class OrSplitter(feelVisitor):
    def __init__(self):
        super(OrSplitter, self).__init__()
        self._operators = []

    def visitCondOr(self, ctx:feelParser.CondOrContext):
        printer = FEELTreePrinter()
        printer.visit(ctx.getChild(0))
        self._operators.append(printer.tree_expression)

        printer.visit(ctx.getChild(2))
        self._operators.append(printer.tree_expression)

    @property
    def result(self):
        return self._operators

    def clear(self):
        self._operators.clear()


class AndSplitter(feelVisitor):
    def __init__(self):
        super(AndSplitter, self).__init__()
        self._operators = []

    def visitCondAnd(self, ctx: feelParser.CondOrContext):
        printer = FEELTreePrinter()
        printer.visit(ctx.getChild(0))
        self._operators.append(printer.tree_expression)

        printer.visit(ctx.getChild(2))
        self._operators.append(printer.tree_expression)

    @property
    def result(self):
        return self._operators

    def clear(self):
        self._operators.clear()


class ScopesDeleter(feelVisitor):
    def __init__(self):
        super(ScopesDeleter, self).__init__()
        self._operator = []

    def visitPrimaryParens(self, ctx:feelParser.PrimaryParensContext):
        printer = FEELTreePrinter()
        printer.visit(ctx.getChild(1))
        self._operator.append(printer.tree_expression)

    @property
    def result(self):
        return self._operator


class FEELTreePrinter(feelVisitor):
    def __init__(self):
        super(FEELTreePrinter, self).__init__()
        self.result = []

    def visitTerminal(self, node):
        self.result.append(node.getText())

    def visitParametersPositional(self, ctx):
        self.result.append(ctx.getText())

    @property
    def tree_expression(self):
        to_return = ' '.join(self.result)
        self.result.clear()
        return to_return