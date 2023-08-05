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
    'ListNotificationHubKeysResult',
    'AwaitableListNotificationHubKeysResult',
    'list_notification_hub_keys',
    'list_notification_hub_keys_output',
]

@pulumi.output_type
class ListNotificationHubKeysResult:
    """
    Namespace/NotificationHub Connection String
    """
    def __init__(__self__, key_name=None, primary_connection_string=None, primary_key=None, secondary_connection_string=None, secondary_key=None):
        if key_name and not isinstance(key_name, str):
            raise TypeError("Expected argument 'key_name' to be a str")
        pulumi.set(__self__, "key_name", key_name)
        if primary_connection_string and not isinstance(primary_connection_string, str):
            raise TypeError("Expected argument 'primary_connection_string' to be a str")
        pulumi.set(__self__, "primary_connection_string", primary_connection_string)
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if secondary_connection_string and not isinstance(secondary_connection_string, str):
            raise TypeError("Expected argument 'secondary_connection_string' to be a str")
        pulumi.set(__self__, "secondary_connection_string", secondary_connection_string)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[str]:
        """
        KeyName of the created AuthorizationRule
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="primaryConnectionString")
    def primary_connection_string(self) -> Optional[str]:
        """
        PrimaryConnectionString of the AuthorizationRule.
        """
        return pulumi.get(self, "primary_connection_string")

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> Optional[str]:
        """
        PrimaryKey of the created AuthorizationRule.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="secondaryConnectionString")
    def secondary_connection_string(self) -> Optional[str]:
        """
        SecondaryConnectionString of the created AuthorizationRule
        """
        return pulumi.get(self, "secondary_connection_string")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> Optional[str]:
        """
        SecondaryKey of the created AuthorizationRule
        """
        return pulumi.get(self, "secondary_key")


class AwaitableListNotificationHubKeysResult(ListNotificationHubKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListNotificationHubKeysResult(
            key_name=self.key_name,
            primary_connection_string=self.primary_connection_string,
            primary_key=self.primary_key,
            secondary_connection_string=self.secondary_connection_string,
            secondary_key=self.secondary_key)


def list_notification_hub_keys(authorization_rule_name: Optional[str] = None,
                               namespace_name: Optional[str] = None,
                               notification_hub_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListNotificationHubKeysResult:
    """
    Gets the Primary and Secondary ConnectionStrings to the NotificationHub


    :param str authorization_rule_name: The connection string of the NotificationHub for the specified authorizationRule.
    :param str namespace_name: The namespace name.
    :param str notification_hub_name: The notification hub name.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['authorizationRuleName'] = authorization_rule_name
    __args__['namespaceName'] = namespace_name
    __args__['notificationHubName'] = notification_hub_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:notificationhubs/v20170401:listNotificationHubKeys', __args__, opts=opts, typ=ListNotificationHubKeysResult).value

    return AwaitableListNotificationHubKeysResult(
        key_name=__ret__.key_name,
        primary_connection_string=__ret__.primary_connection_string,
        primary_key=__ret__.primary_key,
        secondary_connection_string=__ret__.secondary_connection_string,
        secondary_key=__ret__.secondary_key)


@_utilities.lift_output_func(list_notification_hub_keys)
def list_notification_hub_keys_output(authorization_rule_name: Optional[pulumi.Input[str]] = None,
                                      namespace_name: Optional[pulumi.Input[str]] = None,
                                      notification_hub_name: Optional[pulumi.Input[str]] = None,
                                      resource_group_name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListNotificationHubKeysResult]:
    """
    Gets the Primary and Secondary ConnectionStrings to the NotificationHub


    :param str authorization_rule_name: The connection string of the NotificationHub for the specified authorizationRule.
    :param str namespace_name: The namespace name.
    :param str notification_hub_name: The notification hub name.
    :param str resource_group_name: The name of the resource group.
    """
    ...
