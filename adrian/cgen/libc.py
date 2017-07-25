from adrian.cgen import Include, CFuncDescr, CNameDescr, CTypes


_stdlib = Include("stdlib.h")
_stdio = Include("stdio.h")


malloc = CFuncDescr(
    "malloc", rettype=CTypes.ptr(CTypes.void),
    args=(CTypes.size_t, ),
    includes=[_stdlib])

free = CFuncDescr(
    "free", rettype=CTypes.void,
    args=(CTypes.ptr(CTypes.void), ),
    includes=[_stdlib])


# According to http://man7.org/linux/man-pages/man3/assert.3.html:
# > In C89, expression is required to be of type int and undefined
# > behavior results if it is not, but in C99 it may have any scalar type.
assert_ = CFuncDescr(
    "assert", rettype=CTypes.void,
    args=(CTypes.int, ),
    includes=[Include("assert.h")])


stdout = CNameDescr(
    "stdout", type_=CTypes.ptr(CTypes.file), includes=[_stdio])
stderr = CNameDescr(
    "stderr", type_=CTypes.ptr(CTypes.file), includes=[_stdio])

fputs = CFuncDescr(
    "fputs", rettype=CTypes.int,
    args=(CTypes.ptr(CTypes.char), CTypes.ptr(CTypes.file)),
    includes=[_stdio])
