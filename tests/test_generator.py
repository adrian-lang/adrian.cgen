import unittest

from adrian import cgen


class VarTest(unittest.TestCase):

    def test_it_generates(self):
        inp = [cgen.objects.Var("some_name")]
        self.assertIsNone(cgen.check(inp))
        self.assertListEqual(["some_name"], cgen.generate(inp))


if __name__ == "__main__":
    unittest.main()
