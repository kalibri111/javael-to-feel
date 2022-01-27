import unittest
import json
from src.document_info_table.report import dictionary_init, substitute_mnemonic


class TestSubstitution(unittest.TestCase):
    def testExist(self):
        expr = "fields['p_TypeTP'].Code eq '32896' and fields['p_TimeTPType'].Code eq '32898'"
        with open('../src/document_info_table/mnemonics.json', 'r') as file:
            d = json.load(file)
        automaton = dictionary_init(d)
        substituted = substitute_mnemonic(expr, automaton, d)
        self.assertEqual(substituted, "fieldsAtp_Type_Code eq '32896' and fields['p_TimeTPType'].Code eq '32898'")


if __name__ == '__main__':
    unittest.main()
