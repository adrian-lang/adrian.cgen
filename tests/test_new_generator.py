import unittest

from adrian import cgen


class VarTest(unittest.TestCase):

    def test_it_generated(self):
        inp = [cgen.objects.Var("some_name")]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["some_name"], list(generator.generate()))

if __name__ == "__main__":
    unittest.main()
