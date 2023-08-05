# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'ListActiveSecurityUserRuleResult',
    'AwaitableListActiveSecurityUserRuleResult',
    'list_active_security_user_rule',
    'list_active_security_user_rule_output',
]

@pulumi.output_type
class ListActiveSecurityUserRuleResult:
    """
    Result of the request to list active security user rules. It contains a list of active security user rules and a skiptoken to get the next set of results.
    """
    def __init__(__self__, skip_token=None, value=None):
        if skip_token and not isinstance(skip_token, str):
            raise TypeError("Expected argument 'skip_token' to be a str")
        pulumi.set(__self__, "skip_token", skip_token)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="skipToken")
    def skip_token(self) -> Optional[str]:
        """
        When present, the value can be passed to a subsequent query call (together with the same query and scopes used in the current request) to retrieve the next page of data.
        """
        return pulumi.get(self, "skip_token")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence[Any]]:
        """
        Gets a page of active security user rules.
        """
        return pulumi.get(self, "value")


class AwaitableListActiveSecurityUserRuleResult(ListActiveSecurityUserRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListActiveSecurityUserRuleResult(
            skip_token=self.skip_token,
            value=self.value)


def list_active_security_user_rule(network_manager_name: Optional[str] = None,
                                   regions: Optional[Sequence[str]] = None,
                                   resource_group_name: Optional[str] = None,
                                   skip_token: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListActiveSecurityUserRuleResult:
    """
    Lists Active Security User Rules in a network manager.
    API Version: 2021-02-01-preview.


    :param str network_manager_name: The name of the network manager.
    :param Sequence[str] regions: List of regions.
    :param str resource_group_name: The name of the resource group.
    :param str skip_token: When present, the value can be passed to a subsequent query call (together with the same query and scopes used in the current request) to retrieve the next page of data.
    """
    __args__ = dict()
    __args__['networkManagerName'] = network_manager_name
    __args__['regions'] = regions
    __args__['resourceGroupName'] = resource_group_name
    __args__['skipToken'] = skip_token
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network:listActiveSecurityUserRule', __args__, opts=opts, typ=ListActiveSecurityUserRuleResult).value

    return AwaitableListActiveSecurityUserRuleResult(
        skip_token=__ret__.skip_token,
        value=__ret__.value)


@_utilities.lift_output_func(list_active_security_user_rule)
def list_active_security_user_rule_output(network_manager_name: Optional[pulumi.Input[str]] = None,
                                          regions: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                                          resource_group_name: Optional[pulumi.Input[str]] = None,
                                          skip_token: Optional[pulumi.Input[Optional[str]]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListActiveSecurityUserRuleResult]:
    """
    Lists Active Security User Rules in a network manager.
    API Version: 2021-02-01-preview.


    :param str network_manager_name: The name of the network manager.
    :param Sequence[str] regions: List of regions.
    :param str resource_group_name: The name of the resource group.
    :param str skip_token: When present, the value can be passed to a subsequent query call (together with the same query and scopes used in the current request) to retrieve the next page of data.
    """
    ...
