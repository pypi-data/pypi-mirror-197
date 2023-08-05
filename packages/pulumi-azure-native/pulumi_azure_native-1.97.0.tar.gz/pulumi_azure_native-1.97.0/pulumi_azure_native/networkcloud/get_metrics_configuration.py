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
    'GetMetricsConfigurationResult',
    'AwaitableGetMetricsConfigurationResult',
    'get_metrics_configuration',
    'get_metrics_configuration_output',
]

@pulumi.output_type
class GetMetricsConfigurationResult:
    def __init__(__self__, collection_interval=None, detailed_status=None, detailed_status_message=None, disabled_metrics=None, enabled_metrics=None, extended_location=None, id=None, location=None, name=None, provisioning_state=None, system_data=None, tags=None, type=None):
        if collection_interval and not isinstance(collection_interval, float):
            raise TypeError("Expected argument 'collection_interval' to be a float")
        pulumi.set(__self__, "collection_interval", collection_interval)
        if detailed_status and not isinstance(detailed_status, str):
            raise TypeError("Expected argument 'detailed_status' to be a str")
        pulumi.set(__self__, "detailed_status", detailed_status)
        if detailed_status_message and not isinstance(detailed_status_message, str):
            raise TypeError("Expected argument 'detailed_status_message' to be a str")
        pulumi.set(__self__, "detailed_status_message", detailed_status_message)
        if disabled_metrics and not isinstance(disabled_metrics, list):
            raise TypeError("Expected argument 'disabled_metrics' to be a list")
        pulumi.set(__self__, "disabled_metrics", disabled_metrics)
        if enabled_metrics and not isinstance(enabled_metrics, list):
            raise TypeError("Expected argument 'enabled_metrics' to be a list")
        pulumi.set(__self__, "enabled_metrics", enabled_metrics)
        if extended_location and not isinstance(extended_location, dict):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, "extended_location", extended_location)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="collectionInterval")
    def collection_interval(self) -> float:
        """
        The interval in minutes by which metrics will be collected.
        """
        return pulumi.get(self, "collection_interval")

    @property
    @pulumi.getter(name="detailedStatus")
    def detailed_status(self) -> str:
        """
        The more detailed status of the metrics configuration.
        """
        return pulumi.get(self, "detailed_status")

    @property
    @pulumi.getter(name="detailedStatusMessage")
    def detailed_status_message(self) -> str:
        """
        The descriptive message about the current detailed status.
        """
        return pulumi.get(self, "detailed_status_message")

    @property
    @pulumi.getter(name="disabledMetrics")
    def disabled_metrics(self) -> Sequence[str]:
        """
        The list of metrics that are available for the cluster but disabled at the moment.
        """
        return pulumi.get(self, "disabled_metrics")

    @property
    @pulumi.getter(name="enabledMetrics")
    def enabled_metrics(self) -> Optional[Sequence[str]]:
        """
        The list of metric names that have been chosen to be enabled in addition to the core set of enabled metrics.
        """
        return pulumi.get(self, "enabled_metrics")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> 'outputs.ExtendedLocationResponse':
        """
        The extended location of the cluster associated with the resource.
        """
        return pulumi.get(self, "extended_location")

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
        The provisioning state of the metrics configuration.
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
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetMetricsConfigurationResult(GetMetricsConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMetricsConfigurationResult(
            collection_interval=self.collection_interval,
            detailed_status=self.detailed_status,
            detailed_status_message=self.detailed_status_message,
            disabled_metrics=self.disabled_metrics,
            enabled_metrics=self.enabled_metrics,
            extended_location=self.extended_location,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_metrics_configuration(cluster_name: Optional[str] = None,
                              metrics_configuration_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMetricsConfigurationResult:
    """
    Get metrics configuration of the provided cluster.
    API Version: 2022-12-12-preview.


    :param str cluster_name: The name of the cluster.
    :param str metrics_configuration_name: The name of the metrics configuration for the cluster.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['metricsConfigurationName'] = metrics_configuration_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:networkcloud:getMetricsConfiguration', __args__, opts=opts, typ=GetMetricsConfigurationResult).value

    return AwaitableGetMetricsConfigurationResult(
        collection_interval=__ret__.collection_interval,
        detailed_status=__ret__.detailed_status,
        detailed_status_message=__ret__.detailed_status_message,
        disabled_metrics=__ret__.disabled_metrics,
        enabled_metrics=__ret__.enabled_metrics,
        extended_location=__ret__.extended_location,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_metrics_configuration)
def get_metrics_configuration_output(cluster_name: Optional[pulumi.Input[str]] = None,
                                     metrics_configuration_name: Optional[pulumi.Input[str]] = None,
                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMetricsConfigurationResult]:
    """
    Get metrics configuration of the provided cluster.
    API Version: 2022-12-12-preview.


    :param str cluster_name: The name of the cluster.
    :param str metrics_configuration_name: The name of the metrics configuration for the cluster.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
