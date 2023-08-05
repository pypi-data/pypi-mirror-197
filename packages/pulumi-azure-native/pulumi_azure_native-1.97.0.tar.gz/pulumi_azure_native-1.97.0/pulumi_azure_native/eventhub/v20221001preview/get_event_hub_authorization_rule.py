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
    'GetEventHubAuthorizationRuleResult',
    'AwaitableGetEventHubAuthorizationRuleResult',
    'get_event_hub_authorization_rule',
    'get_event_hub_authorization_rule_output',
]

@pulumi.output_type
class GetEventHubAuthorizationRuleResult:
    """
    Single item in a List or Get AuthorizationRule operation
    """
    def __init__(__self__, id=None, location=None, name=None, rights=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if rights and not isinstance(rights, list):
            raise TypeError("Expected argument 'rights' to be a list")
        pulumi.set(__self__, "rights", rights)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rights(self) -> Sequence[str]:
        """
        The rights associated with the rule.
        """
        return pulumi.get(self, "rights")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.EventHub/Namespaces" or "Microsoft.EventHub/Namespaces/EventHubs"
        """
        return pulumi.get(self, "type")


class AwaitableGetEventHubAuthorizationRuleResult(GetEventHubAuthorizationRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventHubAuthorizationRuleResult(
            id=self.id,
            location=self.location,
            name=self.name,
            rights=self.rights,
            system_data=self.system_data,
            type=self.type)


def get_event_hub_authorization_rule(authorization_rule_name: Optional[str] = None,
                                     event_hub_name: Optional[str] = None,
                                     namespace_name: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventHubAuthorizationRuleResult:
    """
    Gets an AuthorizationRule for an Event Hub by rule name.


    :param str authorization_rule_name: The authorization rule name.
    :param str event_hub_name: The Event Hub name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    __args__ = dict()
    __args__['authorizationRuleName'] = authorization_rule_name
    __args__['eventHubName'] = event_hub_name
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventhub/v20221001preview:getEventHubAuthorizationRule', __args__, opts=opts, typ=GetEventHubAuthorizationRuleResult).value

    return AwaitableGetEventHubAuthorizationRuleResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        rights=__ret__.rights,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_event_hub_authorization_rule)
def get_event_hub_authorization_rule_output(authorization_rule_name: Optional[pulumi.Input[str]] = None,
                                            event_hub_name: Optional[pulumi.Input[str]] = None,
                                            namespace_name: Optional[pulumi.Input[str]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventHubAuthorizationRuleResult]:
    """
    Gets an AuthorizationRule for an Event Hub by rule name.


    :param str authorization_rule_name: The authorization rule name.
    :param str event_hub_name: The Event Hub name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    ...
