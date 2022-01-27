from enum import Enum
from queue import Queue
from typing import List

from antlr4 import *

from ANTLR_FEELParser.feelLexer import feelLexer
from ANTLR_FEELParser.feelParser import feelParser
from src.translator.visitors.feel_visitors import OrSplitter, AndSplitter, ScopesDeleter


class OPERATOR(Enum):
    OR = 1,
    AND = 2


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


def delete_external_scopes(expr: ParserRuleContext) -> str or None:
    scopes_deleter = ScopesDeleter()
    scopes_deleter.visit(expr)
    without_scopes = scopes_deleter.result
    if len(without_scopes) > 0:
        return without_scopes[0]
    else:
        return None


def split_by_operator(expr: str, operator: OPERATOR) -> List[str]:
    feel_ast = tree(expr)
    splitter = None
    if operator == OPERATOR.OR:
        splitter = OrSplitter()
    elif operator == OPERATOR.AND:
        splitter = AndSplitter()
    else:
        raise ValueError("split_by_operator got wrong operator type")
    splitter.visit(feel_ast)

    to_return = []

    queue = Queue()
    for op in splitter.result:
        queue.put(op)

    if queue.empty():
        without_scopes = delete_external_scopes(feel_ast)
        if without_scopes:
            return [without_scopes]
        else:
            return [expr]

    while not queue.empty():
        splitter.clear()
        op = queue.get()
        op_tree = tree(op)
        splitter.visit(op_tree)

        if len(splitter.result):
            for new_op in splitter.result:
                queue.put(new_op)
        else:
            without_scopes = delete_external_scopes(op_tree)
            if without_scopes:
                to_return.append(without_scopes)
            else:
                to_return.append(op)

    return to_return
