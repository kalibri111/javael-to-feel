import functools
import random
import string
from collections import namedtuple
from src.translator.xml_conf import *
from lxml import etree
from src.translator.dmn_tree import DMNTreeNode

DEFAULT_SHAPE_WIDTH = 180
DEFAULT_SHAPE_HEIGHT = 80
RANDOM_ID_LEN = 7
CHILD_CNT_MAX = 5
NODE_HEIGHT_MAX = 10
CENTER_X = 300
CENTER_Y = 300

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
        self.shape = DMNShape(s_x, s_y, s_id)
        self.children = []
        self.height = level

    def append(self, s_id: str):
        # предполагаю, что больше CHILD_CNT_MAX детей у ноды нет, высота дерева не более NODE_HEIGHT_MAX
        new_x = ...
        new_y = ...
        self.children.append(DMNShapeOrdered(s_id, new_x, new_y, self.height + 1))

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


def build_shape_xml(root: DMNShapeOrdered) -> etree.Element:
    """
    Генерация корневых тегов, preorder обход дерева зависимостей DMNShapeOrdered
    :param root: корневой тег DMNShapeOrdered
    :return: корневой тег поддерева XML с правилами отрисовки
    """
    dmndi_tag = etree.Element(etree.QName(dmndi, 'DMNDI'))
    dmn_diagram_tag = etree.Element(etree.QName(dmndi, 'DMNDiagram'))
    dmndi_tag.append(dmn_diagram_tag)

    build_shape_xml_algorithm(root, dmn_diagram_tag)

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
    y_from = shape_from.shape.y - DEFAULT_SHAPE_WIDTH / 2

    x_to = shape_to.shape.x
    y_to = shape_to.shape.y - DEFAULT_SHAPE_WIDTH / 2

    edge_tag = etree.Element(etree.QName(dmndi, 'DMNEdge'), id=edge_id(), dmnElementRef=shape_from.shape.id)
    from_waypoint = etree.Element(etree.QName(dmndi, 'waypoint'), x=x_from, y=y_from)
    to_waypoint = etree.Element(etree.QName(dmndi, 'waypoint'), x=x_to, y=y_to)

    edge_tag.append(from_waypoint)
    edge_tag.append(to_waypoint)

    return edge_tag


def build_shape_xml_algorithm(tree_node: DMNShapeOrdered, dmn_diagram_tag: etree.Element) -> None:
    """
    Обход дерева DMNShapeOrdered, создание тегов для каждой ноды, создание связей между ними
    :param tree_node: корень дерева зависимостей
    :param dmn_diagram_tag: тег - предок всех нод
    :return:
    """
    parent_shape = tree_node.shape_tag()
    dmn_diagram_tag.append(parent_shape)

#     creating all waypoint
    for child in tree_node.children:
        dmn_diagram_tag.append(waypoint_between(parent_shape, child))

    for child in tree_node.children:
        build_shape_xml_algorithm(child, dmn_diagram_tag)
