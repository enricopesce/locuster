#!/usr/bin/env python3

import os

import validators
from aws_cdk import core
from locuster.app_stack import AppStack
from locuster.vpc_stack import VpcStack

env=core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"])

app = core.App()

context = app.node.try_get_context("target_url")

if validators.url(context):
    stack_vpc = VpcStack(app,"locuster-vpc", env=env)
    stack_app = AppStack(app, "locuster", vpc=stack_vpc.vpc, target_url=context,
                     slaves=2, env=env)
else:
    print("The target_url is not a valid URL")

app.synth()