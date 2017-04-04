adrian.cgen
===========
.. image:: https://travis-ci.org/adrian-lang/adrian.cgen.svg?branch=master
    :target: https://travis-ci.org/adrian-lang/adrian.cgen

``adrian.cgen`` is a Python EDSL for C code generation.


Installation
------------
Library is `available on PyPI <https://pypi.python.org/pypi/adrian.cgen>`_,
you can use ``pip`` for installation:

.. code-block:: console

    $ pip install adrian.cgen


Running tests
-------------
.. code-block:: console

    $ tox


Getting coverage
----------------
Collect info:

.. code-block:: console

    $ tox -e coverage

View HTML report:

.. code-block:: console

    $ sensible-browser .tox/coverage/tmp/cov_html/index.html


Checking code style
-------------------
Run code checkers:

.. code-block:: console

    $ tox -e checks


Getting documentation
---------------------
Build HTML docs:

.. code-block:: console

    $ tox -e docs

View built docs:

.. code-block:: console

    $ sensible-browser .tox/docs/tmp/docs_html/index.html
