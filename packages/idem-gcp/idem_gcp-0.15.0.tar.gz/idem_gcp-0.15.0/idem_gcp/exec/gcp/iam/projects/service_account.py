"""Exec module for managing ServiceAccounts."""
from idem_gcp.tool.gcp.generate.exec_context import ExecutionContext

__func_alias__ = {"list_": "list"}


async def list_(hub, ctx, project: str = None):
    r"""Lists every ServiceAccount that belongs to a specific project.

    Args:
        project(str, Required):
            The resource name of the project associated with the service accounts.
    """
    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)

    execution_context = ExecutionContext(
        resource_type="iam.projects.service_account",
        method_name="list",
        method_params={"ctx": ctx, "name": f"projects/{project}"},
    )

    return await hub.tool.gcp.generate.generic_exec.execute(execution_context)


async def get(
    hub,
    ctx,
    project: str = None,
    unique_id: str = None,
    email: str = None,
    resource_id: str = None,
):
    r"""Returns the specified ServiceAccount resource.

    Args:
        project(str, Optional):
            Project ID for this request.
        unique_id(str, Optional):
            The unique, stable numeric ID for the service account.
        email(str, Optional):
            The email address of the service account.
        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    if unique_id or email:
        project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
        identifier = unique_id or email
        resource_id = f"projects/{project}/serviceAccounts/{identifier}"
    elif not resource_id:
        result["result"] = False
        result["comment"] = [
            f"gcp.iam.projects.service_account#get(): either resource_id or unique_id or email"
            f" should be specified."
        ]
        return result

    execution_context = ExecutionContext(
        resource_type="iam.projects.service_account",
        method_name="get",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result


async def undelete(
    hub,
    ctx,
    unique_id: str,
    project: str = None,
):
    r"""Restores a deleted service account.

    It is not always possible to restore a deleted service account. Use this method only as a last resort.

    After you delete a service account, IAM permanently removes the service account 30 days later. There is no way to
    restore a deleted service account that has been permanently removed.

    The permission 'iam.serviceAccounts.undelete' is required for undeleting resources.

    Although the GCP documentation states that either email or unique_id can be used as resource name, using an email
    results in the following error: "The service account name must be in the following format:
    projects/{PROJECT_ID}/serviceAccounts/{ACCOUNT_UNIQUE_ID}".

    Args:
        unique_id(str, Required):
            The unique, stable numeric ID for the service account.
        project(str, Optional):
            Project ID for this request.
    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    if not unique_id:
        result["result"] = False
        result["comment"] = [
            f"gcp.iam.projects.service_account#undelete(): unique_id is required"
        ]
        return result

    project = hub.tool.gcp.utils.get_project_from_account(ctx, project)
    resource_id = f"projects/{project}/serviceAccounts/{unique_id}"

    execution_context = ExecutionContext(
        resource_type="iam.projects.service_account",
        method_name="undelete",
        method_params={"ctx": ctx, "name": resource_id},
    )

    ret = await hub.tool.gcp.generate.generic_exec.execute(execution_context)

    result["comment"] += ret["comment"]
    if not ret["result"]:
        result["result"] = False
        return result

    result["ret"] = ret["ret"]
    return result
