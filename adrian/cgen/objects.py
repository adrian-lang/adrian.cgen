class _Type(object):

    def __init__(self):
        pass


class _Int32(_Type):
    pass


class _Int64(_Type):
    pass


class _Char(_Type):
    pass


class _Array(_Type):

    def __init__(self, type_):
        self._type = type_

    @property
    def type_(self):
        return self._type


class _Ptr(_Array):
    pass


class CTypes(object):
    int32 = _Int32()
    int64 = _Int64()
    char = _Char()

    @classmethod
    def ptr(cls, type_):
        return _Ptr(type_)

    @classmethod
    def array(cls, type_):
        return _Array(type_)


class Val(object):

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

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Expr(object):

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

    def __init__(self, body):
        self._body = body

    @property
    def body(self):
        return self._body


class While(object):

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
    pass


class For(object):

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

    def __init__(self, expr):
        self._expr = expr

    @property
    def expr(self):
        return self._expr


class Include(object):

    def __init__(self, module_name):
        self._module_name = module_name

    @property
    def module_name(self):
        return self._module_name


class Func(object):

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
