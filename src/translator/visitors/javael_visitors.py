import re
from typing import List, Set

from antlr4 import ParserRuleContext, TerminalNode
from loguru import logger
from queue import Queue

from ANTLR_JavaELParser.JavaELParser import JavaELParser
from ANTLR_JavaELParser.JavaELParserVisitor import JavaELParserVisitor
from src.translator.ast_algorithm.javael_ast_algorithm import add_color_to_ctx, isCtxSimple
from src.translator.dmn.dmn_tree import DMNTreeNode, OperatorDMN, ExpressionDMN
from src.translator.singleton.singleton_storage import OperatorsStorage
from src.translator.visitors.feel_visitors import FEELTreePrinter

logger = logger.opt(colors=True)
# logger.disable(__name__)

TERNARY_OP_COUNT = 5
TRUE_TERNARY_CHILDREN_NO = 2
FALSE_TERNARY_CHILDREN_NO = 4

keywords = [
    JavaELParser.Not,
    JavaELParser.Empty,
    JavaELParser.Or,
    JavaELParser.And,
    JavaELParser.Minus,
    JavaELParser.Plus,
    JavaELParser.LessEqual,
    JavaELParser.Less,
    JavaELParser.Greater,
    JavaELParser.GreaterEqual,
    JavaELParser.Equality,
    JavaELParser.Mul,
    JavaELParser.Div,
    JavaELParser.DoubleDots,
    JavaELParser.Question,
    JavaELParser.OpenParen,
    JavaELParser.OpenBracket,
    JavaELParser.CloseParen,
    JavaELParser.CloseBracket
]


