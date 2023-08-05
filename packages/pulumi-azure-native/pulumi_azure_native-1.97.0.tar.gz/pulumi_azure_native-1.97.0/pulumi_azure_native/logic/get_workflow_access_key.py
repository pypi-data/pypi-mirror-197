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
    'GetWorkflowAccessKeyResult',
    'AwaitableGetWorkflowAccessKeyResult',
    'get_workflow_access_key',
    'get_workflow_access_key_output',
]

@pulumi.output_type
class GetWorkflowAccessKeyResult:
    def __init__(__self__, id=None, name=None, not_after=None, not_before=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if not_after and not isinstance(not_after, str):
            raise TypeError("Expected argument 'not_after' to be a str")
        pulumi.set(__self__, "not_after", not_after)
        if not_before and not isinstance(not_before, str):
            raise TypeError("Expected argument 'not_before' to be a str")
        pulumi.set(__self__, "not_before", not_before)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Gets or sets the resource id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Gets the workflow access key name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notAfter")
    def not_after(self) -> Optional[str]:
        """
        Gets or sets the not-after time.
        """
        return pulumi.get(self, "not_after")

    @property
    @pulumi.getter(name="notBefore")
    def not_before(self) -> Optional[str]:
        """
        Gets or sets the not-before time.
        """
        return pulumi.get(self, "not_before")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Gets the workflow access key type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWorkflowAccessKeyResult(GetWorkflowAccessKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkflowAccessKeyResult(
            id=self.id,
            name=self.name,
            not_after=self.not_after,
            not_before=self.not_before,
            type=self.type)


def get_workflow_access_key(access_key_name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            workflow_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkflowAccessKeyResult:
    """
    Gets a workflow access key.
    API Version: 2015-02-01-preview.


    :param str access_key_name: The workflow access key name.
    :param str resource_group_name: The resource group name.
    :param str workflow_name: The workflow name.
    """
    __args__ = dict()
    __args__['accessKeyName'] = access_key_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workflowName'] = workflow_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:logic:getWorkflowAccessKey', __args__, opts=opts, typ=GetWorkflowAccessKeyResult).value

    return AwaitableGetWorkflowAccessKeyResult(
        id=__ret__.id,
        name=__ret__.name,
        not_after=__ret__.not_after,
        not_before=__ret__.not_before,
        type=__ret__.type)


@_utilities.lift_output_func(get_workflow_access_key)
def get_workflow_access_key_output(access_key_name: Optional[pulumi.Input[str]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   workflow_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkflowAccessKeyResult]:
    """
    Gets a workflow access key.
    API Version: 2015-02-01-preview.


    :param str access_key_name: The workflow access key name.
    :param str resource_group_name: The resource group name.
    :param str workflow_name: The workflow name.
    """
    ...
