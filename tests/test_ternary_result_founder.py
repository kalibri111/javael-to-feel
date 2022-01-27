import unittest
from src.translator.ast_algorithm.javael_ast_algorithm import tree
from src.translator.visitors.javael_visitors import TernaryResultFounder, JavaELTreePrinter
from loguru import logger


logger.disable("src")


class TestTernaryResultFounder(unittest.TestCase):
    def test_simple_case(self):
        ast = tree("predicate ? value1 : value2")

        decisions = [True]

        visitor = TernaryResultFounder(decisions)
        visitor.visit(ast)

        printer = JavaELTreePrinter()
        printer.visit(visitor.result)

        self.assertEqual("value1", printer.tree_expression, "Test only root ternary")

    def test_complex_case(self):
        ast = tree("predicate1 ? predicate2 ? value1 or other : value2 : value3")

        decisions = [True, True]

        visitor = TernaryResultFounder(decisions)
        visitor.visit(ast)

        printer = JavaELTreePrinter()
        printer.visit(visitor.result)

        self.assertEqual("value1 or other", printer.tree_expression, "Test only root ternary")


if __name__ == '__main__':
    unittest.main()
