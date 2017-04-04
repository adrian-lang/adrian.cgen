import os

import setuptools


def _get_long_description():
    path = os.path.join(os.path.dirname(__file__), "README.rst")
    with open(path, "rb") as file:
        contents = file.read()
    return contents.decode("utf-8")


setuptools.setup(
    name="adrian.cgen",
    description="EDSL for C code generation",
    long_description=_get_long_description(),
    version="1.0.0",
    packages=setuptools.find_packages(),
    install_requires=["paka.funcreg"],
    extras_require={"testing": []},
    include_package_data=True,
    namespace_packages=["adrian"],
    zip_safe=False,
    url="https://github.com/adrian-lang/adrian.cgen",
    keywords="c codegen edsl",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython"],
    license="BSD",
    author="Adrian language team",
    author_email="i@93z.org")
