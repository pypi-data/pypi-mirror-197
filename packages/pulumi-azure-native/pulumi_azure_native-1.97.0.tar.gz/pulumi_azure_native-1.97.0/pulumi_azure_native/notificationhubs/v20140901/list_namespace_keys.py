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
    'ListNamespaceKeysResult',
    'AwaitableListNamespaceKeysResult',
    'list_namespace_keys',
    'list_namespace_keys_output',
]

@pulumi.output_type
class ListNamespaceKeysResult:
    """
    Namespace/NotificationHub Connection String
    """
    def __init__(__self__, primary_connection_string=None, secondary_connection_string=None):
        if primary_connection_string and not isinstance(primary_connection_string, str):
            raise TypeError("Expected argument 'primary_connection_string' to be a str")
        pulumi.set(__self__, "primary_connection_string", primary_connection_string)
        if secondary_connection_string and not isinstance(secondary_connection_string, str):
            raise TypeError("Expected argument 'secondary_connection_string' to be a str")
        pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> Optional[str]:
        """
        Gets or sets the primaryConnectionString of the created Namespace AuthorizationRule.
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> Optional[str]:
        """
        Gets or sets the secondaryConnectionString of the created Namespace AuthorizationRule
        """
        return pulumi.get(self, "secondary_connection_string")


class AwaitableListNamespaceKeysResult(ListNamespaceKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListNamespaceKeysResult(
            primary_connection_string=self.primary_connection_string,
            secondary_connection_string=self.secondary_connection_string)


def list_namespace_keys(authorization_rule_name: Optional[str] = None,
                        namespace_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListNamespaceKeysResult:
    """
    Gets the Primary and Secondary ConnectionStrings to the namespace


    :param str authorization_rule_name: The connection string of the namespace for the specified authorizationRule.
    :param str namespace_name: The namespace name.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['authorizationRuleName'] = authorization_rule_name
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:notificationhubs/v20140901:listNamespaceKeys', __args__, opts=opts, typ=ListNamespaceKeysResult).value

    return AwaitableListNamespaceKeysResult(
        primary_connection_string=__ret__.primary_connection_string,
        secondary_connection_string=__ret__.secondary_connection_string)


@_utilities.lift_output_func(list_namespace_keys)
def list_namespace_keys_output(authorization_rule_name: Optional[pulumi.Input[str]] = None,
                               namespace_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListNamespaceKeysResult]:
    """
    Gets the Primary and Secondary ConnectionStrings to the namespace


    :param str authorization_rule_name: The connection string of the namespace for the specified authorizationRule.
    :param str namespace_name: The namespace name.
    :param str resource_group_name: The name of the resource group.
    """
    ...
