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
    'ListApplicationAllowedUpgradePlansResult',
    'AwaitableListApplicationAllowedUpgradePlansResult',
    'list_application_allowed_upgrade_plans',
    'list_application_allowed_upgrade_plans_output',
]

@pulumi.output_type
class ListApplicationAllowedUpgradePlansResult:
    """
    The array of plan.
    """
    def __init__(__self__, value=None):
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.PlanResponse']]:
        """
        The array of plans.
        """
        return pulumi.get(self, "value")


class AwaitableListApplicationAllowedUpgradePlansResult(ListApplicationAllowedUpgradePlansResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListApplicationAllowedUpgradePlansResult(
            value=self.value)


def list_application_allowed_upgrade_plans(application_name: Optional[str] = None,
                                           resource_group_name: Optional[str] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListApplicationAllowedUpgradePlansResult:
    """
    List allowed upgrade plans for application.


    :param str application_name: The name of the managed application.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['applicationName'] = application_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:solutions/v20210701:listApplicationAllowedUpgradePlans', __args__, opts=opts, typ=ListApplicationAllowedUpgradePlansResult).value

    return AwaitableListApplicationAllowedUpgradePlansResult(
        value=__ret__.value)


@_utilities.lift_output_func(list_application_allowed_upgrade_plans)
def list_application_allowed_upgrade_plans_output(application_name: Optional[pulumi.Input[str]] = None,
                                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListApplicationAllowedUpgradePlansResult]:
    """
    List allowed upgrade plans for application.


    :param str application_name: The name of the managed application.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
