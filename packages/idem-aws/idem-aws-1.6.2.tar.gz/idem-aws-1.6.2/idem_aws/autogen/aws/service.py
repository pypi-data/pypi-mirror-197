"""Read & extract service metadata and its available operations"""
import re

import boto3


def parse_resource_and_operations(
    hub, service_name: str, session: "boto3.session.Session"
):
    """
    Get resource and their available operations for client initialized for a given service

    @returns
        Mapping of resource to its methods and corresponding boto3 operation_name.
        {
            "resource": {
                { "method" : "operation_name" }
            }
        }
    """
    operations = {}
    client = session.client(service_name=service_name, region_name="us-west-2")

    for op in client.meta.method_to_api_mapping:
        try:
            verb, resource = op.split("_", maxsplit=1)
            if re.match(rf"\w+[^aoius]s$", resource):
                resource = hub.tool.format.inflect.singular(resource)
            # Special case for resource names that end with apis
            if resource.endswith("apis"):
                resource = resource[:-1]
            if resource not in operations:
                operations[resource] = {}
            operations[resource][verb] = op
        except ValueError:
            hub.log.error("Failure in extracting operation metadata")

    return operations


def parse_docstring(hub, session: "boto3.session.Session", service_name: str):
    """
    Get service description
    """
    client = session.client(service_name=service_name, region_name="us-west-2")
    plugin_docstring = hub.tool.format.html.parse(client._service_model.documentation)
    return "\n".join(hub.tool.format.wrap.wrap(plugin_docstring, width=120))
