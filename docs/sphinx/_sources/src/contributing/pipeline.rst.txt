=============
CICD Pipeline
=============

About
-----

The documentation shows how to configure a CICD pipeline with ``github actions``.

Getting Started
---------------

The automated agent authenticates by fetching the `pat` directly from your access tokens. The contents of `azure-pipelines.yml` must contain:


.. code-block:: yml

  variables:
    feed_name: <org>
    dist: dist/*

  steps:
  - script: |
      # cmds here

  - task: TwineAuthenticate@1
    inputs:
      artifactFeed: ${{ variables.feed_name }}

  - script: |
      # cmds here

      python3 -m twine \
      upload -r ${{ variables.feed_name }} \
      --config-file $(PYPIRC_PATH) ${{ variables.dist }}
