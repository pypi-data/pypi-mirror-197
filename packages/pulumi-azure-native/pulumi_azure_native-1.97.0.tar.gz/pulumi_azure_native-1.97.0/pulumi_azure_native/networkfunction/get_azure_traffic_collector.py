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
    'GetAzureTrafficCollectorResult',
    'AwaitableGetAzureTrafficCollectorResult',
    'get_azure_traffic_collector',
    'get_azure_traffic_collector_output',
]

@pulumi.output_type
class GetAzureTrafficCollectorResult:
    """
    Azure Traffic Collector resource.
    """
    def __init__(__self__, collector_policies=None, etag=None, id=None, location=None, name=None, provisioning_state=None, system_data=None, tags=None, type=None, virtual_hub=None):
        if collector_policies and not isinstance(collector_policies, list):
            raise TypeError("Expected argument 'collector_policies' to be a list")
        pulumi.set(__self__, "collector_policies", collector_policies)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
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
        if virtual_hub and not isinstance(virtual_hub, dict):
            raise TypeError("Expected argument 'virtual_hub' to be a dict")
        pulumi.set(__self__, "virtual_hub", virtual_hub)

    @property
    @pulumi.getter(name="collectorPolicies")
    def collector_policies(self) -> Optional[Sequence['outputs.CollectorPolicyResponse']]:
        """
        Collector Policies for Azure Traffic Collector.
        """
        return pulumi.get(self, "collector_policies")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the application rule collection resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.TrackedResourceResponseSystemData':
        """
        Metadata pertaining to creation and last modification of the resource.
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
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualHub")
    def virtual_hub(self) -> Optional['outputs.ResourceReferenceResponse']:
        """
        The virtualHub to which the Azure Traffic Collector belongs.
        """
        return pulumi.get(self, "virtual_hub")


class AwaitableGetAzureTrafficCollectorResult(GetAzureTrafficCollectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAzureTrafficCollectorResult(
            collector_policies=self.collector_policies,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            virtual_hub=self.virtual_hub)


def get_azure_traffic_collector(azure_traffic_collector_name: Optional[str] = None,
                                resource_group_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAzureTrafficCollectorResult:
    """
    Gets the specified Azure Traffic Collector in a specified resource group
    API Version: 2022-05-01.


    :param str azure_traffic_collector_name: Azure Traffic Collector name
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['azureTrafficCollectorName'] = azure_traffic_collector_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:networkfunction:getAzureTrafficCollector', __args__, opts=opts, typ=GetAzureTrafficCollectorResult).value

    return AwaitableGetAzureTrafficCollectorResult(
        collector_policies=__ret__.collector_policies,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        virtual_hub=__ret__.virtual_hub)


@_utilities.lift_output_func(get_azure_traffic_collector)
def get_azure_traffic_collector_output(azure_traffic_collector_name: Optional[pulumi.Input[str]] = None,
                                       resource_group_name: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAzureTrafficCollectorResult]:
    """
    Gets the specified Azure Traffic Collector in a specified resource group
    API Version: 2022-05-01.


    :param str azure_traffic_collector_name: Azure Traffic Collector name
    :param str resource_group_name: The name of the resource group.
    """
    ...
