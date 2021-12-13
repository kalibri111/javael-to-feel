import unittest
from src.translator.translate import translate, xml_from_dmntree

XML_TEST_OUT_PATH = 'res/out/test_xml_out'
XSD_PATH = 'res/xsd/dmn.xsd'


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.java_el_expressions = [
            # "empty field",
            # "! field",
            # "!((securityDataProvider.hasRole('tehprisEE_portalUserRegistrator')) or (securityDataProvider.hasRole('tehprisEE_ZayavkaTP')) and empty fields.id)",
            # "fields['p_TypeTP'].Code eq '32896' and fields['p_TimeTPType'].Code eq '32898'",
            '( securityDataProvider_hasRole_tehprisEE_ZayavkaTP and dmn4671452832 ) or ( securityDataProvider.hasRole("tehprisEE_portalUserRegistrator") ) or ( securityDataProvider.loggedInUser )',
        ]
        # self.xmlschema = etree.XMLSchema(etree.parse(XSD_PATH))

    def test_integration(self):
        for expr in self.java_el_expressions:
            dmn_tree = translate(expr)
            xml_from_dmntree(dmn_tree, XML_TEST_OUT_PATH)
            # self.assertTrue(self.xmlschema.validate(etree.parse(XML_TEST_OUT_PATH)))


if __name__ == '__main__':
    unittest.main()
