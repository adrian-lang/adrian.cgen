import unittest

from adrian.cgen import Generator


class CgenTestCase(unittest.TestCase):

    def check_gen(self, asts, expected_lines):
        gen = Generator()
        for ast in asts:
            gen.add_ast(ast)
        self.assertEqual(
            "\n".join(expected_lines),
            "\n".join(gen.generate()))
