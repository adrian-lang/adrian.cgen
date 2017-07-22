"""Objects that represent C language constructions."""

class _Object(object):
    _keys = ()  # Override in subclass.

    def __str__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                "{}={!r}".format(
                    key, getattr(self, key)) for key in self._keys))

    __repr__ = __str__


class _Op(_Object):
    """Base class for EDSL operators."""

    def __init__(self):
        pass


class _Plus(_Op):
    """+."""
    pass


class _Minus(_Op):
    """-."""
    pass


class _Star(_Op):
    """*."""
    pass


class _Slash(_Op):
    """/."""
    pass


class COps(_Object):
    """Container."""
    plus = _Plus()
    minus = _Minus()
    star = _Star()
    slash = _Slash()


class _Type(_Object):
    """Base class for EDSL types."""

    def __init__(self):
        pass


class _UIntFast8(_Type):
    """uint_fast8_t."""
    pass


class _UIntFast32(_Type):
    """uint_fast32_t."""
    pass


class _UIntFast64(_Type):
    """uint_fast64_t."""
    pass


class _IntFast8(_Type):
    """int_fast8_t."""
    pass


class _IntFast32(_Type):
    """int_fast32_t."""
    pass


class _IntFast64(_Type):
    """int_fast64_t."""
    pass


class _Int(_Type):
    """int."""
    pass


class _SizeT(_Type):
    """size_t"""
    pass


class _Char(_Type):
    """char."""
    pass


class _Array(_Type):
    """C array."""

    _keys = ("type_", )

    def __init__(self, type_):
        self._type = type_

    @property
    def type_(self):
        return self._type


class _Ptr(_Array):
    """Pointer."""
    pass


class _Void(_Type):
    """void."""
    pass


class CTypes(_Object):
    """Container to ease importing."""
    int = _Int()
    int_fast8 = _IntFast8()
    int_fast32 = _IntFast32()
    int_fast64 = _IntFast64()
    uint_fast8 = _UIntFast8()
    uint_fast32 = _UIntFast32()
    uint_fast64 = _UIntFast64()
    size_t = _SizeT()
    char = _Char()
    void = _Void()

    @classmethod
    def ptr(cls, type_):
        return _Ptr(type_)

    @classmethod
    def array(cls, type_):
        return _Array(type_)


class StructType(_Object):
    """Struct type"""

    _keys = ("name", )

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class SizeOf(_Object):
    """sizeof operator."""

    _keys = ("type_", )

    def __init__(self, type_):
        self._type = type_

    @property
    def type_(self):
        return self._type


class Val(_Object):
    """Value of any kind."""

    _keys = ("literal", "type_")

    def __init__(self, literal, type_):
        self._literal = literal
        self._type = type_

    @property
    def literal(self):
        return self._literal

    @property
    def type_(self):
        return self._type


class Var(_Object):
    """Variable."""

    _keys = ("name", )

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Expr(_Object):
    """Expression."""

    _keys = ("op", "expr1", "expr2")

    def __init__(self, op, expr1, expr2):
        self._op = op
        self._expr1 = expr1
        self._expr2 = expr2

    @property
    def op(self):
        return self._op

    @property
    def expr1(self):
        return self._expr1

    @property
    def expr2(self):
        return self._expr2


class FuncCall(_Object):
    """Function call."""

    _keys = ("name", "args", "includes")

    def __init__(self, name, *args, includes=None):
        self._name = name
        self._args = args
        self._includes = includes or []

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args

    @property
    def includes(self):
        return self._includes


class Decl(_Object):
    """Declaration"""

    _keys = ("name", "type_", "expr")

    def __init__(self, name, type_=None, expr=None):
        self._name = name
        self._type = None or type_
        self._expr = None or expr

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    @property
    def expr(self):
        return self._expr


