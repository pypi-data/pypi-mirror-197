# -*- coding: utf-8 -*-

"""
function in this module is to provide a more user-friendly boto3 API call
without changing the behavior and avoid adding additional feature.
It is the low level api for the :mod:`aws_cloudformation.deploy` module.

Design Principle:

- native boto3 API should NOT have verbose argument
- custom waiter could have verbose argument
"""

from .stacks import (
    StackIterProxy,
    describe_stacks,
    describe_live_stack,
    create_stack,
    update_stack,
    create_change_set,
    describe_change_set,
    describe_change_set_with_paginator,
    execute_change_set,
    delete_stack,
    wait_create_or_update_stack_to_finish,
    wait_delete_stack_to_finish,
    wait_create_change_set_to_finish,
)

from .stacksets import (
    describe_stack_set,
    create_stack_set,
    update_stack_set,
    delete_stack_set,
    describe_stack_instance,
    create_stack_instances,
    update_stack_instances,
    delete_stack_instances,
    StackInstanceIterProxy,
    list_stack_instances,
    wait_deploy_stack_instances_to_stop,
)
