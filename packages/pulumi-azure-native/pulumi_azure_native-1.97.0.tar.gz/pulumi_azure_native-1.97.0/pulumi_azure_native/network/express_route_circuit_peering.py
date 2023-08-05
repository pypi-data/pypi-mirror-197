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
from ._enums import *
from ._inputs import *

__all__ = ['ExpressRouteCircuitPeeringInitArgs', 'ExpressRouteCircuitPeering']

@pulumi.input_type
class ExpressRouteCircuitPeeringInitArgs:
    def __init__(__self__, *,
                 circuit_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 azure_asn: Optional[pulumi.Input[int]] = None,
                 connections: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitConnectionArgs']]]] = None,
                 gateway_manager_etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipv6_peering_config: Optional[pulumi.Input['Ipv6ExpressRouteCircuitPeeringConfigArgs']] = None,
                 microsoft_peering_config: Optional[pulumi.Input['ExpressRouteCircuitPeeringConfigArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 peer_asn: Optional[pulumi.Input[float]] = None,
                 peering_name: Optional[pulumi.Input[str]] = None,
                 peering_type: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringType']]] = None,
                 primary_azure_port: Optional[pulumi.Input[str]] = None,
                 primary_peer_address_prefix: Optional[pulumi.Input[str]] = None,
                 route_filter: Optional[pulumi.Input['SubResourceArgs']] = None,
                 secondary_azure_port: Optional[pulumi.Input[str]] = None,
                 secondary_peer_address_prefix: Optional[pulumi.Input[str]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringState']]] = None,
                 stats: Optional[pulumi.Input['ExpressRouteCircuitStatsArgs']] = None,
                 vlan_id: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a ExpressRouteCircuitPeering resource.
        :param pulumi.Input[str] circuit_name: The name of the express route circuit.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[int] azure_asn: The Azure ASN.
        :param pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitConnectionArgs']]] connections: The list of circuit connections associated with Azure Private Peering for this circuit.
        :param pulumi.Input[str] gateway_manager_etag: The GatewayManager Etag.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input['Ipv6ExpressRouteCircuitPeeringConfigArgs'] ipv6_peering_config: The IPv6 peering configuration.
        :param pulumi.Input['ExpressRouteCircuitPeeringConfigArgs'] microsoft_peering_config: The Microsoft peering configuration.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[float] peer_asn: The peer ASN.
        :param pulumi.Input[str] peering_name: The name of the peering.
        :param pulumi.Input[Union[str, 'ExpressRoutePeeringType']] peering_type: The peering type.
        :param pulumi.Input[str] primary_azure_port: The primary port.
        :param pulumi.Input[str] primary_peer_address_prefix: The primary address prefix.
        :param pulumi.Input['SubResourceArgs'] route_filter: The reference to the RouteFilter resource.
        :param pulumi.Input[str] secondary_azure_port: The secondary port.
        :param pulumi.Input[str] secondary_peer_address_prefix: The secondary address prefix.
        :param pulumi.Input[str] shared_key: The shared key.
        :param pulumi.Input[Union[str, 'ExpressRoutePeeringState']] state: The peering state.
        :param pulumi.Input['ExpressRouteCircuitStatsArgs'] stats: The peering stats of express route circuit.
        :param pulumi.Input[int] vlan_id: The VLAN ID.
        """
        pulumi.set(__self__, "circuit_name", circuit_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if azure_asn is not None:
            pulumi.set(__self__, "azure_asn", azure_asn)
        if connections is not None:
            pulumi.set(__self__, "connections", connections)
        if gateway_manager_etag is not None:
            pulumi.set(__self__, "gateway_manager_etag", gateway_manager_etag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ipv6_peering_config is not None:
            pulumi.set(__self__, "ipv6_peering_config", ipv6_peering_config)
        if microsoft_peering_config is not None:
            pulumi.set(__self__, "microsoft_peering_config", microsoft_peering_config)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if peer_asn is not None:
            pulumi.set(__self__, "peer_asn", peer_asn)
        if peering_name is not None:
            pulumi.set(__self__, "peering_name", peering_name)
        if peering_type is not None:
            pulumi.set(__self__, "peering_type", peering_type)
        if primary_azure_port is not None:
            pulumi.set(__self__, "primary_azure_port", primary_azure_port)
        if primary_peer_address_prefix is not None:
            pulumi.set(__self__, "primary_peer_address_prefix", primary_peer_address_prefix)
        if route_filter is not None:
            pulumi.set(__self__, "route_filter", route_filter)
        if secondary_azure_port is not None:
            pulumi.set(__self__, "secondary_azure_port", secondary_azure_port)
        if secondary_peer_address_prefix is not None:
            pulumi.set(__self__, "secondary_peer_address_prefix", secondary_peer_address_prefix)
        if shared_key is not None:
            pulumi.set(__self__, "shared_key", shared_key)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if stats is not None:
            pulumi.set(__self__, "stats", stats)
        if vlan_id is not None:
            pulumi.set(__self__, "vlan_id", vlan_id)

    @property
    @pulumi.getter(name="circuitName")
    def circuit_name(self) -> pulumi.Input[str]:
        """
        The name of the express route circuit.
        """
        return pulumi.get(self, "circuit_name")

    @circuit_name.setter
    def circuit_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "circuit_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="azureASN")
    def azure_asn(self) -> Optional[pulumi.Input[int]]:
        """
        The Azure ASN.
        """
        return pulumi.get(self, "azure_asn")

    @azure_asn.setter
    def azure_asn(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "azure_asn", value)

    @property
    @pulumi.getter
    def connections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitConnectionArgs']]]]:
        """
        The list of circuit connections associated with Azure Private Peering for this circuit.
        """
        return pulumi.get(self, "connections")

    @connections.setter
    def connections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitConnectionArgs']]]]):
        pulumi.set(self, "connections", value)

    @property
    @pulumi.getter(name="gatewayManagerEtag")
    def gateway_manager_etag(self) -> Optional[pulumi.Input[str]]:
        """
        The GatewayManager Etag.
        """
        return pulumi.get(self, "gateway_manager_etag")

    @gateway_manager_etag.setter
    def gateway_manager_etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gateway_manager_etag", value)

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
    @pulumi.getter(name="ipv6PeeringConfig")
    def ipv6_peering_config(self) -> Optional[pulumi.Input['Ipv6ExpressRouteCircuitPeeringConfigArgs']]:
        """
        The IPv6 peering configuration.
        """
        return pulumi.get(self, "ipv6_peering_config")

    @ipv6_peering_config.setter
    def ipv6_peering_config(self, value: Optional[pulumi.Input['Ipv6ExpressRouteCircuitPeeringConfigArgs']]):
        pulumi.set(self, "ipv6_peering_config", value)

    @property
    @pulumi.getter(name="microsoftPeeringConfig")
    def microsoft_peering_config(self) -> Optional[pulumi.Input['ExpressRouteCircuitPeeringConfigArgs']]:
        """
        The Microsoft peering configuration.
        """
        return pulumi.get(self, "microsoft_peering_config")

    @microsoft_peering_config.setter
    def microsoft_peering_config(self, value: Optional[pulumi.Input['ExpressRouteCircuitPeeringConfigArgs']]):
        pulumi.set(self, "microsoft_peering_config", value)

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
    @pulumi.getter(name="peerASN")
    def peer_asn(self) -> Optional[pulumi.Input[float]]:
        """
        The peer ASN.
        """
        return pulumi.get(self, "peer_asn")

    @peer_asn.setter
    def peer_asn(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "peer_asn", value)

    @property
    @pulumi.getter(name="peeringName")
    def peering_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the peering.
        """
        return pulumi.get(self, "peering_name")

    @peering_name.setter
    def peering_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "peering_name", value)

    @property
    @pulumi.getter(name="peeringType")
    def peering_type(self) -> Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringType']]]:
        """
        The peering type.
        """
        return pulumi.get(self, "peering_type")

    @peering_type.setter
    def peering_type(self, value: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringType']]]):
        pulumi.set(self, "peering_type", value)

    @property
    @pulumi.getter(name="primaryAzurePort")
    def primary_azure_port(self) -> Optional[pulumi.Input[str]]:
        """
        The primary port.
        """
        return pulumi.get(self, "primary_azure_port")

    @primary_azure_port.setter
    def primary_azure_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_azure_port", value)

    @property
    @pulumi.getter(name="primaryPeerAddressPrefix")
    def primary_peer_address_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The primary address prefix.
        """
        return pulumi.get(self, "primary_peer_address_prefix")

    @primary_peer_address_prefix.setter
    def primary_peer_address_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_peer_address_prefix", value)

    @property
    @pulumi.getter(name="routeFilter")
    def route_filter(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The reference to the RouteFilter resource.
        """
        return pulumi.get(self, "route_filter")

    @route_filter.setter
    def route_filter(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "route_filter", value)

    @property
    @pulumi.getter(name="secondaryAzurePort")
    def secondary_azure_port(self) -> Optional[pulumi.Input[str]]:
        """
        The secondary port.
        """
        return pulumi.get(self, "secondary_azure_port")

    @secondary_azure_port.setter
    def secondary_azure_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_azure_port", value)

    @property
    @pulumi.getter(name="secondaryPeerAddressPrefix")
    def secondary_peer_address_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The secondary address prefix.
        """
        return pulumi.get(self, "secondary_peer_address_prefix")

    @secondary_peer_address_prefix.setter
    def secondary_peer_address_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "secondary_peer_address_prefix", value)

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> Optional[pulumi.Input[str]]:
        """
        The shared key.
        """
        return pulumi.get(self, "shared_key")

    @shared_key.setter
    def shared_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "shared_key", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringState']]]:
        """
        The peering state.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringState']]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def stats(self) -> Optional[pulumi.Input['ExpressRouteCircuitStatsArgs']]:
        """
        The peering stats of express route circuit.
        """
        return pulumi.get(self, "stats")

    @stats.setter
    def stats(self, value: Optional[pulumi.Input['ExpressRouteCircuitStatsArgs']]):
        pulumi.set(self, "stats", value)

    @property
    @pulumi.getter(name="vlanId")
    def vlan_id(self) -> Optional[pulumi.Input[int]]:
        """
        The VLAN ID.
        """
        return pulumi.get(self, "vlan_id")

    @vlan_id.setter
    def vlan_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "vlan_id", value)


class ExpressRouteCircuitPeering(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 azure_asn: Optional[pulumi.Input[int]] = None,
                 circuit_name: Optional[pulumi.Input[str]] = None,
                 connections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitConnectionArgs']]]]] = None,
                 gateway_manager_etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipv6_peering_config: Optional[pulumi.Input[pulumi.InputType['Ipv6ExpressRouteCircuitPeeringConfigArgs']]] = None,
                 microsoft_peering_config: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitPeeringConfigArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 peer_asn: Optional[pulumi.Input[float]] = None,
                 peering_name: Optional[pulumi.Input[str]] = None,
                 peering_type: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringType']]] = None,
                 primary_azure_port: Optional[pulumi.Input[str]] = None,
                 primary_peer_address_prefix: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 route_filter: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 secondary_azure_port: Optional[pulumi.Input[str]] = None,
                 secondary_peer_address_prefix: Optional[pulumi.Input[str]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringState']]] = None,
                 stats: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitStatsArgs']]] = None,
                 vlan_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Peering in an ExpressRouteCircuit resource.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] azure_asn: The Azure ASN.
        :param pulumi.Input[str] circuit_name: The name of the express route circuit.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitConnectionArgs']]]] connections: The list of circuit connections associated with Azure Private Peering for this circuit.
        :param pulumi.Input[str] gateway_manager_etag: The GatewayManager Etag.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[pulumi.InputType['Ipv6ExpressRouteCircuitPeeringConfigArgs']] ipv6_peering_config: The IPv6 peering configuration.
        :param pulumi.Input[pulumi.InputType['ExpressRouteCircuitPeeringConfigArgs']] microsoft_peering_config: The Microsoft peering configuration.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[float] peer_asn: The peer ASN.
        :param pulumi.Input[str] peering_name: The name of the peering.
        :param pulumi.Input[Union[str, 'ExpressRoutePeeringType']] peering_type: The peering type.
        :param pulumi.Input[str] primary_azure_port: The primary port.
        :param pulumi.Input[str] primary_peer_address_prefix: The primary address prefix.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] route_filter: The reference to the RouteFilter resource.
        :param pulumi.Input[str] secondary_azure_port: The secondary port.
        :param pulumi.Input[str] secondary_peer_address_prefix: The secondary address prefix.
        :param pulumi.Input[str] shared_key: The shared key.
        :param pulumi.Input[Union[str, 'ExpressRoutePeeringState']] state: The peering state.
        :param pulumi.Input[pulumi.InputType['ExpressRouteCircuitStatsArgs']] stats: The peering stats of express route circuit.
        :param pulumi.Input[int] vlan_id: The VLAN ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ExpressRouteCircuitPeeringInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Peering in an ExpressRouteCircuit resource.
        API Version: 2020-11-01.

        :param str resource_name: The name of the resource.
        :param ExpressRouteCircuitPeeringInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ExpressRouteCircuitPeeringInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 azure_asn: Optional[pulumi.Input[int]] = None,
                 circuit_name: Optional[pulumi.Input[str]] = None,
                 connections: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitConnectionArgs']]]]] = None,
                 gateway_manager_etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipv6_peering_config: Optional[pulumi.Input[pulumi.InputType['Ipv6ExpressRouteCircuitPeeringConfigArgs']]] = None,
                 microsoft_peering_config: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitPeeringConfigArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 peer_asn: Optional[pulumi.Input[float]] = None,
                 peering_name: Optional[pulumi.Input[str]] = None,
                 peering_type: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringType']]] = None,
                 primary_azure_port: Optional[pulumi.Input[str]] = None,
                 primary_peer_address_prefix: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 route_filter: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 secondary_azure_port: Optional[pulumi.Input[str]] = None,
                 secondary_peer_address_prefix: Optional[pulumi.Input[str]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[Union[str, 'ExpressRoutePeeringState']]] = None,
                 stats: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitStatsArgs']]] = None,
                 vlan_id: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ExpressRouteCircuitPeeringInitArgs.__new__(ExpressRouteCircuitPeeringInitArgs)

            __props__.__dict__["azure_asn"] = azure_asn
            if circuit_name is None and not opts.urn:
                raise TypeError("Missing required property 'circuit_name'")
            __props__.__dict__["circuit_name"] = circuit_name
            __props__.__dict__["connections"] = connections
            __props__.__dict__["gateway_manager_etag"] = gateway_manager_etag
            __props__.__dict__["id"] = id
            __props__.__dict__["ipv6_peering_config"] = ipv6_peering_config
            __props__.__dict__["microsoft_peering_config"] = microsoft_peering_config
            __props__.__dict__["name"] = name
            __props__.__dict__["peer_asn"] = peer_asn
            __props__.__dict__["peering_name"] = peering_name
            __props__.__dict__["peering_type"] = peering_type
            __props__.__dict__["primary_azure_port"] = primary_azure_port
            __props__.__dict__["primary_peer_address_prefix"] = primary_peer_address_prefix
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["route_filter"] = route_filter
            __props__.__dict__["secondary_azure_port"] = secondary_azure_port
            __props__.__dict__["secondary_peer_address_prefix"] = secondary_peer_address_prefix
            __props__.__dict__["shared_key"] = shared_key
            __props__.__dict__["state"] = state
            __props__.__dict__["stats"] = stats
            __props__.__dict__["vlan_id"] = vlan_id
            __props__.__dict__["etag"] = None
            __props__.__dict__["express_route_connection"] = None
            __props__.__dict__["last_modified_by"] = None
            __props__.__dict__["peered_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network/v20150501preview:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20150615:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20160330:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20160601:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20160901:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20161201:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20170301:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20170601:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20170801:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20170901:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20171001:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20171101:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20180101:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20180201:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20180401:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20180601:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20180701:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20180801:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20181001:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20181101:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20181201:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20190201:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20190401:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20190601:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20190701:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20190801:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20190901:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20191101:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20191201:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20200301:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20200401:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20200501:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20200601:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20200701:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20200801:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20201101:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20210201:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20210301:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20210501:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20210801:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20220101:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20220501:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20220701:ExpressRouteCircuitPeering"), pulumi.Alias(type_="azure-native:network/v20220901:ExpressRouteCircuitPeering")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ExpressRouteCircuitPeering, __self__).__init__(
            'azure-native:network:ExpressRouteCircuitPeering',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ExpressRouteCircuitPeering':
        """
        Get an existing ExpressRouteCircuitPeering resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ExpressRouteCircuitPeeringInitArgs.__new__(ExpressRouteCircuitPeeringInitArgs)

        __props__.__dict__["azure_asn"] = None
        __props__.__dict__["connections"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["express_route_connection"] = None
        __props__.__dict__["gateway_manager_etag"] = None
        __props__.__dict__["ipv6_peering_config"] = None
        __props__.__dict__["last_modified_by"] = None
        __props__.__dict__["microsoft_peering_config"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["peer_asn"] = None
        __props__.__dict__["peered_connections"] = None
        __props__.__dict__["peering_type"] = None
        __props__.__dict__["primary_azure_port"] = None
        __props__.__dict__["primary_peer_address_prefix"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["route_filter"] = None
        __props__.__dict__["secondary_azure_port"] = None
        __props__.__dict__["secondary_peer_address_prefix"] = None
        __props__.__dict__["shared_key"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["stats"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vlan_id"] = None
        return ExpressRouteCircuitPeering(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="azureASN")
    def azure_asn(self) -> pulumi.Output[Optional[int]]:
        """
        The Azure ASN.
        """
        return pulumi.get(self, "azure_asn")

    @property
    @pulumi.getter
    def connections(self) -> pulumi.Output[Optional[Sequence['outputs.ExpressRouteCircuitConnectionResponse']]]:
        """
        The list of circuit connections associated with Azure Private Peering for this circuit.
        """
        return pulumi.get(self, "connections")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="expressRouteConnection")
    def express_route_connection(self) -> pulumi.Output[Optional['outputs.ExpressRouteConnectionIdResponse']]:
        """
        The ExpressRoute connection.
        """
        return pulumi.get(self, "express_route_connection")

    @property
    @pulumi.getter(name="gatewayManagerEtag")
    def gateway_manager_etag(self) -> pulumi.Output[Optional[str]]:
        """
        The GatewayManager Etag.
        """
        return pulumi.get(self, "gateway_manager_etag")

    @property
    @pulumi.getter(name="ipv6PeeringConfig")
    def ipv6_peering_config(self) -> pulumi.Output[Optional['outputs.Ipv6ExpressRouteCircuitPeeringConfigResponse']]:
        """
        The IPv6 peering configuration.
        """
        return pulumi.get(self, "ipv6_peering_config")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> pulumi.Output[str]:
        """
        Who was the last to modify the peering.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="microsoftPeeringConfig")
    def microsoft_peering_config(self) -> pulumi.Output[Optional['outputs.ExpressRouteCircuitPeeringConfigResponse']]:
        """
        The Microsoft peering configuration.
        """
        return pulumi.get(self, "microsoft_peering_config")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peerASN")
    def peer_asn(self) -> pulumi.Output[Optional[float]]:
        """
        The peer ASN.
        """
        return pulumi.get(self, "peer_asn")

    @property
    @pulumi.getter(name="peeredConnections")
    def peered_connections(self) -> pulumi.Output[Sequence['outputs.PeerExpressRouteCircuitConnectionResponse']]:
        """
        The list of peered circuit connections associated with Azure Private Peering for this circuit.
        """
        return pulumi.get(self, "peered_connections")

    @property
    @pulumi.getter(name="peeringType")
    def peering_type(self) -> pulumi.Output[Optional[str]]:
        """
        The peering type.
        """
        return pulumi.get(self, "peering_type")

    @property
    @pulumi.getter(name="primaryAzurePort")
    def primary_azure_port(self) -> pulumi.Output[Optional[str]]:
        """
        The primary port.
        """
        return pulumi.get(self, "primary_azure_port")

    @property
    @pulumi.getter(name="primaryPeerAddressPrefix")
    def primary_peer_address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The primary address prefix.
        """
        return pulumi.get(self, "primary_peer_address_prefix")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the express route circuit peering resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="routeFilter")
    def route_filter(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The reference to the RouteFilter resource.
        """
        return pulumi.get(self, "route_filter")

    @property
    @pulumi.getter(name="secondaryAzurePort")
    def secondary_azure_port(self) -> pulumi.Output[Optional[str]]:
        """
        The secondary port.
        """
        return pulumi.get(self, "secondary_azure_port")

    @property
    @pulumi.getter(name="secondaryPeerAddressPrefix")
    def secondary_peer_address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The secondary address prefix.
        """
        return pulumi.get(self, "secondary_peer_address_prefix")

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> pulumi.Output[Optional[str]]:
        """
        The shared key.
        """
        return pulumi.get(self, "shared_key")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[Optional[str]]:
        """
        The peering state.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def stats(self) -> pulumi.Output[Optional['outputs.ExpressRouteCircuitStatsResponse']]:
        """
        The peering stats of express route circuit.
        """
        return pulumi.get(self, "stats")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vlanId")
    def vlan_id(self) -> pulumi.Output[Optional[int]]:
        """
        The VLAN ID.
        """
        return pulumi.get(self, "vlan_id")

