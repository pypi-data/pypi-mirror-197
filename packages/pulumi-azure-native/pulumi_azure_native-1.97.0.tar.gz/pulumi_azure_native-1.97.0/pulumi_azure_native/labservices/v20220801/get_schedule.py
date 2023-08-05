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
    'GetScheduleResult',
    'AwaitableGetScheduleResult',
    'get_schedule',
    'get_schedule_output',
]

@pulumi.output_type
class GetScheduleResult:
    """
    Schedule for automatically turning virtual machines in a lab on and off at specified times.
    """
    def __init__(__self__, id=None, name=None, notes=None, provisioning_state=None, recurrence_pattern=None, start_at=None, stop_at=None, system_data=None, time_zone_id=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notes and not isinstance(notes, str):
            raise TypeError("Expected argument 'notes' to be a str")
        pulumi.set(__self__, "notes", notes)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if recurrence_pattern and not isinstance(recurrence_pattern, dict):
            raise TypeError("Expected argument 'recurrence_pattern' to be a dict")
        pulumi.set(__self__, "recurrence_pattern", recurrence_pattern)
        if start_at and not isinstance(start_at, str):
            raise TypeError("Expected argument 'start_at' to be a str")
        pulumi.set(__self__, "start_at", start_at)
        if stop_at and not isinstance(stop_at, str):
            raise TypeError("Expected argument 'stop_at' to be a str")
        pulumi.set(__self__, "stop_at", stop_at)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if time_zone_id and not isinstance(time_zone_id, str):
            raise TypeError("Expected argument 'time_zone_id' to be a str")
        pulumi.set(__self__, "time_zone_id", time_zone_id)
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
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def notes(self) -> Optional[str]:
        """
        Notes for this schedule.
        """
        return pulumi.get(self, "notes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Current provisioning state of the schedule.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="recurrencePattern")
    def recurrence_pattern(self) -> Optional['outputs.RecurrencePatternResponse']:
        """
        The recurrence pattern of the scheduled actions.
        """
        return pulumi.get(self, "recurrence_pattern")

    @property
    @pulumi.getter(name="startAt")
    def start_at(self) -> Optional[str]:
        """
        When lab user virtual machines will be started. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        return pulumi.get(self, "start_at")

    @property
    @pulumi.getter(name="stopAt")
    def stop_at(self) -> str:
        """
        When lab user virtual machines will be stopped. Timestamp offsets will be ignored and timeZoneId is used instead.
        """
        return pulumi.get(self, "stop_at")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the schedule.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="timeZoneId")
    def time_zone_id(self) -> str:
        """
        The IANA timezone id for the schedule.
        """
        return pulumi.get(self, "time_zone_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetScheduleResult(GetScheduleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScheduleResult(
            id=self.id,
            name=self.name,
            notes=self.notes,
            provisioning_state=self.provisioning_state,
            recurrence_pattern=self.recurrence_pattern,
            start_at=self.start_at,
            stop_at=self.stop_at,
            system_data=self.system_data,
            time_zone_id=self.time_zone_id,
            type=self.type)


def get_schedule(lab_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 schedule_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScheduleResult:
    """
    Returns the properties of a lab Schedule.


    :param str lab_name: The name of the lab that uniquely identifies it within containing lab plan. Used in resource URIs.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str schedule_name: The name of the schedule that uniquely identifies it within containing lab. Used in resource URIs.
    """
    __args__ = dict()
    __args__['labName'] = lab_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['scheduleName'] = schedule_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:labservices/v20220801:getSchedule', __args__, opts=opts, typ=GetScheduleResult).value

    return AwaitableGetScheduleResult(
        id=__ret__.id,
        name=__ret__.name,
        notes=__ret__.notes,
        provisioning_state=__ret__.provisioning_state,
        recurrence_pattern=__ret__.recurrence_pattern,
        start_at=__ret__.start_at,
        stop_at=__ret__.stop_at,
        system_data=__ret__.system_data,
        time_zone_id=__ret__.time_zone_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_schedule)
def get_schedule_output(lab_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        schedule_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetScheduleResult]:
    """
    Returns the properties of a lab Schedule.


    :param str lab_name: The name of the lab that uniquely identifies it within containing lab plan. Used in resource URIs.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str schedule_name: The name of the schedule that uniquely identifies it within containing lab. Used in resource URIs.
    """
    ...
