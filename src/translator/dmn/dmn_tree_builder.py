from antlr4 import TerminalNode, ParserRuleContext
from loguru import logger

from src.translator.dmn.dmn_tree import ExpressionDMN, OperatorDMN, DMNTreeNode
from src.translator.visitors.feel_visitors import FEELTreePrinter
from src.translator.visitors.javael_visitors import KNFToDMNVisitor

logger.opt(colors=True)


class DMNTree:
    def __init__(self, ctx: ParserRuleContext):
        self.ctx = ctx
        if ctx:
            p = FEELTreePrinter()
            p.visit(ctx)
            self.root = ExpressionDMN(p.tree_expression, [ctx])
            find_dependencies(self.root)


def find_dependencies(dmn_tree_node):
    """
    Find dependent sub DMN expressions and replace to id
    example: field.first eq field.second and not (field.third or true) ->
          -> field.first eq field.second and dmn_1
    :return:
    """
    # только один контекст не терминальный
    if isinstance(dmn_tree_node, ExpressionDMN):
        for c in dmn_tree_node.contexts:
            if not isinstance(c, TerminalNode):
                KNFToDMNVisitor(dmn_tree_node).visit(c)

    for child in dmn_tree_node.children:
        find_dependencies(child)


def printDMNTree(dmntree: DMNTree) -> None:
    root_node = dmntree.root
    _printDMNTree(root_node)


def _printDMNTree(node: DMNTreeNode) -> None:
    if isinstance(node, ExpressionDMN):
        logger.debug(
            f"ExpressionDMN node {id(node)} expression: {node.expression}, children: {[node.children]}")
    elif isinstance(node, OperatorDMN):
        logger.debug(
            f"OperatorDMN node {id(node)} operator: {node.operator}")
    for child in node.children:
        _printDMNTree(child)
