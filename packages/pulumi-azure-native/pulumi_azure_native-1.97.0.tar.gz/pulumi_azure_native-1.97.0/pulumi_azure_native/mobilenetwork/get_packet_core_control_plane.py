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
    'GetPacketCoreControlPlaneResult',
    'AwaitableGetPacketCoreControlPlaneResult',
    'get_packet_core_control_plane',
    'get_packet_core_control_plane_output',
]

@pulumi.output_type
class GetPacketCoreControlPlaneResult:
    """
    Packet core control plane resource.
    """
    def __init__(__self__, control_plane_access_interface=None, core_network_technology=None, created_at=None, created_by=None, created_by_type=None, id=None, identity=None, interop_settings=None, last_modified_at=None, last_modified_by=None, last_modified_by_type=None, local_diagnostics_access=None, location=None, mobile_network=None, name=None, platform=None, provisioning_state=None, sku=None, system_data=None, tags=None, type=None, version=None):
        if control_plane_access_interface and not isinstance(control_plane_access_interface, dict):
            raise TypeError("Expected argument 'control_plane_access_interface' to be a dict")
        pulumi.set(__self__, "control_plane_access_interface", control_plane_access_interface)
        if core_network_technology and not isinstance(core_network_technology, str):
            raise TypeError("Expected argument 'core_network_technology' to be a str")
        pulumi.set(__self__, "core_network_technology", core_network_technology)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if created_by and not isinstance(created_by, str):
            raise TypeError("Expected argument 'created_by' to be a str")
        pulumi.set(__self__, "created_by", created_by)
        if created_by_type and not isinstance(created_by_type, str):
            raise TypeError("Expected argument 'created_by_type' to be a str")
        pulumi.set(__self__, "created_by_type", created_by_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if interop_settings and not isinstance(interop_settings, dict):
            raise TypeError("Expected argument 'interop_settings' to be a dict")
        pulumi.set(__self__, "interop_settings", interop_settings)
        if last_modified_at and not isinstance(last_modified_at, str):
            raise TypeError("Expected argument 'last_modified_at' to be a str")
        pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by and not isinstance(last_modified_by, str):
            raise TypeError("Expected argument 'last_modified_by' to be a str")
        pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type and not isinstance(last_modified_by_type, str):
            raise TypeError("Expected argument 'last_modified_by_type' to be a str")
        pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)
        if local_diagnostics_access and not isinstance(local_diagnostics_access, dict):
            raise TypeError("Expected argument 'local_diagnostics_access' to be a dict")
        pulumi.set(__self__, "local_diagnostics_access", local_diagnostics_access)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if mobile_network and not isinstance(mobile_network, dict):
            raise TypeError("Expected argument 'mobile_network' to be a dict")
        pulumi.set(__self__, "mobile_network", mobile_network)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform and not isinstance(platform, dict):
            raise TypeError("Expected argument 'platform' to be a dict")
        pulumi.set(__self__, "platform", platform)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="controlPlaneAccessInterface")
    def control_plane_access_interface(self) -> 'outputs.InterfacePropertiesResponse':
        """
        The control plane interface on the access network. For 5G networks, this is the N2 interface. For 4G networks, this is the S1-MME interface.
        """
        return pulumi.get(self, "control_plane_access_interface")

    @property
    @pulumi.getter(name="coreNetworkTechnology")
    def core_network_technology(self) -> Optional[str]:
        """
        The core network technology generation (5G core or EPC / 4G core).
        """
        return pulumi.get(self, "core_network_technology")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ManagedServiceIdentityResponse']:
        """
        The identity used to retrieve the ingress certificate from Azure key vault.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="interopSettings")
    def interop_settings(self) -> Optional[Any]:
        """
        Settings to allow interoperability with third party components e.g. RANs and UEs.
        """
        return pulumi.get(self, "interop_settings")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

    @property
    @pulumi.getter(name="localDiagnosticsAccess")
    def local_diagnostics_access(self) -> Optional['outputs.LocalDiagnosticsAccessConfigurationResponse']:
        """
        The kubernetes ingress configuration to control access to packet core diagnostics over local APIs.
        """
        return pulumi.get(self, "local_diagnostics_access")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mobileNetwork")
    def mobile_network(self) -> 'outputs.MobileNetworkResourceIdResponse':
        """
        Mobile network in which this packet core control plane is deployed.
        """
        return pulumi.get(self, "mobile_network")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> Optional['outputs.PlatformConfigurationResponse']:
        """
        The platform where the packet core is deployed.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the packet core control plane resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        The SKU defining the throughput and SIM allowances for this packet core control plane deployment.
        """
        return pulumi.get(self, "sku")

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

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        The version of the packet core software that is deployed.
        """
        return pulumi.get(self, "version")


class AwaitableGetPacketCoreControlPlaneResult(GetPacketCoreControlPlaneResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPacketCoreControlPlaneResult(
            control_plane_access_interface=self.control_plane_access_interface,
            core_network_technology=self.core_network_technology,
            created_at=self.created_at,
            created_by=self.created_by,
            created_by_type=self.created_by_type,
            id=self.id,
            identity=self.identity,
            interop_settings=self.interop_settings,
            last_modified_at=self.last_modified_at,
            last_modified_by=self.last_modified_by,
            last_modified_by_type=self.last_modified_by_type,
            local_diagnostics_access=self.local_diagnostics_access,
            location=self.location,
            mobile_network=self.mobile_network,
            name=self.name,
            platform=self.platform,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            version=self.version)


def get_packet_core_control_plane(packet_core_control_plane_name: Optional[str] = None,
                                  resource_group_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPacketCoreControlPlaneResult:
    """
    Gets information about the specified packet core control plane.
    API Version: 2022-04-01-preview.


    :param str packet_core_control_plane_name: The name of the packet core control plane.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['packetCoreControlPlaneName'] = packet_core_control_plane_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:mobilenetwork:getPacketCoreControlPlane', __args__, opts=opts, typ=GetPacketCoreControlPlaneResult).value

    return AwaitableGetPacketCoreControlPlaneResult(
        control_plane_access_interface=__ret__.control_plane_access_interface,
        core_network_technology=__ret__.core_network_technology,
        created_at=__ret__.created_at,
        created_by=__ret__.created_by,
        created_by_type=__ret__.created_by_type,
        id=__ret__.id,
        identity=__ret__.identity,
        interop_settings=__ret__.interop_settings,
        last_modified_at=__ret__.last_modified_at,
        last_modified_by=__ret__.last_modified_by,
        last_modified_by_type=__ret__.last_modified_by_type,
        local_diagnostics_access=__ret__.local_diagnostics_access,
        location=__ret__.location,
        mobile_network=__ret__.mobile_network,
        name=__ret__.name,
        platform=__ret__.platform,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        version=__ret__.version)


@_utilities.lift_output_func(get_packet_core_control_plane)
def get_packet_core_control_plane_output(packet_core_control_plane_name: Optional[pulumi.Input[str]] = None,
                                         resource_group_name: Optional[pulumi.Input[str]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPacketCoreControlPlaneResult]:
    """
    Gets information about the specified packet core control plane.
    API Version: 2022-04-01-preview.


    :param str packet_core_control_plane_name: The name of the packet core control plane.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
