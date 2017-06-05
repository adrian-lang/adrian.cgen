import unittest

from adrian import cgen


class VarTest(unittest.TestCase):

    def test_lowercase_name(self):
        inp = [cgen.objects.Var("lcname")]
        self.assertIsNone(cgen.check(inp))

    def test_uppercase_name(self):
        inp = [cgen.objects.Var("UCNAME")]
        self.assertIsNone(cgen.check(inp))

    def test_camelcase_name(self):
        inp = [cgen.objects.Var("CamelCaseName")]
        self.assertIsNone(cgen.check(inp))

    def test_underscore_name(self):
        inp = [cgen.objects.Var("_")]
        self.assertIsNone(cgen.check(inp))

    def test_underscore_and_digits_name(self):
        inp = [cgen.objects.Var("_123")]
        self.assertIsNone(cgen.check(inp))

    def test_mixed_name(self):
        inp = [cgen.objects.Var("fOO_bAr_123")]
        self.assertIsNone(cgen.check(inp))

    def test_while_name(self):
        inp = [cgen.objects.Var("while")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_NAME.format_map({"name": "while"}))

    def test_digit_and_letters_name(self):
        inp = [cgen.objects.Var("2foo")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_NAME.format_map({"name": "2foo"}))

    def test_letters_space_letters_name(self):
        inp = [cgen.objects.Var("my foo")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_NAME.format_map({"name": "my foo"}))

    def test_specsymb_and_letters_name(self):
        inp = [cgen.objects.Var("$Foo")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_NAME.format_map({"name": "$Foo"}))

    def test_int_name(self):
        inp = [cgen.objects.Var("int")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_NAME.format_map({"name": "int"}))


class ValIntFast8Test(unittest.TestCase):

    def test_int_fast8_number(self):
        inp = [cgen.objects.Val(
            "200", type_=cgen.objects.CTypes.int_fast8)]
        self.assertIsNone(cgen.check(inp))

    def test_int_fast8_number_starts_with_zero(self):
        inp = [cgen.objects.Val(
            "0123", type_=cgen.objects.CTypes.int_fast8)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "0123"
            }))

    def test_int_fast8_number_zero(self):
        inp = [cgen.objects.Val(
            "0", type_=cgen.objects.CTypes.int_fast8)]
        self.assertIsNone(cgen.check(inp))

    def test_int_fast8_some_string(self):
        inp = [cgen.objects.Val(
            "some_string_here123",
            type_=cgen.objects.CTypes.int_fast8)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string_here123"
            }))


class ValUIntFast8Test(unittest.TestCase):

    def test_uint_fast8_number(self):
        inp = [cgen.objects.Val(
            "200", type_=cgen.objects.CTypes.uint_fast8)]
        self.assertIsNone(cgen.check(inp))

    def test_uint_fast8_number_starts_with_zero(self):
        inp = [cgen.objects.Val(
            "0123", type_=cgen.objects.CTypes.uint_fast8)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "0123"
            }))

    def test_uint_fast8_number_zero(self):
        inp = [cgen.objects.Val(
            "0", type_=cgen.objects.CTypes.uint_fast8)]
        self.assertIsNone(cgen.check(inp))

    def test_uint_fast8_some_string(self):
        inp = [cgen.objects.Val(
            "some_string_here123",
            type_=cgen.objects.CTypes.uint_fast8)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string_here123"
            }))


class ValIntFast32Test(unittest.TestCase):

    def test_int_fast32_number(self):
        inp = [cgen.objects.Val(
            "200", type_=cgen.objects.CTypes.int_fast32)]
        self.assertIsNone(cgen.check(inp))

    def test_int_fast32_number_starts_with_zero(self):
        inp = [cgen.objects.Val(
            "0123", type_=cgen.objects.CTypes.int_fast32)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "0123"
            }))

    def test_int_fast32_number_zero(self):
        inp = [cgen.objects.Val(
            "0", type_=cgen.objects.CTypes.int_fast32)]
        self.assertIsNone(cgen.check(inp))

    def test_int_fast32_some_string(self):
        inp = [cgen.objects.Val(
            "some_string_here123",
            type_=cgen.objects.CTypes.int_fast32)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string_here123"
            }))


class ValUIntFast32Test(unittest.TestCase):

    def test_uint_fast32_number(self):
        inp = [cgen.objects.Val(
            "200", type_=cgen.objects.CTypes.uint_fast32)]
        self.assertIsNone(cgen.check(inp))

    def test_uint_fast32_number_starts_with_zero(self):
        inp = [cgen.objects.Val(
            "0123", type_=cgen.objects.CTypes.uint_fast32)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "0123"
            }))

    def test_uint_fast32_number_zero(self):
        inp = [cgen.objects.Val(
            "0", type_=cgen.objects.CTypes.uint_fast32)]
        self.assertIsNone(cgen.check(inp))

    def test_uint_fast32_some_string(self):
        inp = [cgen.objects.Val(
            "some_string_here123",
            type_=cgen.objects.CTypes.uint_fast32)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string_here123"
            }))


class ValIntFast64Test(unittest.TestCase):

    def test_int_fast64_number(self):
        inp = [cgen.objects.Val(
            "200", type_=cgen.objects.CTypes.int_fast8)]
        self.assertIsNone(cgen.check(inp))

    def test_int_fast64_number_starts_with_zero(self):
        inp = [cgen.objects.Val(
            "0123", type_=cgen.objects.CTypes.int_fast64)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "0123"
            }))

    def test_int_fast64_number_zero(self):
        inp = [cgen.objects.Val(
            "0", type_=cgen.objects.CTypes.int_fast64)]
        self.assertIsNone(cgen.check(inp))

    def test_int_fast64_some_string(self):
        inp = [cgen.objects.Val(
            "some_string_here123",
            type_=cgen.objects.CTypes.int_fast64)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string_here123"
            }))


class ValUIntFast64Test(unittest.TestCase):

    def test_uint_fast64_number(self):
        inp = [cgen.objects.Val(
            "200", type_=cgen.objects.CTypes.uint_fast8)]
        self.assertIsNone(cgen.check(inp))

    def test_uint_fast64_number_starts_with_zero(self):
        inp = [cgen.objects.Val(
            "0123", type_=cgen.objects.CTypes.uint_fast64)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "0123"
            }))

    def test_uint_fast64_number_zero(self):
        inp = [cgen.objects.Val(
            "0", type_=cgen.objects.CTypes.uint_fast64)]
        self.assertIsNone(cgen.check(inp))

    def test_uint_fast64_some_string(self):
        inp = [cgen.objects.Val(
            "some_string_here123",
            type_=cgen.objects.CTypes.uint_fast64)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string_here123"
            }))


class ValTest(unittest.TestCase):

    def test_char(self):
        inp = [cgen.objects.Val(
            "a", type_=cgen.objects.CTypes.char)]
        self.assertIsNone(cgen.check(inp))

    def test_char_long_string(self):
        inp = [cgen.objects.Val(
            "some_string", type_=cgen.objects.CTypes.char)]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message,
            cgen.errors._BAD_LITERAL.format_map({
                "literal": "some_string"
            }))

    def test_int_array(self):
        inp = [cgen.objects.Val((
            cgen.objects.Val(
                "0", type_=cgen.objects.CTypes.int_fast32),
            cgen.objects.Val(
                "1", type_=cgen.objects.CTypes.int_fast32)),
            type_=cgen.objects.CTypes.array(
                cgen.objects.CTypes.int_fast32))
        ]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(
            err.exception.message, cgen.errors._NOT_IMPLEMENTED)


if __name__ == "__main__":
    unittest.main()
