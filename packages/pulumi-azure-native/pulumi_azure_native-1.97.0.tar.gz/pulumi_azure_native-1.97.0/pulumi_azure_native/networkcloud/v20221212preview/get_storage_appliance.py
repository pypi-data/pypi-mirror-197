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
    'GetStorageApplianceResult',
    'AwaitableGetStorageApplianceResult',
    'get_storage_appliance',
    'get_storage_appliance_output',
]

@pulumi.output_type
class GetStorageApplianceResult:
    def __init__(__self__, administrator_credentials=None, capacity=None, capacity_used=None, cluster_id=None, detailed_status=None, detailed_status_message=None, extended_location=None, id=None, location=None, management_ipv4_address=None, name=None, provisioning_state=None, rack_id=None, rack_slot=None, remote_vendor_management_feature=None, remote_vendor_management_status=None, serial_number=None, storage_appliance_sku_id=None, system_data=None, tags=None, type=None):
        if administrator_credentials and not isinstance(administrator_credentials, dict):
            raise TypeError("Expected argument 'administrator_credentials' to be a dict")
        pulumi.set(__self__, "administrator_credentials", administrator_credentials)
        if capacity and not isinstance(capacity, float):
            raise TypeError("Expected argument 'capacity' to be a float")
        pulumi.set(__self__, "capacity", capacity)
        if capacity_used and not isinstance(capacity_used, float):
            raise TypeError("Expected argument 'capacity_used' to be a float")
        pulumi.set(__self__, "capacity_used", capacity_used)
        if cluster_id and not isinstance(cluster_id, str):
            raise TypeError("Expected argument 'cluster_id' to be a str")
        pulumi.set(__self__, "cluster_id", cluster_id)
        if detailed_status and not isinstance(detailed_status, str):
            raise TypeError("Expected argument 'detailed_status' to be a str")
        pulumi.set(__self__, "detailed_status", detailed_status)
        if detailed_status_message and not isinstance(detailed_status_message, str):
            raise TypeError("Expected argument 'detailed_status_message' to be a str")
        pulumi.set(__self__, "detailed_status_message", detailed_status_message)
        if extended_location and not isinstance(extended_location, dict):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, "extended_location", extended_location)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if management_ipv4_address and not isinstance(management_ipv4_address, str):
            raise TypeError("Expected argument 'management_ipv4_address' to be a str")
        pulumi.set(__self__, "management_ipv4_address", management_ipv4_address)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if rack_id and not isinstance(rack_id, str):
            raise TypeError("Expected argument 'rack_id' to be a str")
        pulumi.set(__self__, "rack_id", rack_id)
        if rack_slot and not isinstance(rack_slot, float):
            raise TypeError("Expected argument 'rack_slot' to be a float")
        pulumi.set(__self__, "rack_slot", rack_slot)
        if remote_vendor_management_feature and not isinstance(remote_vendor_management_feature, str):
            raise TypeError("Expected argument 'remote_vendor_management_feature' to be a str")
        pulumi.set(__self__, "remote_vendor_management_feature", remote_vendor_management_feature)
        if remote_vendor_management_status and not isinstance(remote_vendor_management_status, str):
            raise TypeError("Expected argument 'remote_vendor_management_status' to be a str")
        pulumi.set(__self__, "remote_vendor_management_status", remote_vendor_management_status)
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if storage_appliance_sku_id and not isinstance(storage_appliance_sku_id, str):
            raise TypeError("Expected argument 'storage_appliance_sku_id' to be a str")
        pulumi.set(__self__, "storage_appliance_sku_id", storage_appliance_sku_id)
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
    @pulumi.getter(name="administratorCredentials")
    def administrator_credentials(self) -> 'outputs.AdministrativeCredentialsResponse':
        return pulumi.get(self, "administrator_credentials")

    @property
    @pulumi.getter
    def capacity(self) -> float:
        """
        The total capacity of the storage appliance.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter(name="capacityUsed")
    def capacity_used(self) -> float:
        """
        The amount of storage consumed.
        """
        return pulumi.get(self, "capacity_used")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        """
        The resource ID of the cluster this storage appliance is associated with.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="detailedStatus")
    def detailed_status(self) -> str:
        """
        The detailed status of the storage appliance.
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
    @pulumi.getter(name="managementIpv4Address")
    def management_ipv4_address(self) -> str:
        """
        The endpoint for the management interface of the storage appliance.
        """
        return pulumi.get(self, "management_ipv4_address")

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
        The provisioning state of the storage appliance.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="rackId")
    def rack_id(self) -> str:
        """
        The resource ID of the rack where this storage appliance resides.
        """
        return pulumi.get(self, "rack_id")

    @property
    @pulumi.getter(name="rackSlot")
    def rack_slot(self) -> float:
        """
        The slot the storage appliance is in the rack based on the BOM configuration.
        """
        return pulumi.get(self, "rack_slot")

    @property
    @pulumi.getter(name="remoteVendorManagementFeature")
    def remote_vendor_management_feature(self) -> str:
        """
        The indicator of whether the storage appliance supports remote vendor management.
        """
        return pulumi.get(self, "remote_vendor_management_feature")

    @property
    @pulumi.getter(name="remoteVendorManagementStatus")
    def remote_vendor_management_status(self) -> str:
        """
        The indicator of whether the remote vendor management feature is enabled or disabled, or unsupported if it is an unsupported feature.
        """
        return pulumi.get(self, "remote_vendor_management_status")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> str:
        """
        The serial number for the storage appliance.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="storageApplianceSkuId")
    def storage_appliance_sku_id(self) -> str:
        """
        The SKU for the storage appliance.
        """
        return pulumi.get(self, "storage_appliance_sku_id")

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


