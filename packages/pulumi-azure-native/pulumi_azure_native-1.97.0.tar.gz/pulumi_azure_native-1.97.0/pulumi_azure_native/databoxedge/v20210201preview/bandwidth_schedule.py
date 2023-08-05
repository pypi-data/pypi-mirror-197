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
from ._enums import *

__all__ = ['BandwidthScheduleArgs', 'BandwidthSchedule']

@pulumi.input_type
class BandwidthScheduleArgs:
    def __init__(__self__, *,
                 days: pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]],
                 device_name: pulumi.Input[str],
                 rate_in_mbps: pulumi.Input[int],
                 resource_group_name: pulumi.Input[str],
                 start: pulumi.Input[str],
                 stop: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BandwidthSchedule resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]] days: The days of the week when this schedule is applicable.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[int] rate_in_mbps: The bandwidth rate in Mbps.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] start: The start time of the schedule in UTC.
        :param pulumi.Input[str] stop: The stop time of the schedule in UTC.
        :param pulumi.Input[str] name: The bandwidth schedule name which needs to be added/updated.
        """
        pulumi.set(__self__, "days", days)
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "rate_in_mbps", rate_in_mbps)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "start", start)
        pulumi.set(__self__, "stop", stop)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def days(self) -> pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]:
        """
        The days of the week when this schedule is applicable.
        """
        return pulumi.get(self, "days")

    @days.setter
    def days(self, value: pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]):
        pulumi.set(self, "days", value)

    @property
    @pulumi.getter(name="deviceName")
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, "device_name")

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_name", value)

    @property
    @pulumi.getter(name="rateInMbps")
    def rate_in_mbps(self) -> pulumi.Input[int]:
        """
        The bandwidth rate in Mbps.
        """
        return pulumi.get(self, "rate_in_mbps")

    @rate_in_mbps.setter
    def rate_in_mbps(self, value: pulumi.Input[int]):
        pulumi.set(self, "rate_in_mbps", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def start(self) -> pulumi.Input[str]:
        """
        The start time of the schedule in UTC.
        """
        return pulumi.get(self, "start")

    @start.setter
    def start(self, value: pulumi.Input[str]):
        pulumi.set(self, "start", value)

    @property
    @pulumi.getter
    def stop(self) -> pulumi.Input[str]:
        """
        The stop time of the schedule in UTC.
        """
        return pulumi.get(self, "stop")

    @stop.setter
    def stop(self, value: pulumi.Input[str]):
        pulumi.set(self, "stop", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The bandwidth schedule name which needs to be added/updated.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class BandwidthSchedule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 days: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rate_in_mbps: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start: Optional[pulumi.Input[str]] = None,
                 stop: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The bandwidth schedule details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]] days: The days of the week when this schedule is applicable.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] name: The bandwidth schedule name which needs to be added/updated.
        :param pulumi.Input[int] rate_in_mbps: The bandwidth rate in Mbps.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[str] start: The start time of the schedule in UTC.
        :param pulumi.Input[str] stop: The stop time of the schedule in UTC.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BandwidthScheduleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The bandwidth schedule details.

        :param str resource_name: The name of the resource.
        :param BandwidthScheduleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BandwidthScheduleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 days: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'DayOfWeek']]]]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rate_in_mbps: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 start: Optional[pulumi.Input[str]] = None,
                 stop: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BandwidthScheduleArgs.__new__(BandwidthScheduleArgs)

            if days is None and not opts.urn:
                raise TypeError("Missing required property 'days'")
            __props__.__dict__["days"] = days
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            __props__.__dict__["name"] = name
            if rate_in_mbps is None and not opts.urn:
                raise TypeError("Missing required property 'rate_in_mbps'")
            __props__.__dict__["rate_in_mbps"] = rate_in_mbps
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if start is None and not opts.urn:
                raise TypeError("Missing required property 'start'")
            __props__.__dict__["start"] = start
            if stop is None and not opts.urn:
                raise TypeError("Missing required property 'stop'")
            __props__.__dict__["stop"] = stop
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databoxedge:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20190301:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20190701:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20190801:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20200501preview:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20200901preview:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20210201:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20210601:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20210601preview:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20220301:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20220401preview:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20221201preview:BandwidthSchedule"), pulumi.Alias(type_="azure-native:databoxedge/v20230101preview:BandwidthSchedule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BandwidthSchedule, __self__).__init__(
            'azure-native:databoxedge/v20210201preview:BandwidthSchedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BandwidthSchedule':
        """
        Get an existing BandwidthSchedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BandwidthScheduleArgs.__new__(BandwidthScheduleArgs)

        __props__.__dict__["days"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["rate_in_mbps"] = None
        __props__.__dict__["start"] = None
        __props__.__dict__["stop"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return BandwidthSchedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def days(self) -> pulumi.Output[Sequence[str]]:
        """
        The days of the week when this schedule is applicable.
        """
        return pulumi.get(self, "days")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="rateInMbps")
    def rate_in_mbps(self) -> pulumi.Output[int]:
        """
        The bandwidth rate in Mbps.
        """
        return pulumi.get(self, "rate_in_mbps")

    @property
    @pulumi.getter
    def start(self) -> pulumi.Output[str]:
        """
        The start time of the schedule in UTC.
        """
        return pulumi.get(self, "start")

    @property
    @pulumi.getter
    def stop(self) -> pulumi.Output[str]:
        """
        The stop time of the schedule in UTC.
        """
        return pulumi.get(self, "stop")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Bandwidth object related to ASE resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

