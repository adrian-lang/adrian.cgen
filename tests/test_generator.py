import unittest

from adrian import cgen


class VarTest(unittest.TestCase):

    def test_it_generates(self):
        inp = [cgen.objects.Var("some_name")]
        self.assertIsNone(cgen.check(inp))
        self.assertListEqual(["some_name"], cgen.generate(inp))


class ValTest(unittest.TestCase):

    def test_it_generates_int32(self):
        inp = [cgen.objects.Val("223", type_=cgen.objects.CTypes.int32)]
        self.assertIsNone(cgen.check(inp))
        self.assertListEqual(["223"], cgen.generate(inp))

    def test_it_generates_int64(self):
        inp = [cgen.objects.Val("223", type_=cgen.objects.CTypes.int64)]
        self.assertIsNone(cgen.check(inp))
        self.assertListEqual(["223"], cgen.generate(inp))

    def test_it_generates_char(self):
        inp = [cgen.objects.Val("a", type_=cgen.objects.CTypes.char)]
        self.assertIsNone(cgen.check(inp))
        self.assertListEqual(["'a'"], cgen.generate(inp))

    def test_it_generates_int_array(self):
        inp = [cgen.objects.Val((
            cgen.objects.Val("0", type_=cgen.objects.CTypes.int32),
            cgen.objects.Val("1", type_=cgen.objects.CTypes.int32)),
            type_=cgen.objects.CTypes.array(cgen.objects.CTypes.int32))
        ]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(err.exception.message, cgen.errors._NOT_IMPLEMENTED)
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.generate(inp)
        self.assertEqual(err.exception.message, cgen.errors._NOT_IMPLEMENTED)


if __name__ == "__main__":
    unittest.main()
