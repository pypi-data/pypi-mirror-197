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
    'GetVirtualNetworkTapResult',
    'AwaitableGetVirtualNetworkTapResult',
    'get_virtual_network_tap',
    'get_virtual_network_tap_output',
]

@pulumi.output_type
class GetVirtualNetworkTapResult:
    """
    Virtual Network Tap resource.
    """
    def __init__(__self__, destination_load_balancer_front_end_ip_configuration=None, destination_network_interface_ip_configuration=None, destination_port=None, etag=None, id=None, location=None, name=None, network_interface_tap_configurations=None, provisioning_state=None, resource_guid=None, tags=None, type=None):
        if destination_load_balancer_front_end_ip_configuration and not isinstance(destination_load_balancer_front_end_ip_configuration, dict):
            raise TypeError("Expected argument 'destination_load_balancer_front_end_ip_configuration' to be a dict")
        pulumi.set(__self__, "destination_load_balancer_front_end_ip_configuration", destination_load_balancer_front_end_ip_configuration)
        if destination_network_interface_ip_configuration and not isinstance(destination_network_interface_ip_configuration, dict):
            raise TypeError("Expected argument 'destination_network_interface_ip_configuration' to be a dict")
        pulumi.set(__self__, "destination_network_interface_ip_configuration", destination_network_interface_ip_configuration)
        if destination_port and not isinstance(destination_port, int):
            raise TypeError("Expected argument 'destination_port' to be a int")
        pulumi.set(__self__, "destination_port", destination_port)
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
        if network_interface_tap_configurations and not isinstance(network_interface_tap_configurations, list):
            raise TypeError("Expected argument 'network_interface_tap_configurations' to be a list")
        pulumi.set(__self__, "network_interface_tap_configurations", network_interface_tap_configurations)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_guid and not isinstance(resource_guid, str):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, "resource_guid", resource_guid)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="destinationLoadBalancerFrontEndIPConfiguration")
    def destination_load_balancer_front_end_ip_configuration(self) -> Optional['outputs.FrontendIPConfigurationResponse']:
        """
        The reference to the private IP address on the internal Load Balancer that will receive the tap.
        """
        return pulumi.get(self, "destination_load_balancer_front_end_ip_configuration")

    @property
    @pulumi.getter(name="destinationNetworkInterfaceIPConfiguration")
    def destination_network_interface_ip_configuration(self) -> Optional['outputs.NetworkInterfaceIPConfigurationResponse']:
        """
        The reference to the private IP Address of the collector nic that will receive the tap.
        """
        return pulumi.get(self, "destination_network_interface_ip_configuration")

    @property
    @pulumi.getter(name="destinationPort")
    def destination_port(self) -> Optional[int]:
        """
        The VXLAN destination port that will receive the tapped traffic.
        """
        return pulumi.get(self, "destination_port")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
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
    @pulumi.getter(name="networkInterfaceTapConfigurations")
    def network_interface_tap_configurations(self) -> Sequence['outputs.NetworkInterfaceTapConfigurationResponse']:
        """
        Specifies the list of resource IDs for the network interface IP configuration that needs to be tapped.
        """
        return pulumi.get(self, "network_interface_tap_configurations")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the virtual network tap. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> str:
        """
        The resourceGuid property of the virtual network tap.
        """
        return pulumi.get(self, "resource_guid")

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


class AwaitableGetVirtualNetworkTapResult(GetVirtualNetworkTapResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkTapResult(
            destination_load_balancer_front_end_ip_configuration=self.destination_load_balancer_front_end_ip_configuration,
            destination_network_interface_ip_configuration=self.destination_network_interface_ip_configuration,
            destination_port=self.destination_port,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            network_interface_tap_configurations=self.network_interface_tap_configurations,
            provisioning_state=self.provisioning_state,
            resource_guid=self.resource_guid,
            tags=self.tags,
            type=self.type)


def get_virtual_network_tap(resource_group_name: Optional[str] = None,
                            tap_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualNetworkTapResult:
    """
    Gets information about the specified virtual network tap.


    :param str resource_group_name: The name of the resource group.
    :param str tap_name: The name of virtual network tap.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['tapName'] = tap_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20190401:getVirtualNetworkTap', __args__, opts=opts, typ=GetVirtualNetworkTapResult).value

    return AwaitableGetVirtualNetworkTapResult(
        destination_load_balancer_front_end_ip_configuration=__ret__.destination_load_balancer_front_end_ip_configuration,
        destination_network_interface_ip_configuration=__ret__.destination_network_interface_ip_configuration,
        destination_port=__ret__.destination_port,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        network_interface_tap_configurations=__ret__.network_interface_tap_configurations,
        provisioning_state=__ret__.provisioning_state,
        resource_guid=__ret__.resource_guid,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_virtual_network_tap)
def get_virtual_network_tap_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                   tap_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualNetworkTapResult]:
    """
    Gets information about the specified virtual network tap.


    :param str resource_group_name: The name of the resource group.
    :param str tap_name: The name of virtual network tap.
    """
    ...
