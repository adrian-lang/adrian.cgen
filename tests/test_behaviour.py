import unittest

from adrian.cgen import CTypes, Val


class TypeEqualityTest(unittest.TestCase):

    def test_simple(self):
        get_type = lambda name: getattr(CTypes, name)
        types = (
            "int", "int_fast8", "int_fast32", "int_fast64",
            "uint_fast8", "uint_fast32", "uint_fast64", "size",
            "char", "void", "file")
        for type_ in types:
            with self.subTest(type_=type_):
                self.assertEqual(get_type(type_), get_type(type_))

    def test_ptr(self):
        self.assertEqual(
            CTypes.ptr(CTypes.int),
            CTypes.ptr(CTypes.int))
        self.assertNotEqual(
            CTypes.ptr(CTypes.size),
            CTypes.ptr(CTypes.int))
        self.assertEqual(
            CTypes.ptr(CTypes.ptr(CTypes.size)),
            CTypes.ptr(CTypes.ptr(CTypes.size)))

    def test_array(self):
        self.assertNotEqual(
            CTypes.array(CTypes.int, size="auto"),
            CTypes.array(CTypes.int))
        self.assertEqual(
            CTypes.array(CTypes.int),
            CTypes.array(CTypes.int))
        self.assertNotEqual(
            CTypes.array(CTypes.int),
            CTypes.array(CTypes.size))
        self.assertEqual(
            CTypes.array(CTypes.int, size="auto"),
            CTypes.array(CTypes.int, size="auto"))
        self.assertNotEqual(
            CTypes.array(CTypes.int, size=3),
            CTypes.array(CTypes.int, size="auto"))
        self.assertEqual(
            CTypes.array(CTypes.int, size=3),
            CTypes.array(CTypes.int, size=3))
        self.assertNotEqual(
            CTypes.array(CTypes.int, size=3),
            CTypes.array(CTypes.int, size=4))


class ValEqualityTest(unittest.TestCase):

    def test_simple_type(self):
        self.assertEqual(
            Val(1, type_=CTypes.int),
            Val(1, type_=CTypes.int))
        self.assertEqual(
            Val(1, type_=CTypes.size),
            Val(1, type_=CTypes.size))

    def test_ptr(self):
        self.assertEqual(
            Val("ab", type_=CTypes.ptr(CTypes.char)),
            Val("ab", type_=CTypes.ptr(CTypes.char)))
        self.assertNotEqual(
            Val("ab", type_=CTypes.ptr(CTypes.uint_fast8)),
            Val("ab", type_=CTypes.ptr(CTypes.char)))
        self.assertNotEqual(
            Val("ab", type_=CTypes.ptr(CTypes.uint_fast8)),
            Val("ac", type_=CTypes.ptr(CTypes.uint_fast8)))

    def test_array(self):
        self.assertEqual(
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.int)),
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.int)))
        self.assertNotEqual(
            Val(
                (Val("1", type_=CTypes.int), Val("2", type_=CTypes.int)),
                type_=CTypes.array(CTypes.int)),
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.int)))
        self.assertNotEqual(
            Val(
                (Val("1", type_=CTypes.char), ),
                type_=CTypes.array(CTypes.int)),
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.int)))
        self.assertNotEqual(
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.int)),
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.char)))
        self.assertNotEqual(
            Val(
                (Val("2", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.char)),
            Val(
                (Val("1", type_=CTypes.int), ),
                type_=CTypes.array(CTypes.char)))

    def test_similar(self):
        self.assertNotEqual(
            Val(1, type_=CTypes.int),
            Val("1", type_=CTypes.int))
        self.assertNotEqual(
            Val(1, type_=CTypes.int_fast8),
            Val(1, type_=CTypes.int))
        self.assertNotEqual(
            Val(1, type_=CTypes.int_fast8),
            Val(2, type_=CTypes.int_fast8))
