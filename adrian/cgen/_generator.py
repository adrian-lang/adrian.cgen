from . import errors
from . import objects
from . import _context

from paka import funcreg


_FUNCS = funcreg.TypeRegistry()


@_FUNCS.register(objects.Val)
def val(stmt, context):
    if isinstance(stmt.type_, (type(objects.CTypes.int32), type(objects.CTypes.int64))):
        return stmt.literal
    errors.not_implemented()


@_FUNCS.register(objects.Var)
def var(stmt, context):
    return stmt.name


def main(ast_):
    context = _context.Context()
    return [_FUNCS[stmt](stmt, context=context) for stmt in ast_]
