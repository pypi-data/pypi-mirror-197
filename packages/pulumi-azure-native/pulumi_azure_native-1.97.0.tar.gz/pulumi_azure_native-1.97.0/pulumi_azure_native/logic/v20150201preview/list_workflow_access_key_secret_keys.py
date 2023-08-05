# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListWorkflowAccessKeySecretKeysResult',
    'AwaitableListWorkflowAccessKeySecretKeysResult',
    'list_workflow_access_key_secret_keys',
    'list_workflow_access_key_secret_keys_output',
]

@pulumi.output_type
class ListWorkflowAccessKeySecretKeysResult:
    def __init__(__self__, primary_secret_key=None, secondary_secret_key=None):
        if primary_secret_key and not isinstance(primary_secret_key, str):
            raise TypeError("Expected argument 'primary_secret_key' to be a str")
        pulumi.set(__self__, "primary_secret_key", primary_secret_key)
        if secondary_secret_key and not isinstance(secondary_secret_key, str):
            raise TypeError("Expected argument 'secondary_secret_key' to be a str")
        pulumi.set(__self__, "secondary_secret_key", secondary_secret_key)

    @property
    @pulumi.getter(name="primarySecretKey")
    def primary_secret_key(self) -> str:
        """
        Gets the primary secret key.
        """
        return pulumi.get(self, "primary_secret_key")

    @property
    @pulumi.getter(name="secondarySecretKey")
    def secondary_secret_key(self) -> str:
        """
        Gets the secondary secret key.
        """
        return pulumi.get(self, "secondary_secret_key")


class AwaitableListWorkflowAccessKeySecretKeysResult(ListWorkflowAccessKeySecretKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWorkflowAccessKeySecretKeysResult(
            primary_secret_key=self.primary_secret_key,
            secondary_secret_key=self.secondary_secret_key)


def list_workflow_access_key_secret_keys(access_key_name: Optional[str] = None,
                                         resource_group_name: Optional[str] = None,
                                         workflow_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWorkflowAccessKeySecretKeysResult:
    """
    Lists secret keys.


    :param str access_key_name: The workflow access key name.
    :param str resource_group_name: The resource group name.
    :param str workflow_name: The workflow name.
    """
    __args__ = dict()
    __args__['accessKeyName'] = access_key_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workflowName'] = workflow_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:logic/v20150201preview:listWorkflowAccessKeySecretKeys', __args__, opts=opts, typ=ListWorkflowAccessKeySecretKeysResult).value

    return AwaitableListWorkflowAccessKeySecretKeysResult(
        primary_secret_key=__ret__.primary_secret_key,
        secondary_secret_key=__ret__.secondary_secret_key)


@_utilities.lift_output_func(list_workflow_access_key_secret_keys)
def list_workflow_access_key_secret_keys_output(access_key_name: Optional[pulumi.Input[str]] = None,
                                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                                workflow_name: Optional[pulumi.Input[str]] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListWorkflowAccessKeySecretKeysResult]:
    """
    Lists secret keys.


    :param str access_key_name: The workflow access key name.
    :param str resource_group_name: The resource group name.
    :param str workflow_name: The workflow name.
    """
    ...