class JavaELTreePrinter(JavaELParserVisitor):
    def __init__(self):
        super(JavaELTreePrinter, self).__init__()
        self.result = []

    def lastContextWasDMN(self):
        return len(self.result) > 0 and 'dmn_' in self.result[-1]

    def passIfNoDMN(self, ctx):
        if hasattr(ctx, 'colors') and len(ctx.colors):
            self.result.append(ctx.colors[-1])
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Terminal: <red>{id(node)}</red> <green>{node.getText()}</green> dmn: {hasattr(node, "colors")}')

        if node.symbol.type in keywords:
            self.result.append(' ')
            self.result.append(node.getText())
            self.result.append(' ')
        else:
            self.result.append(node.getText())

    def visitPrimitive(self, ctx: JavaELParser.PrimitiveContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Primitive: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitValue(self, ctx: JavaELParser.ValueContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Value: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Base: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Member: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Algebraic: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Relation: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Equality: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitTerm(self, ctx: JavaELParser.TermContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Term: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Expression: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        logger.opt(colors=True).info(
            f'JavaELTreePrinter visits Ternary: <red>{id(ctx)}</red> <green>{ctx.getText()}</green> dmn: {hasattr(ctx, "colors")}')
        if not self.lastContextWasDMN():
            return self.passIfNoDMN(ctx)

    @property
    def tree_expression(self):
        """
        returns stored expression and clear storage
        :return: string representation of expression
        """
        to_return = ''.join(self.result)
        to_return = " ".join(to_return.split())
        self.result.clear()
        return to_return


class SimpleExprDetector(JavaELParserVisitor):
    def __init__(self):
        super(JavaELParserVisitor, self).__init__()
        self._subtrees = 0

    @property
    def is_simple(self):
        return self._subtrees < 2

    @property
    def levels(self):
        return self._subtrees

    def subtree_cnt_update(self, ctx):
        if ctx.getChildCount() > 1:
            self._subtrees += 1

    def visitBase(self, ctx: JavaELParser.BaseContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitTerm(self, ctx: JavaELParser.TermContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        self.subtree_cnt_update(ctx)
        self.visitChildren(ctx)


class ToFEELConverter(JavaELParserVisitor):
    def __init__(self):
        super(ToFEELConverter, self).__init__()
        self.translated = []
        self.visited = []

    @property
    def result(self):
        to_ret = ''
        for i in self.translated:
            if i is not None:
                to_ret += i + ' '
        to_ret = to_ret.replace(' .', '.').replace('. ', '.').strip()
        to_ret = re.sub(r'\s+', ' ', to_ret)
        return to_ret

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        # logger.debug("visit Ternary {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()],
        #              self.translated)
        if ctx.getChildCount() > 1:  # ternary expression
            ctx_children = list(ctx.getChildren())
            condition_expression = ctx_children[0]
            true_ternary = ctx_children[2]
            false_ternary = ctx_children[4]

            self.translated.append('if')
            self.translated.append(self.visit(condition_expression))
            self.translated.append('then')
            self.translated.append(self.visit(true_ternary))
            self.translated.append('else')
            self.translated.append(self.visit(false_ternary))
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        # logger.debug("visit Relation {}: {} with translated {}", ctx.getText(),
        #              [i.getText() for i in ctx.getChildren()], self.translated)
        if ctx.getChildCount() > 1 and isinstance(ctx.getChild(1), TerminalNode):
            left_algebraic = ctx.getChild(0)
            right_algebraic = ctx.getChild(2)
            ctx_operator = ctx.getChild(1)

            self.translated.append(self.visit(left_algebraic))
            self.translated.append(self.translateRelationalToFEEL(ctx_operator))
            self.translated.append(self.visit(right_algebraic))

        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        # logger.debug("visit Equality {}: {} with translated {}", ctx.getText(),
        #              [i.getText() for i in ctx.getChildren()], self.translated)
        if ctx.getChildCount() > 1:
            self.translateEqualityToFEEL(ctx)
        else:
            return self.visitChildren(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        # logger.debug("visit Base {}: {} with translated {}", ctx.getText(), [i.getText() for i in ctx.getChildren()],
        #              self.translated)
        if ctx.getChildCount() > 1:
            self.translateUnaryToFEEL(ctx)
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        # logger.debug("visit Terminal {}", node.getText())
        self.translated.append(node.getText())

    def visitPrimitive(self, ctx: JavaELParser.PrimitiveContext):
        # logger.debug("visit Primitive {}: {} with translated {}", ctx.getText(),
        #              [i.getText() for i in ctx.getChildren()],
        #              self.translated)
        self.translated.append(ctx.getText())

    def translateUnaryToFEEL(self, ctx: ParserRuleContext):
        child_cht = ctx.getChildCount()
        for i in range(child_cht):
            child = ctx.getChild(i)
            if child not in self.visited:
                if isinstance(child, TerminalNode):
                    operator = child.symbol.type
                    self.visited.append(child)

                    if operator == JavaELParser.Not:
                        self.translated.append('not(')
                        self.translateUnaryToFEEL(ctx)
                        self.translated.append(')')

                    elif operator == JavaELParser.Empty:
                        self.translateUnaryToFEEL(ctx)
                        self.translated.append(' ')
                        self.translated.append(' = ')
                        self.translated.append('null')
                else:
                    self.visit(child)
                    self.visited.append(child)

    def visitChildren(self, node):
        result = self.defaultResult()
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return result

            c = node.getChild(i)
            childResult = None
            if c not in self.visited:
                childResult = c.accept(self)
            result = self.aggregateResult(result, childResult)

        return result

    @staticmethod
    def translateRelationalToFEEL(operator: str) -> str:
        if operator == 'gt':
            return '>'
        elif operator == 'lt':
            return '<'
        elif operator == 'ge':
            return '>='
        elif operator == 'le':
            return '<='

    def translateEqualityToFEEL(self, ctx: ParserRuleContext):
        operator = ctx.getChild(1).getText()
        if operator == '==' or operator == 'eq':
            self.translated.append(self.visit(ctx.getChild(0)))
            self.translated.append('=')
            self.translated.append(self.visit(ctx.getChild(2)))

        elif operator == '!=' or operator == 'ne':
            self.translated.append(self.visit(ctx.getChild(0)))
            self.translated.append('not(')
            self.translated.append(self.visit(ctx.getChild(2)))
            self.translated.append(')')


class FormulaZipper(JavaELParserVisitor):
    def __init__(self):
        super(FormulaZipper, self).__init__()
        self._zipped = []

    @property
    def result(self):
        to_ret = ''.join([token for token in self._zipped if token is not None]).replace(' . ', '.')
        to_ret = re.sub(r'\s+', ' ', to_ret)
        return to_ret

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        """
        A ? B : C ==
        (A -> B) and (!A -> C) == (!A or B) and (A or C) ==
        (!A and A) or (!A and С) or (B and A) or (B and С) ==
        (!A and С) or (A and B) or (B and С)
        :param ctx:
        :return:
        """
        if ctx.getChildCount() > 1:  # ternary expression here
            ctx_children = list(ctx.getChildren())
            condition_expression = ctx_children[0]
            true_ternary = ctx_children[2]
            false_ternary = ctx_children[4]

            # (not (A) and C)
            self._zipped.append('(! (')
            self._zipped.append(self.visit(condition_expression))
            self._zipped.append(') and ')
            self._zipped.append(self.visit(false_ternary))
            self._zipped.append(')')
            # or
            self._zipped.append(' or ')
            # (A and B)
            self._zipped.append('(')
            self._zipped.append(self.visit(condition_expression))
            self._zipped.append(' and ')
            self._zipped.append(self.visit(true_ternary))
            self._zipped.append(')')
            # # or
            # self._zipped.append(' or ')
            # # (B and C)
            # self._zipped.append('(')
            # self._zipped.append(self.visit(false_ternary))
            # self._zipped.append(' and ')
            # self._zipped.append(self.visit(true_ternary))
            # self._zipped.append(')')
        else:
            return self.visitChildren(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        return self.addIdIfSimple(ctx)

    def visitTerm(self, ctx: JavaELParser.TermContext):
        return self.addIdIfSimple(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        return self.addIdIfSimple(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        return self.addIdIfSimple(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        return self.addIdIfSimple(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        return self.addIdIfSimple(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        return self.addIdIfSimple(ctx)

    def visitValue(self, ctx: JavaELParser.ValueContext):
        return self.addIdIfSimple(ctx)

    def visitPrimitive(self, ctx: JavaELParser.PrimitiveContext):
        return self.addIdIfSimple(ctx)

    def visitTerminal(self, node):
        self._zipped.append(node.getText() + ' ')

    def addIdIfSimple(self, ctx: ParserRuleContext):
        if hasattr(ctx, 'is_simple_operand') and ctx.is_simple_operand:
            self._zipped.append('op_' + str(id(ctx)) + ' ')
            OperatorsStorage()[str(id(ctx))] = ctx
        else:
            return self.visitChildren(ctx)


class SimpleOperandMarker(JavaELParserVisitor):
    """
    Find and mark logical operands without other logical operators
    """

    @staticmethod
    def _findSimpleOperandAncestor(ctx: ParserRuleContext) -> ParserRuleContext or None:
        while ctx.parentCtx:
            if hasattr(ctx, 'is_simple_operand') and ctx.is_simple_operand:
                return ctx
            else:
                ctx = ctx.parentCtx
        return None

    @staticmethod
    def _mark_simple(ctx: ParserRuleContext, operator: TerminalNode):
        children = list(ctx.getChildren())
        children_cnt = len(children)

        if isinstance(ctx, (JavaELParser.ExpressionContext, JavaELParser.TermContext)):
            for i in range(children_cnt):
                if hasattr(children[i], 'symbol') and children[i].symbol.type == operator:
                    # убрать is_simple_operand у прямых родителей
                    if i - 1 >= 0:
                        left_operand_parent_with_simple = SimpleOperandMarker._findSimpleOperandAncestor(
                            children[i - 1])
                        if left_operand_parent_with_simple:
                            left_operand_parent_with_simple.is_simple_operand = False
                        children[i - 1].is_simple_operand = True

                    if i + 1 < children_cnt:
                        right_operand_parent_with_simple = SimpleOperandMarker._findSimpleOperandAncestor(
                            children[i + 1])
                        if right_operand_parent_with_simple:
                            right_operand_parent_with_simple.is_simple_operand = False
                        children[i + 1].is_simple_operand = True
        elif isinstance(ctx, JavaELParser.BaseContext):
            for i in range(children_cnt):
                if not (hasattr(children[i], 'symbol') and children[i].symbol.type in [JavaELParser.Not,
                                                                                       JavaELParser.Empty,
                                                                                       JavaELParser.Minus]):
                    # operand branch
                    operand_marked_parent = SimpleOperandMarker._findSimpleOperandAncestor(children[i])
                    if operand_marked_parent:
                        operand_marked_parent.is_simple_operand = False
                    children[i].is_simple_operand = True
                    return

    def visitTerm(self, ctx: JavaELParser.TermContext):

        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        self._mark_simple(ctx, JavaELParser.And)
        return self.visitChildren(ctx)

    def visitExpression(self, ctx: JavaELParser.ExpressionContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return

        self._mark_simple(ctx, JavaELParser.Or)
        return self.visitChildren(ctx)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return

        self._mark_simple(ctx, JavaELParser.Not)
        return self.visitChildren(ctx)

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        # если нода помечена как dmn, то она простая
        if hasattr(ctx, 'colors') and len(ctx.colors):
            ctx.is_simple_operand = True
            return
        else:
            return self.visitChildren(ctx)

    def visitTerminal(self, node):
        # если нода помечена как dmn, то она простая
        if hasattr(node, 'colors') and len(node.colors):
            node.is_simple_operand = True
            return
        else:
            return self.visitChildren(node)


class KNFToDMNVisitor(JavaELParserVisitor):
    """
    Extract to DMN node operands of non-logical operators
    """

    def __init__(self, node: DMNTreeNode):
        super(KNFToDMNVisitor, self).__init__()
        self.node = node

    def add_binary_children(self, ctx_l: ParserRuleContext, ctx_r: ParserRuleContext, operator: int):
        # self.node
        #    |
        #    |
        # operator
        #  |    |
        #  |    |
        # left right
        new_op_node = OperatorDMN(operator)

        ast_printer = FEELTreePrinter()

        ast_printer.visit(ctx_l)
        new_expr_node_l = ExpressionDMN(ast_printer.tree_expression, [ctx_l])

        ast_printer.visit(ctx_r)
        new_expr_node_r = ExpressionDMN(ast_printer.tree_expression, [ctx_r])

        new_op_node.children.append(new_expr_node_l)
        new_op_node.children.append(new_expr_node_r)

        self.node.children.append(new_op_node)
        return id(new_op_node)

    def add_unary_children(self, text: str, ctxs: List[ParserRuleContext], operator: int = None):
        """
        Генерирует имя для DMNTreeNode, создает нового ребенка у node,
        в выражении родителя заменяет выражение ребенка на dmn id вида dmn_{int}
        :param ctxs:
        :param text: часть выражения, записанная с пробелами
        :param operator:
        :return:
        """
        # self.node
        #    |
        #    |
        # operator
        #    |
        #    |
        # expression
        if operator:
            new_op_node = OperatorDMN(operator)
            new_expr_node = ExpressionDMN(text, ctxs)
            new_op_node.children.append(new_expr_node)
            self.node.children.append(new_op_node)
            return id(new_op_node)
        else:
            new_node = ExpressionDMN(text, ctxs)
            self.node.children.append(new_node)
            return id(new_node)

    def visitBase(self, ctx: JavaELParser.BaseContext):
        if ctx.getChildCount() > 1:
            self.processUnary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitMember(self, ctx: JavaELParser.MemberContext):
        if ctx.getChildCount() > 1:
            self.processBinary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitAlgebraic(self, ctx: JavaELParser.AlgebraicContext):
        if ctx.getChildCount() > 1:
            self.processBinary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitEquality(self, ctx: JavaELParser.EqualityContext):
        if ctx.getChildCount() > 1:
            self.processBinary(ctx)
        else:
            return self.visitChildren(ctx)

    def visitRelation(self, ctx: JavaELParser.RelationContext):
        if ctx.getChildCount() > 1:
            # пропустить скобки
            if not (isinstance(ctx.getChild(0), TerminalNode) and ctx.getChild(
                    0).symbol.type == JavaELParser.OpenParen) and not (
                    isinstance(ctx.getChild(2), TerminalNode) and ctx.getChild(
                2).token.type != JavaELParser.CloseParen):
                self.processBinary(ctx)
            else:
                return self.visitChildren(ctx)
        else:
            return self.visitChildren(ctx)

    def processUnary(self, ctx: ParserRuleContext):
        """
        Add DMNNode represents unary operator if operand not simple. Remove operator and replace operands to dmn11111...
        :param ctx:
        :return:
        """
        children_count = ctx.getChildCount()
        for i in range(children_count):

            # pass operated
            if not hasattr(ctx.getChild(i), 'visited') or not ctx.getChild(i).visited:
                maybe_operator = ctx.getChild(i)
                maybe_operand = ctx.getChild(i + 1)

                ast_printer = FEELTreePrinter()
                # case with chain unary operators
                if isinstance(maybe_operand, TerminalNode):
                    maybe_operator.visited = True

                    new_child_ctxs = []
                    new_child_text = []

                    for j in range(i + 1, children_count):
                        new_child_ctxs.append(ctx.getChild(j))
                        ast_printer.visit(ctx.getChild(j))
                        new_child_text.append(ast_printer.tree_expression)

                    new_child_text = ' '.join(new_child_text)

                    new_child_id = 'dmn' + str(self.add_unary_children(new_child_text, new_child_ctxs, maybe_operator))

                    # редактируем свое выражение
                    ast_printer.visit(maybe_operand)
                    self.node.expression = self.node.expression.replace(ast_printer.tree_expression,
                                                                        ' ' + new_child_id + ' ').replace(
                        maybe_operator.getText(), '')

                    # все следующие пометить как принадлежащие node
                    for j in range(i + 1, children_count):
                        ast_printer.visit(ctx.getChild(j))
                        self.node.expression = self.node.expression.replace(ast_printer.tree_expression, '')
                        add_color_to_ctx(ctx.getChild(j), new_child_id)
                    break
                else:
                    maybe_operator.visited = True
                    maybe_operand.visited = True

                    # TODO: maybe_operand захватывает все выражение, а не только операнд
                    ast_printer.visit(maybe_operand)
                    new_child_id = 'dmn' + str(
                        self.add_unary_children(ast_printer.tree_expression, [maybe_operand], maybe_operator))

                    ast_printer.visit(maybe_operand)

                    # редактируем свое выражение
                    self.node.expression = self.node.expression.replace(ast_printer.tree_expression,
                                                                        ' ' + new_child_id + ' ').replace(
                        maybe_operator.getText(), '')
                    # пометить операнд как принадлежащий node
                    add_color_to_ctx(maybe_operand, new_child_id)
                    # self.node.expression = self.node.expression.replace(maybe_operand.getText(), ' ' + new_child_id + ' ')

                    break

    def processBinary(self, ctx: ParserRuleContext):
        """
        Add DMNNode if at least one operand not simple
        :param ctx:
        :return:
        """
        children_count = ctx.getChildCount()
        if children_count > 1:
            if not isCtxSimple(ctx.getChild(0)) or not isCtxSimple(ctx.getChild(2)):
                self.add_binary_children(ctx.getChild(0), ctx.getChild(2), ctx.getChild(1).symbol.type)
                # if not isinstance(ctx.getChild(0), TerminalNode):
                #     if not isCtxSimple(ctx.getChild(0)):
                #         self.add_unary_children(ctx.getChild(0), ctx.getChild(1))
                #         add_color_to_ctx(ctx.getChild(0), 'dmn_id' + str(id(self.node)))
                # if not isinstance(ctx.getChild(2), TerminalNode):
                #     if not isCtxSimple(ctx.getChild(2)):
                #         self.add_unary_children(ctx.getChild(2), ctx.getChild(1))
                #         add_color_to_ctx(ctx.getChild(2), 'dmn_id' + str(id(self.node)))


class TernaryNodesCollector(JavaELParserVisitor):
    """
    Found all exactly ternary nodes
    """

    def __init__(self):
        super(TernaryNodesCollector, self).__init__()
        self._ternary_ctx_buffer = set()

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        if ctx.getChildCount() == TERNARY_OP_COUNT:
            self._ternary_ctx_buffer.add(ctx)
        self.visitChildren(ctx)

    @property
    def result(self) -> Set[JavaELParser.TernaryContext]:
        return self._ternary_ctx_buffer


class NestingCounter(JavaELParserVisitor):
    """
    Count height of included ternaries trie
    """

    def __init__(self, ternary_marked: set):
        super(NestingCounter, self).__init__()
        self._height = 0
        self._ternaries = ternary_marked

    def visit_included_ternary(self, ctx):
        for child in ctx.getChildren():
            if child in self._ternaries:
                self._height += 1
                self.visit(child)

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        # root case
        if self._height == 0 and ctx.getChildCount() == TERNARY_OP_COUNT:
            self._height = 1
            self.visit_included_ternary(ctx)
        # common case
        elif ctx.getChildCount() == TERNARY_OP_COUNT:
            self.visit_included_ternary(ctx)

    @property
    def result(self):
        return self._height


class TernaryResultFounder(JavaELParserVisitor):
    """
    Visitor for finding which value relates to sequence of decisions
    """

    def __init__(self, decisions: List[bool]):
        super(TernaryResultFounder, self).__init__()
        self._answer_ctx = None
        self._decisions = Queue()
        for ans in decisions:
            self._decisions.put(ans)

    def visitTernary(self, ctx: JavaELParser.TernaryContext):
        """
        Find first node with only 1 children
        :param ctx:
        :return:
        """
        if ctx.getChildCount() == TERNARY_OP_COUNT:

            current_transition = self._decisions.get()

            if current_transition:
                true_context = ctx.getChild(TRUE_TERNARY_CHILDREN_NO)
                self.visit(true_context)
            else:
                false_context = ctx.getChild(FALSE_TERNARY_CHILDREN_NO)
                self.visit(false_context)

        else:
            self._answer_ctx = ctx

    @property
    def result(self):
        return self._answer_ctx
