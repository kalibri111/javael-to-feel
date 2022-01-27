import unittest
from src.translator.ast_algorithm.javael_ast_algorithm import tree
from src.translator.visitors.javael_visitors import TernaryNodesCollector


class TestTernaryNodesCollector(unittest.TestCase):
    def test_simple_case(self):
        ast = tree("predicate ? value1 : value2")
        counter = TernaryNodesCollector()
        counter.visit(ast)
        self.assertTrue(ast in counter.result, "Test only root ternary")

    def test_complex_case(self):
        ast = tree("predicate1 ? predicate2 ? value1 : value2 : value3")
        counter = TernaryNodesCollector()
        counter.visit(ast)
        self.assertTrue(
            ast in counter.result and ast.getChild(2) in counter.result,
            "Test complex ternary"
        )


if __name__ == '__main__':
    unittest.main()
