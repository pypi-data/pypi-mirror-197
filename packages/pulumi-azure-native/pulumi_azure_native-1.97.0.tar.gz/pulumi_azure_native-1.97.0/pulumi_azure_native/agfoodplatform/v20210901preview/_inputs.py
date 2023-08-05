# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'ApiPropertiesArgs',
    'IdentityArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'SensorIntegrationArgs',
    'SolutionPropertiesArgs',
]

@pulumi.input_type
class ApiPropertiesArgs:
    def __init__(__self__, *,
                 api_freshness_time_in_minutes: Optional[pulumi.Input[int]] = None):
        """
        Api properties.
        :param pulumi.Input[int] api_freshness_time_in_minutes: Interval in minutes for which the weather data for the api needs to be refreshed.
        """
        if api_freshness_time_in_minutes is not None:
            pulumi.set(__self__, "api_freshness_time_in_minutes", api_freshness_time_in_minutes)

    @property
    @pulumi.getter(name="apiFreshnessTimeInMinutes")
    def api_freshness_time_in_minutes(self) -> Optional[pulumi.Input[int]]:
        """
        Interval in minutes for which the weather data for the api needs to be refreshed.
        """
        return pulumi.get(self, "api_freshness_time_in_minutes")

    @api_freshness_time_in_minutes.setter
    def api_freshness_time_in_minutes(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "api_freshness_time_in_minutes", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        Identity for the resource.
        :param pulumi.Input['ResourceIdentityType'] type: The identity type.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class SensorIntegrationArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[str]] = None):
        """
        Sensor integration request model.
        :param pulumi.Input[str] enabled: Sensor integration enable state. Allowed values are True, None
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[str]]:
        """
        Sensor integration enable state. Allowed values are True, None
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enabled", value)


@pulumi.input_type
class SolutionPropertiesArgs:
    def __init__(__self__, *,
                 marketplace_publisher_id: pulumi.Input[str],
                 offer_id: pulumi.Input[str],
                 plan_id: pulumi.Input[str],
                 saas_subscription_id: pulumi.Input[str],
                 saas_subscription_name: pulumi.Input[str],
                 term_id: pulumi.Input[str]):
        """
        Solution resource properties.
        :param pulumi.Input[str] marketplace_publisher_id: SaaS application Publisher Id.
        :param pulumi.Input[str] offer_id: SaaS application Offer Id.
        :param pulumi.Input[str] plan_id: SaaS application Plan Id.
        :param pulumi.Input[str] saas_subscription_id: SaaS subscriptionId of the installed SaaS application.
        :param pulumi.Input[str] saas_subscription_name: SaaS subscription name of the installed SaaS application.
        :param pulumi.Input[str] term_id: SaaS application Term Id.
        """
        pulumi.set(__self__, "marketplace_publisher_id", marketplace_publisher_id)
        pulumi.set(__self__, "offer_id", offer_id)
        pulumi.set(__self__, "plan_id", plan_id)
        pulumi.set(__self__, "saas_subscription_id", saas_subscription_id)
        pulumi.set(__self__, "saas_subscription_name", saas_subscription_name)
        pulumi.set(__self__, "term_id", term_id)

    @property
    @pulumi.getter(name="marketplacePublisherId")
    def marketplace_publisher_id(self) -> pulumi.Input[str]:
        """
        SaaS application Publisher Id.
        """
        return pulumi.get(self, "marketplace_publisher_id")

    @marketplace_publisher_id.setter
    def marketplace_publisher_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "marketplace_publisher_id", value)

    @property
    @pulumi.getter(name="offerId")
    def offer_id(self) -> pulumi.Input[str]:
        """
        SaaS application Offer Id.
        """
        return pulumi.get(self, "offer_id")

    @offer_id.setter
    def offer_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "offer_id", value)

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> pulumi.Input[str]:
        """
        SaaS application Plan Id.
        """
        return pulumi.get(self, "plan_id")

    @plan_id.setter
    def plan_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "plan_id", value)

    @property
    @pulumi.getter(name="saasSubscriptionId")
    def saas_subscription_id(self) -> pulumi.Input[str]:
        """
        SaaS subscriptionId of the installed SaaS application.
        """
        return pulumi.get(self, "saas_subscription_id")

    @saas_subscription_id.setter
    def saas_subscription_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "saas_subscription_id", value)

    @property
    @pulumi.getter(name="saasSubscriptionName")
    def saas_subscription_name(self) -> pulumi.Input[str]:
        """
        SaaS subscription name of the installed SaaS application.
        """
        return pulumi.get(self, "saas_subscription_name")

    @saas_subscription_name.setter
    def saas_subscription_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "saas_subscription_name", value)

    @property
    @pulumi.getter(name="termId")
    def term_id(self) -> pulumi.Input[str]:
        """
        SaaS application Term Id.
        """
        return pulumi.get(self, "term_id")

    @term_id.setter
    def term_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "term_id", value)