class AwaitableGetStorageApplianceResult(GetStorageApplianceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageApplianceResult(
            administrator_credentials=self.administrator_credentials,
            capacity=self.capacity,
            capacity_used=self.capacity_used,
            cluster_id=self.cluster_id,
            detailed_status=self.detailed_status,
            detailed_status_message=self.detailed_status_message,
            extended_location=self.extended_location,
            id=self.id,
            location=self.location,
            management_ipv4_address=self.management_ipv4_address,
            name=self.name,
            provisioning_state=self.provisioning_state,
            rack_id=self.rack_id,
            rack_slot=self.rack_slot,
            remote_vendor_management_feature=self.remote_vendor_management_feature,
            remote_vendor_management_status=self.remote_vendor_management_status,
            serial_number=self.serial_number,
            storage_appliance_sku_id=self.storage_appliance_sku_id,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_storage_appliance(resource_group_name: Optional[str] = None,
                          storage_appliance_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStorageApplianceResult:
    """
    Get properties of the provided storage appliance.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str storage_appliance_name: The name of the storage appliance.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['storageApplianceName'] = storage_appliance_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:networkcloud/v20221212preview:getStorageAppliance', __args__, opts=opts, typ=GetStorageApplianceResult).value

    return AwaitableGetStorageApplianceResult(
        administrator_credentials=__ret__.administrator_credentials,
        capacity=__ret__.capacity,
        capacity_used=__ret__.capacity_used,
        cluster_id=__ret__.cluster_id,
        detailed_status=__ret__.detailed_status,
        detailed_status_message=__ret__.detailed_status_message,
        extended_location=__ret__.extended_location,
        id=__ret__.id,
        location=__ret__.location,
        management_ipv4_address=__ret__.management_ipv4_address,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        rack_id=__ret__.rack_id,
        rack_slot=__ret__.rack_slot,
        remote_vendor_management_feature=__ret__.remote_vendor_management_feature,
        remote_vendor_management_status=__ret__.remote_vendor_management_status,
        serial_number=__ret__.serial_number,
        storage_appliance_sku_id=__ret__.storage_appliance_sku_id,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_storage_appliance)
def get_storage_appliance_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                 storage_appliance_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetStorageApplianceResult]:
    """
    Get properties of the provided storage appliance.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str storage_appliance_name: The name of the storage appliance.
    """
    ...
