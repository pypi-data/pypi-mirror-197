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
    'ListBotConnectionServiceProvidersResult',
    'AwaitableListBotConnectionServiceProvidersResult',
    'list_bot_connection_service_providers',
]

@pulumi.output_type
class ListBotConnectionServiceProvidersResult:
    """
    The list of bot service providers response.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> Optional[str]:
        """
        The link used to get the next page of bot service providers.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.ServiceProviderResponse']:
        """
        Gets the list of bot service providers and their properties.
        """
        return pulumi.get(self, "value")


class AwaitableListBotConnectionServiceProvidersResult(ListBotConnectionServiceProvidersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListBotConnectionServiceProvidersResult(
            next_link=self.next_link,
            value=self.value)


def list_bot_connection_service_providers(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListBotConnectionServiceProvidersResult:
    """
    Lists the available Service Providers for creating Connection Settings
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:botservice/v20210501preview:listBotConnectionServiceProviders', __args__, opts=opts, typ=ListBotConnectionServiceProvidersResult).value

    return AwaitableListBotConnectionServiceProvidersResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
