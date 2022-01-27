import unittest
import json

from src.document_info_table.report import dictionary_init, substitute_mnemonic, main, generate_report
from src.translator.ast_algorithm.el_expression_to_dmn_tree import translate, xml_from_dmntree
from src.translator.runner import generate_drd

DMN_TEST_OUT_PATH = 'res/out/test_xml_out'
SOURCE_TEST_FILE = 'res/data_samples/Заявка_на_установку_замену_ПУ_522_прод_01_03_2021.xml'
MNEMONICS_PATH = '../src/document_info_table/mnemonics.json'
XSD_PATH = 'res/xsd/dmn.xsd'


class TestIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.java_el_expressions_common = [
            # "empty field",
            # "! field",
            # "!((securityDataProvider.hasRole('tehprisEE_portalUserRegistrator')) or (securityDataProvider.hasRole('tehprisEE_ZayavkaTP')) and empty fields.id)",
            # "!(empty securityDataProvider.loggedInUser or securityDataProvider.hasRole('tehprisEE_portalUserRegistrator') or (securityDataProvider.hasRole('tehprisEE_ZayavkaTP')) or (securityDataProvider.hasRole('tehprisEE_ZayavkaTP')) and empty fields.id)",
            # "fields['p_TypeTP'].Code eq '32896' and fields['p_TimeTPType'].Code eq '32898'",
            # '( securityDataProvider_hasRole_tehprisEE_ZayavkaTP() and dmn4671452832 ) or ( securityDataProvider_hasRole_tehprisEE_ZayavkaTT() ) or ( securityDataProvider_loggedInUser )',
            # "fields_ApplicantType_value_fields_Code eq 'UL' ? 'Юридический адрес' : 'Адрес места регистрации'",
            "!empty fields_isSimpleTPScheme ? fields_isSimpleTPScheme : ((empty fields_id or fields_SendDate > elUtils_toDate) and fields_p_TypeTP_Code eq '32880' and ((fields_ApplicantType_value_fields_Code eq 'FL' and fields_p_TypeOfLoad_value_fields_Code eq '56997' and D_contains_fields_p_ReliabilityCategory_Code and fields_FullPowerD eq 15) or (A_contains_fields_ApplicantType_Code and fields_FullPowerD le 150 ))) ? true : null"
        ]
        # self.xmlschema = etree.XMLSchema(etree.parse(XSD_PATH))

    def test_generate_drd(self):
        for expr in self.java_el_expressions_common:
            # ahocorasic initialization
            with open('../src/document_info_table/mnemonics.json', 'r') as mnemonic_file:
                dict_of_mnemonics = json.load(mnemonic_file)

            suf_automaton = dictionary_init(dict_of_mnemonics)

            expr = substitute_mnemonic(expr, suf_automaton, dict_of_mnemonics)

            generate_drd(expr, DMN_TEST_OUT_PATH)

    def test_generate_report(self):
        generate_report(SOURCE_TEST_FILE, DMN_TEST_OUT_PATH, MNEMONICS_PATH)


if __name__ == '__main__':
    unittest.main()
