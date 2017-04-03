API Design
==========

Literal
-------
.. code-block:: c

    3

.. code-block:: python

    Val(literal="3", type_=CTypes.int)

Variable
--------
.. code-block:: c

    x

.. code-block:: python

    Var("x")

Expression
----------
.. code-block:: c

    1 + 1

.. code-block:: python

    Expr(
        COps.plus,
        Val(literal="1", type_=CTypes.int), Val(literal="1", type_=CTypes.int))

Function call
-------------
.. code-block:: c

    my_func(1)

.. code-block:: python

    FuncCall("my_func", Val("1"))

Declaration of string with initialization
-----------------------------------------
.. code-block:: c

    char *my_s = "test"

.. code-block:: python

    Decl(
        "my_s",
        Val(
            literal="test",
            type_=CTypes.str))

``CTypes.str`` is equivalent to ``CTypes.ptr(CTypes.char)``.

Declaration
-----------
.. code-block:: c

    int a

.. code-block:: python

    Decl("a", CTypes.int)

Declaration of int with initialization
--------------------------------------
.. code-block:: c

    int a = 1

.. code-block:: python

    Decl("a", Val(type_=CTypes.int, literal="1"))

Declaration of int with initialization by expression
----------------------------------------------------
.. code-block:: c

    int a = 1 + 1

.. code-block:: python

    Decl(
        "a",
        Val(  # type is inferred
            Expr(
                COps.plus,
                Val(literal="1", type_=CTypes.int),
                Val(literal="1", type_=CTypes.int))))

Declaration of int array
------------------------
.. code-block:: c

    int a[2] = {0, 1}

.. code-block:: python

    Decl(
        "a",
        Val(
            (Val("0", type_=CTypes.int), Val("1", CTypes.int)),
            CTypes.array))

Assignment
----------
.. code-block:: c

    /* int a = 0 is done above */
    a = a * 3

.. code-block:: python

    Assignment(
        "a",
        Expr(COps.star, Var("a"), Val("3")))

Type of ``Val("3")`` should be inferred from type of ``Var("a")`` or ``Assignment("a", ...)``.

Setting first element of int array
----------------------------------
.. code-block:: c

    /* int a[2] = {0, 1} is done above */
    a[0] = 1

.. code-block:: python

    Assignment(
        ArrayElemByIndex("a", "0"),
        Val("1", type_=CTypes.int))

Setting first element and getting second element of int array
-------------------------------------------------------------
.. code-block:: c

    /* int a[2] = {0, 1} is done above */
    a[0] = a[1]

.. code-block:: python

    Assignment(
        ArrayElemByIndex("a", "0"),
        ArrayElemByIndex("a", "1"))


Struct declaration
------------------
.. code-block:: c

    struct account {
      int id;
      char *first_name;
      char *last_name;
      int balance;
    }

.. code-block:: python

    acc_struct = Struct(
        "account",
        (
            Decl("id", CTypes.int),
            Decl("first_name", CTypes.str),
            Decl("last_name", CTypes.str),
            Decl("balance", CTypes.int)))

.. code-block:: c

    struct account jdoe = {1, "John", "Doe", 123456}

.. code-block:: python

    Decl(
        "jdoe",
        Val(
            {
                "id": Val("1", CTypes.int),
                "first_name": Val("John", CTypes.str),
                "last_name": Val("Doe", CTypes.str),
                "balance": Val("123456", CTypes.int)},
            type_=acc_struct))

.. code-block:: c

    struct account *jcole = {1, "John", "Cole", 123456}

.. code-block:: python

    Decl(
        "jcole",
        Val(
            {
                "id": Val("1", CTypes.int),
                "first_name": Val("John", CTypes.str),
                "last_name": Val("Cole", CTypes.str),
                "balance": Val("123456", CTypes.int)},
            type_=CTypes.ptr(acc_struct)))

``type_=acc_struct`` is equivalent to ``type_=CTypes.struct("account")``.
Can we work without ``CTypes.struct("account")`` feature?

Getting item from struct
------------------------

.. code-block:: c

    /* Declaration of struct account and jcole variable is done above */
    int jcole_id = jcole->id;

.. code-block:: python

    Decl(
        "jcole_id",
        StructElem("jcole", "id"))

