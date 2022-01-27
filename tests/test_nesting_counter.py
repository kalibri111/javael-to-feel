import unittest
from src.translator.ast_algorithm.javael_ast_algorithm import tree
from src.translator.visitors.javael_visitors import TernaryNodesCollector, NestingCounter


class TestNestingCounter(unittest.TestCase):
    def test_no_ternary(self):
        ast = tree("first and second")
        visitor = TernaryNodesCollector()
        visitor.visit(ast)

        counter = NestingCounter(visitor.result)
        counter.visit(ast)

        self.assertEqual(0, counter.result, "Test not ternary")

    def test_simple_case(self):
        ast = tree("predicate ? value1 : value2")
        visitor = TernaryNodesCollector()
        visitor.visit(ast)

        counter = NestingCounter(visitor.result)
        counter.visit(ast)

        self.assertEqual(1, counter.result, "Test only root ternary")

    def test_complex_case(self):
        ast = tree("predicate1 ? predicate2 ? value1 : value2 : value3")
        visitor = TernaryNodesCollector()
        visitor.visit(ast)

        counter = NestingCounter(visitor.result)
        counter.visit(ast)

        self.assertEqual(2, counter.result, "Test complex ternary")


if __name__ == '__main__':
    unittest.main()
