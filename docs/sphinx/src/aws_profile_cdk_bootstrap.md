# About

The guide shows how to bootstrap your AWS environment.

# Motivation

TODO

# Bootstrapping

Having authenticated with your AWS profile ([guide](aws_profile_authenticate.md)), and installed the project's dependencies ([guide](init.md)), bootstrap the environment by running:

`npm run boot aws:/<profile-account-id>/<profile-region> -- --profile <profile>`

or

`cdk bootstrap aws:/<profile-account-id>/<profile-region> --profile <profile>`