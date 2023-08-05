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
    'GetPartnerTopicEventSubscriptionFullUrlResult',
    'AwaitableGetPartnerTopicEventSubscriptionFullUrlResult',
    'get_partner_topic_event_subscription_full_url',
    'get_partner_topic_event_subscription_full_url_output',
]

@pulumi.output_type
class GetPartnerTopicEventSubscriptionFullUrlResult:
    """
    Full endpoint url of an event subscription
    """
    def __init__(__self__, endpoint_url=None):
        if endpoint_url and not isinstance(endpoint_url, str):
            raise TypeError("Expected argument 'endpoint_url' to be a str")
        pulumi.set(__self__, "endpoint_url", endpoint_url)

    @property
    @pulumi.getter(name="endpointUrl")
    def endpoint_url(self) -> Optional[str]:
        """
        The URL that represents the endpoint of the destination of an event subscription.
        """
        return pulumi.get(self, "endpoint_url")


class AwaitableGetPartnerTopicEventSubscriptionFullUrlResult(GetPartnerTopicEventSubscriptionFullUrlResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPartnerTopicEventSubscriptionFullUrlResult(
            endpoint_url=self.endpoint_url)


def get_partner_topic_event_subscription_full_url(event_subscription_name: Optional[str] = None,
                                                  partner_topic_name: Optional[str] = None,
                                                  resource_group_name: Optional[str] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPartnerTopicEventSubscriptionFullUrlResult:
    """
    Get the full endpoint URL for an event subscription of a partner topic.


    :param str event_subscription_name: Name of the event subscription to be created. Event subscription names must be between 3 and 100 characters in length and use alphanumeric letters only.
    :param str partner_topic_name: Name of the partner topic.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    __args__ = dict()
    __args__['eventSubscriptionName'] = event_subscription_name
    __args__['partnerTopicName'] = partner_topic_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventgrid/v20211015preview:getPartnerTopicEventSubscriptionFullUrl', __args__, opts=opts, typ=GetPartnerTopicEventSubscriptionFullUrlResult).value

    return AwaitableGetPartnerTopicEventSubscriptionFullUrlResult(
        endpoint_url=__ret__.endpoint_url)


@_utilities.lift_output_func(get_partner_topic_event_subscription_full_url)
def get_partner_topic_event_subscription_full_url_output(event_subscription_name: Optional[pulumi.Input[str]] = None,
                                                         partner_topic_name: Optional[pulumi.Input[str]] = None,
                                                         resource_group_name: Optional[pulumi.Input[str]] = None,
                                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPartnerTopicEventSubscriptionFullUrlResult]:
    """
    Get the full endpoint URL for an event subscription of a partner topic.


    :param str event_subscription_name: Name of the event subscription to be created. Event subscription names must be between 3 and 100 characters in length and use alphanumeric letters only.
    :param str partner_topic_name: Name of the partner topic.
    :param str resource_group_name: The name of the resource group within the user's subscription.
    """
    ...
