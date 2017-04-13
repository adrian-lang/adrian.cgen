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
    if isinstance(stmt.type_, (objects.CTypes.int32, objects.CTypes.int64)):
        good_int = re.compile(r"^[0-9]+$")
        if not good_int.match(stmt.literal):
            errors.bad_literal(stmt.literal)
    else:
        errors.not_implemented()


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
