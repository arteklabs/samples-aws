============
Unit Testing
============

The section shows how to design and develop, run, debug and document the unit tests on the project. TODO get all this documentation from the `test` module.

BDD And TDD
-----------

TODO

Executing
---------

TODO

Debugging
---------


VSCode Configuration: Python Interpreter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Read the ``VSCode Python Interpreter`` documentation.

Debugging
~~~~~~~~~

``.vscode/launch.json`` contains unit test configurations for the vscode debugger.


Debugging pytest unit tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example below defines the configuration for the unit test ``no_args_invalid_user`` of the test suite ``redshift``, i.e., the ``test_redshift_connection_no_args_invalid_user`` unit test of the ``test/test_redshift_connection.py`` test suite. Add to ``.vscode/launch.json::configurations``:

.. code-block:: json

    {
        "version": "<version>",
        "configurations": [
            {
                "name": "suite: redshift, test: no_args_invalid_user",
                "type": "python",
                "request": "launch",
                "module": "pytest",
                "python": "${workspaceFolder}/.env/bin/python3",
                "console": "integratedTerminal",
                "args": [
                    "test/test_redshift_connection.py::test_redshift_connection_no_args_invalid_user", "-s"
                ],
            },
        ]
    }

 The example below defines the configuration for the unit test ``invalid_user`` of the test suite ``redshift``. Notice how the secret values are persisted in plain test in the script. This is why ``.vscode/launch.json`` is ignored in ``.vscode/.gitignore``.

.. code-block:: json

    {
        "version": "<version>",
        "configurations": [
            {
                "name": "suite: empower, test: no_args_invalid_user",
                "type": "python",
                "request": "launch",
                "module": "pytest",
                "python": "${workspaceFolder}/.env/bin/python3",
                "console": "integratedTerminal",
                "args": [
                    "test/test_redshift_connection.py::test_redshift_connection_no_args_invalid_user", "--user", "<user>"
                    , "--password", "<password>"
                ],
            },
        ]
    }

To debug the unit test, place you breakpoints on the desired lines of code, and debug.


Disclaimer
~~~~~~~~~~

* It is recommended that the unit tests all be added manually to ``.vscode/launch.json`` so they can be conveniently debugged from vscode. It is FORBIDDEN to write secrets in  ``.vscode/launch.json``.
* Don't forget to specify the package's version in ``.vscode/launch.json::version``.

Documenting
-----------

TODO
