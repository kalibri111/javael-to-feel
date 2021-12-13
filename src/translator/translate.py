from lxml import etree

from src.translator.ast_printer import FEELTreePrinter
from src.translator.dmn_tree import DMNTreeNode, ExpressionDMN, DMNTree, printDMNTree, OperatorDMN
from src.translator.feel_translator import ToFEELConverter
from src.translator.knf_converter import toDMNReady
from src.translator.node_algorithm import tree
from src.translator.to_knf_zipper import zipFormula, unpack, concatWithOr
from loguru import logger

from src.translator.xml_packer import DMN_XML, ShapesDrawer
from src.translator.zip_storage import OperatorsStorage, TableToDepTables, TableToDepInputDatas, InputDataToInfoReq


def translate(java_el_expr: str) -> DMNTree:
    """
    Builds DMNTree representation of translated to FEEL java_el_expr
    :param java_el_expr: Valid Java EL expression
    :return: translated representation of given expression
    """
    el_tree = tree(java_el_expr)
    dmn_tree = DMNTree(el_tree)
    logger.debug('This tree wil be translated')
    printDMNTree(dmn_tree)
    logger.debug('---------------------------')
    # logger.opt(colors=True).debug('<green>Syntax tree after dmn defragmentation</green>')
    # stp = FEELTreePrinter()
    # stp.visit(el_tree)
    # logger.opt(colors=True).debug(f'<green>{stp.tree_expression}</green>')
    # logger.debug('---------------------------')
    translateDMNReadyinDMNTree(dmn_tree)
    logger.debug(f'Operators storage saves: {OperatorsStorage().keys()}')
    logger.debug('Translated DMN tree')
    printDMNTree(dmn_tree)
    logger.debug('---------------------------')
    return dmn_tree


def xml_from_dmntree(dmn_tree_translated_root: DMNTree, xml_out_path: str) -> str:
    """
    Builds xml representation of DMN structure and returns path to generated file
    :param dmn_tree_translated_root: represents FEEL expressions, connected by non-logical operators
    :param xml_out_path: path where to build xml
    :return: None
    """
    dmn_xml_root = DMN_XML().visit(dmn_tree_translated_root)

    logger.debug(f"DependenceStorage has state: {TableToDepTables()}")
    logger.debug(f"InputDataStorage has state: {TableToDepInputDatas()}")
    logger.debug(f"InputDataToInfoReq has state: {InputDataToInfoReq()}")

    shapes_tag_root = ShapesDrawer().draw(dmn_tree_translated_root)

    dmn_xml_root.append(shapes_tag_root)

    generated_filepath = xml_out_path + str(id(dmn_tree_translated_root)) + '.xml'
    etree.ElementTree(dmn_xml_root).write(generated_filepath, pretty_print=True)
    return generated_filepath


def translateDMNReadyinDMNTree(dmntree: DMNTree) -> None:
    root_node = dmntree.root
    _translateDMNReadyinDMNTree(root_node)


def _translateDMNReadyinDMNTree(node: DMNTreeNode) -> None:
    # нет оператора -> выражение состоит только из логических операторов,
    # нелогические операторы имеют только простые операнды

    for child in node.children:
        _translateDMNReadyinDMNTree(child)

    if isinstance(node, ExpressionDMN):
        printer = FEELTreePrinter()
        printer.visit(tree(node.expression))
        node.expression = zipFormula(tree(printer.tree_expression)).expression
        printer.visit(tree(node.expression))
        node.expression = printer.tree_expression
        logger.debug(f"translating ExpressionDMN node {node.expression}")
        node.expression = toDMNReady(node.expression)
        node.expression = unpack(concatWithOr(node.expression))
        logger.debug(f"dnf converted: {node.expression}")
        dmn_ready_tree = tree(node.expression)
        conv = ToFEELConverter()
        conv.visit(dmn_ready_tree)
        node.expression = conv.result
    elif isinstance(node, OperatorDMN):
        logger.debug(f"skip OperatorDMN node {node.operator}")
