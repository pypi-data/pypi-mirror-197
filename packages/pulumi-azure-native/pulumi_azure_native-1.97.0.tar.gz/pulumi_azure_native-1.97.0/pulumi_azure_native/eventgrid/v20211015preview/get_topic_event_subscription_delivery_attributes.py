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
    'GetTopicEventSubscriptionDeliveryAttributesResult',
    'AwaitableGetTopicEventSubscriptionDeliveryAttributesResult',
    'get_topic_event_subscription_delivery_attributes',
    'get_topic_event_subscription_delivery_attributes_output',
]

@pulumi.output_type
class GetTopicEventSubscriptionDeliveryAttributesResult:
    """
    Result of the Get delivery attributes operation.
    """
    def __init__(__self__, value=None):
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence[Any]]:
        """
        A collection of DeliveryAttributeMapping
        """
        return pulumi.get(self, "value")


class AwaitableGetTopicEventSubscriptionDeliveryAttributesResult(GetTopicEventSubscriptionDeliveryAttributesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTopicEventSubscriptionDeliveryAttributesResult(
            value=self.value)


def get_topic_event_subscription_delivery_attributes(event_subscription_name: Optional[str] = None,
                                                     resource_group_name: Optional[str] = None,
                                                     topic_name: Optional[str] = None,
                                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTopicEventSubscriptionDeliveryAttributesResult:
    """
    Get all delivery attributes for an event subscription for topic.


    :param str event_subscription_name: Name of the event subscription.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    :param str topic_name: Name of the domain topic.
    """
    __args__ = dict()
    __args__['eventSubscriptionName'] = event_subscription_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['topicName'] = topic_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventgrid/v20211015preview:getTopicEventSubscriptionDeliveryAttributes', __args__, opts=opts, typ=GetTopicEventSubscriptionDeliveryAttributesResult).value

    return AwaitableGetTopicEventSubscriptionDeliveryAttributesResult(
        value=__ret__.value)


@_utilities.lift_output_func(get_topic_event_subscription_delivery_attributes)
def get_topic_event_subscription_delivery_attributes_output(event_subscription_name: Optional[pulumi.Input[str]] = None,
                                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                                            topic_name: Optional[pulumi.Input[str]] = None,
                                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTopicEventSubscriptionDeliveryAttributesResult]:
    """
    Get all delivery attributes for an event subscription for topic.


    :param str event_subscription_name: Name of the event subscription.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    :param str topic_name: Name of the domain topic.
    """
    ...
