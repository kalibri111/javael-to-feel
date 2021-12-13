import queue
import string
import random
import re
import typing

from lxml import etree
from enum import Enum
from collections import namedtuple
from src.translator.dmn_shape import DMNShapeOrdered, DMNShape, CENTER_X, CENTER_Y, build_shape_xml
from src.translator.dmn_tree import DMNTree, DMNTreeNode, OperatorDMN, ExpressionDMN
from src.translator.zip_storage import TableToDepTables, TableToDepInputDatas, InputDataToInfoReq
from src.translator.knf_converter import toDMNReady
from typing import Dict, Iterable, Set, List, Collection
from loguru import logger
from src.translator.feel_analizer import tree, FEELInputExtractor, FEELRuleExtractor, AndSplitter, OrSplitter, \
    ScopesDeleter
from ANTLR_JavaELParser.JavaELParser import JavaELParser
from src.translator.xml_conf import *

RuleTag = namedtuple('RuleTag', ('inputEntries', 'outputEntry'))

logger = logger.opt(colors=True)


class TypeRef(Enum):
    STRING = 1,
    INTEGER = 2


class DmnElementsExtracter:
    AND_OPERANDS_RE = re.compile(r'^and\((.*)\)$')
    WITH_BOOLEAN_METHOD = re.compile(r'^(.+?)\..+?\(\)$')

    @classmethod
    def _getInput(cls, expr: str):
        """
        Suggesting that only one identifier in expression
        :param expr:
        :return:
        """
        feel_expr_tree = tree(expr)
        extractor = FEELInputExtractor()
        extractor.visit(feel_expr_tree)
        if len(extractor.result) > 1:
            raise ValueError(f"Expected only one input in {expr}")

        return extractor.result.pop()

    @classmethod
    def _getOutput(cls, expr: str):
        tokens = expr.split()
        if len(tokens) == 1 and cls.WITH_BOOLEAN_METHOD.findall(tokens[0]) is None:
            return tokens[0]

    @staticmethod
    def _getRule(expr: str):
        """
        operand op value -> op value
        operand.field op value -> op value
        operand.field[] op value-> operand.field[] op value
        operand[val] = null -> operand[val] = null

        :param expr: FEEL expression without logical
        :return:
        """
        expr_tree = tree(expr)
        rule_extr = FEELRuleExtractor()
        rule_extr.visit(expr_tree)
        if rule_extr.result:
            return rule_extr.result
        else:
            return 'information_source'

    @classmethod
    def _split_by_or_by_and(cls, expr: str) -> List[List[str]]:
        """
        (... and ... and ...) or (... and ... and ...) -> [ [and operands]]
        :param expr: {'... and ...',..}
        :return: [[operands], ..]
        """

        # TODO: рекурсивный обход с or
        feel_ast = tree(expr)
        or_splitter = OrSplitter()
        or_splitter.visit(feel_ast)
        or_operands = or_splitter.result

        if not or_operands:
            scopes_deleter = ScopesDeleter()
            scopes_deleter.visit(feel_ast)
            or_operands = scopes_deleter.result

        to_return = []
        for or_op in or_operands:
            or_op_ast = tree(or_op)
            and_splitter = AndSplitter()
            and_splitter.visit(or_op_ast)
            if and_splitter.result:
                to_return.append(and_splitter.result)
            else:
                scopes_deleter = ScopesDeleter()
                scopes_deleter.visit(or_op_ast)
                to_return.append(scopes_deleter.result)
        return to_return

    @classmethod
    def getInputs(cls, expr: str) -> Set[str]:
        """
        :param expr: simple dmn expression
        :return: Set[str]
        """
        feel_expr_tree = tree(expr)
        extractor = FEELInputExtractor()
        extractor.visit(feel_expr_tree)
        return extractor.result

    @classmethod
    def getRulesOrdered(cls, expr: str, inputs) -> Iterable[RuleTag]:
        """
        :param inputs: order of rules
        :param expr:
        :return:
        """
        rules = dict().fromkeys(inputs)
        used_inputs = []
        to_return = []
        is_none_row_needs = False

        for row in cls._split_by_or_by_and(expr):
            output = []

            for cell in row:
                inputName, ruleExpr = cls._getInput(cell), cls._getRule(cell)

                out = cls._getOutput(cell)
                if out:
                    output.append(out)

                used_inputs.append(inputName)

                if rules[inputName]:
                    if ruleExpr == 'boolean' or ruleExpr == 'information_source':
                        if 'true' in rules[inputName]:
                            rules[inputName].append('false')
                        else:
                            rules[inputName].append('true')
                    else:
                        rules[inputName].append(ruleExpr)
                else:
                    if ruleExpr == 'boolean' or ruleExpr == 'information_source':
                        rules[inputName] = ['true']
                    else:
                        rules[inputName] = [ruleExpr]

            # rule of missed input is None
            for key in rules.keys():
                if key not in used_inputs:
                    if rules[key]:
                        rules[key].append(None)
                    else:
                        rules[key] = [None]
            used_inputs.clear()
            # или все outputEntries это rvalue, или все outputEntries это boolean вида:
            # inputEntry, inputEntry, ... : true
            # inputEntry, inputEntry, ... : true
            # ...
            # None      , None      , ... : false
            row_input_entries = []
            for key in inputs:
                # get last rule ordered to inputs arg
                row_input_entries.append(rules[key][-1])

            if len(output) == 1:
                # случай с rvalue
                to_return.append(RuleTag(inputEntries=row_input_entries, outputEntry=output[0]))

            elif len(output) == 0:
                # случай с bool, необходимо добавить строку с None и false
                to_return.append(RuleTag(inputEntries=row_input_entries, outputEntry='true'))
                is_none_row_needs = True
            else:
                raise ValueError('Rule must have only 1 output')

        if is_none_row_needs:
            none_row = []
            for _ in inputs:
                # get last rule ordered to inputs arg
                none_row.append(None)
            to_return.append(RuleTag(inputEntries=none_row, outputEntry='false'))

        return to_return


