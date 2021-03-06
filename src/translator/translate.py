from lxml import etree

from src.translator.treeFormula import tree, DMNTree, translateDMNReadyinDMNTree, DMN_XML, printDMNTree, \
    SyntaxTreePrinter
from loguru import logger


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
    # stp = SyntaxTreePrinter()
    # stp.visit(el_tree)
    # logger.opt(colors=True).debug(f'<green>{stp.tree_expression}</green>')
    # logger.debug('---------------------------')
    translateDMNReadyinDMNTree(dmn_tree)
    logger.debug('Translated DMN tree')
    printDMNTree(dmn_tree)
    logger.debug('---------------------------')
    return dmn_tree


def xml_from_dmntree(dmn_tree_translated: DMNTree, xml_out_path: str) -> None:
    """
    Builds xml representation of DMN structure
    :param dmn_tree_translated: represents FEEL expressions, connected by non-logical operators
    :param xml_out_path: path where to build xml
    :return: None
    """
    dmn_xml_root = DMN_XML().visit(dmn_tree_translated)

    etree.ElementTree(dmn_xml_root).write(xml_out_path + str(id(dmn_tree_translated)) + '.xml', pretty_print=True)
    # with open(xml_out_path, 'w') as xml_out:
    #     xml_out.write(etree.tostring(dmn_xml_root, pretty_print=True))
