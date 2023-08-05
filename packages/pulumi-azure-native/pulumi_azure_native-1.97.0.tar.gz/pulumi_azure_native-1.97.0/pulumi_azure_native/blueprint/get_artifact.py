# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetArtifactResult',
    'AwaitableGetArtifactResult',
    'get_artifact',
    'get_artifact_output',
]

warnings.warn("""Please use one of the variants: PolicyAssignmentArtifact, RoleAssignmentArtifact, TemplateArtifact.""", DeprecationWarning)

@pulumi.output_type
class GetArtifactResult:
    """
    Represents a blueprint artifact.
    """
    def __init__(__self__, id=None, kind=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        String Id used to locate any resource on Azure.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Specifies the kind of blueprint artifact.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of this resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of this resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetArtifactResult(GetArtifactResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetArtifactResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            type=self.type)


def get_artifact(artifact_name: Optional[str] = None,
                 blueprint_name: Optional[str] = None,
                 resource_scope: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetArtifactResult:
    """
    Get a blueprint artifact.
    API Version: 2018-11-01-preview.


    :param str artifact_name: Name of the blueprint artifact.
    :param str blueprint_name: Name of the blueprint definition.
    :param str resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
    """
    pulumi.log.warn("""get_artifact is deprecated: Please use one of the variants: PolicyAssignmentArtifact, RoleAssignmentArtifact, TemplateArtifact.""")
    __args__ = dict()
    __args__['artifactName'] = artifact_name
    __args__['blueprintName'] = blueprint_name
    __args__['resourceScope'] = resource_scope
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:blueprint:getArtifact', __args__, opts=opts, typ=GetArtifactResult).value

    return AwaitableGetArtifactResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        type=__ret__.type)


@_utilities.lift_output_func(get_artifact)
def get_artifact_output(artifact_name: Optional[pulumi.Input[str]] = None,
                        blueprint_name: Optional[pulumi.Input[str]] = None,
                        resource_scope: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetArtifactResult]:
    """
    Get a blueprint artifact.
    API Version: 2018-11-01-preview.


    :param str artifact_name: Name of the blueprint artifact.
    :param str blueprint_name: Name of the blueprint definition.
    :param str resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
    """
    pulumi.log.warn("""get_artifact is deprecated: Please use one of the variants: PolicyAssignmentArtifact, RoleAssignmentArtifact, TemplateArtifact.""")
    ...
