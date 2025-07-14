sphinx-pieces
===================

.. image:: https://travis-ci.org/neongreen/sphinx-pieces.svg?branch=master
    :target: https://travis-ci.org/neongreen/sphinx-pieces

A Sphinx extension for adding unit identifiers to content headers.

Overview
--------

This extension provides a ``unit`` directive that allows you to apply unit identifiers to the headers that follow them. The unit parameter is appended to the header text during document processing.

Installation
------------

Install the extension using pip::

    pip install sphinx-pieces

Or install from source::

    git clone https://github.com/neongreen/sphinx-pieces
    cd sphinx-pieces
    pip install -e .

Configuration
-------------

Add the extension to your Sphinx configuration in ``conf.py``::

    extensions = [
        'sphinx-pieces',
        # ... other extensions
    ]

Usage
-----

The ``unit`` directive is used with the syntax ``.. unit:: parameter`` where ``parameter`` is the unit identifier you want to apply to the following header.

Basic Example
~~~~~~~~~~~~~

.. code-block:: rst

    Main Document
    =============

    .. unit:: fafafa

    Bar
    ---

    Some content here under the Bar section.

    .. unit:: test123

    Another Section
    ~~~~~~~~~~~~~~~

    More content here.

This will render as headers with the unit parameters appended:

- "Bar fafafa"
- "Another Section test123"

Advanced Usage
~~~~~~~~~~~~~~

The directive works with all header levels in reStructuredText:

.. code-block:: rst

    .. unit:: module-a

    Chapter Title
    =============

    .. unit:: section-1

    Major Section
    -------------

    .. unit:: subsec-2

    Subsection
    ~~~~~~~~~~

    .. unit:: point-3

    Subsubsection
    ^^^^^^^^^^^^^

Edge Cases
~~~~~~~~~~

- If a ``unit`` directive is not followed by a header, it will be ignored silently
- Multiple ``unit`` directives can be used throughout a document
- The unit parameter can contain any text (alphanumeric, symbols, spaces)

Development
-----------

Setting Up Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository::

    git clone https://github.com/neongreen/sphinx-pieces
    cd sphinx-pieces

2. Create a virtual environment and install dependencies::

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -e .
    pip install pytest sphinx

Running Tests
~~~~~~~~~~~~~

The extension includes comprehensive tests to ensure functionality. To run the tests::

    # Run all tests
    pytest

    # Run tests with verbose output
    pytest -v

    # Run specific test file
    pytest tests/test_unit_directive.py

    # Run specific test function
    pytest tests/test_unit_directive.py::test_unit_directive_integration

Test Structure
~~~~~~~~~~~~~~

The test suite includes:

- **Basic functionality tests**: Verify that unit directives properly modify following headers
- **Multiple header level tests**: Ensure the directive works with all reStructuredText header levels
- **Edge case tests**: Test behavior when no header follows a unit directive
- **Integration tests**: Full Sphinx build tests with real document processing

The tests use Sphinx's testing framework to create temporary documentation projects and verify the generated output.

Example Test Document
~~~~~~~~~~~~~~~~~~~~~

The tests use sample documents like this:

.. code-block:: rst

    Test Document
    =============

    .. unit:: test123

    Main Title
    ==========

    Some content under the main title.

    .. unit:: fafafa

    Bar
    ---

    Some content here under Bar.

    Regular Header
    --------------

    This header should not be affected.

Building Documentation Locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To test the extension with a real Sphinx project:

1. Create a test directory with ``conf.py``::

    extensions = ['sphinx-pieces']
    master_doc = 'index'

2. Create an ``index.rst`` file with unit directives
3. Build the documentation::

    sphinx-build -b html . _build

Links
-----

- Source: https://github.com/neongreen/sphinx-pieces
- Bugs: https://github.com/neongreen/sphinx-pieces/issues
