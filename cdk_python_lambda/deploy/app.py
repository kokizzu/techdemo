#!/usr/bin/env python3
"""
Cloudformation generation
"""
import aws_cdk as cdk

import my_stack


app = cdk.App()

# Best practice is to explicitly set account ids and region
ACME_ENV_WEST = cdk.Environment(account="123412341234", region="us-west-2")

my_stack.MyStack(app,
        "acme-prod-DemoLambda",
        env=ACME_ENV_WEST,
        )

app.synth()
