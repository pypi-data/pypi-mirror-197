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
    'GetVirtualNetworkRuleResult',
    'AwaitableGetVirtualNetworkRuleResult',
    'get_virtual_network_rule',
    'get_virtual_network_rule_output',
]

@pulumi.output_type
class GetVirtualNetworkRuleResult:
    """
    Data Lake Store virtual network rule information.
    """
    def __init__(__self__, id=None, name=None, subnet_id=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The resource identifier for the subnet.
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetVirtualNetworkRuleResult(GetVirtualNetworkRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkRuleResult(
            id=self.id,
            name=self.name,
            subnet_id=self.subnet_id,
            type=self.type)


def get_virtual_network_rule(account_name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             virtual_network_rule_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualNetworkRuleResult:
    """
    Gets the specified Data Lake Store virtual network rule.


    :param str account_name: The name of the Data Lake Store account.
    :param str resource_group_name: The name of the Azure resource group.
    :param str virtual_network_rule_name: The name of the virtual network rule to retrieve.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualNetworkRuleName'] = virtual_network_rule_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:datalakestore/v20161101:getVirtualNetworkRule', __args__, opts=opts, typ=GetVirtualNetworkRuleResult).value

    return AwaitableGetVirtualNetworkRuleResult(
        id=__ret__.id,
        name=__ret__.name,
        subnet_id=__ret__.subnet_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_virtual_network_rule)
def get_virtual_network_rule_output(account_name: Optional[pulumi.Input[str]] = None,
                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                    virtual_network_rule_name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualNetworkRuleResult]:
    """
    Gets the specified Data Lake Store virtual network rule.


    :param str account_name: The name of the Data Lake Store account.
    :param str resource_group_name: The name of the Azure resource group.
    :param str virtual_network_rule_name: The name of the virtual network rule to retrieve.
    """
    ...
