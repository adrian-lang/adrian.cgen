from adrian.cgen import Include, CFuncDescr, CTypes


_stdlib = Include("stdlib.h")


malloc = CFuncDescr(
    "malloc", rettype=CTypes.ptr(CTypes.void),
    args=(CTypes.size_t, ),
    includes=[_stdlib])

free = CFuncDescr(
    "free", rettype=CTypes.void,
    args=(CTypes.ptr(CTypes.void), ),
    includes=[_stdlib])
