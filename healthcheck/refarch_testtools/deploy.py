import datetime
import logging

import boto3
from botocore.exceptions import WaiterError

_logger = logging.getLogger("deploy")


def deploy_stack(template_url, template_parameters, region, stack_base_name="refArchTest", extra_parameters={}):
    stack_name = _create_stack_name(stack_base_name)
    _logger.info(f"Deploying stack {stack_name}")

    cloudformation = boto3.resource("cloudformation", region_name=region)
    stack = cloudformation.create_stack(
        StackName=stack_name,
        TemplateURL=template_url,
        Parameters=template_parameters,
        Capabilities=["CAPABILITY_IAM"])

    try:
        _wait_for_create_complete(cloudformation, stack)
        stack.reload()

        return stack
    except WaiterError as e:
        raise

def _wait_for_create_complete(cloudformation, stack):
    cf_client = cloudformation.meta.client
    creation_waiter = cf_client.get_waiter("stack_create_complete")
    creation_waiter.wait(StackName=stack.stack_name)


def delete_stack(stack):
    stack.delete()

    deletion_waiter = stack.meta.client.get_waiter("stack_delete_complete")
    deletion_waiter.wait(StackName=stack.stack_name)


def get_stack_output_value(stack, outputKey):
    output = next(output for output in stack.outputs if output["OutputKey"] == outputKey)
    return output["OutputValue"]


def _create_stack_name(name_base):
    return name_base + "-" + datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S")


def log():
    _logger.info("info")
    _logger.debug("debug")
    _logger.error("error")
    _logger.critical("critical")
    _logger.warning("warning")
