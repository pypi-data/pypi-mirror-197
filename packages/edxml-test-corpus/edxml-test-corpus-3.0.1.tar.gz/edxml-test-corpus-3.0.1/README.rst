|license| |pyversion|

.. |license| image::  https://img.shields.io/badge/License-MIT-blue.svg
.. |pyversion| image::  https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue

====================================
The EDXML Test Corpus Python Package
====================================

This is a Python package that provides the EDXML test corpus. It can be used to include the test corpus in Python projects by adding this package as a dependency.

Installing
==========

The package can be installed using Pip::

  pip install edxml-test-corpus

Usage
=====

Besides the corpus data files the package also provides a constant which contains the path to the root directory containing the data files. It can be imported like this::

    from edxml_test_corpus import CORPUS_PATH

