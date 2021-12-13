from ANTLR_FEELParser.feelVisitor import feelVisitor
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor


class SimpleExprDetector(JavaELParserVisitor):
    def __init__(self):
        super(JavaELParserVisitor, self).__init__()
        self._subtrees = 0

    @property
    def is_simple(self):
        return self._subtrees < 2

    def subtree_cnt_update(self, ctx):
        if ctx.getChildCount() > 1:
            self._subtrees += 1

    def visitBase(self, ctx:JavaELParser.BaseContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitMember(self, ctx:JavaELParser.MemberContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitAlgebraic(self, ctx:JavaELParser.AlgebraicContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitRelation(self, ctx:JavaELParser.RelationContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitEquality(self, ctx:JavaELParser.EqualityContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitTerm(self, ctx:JavaELParser.TermContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitExpression(self, ctx:JavaELParser.ExpressionContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitTernary(self, ctx:JavaELParser.TernaryContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)
