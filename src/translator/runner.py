from lxml import etree

from src.translator.ast_algorithm.el_expression_to_dmn_tree import translate, xml_from_dmntree, element_from_dmntree
from src.translator.ast_algorithm.javael_ast_algorithm import tree
from src.translator.xml.xml_packer import DMN_XML, DecisionTable, TagIdGenerator, TypeRef
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from src.translator.visitors.javael_visitors import TernaryNodesCollector, NestingCounter, TernaryResultFounder, \
    JavaELTreePrinter
from loguru import logger

logger.opt(colors=True)


def _generate_common_drd(java_el_expression: str, xml_storage_path: str) -> str:
    """
    Generate DRD from not pure ternary expression
    :param java_el_expression:
    :param xml_storage_path:
    :return:
    """
    dmn_tree = translate(java_el_expression)
    return xml_from_dmntree(dmn_tree, xml_storage_path)


def _generate_ternary_filename(directory: str, seed: str) -> str:
    """
    Generate name of xml represented pure ternary expression
    :param directory: directory file will create
    :param seed: unique part
    :return: filepath
    """
    return directory + '_ternary_' + str(id(seed)) + '.xml'


def _generate_ternary_drd(java_el_ast: JavaELParser.ExpressionContext, xml_storage_path: str, nesting: int) -> str:
    """
    Generate DRD from pure (recursively defined) ternary expression
    :param nesting: number of nesting ternaries
    :param java_el_ast:
    :param xml_storage_path:
    :return:
    """
    p = JavaELTreePrinter()
    p.visit(java_el_ast)
    logger.debug(f"Generating ternary from {p.tree_expression}")
    doc_root = DMN_XML.xml_header()
    rows_cnt = 2**nesting

    root_decision = DecisionTable.decisionTable(TagIdGenerator.DecisionTableId())

    # prepare dependents expressions translate + element_from_dmntree
    ternaries = TernaryNodesCollector()
    ternaries.visit(java_el_ast)

    printer = JavaELTreePrinter()

    # create branches for inputs
    for input_expr in ternaries.result:
        predicate = input_expr.getChild(0)
        printer.visit(predicate)
        predicate_text = printer.tree_expression
        input_dmn_tree = translate(predicate_text)
        input_xml_branch = element_from_dmntree(input_dmn_tree, draw=False)[0]  # decision tag
        logger.debug(etree.tostring(input_xml_branch, pretty_print=True).decode('UTF-8'))
        doc_root.append(input_xml_branch)

        input_tag = DecisionTable.input(TagIdGenerator.InputId(), input_xml_branch.attrib['id'])
        input_tag.append(
            DecisionTable.inputExpression(
                TagIdGenerator.InputExpressionId(),
                TypeRef.STRING,
                input_xml_branch.attrib['id']  # input - inputExpression ??
            )
        )

        root_decision.append(input_xml_branch)
        root_decision.append(input_tag)

    # create true/false permutations
    perm_mask = 0
    for r_idx in range(rows_cnt):
        r_rule_id = TagIdGenerator.RuleId()
        r_rule = DecisionTable.rule(r_rule_id)

        state_path = []

        for c_idx in range(nesting):
            perm_val = perm_mask & (1 << c_idx)  # get particular byte
            state_path.append(perm_val == 1)
            perm_val_str = 'true' if perm_val == 1 else 'false'

            inp_id = TagIdGenerator.InputEntryId()
            c_input = DecisionTable.inputEntry(inp_id, perm_val_str)
            r_rule.append(c_input)

        result_founder = TernaryResultFounder(state_path)
        result_founder.visit(java_el_ast)
        result_expr = result_founder.result

        printer.visit(result_expr)

        result_dmn_tree = translate(printer.tree_expression)
        result_xml_branch = element_from_dmntree(result_dmn_tree, draw=False)

        r_rule.append(result_xml_branch)

        root_decision.append(r_rule)
        perm_mask += 1

    # TODO: seed can be more stable?
    to_return_fpath = _generate_ternary_filename(xml_storage_path, str(id(doc_root)))
    return etree.ElementTree(doc_root).write(to_return_fpath, pretty_print=True)


def generate_drd(java_el_expression: str, xml_storage_path: str) -> str:
    """
    Main function generates DRD in xml and return absolute path to generated file
    :param java_el_expression: valid el expression
    :param xml_storage_path: path to create XML file
    :return:
    """
    ast = tree(java_el_expression)

    counter = TernaryNodesCollector()
    counter.visit(ast)

    nesting_nodes_cntr = NestingCounter(counter.result)
    nesting_nodes_cntr.visit(ast)

    if nesting_nodes_cntr.result > 0:
        return _generate_ternary_drd(ast, xml_storage_path, nesting_nodes_cntr.result)
    else:
        return _generate_common_drd(java_el_expression, xml_storage_path)