class Assignment(_Object):
    """Assignment."""

    _keys = ("name", "expr")

    def __init__(self, name, expr):
        self._name = name
        self._expr = expr

    @property
    def name(self):
        return self._name

    @property
    def expr(self):
        return self._expr


class ArrayElemByIndex(_Object):
    """Representation of getting array element."""

    _keys = ("name", "index")

    def __init__(self, name, index):
        self._name = name
        self._index = index

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index


class Struct(_Object):
    """struct."""

    _keys = ("name", "body")

    def __init__(self, name, body):
        self._name = name
        self._body = body

    @property
    def name(self):
        return self._name

    @property
    def body(self):
        return self._body


class StructElem(_Object):
    """Representation of getting element of struct."""

    _keys = ("struct_name", "elem_name")

    def __init__(self, struct_name, elem_name):
        self._struct_name = struct_name
        self._elem_name = elem_name

    @property
    def struct_name(self):
        return self._struct_name

    @property
    def elem_name(self):
        return self._elem_name


class If(_Object):
    """An if."""

    _keys = ("cond", "body", "else_ifs", "else_")

    def __init__(self, cond, body, else_ifs=[], else_=None):
        self._cond = cond
        self._body = body
        self._else_ifs = else_ifs
        self._else = else_

    @property
    def cond(self):
        return self._cond

    @property
    def body(self):
        return self._body

    @property
    def else_ifs(self):
        return self._else_ifs

    @property
    def else_(self):
        return self._else


class ElseIf(_Object):
    """An else-if."""

    _keys = ("cond", "body")

    def __init__(self, cond, body):
        self._cond = cond
        self._body = body

    @property
    def cond(self):
        return self._cond

    @property
    def body(self):
        return self._body


class Else(_Object):
    """An else."""

    _keys = ("body", )

    def __init__(self, body):
        self._body = body

    @property
    def body(self):
        return self._body


class While(_Object):
    """While."""

    _keys = ("cond", "body")

    def __init__(self, cond, body):
        self._cond = cond
        self._body = body

    @property
    def cond(self):
        return self._cond

    @property
    def body(self):
        return self._body


class DoWhile(While):
    """TODO"""
    pass


class For(_Object):
    """A for."""

    _keys = ("cond", "body")

    def __init__(self, cond, body):
        self._cond = cond
        self._body = body

    @property
    def cond(self):
        return self._cond

    @property
    def body(self):
        return self._body


class Return(_Object):
    """Return statement."""

    _keys = ("expr", )

    def __init__(self, expr):
        self._expr = expr

    @property
    def expr(self):
        return self._expr


class Include(_Object):
    """Representation of C include directive."""

    _keys = ("module_name", )

    def __init__(self, module_name):
        self._module_name = module_name

    @property
    def module_name(self):
        return self._module_name


class Func(_Object):
    """Definition of function."""

    _keys = ("name", "rettype", "args", "body")

    def __init__(self, name, rettype, args, body):
        self._name = name
        self._rettype = rettype
        self._args = args
        self._body = body

    @property
    def name(self):
        return self._name

    @property
    def rettype(self):
        return self._rettype

    @property
    def args(self):
        return self._args

    @property
    def body(self):
        return self._body


class CFuncDescr(_Object):
    """Declaration of C function for FFI."""

    _keys = ("name", "rettype", "args", "includes")

    def __init__(self, name, rettype, args, includes):
        self._name = name
        self._rettype = rettype
        self._args = args
        self._includes = includes

    def __call__(self, *args):
        return FuncCall(self.name, *args, includes=self._includes)

    @property
    def name(self):
        return self._name

    @property
    def rettype(self):
        return self._rettype

    @property
    def args(self):
        return self._args

    @property
    def includes(self):
        return self._includes


class CVarDescr(_Object):
    """Definition of C variable or constant for FFI."""

    _keys = ("name", "type_", "includes")

    def __init__(self, name, type_, includes):
        self._name = name
        self._type = type_
        self._includes = includes

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    @property
    def includes(self):
        return self._includes
