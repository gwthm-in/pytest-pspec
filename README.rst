pytest-pspec
==============

.. image:: https://travis-ci.org/gowtham-sai/pytest-pspec.svg?branch=master
    :target: https://travis-ci.org/gowtham-sai/pytest-pspec

.. image:: https://codecov.io/gh/gowtham-sai/pytest-pspec/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/gowtham-sai/pytest-pspec

A `pspec format`_ reporter for pytest

.. _pspec format: https://en.wikipedia.org/wiki/RSpec

.. image:: https://i.imgur.com/cCMJXHe.png

Install
-------

::

    pip install pytest-pspec


Usage
-----

Add the parameter `--pspec` when running `pytest`. Ex:

::

    pytest --pspec your-tests/

Tip: If you don't want to type ``--pspec`` every time you run ``pytest``, add it
to `addopts <https://docs.pytest.org/en/latest/customize.html#confval-addopts>`_
in your `ini file <https://docs.pytest.org/en/latest/customize.html#initialization-determining-rootdir-and-inifile>`_. Ex:

.. code-block:: ini

    # content of pytest.ini
    # (or tox.ini or setup.cfg)
    [pytest]
    addopts = --pspec


Demo Code
---------

Add the doc strings Ex:

.. code-block:: python

    import unittest

    class TestWayTwo(unittest.TestCase):
        "Pspec Python TDD"

        def test_should_add(self):
            "it adds two integers and returns integer"
            self.assertEqual(2+2, 4)

        def test_should_find_difference_between_integers(self):
            self.assertEqual(4-2, 2)

running ``pytest --pspec`` outputs

.. code-block::

    demo
     ✓ it adds two integers and returns integer
     ✓ should find difference between integers



Configuration file options
--------------------------

pspec\_format
~~~~~~~~~~~~~~~

Specifies pspec report format, ``plaintext`` or ``utf8`` (default:
``utf8``). Ex:

.. code:: ini

    # content of pytest.ini
    # (or tox.ini or setup.cfg)
    [pytest]
    pspec_format = plaintext

::

    $ pytest test_demo.py
    ============================= test session starts ==============================
    platform darwin -- Python 3.5.0, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
    rootdir: /private/tmp/demo, inifile: pytest.ini
    plugins: pspec-dev
    collected 2 items

    test_demo.py
    Pytest pspec
     [x] prints a BDD style output to your tests
     [x] lets you focus on the behavior
