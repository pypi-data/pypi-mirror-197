# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetSourceControlResult',
    'AwaitableGetSourceControlResult',
    'get_source_control',
    'get_source_control_output',
]

@pulumi.output_type
class GetSourceControlResult:
    """
    Represents a SourceControl in Azure Security Insights.
    """
    def __init__(__self__, content_types=None, description=None, display_name=None, etag=None, id=None, last_deployment_info=None, name=None, repo_type=None, repository=None, repository_resource_info=None, system_data=None, type=None, version=None):
        if content_types and not isinstance(content_types, list):
            raise TypeError("Expected argument 'content_types' to be a list")
        pulumi.set(__self__, "content_types", content_types)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_deployment_info and not isinstance(last_deployment_info, dict):
            raise TypeError("Expected argument 'last_deployment_info' to be a dict")
        pulumi.set(__self__, "last_deployment_info", last_deployment_info)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if repo_type and not isinstance(repo_type, str):
            raise TypeError("Expected argument 'repo_type' to be a str")
        pulumi.set(__self__, "repo_type", repo_type)
        if repository and not isinstance(repository, dict):
            raise TypeError("Expected argument 'repository' to be a dict")
        pulumi.set(__self__, "repository", repository)
        if repository_resource_info and not isinstance(repository_resource_info, dict):
            raise TypeError("Expected argument 'repository_resource_info' to be a dict")
        pulumi.set(__self__, "repository_resource_info", repository_resource_info)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="contentTypes")
    def content_types(self) -> Sequence[str]:
        """
        Array of source control content types.
        """
        return pulumi.get(self, "content_types")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the source control
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name of the source control
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastDeploymentInfo")
    def last_deployment_info(self) -> Optional['outputs.DeploymentInfoResponse']:
        """
        Information regarding the latest deployment for the source control.
        """
        return pulumi.get(self, "last_deployment_info")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="repoType")
    def repo_type(self) -> str:
        """
        The repository type of the source control
        """
        return pulumi.get(self, "repo_type")

    @property
    @pulumi.getter
    def repository(self) -> 'outputs.RepositoryResponse':
        """
        Repository metadata.
        """
        return pulumi.get(self, "repository")

    @property
    @pulumi.getter(name="repositoryResourceInfo")
    def repository_resource_info(self) -> Optional['outputs.RepositoryResourceInfoResponse']:
        """
        Information regarding the resources created in user's repository.
        """
        return pulumi.get(self, "repository_resource_info")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        The version number associated with the source control
        """
        return pulumi.get(self, "version")


class AwaitableGetSourceControlResult(GetSourceControlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSourceControlResult(
            content_types=self.content_types,
            description=self.description,
            display_name=self.display_name,
            etag=self.etag,
            id=self.id,
            last_deployment_info=self.last_deployment_info,
            name=self.name,
            repo_type=self.repo_type,
            repository=self.repository,
            repository_resource_info=self.repository_resource_info,
            system_data=self.system_data,
            type=self.type,
            version=self.version)


def get_source_control(resource_group_name: Optional[str] = None,
                       source_control_id: Optional[str] = None,
                       workspace_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSourceControlResult:
    """
    Gets a source control byt its identifier.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str source_control_id: Source control Id
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['sourceControlId'] = source_control_id
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20221201preview:getSourceControl', __args__, opts=opts, typ=GetSourceControlResult).value

    return AwaitableGetSourceControlResult(
        content_types=__ret__.content_types,
        description=__ret__.description,
        display_name=__ret__.display_name,
        etag=__ret__.etag,
        id=__ret__.id,
        last_deployment_info=__ret__.last_deployment_info,
        name=__ret__.name,
        repo_type=__ret__.repo_type,
        repository=__ret__.repository,
        repository_resource_info=__ret__.repository_resource_info,
        system_data=__ret__.system_data,
        type=__ret__.type,
        version=__ret__.version)


@_utilities.lift_output_func(get_source_control)
def get_source_control_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                              source_control_id: Optional[pulumi.Input[str]] = None,
                              workspace_name: Optional[pulumi.Input[str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSourceControlResult]:
    """
    Gets a source control byt its identifier.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str source_control_id: Source control Id
    :param str workspace_name: The name of the workspace.
    """
    ...
