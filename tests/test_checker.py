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
        self.assertEqual(err.exception.message, cgen.errors._BAD_NAME.format_map({"name": "while"}))

    def test_digit_and_letters_name(self):
        inp = [cgen.objects.Var("2foo")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(err.exception.message, cgen.errors._BAD_NAME.format_map({"name": "2foo"}))

    def test_letters_space_letters_name(self):
        inp = [cgen.objects.Var("my foo")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(err.exception.message, cgen.errors._BAD_NAME.format_map({"name": "my foo"}))

    def test_specsymb_and_letters_name(self):
        inp = [cgen.objects.Var("$Foo")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(err.exception.message, cgen.errors._BAD_NAME.format_map({"name": "$Foo"}))

    def test_int_name(self):
        inp = [cgen.objects.Var("int")]
        with self.assertRaises(cgen.errors.CheckError) as err:
            cgen.check(inp)
        self.assertEqual(err.exception.message, cgen.errors._BAD_NAME.format_map({"name": "int"}))


if __name__ == "__main__":
    unittest.main()
