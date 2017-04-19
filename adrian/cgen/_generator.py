from . import errors
from . import objects
from . import _context

from paka import funcreg


_FUNCS = funcreg.TypeRegistry()


@_FUNCS.register(objects.Val)
def val(stmt, context):
    if isinstance(stmt.type_, tuple(map(type, (
            objects.CTypes.int32, objects.CTypes.int64,
            objects.CTypes.char)))):
        return val.reg[stmt.type_](stmt, context)
    else:
        errors.not_implemented()


val.reg = funcreg.TypeRegistry()


@val.reg.register(type(objects.CTypes.int32))
@val.reg.register(type(objects.CTypes.int64))
def _val_int32_int64(stmt, context):
    return stmt.literal


@val.reg.register(type(objects.CTypes.char))
def _val_char(stmt, context):
    return "'" + stmt.literal + "'"


@_FUNCS.register(objects.Var)
def var(stmt, context):
    return stmt.name


def main(ast_):
    context = _context.Context()
    return [_FUNCS[stmt](stmt, context=context) for stmt in ast_]
