# About

The guide shows how to setup and use the AWS CLI (V2).

# Getting Started

AWS CLI enables you to make API calls to AWS services in an AWS profile `<profile>` from the CLI. Start by bootstrapping your project ([guide](init.md)) so that the AWS CLI and the AWS profile `<profile>` are properly configured.

We'll be having the `S3` service API as an example. Listing the buckets in `<profile>`:

```shell
$ aws s3 ls --profile <profile>
<datetime-of-creation> <bucket-name>
```

Listing a bucket in `<profile>`:

```shell
$ aws s3 ls s3://<bucket> --profile <profile>
<datetime-of-creation> <bytes> <object>
```

Listing a bucket object in `<profile>`:

```shell
$ aws s3 ls s3://<bucket>/<object>/ --profile <profile>
<datetime-of-creation> <bytes> <object>
```

An object is either a file or a folder.

To remove a bucket in `<profile>`, the bucket must be empty and all versions of the bucket objects must have been deleted. Notice how the service handling the deletion of the S3 bucket changes from the service handling the listing of the S3 bucket. Different AWS services implement the API for an AWS service like S3. These services are not to be mistaken for the services that AWS exposes like `S3`, `Athena`, *etc*, these are simply services implementing the API of the aforementioned services.

```shell
$ aws s3api delete-bucket --bucket <bucket> --profile <profile>
<datetime-of-creation> <bytes> <object>
```


Removing a bucket object in `<profile>`:

```shell
$ aws s3 rm s3://<bucket>/<object>/ --profile <profile>
delete: s3://<bucket>/<object>/
```