class DecisionTable:
    RANDOM_ID_LEN = 7
    OPERATION_RESULT_LABEL = 'operation_result'

    @classmethod
    def newInformationRequirement(cls, dependence_href: str) -> etree.Element:
        info_requirement_tag = cls.informationRequirement(cls._constructInformationRequirementId())
        req_input_tag = cls.requiredInput(dependence_href)
        info_requirement_tag.append(req_input_tag)

        InputDataToInfoReq().add(dependence_href.replace('#', ''), info_requirement_tag)

        return info_requirement_tag

    @classmethod
    def newTable(cls, inputs: Collection, output_name: str, rules_rows: Iterable[RuleTag], dependentDMNs: List[str],
                 dmn_id: str, input_data_hrefs: List[str] = None) -> etree.Element:
        decision_tag = cls.decision(cls._constructDecisionId(dmn_id), dmn_id)

        logger.debug(f'DecisionTable from newTable got dependentDMNs: {dependentDMNs}')

        for dependence in dependentDMNs:
            info_requirement_tag = cls.newInformationRequirement(dependence)
            decision_tag.append(info_requirement_tag)

        decisionTable = cls.decisionTable(cls._constructDecisionTableId())
        decision_tag.append(decisionTable)

        # создать связь с InputData
        if input_data_hrefs:
            for input_data_href in input_data_hrefs:
                input_data_info_req_tag = cls.newInformationRequirement(input_data_href)
                decision_tag.append(input_data_info_req_tag)

        # construct input tag branch
        for inputVar in inputs:
            input_tag = cls.input(cls._constructInputId(), inputVar)
            # TODO: TypeRef.STRING всегда?
            input_tag.append(cls.inputExpression(cls._constructInputExpressionId(), TypeRef.STRING, inputVar))

            decisionTable.append(
                input_tag
            )

        # construct output tag
        # TODO: тип output?
        decisionTable.append(
            cls.output(cls._constructOutputId(), output_name, output_name, TypeRef.STRING)
        )

        # construct rule tag branch
        for rulePack in rules_rows:
            rule = cls.rule(cls._constructRuleId())

            for singleInput in rulePack.inputEntries:
                rule.append(cls.inputEntry(cls._constructInputEntryId(), singleInput))

            rule.append(cls.outputEntry(cls._constructOutputId(), rulePack.outputEntry))
            decisionTable.append(rule)
        return decision_tag

    @classmethod
    def from_expression(cls, expression: str, inputs: Set[str], input_data_hrefs: List[str], output_name: str,
                        dependentDMNs: List[str], dmn_id) -> etree.Element:
        logger.debug(f"DecisionTable constructs from expression with dmn_id: {dmn_id}")
        return cls.newTable(
            inputs,
            output_name,
            DmnElementsExtracter.getRulesOrdered(expression, inputs),
            dependentDMNs,
            dmn_id,
            input_data_hrefs
        )

    @classmethod
    def from_constraint(cls, dmn_id: str, operator: int, dependentDMNs: List[str], left_operand, right_operand=None):

        if operator == JavaELParser.Equal:

            return cls._constructEqual(left_operand, right_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.NotEqual:

            return cls._constructNotEqual(left_operand, right_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.Greater:

            return cls._constructGreater(left_operand, right_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.GreaterEqual:

            return cls._constructGreaterEqual(left_operand, right_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.Less:

            return cls._constructLess(left_operand, right_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.LessEqual:

            return cls._constructLessEqual(left_operand, right_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.Not:

            return cls._constructNot(left_operand, dependentDMNs, dmn_id)

        elif operator == JavaELParser.Empty:

            return cls._constructEmpty(left_operand, dependentDMNs, dmn_id)

    @classmethod
    def _constructEqual(cls, left_op: etree.Element, right_op: etree.Element, dependentDMNs: List[str], dmn_id: str):

        logger.debug(
            f'DecisionTable constructs from constraint <green>equal</green>, left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'not( {0} )'.format(left_op.get('id'))),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructNotEqual(cls, left_op, right_op, dependentDMNs: List[str], dmn_id: str):

        logger.debug(
            f'DecisionTable constructs from constraint <green>not equal</green>, left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'not( {0} )'.format(left_op.get('id'))),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructLess(cls, left_op, right_op, dependentDMNs: List[str], dmn_id):

        logger.debug(
            f'DecisionTable constructs from constraint <green>less</green>: left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'< {0}'.format(left_op.get('id'))),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructLessEqual(cls, left_op, right_op, dependentDMNs: List[str], dmn_id):

        logger.debug(
            f'DecisionTable constructs from constraint <green>less equal</green>: left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'<= {0}'.format(left_op.get('id'))),
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='false'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructGreater(cls, left_op, right_op, dependentDMNs: List[str], dmn_id: str):

        logger.debug(
            f'DecisionTable constructs from constraint <green>greater</green>: left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'< {0}'.format(left_op.get('id'))),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructGreaterEqual(cls, left_op, right_op, dependentDMNs: List[str], dmn_id: str):

        logger.debug(
            f'DecisionTable constructs from constraint <green>greater equal</green>: left_op: <red>{left_op}</red>, right_op: <red>{right_op}</red>')

        rules = (
            RuleTag(
                inputEntries=('', f'<= {0}'.format(left_op.get('id'))),
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=('', ''),
                outputEntry='true'
            )
        )
        return cls.newTable(
            (left_op.get('id'), right_op.get('id')),
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructNot(cls, op, dependentDMNs: List[str], dmn_id: str):

        logger.debug(
            f'DecisionTable constructs from constraint <green>not</green>: op: <red>{op}</red>')

        rules = (
            RuleTag(
                inputEntries=['true'],
                outputEntry='false'
            ),
            RuleTag(
                inputEntries=[''],
                outputEntry='true'
            )
        )
        return cls.newTable(
            [dependentDMNs[0]],
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def _constructEmpty(cls, op, dependentDMNs: List[str], dmn_id: str):

        logger.debug(
            f'DecisionTable constructs from constraint <green>empty</green>: op: <red>{op}</red>')

        rules = (
            RuleTag(
                inputEntries=['null'],
                outputEntry='true'
            ),
            RuleTag(
                inputEntries=[''],
                outputEntry='false'
            )
        )
        return cls.newTable(
            [dependentDMNs[0]],
            cls.OPERATION_RESULT_LABEL,
            rules,
            dependentDMNs,
            dmn_id
        )

    @classmethod
    def decision(cls, id_attr: str, name_attr: str):
        return etree.Element('decision', id=id_attr, name=name_attr)

    @staticmethod
    def decisionTable(id_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>decisionTable</green> xml tag, id: <red>{id_attr}</red>')

        return etree.Element('decisionTable', id=id_attr)

    @staticmethod
    def input(id_attr: str, label_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>input</green> xml tag, id: <red>{id_attr}</red>, label: <red>{label_attr}</red>')

        if not label_attr:
            label_attr = ''

        return etree.Element('input', id=id_attr, label=label_attr)

    @staticmethod
    def inputExpression(id_attr: str, typeRef_attr: TypeRef, text_val: str):

        logger.debug(
            f'DecisionTable constructs new <green>inputExpression</green> xml tag, id: <red>{id_attr}</red>, typeRef: <red>{typeRef_attr}</red>, text: <red>{text_val}</red>')

        to_return = None

        if typeRef_attr == TypeRef.STRING:
            to_return = etree.Element('inputExpression', id=id_attr, typeRef='string')
        elif typeRef_attr == TypeRef.INTEGER:
            to_return = etree.Element('inputExpression', id=id_attr, typeRef='integer')

        to_return.append(DecisionTable.text(text_val))
        return to_return

    @staticmethod
    def output(id_attr: str, label_attr: str, name_attr: str, typeRef_attr: TypeRef):

        logger.debug(
            f'DecisionTable constructs new <green>output</green> xml tag, id: <red>{id_attr}</red>, typeRef: <red>{typeRef_attr}</red>, label: <red>{label_attr}</red>, name: <red>{name_attr}</red>')

        if typeRef_attr == TypeRef.STRING:
            return etree.Element('output', id=id_attr, label=label_attr, name=name_attr, typeRef='string')
        elif typeRef_attr == TypeRef.INTEGER:
            return etree.Element('output', id=id_attr, label=label_attr, name=name_attr, typeRef='integer')

    @staticmethod
    def rule(id_attr: str, description_tag_text: str = None):

        logger.debug(
            f'DecisionTable constructs new <green>rule</green> xml tag, id: <red>{id_attr}</red>, description: <red>{description_tag_text}</red>')

        to_return = etree.Element('rule', id=id_attr)

        description = etree.Element('description')
        description.text = description_tag_text

        to_return.append(description)
        return to_return

    @staticmethod
    def text(text_value):

        to_return = etree.Element('text')
        to_return.text = text_value
        return to_return

    @staticmethod
    def inputEntry(id_attr: str, text_val: str):
        logger.debug(
            f'DecisionTable constructs new <green>inputEntry</green> xml tag, id: <red>{id_attr}</red>, text: <red>{text_val}</red>')

        if not text_val:
            text_val = ''

        to_return = etree.Element('inputEntry', id=id_attr)
        to_return.append(DecisionTable.text(text_val))
        return to_return

    @staticmethod
    def outputEntry(id_attr: str, text_val: str):

        if not text_val:
            text_val = ''

        logger.debug(
            f'DecisionTable constructs new <green>outputEntry</green> xml tag, id: <red>{id_attr}</red>, text: <red>{text_val}</red>')

        to_return = etree.Element('outputEntry', id=id_attr)
        to_return.append(DecisionTable.text(text_val))
        return to_return

    @staticmethod
    def informationRequirement(id_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>informationRequirement</green> xml tag, id: <red>{id_attr}</red>')

        return etree.Element('informationRequirement', id=id_attr)

    @staticmethod
    def requiredInput(href_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>requiredInput</green> xml tag, href: <red>{href_attr}</red>')

        return etree.Element('requiredInput', href=href_attr)

    @staticmethod
    def requiredDecision(href_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>requiredDecision</green> xml tag, href: <red>{href_attr}</red>')

        return etree.Element('requiredDecision', href=href_attr)

    @staticmethod
    def authorityRequirement(id_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>authorityRequirement</green> xml tag, id: <red>{id_attr}</red>')

        return etree.Element('authorityRequirement', id=id_attr)

    @staticmethod
    def requiredAuthority(href_attr: str):
        logger.debug(
            f'DecisionTable constructs new <green>requiredAuthority</green> xml tag, href: <red>{href_attr}</red>')

        return etree.Element('requiredAuthority', href=href_attr)

    @staticmethod
    def definitions(id_attr: str, name_attr: str):
        pass

    @staticmethod
    def _constructDecisionTableId():
        return 'DecisionTable_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInputId():
        return 'Input_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInputExpressionId():
        return 'InputExpression_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructOutputId():
        return 'Output_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructRuleId():
        return 'DecisionRule_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructInputEntryId():
        return 'UnaryTest_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructOutputEntryId():
        return 'LiteralExpression_' + DecisionTable._constructIdSuffix()

    @staticmethod
    def _constructIdSuffix() -> str:
        return ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(DecisionTable.RANDOM_ID_LEN)
        )

    @staticmethod
    def _constructDecisionId(dmn_id: str) -> str:
        new_id = 'Decision_' + DecisionTable._constructIdSuffix()

        TableToDepTables()[dmn_id] = new_id
        return new_id

    @staticmethod
    def _constructInformationRequirementId() -> str:
        return 'InformationRequirement_' + DecisionTable._constructIdSuffix()


class InputData:
    def __init__(self, name_attr: str):
        self._tag_id = self._id()
        logger.debug(f"InputData creates: id: {self._tag_id}, name: {name_attr}")
        self._tag_name = name_attr

    def xml_tag(self):
        return etree.Element('inputData', id=self._tag_id, name=self._tag_name)

    def dmn_shape(self):
        return

    def _id(self):
        return "InputData_" + ''.join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(DecisionTable.RANDOM_ID_LEN)
        )

    @property
    def tag_id(self):
        return self._tag_id

    @property
    def href(self):
        return '#' + self._tag_id


class ShapesDrawer:
    @classmethod
    def draw(cls, tree: DMNTree) -> etree.Element:
        shape_ordered_root = cls.extract_dependency(tree.root)
        shape_tag = build_shape_xml(shape_ordered_root)
        return shape_tag

    @classmethod
    def related_tags(cls, node: DMNTreeNode) -> List[etree.Element]:
        """
        Returns [node_tag_xml_id, ...(other related)]
        :param node:
        :return:
        """
        if isinstance(node, ExpressionDMN):
            return [TableToDepTables()['dmn' + str(id(c))] for c in node.children]
        elif isinstance(node, OperatorDMN):
            dependents = []

            # все зависимые dmn диаграммы
            for c in node.children:
                if 'dmn' + str(id(c)) in TableToDepTables().keys():
                    dependents.append(TableToDepTables()['dmn' + str(id(c))])
            # все зависимые inputData
            for c in node.children:
                if 'dmn' + str(id(c)) in TableToDepInputDatas().keys():
                    dependents.extend(
                        [
                            i.tag_id for i in TableToDepInputDatas()['dmn' + str(id(c))]
                        ]
                    )
            return dependents

    @classmethod
    def extract_dependency(cls, root: DMNTreeNode) -> DMNShapeOrdered:
        """
        BFS c двумя очередями
        :param decisions:
        :param root:
        :param shape_node:
        :return:
        """
        dmn_nodes_queue = queue.Queue()
        shape_nodes_queue = queue.Queue()

        shape_root_tag = cls.related_tags(root)

        # only one DMN table in expression
        if len(shape_root_tag) == 0:
            return DMNShapeOrdered(TableToDepTables()['dmn' + str(id(root))], CENTER_X, CENTER_Y, 0)

        if len(shape_root_tag) > 1:
            raise ValueError(f'ShapesDrawer.draw wrong root count to initialize: {len(shape_root_tag)}')

        shape_root = DMNShapeOrdered(shape_root_tag[0], CENTER_X, CENTER_Y, 0)

        for c in root.children:
            dmn_nodes_queue.put(c)

        shape_nodes_queue.put(shape_root)

        while not dmn_nodes_queue.empty():
            dmn_tag = dmn_nodes_queue.get()

            shape_children = cls.related_tags(dmn_tag)
            shape_parent = shape_nodes_queue.get()

            for c in shape_children:
                shape_parent.append(c)

            for c in shape_parent.children:
                shape_nodes_queue.put(c)

            for d in dmn_tag.children:
                dmn_nodes_queue.put(d)
        return shape_root


class DMN_XML:
    @classmethod
    def build_xml(cls, drd_id: str, decisions: List[etree.Element]):
        NSMAP = {'dmndi': dmndi, 'dc': dc, 'biodi': biodi, 'di': di, }
        root = etree.Element('definitions', xmlns=xmlns, nsmap=NSMAP)
        attributes = root.attrib
        attributes['name'] = 'DRD'
        attributes['namespace'] = namespace
        attributes['exporter'] = exporter
        attributes['exporterVersion'] = exporterVersion

        for d in decisions:
            if d.tag == 'decision':
                root.append(d)

        input_data_values = []

        for i in TableToDepInputDatas().values():
            input_data_values.extend(i)

        for input_data in set(input_data_values):
            input_data_tag = input_data.xml_tag()
            root.append(input_data_tag)

        return root

    @classmethod
    def visit(cls, tree: DMNTree) -> etree.Element:
        """
        DFS на возврате
        :return:
        """
        root = tree.root
        decisions = []
        cls.inorder_travers(root, decisions)
        return cls.build_xml('drd_id', decisions)

    @classmethod
    def inorder_travers(cls, node: DMNTreeNode, decisions: List[etree.Element]):
        if len(node.children):
            for child in node.children:
                cls.inorder_travers(child, decisions)

        # constraint dmn node
        if isinstance(node, OperatorDMN):
            DMNTreeVisitor.visit_constraint(node, decisions)
        elif isinstance(node, ExpressionDMN):
            # expression node
            DMNTreeVisitor.visit_expression(node, decisions)
        else:
            raise ValueError('XML builder got wrong DMN node type')


class DMNTreeVisitor:
    @classmethod
    def visit_expression(cls, node: ExpressionDMN, decision_list: List[etree.Element]) -> None:
        logger.debug(f'DMNTreeVisitor constructs xml from <red>expression</red>: <green>{node.expression}</green>')

        # dependents = ['#' + DependenceStorage()['dmn' + str(id(c))] for c in node.children]
        dependents = []

        # все зависимые dmn диаграммы
        for c in node.children:
            if 'dmn' + str(id(c)) in TableToDepTables().keys():
                dependents.append(TableToDepTables()['dmn' + str(id(c))])
        # все зависимые inputData
        for c in node.children:
            if 'dmn' + str(id(c)) in TableToDepInputDatas().keys():
                dependents.append(TableToDepInputDatas()['dmn' + str(id(c))].href())

        logger.debug(f'DMNTreeVisitor from visit_expression found dependencies: {dependents}')

        self_id = 'dmn' + str(id(node))

        inputs = set()
        input_data_hrefs = []

        input_data_tags = []

        for input_data_candidate in DmnElementsExtracter.getInputs(node.expression):
            if input_data_candidate not in TableToDepInputDatas():
                if 'dmn' not in input_data_candidate:
                    new_input_data = InputData(input_data_candidate)

                    if self_id not in TableToDepInputDatas().keys():
                        TableToDepInputDatas()[self_id] = [new_input_data]
                    else:
                        TableToDepInputDatas()[self_id].append(new_input_data)

                    input_data_hrefs.append(new_input_data.href)
                    input_data_tags.append(new_input_data)
            # else:
            inputs.add(input_data_candidate)

        if inputs:
            new_table = DecisionTable.from_expression(node.expression, inputs, input_data_hrefs, 'output_name here',
                                                      dependents, self_id)

            if new_table is None:
                logger.error(
                    f'DMNTreeVisitor constructs xml from <red>expression</red>: <green>{node.expression}</green> failure')
                raise ValueError('DecisionTable is None')

            logger.debug(f'GENERATED XML FROM EXPRESSION')
            logger.debug(f'Expression: <red>{node.expression}</red>')
            logger.opt(colors=False).debug(f'\n{etree.tostring(new_table, pretty_print=True).decode("UTF-8")}')
            decision_list.append(new_table)
        else:
            logger.debug(f'DMN_XML constructs inputData tags: {input_data_hrefs}')
            # добавление inputData объекта в decision_list, предполагаю, что они тут единственные операнды
            for input_data in input_data_tags:
                decision_list.append(input_data.xml_tag())

    @classmethod
    def visit_constraint(cls, node: OperatorDMN, decision_list: List[etree.Element]) -> None:
        logger.debug(f'DMNTreeVisitor constructs xml from <red>constraint</red>: <green>{node.operator}</green>')

        dependents = []

        # все зависимые dmn диаграммы
        for c in node.children:
            if 'dmn' + str(id(c)) in TableToDepTables().keys():
                dependents.append(TableToDepTables()['dmn' + str(id(c))])
        # все зависимые inputData
        for c in node.children:
            if 'dmn' + str(id(c)) in TableToDepInputDatas().keys():
                dependents.extend([i.href for i in TableToDepInputDatas()['dmn' + str(id(c))]])

        logger.debug(f'DMNTreeVisitor from visit_constraint found dependencies: {dependents}')

        self_id = 'dmn' + str(id(node))

        new_table = None
        if node.operator.symbol.type in [JavaELParser.Empty, JavaELParser.Not]:
            new_table = DecisionTable.from_constraint(self_id, node.operator.symbol.type, dependents, decision_list[-1])

            if new_table is None:
                logger.error(
                    f'DMNTreeVisitor constructs xml from <red>constraint</red>: <green>{node.operator}</green> failure')
                raise ValueError('DecisionTable is None')

            decision_list.append(new_table)
        else:
            left_op = decision_list[-2]
            right_op = decision_list[-1]

            new_table = DecisionTable.from_constraint(self_id, node.operator, dependents, left_op, right_op)

            if new_table is None:
                logger.error(
                    f'DMNTreeVisitor constructs xml from <red>constraint</red>: <green>{node.operator}</green> failure')
                raise ValueError('DecisionTable is None')

            decision_list.append(new_table)

        logger.debug(f'GENERATED XML FROM CONSTRAINT')
        logger.debug(f'Constraint: <red>{node.operator}</red>')
        logger.opt(colors=False).debug(f'\n{etree.tostring(new_table, pretty_print=True).decode("UTF-8")}')


def dmn_shape(coord_x: int, coord_y: int, element_id: str):
    tag = etree.Element(etree.QName(dmndi, 'DMNShape'), dmnElementRef=element_id)
    bound = etree.SubElement(tag, etree.QName(dc, 'Bounds'), height='80', width='180', x=str(coord_x), y=str(coord_y))
    return tag
