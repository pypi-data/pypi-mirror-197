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
    'GetNamespaceVirtualNetworkRuleResult',
    'AwaitableGetNamespaceVirtualNetworkRuleResult',
    'get_namespace_virtual_network_rule',
    'get_namespace_virtual_network_rule_output',
]

@pulumi.output_type
class GetNamespaceVirtualNetworkRuleResult:
    """
    Single item in a List or Get VirtualNetworkRules operation
    """
    def __init__(__self__, id=None, name=None, type=None, virtual_network_subnet_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if virtual_network_subnet_id and not isinstance(virtual_network_subnet_id, str):
            raise TypeError("Expected argument 'virtual_network_subnet_id' to be a str")
        pulumi.set(__self__, "virtual_network_subnet_id", virtual_network_subnet_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> Optional[str]:
        """
        Resource ID of Virtual Network Subnet
        """
        return pulumi.get(self, "virtual_network_subnet_id")


class AwaitableGetNamespaceVirtualNetworkRuleResult(GetNamespaceVirtualNetworkRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNamespaceVirtualNetworkRuleResult(
            id=self.id,
            name=self.name,
            type=self.type,
            virtual_network_subnet_id=self.virtual_network_subnet_id)


def get_namespace_virtual_network_rule(namespace_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       virtual_network_rule_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNamespaceVirtualNetworkRuleResult:
    """
    Gets an VirtualNetworkRule for a Namespace by rule name.


    :param str namespace_name: The namespace name
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str virtual_network_rule_name: The Virtual Network Rule name.
    """
    __args__ = dict()
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualNetworkRuleName'] = virtual_network_rule_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:servicebus/v20180101preview:getNamespaceVirtualNetworkRule', __args__, opts=opts, typ=GetNamespaceVirtualNetworkRuleResult).value

    return AwaitableGetNamespaceVirtualNetworkRuleResult(
        id=__ret__.id,
        name=__ret__.name,
        type=__ret__.type,
        virtual_network_subnet_id=__ret__.virtual_network_subnet_id)


@_utilities.lift_output_func(get_namespace_virtual_network_rule)
def get_namespace_virtual_network_rule_output(namespace_name: Optional[pulumi.Input[str]] = None,
                                              resource_group_name: Optional[pulumi.Input[str]] = None,
                                              virtual_network_rule_name: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNamespaceVirtualNetworkRuleResult]:
    """
    Gets an VirtualNetworkRule for a Namespace by rule name.


    :param str namespace_name: The namespace name
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str virtual_network_rule_name: The Virtual Network Rule name.
    """
    ...
