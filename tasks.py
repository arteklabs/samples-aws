"""
`invoke <https://www.pyinvoke.org/>`_ is the project's task runner. The tasks are defined at ``tasks.py``.
"""
from invoke import task
import os
import sys
from pathlib import Path

docs_docker_image = 'python:3.8'
docs_debug_container_name = 'samples_aws_docs'
sphinx_server_default_port = '8000'
docker_host_sphinx_server_default_port = '8010'
docs_debug_mnt_path = f"{os.getcwd()}/docs/sphinx/_build/html"
docs_debug_container_path = "/root"

@task
def git(ctx, clone=False, push=''):
    """Git ops.

    Clone
    -----

    Clone an arteklabs exercise repo.

    Push
    ----

    Stage, commit and push.

    TODO: may commit more than its supposed to.

    :param ctx: _description_
    :type ctx: _type_
    :param clone: True
    :type clone: _type_
    :param push: the commit message
    :type push: _type_
    """

    if clone:
        repo = input('repo: ')
        if not repo:
            sys.exit("Please insert the valid name of an arteklabs exercise: 'samples-*'")
        usr_name = input('user: ')
        if not usr_name:
            sys.exit('Please provide the name of a github user')
        usr_email = input('user email: ')
        if not usr_email:
            sys.exit('Please provide the email of a github user')
        home = str(Path.home())
        repo_path = input('path [~/arteklabs]: ') or f'{home}/arteklabs'
        if os.path.exists(repo_path):
            cmds = [
                f"git clone github:lifespline/{repo}.git {repo_path}/{repo}",
                f"git -C {repo_path}/{repo} config user.name {usr_name}",
                f"git -C {repo_path}/{repo} config user.email {usr_email}",
            ]
            for cmd in cmds:
                ctx.run(cmd, hide='both')
    if push:
        cmds = [
            f"git add docs/sphinx/src/backlog/requirements",
            f"git add docs/sphinx/src/backlog/requirements.rst",
            f"git add docs/sphinx/src/backlog/problem_statements.rst",
            f"git add docs/sphinx/src/backlog/issues.rst",
            f"git commit -m \"{push}\"",
            "git push"
        ]
        for cmd in cmds:
            ctx.run(cmd, hide='both')


@task
def docs(ctx, step='build', port=docker_host_sphinx_server_default_port, verbose=False):
    """Documentation ops.

    Build ``--step build``
    -----------------------------

    Builds the docs and checks for WARNINGS or ERRORS. If none occurs, the docs are published to the repo.

    Build ``--step run --port PORT``
    -----------------------------------------

    Builds the docker image and runs the container to debug the docs with a contaneirized sphinx server listenning on 0.0.0.0:``port``.

    Debug ``--step debug --port PORT``
    ----------------------------------

    Start a debugging local sphinx python server in a docker container.

    Stop ``--step stop``
    ----------------

    Stop the local debugging container with a sphinx python server.

    :param step: _description_, defaults to 'build'
    :type step: str, optional
    :param verbose: _description_, defaults to False
    :type verbose: bool, optional
    """
    if step == 'build':

        cmds = [
            "cd docs/sphinx",
            "make html",
        ]

        if verbose:
            res = ctx.run(';'.join(cmds))
        else:
            res = ctx.run(';'.join(cmds), hide='both')

        if 'WARNING' in res.stdout:
            sys.exit("There seems to be a WARNING in the build process. Please fix it before publishing the docs. Add the flag '--verbose' to see the stdout.")
        elif res.stderr:
            sys.exit("There seems to be an ERROR in the build process. Add the flag '--verbose' to see the stderr.")

        print('build: OK')

    if step == 'run':
        cmd = f"""
        # run container it it doesn't exist locally already
        if [[ "docker container inspect -f '{{{{.State.Running}}}}' {docs_debug_container_name}" != "true" ]]; then
            docker run \
                --rm \
                -d \
                --name {docs_debug_container_name} \
                -p 0.0.0.0:{port}:{sphinx_server_default_port} \
                --mount type=bind,source={docs_debug_mnt_path},target={docs_debug_container_path} \
                {docs_docker_image} \
                sleep infinity
        fi

        # have the container running the sphinx server
        docker exec \
            -d \
            -w {docs_debug_container_path} \
            {docs_debug_container_name} \
            python -m http.server
        """
        
        if verbose:
            ctx.run(cmd)
        else:
            ctx.run(cmd, hide='both')

        print('local sphinx run: OK')
        print(f'container: {docs_debug_container_name}')
        print(f'host: http://0.0.0.0:{port}')
        print('stop: inv docs --stop')

    if step == 'stop':
        ctx.run(f'docker stop {docs_debug_container_name}')

    if step == 'publish':
        docs(ctx,  step='build', port=port)
        cmds = [
            "cp -a docs/sphinx/_build/html/. docs",
            "cd docs/sphinx",
            "make clean",
            "cd ../..",
            "git add docs",
            "git commit -m \"publish docs to githubpages\""
        ]

        if verbose:
            res = ctx.run(';'.join(cmds))
        else:
            res = ctx.run(';'.join(cmds), hide='both')

        print('github pages publish: OK')

    if step == 'clean':
        cmds = [
            "cd docs/sphinx",
            "make clean",
            "cd ..",
            "rm -rf _downloads",
            "rm -rf _images",
            "rm -rf src",
            "rm -rf .buildinfo",
            "rm -rf _sources",
            "rm -rf _static",
            "rm -rf genindex.html",
            "rm -rf index.html",
            "rm -rf objects.inv",
            "rm -rf search.html",
            "rm -rf searchindex.js",
            "rm -rf py-modindex.html",
        ]

        print('local clean: OK')

