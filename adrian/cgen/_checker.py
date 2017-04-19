import re

from . import errors
from . import objects
from . import _context

from paka import funcreg


CKEYWORDS = (
    "while",
    )

CTYPES = (
    "int",
    )


_FUNCS = funcreg.TypeRegistry()


@_FUNCS.register(objects.Val)
def val(stmt, context):
    if isinstance(stmt.type_, tuple(map(type, (
            objects.CTypes.int32, objects.CTypes.int64,
            objects.CTypes.char)))):
        val.reg[stmt.type_](stmt, context)
    else:
        errors.not_implemented()


val.reg = funcreg.TypeRegistry()


@val.reg.register(type(objects.CTypes.int32))
@val.reg.register(type(objects.CTypes.int64))
def _val_int32_int64(stmt, context):
    good_int = re.compile(r"^[0-9]+$")
    if ((stmt.literal.startswith("0") and len(stmt.literal) > 1) or \
            not good_int.match(stmt.literal)):
        errors.bad_literal(stmt.literal)


@val.reg.register(type(objects.CTypes.char))
def _val_char(stmt, context):
    if len(stmt.literal) > 1:
        errors.bad_literal(stmt.literal)


@_FUNCS.register(objects.Var)
def var(stmt, context):
    good_naming = re.compile(r"^[a-zA-Z_][a-zA-Z_0-9]*$")
    # Full name must be good.
    match = good_naming.match(stmt.name)
    if match and stmt.name not in CKEYWORDS and stmt.name not in CTYPES:
        pass
    else:
        errors.bad_name(stmt.name)


def main(ast_):
    context = _context.Context()
    for stmt in ast_:
        _FUNCS[stmt](stmt, context=context)
