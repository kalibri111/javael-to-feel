from src.translator.translate import translate, xml_from_dmntree


def generate_drd(java_el_expression: str, xml_storage_path: str) -> str:
    """
    Main function generates DRD in xml and return absolute path to generated file
    :param java_el_expression:
    :param xml_storage_path:
    :return:
    """
    dmn_tree = translate(java_el_expression)
    return xml_from_dmntree(dmn_tree, xml_storage_path)