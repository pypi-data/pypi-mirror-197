import pathlib

import boto3.session
from boto3.exceptions import ResourceNotExistsError
from dict_tools.data import NamespaceDict

try:
    import tqdm

    HAS_LIBS = (True,)
except ImportError as e:
    HAS_LIBS = False, str(e)


def __virtual__(hub):
    return HAS_LIBS


def context(hub, ctx, directory: pathlib.Path):
    ctx = hub.pop_create.idem_cloud.init.context(ctx, directory)
    ctx.servers = [None]

    # AWS already has an acct plugin
    ctx.has_acct_plugin = False
    ctx.service_name = "aws_auto"

    # Initialize cloud spec
    request_format = {}
    if ctx.create_plugin == "auto_state":
        # TODO: Implement auto_states for AWS plugin
        request_format = {
            "get": hub.pop_create.aws.template.GET_REQUEST_FORMAT,
            "create": hub.pop_create.aws.template.CREATE_REQUEST_FORMAT,
            "delete": hub.pop_create.aws.template.DELETE_REQUEST_FORMAT,
            "update": hub.pop_create.aws.template.UPDATE_REQUEST_FORMAT,
            "list": hub.pop_create.aws.template.LIST_REQUEST_FORMAT,
        }
    elif ctx.create_plugin == "state_modules":
        request_format = {
            "present": hub.pop_create.aws.template.PRESENT_REQUEST_FORMAT,
            "absent": hub.pop_create.aws.template.ABSENT_REQUEST_FORMAT,
            "describe": hub.pop_create.aws.template.DESCRIBE_REQUEST_FORMAT,
        }

    # Now start getting into AWS resource plugin creation
    session = boto3.session.Session()

    # If CLI provides services then use those services first
    # e.g. --services rds
    services = hub.OPT.pop_create.services or session.get_available_services()
    # This takes a while because we are making http calls to aws
    for aws_service_name in tqdm.tqdm(services, desc="services"):
        # Clean out the service name
        aws_service_name = (
            aws_service_name.lower().strip().replace(" ", "_").replace("-", "_")
        )
        aws_service_name = hub.tool.format.keyword.unclash(aws_service_name)

        # Get supported operations for this service
        resource_operations = hub.pop_create.aws.service.parse_resource_and_operations(
            service_name=aws_service_name,
            session=session,
        )

        requested_service_resources = hub.OPT.pop_create.service_resources
        if bool(requested_service_resources):
            # if the CLI provides resources, filter the list of resources to process
            # e.g. --service_resources db_cluster db_instance
            resource_operations = {
                r: resource_operations[r]
                for r in requested_service_resources
                if r in resource_operations
            }

        plugins = dict()
        plugins[f"{aws_service_name}.init"] = {
            "imports": [],
            "functions": {},
            "doc": hub.pop_create.aws.service.parse_docstring(
                session, aws_service_name
            ),
            "sub_alias": [aws_service_name],
        }

        for resource_name, functions in tqdm.tqdm(
            resource_operations.items(), desc="operations"
        ):
            # Clean out resource name
            resource_name = (
                resource_name.lower().strip().replace(" ", "_").replace("-", "_")
            )

            # Check if the plugin should be created
            #   - see if it exists
            #   - or --overwrite flag is used
            resource_plugin_exists = hub.pop_create.aws.init.plugin_exists(
                ctx, aws_service_name, resource_name
            )
            should_create_resource_plugin = (
                ctx.overwrite_existing or not resource_plugin_exists
            )

            if should_create_resource_plugin:
                # parse known or commonly used resource actions for the resource
                resource_actions = hub.pop_create.aws.resource.parse_actions(
                    session,
                    aws_service_name,
                    resource_name,
                    functions,
                )

                # create shared resource data to be used when creating resource plugins
                shared_resource_data = {
                    "aws_service_name": aws_service_name,
                    "resource_name": resource_name,
                    "get": resource_actions.get("get"),
                    "create": resource_actions.get("create"),
                    "update": resource_actions.get("update"),
                    "delete": resource_actions.get("delete"),
                    "list": resource_actions.get("list"),
                    "tag_resource": resource_actions.get("tag_resource"),
                    "generic_resource_init_call": hub.pop_create.aws.resource.build_resource_init_call(
                        aws_service_name, resource_name
                    ),
                    "generic_resource_describe_call": hub.pop_create.aws.resource.build_get_by_resource_call(),
                }

                # parse resource plugin metadata from extracted API references above for the resource
                resource_plugin = hub.pop_create.aws.plugin.parse(
                    ctx, resource_name, shared_resource_data
                )

                if not bool(resource_plugin):
                    # if for whatever reason the plugin cannot be created, move on to next
                    continue

                plugin_key = f"{aws_service_name}.{resource_name}"
                plugins[plugin_key] = resource_plugin

        if plugins:
            try:
                # Initialize cloud spec and run it with provided create_plugin
                ctx.cloud_spec = NamespaceDict(
                    api_version="",
                    project_name=ctx.project_name,
                    service_name=ctx.service_name,
                    request_format=request_format,
                    plugins=plugins,
                )
                hub.cloudspec.init.run(
                    ctx,
                    directory,
                    create_plugins=[ctx.create_plugin],
                )
            finally:
                hub.log.info(
                    f"Finished creating plugin for service [{aws_service_name}] and resources {list(resource_operations.keys())} with create plugin {ctx.create_plugin}]"
                )

    return ctx


def plugin_exists(hub, ctx, aws_service_name: str, resource_name: str) -> bool:
    """
    Validate if the plugin path exists based on create plugin
    """
    path = pathlib.Path(ctx.target_directory).absolute() / ctx.clean_name
    if ctx.create_plugin == "auto_state":
        path = path / "exec" / aws_service_name
    elif ctx.create_plugin == "state_modules":
        path = path / "states" / aws_service_name
    elif ctx.create_plugin == "tests":
        path = path / "tests" / "integration" / "states"

    path = path / aws_service_name / f"{resource_name}.py"
    if path.exists():
        hub.log.info(f"Plugin already exists at '{path}', use `--overwrite` to modify")
        return True

    return False
