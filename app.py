#!/usr/bin/env python3

import os
from aws_cdk import core
from locuster.app_stack import AppStack
from locuster.vpc_stack import VpcStack

env=core.Environment(
    account=os.environ["CDK_DEFAULT_ACCOUNT"],
    region=os.environ["CDK_DEFAULT_REGION"])

app = core.App()

context = app.node.try_get_context("target_url")

stack_vpc = VpcStack(app,"locuster-vpc", env=env, from_vpc_name="VPC-RD")
stack_app = AppStack(app, "locuster", vpc=stack_vpc.vpc, slaves=10, env=env)

app.synth()