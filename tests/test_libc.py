from adrian.cgen import (
    SizeOf, Decl, Val, Var, Null, Expr, Return, CTypes, COps,
    make_main0, libc)

from testutils import CgenTestCase


class LibcTest(CgenTestCase):

    def test_malloc_and_free_in_main(self):
        chunk_size = 1645
        main_func = make_main0(
            Decl(
                "chunk", type_=CTypes.ptr(CTypes.void),
                expr=libc.malloc(Val(chunk_size, type_=CTypes.size_t))),
            libc.free(Var("chunk")),  # yeah, no NULL check :)
            Return(Val(0, type_=CTypes.int)))
        expected = (
            "#include <stdlib.h>",
            "int main(void) {",
            "void* chunk = malloc(1645);",
            "free(chunk);",
            "return 0;",
            "}")
        self.check_gen([[main_func]], expected)

    def test_assert(self):
        var_name = "v"
        main_func = make_main0(
            Decl(
                var_name, type_=CTypes.ptr(CTypes.void),
                expr=libc.malloc(Val(10, type_=CTypes.size_t))),
            libc.assert_(Expr(COps.neq, Var(var_name), Null)),
            libc.free(Var(var_name)),
            Return(Val(0, type_=CTypes.int)))
        expected = (
            "#include <assert.h>",
            "#include <stdlib.h>",
            "int main(void) {",
            "void* v = malloc(10);",
            "assert(v != NULL);",
            "free(v);",
            "return 0;",
            "}")
        self.check_gen([[main_func]], expected)
