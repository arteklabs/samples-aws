"""This is the project's task runner.
"""
from invoke import task
import os

@task
def docs(ctx, step='build'):
    """Generate documentation."""
    cmds = [
        "cd docs/sphinx",
        "make html",
        "cp -a _build/html/. ..",
        "make clean",
        "echo && echo && echo && echo Your static documentation pages can be found at \'docs\' \(Ctrl+Click\) && echo",
    ]

    ctx.run(';'.join(cmds))
