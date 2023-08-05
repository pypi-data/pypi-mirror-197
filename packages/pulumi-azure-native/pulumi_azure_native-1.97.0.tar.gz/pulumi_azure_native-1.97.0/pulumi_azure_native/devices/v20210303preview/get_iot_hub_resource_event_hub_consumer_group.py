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
    'GetIotHubResourceEventHubConsumerGroupResult',
    'AwaitableGetIotHubResourceEventHubConsumerGroupResult',
    'get_iot_hub_resource_event_hub_consumer_group',
    'get_iot_hub_resource_event_hub_consumer_group_output',
]

@pulumi.output_type
class GetIotHubResourceEventHubConsumerGroupResult:
    """
    The properties of the EventHubConsumerGroupInfo object.
    """
    def __init__(__self__, etag=None, id=None, name=None, properties=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        The etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The Event Hub-compatible consumer group identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The Event Hub-compatible consumer group name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> Mapping[str, str]:
        """
        The tags.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        the resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetIotHubResourceEventHubConsumerGroupResult(GetIotHubResourceEventHubConsumerGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIotHubResourceEventHubConsumerGroupResult(
            etag=self.etag,
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_iot_hub_resource_event_hub_consumer_group(event_hub_endpoint_name: Optional[str] = None,
                                                  name: Optional[str] = None,
                                                  resource_group_name: Optional[str] = None,
                                                  resource_name: Optional[str] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIotHubResourceEventHubConsumerGroupResult:
    """
    Get a consumer group from the Event Hub-compatible device-to-cloud endpoint for an IoT hub.


    :param str event_hub_endpoint_name: The name of the Event Hub-compatible endpoint in the IoT hub.
    :param str name: The name of the consumer group to retrieve.
    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    __args__ = dict()
    __args__['eventHubEndpointName'] = event_hub_endpoint_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:devices/v20210303preview:getIotHubResourceEventHubConsumerGroup', __args__, opts=opts, typ=GetIotHubResourceEventHubConsumerGroupResult).value

    return AwaitableGetIotHubResourceEventHubConsumerGroupResult(
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)


@_utilities.lift_output_func(get_iot_hub_resource_event_hub_consumer_group)
def get_iot_hub_resource_event_hub_consumer_group_output(event_hub_endpoint_name: Optional[pulumi.Input[str]] = None,
                                                         name: Optional[pulumi.Input[str]] = None,
                                                         resource_group_name: Optional[pulumi.Input[str]] = None,
                                                         resource_name: Optional[pulumi.Input[str]] = None,
                                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIotHubResourceEventHubConsumerGroupResult]:
    """
    Get a consumer group from the Event Hub-compatible device-to-cloud endpoint for an IoT hub.


    :param str event_hub_endpoint_name: The name of the Event Hub-compatible endpoint in the IoT hub.
    :param str name: The name of the consumer group to retrieve.
    :param str resource_group_name: The name of the resource group that contains the IoT hub.
    :param str resource_name: The name of the IoT hub.
    """
    ...
