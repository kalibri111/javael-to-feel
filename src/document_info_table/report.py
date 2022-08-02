import sys
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../../')
sys.path.append(filename)

import re
import copy
import click
import sys
import pandas as pd
import xml.etree.ElementTree as ET
from loguru import logger
from collections import namedtuple
from typing import List, Set, Dict
from src.document_info_table.legacy.JavaEL_tokenize import JavaELTokenType, tokenize_expression
from src.translator.ast_algorithm.javael_ast_algorithm import tree
from src.translator.runner import generate_drd
from src.translator.visitors.javael_visitors import SimpleExprDetector
from src.translator.ast_algorithm.syntax_error_listener import JavaELSyntaxError
import ahocorasick
import json

ExpressionDependencyBase = namedtuple(
    'ExpressionDependencyBase',
    (
        'code',
        'expression',
        'dmn_name',
        'attr',
        'form',
        'name',
    )
)

ExpressionOpReport = namedtuple(
    'ExpressionOpReport',
    (
        'andCnt',
        'orCnt',
        'treeLvl',
        'attrsCnt'
    )
)

class ExpressionDependency(ExpressionDependencyBase):
    pass


logger.remove()
logger.add(sys.stdout, colorize=True, level='DEBUG', format='{level} {message}')

# find <key>(...)</key><value(...)>
property_expression_re = re.compile(r'(?<=<key>)(.*?)(?=</key>\s*<value(.*?)>)')
# find JavaEL expression
expression_re = re.compile(r'(\w+)=\"#{(.*?)}\"')
# file extension regexp
extract_filetype_re = re.compile(r'\w+\.(xml)')
# find form name
form_name_re = re.compile(r'objectForm name=\"(.+?)\"')
# find russian name
russian_name_re = re.compile(r'name=\"(.+?)\"')
# find english name
english_name_re = re.compile(r'code=\"(.+?)\"')

# compiled dataframe columns names
DATAFRAME_SRC_FORM_NAME = 'srcFormName'
DATAFRAME_SRC_FIELD_NAME = 'srcFieldName'
DATAFRAME_SRC_FIELD_CODE = 'srcFieldCode'
DATAFRAME_SRC_FIELD_PROP = 'srcFieldProp'
DATAFRAME_DMN_NAME = 'DMN_name'
DATAFRAME_EXPRESSION = 'expression'
DATAFRAME_IS_SIMPLE = 'isSimple'
DATAFRAME_DRD_FILE = 'DRDFile'
AND_CNT = 'andCnt'
OR_CNT = 'orCnt'
ATRS_CNT = 'atrsCnt'
TREE_LVL_CNT = 'treeLvlCnt'

MNEMONICS_PATH = 'mnemonics.json'


def extract_prop_dependency_from_file(xml_file_path) -> Dict[str, List[ExpressionDependency]]:
    """
    get Java EL expressions from xml file with <form> tags
    :param xml_file_path: path to form xml file
    :return: dict {
                    'formName1': [ExpressionsDependency ...],
                    'formName2': [ExpressionsDependency ...],
                    ...
                    }
    """
    if extract_filetype_re.findall(xml_file_path)[0] != 'xml':
        raise ValueError('Invalid xml file')
    forms_exprs_props = {}

    xml_tree = ET.parse(xml_file_path)
    root = xml_tree.getroot()
    forms = list(root.iter('forms'))

    for form in forms:
        props_exprs = re.findall(property_expression_re, form.text)
        form_name = form_name_re.findall(form.text)[0]

        if props_exprs:
            forms_exprs_props[form_name] = []

            for match in props_exprs:
                print("NEW MATCH: " + match[1])

                exprs = re.findall(expression_re, match[1])
                if exprs:
                    prop_name = re.findall(russian_name_re, match[1])

                    if len(prop_name):
                        prop_name = prop_name[0]
                    else:
                        prop_name = "ERROR"

                    for e in exprs:
                        forms_exprs_props[form_name].append(
                            ExpressionDependency(
                                code=match[0],
                                dmn_name=match[0] + '.' + e[0],
                                attr=e[0],
                                expression=e[1],
                                form=form_name,
                                name=prop_name
                            )
                        )

    return forms_exprs_props


def extract_props_from_expression(expr_dep: str) -> Set[str]:
    """
    From all lvalues remove "fields." prefix and properties or rvalue like prop.attr
    :param expr_dep: ExpressionDependency
    :return: List[str]
    """
    tokens = tokenize_expression(expr_dep)
    dependents = set()

    for token in tokens:
        if token.token_type == JavaELTokenType.LVALUE:
            val = copy.deepcopy(token.token_value)
            val = re.sub(r'^fields.', '', val)
            val = re.search(r'\w+', val)
            if val:
                dependents.add(val[0])
            else:
                logger.debug(f'Syntax error during extract dependent property from {token.token_value}')
        elif token.token_type == JavaELTokenType.RVALUE:
            val = copy.deepcopy(token.token_value)
            val = re.findall(r'^(\w+)\.', val)
            if val:
                dependents.add(val[0])

    return dependents


def csv_filename_generator(storage: str) -> str:
    return storage + '/general_info.csv'


