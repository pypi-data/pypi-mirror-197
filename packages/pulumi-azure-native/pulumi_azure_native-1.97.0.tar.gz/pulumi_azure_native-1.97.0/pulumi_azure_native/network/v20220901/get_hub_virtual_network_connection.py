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
    'GetHubVirtualNetworkConnectionResult',
    'AwaitableGetHubVirtualNetworkConnectionResult',
    'get_hub_virtual_network_connection',
    'get_hub_virtual_network_connection_output',
]

@pulumi.output_type
class GetHubVirtualNetworkConnectionResult:
    """
    HubVirtualNetworkConnection Resource.
    """
    def __init__(__self__, allow_hub_to_remote_vnet_transit=None, allow_remote_vnet_to_use_hub_vnet_gateways=None, enable_internet_security=None, etag=None, id=None, name=None, provisioning_state=None, remote_virtual_network=None, routing_configuration=None):
        if allow_hub_to_remote_vnet_transit and not isinstance(allow_hub_to_remote_vnet_transit, bool):
            raise TypeError("Expected argument 'allow_hub_to_remote_vnet_transit' to be a bool")
        pulumi.set(__self__, "allow_hub_to_remote_vnet_transit", allow_hub_to_remote_vnet_transit)
        if allow_remote_vnet_to_use_hub_vnet_gateways and not isinstance(allow_remote_vnet_to_use_hub_vnet_gateways, bool):
            raise TypeError("Expected argument 'allow_remote_vnet_to_use_hub_vnet_gateways' to be a bool")
        pulumi.set(__self__, "allow_remote_vnet_to_use_hub_vnet_gateways", allow_remote_vnet_to_use_hub_vnet_gateways)
        if enable_internet_security and not isinstance(enable_internet_security, bool):
            raise TypeError("Expected argument 'enable_internet_security' to be a bool")
        pulumi.set(__self__, "enable_internet_security", enable_internet_security)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if remote_virtual_network and not isinstance(remote_virtual_network, dict):
            raise TypeError("Expected argument 'remote_virtual_network' to be a dict")
        pulumi.set(__self__, "remote_virtual_network", remote_virtual_network)
        if routing_configuration and not isinstance(routing_configuration, dict):
            raise TypeError("Expected argument 'routing_configuration' to be a dict")
        pulumi.set(__self__, "routing_configuration", routing_configuration)

    @property
    @pulumi.getter(name="allowHubToRemoteVnetTransit")
    def allow_hub_to_remote_vnet_transit(self) -> Optional[bool]:
        """
        Deprecated: VirtualHub to RemoteVnet transit to enabled or not.
        """
        return pulumi.get(self, "allow_hub_to_remote_vnet_transit")

    @property
    @pulumi.getter(name="allowRemoteVnetToUseHubVnetGateways")
    def allow_remote_vnet_to_use_hub_vnet_gateways(self) -> Optional[bool]:
        """
        Deprecated: Allow RemoteVnet to use Virtual Hub's gateways.
        """
        return pulumi.get(self, "allow_remote_vnet_to_use_hub_vnet_gateways")

    @property
    @pulumi.getter(name="enableInternetSecurity")
    def enable_internet_security(self) -> Optional[bool]:
        """
        Enable internet security.
        """
        return pulumi.get(self, "enable_internet_security")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
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
    def name(self) -> Optional[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the hub virtual network connection resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="remoteVirtualNetwork")
    def remote_virtual_network(self) -> Optional['outputs.SubResourceResponse']:
        """
        Reference to the remote virtual network.
        """
        return pulumi.get(self, "remote_virtual_network")

    @property
    @pulumi.getter(name="routingConfiguration")
    def routing_configuration(self) -> Optional['outputs.RoutingConfigurationResponse']:
        """
        The Routing Configuration indicating the associated and propagated route tables on this connection.
        """
        return pulumi.get(self, "routing_configuration")


class AwaitableGetHubVirtualNetworkConnectionResult(GetHubVirtualNetworkConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHubVirtualNetworkConnectionResult(
            allow_hub_to_remote_vnet_transit=self.allow_hub_to_remote_vnet_transit,
            allow_remote_vnet_to_use_hub_vnet_gateways=self.allow_remote_vnet_to_use_hub_vnet_gateways,
            enable_internet_security=self.enable_internet_security,
            etag=self.etag,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            remote_virtual_network=self.remote_virtual_network,
            routing_configuration=self.routing_configuration)


def get_hub_virtual_network_connection(connection_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       virtual_hub_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHubVirtualNetworkConnectionResult:
    """
    Retrieves the details of a HubVirtualNetworkConnection.


    :param str connection_name: The name of the vpn connection.
    :param str resource_group_name: The resource group name of the VirtualHub.
    :param str virtual_hub_name: The name of the VirtualHub.
    """
    __args__ = dict()
    __args__['connectionName'] = connection_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualHubName'] = virtual_hub_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220901:getHubVirtualNetworkConnection', __args__, opts=opts, typ=GetHubVirtualNetworkConnectionResult).value

    return AwaitableGetHubVirtualNetworkConnectionResult(
        allow_hub_to_remote_vnet_transit=__ret__.allow_hub_to_remote_vnet_transit,
        allow_remote_vnet_to_use_hub_vnet_gateways=__ret__.allow_remote_vnet_to_use_hub_vnet_gateways,
        enable_internet_security=__ret__.enable_internet_security,
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        remote_virtual_network=__ret__.remote_virtual_network,
        routing_configuration=__ret__.routing_configuration)


@_utilities.lift_output_func(get_hub_virtual_network_connection)
def get_hub_virtual_network_connection_output(connection_name: Optional[pulumi.Input[str]] = None,
                                              resource_group_name: Optional[pulumi.Input[str]] = None,
                                              virtual_hub_name: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHubVirtualNetworkConnectionResult]:
    """
    Retrieves the details of a HubVirtualNetworkConnection.


    :param str connection_name: The name of the vpn connection.
    :param str resource_group_name: The resource group name of the VirtualHub.
    :param str virtual_hub_name: The name of the VirtualHub.
    """
    ...
