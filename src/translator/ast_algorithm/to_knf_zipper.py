import re
from collections import namedtuple
from typing import Set

from antlr4 import ParserRuleContext
from loguru import logger

from src.translator.visitors.feel_visitors import FEELTreePrinter
from src.translator.visitors.javael_visitors import SimpleOperandMarker, FormulaZipper
from src.translator.singleton.singleton_storage import OperatorsStorage

ExpressionZipped = namedtuple('ExpressionZipped', ('expression', 'tree'))

logger = logger.opt(colors=True)

extract_id_re = re.compile(r'op_(\d+)')

not_re = re.compile(r'~([\d\w_]+)')


def zipFormula(context: ParserRuleContext) -> ExpressionZipped:
    SimpleOperandMarker().visit(context)
    zipper = FormulaZipper()
    zipper.visit(context)
    return ExpressionZipped(zipper.result, context)


def unzipOperand(operand_id: str) -> str:
    operand = OperatorsStorage()[operand_id]

    logger.opt(colors=True).debug(
        f'<green>unzip {operand_id}</green> to class: {operand.__class__.__name__}, attrs: {operand.__dict__}')

    printer = FEELTreePrinter()
    printer.visit(operand)
    result = printer.tree_expression
    return result


def concatWithOr(or_operands: Set[str]):
    scoped_or_operands = set()
    for s in or_operands:
        scoped_or_operands.add('(' + s + ')')

    return ' or '.join(scoped_or_operands)


def unpack(formula: str) -> str:
    # set scopes after not
    for not_m in not_re.findall(formula):
        formula = formula.replace(not_m, '(' + not_m + ')')

    # unzip by id
    for m in extract_id_re.findall(formula):
        formula = formula.replace(m, unzipOperand(m))
    formula = formula.replace('op_', ' ')
    formula = re.sub(r'_(..)_', r' \g<1> ', formula)
    formula = formula.replace('_ ', ' ').replace(' _', ' ').replace("\'", "\"")

    # java el logical operators form
    formula = formula.replace('~', '!').replace('And', 'and').replace('Or', 'or')
    return ' '.join(formula.split())
