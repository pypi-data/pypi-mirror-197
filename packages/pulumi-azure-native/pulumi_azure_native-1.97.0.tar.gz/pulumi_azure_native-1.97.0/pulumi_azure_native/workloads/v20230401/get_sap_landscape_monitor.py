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
    'GetSapLandscapeMonitorResult',
    'AwaitableGetSapLandscapeMonitorResult',
    'get_sap_landscape_monitor',
    'get_sap_landscape_monitor_output',
]

@pulumi.output_type
class GetSapLandscapeMonitorResult:
    """
    configuration associated with SAP Landscape Monitor Dashboard.
    """
    def __init__(__self__, grouping=None, id=None, name=None, provisioning_state=None, system_data=None, top_metrics_thresholds=None, type=None):
        if grouping and not isinstance(grouping, dict):
            raise TypeError("Expected argument 'grouping' to be a dict")
        pulumi.set(__self__, "grouping", grouping)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if top_metrics_thresholds and not isinstance(top_metrics_thresholds, list):
            raise TypeError("Expected argument 'top_metrics_thresholds' to be a list")
        pulumi.set(__self__, "top_metrics_thresholds", top_metrics_thresholds)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def grouping(self) -> Optional['outputs.SapLandscapeMonitorPropertiesResponseGrouping']:
        """
        Gets or sets the SID groupings by landscape and Environment.
        """
        return pulumi.get(self, "grouping")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        State of provisioning of the SAP monitor.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="topMetricsThresholds")
    def top_metrics_thresholds(self) -> Optional[Sequence['outputs.SapLandscapeMonitorMetricThresholdsResponse']]:
        """
        Gets or sets the list Top Metric Thresholds for SAP Landscape Monitor Dashboard
        """
        return pulumi.get(self, "top_metrics_thresholds")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSapLandscapeMonitorResult(GetSapLandscapeMonitorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSapLandscapeMonitorResult(
            grouping=self.grouping,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            top_metrics_thresholds=self.top_metrics_thresholds,
            type=self.type)


def get_sap_landscape_monitor(monitor_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSapLandscapeMonitorResult:
    """
    Gets configuration values for Single Pane Of Glass for SAP monitor for the specified subscription, resource group, and resource name.


    :param str monitor_name: Name of the SAP monitor resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['monitorName'] = monitor_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:workloads/v20230401:getSapLandscapeMonitor', __args__, opts=opts, typ=GetSapLandscapeMonitorResult).value

    return AwaitableGetSapLandscapeMonitorResult(
        grouping=__ret__.grouping,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        top_metrics_thresholds=__ret__.top_metrics_thresholds,
        type=__ret__.type)


@_utilities.lift_output_func(get_sap_landscape_monitor)
def get_sap_landscape_monitor_output(monitor_name: Optional[pulumi.Input[str]] = None,
                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSapLandscapeMonitorResult]:
    """
    Gets configuration values for Single Pane Of Glass for SAP monitor for the specified subscription, resource group, and resource name.


    :param str monitor_name: Name of the SAP monitor resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
