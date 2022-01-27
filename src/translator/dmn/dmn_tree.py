from typing import List

from antlr4 import *
from loguru import logger

logger = logger.opt(colors=True)


class DMNTreeNode:
    def __init__(self):
        self.children = []
        self.contexts = None


class ExpressionDMN(DMNTreeNode):
    def __init__(self, expr: str, ctxs: List[ParserRuleContext]):
        super(ExpressionDMN, self).__init__()
        self.expression = expr
        self.contexts = ctxs
        self.children = []


class OperatorDMN(DMNTreeNode):
    def __init__(self, operator: int):
        super(OperatorDMN, self).__init__()
        self.operator = operator
