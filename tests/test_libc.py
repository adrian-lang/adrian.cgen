import unittest

from adrian.cgen import (
    Generator, SizeOf, Decl, Val, Var, CTypes, make_main0, libc)


class LibcTest(unittest.TestCase):

    def check_gen(self, asts, expected_lines):
        gen = Generator()
        for ast in asts:
            gen.add_ast(ast)
        self.assertEqual(
            "\n".join(expected_lines),
            "\n".join(gen.generate()))

    def test_malloc_and_free_in_main(self):
        chunk_size = 1645
        main_func = make_main0(
            Decl(
                "chunk", type_=CTypes.ptr(CTypes.void),
                expr=libc.malloc(Val(chunk_size, type_=CTypes.size_t))),
            libc.free(Var("chunk")))  # yeah, no NULL check :)
        expected = (
            "#include <stdlib.h>",
            "int main(void) {",
            "void* chunk = malloc(1645);",
            "free(chunk);",
            "}")
        self.check_gen([[main_func]], expected)
