- [About](#about)
- [AWS CDK: A Minimalistic Introduction](#aws-cdk-a-minimalistic-introduction)
- [Getting Started With Your TS CDK Project](#getting-started-with-your-ts-cdk-project)
  - [Examples:](#examples)
    - [CDK Walkthrough: Example 1](#cdk-walkthrough-example-1)
    - [CDK Walkthrough: Example 3](#cdk-walkthrough-example-3)
- [Resources](#resources)

# About

The guide is a hands-on introduction to the AWS CDK (V2) with Typescript and how to make use of the `hawk-typescript-template` as your CDK project bootstrap. You'll learn about:
+ Writing an AWS CDK (V2) construct and a stack with TS
+ deploying the stack to an AWS bootstrapped environment
+ changing the stack locally and verifying the changes against the cloud deployment
+ re-deploying the changed stack
+ removing the stack from the AWS environment

# AWS CDK: A Minimalistic Introduction

The AWS CDK enables you to build cloud infrastructure with high-level constructs, testing locally and performing deployments with rollback on error. The core concepts within the CDK are those of `Stack` and `Construct`. A `Construct` is a representation of an AWS resource (ex.: the `s3.Bucket` class represents an Amazon S3 bucket) A `Stack` is a set of `Construct`. There are three levels of constructs:

1. **L1**, or *CFN Resources*. They are a direct representation of all the resources available in AWS CloudFormation, named as `Cfn<resource>` (ex.: `CfnBucket` represents the `AWS::S3::Bucket` AWS CloudFormation resource). Using Cfn resources requires you to explicitly configure all resource properties, which demands a complete understanding of the details of the underlying AWS CloudFormation resource model.
2. **L2** offer a layer of abstraction over **L1** with a higher-level, intent-based API. They provide the defaults, boilerplate, and glue logic otherwise written manually with **L1**. We will typically use **L2** constructs unless an AWS resource is not yet available in **L2** (ex.: `AWS::Redshift`).
3. **L3** or *patterns*. These constructs are designed to help you complete common tasks in AWS, often involving multiple kinds of resources.

Read through the [resources](#resources) to learn more.

# Getting Started With Your TS CDK Project

The section provides a hands-on introduction to CDK so you can start using the template. You can skip the introduction by going directly to the [bootstrap](bootstrap.md) guide.

## Examples: 

### CDK Walkthrough: Example 1

The [Example 1](#cdk-walkthrough-example-1) teaches you about the usage of the `cdk` command by deploying, changing and destroying a stack consisting of one S3 bucket.

Having bootstrapped your project ([guide](bootstrap.md)), open the example stack `lib/ExampleStack.ts` which we shall use for our introduction. The stack deploys a bucket named `examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1>` to profile `<profile>`.

```typescript
import { Stack, StackProps, aws_s3 as s3 } from 'aws-cdk-lib';
import { Construct } from 'constructs';

class ExampleStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const bucket = new s3.Bucket(this, 'BucketDeployedThroughCDK', {
      versioned: false,
    });
  }
}

export default ExampleStack;
```

Notice that it suffices to instantiate the bucket class in the stack's constructor so that the bucket is deployed. The same applies for the stack itself, it suffices to instantiate the stack in the cdk app `bin/app.ts` for it to be deployed to the profile:

```typescript
#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import ExampleStack from '../lib/ExampleStack';

const app = new cdk.App();
new ExampleStack(app, 'ExampleStack', {});
```

So that cdk finds the app, its' path must be specified in `cdk.json` as:

```json
{
    "app": "npx ts-node --prefer-ts-exts bin/app.ts"
}
```

Running cdk will output a CloudFormation template `cdk.out/ExampleStack.template.json` which is a conversion from your app stacks `ExampleStack` into a `.json` file. The cdk output at `cdk.out` is ignored is `.gitignore` as:

```txt
cdk.out
```

This conversion or synthesis can be generated manually with:

```shell
$ npm run synth
```

But as cdk synthesizes the stacks before deploying them, this is an optional step. Having bootstrapped the environment ([guide ](bootstrap.md)) and authenticated with the profile ([guide](aws_profile_authenticate.md)), the stack is deployed with:

```shell
$ npm run deploy -- --profile <profile>

✨  Synthesis time: <time-of-synthesis>s

ExampleStack: deploying...
[0%] start: Publishing <hash>:current_account-current_region
[100%] success: Published <hash>:current_account-current_region
ExampleStack: creating CloudFormation changeset...

 ✅  ExampleStack

✨  Deployment time: <time-of-deployment>s

Stack ARN:
arn:aws:cloudformation:<profile-region>:<profile-account-id>:stack/ExampleStack/????????-????-????-????-????????????

✨  Total time: <total-time>s

```

Let's verify that the new bucket was deployed by issuing a S3-listing API request through the AWS CLI ([guide](aws_profile_authenticate.md)):

```shell
$ aws s3 ls --profile <profile> | grep examplestack
<datetime-of-creation> examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1>
```

You can affect local changes to the infrastructure and verify them against the cloud deployment. Affecting no changes yields:

```shell
$ npm run diff -- --profile dev
Stack ExampleStack
There were no differences

```

Let's add a tag to the bucket by adding a tag to the stack and verify the difference. The current bucket tags are:

```shell
$ aws s3api get-bucket-tagging --bucket examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1> --profile <profile>
{
    "TagSet": [
        {
            "Key": "aws:cloudformation:stack-id",
            "Value": "arn:aws:cloudformation:eu-central-1:<profile-account-id>:stack/ExampleStack/????????-????-????-????-????????????"
        },
        {
            "Key": "aws:cloudformation:stack-name",
            "Value": "ExampleStack"
        },
        {
            "Key": "aws:cloudformation:logical-id",
            "Value": "BucketDeployedThrough<logical-id-1>"
        }
    ]
}
```

Edit the bucket tags in `bin/app.ts` such that:

```typescript
const app = new cdk.App();
const stack = new ExampleStack(app, 'ExampleStack', {});
cdk.Tags.of(stack).add('author', '<author>');
```

Verify that the local stack differs from the cloud deployment:

```shell
$ cdk diff --profile <profile>
Stack ExampleStack
Resources
[~] AWS::S3::Bucket BucketDeployedThroughCDK BucketDeployedThrough<LOGICAL-ID-1> 
 └─ [+] Tags
     └─ [{"Key":"author","Value":"<author>"}]
```

Re-deploy the stack (`cdk deploy --profile <profile>`) and list the bucket tags:

```shell
{
    "TagSet": [
        <...>,
        {
            "Key": "author",
            "Value": "<author>"
        }
    ]
}
```

The infrastructure was changed easily. How about changing something like the bucket name?

```shell
$ npm run diff -- --profile dev
Stack ExampleStack
Resources
[-] AWS::S3::Bucket BucketDeployedThrough<LOGICAL-ID-1> orphan
[+] AWS::S3::Bucket ExampleStackBucket ExampleStackBucket<LOGICAL-ID-2>
```

If the stack is to be re-deployed, the old bucket becomes an `orphan` of the stack and the new bucket will receives a new logical ID, so a re-deploy simply creates a new bucket:

```shell
$ aws s3 ls --profile dev | grep examplestack
<datetime-of-creation> examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1>
<datetime-of-creation> examplestack-examplestackbucket<logical-id-2>-<hash-2>
```

Notice how being a stack `orphan`, the first bucket `examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1>` has lost the stack tags:

```shell
$ aws s3api get-bucket-tagging --bucket examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1> --profile <profile>
{
    "TagSet": [
        {
            "Key": "author",
            "Value": "<author>"
        }
    ]
}
```

Whereas:

```shell
$ aws s3api get-bucket-tagging --bucket examplestack-examplestackbucket<logical-id-2>-<hash-2> --profile <profile>
{
    "TagSet": [
        {
            "Key": "aws:cloudformation:stack-name",
            "Value": "ExampleStack"
        },
        {
            "Key": "aws:cloudformation:logical-id",
            "Value": "ExampleStackBucket<logical-id-2>"
        },
        {
            "Key": "aws:cloudformation:stack-id",
            "Value": "arn:aws:cloudformation:eu-central-1:<profile-account-id>:stack/ExampleStack/????????-????-????-????-????????????"
        },
        {
            "Key": "author",
            "Value": "<author>"
        }
    ]
}
```

Deleting the deployed stack will not delete the stack bucket unless the `removal policy` is specified, but the stack information is deleted from the bucket tags because the bucket becomes a stack `orphan`:

```shell
$ npm run destroy -- --profile <profile>
Are you sure you want to delete: ExampleStack (y/n)? y
ExampleStack: destroying...

 ✅  ExampleStack: destroyed

$ aws s3 ls --profile dev | grep example
2022-07-16 17:27:35 examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1>
2022-07-16 17:33:16 examplestack-examplestackbucket<logical-id-2>-<hash-2>

$ aws s3api get-bucket-tagging --bucket examplestack-examplestackbucket<logical-id-2>-<hash-2> --profile <profile>
{
    "TagSet": [
        {
            "Key": "author",
            "Value": "<author>"
        }
    ]
}
```

So that the stack is destroyed along with its' resources, let's edit the bucket's removal policy, re-deploy the stack, verify the changes, destroy the deployed stack and verify that the stack's resources hasv been completely removed from the AWS environment. `lib/ExampleStack.ts` becomes:

```typescript
const bucketProps = {
    versioned: false,
    removalPolicy: RemovalPolicy.DESTROY,
    autoDeleteObjects: true,
};

// eslint-disable-next-line no-unused-vars
const bucket = new s3.Bucket(this, 'ExampleStackBucket', bucketProps);
```

Once again, the procedure:

```shell
$ npm run deploy -- --profile <profile>

✨  Synthesis time: 5.99s

This deployment will make potentially sensitive changes according to your current security approval level (--require-approval broadening).
Please confirm you intend to make the following modifications:

IAM Statement Changes
┌───┬────────────────────────────────────────┬────────┬────────────────────────────────────────┬────────────────────────────────────────┬───────────┐
│   │ Resource                               │ Effect │ Action                                 │ Principal                              │ Condition │
├───┼────────────────────────────────────────┼────────┼────────────────────────────────────────┼────────────────────────────────────────┼───────────┤
│ + │ ${Custom::S3AutoDeleteObjectsCustomRes │ Allow  │ sts:AssumeRole                         │ Service:lambda.amazonaws.com           │           │
│   │ ourceProvider/Role.Arn}                │        │                                        │                                        │           │
├───┼────────────────────────────────────────┼────────┼────────────────────────────────────────┼────────────────────────────────────────┼───────────┤
│ + │ ${canyoubelievehowcomplexthisnameis.Ar │ Allow  │ s3:DeleteObject*                       │ AWS:${Custom::S3AutoDeleteObjectsCusto │           │
│   │ n}                                     │        │ s3:GetBucket*                          │ mResourceProvider/Role.Arn}            │           │
│   │ ${canyoubelievehowcomplexthisnameis.Ar │        │ s3:List*                               │                                        │           │
│   │ n}/*                                   │        │                                        │                                        │           │
└───┴────────────────────────────────────────┴────────┴────────────────────────────────────────┴────────────────────────────────────────┴───────────┘
IAM Policy Changes
┌───┬───────────────────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────────────┐
│   │ Resource                                                              │ Managed Policy ARN                                                    │
├───┼───────────────────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────────────┤
│ + │ ${Custom::S3AutoDeleteObjectsCustomResourceProvider/Role}             │ {"Fn::Sub":"arn:${AWS::Partition}:iam::aws:policy/service-role/AWSLam │
│   │                                                                       │ bdaBasicExecutionRole"}                                               │
└───┴───────────────────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Do you wish to deploy these changes (y/n)? y

ExampleStack: deploying...
[0%] start: Publishing <hash>:current_account-current_region
[100%] success: Published <hash>:current_account-current_region
ExampleStack: creating CloudFormation changeset...

 ✅  ExampleStack

✨  Deployment time: <time-of-deployment>s

Stack ARN:
arn:aws:cloudformation:eu-central-1:<profile-account-id>:stack/ExampleStack/????????-????-????-????-????????????

✨  Total time: <total-time>s


$ aws s3 ls --profile dev | grep example
2022-07-16 17:27:35 examplestack-bucketdeployedthroughcdk<logical-id-1>-<hash-1>
2022-07-16 17:33:16 examplestack-examplestackbucket<logical-id-2>-<hash-2>
2022-07-17 17:50:45 examplestack-examplestackbucket<logical-id-2>-<hash-3>

$ npm run destroy -- --profile <profile>
Are you sure you want to delete: ExampleStack (y/n)? y
ExampleStack: destroying...

 ✅  ExampleStack: destroyed

$ aws s3 ls --profile dev | grep example
2022-07-16 17:27:35 examplestack-bucketdeployedthroughcdk<logical-id-1>-?????????????
2022-07-16 17:33:16 examplestack-examplestackbucket<logical-id-2>-<hash-1>
```

### [CDK Walkthrough: Example 3](../asset/lambda/example3/README.md)

# Resources

Below you'll find a set of resources that will help you develop your CDK expertise.

+ [AWS CDK - Intro](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
+ [AWS CDK (V2) Migration](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html)
+ [AWS Constructs - API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)
+ [AWS CDK - Write Your First App](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html)
+ [AWS CDK (V2) - API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html)
+ [CDK Workshop](https://cdkworkshop.com/)
+ [CDK Identifiers](https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html)
+ [AWS Overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/aws-overview.pdf)
+ Resources:
  + Redshift
    + [sizing the cluster](https://d1.awsstatic.com/whitepapers/Size-Cloud-Data-Warehouse-on-AWS.pdf)


