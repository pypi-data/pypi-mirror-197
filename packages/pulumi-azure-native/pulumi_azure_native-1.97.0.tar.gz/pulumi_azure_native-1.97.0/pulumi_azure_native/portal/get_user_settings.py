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
    'GetUserSettingsResult',
    'AwaitableGetUserSettingsResult',
    'get_user_settings',
    'get_user_settings_output',
]

@pulumi.output_type
class GetUserSettingsResult:
    """
    Response to get user settings
    """
    def __init__(__self__, properties=None):
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.UserPropertiesResponse':
        """
        The cloud shell user settings properties.
        """
        return pulumi.get(self, "properties")


class AwaitableGetUserSettingsResult(GetUserSettingsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserSettingsResult(
            properties=self.properties)


def get_user_settings(user_settings_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserSettingsResult:
    """
    Get current user settings for current signed in user. This operation returns settings for the user's cloud shell preferences including preferred location, storage profile, shell type, font and size settings.
    API Version: 2018-10-01.


    :param str user_settings_name: The name of the user settings
    """
    __args__ = dict()
    __args__['userSettingsName'] = user_settings_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:portal:getUserSettings', __args__, opts=opts, typ=GetUserSettingsResult).value

    return AwaitableGetUserSettingsResult(
        properties=__ret__.properties)


@_utilities.lift_output_func(get_user_settings)
def get_user_settings_output(user_settings_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserSettingsResult]:
    """
    Get current user settings for current signed in user. This operation returns settings for the user's cloud shell preferences including preferred location, storage profile, shell type, font and size settings.
    API Version: 2018-10-01.


    :param str user_settings_name: The name of the user settings
    """
    ...
