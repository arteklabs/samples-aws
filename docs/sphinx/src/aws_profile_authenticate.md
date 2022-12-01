# About #

The guide explains how to authenticate with your AWS environment.

# Getting started #

Having installed the `aws-cli` (part of the `init.sh`), you have to [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) the `profile` with information regarding your AWS environment, i.e., the `account-id` and the `region`. The file `~/.aws/config` persists the profile configuration under the following structure (for accounts with SSO authentication):

```cfg
[default]
sso_start_url = <aws-org-sso-portal-url>
sso_region = <aws-org-sso-portal-region>
sso_account_id = <authenticated-aws-acc-id>
sso_role_name = <sso-authorization-provided-role>
region = <aws-api-server-region>
output = <aws-api-server-response-format>

[profile <profile>]
...
```

`default` is the default profile should no profile be specified to authenticate with. Notice that:

```cfg
sso_start_url = <aws-org-sso-portal-url>
sso_region = <aws-org-sso-portal-region>
```

To authenticate with SSO, run:

```sh
$ aws sso login --profile <profile>
```

The role provided by the SSO authentication + authorization is accompanied by temporary credentials stored locally at `~/.aws/config/sso/cache/*.json`. These credentials enable the `aws-cli` to request services to the AWS API. The credentials have the following structure:

```json
{
    "startUrl": "<aws-org-sso-portal-url>",
    "region": "<aws-org-sso-portal-region>",
    "accessToken": "<tmp-sso-token>",
    "expiresAt": "<sso-token-expiration-date>"
}
```

When using aws sso login on AWS CLI v2 as of July 27th, 2020, the credentials are stored so they will work with the CLI itself (v2) but don't work on the AWS SDKs and other tools that expect credentials to be readable from  `~/.aws/credentials` (v1). Until a solution is implemented in AWS CLI v2 is is necessary to update the`~/.aws/credentials` file for AWS SSO users by updating/creating the corresponding profile section in `~/.aws/credentials` with temporary role credentials. The `~/.aws/credentials` file has the following structure:

```cfg
[default]
aws_access_key = <iam-access-key-id>
aws_secret_access_key = <iam-access-key>
aws_session_token = <tmp-sso-token>
```

Extract the credentials stored at `~/.aws/config/sso/cache/*.json` to `~/.aws/credentials` by running:

```sh
npm run cpsso -- -p <profile>
```

The SDK and the CDK are now able to request services to the AWS API. Read about authenticating with each one of them at:

+ [SDK authentication](getting_started_with_sdk.md)
+ [CDK authentication](getting_started_with_cdk.md)