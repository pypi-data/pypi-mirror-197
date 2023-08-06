graphqldomain
==============

.. image:: https://readthedocs.org/projects/graphqldomain/badge/?version=latest
    :target: https://graphqldomain.readthedocs.org
    :alt: Documentation

.. image:: https://github.com/AWhetter/graphqldomain/actions/workflows/main.yml/badge.svg?branch=main
    :target: https://github.com/AWhetter/graphqldomain/actions/workflows/main.yml?query=branch%3Amain
    :alt: Github Build Status

.. image:: https://img.shields.io/pypi/v/graphqldomain.svg
    :target: https://pypi.org/project/graphqldomain/
    :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/graphqldomain.svg
    :target: https://pypi.org/project/graphqldomain/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/python/black
    :alt: Formatted with Black

A Sphinx domain for describing GraphQL schemas.


Getting Started
---------------

The following steps will walk through how to add ``graphqldomain`` to an existing Sphinx project.
For instructions on how to set up a Sphinx project,
see Sphinx's documentation on
`Getting Started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.


Installation
~~~~~~~~~~~~

```graphqldomain`` can be installed through pip:

.. code-block:: bash

    pip install graphqldomain

Next, add ``graphqldomain`` to the ``extensions`` list in your Sphinx project's `conf.py`.

.. code-block:: python

    extensions.append("graphqldomain")


Usage
-----

Each directive accepts a small snippet of the original schema.
For more detailed usage, see the documentation:
https://graphqldomain.readthedocs.io/en/latest/

.. code-block:: rst

   .. gql:directive:: @slow(super: Boolean = false) on FIELD_DEFINITION | ARGUMENT_DEFINITION

      Indicates that the usage of this field or argument is slow,
      and therefore queries with this field or argument should be made sparingly.

      :argument super: Whether usage will be super slow, or just a bit slow.

   .. gql:enum:: CharacterCase

      The casing of a character.

      .. gql:enum:value:: UPPER

         Upper case.

      .. gql:enum:value:: LOWER

         Lower case.

   .. gql:input:: Point2D

      A point in a 2D coordinate system.

      .. gql:input:field:: x: Float

         The ``x`` coordinate of the point.

      .. gql:input:field:: y: Float

         The ``y`` coordinate of the point.

   .. gql:interface:: NamedEntity

      An entity with a name.

      .. gql:interface:field:: name(lower: Boolean = false): String

         The name of the entity.

         :argument lower: Whether to lowercase the name or not.

   .. gql:type:: Person implements NamedEntity

      A human person.

      .. gql:type:field:: age: Int

         How old the person is in years.

      .. gql:type:field:: picture: Url

   .. gql:union:: Centre = Person | Point2D

      A possible centre of the universe.


Contributing
------------


Running the tests
~~~~~~~~~~~~~~~~~

Tests are executed through `tox <https://tox.readthedocs.io/en/latest/>`_.

.. code-block:: bash

    tox


Code Style
~~~~~~~~~~

Code is formatted using `black <https://github.com/python/black>`_.

You can check your formatting using black's check mode:

.. code-block:: bash

    tox -e formatting

You can also get black to format your changes for you:

.. code-block:: bash

    black graphqldomain.py tests/


Versioning
----------

We use `SemVer <https://semver.org/>`_ for versioning. For the versions available, see the `tags on this repository <https://github.com/AWhetter/graphqldomain/tags>`_.


License
-------

This project is licensed under the MIT License.
See the `LICENSE.rst <LICENSE.rst>`_ file for details.
