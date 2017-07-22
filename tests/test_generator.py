import unittest

from adrian import cgen


stdlib_incl = cgen.Include("stdlib.h")
malloc_func = cgen.CFuncDescr(
    name="malloc", rettype=cgen.CTypes.ptr(cgen.CTypes.void),
    args=(cgen.CTypes.size_t, ),
    includes=[stdlib_incl])


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

    def test_use_in_complex_function(self):
        inp = [
            cgen.Func(
                "initMyStruct", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(cgen.Decl("data", type_=cgen.CTypes.int_fast8), ),
                body=(
                    cgen.Decl(
                        "self",
                        type_=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                        expr=malloc_func(cgen.SizeOf(cgen.StructType("MyStruct")))),
                    cgen.Assignment(
                        name=cgen.StructElem(
                            cgen.CTypes.ptr(cgen.Var("self")), "data"),
                        expr=cgen.Var("data")),
                    cgen.Return(cgen.Var("self"))))]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertEqual(
            "\n".join([
                "#include <stdint.h>",
                "#include <stdlib.h>",
                "struct MyStruct* initMyStruct(int_fast8_t data) {",
                "struct MyStruct* self = malloc(sizeof(struct MyStruct));",
                "self->data = data;",
                "return self;",
                "}"
            ]),
            "\n".join(list(generator.generate())))

    def test_use_in_simple_function(self):
        inp = [
            cgen.Func(
                "lol", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(),
                body=(
                    cgen.Return(
                        cgen.FuncCall("initMyStruct", cgen.Val("23", type_=cgen.CTypes.int_fast8))), ))]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertEqual(
            "\n".join([
                "#include <stdint.h>",
                "struct MyStruct* lol() {",
                "return initMyStruct(23);",
                "}"
            ]),
            "\n".join(list(generator.generate())))

    def test_use_in_large_example(self):
        inp = [
            cgen.Struct(
                "MyStruct", (
                    cgen.Decl("data", type_=cgen.CTypes.int_fast8), )),
            cgen.Func(
                "initMyStruct", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(cgen.Decl("data", type_=cgen.CTypes.int_fast8), ),
                body=(
                    cgen.Decl(
                        "self",
                        type_=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                        expr=malloc_func(cgen.SizeOf(cgen.StructType("MyStruct")))),
                    cgen.Assignment(
                        name=cgen.StructElem(
                            cgen.CTypes.ptr(cgen.Var("self")), "data"),
                        expr=cgen.Var("data")),
                    cgen.Return(cgen.Var("self")))),
            cgen.Func(
                "lol", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(),
                body=(
                    cgen.Return(
                        cgen.FuncCall("initMyStruct", cgen.Val("23", type_=cgen.CTypes.int_fast8))), ))
        ]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertEqual(
            "\n".join([
                "#include <stdint.h>",
                "#include <stdlib.h>",
                "struct MyStruct {",
                "int_fast8_t data;",
                "};",
                "struct MyStruct* initMyStruct(int_fast8_t data) {",
                "struct MyStruct* self = malloc(sizeof(struct MyStruct));",
                "self->data = data;",
                "return self;",
                "}",
                "struct MyStruct* lol() {",
                "return initMyStruct(23);",
                "}"
            ]),
            "\n".join(list(generator.generate())))


if __name__ == "__main__":
    unittest.main()
