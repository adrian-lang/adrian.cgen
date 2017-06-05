"""Objects that represent C language constructions."""


class _Type(object):
    """Base class for EDSL objects."""

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



class _Char(_Type):
    """char."""
    pass


class _Array(_Type):
    """C array."""

    def __init__(self, type_):
        self._type = type_

    @property
    def type_(self):
        return self._type


class _Ptr(_Array):
    """Pointer."""
    pass


class CTypes(object):
    """Container to ease importing."""
    int_fast8 = _IntFast8()
    int_fast32 = _IntFast32()
    int_fast64 = _IntFast64()
    uint_fast8 = _UIntFast8()
    uint_fast32 = _UIntFast32()
    uint_fast64 = _UIntFast64()
    char = _Char()

    @classmethod
    def ptr(cls, type_):
        return _Ptr(type_)

    @classmethod
    def array(cls, type_):
        return _Array(type_)


class Val(object):
    """Value of any kind."""

    def __init__(self, literal, type_):
        self._literal = literal
        self._type = type_

    @property
    def literal(self):
        return self._literal

    @property
    def type_(self):
        return self._type


class Var(object):
    """Variable."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Expr(object):
    """Expression."""

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


class FuncCall(object):
    """Function call."""

    def __init__(self, name, *args):
        self._name = name
        self._args = args

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args


class Decl(object):
    """Declaration"""

    def __init__(self, name, type_or_expr):
        self._name = name
        self._type = None
        self._expr = None
        if isinstance(type_or_expr, (Val, FuncCall, Var, Expr)):
            self._expr = type_or_expr
        else:
            self._type = type_or_expr

    @property
    def name(self):
        return self._name

    @property
    def type_(self):
        return self._type

    @property
    def expr(self):
        return self._expr


class Assignment(object):
    """Assignment."""

    def __init__(self, name, expr):
        self._name = name
        self._expr = expr

    @property
    def name(self):
        return self._name

    @property
    def expr(self):
        return self._expr


class ArrayElemByIndex(object):
    """Representation of getting array element."""

    def __init__(self, name, index):
        self._name = name
        self._index = index

    @property
    def name(self):
        return self._name

    @property
    def index(self):
        return self._index


class Struct(object):
    """struct."""

    def __init__(self, name, body):
        self._name = name
        self._body = body

    @property
    def name(self):
        return self._name

    @property
    def body(self):
        return self._body


class StructElem(object):
    """Representation of getting element of struct."""

    def __init__(self, struct_name, elem_name):
        self._struct_name = struct_name
        self._elem_name = elem_name

    @property
    def struct_name(self):
        return self._struct_name

    @property
    def elem_name(self):
        return self._elem_name


class If(object):
    """An if."""

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


class ElseIf(object):
    """An else-if."""

    def __init__(self, cond, body):
        self._cond = cond
        self._body = body

    @property
    def cond(self):
        return self._cond

    @property
    def body(self):
        return self._body


class Else(object):
    """An else."""

    def __init__(self, body):
        self._body = body

    @property
    def body(self):
        return self._body


class While(object):
    """While."""

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


class For(object):
    """A for."""

    def __init__(self, cond, body):
        self._cond = cond
        self._body = body

    @property
    def cond(self):
        return self._cond

    @property
    def body(self):
        return self._body


class Return(object):
    """Return statement."""

    def __init__(self, expr):
        self._expr = expr

    @property
    def expr(self):
        return self._expr


class Include(object):
    """Representation of C include directive."""

    def __init__(self, module_name):
        self._module_name = module_name

    @property
    def module_name(self):
        return self._module_name


class Func(object):
    """Definition of function."""

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


class CFuncDescr(object):
    """Declaration of C function for FFI."""

    def __init__(self, name, rettype, args, includes):
        self._name = name
        self._rettype = rettype
        self._args = args
        self._includes = includes

    def __call__(self, *args):
        return FuncCall(self.name, *args)

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

    @property
    def call_args(self):
        return self._call_args


class CVarDescr(object):
    """Definition of C variable or constant for FFI."""

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
