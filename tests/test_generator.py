import unittest

from adrian import cgen


class StructTest(unittest.TestCase):

    def test_it_generates(self):
        inp = [cgen.Struct(
            "MyStruct", (
                cgen.Decl("data", type_=cgen.CTypes.int_fast8), ))]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertEqual(
            "\n".join([
                "#include <stdint.h>",
                "struct MyStruct {",
                "int_fast8_t data;",
                "};"
            ]),
            "\n".join(list(generator.generate())))


if __name__ == "__main__":
    unittest.main()
