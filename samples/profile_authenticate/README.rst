AWS Profile Authentication
==========================

CLI Authentication
------------------

A ``profile`` is a collection of settings and credentials that you can apply to a AWS CLI command. When you specify a profile to run a command, the settings and credentials are used to run that command. Multiple SSO profiles can be stored in the ``config`` (``.aws/config``) and ``credentials`` (``.aws/credentials``, ``sso/cache/*.json``) files. If your profile has SSO, configure the profile with (having installed the ``aws-cli-v2``):

.. code:: shell

   $ aws sso configure --profile $PROFILE
   SSO session name (Recommended): SSO-PORTAL
   SSO start URL [None]: https://SSO-PORTAL-URL.awsapps.com/start/
   SSO region [None]: REGION
   SSO registration scopes [sso:account:access]: sso:account:access
   ...
   There are NUMBER_OF_ACCOUNTS_WITH_SSO_ACCESS AWS accounts available to you.
   Using the account ID 123456789ABC
   There are NUMBER_OF_ROLES roles available to you.
   Using the role name "ROLE"
   CLI default client Region [None]: eu-central-1
   CLI default output format [None]: json

Notice that is has been created in ``~/.aws/config``:

.. code-block:: cfg

   [profile PROFILE]
   sso_session = SSO-PORTAL
   sso_account_id = 123456789ABC
   sso_role_name = ROLE
   region = REGION
   output = json

   [sso-session SSO-PORTAL]
   sso_region = REGION
   sso_start_url = https://SSO-PORTAL-URL.awsapps.com/start/
   sso_registration_scopes = sso:account:access

The profile is given temporary access credentials through (``sso/cache/*.json``):

.. code:: shell

   $ aws sso login --profile $PROFILE

The profile role temporary credentials provided by the SSO authentication + authorization are stored locally at ``~/.aws/config/sso/cache/*.json``. These credentials enable the ``aws-cli`` to request services to the AWS API. The credentials have the following structure:

.. code-block:: json

   {
       "startUrl": "https://SSO-PORTAL-URL.awsapps.com/start/",
       "region": "REGION",
       "accessToken": "TMP_SSO_TOKEN",
       "expiresAt": "TMP_SSO_TOKEN_EXP_DATE"
   }

SDK/CDK Authentication
----------------------

When using aws sso login on AWS CLI v2 as of July 27th, 2020, the credentials are stored so they will work with the CLI itself (v2) but don't work on the AWS SDKs and other tools that expect credentials to be readable from  ``~/.aws/credentials`` (v1). Until a solution is implemented in AWS CLI v2 is is necessary to update the ``~/.aws/credentials`` file for AWS SSO users by updating/creating the corresponding profile section in ``~/.aws/credentials`` with temporary role credentials. The ``~/.aws/credentials`` file has the following structure:

.. code-block:: cfg

   [default]
   aws_access_key = IAM_ACCESS_KEY_ID
   aws_secret_access_key = IAM_ACCESS_KEY
   aws_session_token = TMP_ACCESS_TOKEN


Extract the credentials stored at ``~/.aws/config/sso/cache/*.json`` to ``~/.aws/credentials`` by running:

.. code:: shell

   npm run cpsso -- -p  PROFILE
