=====
Debug
=====

The documentation shows how to configure vscode to debug the code.

VSCode Configuration: Python Interpreter
----------------------------------------

The debugger needs to know the path to the libs installed in your project's virtual environment. Define the python interpreter path with:

1. ``ctrl+shift+P``
2. ``>Python: Select Interpreter``
3. ``Entire Workspace``
4. ``+Enter interpreter path...``
5. ``Find...``
6. ``<your-project-abs-path>/.env/bin/python3``


Debug
-----

``.vscode/launch.json`` contains unit test configurations for the vscode debugger.


The example below defines the configuration to debug the command ``inv ci --suite utils --user <user> --password <password>``. Notice how the ``invoke`` module is specified. Add to ``.vscode/launch.json::configurations``:

.. code-block:: json

    {
        "name": "suite: redshift",
        "type": "python",
        "request": "launch",
        "module": "invoke",
        "python": "${workspaceFolder}/.env/bin/python3",
        "console": "integratedTerminal",
        "args": [
        "ci", "--suite", "redshift",
        "--user", "<user>",
        "--password", "<password>",
        ],
    }

Disclaimer
~~~~~~~~~~

+ It is recommended that the unit tests all be added manually to ``.vscode/launch.json`` so they can be conveniently debugged from vscode. It is FORBIDDEN to write secrets in  ``.vscode/launch.json``.
+ Don't forget to specify the package's version in ``.vscode/launch.json::version``.
