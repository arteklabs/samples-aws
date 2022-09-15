===================
Semantic Versioning
===================

About
-----

The Documentation shows how to version your project with ``minimal semantic versioning``.

Getting Started
---------------

Syntax: ``<MAJOR>.<MINOR>.<PATCH>[-<identifier>]``, where:

* ``MAJOR`` backwards incompatible changes
* ``MINOR`` add backwards compatible functionality (non-negative integer)
* ``PATCH`` add backwards compatible bug fixes (non-negative integer). A bug fix is that which fixes incorrect behaviour.
* ``[-<identifier>]`` optional pre-release identifiers. Examples:
  * 1.0.0-alpha
  * 1.0.0-alpha.1
  * 1.0.0-0.3.7
  * 1.0.0-x.7.z.92
  * 1.0.0-x-y-z.–.

``<MAJOR>``, ``<MINOR>`` and ``<PATCH>`` are incrementing positive integer values. When ``<MAJOR>`` increases, ``<MINOR>`` resets to 0. When ``<MINOR>`` increases, ``<PATCH>`` resets to 0.

``[-<identifier>]`` is an alphanumeric value of the format ``[-.a-zA-Z0-9]+``. It MUST follow the rules that apply to ``<MAJOR>.<MINOR>.<PATCH>``.

Resources
---------

* `semver <https://semver.org/>`_
