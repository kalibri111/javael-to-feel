import functools
import random
import string
from collections import namedtuple
from src.translator.xml.xml_conf import *
from lxml import etree
from loguru import logger

from src.translator.singleton.singleton_storage import InputDataToInfoReq

logger.opt(colors=True)

DEFAULT_SHAPE_WIDTH = 180
DEFAULT_SHAPE_HEIGHT = 80
RANDOM_ID_LEN = 7
CHILD_CNT_MAX = 5
TREE_HEIGHT_MAX = 10
CENTER_X = 300
CENTER_Y = 300

Y_STEP = 50
X_STEP = 50

WIDTH_SUMMARY = 1000

DMNWaypoint = namedtuple("DMNWaypoint", ('x', 'y'))


class DMNShape:
    def __init__(self, x: int, y: int, element_id: str):
        self.x = x
        self.y = y
        self.id = element_id

    @functools.cached_property
    def waypoint(self):
        return DMNWaypoint(x=self.x, y=self.y - DEFAULT_SHAPE_WIDTH / 2)


class DMNShapeOrdered:
    def __init__(self, s_id: str, s_x: int, s_y: int, level: int):
        logger.debug(f'Constructor DMNShapeOrdered called with params: [id: {s_id}, x: {s_x}, y:{s_y}, level: {level}]')
        self.shape = DMNShape(s_x, s_y, s_id)
        self._children = []
        self.tree_height = level

    def append(self, s_id: str):
        # предполагаю, что больше CHILD_CNT_MAX детей у ноды нет, высота дерева не более NODE_HEIGHT_MAX
        new_x = self.shape.x
        if len(self._children):
            new_x = self._children[-1].shape.x + 50 + DEFAULT_SHAPE_WIDTH
        new_y = self.shape.y + DEFAULT_SHAPE_HEIGHT + Y_STEP
        self._children.append(DMNShapeOrdered(s_id, new_x, new_y, self.tree_height + 1))

    @property
    def shape_tag(self):
        tag = etree.Element(etree.QName(dmndi, 'DMNShape'), dmnElementRef=self.shape.id)
        bound = etree.SubElement(
            tag,
            etree.QName(dc, 'Bounds'),
            height='80',
            width='180',
            x=str(self.shape.x),
            y=str(self.shape.y)
        )
        return tag

    @property
    def children(self):
        return self._children


def build_shape_xml(root: DMNShapeOrdered) -> etree.Element:
    """
    Генерация корневых тегов, preorder обход дерева зависимостей DMNShapeOrdered
    :param root: корневой тег DMNShapeOrdered
    :return: корневой тег поддерева XML с правилами отрисовки
    """
    logger.debug(f'build_shape_xml starts')
    dmndi_tag = etree.Element(etree.QName(dmndi, 'DMNDI'))
    dmn_diagram_tag = etree.Element(etree.QName(dmndi, 'DMNDiagram'))
    dmndi_tag.append(dmn_diagram_tag)

    build_shape_xml_algorithm(root, dmn_diagram_tag)

    logger.debug(f'build_shape_xml successfully')
    return dmndi_tag


def edge_id():
    return 'DMNEdge_' + ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(RANDOM_ID_LEN)
    )


def waypoint_between(shape_from: DMNShapeOrdered, shape_to: DMNShapeOrdered) -> etree.Element:
    """
    Стрелочка между DMNShapeOrdered
    :param shape_from: зависимая нода
    :param shape_to: главная нода
    :return:
    """
    x_from = shape_from.shape.x
    y_from = shape_from.shape.y

    x_to = shape_to.shape.x
    y_to = shape_to.shape.y

    edge_tag = etree.Element(etree.QName(dmndi, 'DMNEdge'), id=edge_id(),
                             dmnElementRef=InputDataToInfoReq()[shape_to.shape.id][0])

    from_waypoint = etree.Element(etree.QName(di, 'waypoint'), x=str(x_from), y=str(y_from))
    to_waypoint = etree.Element(etree.QName(di, 'waypoint'), x=str(x_to), y=str(y_to))

    edge_tag.append(to_waypoint)  # be careful, this first
    edge_tag.append(from_waypoint)  # be careful, this second

    return edge_tag


def build_shape_xml_algorithm(tree_node: DMNShapeOrdered, dmn_diagram_tag: etree.Element) -> None:
    """
    Обход дерева DMNShapeOrdered, создание тегов для каждой ноды, создание связей между ними
    :param tree_node: корень дерева зависимостей
    :param dmn_diagram_tag: тег - предок всех нод
    :return:
    """
    parent_shape = tree_node.shape_tag
    dmn_diagram_tag.append(parent_shape)

    #     creating all waypoint
    for child in tree_node.children:
        logger.debug(f'adding waypoint {tree_node.shape.id} -- {child.shape.id}')
        dmn_diagram_tag.append(waypoint_between(tree_node, child))

    for child in tree_node.children:
        build_shape_xml_algorithm(child, dmn_diagram_tag)
