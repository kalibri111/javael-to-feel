import unittest
from src.translator.runner import generate_drd

SIMPLE_TERNARY_EXPRESSION = "fields_ApplicantType_value_fields_Code eq 'UL' ? 'Юридический адрес' : 'Адрес места регистрации'"


class TestGenerateTernary(unittest.TestCase):
    def test_generate_simple(self):
        generate_drd(SIMPLE_TERNARY_EXPRESSION, '../out')


if __name__ == '__main__':
    unittest.main()
