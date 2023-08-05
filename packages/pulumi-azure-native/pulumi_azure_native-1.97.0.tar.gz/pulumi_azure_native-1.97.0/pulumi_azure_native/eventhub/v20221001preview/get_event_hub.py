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
    'GetEventHubResult',
    'AwaitableGetEventHubResult',
    'get_event_hub',
    'get_event_hub_output',
]

@pulumi.output_type
class GetEventHubResult:
    """
    Single item in List or Get Event Hub operation
    """
    def __init__(__self__, capture_description=None, created_at=None, id=None, location=None, message_retention_in_days=None, name=None, partition_count=None, partition_ids=None, retention_description=None, status=None, system_data=None, type=None, updated_at=None):
        if capture_description and not isinstance(capture_description, dict):
            raise TypeError("Expected argument 'capture_description' to be a dict")
        pulumi.set(__self__, "capture_description", capture_description)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if message_retention_in_days and not isinstance(message_retention_in_days, float):
            raise TypeError("Expected argument 'message_retention_in_days' to be a float")
        pulumi.set(__self__, "message_retention_in_days", message_retention_in_days)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if partition_count and not isinstance(partition_count, float):
            raise TypeError("Expected argument 'partition_count' to be a float")
        pulumi.set(__self__, "partition_count", partition_count)
        if partition_ids and not isinstance(partition_ids, list):
            raise TypeError("Expected argument 'partition_ids' to be a list")
        pulumi.set(__self__, "partition_ids", partition_ids)
        if retention_description and not isinstance(retention_description, dict):
            raise TypeError("Expected argument 'retention_description' to be a dict")
        pulumi.set(__self__, "retention_description", retention_description)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="captureDescription")
    def capture_description(self) -> Optional['outputs.CaptureDescriptionResponse']:
        """
        Properties of capture description
        """
        return pulumi.get(self, "capture_description")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Exact time the Event Hub was created.
        """
        return pulumi.get(self, "created_at")

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
    @pulumi.getter(name="messageRetentionInDays")
    def message_retention_in_days(self) -> Optional[float]:
        """
        Number of days to retain the events for this Event Hub, value should be 1 to 7 days
        """
        return pulumi.get(self, "message_retention_in_days")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partitionCount")
    def partition_count(self) -> Optional[float]:
        """
        Number of partitions created for the Event Hub, allowed values are from 1 to 32 partitions.
        """
        return pulumi.get(self, "partition_count")

    @property
    @pulumi.getter(name="partitionIds")
    def partition_ids(self) -> Sequence[str]:
        """
        Current number of shards on the Event Hub.
        """
        return pulumi.get(self, "partition_ids")

    @property
    @pulumi.getter(name="retentionDescription")
    def retention_description(self) -> Optional['outputs.RetentionDescriptionResponse']:
        """
        Event Hub retention settings
        """
        return pulumi.get(self, "retention_description")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Enumerates the possible values for the status of the Event Hub.
        """
        return pulumi.get(self, "status")

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

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The exact time the message was updated.
        """
        return pulumi.get(self, "updated_at")


class AwaitableGetEventHubResult(GetEventHubResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventHubResult(
            capture_description=self.capture_description,
            created_at=self.created_at,
            id=self.id,
            location=self.location,
            message_retention_in_days=self.message_retention_in_days,
            name=self.name,
            partition_count=self.partition_count,
            partition_ids=self.partition_ids,
            retention_description=self.retention_description,
            status=self.status,
            system_data=self.system_data,
            type=self.type,
            updated_at=self.updated_at)


def get_event_hub(event_hub_name: Optional[str] = None,
                  namespace_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventHubResult:
    """
    Gets an Event Hubs description for the specified Event Hub.


    :param str event_hub_name: The Event Hub name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    __args__ = dict()
    __args__['eventHubName'] = event_hub_name
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventhub/v20221001preview:getEventHub', __args__, opts=opts, typ=GetEventHubResult).value

    return AwaitableGetEventHubResult(
        capture_description=__ret__.capture_description,
        created_at=__ret__.created_at,
        id=__ret__.id,
        location=__ret__.location,
        message_retention_in_days=__ret__.message_retention_in_days,
        name=__ret__.name,
        partition_count=__ret__.partition_count,
        partition_ids=__ret__.partition_ids,
        retention_description=__ret__.retention_description,
        status=__ret__.status,
        system_data=__ret__.system_data,
        type=__ret__.type,
        updated_at=__ret__.updated_at)


@_utilities.lift_output_func(get_event_hub)
def get_event_hub_output(event_hub_name: Optional[pulumi.Input[str]] = None,
                         namespace_name: Optional[pulumi.Input[str]] = None,
                         resource_group_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventHubResult]:
    """
    Gets an Event Hubs description for the specified Event Hub.


    :param str event_hub_name: The Event Hub name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    ...