def is_expression_simple(expr: str) -> bool:
    # TODO: other metrics
    ast = tree(expr)
    visitor = SimpleExprDetector()
    visitor.visit(ast)
    return visitor.is_simple


def dictionary_init(json_dict: dict) -> ahocorasick.Automaton:
    automaton = ahocorasick.Automaton()
    for key in json_dict.keys():
        automaton.add_word(key, key)
    automaton.make_automaton()
    return automaton


def substitute_mnemonic(expr: str, automaton: ahocorasick.Automaton, json_dict: dict) -> str:
    """
    find substring and substitute with mnemonic using ahocorasik algorithm
    :param json_dict: dict of mnemonics
    :param automaton: initialized strings automaton
    :param expr: expression to modify
    :return: modified expression
    """
    for end_index, value in automaton.iter(expr):
        expr = expr.replace(value, json_dict[value])
    return expr


def expression_op_report(expr: str, attrs: Set[str]):
    """
    Dummy function for expression statistic
    :param expr:
    :param attrs:
    :return:
    """
    attrs_cnt = 0
    and_cnt = expr.count(' and ')
    or_cnt = expr.count(' or ')
    tre_lvl_cnt = 0

    for atr in attrs:
        if atr in expr:
            attrs_cnt += 1

    ast = tree(expr)
    visitor = SimpleExprDetector()
    visitor.visit(ast)
    tre_lvl_cnt = visitor.levels

    return ExpressionOpReport(andCnt=and_cnt, orCnt=or_cnt, treeLvl=tre_lvl_cnt, attrsCnt=attrs_cnt)


def generate_report(path, out, mnemonics):
    """
    Generates report table
    :param mnemonics: json with substitutions for complex lexems
    :param path: path to source document
    :param out: directory to generate report csv file
    :return: None
    """
    javael_exprs_from_file = extract_prop_dependency_from_file(xml_file_path=path)

    adjacency = {}  # str: List[str]

    attrs = set()

    for form in javael_exprs_from_file.keys():
        for expr in javael_exprs_from_file[form]:
            logger.debug(expr.expression)
            # find dependent expressions here
            try:
                adjacency[expr] = extract_props_from_expression(expr.expression)
                attrs.add(expr.attr)
            except ValueError:
                # TODO: error handler
                pass

    logger.debug(f"attrs: {attrs}")
    dataframe = pd.DataFrame(
        columns=[
            DATAFRAME_SRC_FORM_NAME,
            DATAFRAME_SRC_FIELD_NAME,
            DATAFRAME_DMN_NAME,
            DATAFRAME_SRC_FIELD_CODE,
            DATAFRAME_SRC_FIELD_PROP,
            DATAFRAME_IS_SIMPLE,
            DATAFRAME_EXPRESSION,
            DATAFRAME_DRD_FILE,
            OR_CNT,
            AND_CNT,
            ATRS_CNT,
            TREE_LVL_CNT
        ]
    )

    dataframe_rows = []

    # ahocorasic initialization
    with open(mnemonics, 'r') as mnemonic_file:
        dict_of_mnemonics = json.load(mnemonic_file)

    suf_automaton = dictionary_init(dict_of_mnemonics)

    for key in adjacency.keys():
        try:
            is_simple = is_expression_simple(key.expression)
        except JavaELSyntaxError:
            is_simple = 'syntax_error'
            continue
        generated_file = ''

        # substitute the mnemonic
        logger.info(f'substitute mnemonic from {key.expression}')

        subst_expr = substitute_mnemonic(key.expression, suf_automaton, dict_of_mnemonics)

        if not is_simple:
            try:
                logger.info(f'start generating xml from {subst_expr}')
                # TODO: disabled drd generation
                # generated_file = generate_drd(subst_expr, out)

            except JavaELSyntaxError:
                logger.info(f'syntax error during xml form {subst_expr} generation')
                generated_file = 'syntax_error'
            else:
                logger.info(f'successfully generated xml from {subst_expr}')

        expr_report = expression_op_report(key.expression, attrs)

        new_row = {
            DATAFRAME_SRC_FORM_NAME: key.form,
            DATAFRAME_SRC_FIELD_NAME: key.name,
            DATAFRAME_DMN_NAME: key.dmn_name,
            DATAFRAME_SRC_FIELD_CODE: key.code,
            DATAFRAME_SRC_FIELD_PROP: key.attr,
            DATAFRAME_EXPRESSION: subst_expr,
            DATAFRAME_IS_SIMPLE: 'true' if is_simple else 'false',
            DATAFRAME_DRD_FILE: generated_file,
            OR_CNT: expr_report.orCnt,
            AND_CNT: expr_report.andCnt,
            ATRS_CNT: expr_report.attrsCnt,
            TREE_LVL_CNT: expr_report.treeLvl
        }

        logger.debug(f'adding row {new_row}')

        dataframe_rows.append(
            new_row
        )
    dataframe = dataframe.append(pd.DataFrame(dataframe_rows))

    dataframe.to_csv(csv_filename_generator(out), index=False)


@click.command()
@click.argument('path')
@click.argument('out')
def main(path, out):
    generate_report(path, out, MNEMONICS_PATH)


if __name__ == '__main__':
    main()
