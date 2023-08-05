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
    'GetConsoleWithLocationResult',
    'AwaitableGetConsoleWithLocationResult',
    'get_console_with_location',
    'get_console_with_location_output',
]

@pulumi.output_type
class GetConsoleWithLocationResult:
    """
    Cloud shell console
    """
    def __init__(__self__, properties=None):
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ConsolePropertiesResponse':
        """
        Cloud shell console properties.
        """
        return pulumi.get(self, "properties")


class AwaitableGetConsoleWithLocationResult(GetConsoleWithLocationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConsoleWithLocationResult(
            properties=self.properties)


def get_console_with_location(console_name: Optional[str] = None,
                              location: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConsoleWithLocationResult:
    """
    Gets the console for the user.
    API Version: 2018-10-01.


    :param str console_name: The name of the console
    :param str location: The provider location
    """
    __args__ = dict()
    __args__['consoleName'] = console_name
    __args__['location'] = location
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:portal:getConsoleWithLocation', __args__, opts=opts, typ=GetConsoleWithLocationResult).value

    return AwaitableGetConsoleWithLocationResult(
        properties=__ret__.properties)


@_utilities.lift_output_func(get_console_with_location)
def get_console_with_location_output(console_name: Optional[pulumi.Input[str]] = None,
                                     location: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConsoleWithLocationResult]:
    """
    Gets the console for the user.
    API Version: 2018-10-01.


    :param str console_name: The name of the console
    :param str location: The provider location
    """
    ...
