"""Build plugin metadata which can be used by pop-create for plugin code generation"""
from typing import Any
from typing import Dict

__func_alias__ = {"type_": "type"}


def parse(
    hub,
    ctx,
    resource_name: str,
    shared_resource_data: dict,
) -> Dict[str, Any]:
    """
    Plugin related
    """
    missing_requisites = False

    if ctx.create_plugin == "state_modules":
        missing_requisites = (
            hub.pop_create.aws.plugin.missing_requisites_for_state_modules(
                shared_resource_data
            )
        )
    elif ctx.create_plugin == "auto_state":
        missing_requisites = (
            hub.pop_create.aws.plugin.missing_requisites_for_auto_states(
                shared_resource_data
            )
        )

    if missing_requisites:
        # TODO: Support partial resource plugin.
        hub.log.info(
            f"The resource {resource_name} is missing requisite for {ctx.create_plugin}"
        )
        return dict()

    plugin = {
        "doc": "",
        "imports": [
            "import copy",
            "from dataclasses import field",
            "from dataclasses import make_dataclass",
            "from typing import *",
        ],
        "virtualname": resource_name,
        "functions": hub.pop_create.aws.plugin.generate_functions(
            ctx, resource_name, shared_resource_data
        ),
    }

    if ctx.create_plugin == "auto_state":
        plugin["contracts"] = ["auto_state", "soft_fail"]
    elif ctx.create_plugin == "state_modules":
        plugin["contracts"] = ["resource"]

    return plugin


def missing_requisites_for_state_modules(hub, shared_resource_data: dict) -> bool:
    # If the resource has no list/create/delete call
    required_operations = {
        r: shared_resource_data[r]
        for r in ["create", "delete", "list"]
        if r in shared_resource_data
    }
    return any(len(value) == 0 for value in required_operations.values())


def missing_requisites_for_auto_states(hub, shared_resource_data: dict) -> bool:
    # If the resource has no get/list/create/delete call
    required_operations = {
        r: shared_resource_data[r]
        for r in ["get", "create", "delete", "list"]
        if r in shared_resource_data
    }
    return any(len(value) == 0 for value in required_operations.values())


def generate_functions(hub, ctx, resource_name, shared_resource_data):
    functions = dict()

    if ctx.create_plugin == "state_modules":
        functions["present"] = hub.pop_create.aws.plugin.generate_present(
            ctx, resource_name, shared_resource_data
        )
        functions["absent"] = hub.pop_create.aws.plugin.generate_absent(
            ctx, resource_name, shared_resource_data
        )
        functions["describe"] = hub.pop_create.aws.plugin.generate_list(
            resource_name, shared_resource_data
        )
    elif ctx.create_plugin == "auto_state":
        functions["get"] = hub.pop_create.aws.plugin.generate_get(
            ctx, resource_name, shared_resource_data
        )
        functions["list"] = hub.pop_create.aws.plugin.generate_list(
            resource_name, shared_resource_data
        )
        functions["create"] = hub.pop_create.aws.plugin.generate_present(
            ctx, resource_name, shared_resource_data
        )
        functions["update"] = hub.pop_create.aws.plugin.generate_update(
            ctx, resource_name, shared_resource_data
        )
        functions["delete"] = hub.pop_create.aws.plugin.generate_absent(
            ctx, resource_name, shared_resource_data
        )

    return functions


def generate_list(hub, resource_name, shared_resource_data):
    describe_function_definition = shared_resource_data["list"]
    params = describe_function_definition.get("params", {})
    return {
        "doc": f"List all {resource_name} resources for the given account. \n{describe_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            response_key=next(
                iter(
                    describe_function_definition.get("hardcoded", {})
                    .get("return_fields", {})
                    .keys()
                )
            ),
            **describe_function_definition.get("hardcoded", {}),
        ),
    }


def generate_present(hub, ctx, resource_name, shared_resource_data):
    create_function_definition = shared_resource_data["create"]
    params = create_function_definition.get("params", {})
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"{create_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **create_function_definition.get("hardcoded", {}),
        ),
    }


def generate_absent(hub, ctx, resource_name, shared_resource_data):
    delete_function_definition = shared_resource_data["delete"]
    params = delete_function_definition.get("params", {})
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"{delete_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **delete_function_definition.get("hardcoded", {}),
        ),
    }


def generate_get(hub, ctx, resource_name, shared_resource_data):
    get_function_definition = shared_resource_data["get"]
    params = get_function_definition.get("params", {})
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"Get {resource_name} resources for the given account. \n{get_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            response_key=next(
                iter(
                    get_function_definition.get("hardcoded", {})
                    .get("return_fields", {})
                    .keys()
                )
            ),
            **get_function_definition.get("hardcoded", {}),
        ),
    }


def generate_update(hub, ctx, resource_name, shared_resource_data):
    update_function_definition = shared_resource_data["update"]
    params = update_function_definition.get("params", {})
    hub.pop_create.aws.plugin.resolve_resource_id_and_name_params(ctx, params)
    return {
        "doc": f"{update_function_definition.get('doc', '')}",
        "params": params,
        "hardcoded": dict(
            **update_function_definition.get("hardcoded", {}),
        ),
    }


def resolve_resource_id_and_name_params(hub, ctx, params: dict):
    # auto_state already puts name and resource_id by default in header params
    if ctx.create_plugin == "state_modules":
        params["resource_id"] = hub.pop_create.aws.template.RESOURCE_ID_PARAMETER.copy()
        if "Name" not in params.keys():
            # If we come here that means name was not present in AWS function definition
            params["Name"] = hub.pop_create.aws.template.NAME_PARAMETER.copy()
