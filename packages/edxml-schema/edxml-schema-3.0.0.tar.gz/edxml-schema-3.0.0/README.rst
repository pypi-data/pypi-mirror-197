|license| |pyversion|

.. |license| image::  https://img.shields.io/badge/License-MIT-blue.svg
.. |pyversion| image::  https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue

===============================
The EDXML Schema Python Package
===============================

This is a Python package that provides the EDXML RelaxNG schema. It can be used to include the schema in Python projects by adding this package as a dependency.

Installing
==========

The package can be installed using Pip::

  pip install edxml-schema

Usage
=====

Besides the actual schema the package also provides constants which contain the path to the various versions of the schema. These can be imported like this:

.. code-block:: python

    from edxml_schema import SCHEMA_PATH_3_0

    print(f"The schema can be found here: {SCHEMA_PATH_3_0}")
