DESCRIBE_FUNCTIONS = ("get", "search", "describe")

LIST_FUNCTIONS = ("describe", "search", "list")

DELETE_FUNCTIONS = (
    "delete",
    "disassociate",
    "reject",
    "deallocate",
    "unassign",
    "deregister",
    "deprovision",
    "revoke",
    "release",
    "terminate",
    "cancel",
    "disable",
)

CREATE_FUNCTIONS = (
    "create",
    "associate",
    "accept",
    "allocate",
    "assign",
    "register",
    "provision",
    "authorize",
    "run",
    "enable",
    "upload",
    "put",
    "publish",
    "request",
    "put",
    "add",
)

UPDATE_FUNCTIONS = ("modify",)

NAME_PARAMETER = {
    "default": None,
    "doc": "An Idem name of the resource",
    "param_type": "str",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

RESOURCE_ID_PARAMETER = {
    "default": None,
    "doc": "An identifier of the resource in the provider",
    "param_type": "str",
    "required": False,
    "target": "hardcoded",
    "target_type": "arg",
}

PRESENT_REQUEST_FORMAT = """
    # TODO: result["old_state"] and result["new_state"] should be populated with the same parameters as the present() input parameters.
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        {{ function.hardcoded.resource_function_call }}
        before = {{ function.hardcoded.describe_function_call }}
    if before:
        # TODO perform day-2 modifications as needed here
        # TODO if ctx.test is True, no update call should be made to AWS, but parameter values should still be compared
        # and the "new_state" return should reflect the updated value that would be made if actual update calls happened.
        resource_updated = True
        if ctx.get("test", False) and resource_updated:
            # TODO populate result["new_state"]
            result["comment"] = (f"Would update aws.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource }} '{name}'",)
            return result
        if not resource_updated:
            result["comment"] = (f"'{name}' already exists",)
    else:
        if ctx.get("test", False):
            # TODO populate result["new_state"]
            result["comment"] = (f"Would create aws.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource }} {name}",)
            return result
        try:
            ret = await {{ function.hardcoded.create_function }}(
                ctx,
                {{ "ClientToken=name," if function.hardcoded.has_client_token }}
                **{{ parameter.mapping.kwargs|default({}) }}
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = (f"Created '{name}'",)
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)
            result["result"] = False

    {{ function.hardcoded.waiter_call }}
    # TODO perform other modifications as needed here
    ...

    try:
        if ctx.get("test", False):
            # TODO populate result["new_state"]
            ...
        elif (not before) or resource_updated:
            after = {{ function.hardcoded.describe_function_call }}
            result["new_state"] = after
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] = result["comment"] + (str(e),)
        result["result"] = False
    return result
"""

ABSENT_REQUEST_FORMAT = """
    result = dict(comment=(), old_state=None, new_state=None, name=name, result=True)
    {{ function.hardcoded.resource_function_call }}
    before = {{ function.hardcoded.describe_function_call }}

    if not before:
        result["comment"] = (f"'{name}' already absent",)
    elif ctx.get("test", False):
        # TODO populate result["new_state"]
        result["comment"] = (f"Would delete aws.{{ function.hardcoded.service_name }}.{{ function.hardcoded.resource }} '{name}'",)
        return result
    else:
        # TODO populate result["old_state"]
        result["old_state"] = before
        try:
            ret = await {{ function.hardcoded.delete_function }}(
                ctx,
                {{ "ClientToken=name," if function.hardcoded.has_client_token }}
                **{{ parameter.mapping.kwargs|default({}) }}
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = (f"Deleted '{name}'",)
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = result["comment"] + (f"{e.__class__.__name__}: {e}",)

    {{ function.hardcoded.waiter_call }}

    return result
"""

DESCRIBE_REQUEST_FORMAT = """
    result = {}
    ret = await {{ function.hardcoded.list_function}}(ctx)

    if not ret["status"]:
        hub.log.debug(f"Could not describe {{ function.hardcoded.resource }} {ret['comment']}")
        return {}

    # TODO: The parameters of the describe() output should be the same as the present() input parameters.
    for {{ function.hardcoded.resource }} in ret["ret"]["{{ function.hardcoded.list_item }}"]:
        # Including fields to match the 'present' function parameters
        # TODO convert the dictionary values from string to object by removing the quotes.
        # TODO From 'resource[param]' to resource[param]
        new_{{ function.hardcoded.resource }} = {{ function.hardcoded.present_params }}
        result[{{ function.hardcoded.resource }}["{{ function.hardcoded.resource_id }}"]] = {"{{ function.ref }}.present": new_{{ function.hardcoded.resource }}}

    return result
"""

GET_REQUEST_FORMAT = """
    result = dict(comment=[], ret=None, result=True)

    # TODO: Change function methods params if needed. Map `resource_id` to correct identifier
    get = await {{ function.hardcoded.boto3_function }}(
        ctx=ctx,
        {{ function.hardcoded.boto3_function_params }}
    )

    # Case: Error
    if not get["result"]:
        # Do not return success=false when it is not found.
        # Most of the resources would return "*NotFound*" type of exception when it is 404
        if "NotFound" in str(get["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }}",
                    name=resource_id
                )
            )
            result["comment"] += list(get["comment"])
            return result

        result["comment"] += list(get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get["ret"].get("{{ function.hardcoded.response_key }}"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }}",
                name=resource_id
            )
        )
        return result

    # Case: More than one found
    if len(get["ret"].get("{{ function.hardcoded.response_key }}")) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }}",
                name=resource_id
            )
        )

    # Case: One matching record is found (If more than one is found, then taking first)
    resource = get["ret"].get("{{ function.hardcoded.response_key }}")[0]

    # TODO: Tags

    result["ret"] = hub.tool.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.aws_service_name }}.conversion_utils.convert_raw_{{ function.hardcoded.aws_service_name }}_to_present(
        raw_resource=resource,
        tags={},
        idem_resource_name=name,
    )

    return result
"""


LIST_REQUEST_FORMAT = """
    result = dict(comment=[], ret=None, result=True)
    # TODO: Change function methods params if needed
    ret = await {{ function.hardcoded.boto3_function }}(
        ctx=ctx,
        **{{ parameter.mapping.kwargs|default({}) }}
    )

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("{{ function.hardcoded.response_key }}"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }}", name=None
            )
        )
        return result

    for resource in ret["ret"]["{{ function.hardcoded.response_key }}"]:
        result["ret"].append(hub.tool.aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }}.conversion_utils.convert_raw_{{ function.hardcoded.resource_name }}_to_present(
                    raw_resource=resource
                ))
    return result
"""


CREATE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    # TODO: Change function methods params if needed. Map `resource_id` to correct identifier
    ret = await {{ function.hardcoded.boto3_function }}(
        ctx,
        {{ "ClientToken=name," if function.hardcoded.has_client_token }}
        **{{ parameter.mapping.kwargs|default({}) }}
    )

    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"] += ret["comment"]
        return result

    result["comment"] = (f"Created aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)
    result["ret"] = result["ret"]["{{ function.hardcoded.response_key }}"]

    {% if function.hardcoded.waiter_call_exists %}
    # TODO: Add waiter_call from below
    #     **{{ function.hardcoded.available_waiter_calls }}
    #     try:
    #       waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
    #           default_delay=<TODO: in seconds>,
    #           default_max_attempts=<TODO: max-attempts>,
    #       )
    #       await hub.tool.boto3.client.wait(
    #           ctx,
    #           "{{ function.hardcoded.aws_service_name }}",
    #           "<TODO: waiter_name>",
    #           "<TODO: identifier>",
    #           WaiterConfig=waiter_config,
    #       )
    #     except Exception as e:
    #       result["comment"] += result["comment"] + (str(e),)
    #       result["result"] = False
    {% endif %}

    return result
"""

UPDATE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    # TODO: Change function methods params if needed. Map `resource_id` to correct identifier
    ret = await {{ function.hardcoded.boto3_function }}(
        ctx,
        {{ "ClientToken=name," if function.hardcoded.has_client_token }}
        **{{ parameter.mapping.kwargs|default({}) }}
    )

    if not ret["result"]:
        result["result"] = False
        result["comment"] += (
            f"Could not update aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.aws_service_name }} '{name}'",
        )
        result["comment"] += ret["comment"]
        return result

    result["comment"] = (f"Updated aws.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.resource_name }} '{name}'",)

    updated_resource = result["ret"]["{{ function.hardcoded.response_key }}"]
    result["ret"] = hub.tool.{{ function.hardcoded.aws_service_name }}.{{ function.hardcoded.aws_service_name }}.conversion_utils.convert_raw_{{ function.hardcoded.aws_service_name }}_to_present(
        raw_resource=updated_resource,
        tags={},
        idem_resource_name=name,
    )

    return result
"""

DELETE_REQUEST_FORMAT = """
    result = dict(comment=[], ret=[], result=True)

    # TODO: Change function methods params if needed. Map `resource_id` to correct identifier
    ret = await {{ function.hardcoded.boto3_function }}(
        ctx,
        {{ "ClientToken=name," if function.hardcoded.has_client_token }}
        **{{ parameter.mapping.kwargs|default({}) }}
    )

    result["result"] = ret["result"]

    if not result["result"]:
        result["comment"] = ret["comment"]
        result["result"] = False
        return result

    result["comment"] += (f"Deleted '{name}'",)
    return result
"""
