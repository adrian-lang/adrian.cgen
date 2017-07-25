import unittest

from adrian import cgen

from testutils import CgenTestCase


stdlib_incl = cgen.Include("stdlib.h")
malloc_func = cgen.CFuncDescr(
    name="malloc", rettype=cgen.CTypes.ptr(cgen.CTypes.void),
    args=(cgen.CTypes.size_t, ),
    includes=[stdlib_incl])


class DeclTest(CgenTestCase):

    def test_no_size(self):
        inp = [cgen.Decl(
            "a", type_=cgen.CTypes.array(cgen.CTypes.int),
            expr=cgen.Val((cgen.Val("0", type_=cgen.CTypes.int), cgen.Val("1", cgen.CTypes.int)),
                cgen.CTypes.array(cgen.CTypes.int)))]
        self.check_gen(
            [inp],
            ("int a[] = {0, 1};", ))

    def test_explicit_size(self):
        inp = [cgen.Decl(
            "a", type_=cgen.CTypes.array(cgen.CTypes.int, size=20))]
        self.check_gen([inp], ("int a[20];", ))

    def test_auto_size(self):
        inp = [cgen.Decl(
            "a", type_=cgen.CTypes.array(cgen.CTypes.int, size="auto"),
            expr=cgen.Val((cgen.Val("0", type_=cgen.CTypes.int), cgen.Val("1", cgen.CTypes.int)),
                cgen.CTypes.array(cgen.CTypes.int)))]
        self.check_gen([inp], ("int a[2] = {0, 1};", ))


class AssignmentTest(CgenTestCase):

    def test_array_elem_by_index(self):
        inp = [cgen.Assignment(
            cgen.ArrayElemByIndex("a", cgen.Val("0", type_=cgen.CTypes.int)),
            cgen.Val("1", type_=cgen.CTypes.int))]
        self.check_gen([inp], ("a[0] = 1;", ))

    def test_struct_elem(self):
        inp = [cgen.Assignment(
            cgen.StructElem(cgen.Var("self"), cgen.Var("data")),
            cgen.Var("data"))]
        self.check_gen([inp], ("self.data = data;", ))


class ExprTest(CgenTestCase):

    def test_it_generates(self):
        inp = [cgen.Expr(
            cgen.COps.plus, cgen.Val("1", type_=cgen.CTypes.int),
            cgen.Expr(cgen.COps.star, cgen.Val("3", type_=cgen.CTypes.int),
            cgen.Expr(cgen.COps.minus, cgen.Val("5", type_=cgen.CTypes.int),
            cgen.Expr(cgen.COps.slash, cgen.Val("8", type_=cgen.CTypes.int),
                cgen.Val("4", type_=cgen.CTypes.int)))))]
        self.check_gen([inp], ("1 + 3 * 5 - 8 / 4;", ))


class FuncCallTest(CgenTestCase):

    def test_it_generates(self):
        inp = [cgen.FuncCall(
            "lol", cgen.Val("d", type_=cgen.CTypes.char),
            cgen.Val("some string", type_=cgen.CTypes.ptr(cgen.CTypes.char)))]
        self.check_gen([inp], ("lol('d', \"some string\");", ))


class StructTest(CgenTestCase):

    def test_it_generates(self):
        inp = [cgen.Struct(
            "MyStruct", (
                cgen.Decl("data", type_=cgen.CTypes.int_fast8), ))]
        expected = (
            "#include <stdint.h>",
            "struct MyStruct {",
            "int_fast8_t data;",
            "};")
        self.check_gen([inp], expected)

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
                            cgen.CTypes.ptr(cgen.Var("self")), cgen.Var("data")),
                        expr=cgen.Var("data")),
                    cgen.Return(cgen.Var("self"))))]
        expected = (
            "#include <stdint.h>",
            "#include <stdlib.h>",
            "struct MyStruct* initMyStruct(int_fast8_t data) {",
            "struct MyStruct* self = malloc(sizeof(struct MyStruct));",
            "self->data = data;",
            "return self;",
            "}")
        self.check_gen([inp], expected)

    def test_use_in_simple_function(self):
        inp = [
            cgen.Func(
                "lol", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(),
                body=(
                    cgen.Return(
                        cgen.FuncCall("initMyStruct", cgen.Val("23", type_=cgen.CTypes.int_fast8))), ))]
        expected = (
            "#include <stdint.h>",
            "struct MyStruct* lol() {",
            "return initMyStruct(23);",
            "}")
        self.check_gen([inp], expected)

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
                            cgen.CTypes.ptr(cgen.Var("self")), cgen.Var("data")),
                        expr=cgen.Var("data")),
                    cgen.Return(cgen.Var("self"))))]
        lol = [
            cgen.Func(
                "lol", rettype=cgen.CTypes.ptr(cgen.StructType("MyStruct")),
                args=(),
                body=(
                    cgen.Return(
                        cgen.FuncCall("initMyStruct", cgen.Val("23", type_=cgen.CTypes.int_fast8))), ))]
        expected = (
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
            "}")
        self.check_gen([struct_decl, init_my_struct, lol], expected)
