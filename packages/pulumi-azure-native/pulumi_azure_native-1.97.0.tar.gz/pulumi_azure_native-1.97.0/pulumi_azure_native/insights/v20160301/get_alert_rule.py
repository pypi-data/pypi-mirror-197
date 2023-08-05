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
    'GetAlertRuleResult',
    'AwaitableGetAlertRuleResult',
    'get_alert_rule',
    'get_alert_rule_output',
]

@pulumi.output_type
class GetAlertRuleResult:
    """
    The alert rule resource.
    """
    def __init__(__self__, action=None, actions=None, condition=None, description=None, id=None, is_enabled=None, last_updated_time=None, location=None, name=None, provisioning_state=None, tags=None, type=None):
        if action and not isinstance(action, dict):
            raise TypeError("Expected argument 'action' to be a dict")
        pulumi.set(__self__, "action", action)
        if actions and not isinstance(actions, list):
            raise TypeError("Expected argument 'actions' to be a list")
        pulumi.set(__self__, "actions", actions)
        if condition and not isinstance(condition, dict):
            raise TypeError("Expected argument 'condition' to be a dict")
        pulumi.set(__self__, "condition", condition)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_enabled and not isinstance(is_enabled, bool):
            raise TypeError("Expected argument 'is_enabled' to be a bool")
        pulumi.set(__self__, "is_enabled", is_enabled)
        if last_updated_time and not isinstance(last_updated_time, str):
            raise TypeError("Expected argument 'last_updated_time' to be a str")
        pulumi.set(__self__, "last_updated_time", last_updated_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def action(self) -> Optional[Any]:
        """
        action that is performed when the alert rule becomes active, and when an alert condition is resolved.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def actions(self) -> Optional[Sequence[Any]]:
        """
        the array of actions that are performed when the alert rule becomes active, and when an alert condition is resolved.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def condition(self) -> Any:
        """
        the condition that results in the alert rule being activated.
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        the description of the alert rule that will be included in the alert email.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> bool:
        """
        the flag that indicates whether the alert rule is enabled.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter(name="lastUpdatedTime")
    def last_updated_time(self) -> str:
        """
        Last time the rule was updated in ISO8601 format.
        """
        return pulumi.get(self, "last_updated_time")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        the provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetAlertRuleResult(GetAlertRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAlertRuleResult(
            action=self.action,
            actions=self.actions,
            condition=self.condition,
            description=self.description,
            id=self.id,
            is_enabled=self.is_enabled,
            last_updated_time=self.last_updated_time,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type)


def get_alert_rule(resource_group_name: Optional[str] = None,
                   rule_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAlertRuleResult:
    """
    Gets a classic metric alert rule


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_name: The name of the rule.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleName'] = rule_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:insights/v20160301:getAlertRule', __args__, opts=opts, typ=GetAlertRuleResult).value

    return AwaitableGetAlertRuleResult(
        action=__ret__.action,
        actions=__ret__.actions,
        condition=__ret__.condition,
        description=__ret__.description,
        id=__ret__.id,
        is_enabled=__ret__.is_enabled,
        last_updated_time=__ret__.last_updated_time,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_alert_rule)
def get_alert_rule_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                          rule_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAlertRuleResult]:
    """
    Gets a classic metric alert rule


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_name: The name of the rule.
    """
    ...
