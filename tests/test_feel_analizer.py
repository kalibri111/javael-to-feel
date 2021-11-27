import unittest
from src.translator.feel_analizer import FEELInputExtractor, tree


class TestFEELInputExtractor(unittest.TestCase):
    def test_complex_input(self):
        test_expression = "securityDataProvider.hasRole(\"tehprisEE_ZayavkaTP\") and dmn4987271104"
        feel_tree = tree(test_expression)
        visitor = FEELInputExtractor()
        visitor.visit(feel_tree)
        self.assertEqual('securityDataProvider_hasRole _"tehprisEE_portalUserRegistrator"_', visitor.result.pop())


if __name__ == '__main__':
    unittest.main()
