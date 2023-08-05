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
    'GetClusterResult',
    'AwaitableGetClusterResult',
    'get_cluster',
    'get_cluster_output',
]

@pulumi.output_type
class GetClusterResult:
    """
    Class representing a Kusto cluster.
    """
    def __init__(__self__, data_ingestion_uri=None, enable_disk_encryption=None, enable_streaming_ingest=None, id=None, location=None, name=None, optimized_autoscale=None, provisioning_state=None, sku=None, state=None, tags=None, trusted_external_tenants=None, type=None, uri=None, virtual_network_configuration=None, zones=None):
        if data_ingestion_uri and not isinstance(data_ingestion_uri, str):
            raise TypeError("Expected argument 'data_ingestion_uri' to be a str")
        pulumi.set(__self__, "data_ingestion_uri", data_ingestion_uri)
        if enable_disk_encryption and not isinstance(enable_disk_encryption, bool):
            raise TypeError("Expected argument 'enable_disk_encryption' to be a bool")
        pulumi.set(__self__, "enable_disk_encryption", enable_disk_encryption)
        if enable_streaming_ingest and not isinstance(enable_streaming_ingest, bool):
            raise TypeError("Expected argument 'enable_streaming_ingest' to be a bool")
        pulumi.set(__self__, "enable_streaming_ingest", enable_streaming_ingest)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if optimized_autoscale and not isinstance(optimized_autoscale, dict):
            raise TypeError("Expected argument 'optimized_autoscale' to be a dict")
        pulumi.set(__self__, "optimized_autoscale", optimized_autoscale)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if trusted_external_tenants and not isinstance(trusted_external_tenants, list):
            raise TypeError("Expected argument 'trusted_external_tenants' to be a list")
        pulumi.set(__self__, "trusted_external_tenants", trusted_external_tenants)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if uri and not isinstance(uri, str):
            raise TypeError("Expected argument 'uri' to be a str")
        pulumi.set(__self__, "uri", uri)
        if virtual_network_configuration and not isinstance(virtual_network_configuration, dict):
            raise TypeError("Expected argument 'virtual_network_configuration' to be a dict")
        pulumi.set(__self__, "virtual_network_configuration", virtual_network_configuration)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="dataIngestionUri")
    def data_ingestion_uri(self) -> str:
        """
        The cluster data ingestion URI.
        """
        return pulumi.get(self, "data_ingestion_uri")

    @property
    @pulumi.getter(name="enableDiskEncryption")
    def enable_disk_encryption(self) -> Optional[bool]:
        """
        A boolean value that indicates if the cluster's disks are encrypted.
        """
        return pulumi.get(self, "enable_disk_encryption")

    @property
    @pulumi.getter(name="enableStreamingIngest")
    def enable_streaming_ingest(self) -> Optional[bool]:
        """
        A boolean value that indicates if the streaming ingest is enabled.
        """
        return pulumi.get(self, "enable_streaming_ingest")

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
    @pulumi.getter(name="optimizedAutoscale")
    def optimized_autoscale(self) -> Optional['outputs.OptimizedAutoscaleResponse']:
        """
        Optimized auto scale definition.
        """
        return pulumi.get(self, "optimized_autoscale")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioned state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.AzureSkuResponse':
        """
        The SKU of the cluster.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the resource.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="trustedExternalTenants")
    def trusted_external_tenants(self) -> Optional[Sequence['outputs.TrustedExternalTenantResponse']]:
        """
        The cluster's external tenants.
        """
        return pulumi.get(self, "trusted_external_tenants")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uri(self) -> str:
        """
        The cluster URI.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter(name="virtualNetworkConfiguration")
    def virtual_network_configuration(self) -> Optional['outputs.VirtualNetworkConfigurationResponse']:
        """
        Virtual network definition.
        """
        return pulumi.get(self, "virtual_network_configuration")

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        The availability zones of the cluster.
        """
        return pulumi.get(self, "zones")


class AwaitableGetClusterResult(GetClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetClusterResult(
            data_ingestion_uri=self.data_ingestion_uri,
            enable_disk_encryption=self.enable_disk_encryption,
            enable_streaming_ingest=self.enable_streaming_ingest,
            id=self.id,
            location=self.location,
            name=self.name,
            optimized_autoscale=self.optimized_autoscale,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            state=self.state,
            tags=self.tags,
            trusted_external_tenants=self.trusted_external_tenants,
            type=self.type,
            uri=self.uri,
            virtual_network_configuration=self.virtual_network_configuration,
            zones=self.zones)


def get_cluster(cluster_name: Optional[str] = None,
                resource_group_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetClusterResult:
    """
    Gets a Kusto cluster.


    :param str cluster_name: The name of the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:kusto/v20190515:getCluster', __args__, opts=opts, typ=GetClusterResult).value

    return AwaitableGetClusterResult(
        data_ingestion_uri=__ret__.data_ingestion_uri,
        enable_disk_encryption=__ret__.enable_disk_encryption,
        enable_streaming_ingest=__ret__.enable_streaming_ingest,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        optimized_autoscale=__ret__.optimized_autoscale,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        state=__ret__.state,
        tags=__ret__.tags,
        trusted_external_tenants=__ret__.trusted_external_tenants,
        type=__ret__.type,
        uri=__ret__.uri,
        virtual_network_configuration=__ret__.virtual_network_configuration,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_cluster)
def get_cluster_output(cluster_name: Optional[pulumi.Input[str]] = None,
                       resource_group_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetClusterResult]:
    """
    Gets a Kusto cluster.


    :param str cluster_name: The name of the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    ...
