from adrian.cgen import CFuncDescr, CNameDescr, CTypes, includes


malloc = CFuncDescr(
    "malloc", rettype=CTypes.ptr(CTypes.void),
    args=(CTypes.size, ),
    includes=[includes.stdlib])

free = CFuncDescr(
    "free", rettype=CTypes.void,
    args=(CTypes.ptr(CTypes.void), ),
    includes=[includes.stdlib])


# According to http://man7.org/linux/man-pages/man3/assert.3.html:
# > In C89, expression is required to be of type int and undefined
# > behavior results if it is not, but in C99 it may have any scalar type.
assert_ = CFuncDescr(
    "assert", rettype=CTypes.void,
    args=(CTypes.int, ),
    includes=[includes.assert_])


stdout = CNameDescr(
    "stdout", type_=CTypes.ptr(CTypes.file), includes=[includes.stdio])
stderr = CNameDescr(
    "stderr", type_=CTypes.ptr(CTypes.file), includes=[includes.stdio])

fputs = CFuncDescr(
    "fputs", rettype=CTypes.int,
    args=(CTypes.ptr(CTypes.char), CTypes.ptr(CTypes.file)),
    includes=[includes.stdio])

fflush = CFuncDescr(
    "fflush", rettype=CTypes.int,
    args=(CTypes.ptr(CTypes.file), ),
    includes=[includes.stdio])
