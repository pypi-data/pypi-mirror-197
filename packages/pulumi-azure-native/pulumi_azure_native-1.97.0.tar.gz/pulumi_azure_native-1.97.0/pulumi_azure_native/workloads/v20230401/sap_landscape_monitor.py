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
from ._inputs import *

__all__ = ['SapLandscapeMonitorArgs', 'SapLandscapeMonitor']

@pulumi.input_type
class SapLandscapeMonitorArgs:
    def __init__(__self__, *,
                 monitor_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 grouping: Optional[pulumi.Input['SapLandscapeMonitorPropertiesGroupingArgs']] = None,
                 top_metrics_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input['SapLandscapeMonitorMetricThresholdsArgs']]]] = None):
        """
        The set of arguments for constructing a SapLandscapeMonitor resource.
        :param pulumi.Input[str] monitor_name: Name of the SAP monitor resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input['SapLandscapeMonitorPropertiesGroupingArgs'] grouping: Gets or sets the SID groupings by landscape and Environment.
        :param pulumi.Input[Sequence[pulumi.Input['SapLandscapeMonitorMetricThresholdsArgs']]] top_metrics_thresholds: Gets or sets the list Top Metric Thresholds for SAP Landscape Monitor Dashboard
        """
        pulumi.set(__self__, "monitor_name", monitor_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if grouping is not None:
            pulumi.set(__self__, "grouping", grouping)
        if top_metrics_thresholds is not None:
            pulumi.set(__self__, "top_metrics_thresholds", top_metrics_thresholds)

    @property
    @pulumi.getter(name="monitorName")
    def monitor_name(self) -> pulumi.Input[str]:
        """
        Name of the SAP monitor resource.
        """
        return pulumi.get(self, "monitor_name")

    @monitor_name.setter
    def monitor_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "monitor_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def grouping(self) -> Optional[pulumi.Input['SapLandscapeMonitorPropertiesGroupingArgs']]:
        """
        Gets or sets the SID groupings by landscape and Environment.
        """
        return pulumi.get(self, "grouping")

    @grouping.setter
    def grouping(self, value: Optional[pulumi.Input['SapLandscapeMonitorPropertiesGroupingArgs']]):
        pulumi.set(self, "grouping", value)

    @property
    @pulumi.getter(name="topMetricsThresholds")
    def top_metrics_thresholds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SapLandscapeMonitorMetricThresholdsArgs']]]]:
        """
        Gets or sets the list Top Metric Thresholds for SAP Landscape Monitor Dashboard
        """
        return pulumi.get(self, "top_metrics_thresholds")

    @top_metrics_thresholds.setter
    def top_metrics_thresholds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SapLandscapeMonitorMetricThresholdsArgs']]]]):
        pulumi.set(self, "top_metrics_thresholds", value)


class SapLandscapeMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 grouping: Optional[pulumi.Input[pulumi.InputType['SapLandscapeMonitorPropertiesGroupingArgs']]] = None,
                 monitor_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 top_metrics_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SapLandscapeMonitorMetricThresholdsArgs']]]]] = None,
                 __props__=None):
        """
        configuration associated with SAP Landscape Monitor Dashboard.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SapLandscapeMonitorPropertiesGroupingArgs']] grouping: Gets or sets the SID groupings by landscape and Environment.
        :param pulumi.Input[str] monitor_name: Name of the SAP monitor resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SapLandscapeMonitorMetricThresholdsArgs']]]] top_metrics_thresholds: Gets or sets the list Top Metric Thresholds for SAP Landscape Monitor Dashboard
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SapLandscapeMonitorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        configuration associated with SAP Landscape Monitor Dashboard.

        :param str resource_name: The name of the resource.
        :param SapLandscapeMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SapLandscapeMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 grouping: Optional[pulumi.Input[pulumi.InputType['SapLandscapeMonitorPropertiesGroupingArgs']]] = None,
                 monitor_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 top_metrics_thresholds: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SapLandscapeMonitorMetricThresholdsArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SapLandscapeMonitorArgs.__new__(SapLandscapeMonitorArgs)

            __props__.__dict__["grouping"] = grouping
            if monitor_name is None and not opts.urn:
                raise TypeError("Missing required property 'monitor_name'")
            __props__.__dict__["monitor_name"] = monitor_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["top_metrics_thresholds"] = top_metrics_thresholds
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:workloads/v20221101preview:SapLandscapeMonitor")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SapLandscapeMonitor, __self__).__init__(
            'azure-native:workloads/v20230401:SapLandscapeMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SapLandscapeMonitor':
        """
        Get an existing SapLandscapeMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SapLandscapeMonitorArgs.__new__(SapLandscapeMonitorArgs)

        __props__.__dict__["grouping"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["top_metrics_thresholds"] = None
        __props__.__dict__["type"] = None
        return SapLandscapeMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def grouping(self) -> pulumi.Output[Optional['outputs.SapLandscapeMonitorPropertiesResponseGrouping']]:
        """
        Gets or sets the SID groupings by landscape and Environment.
        """
        return pulumi.get(self, "grouping")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        State of provisioning of the SAP monitor.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="topMetricsThresholds")
    def top_metrics_thresholds(self) -> pulumi.Output[Optional[Sequence['outputs.SapLandscapeMonitorMetricThresholdsResponse']]]:
        """
        Gets or sets the list Top Metric Thresholds for SAP Landscape Monitor Dashboard
        """
        return pulumi.get(self, "top_metrics_thresholds")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

