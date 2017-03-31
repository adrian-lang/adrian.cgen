import doctest
import unittest


def load_tests(loader, tests, pattern):
    suite = doctest.DocFileSuite("../README.rst")
    tests.addTests(suite)
    return tests
