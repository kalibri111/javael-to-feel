from lxml import etree


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OperatorsStorage(dict, metaclass=Singleton):
    pass


class TableToDepTables(dict, metaclass=Singleton):
    """
    id of DMN node to related tables
    """
    pass


class TableToDepInputDatas(dict, metaclass=Singleton):
    """
    id of DMN to related list of InputData
    """
    pass


class InputDataToInfoReq(dict, metaclass=Singleton):
    """
    id of DMN to related InformationRequirements
    """
    def add(self, inputId: str, info_requirement_tag: etree.Element):
        if inputId in super().keys():
            self[inputId].append(info_requirement_tag.attrib['id'])
        else:
            self[inputId] = [info_requirement_tag.attrib['id']]

