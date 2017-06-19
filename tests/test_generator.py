import unittest

from adrian import cgen


class VarTest(unittest.TestCase):

    def test_it_generated(self):
        inp = [cgen.objects.Var("some_name")]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["some_name"], list(generator.generate()))


class ValTest(unittest.TestCase):

    def test_it_generates_int_fast8(self):
        inp = [cgen.objects.Val(
            "223", type_=cgen.objects.CTypes.int_fast8)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["223"], list(generator.generate()))

    def test_it_generates_int_fast32(self):
        inp = [cgen.objects.Val(
            "223", type_=cgen.objects.CTypes.int_fast32)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["223"], list(generator.generate()))

    def test_it_generates_int_fast64(self):
        inp = [cgen.objects.Val(
            "223", type_=cgen.objects.CTypes.int_fast64)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["223"], list(generator.generate()))

    def test_it_generates_uint_fast8(self):
        inp = [cgen.objects.Val(
            "223", type_=cgen.objects.CTypes.uint_fast8)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["223"], list(generator.generate()))

    def test_it_generates_uint_fast32(self):
        inp = [cgen.objects.Val(
            "223", type_=cgen.objects.CTypes.uint_fast32)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["223"], list(generator.generate()))

    def test_it_generates_uint_fast64(self):
        inp = [cgen.objects.Val(
            "223", type_=cgen.objects.CTypes.uint_fast64)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["223"], list(generator.generate()))

    def test_it_generates_char(self):
        inp = [cgen.objects.Val("a", type_=cgen.objects.CTypes.char)]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertListEqual(["'a'"], list(generator.generate()))

    # def test_it_generates_int_array(self):
    #     inp = [cgen.objects.Val((
    #         cgen.objects.Val("0", type_=cgen.objects.CTypes.int_fast32),
    #         cgen.objects.Val("1", type_=cgen.objects.CTypes.int_fast32)),
    #         type_=cgen.objects.CTypes.array(
    #             cgen.objects.CTypes.int_fast32))
    #     ]
    #     with self.assertRaises(cgen.errors.CheckError) as err:
    #         cgen.check(inp)
    #     self.assertEqual(err.exception.message, cgen.errors._NOT_IMPLEMENTED)
    #     with self.assertRaises(cgen.errors.CheckError) as err:
    #         cgen.generate(inp)
    #     self.assertEqual(err.exception.message, cgen.errors._NOT_IMPLEMENTED)


if __name__ == "__main__":
    unittest.main()
