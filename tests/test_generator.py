import unittest

from adrian import cgen


stdlib_incl = cgen.Include("stdlib.h")
malloc_func = cgen.CFuncDescr(
    name="malloc", rettype=cgen.CTypes.ptr(cgen.CTypes.void),
    args=(cgen.CTypes.size_t, ),
    includes=[stdlib_incl])


class ExprTest(unittest.TestCase):

    def test_it_generates(self):
        inp = [cgen.Expr(
            cgen.COps.plus, cgen.Val("1", type_=cgen.CTypes.int),
            cgen.Expr(cgen.COps.star, cgen.Val("3", type_=cgen.CTypes.int),
            cgen.Expr(cgen.COps.minus, cgen.Val("5", type_=cgen.CTypes.int),
            cgen.Expr(cgen.COps.slash, cgen.Val("8", type_=cgen.CTypes.int),
                cgen.Val("4", type_=cgen.CTypes.int)))))]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertEqual(
            "\n".join([
                "1 + 3 * 5 - 8 / 4"
            ]),
            "\n".join(list(generator.generate())))


class FuncCallTest(unittest.TestCase):

    def test_it_generates(self):
        inp = [cgen.FuncCall(
            "lol", cgen.Val("d", type_=cgen.CTypes.char),
            cgen.Val("some string", type_=cgen.CTypes.ptr(cgen.CTypes.char)))]
        generator = cgen.Generator()
        generator.add_ast(inp)
        self.assertEqual(
            "\n".join([
                "lol('d', \"some string\");"
            ]),
            "\n".join(list(generator.generate())))


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
        struct_decl = [
            cgen.Struct(
                "MyStruct", (
                    cgen.Decl("data", type_=cgen.CTypes.int_fast8), ))]
        init_my_struct = [
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
        lol = [
            cgen.Func(
                "lol", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(),
                body=(
                    cgen.Return(
                        cgen.FuncCall("initMyStruct", cgen.Val("23", type_=cgen.CTypes.int_fast8))), ))]
        generator = cgen.Generator()
        generator.add_ast(struct_decl)
        generator.add_ast(init_my_struct)
        generator.add_ast(lol)
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