.. code-block:: c

    /* Declaration of struct account and jdoe variable is done above */
    int jdoe_id = jdoe.id

.. code-block:: python

    Decl(
        "jdoe_id",
        StructElem("jdoe", "id"))

StructElem determines a type of struct and according to this type does translation.

If
--
.. code-block:: c

    if (cond) {
      body_if
    }

.. code-block:: python

    If(..., (...))

.. code-block:: c

    if (cond) {
      body_if
    } else {
      body_else
    }

.. code-block:: python

    If(..., (...), (...))

While, do-while
---------------
.. code-block:: c

    while (cond) {
      body
    }

.. code-block:: python

    While(..., (...))

.. code-block:: c

    do {
      body
    } while (1)

.. code-block:: python

    DoWhile(CBool.true, (...))

For
---
.. code-block:: c

    for (int i = 0; i < 10; i++) {
      body
    }

.. code-block:: python

    For(
        (
            Decl("i", type_=CTypes.int, value=0),
            Expr(COps.lt, Var("i"), Val("10", type_=CTypes.int)),
            Incr("i")),
        (...))

Function
--------
.. code-block:: c

    int sum(int a, int b) {
      return a + b;
    }

.. code-block:: python

    Func(
        "sum",
        rettype=CTypes.int,
        args=(Decl("a", CTypes.int), Decl("b", CTypes.int)),
        body=(
            Return(Expr(COps.plus, Var("a"), Val("b"))), ))

Should we split this to support function prototypes?

Function from standard library
------------------------------
.. code-block:: c

    #include <stdio.h>
    int main (void) {
      puts("Hello, cgen!");
      return 0;
    }

.. code-block:: python

    c_incl_stdio = Include("stdio.h")
    c_puts = CFuncDescr(
        "puts",
        rettype=CTypes.void,
        args=(CTypes.str, ),
        includes=[c_incl_stdio])

    Func(
        "main",
        rettype=CTypes.int,
        args=(CTypes.void, ),
        body=(
            c_puts(Val("Hello, cgen!")),
            Return(Val("0"))))

Constant and function from standard library
-------------------------------------------
.. code-block:: c

    #include <stdio.h>
    #include <stdlib.h>
    printf("%d\n", EXIT_SUCCESS)

.. code-block:: python

    c_incl_stdio = Include("stdio.h")
    c_incl_stdlib = Include("stdlib.h")

    printf = CFuncDescr(
        "printf",
        rettype=CTypes.void,
        args=(CTypes.str, CTypes.vargs),
        includes=[c_incl_stdio])

    EXIT_SUCCESS = CVarDescr(
        "EXIT_SUCCESS",
        CTypes.int,
        includes=[c_incl_stdlib])

    printf(Val("%d\n"), EXIT_SUCCESS)


Large example
-------------
.. code-block:: python

    c_incl_stdio = Include("stdio.h")

    c_printf = CFuncDescr(
        "printf",
        rettype=CTypes.void,
        args=(CTypes.str, CTypes.vargs),
        includes=[c_incl_stdio])

.. code-block:: python

    file_a = [
        Func(
            "add",
            rettype=CTypes.int,
            args=(Decl("a", CTypes.int), Decl("b", CTypes.int)),
            body=(
                Return(Expr(COps.plus, Var("a"), Val("b"))), ))]

.. code-block:: python

    file_b = [
        Func(
            "main",
            rettype=CTypes.int,
            args=(CTypes.void, ),
            body=(
                Decl("x", Val("1", CTypes.int)),
                Decl("y", Val("2", CTypes.int)),
                Decl("result", FuncCall("add", Var("x"), Var("y"))),
                c_printf(Val("x + y: %d\n"), Var("result")),
                Return(Val("0"))))]

.. code-block:: python

    resulting_ast = merge(file_a, file_b)
    try:
        check(resulting_ast)
    except CheckError as e:
        print(e)
        exit(1)

    chunks = []
    for chunk in generate(resulting_ast):
        chunks.append(chunk)
    print("".join(chunks))

Things to think about
---------------------
- maybe there must be some kind of context object where ``CFuncDescr``
  and ``CVarDescr`` (what about ``struct``\ s?) are "registered"
