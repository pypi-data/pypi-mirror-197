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

__all__ = ['HubVirtualNetworkConnectionArgs', 'HubVirtualNetworkConnection']

@pulumi.input_type
class HubVirtualNetworkConnectionArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 virtual_hub_name: pulumi.Input[str],
                 allow_hub_to_remote_vnet_transit: Optional[pulumi.Input[bool]] = None,
                 allow_remote_vnet_to_use_hub_vnet_gateways: Optional[pulumi.Input[bool]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_internet_security: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_virtual_network: Optional[pulumi.Input['SubResourceArgs']] = None,
                 routing_configuration: Optional[pulumi.Input['RoutingConfigurationArgs']] = None):
        """
        The set of arguments for constructing a HubVirtualNetworkConnection resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the HubVirtualNetworkConnection.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
        :param pulumi.Input[bool] allow_hub_to_remote_vnet_transit: Deprecated: VirtualHub to RemoteVnet transit to enabled or not.
        :param pulumi.Input[bool] allow_remote_vnet_to_use_hub_vnet_gateways: Deprecated: Allow RemoteVnet to use Virtual Hub's gateways.
        :param pulumi.Input[str] connection_name: The name of the HubVirtualNetworkConnection.
        :param pulumi.Input[bool] enable_internet_security: Enable internet security.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input['SubResourceArgs'] remote_virtual_network: Reference to the remote virtual network.
        :param pulumi.Input['RoutingConfigurationArgs'] routing_configuration: The Routing Configuration indicating the associated and propagated route tables on this connection.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_hub_name", virtual_hub_name)
        if allow_hub_to_remote_vnet_transit is not None:
            pulumi.set(__self__, "allow_hub_to_remote_vnet_transit", allow_hub_to_remote_vnet_transit)
        if allow_remote_vnet_to_use_hub_vnet_gateways is not None:
            pulumi.set(__self__, "allow_remote_vnet_to_use_hub_vnet_gateways", allow_remote_vnet_to_use_hub_vnet_gateways)
        if connection_name is not None:
            pulumi.set(__self__, "connection_name", connection_name)
        if enable_internet_security is not None:
            pulumi.set(__self__, "enable_internet_security", enable_internet_security)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if remote_virtual_network is not None:
            pulumi.set(__self__, "remote_virtual_network", remote_virtual_network)
        if routing_configuration is not None:
            pulumi.set(__self__, "routing_configuration", routing_configuration)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name of the HubVirtualNetworkConnection.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="virtualHubName")
    def virtual_hub_name(self) -> pulumi.Input[str]:
        """
        The name of the VirtualHub.
        """
        return pulumi.get(self, "virtual_hub_name")

    @virtual_hub_name.setter
    def virtual_hub_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_hub_name", value)

    @property
    @pulumi.getter(name="allowHubToRemoteVnetTransit")
    def allow_hub_to_remote_vnet_transit(self) -> Optional[pulumi.Input[bool]]:
        """
        Deprecated: VirtualHub to RemoteVnet transit to enabled or not.
        """
        return pulumi.get(self, "allow_hub_to_remote_vnet_transit")

    @allow_hub_to_remote_vnet_transit.setter
    def allow_hub_to_remote_vnet_transit(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_hub_to_remote_vnet_transit", value)

    @property
    @pulumi.getter(name="allowRemoteVnetToUseHubVnetGateways")
    def allow_remote_vnet_to_use_hub_vnet_gateways(self) -> Optional[pulumi.Input[bool]]:
        """
        Deprecated: Allow RemoteVnet to use Virtual Hub's gateways.
        """
        return pulumi.get(self, "allow_remote_vnet_to_use_hub_vnet_gateways")

    @allow_remote_vnet_to_use_hub_vnet_gateways.setter
    def allow_remote_vnet_to_use_hub_vnet_gateways(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_remote_vnet_to_use_hub_vnet_gateways", value)

    @property
    @pulumi.getter(name="connectionName")
    def connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the HubVirtualNetworkConnection.
        """
        return pulumi.get(self, "connection_name")

    @connection_name.setter
    def connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_name", value)

    @property
    @pulumi.getter(name="enableInternetSecurity")
    def enable_internet_security(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable internet security.
        """
        return pulumi.get(self, "enable_internet_security")

    @enable_internet_security.setter
    def enable_internet_security(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_internet_security", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="remoteVirtualNetwork")
    def remote_virtual_network(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        Reference to the remote virtual network.
        """
        return pulumi.get(self, "remote_virtual_network")

    @remote_virtual_network.setter
    def remote_virtual_network(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "remote_virtual_network", value)

    @property
    @pulumi.getter(name="routingConfiguration")
    def routing_configuration(self) -> Optional[pulumi.Input['RoutingConfigurationArgs']]:
        """
        The Routing Configuration indicating the associated and propagated route tables on this connection.
        """
        return pulumi.get(self, "routing_configuration")

    @routing_configuration.setter
    def routing_configuration(self, value: Optional[pulumi.Input['RoutingConfigurationArgs']]):
        pulumi.set(self, "routing_configuration", value)


class HubVirtualNetworkConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_hub_to_remote_vnet_transit: Optional[pulumi.Input[bool]] = None,
                 allow_remote_vnet_to_use_hub_vnet_gateways: Optional[pulumi.Input[bool]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_internet_security: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_virtual_network: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_configuration: Optional[pulumi.Input[pulumi.InputType['RoutingConfigurationArgs']]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        HubVirtualNetworkConnection Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_hub_to_remote_vnet_transit: Deprecated: VirtualHub to RemoteVnet transit to enabled or not.
        :param pulumi.Input[bool] allow_remote_vnet_to_use_hub_vnet_gateways: Deprecated: Allow RemoteVnet to use Virtual Hub's gateways.
        :param pulumi.Input[str] connection_name: The name of the HubVirtualNetworkConnection.
        :param pulumi.Input[bool] enable_internet_security: Enable internet security.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] remote_virtual_network: Reference to the remote virtual network.
        :param pulumi.Input[str] resource_group_name: The resource group name of the HubVirtualNetworkConnection.
        :param pulumi.Input[pulumi.InputType['RoutingConfigurationArgs']] routing_configuration: The Routing Configuration indicating the associated and propagated route tables on this connection.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HubVirtualNetworkConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        HubVirtualNetworkConnection Resource.

        :param str resource_name: The name of the resource.
        :param HubVirtualNetworkConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HubVirtualNetworkConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_hub_to_remote_vnet_transit: Optional[pulumi.Input[bool]] = None,
                 allow_remote_vnet_to_use_hub_vnet_gateways: Optional[pulumi.Input[bool]] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_internet_security: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_virtual_network: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_configuration: Optional[pulumi.Input[pulumi.InputType['RoutingConfigurationArgs']]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HubVirtualNetworkConnectionArgs.__new__(HubVirtualNetworkConnectionArgs)

            __props__.__dict__["allow_hub_to_remote_vnet_transit"] = allow_hub_to_remote_vnet_transit
            __props__.__dict__["allow_remote_vnet_to_use_hub_vnet_gateways"] = allow_remote_vnet_to_use_hub_vnet_gateways
            __props__.__dict__["connection_name"] = connection_name
            __props__.__dict__["enable_internet_security"] = enable_internet_security
            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            __props__.__dict__["remote_virtual_network"] = remote_virtual_network
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["routing_configuration"] = routing_configuration
            if virtual_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_name'")
            __props__.__dict__["virtual_hub_name"] = virtual_hub_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["provisioning_state"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20200501:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20200601:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20200701:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20200801:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20201101:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20210201:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20210301:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20210801:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20220101:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20220501:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20220701:HubVirtualNetworkConnection"), pulumi.Alias(type_="azure-native:network/v20220901:HubVirtualNetworkConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(HubVirtualNetworkConnection, __self__).__init__(
            'azure-native:network/v20210501:HubVirtualNetworkConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'HubVirtualNetworkConnection':
        """
        Get an existing HubVirtualNetworkConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = HubVirtualNetworkConnectionArgs.__new__(HubVirtualNetworkConnectionArgs)

        __props__.__dict__["allow_hub_to_remote_vnet_transit"] = None
        __props__.__dict__["allow_remote_vnet_to_use_hub_vnet_gateways"] = None
        __props__.__dict__["enable_internet_security"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["remote_virtual_network"] = None
        __props__.__dict__["routing_configuration"] = None
        return HubVirtualNetworkConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowHubToRemoteVnetTransit")
    def allow_hub_to_remote_vnet_transit(self) -> pulumi.Output[Optional[bool]]:
        """
        Deprecated: VirtualHub to RemoteVnet transit to enabled or not.
        """
        return pulumi.get(self, "allow_hub_to_remote_vnet_transit")

    @property
    @pulumi.getter(name="allowRemoteVnetToUseHubVnetGateways")
    def allow_remote_vnet_to_use_hub_vnet_gateways(self) -> pulumi.Output[Optional[bool]]:
        """
        Deprecated: Allow RemoteVnet to use Virtual Hub's gateways.
        """
        return pulumi.get(self, "allow_remote_vnet_to_use_hub_vnet_gateways")

    @property
    @pulumi.getter(name="enableInternetSecurity")
    def enable_internet_security(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable internet security.
        """
        return pulumi.get(self, "enable_internet_security")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the hub virtual network connection resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="remoteVirtualNetwork")
    def remote_virtual_network(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Reference to the remote virtual network.
        """
        return pulumi.get(self, "remote_virtual_network")

    @property
    @pulumi.getter(name="routingConfiguration")
    def routing_configuration(self) -> pulumi.Output[Optional['outputs.RoutingConfigurationResponse']]:
        """
        The Routing Configuration indicating the associated and propagated route tables on this connection.
        """
        return pulumi.get(self, "routing_configuration")

