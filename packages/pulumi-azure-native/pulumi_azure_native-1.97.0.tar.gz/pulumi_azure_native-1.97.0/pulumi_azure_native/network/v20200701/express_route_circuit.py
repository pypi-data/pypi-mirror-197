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
from ._enums import *
from ._inputs import *

__all__ = ['ExpressRouteCircuitArgs', 'ExpressRouteCircuit']

@pulumi.input_type
class ExpressRouteCircuitArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 allow_classic_operations: Optional[pulumi.Input[bool]] = None,
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitAuthorizationArgs']]]] = None,
                 bandwidth_in_gbps: Optional[pulumi.Input[float]] = None,
                 circuit_name: Optional[pulumi.Input[str]] = None,
                 circuit_provisioning_state: Optional[pulumi.Input[str]] = None,
                 express_route_port: Optional[pulumi.Input['SubResourceArgs']] = None,
                 gateway_manager_etag: Optional[pulumi.Input[str]] = None,
                 global_reach_enabled: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peerings: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitPeeringArgs']]]] = None,
                 service_key: Optional[pulumi.Input[str]] = None,
                 service_provider_notes: Optional[pulumi.Input[str]] = None,
                 service_provider_properties: Optional[pulumi.Input['ExpressRouteCircuitServiceProviderPropertiesArgs']] = None,
                 service_provider_provisioning_state: Optional[pulumi.Input[Union[str, 'ServiceProviderProvisioningState']]] = None,
                 sku: Optional[pulumi.Input['ExpressRouteCircuitSkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ExpressRouteCircuit resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[bool] allow_classic_operations: Allow classic operations.
        :param pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitAuthorizationArgs']]] authorizations: The list of authorizations.
        :param pulumi.Input[float] bandwidth_in_gbps: The bandwidth of the circuit when the circuit is provisioned on an ExpressRoutePort resource.
        :param pulumi.Input[str] circuit_name: The name of the circuit.
        :param pulumi.Input[str] circuit_provisioning_state: The CircuitProvisioningState state of the resource.
        :param pulumi.Input['SubResourceArgs'] express_route_port: The reference to the ExpressRoutePort resource when the circuit is provisioned on an ExpressRoutePort resource.
        :param pulumi.Input[str] gateway_manager_etag: The GatewayManager Etag.
        :param pulumi.Input[bool] global_reach_enabled: Flag denoting global reach status.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitPeeringArgs']]] peerings: The list of peerings.
        :param pulumi.Input[str] service_key: The ServiceKey.
        :param pulumi.Input[str] service_provider_notes: The ServiceProviderNotes.
        :param pulumi.Input['ExpressRouteCircuitServiceProviderPropertiesArgs'] service_provider_properties: The ServiceProviderProperties.
        :param pulumi.Input[Union[str, 'ServiceProviderProvisioningState']] service_provider_provisioning_state: The ServiceProviderProvisioningState state of the resource.
        :param pulumi.Input['ExpressRouteCircuitSkuArgs'] sku: The SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if allow_classic_operations is not None:
            pulumi.set(__self__, "allow_classic_operations", allow_classic_operations)
        if authorizations is not None:
            pulumi.set(__self__, "authorizations", authorizations)
        if bandwidth_in_gbps is not None:
            pulumi.set(__self__, "bandwidth_in_gbps", bandwidth_in_gbps)
        if circuit_name is not None:
            pulumi.set(__self__, "circuit_name", circuit_name)
        if circuit_provisioning_state is not None:
            pulumi.set(__self__, "circuit_provisioning_state", circuit_provisioning_state)
        if express_route_port is not None:
            pulumi.set(__self__, "express_route_port", express_route_port)
        if gateway_manager_etag is not None:
            pulumi.set(__self__, "gateway_manager_etag", gateway_manager_etag)
        if global_reach_enabled is not None:
            pulumi.set(__self__, "global_reach_enabled", global_reach_enabled)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if peerings is not None:
            pulumi.set(__self__, "peerings", peerings)
        if service_key is not None:
            pulumi.set(__self__, "service_key", service_key)
        if service_provider_notes is not None:
            pulumi.set(__self__, "service_provider_notes", service_provider_notes)
        if service_provider_properties is not None:
            pulumi.set(__self__, "service_provider_properties", service_provider_properties)
        if service_provider_provisioning_state is not None:
            pulumi.set(__self__, "service_provider_provisioning_state", service_provider_provisioning_state)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter(name="allowClassicOperations")
    def allow_classic_operations(self) -> Optional[pulumi.Input[bool]]:
        """
        Allow classic operations.
        """
        return pulumi.get(self, "allow_classic_operations")

    @allow_classic_operations.setter
    def allow_classic_operations(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_classic_operations", value)

    @property
    @pulumi.getter
    def authorizations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitAuthorizationArgs']]]]:
        """
        The list of authorizations.
        """
        return pulumi.get(self, "authorizations")

    @authorizations.setter
    def authorizations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitAuthorizationArgs']]]]):
        pulumi.set(self, "authorizations", value)

    @property
    @pulumi.getter(name="bandwidthInGbps")
    def bandwidth_in_gbps(self) -> Optional[pulumi.Input[float]]:
        """
        The bandwidth of the circuit when the circuit is provisioned on an ExpressRoutePort resource.
        """
        return pulumi.get(self, "bandwidth_in_gbps")

    @bandwidth_in_gbps.setter
    def bandwidth_in_gbps(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "bandwidth_in_gbps", value)

    @property
    @pulumi.getter(name="circuitName")
    def circuit_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the circuit.
        """
        return pulumi.get(self, "circuit_name")

    @circuit_name.setter
    def circuit_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "circuit_name", value)

    @property
    @pulumi.getter(name="circuitProvisioningState")
    def circuit_provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        The CircuitProvisioningState state of the resource.
        """
        return pulumi.get(self, "circuit_provisioning_state")

    @circuit_provisioning_state.setter
    def circuit_provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "circuit_provisioning_state", value)

    @property
    @pulumi.getter(name="expressRoutePort")
    def express_route_port(self) -> Optional[pulumi.Input['SubResourceArgs']]:
        """
        The reference to the ExpressRoutePort resource when the circuit is provisioned on an ExpressRoutePort resource.
        """
        return pulumi.get(self, "express_route_port")

    @express_route_port.setter
    def express_route_port(self, value: Optional[pulumi.Input['SubResourceArgs']]):
        pulumi.set(self, "express_route_port", value)

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
    @pulumi.getter(name="globalReachEnabled")
    def global_reach_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag denoting global reach status.
        """
        return pulumi.get(self, "global_reach_enabled")

    @global_reach_enabled.setter
    def global_reach_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "global_reach_enabled", value)

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
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def peerings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitPeeringArgs']]]]:
        """
        The list of peerings.
        """
        return pulumi.get(self, "peerings")

    @peerings.setter
    def peerings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExpressRouteCircuitPeeringArgs']]]]):
        pulumi.set(self, "peerings", value)

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> Optional[pulumi.Input[str]]:
        """
        The ServiceKey.
        """
        return pulumi.get(self, "service_key")

    @service_key.setter
    def service_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_key", value)

    @property
    @pulumi.getter(name="serviceProviderNotes")
    def service_provider_notes(self) -> Optional[pulumi.Input[str]]:
        """
        The ServiceProviderNotes.
        """
        return pulumi.get(self, "service_provider_notes")

    @service_provider_notes.setter
    def service_provider_notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_provider_notes", value)

    @property
    @pulumi.getter(name="serviceProviderProperties")
    def service_provider_properties(self) -> Optional[pulumi.Input['ExpressRouteCircuitServiceProviderPropertiesArgs']]:
        """
        The ServiceProviderProperties.
        """
        return pulumi.get(self, "service_provider_properties")

    @service_provider_properties.setter
    def service_provider_properties(self, value: Optional[pulumi.Input['ExpressRouteCircuitServiceProviderPropertiesArgs']]):
        pulumi.set(self, "service_provider_properties", value)

    @property
    @pulumi.getter(name="serviceProviderProvisioningState")
    def service_provider_provisioning_state(self) -> Optional[pulumi.Input[Union[str, 'ServiceProviderProvisioningState']]]:
        """
        The ServiceProviderProvisioningState state of the resource.
        """
        return pulumi.get(self, "service_provider_provisioning_state")

    @service_provider_provisioning_state.setter
    def service_provider_provisioning_state(self, value: Optional[pulumi.Input[Union[str, 'ServiceProviderProvisioningState']]]):
        pulumi.set(self, "service_provider_provisioning_state", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['ExpressRouteCircuitSkuArgs']]:
        """
        The SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ExpressRouteCircuitSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ExpressRouteCircuit(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_classic_operations: Optional[pulumi.Input[bool]] = None,
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitAuthorizationArgs']]]]] = None,
                 bandwidth_in_gbps: Optional[pulumi.Input[float]] = None,
                 circuit_name: Optional[pulumi.Input[str]] = None,
                 circuit_provisioning_state: Optional[pulumi.Input[str]] = None,
                 express_route_port: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 gateway_manager_etag: Optional[pulumi.Input[str]] = None,
                 global_reach_enabled: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peerings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitPeeringArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_key: Optional[pulumi.Input[str]] = None,
                 service_provider_notes: Optional[pulumi.Input[str]] = None,
                 service_provider_properties: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitServiceProviderPropertiesArgs']]] = None,
                 service_provider_provisioning_state: Optional[pulumi.Input[Union[str, 'ServiceProviderProvisioningState']]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ExpressRouteCircuit resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_classic_operations: Allow classic operations.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitAuthorizationArgs']]]] authorizations: The list of authorizations.
        :param pulumi.Input[float] bandwidth_in_gbps: The bandwidth of the circuit when the circuit is provisioned on an ExpressRoutePort resource.
        :param pulumi.Input[str] circuit_name: The name of the circuit.
        :param pulumi.Input[str] circuit_provisioning_state: The CircuitProvisioningState state of the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] express_route_port: The reference to the ExpressRoutePort resource when the circuit is provisioned on an ExpressRoutePort resource.
        :param pulumi.Input[str] gateway_manager_etag: The GatewayManager Etag.
        :param pulumi.Input[bool] global_reach_enabled: Flag denoting global reach status.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitPeeringArgs']]]] peerings: The list of peerings.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_key: The ServiceKey.
        :param pulumi.Input[str] service_provider_notes: The ServiceProviderNotes.
        :param pulumi.Input[pulumi.InputType['ExpressRouteCircuitServiceProviderPropertiesArgs']] service_provider_properties: The ServiceProviderProperties.
        :param pulumi.Input[Union[str, 'ServiceProviderProvisioningState']] service_provider_provisioning_state: The ServiceProviderProvisioningState state of the resource.
        :param pulumi.Input[pulumi.InputType['ExpressRouteCircuitSkuArgs']] sku: The SKU.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ExpressRouteCircuitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ExpressRouteCircuit resource.

        :param str resource_name: The name of the resource.
        :param ExpressRouteCircuitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ExpressRouteCircuitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_classic_operations: Optional[pulumi.Input[bool]] = None,
                 authorizations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitAuthorizationArgs']]]]] = None,
                 bandwidth_in_gbps: Optional[pulumi.Input[float]] = None,
                 circuit_name: Optional[pulumi.Input[str]] = None,
                 circuit_provisioning_state: Optional[pulumi.Input[str]] = None,
                 express_route_port: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 gateway_manager_etag: Optional[pulumi.Input[str]] = None,
                 global_reach_enabled: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 peerings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ExpressRouteCircuitPeeringArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_key: Optional[pulumi.Input[str]] = None,
                 service_provider_notes: Optional[pulumi.Input[str]] = None,
                 service_provider_properties: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitServiceProviderPropertiesArgs']]] = None,
                 service_provider_provisioning_state: Optional[pulumi.Input[Union[str, 'ServiceProviderProvisioningState']]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ExpressRouteCircuitSkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ExpressRouteCircuitArgs.__new__(ExpressRouteCircuitArgs)

            __props__.__dict__["allow_classic_operations"] = allow_classic_operations
            __props__.__dict__["authorizations"] = authorizations
            __props__.__dict__["bandwidth_in_gbps"] = bandwidth_in_gbps
            __props__.__dict__["circuit_name"] = circuit_name
            __props__.__dict__["circuit_provisioning_state"] = circuit_provisioning_state
            __props__.__dict__["express_route_port"] = express_route_port
            __props__.__dict__["gateway_manager_etag"] = gateway_manager_etag
            __props__.__dict__["global_reach_enabled"] = global_reach_enabled
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            __props__.__dict__["peerings"] = peerings
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["service_key"] = service_key
            __props__.__dict__["service_provider_notes"] = service_provider_notes
            __props__.__dict__["service_provider_properties"] = service_provider_properties
            __props__.__dict__["service_provider_provisioning_state"] = service_provider_provisioning_state
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["stag"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20150501preview:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20150615:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20160330:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20160601:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20160901:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20161201:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20170301:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20170601:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20170801:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20170901:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20171001:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20171101:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20180101:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20180201:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20180401:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20180601:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20180701:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20180801:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20181001:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20181101:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20181201:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20190201:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20190401:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20190601:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20190701:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20190801:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20190901:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20191101:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20191201:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20200301:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20200401:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20200501:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20200601:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20200801:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20201101:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20210201:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20210301:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20210501:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20210801:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20220101:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20220501:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20220701:ExpressRouteCircuit"), pulumi.Alias(type_="azure-native:network/v20220901:ExpressRouteCircuit")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ExpressRouteCircuit, __self__).__init__(
            'azure-native:network/v20200701:ExpressRouteCircuit',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ExpressRouteCircuit':
        """
        Get an existing ExpressRouteCircuit resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ExpressRouteCircuitArgs.__new__(ExpressRouteCircuitArgs)

        __props__.__dict__["allow_classic_operations"] = None
        __props__.__dict__["authorizations"] = None
        __props__.__dict__["bandwidth_in_gbps"] = None
        __props__.__dict__["circuit_provisioning_state"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["express_route_port"] = None
        __props__.__dict__["gateway_manager_etag"] = None
        __props__.__dict__["global_reach_enabled"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["peerings"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["service_key"] = None
        __props__.__dict__["service_provider_notes"] = None
        __props__.__dict__["service_provider_properties"] = None
        __props__.__dict__["service_provider_provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["stag"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ExpressRouteCircuit(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowClassicOperations")
    def allow_classic_operations(self) -> pulumi.Output[Optional[bool]]:
        """
        Allow classic operations.
        """
        return pulumi.get(self, "allow_classic_operations")

    @property
    @pulumi.getter
    def authorizations(self) -> pulumi.Output[Optional[Sequence['outputs.ExpressRouteCircuitAuthorizationResponse']]]:
        """
        The list of authorizations.
        """
        return pulumi.get(self, "authorizations")

    @property
    @pulumi.getter(name="bandwidthInGbps")
    def bandwidth_in_gbps(self) -> pulumi.Output[Optional[float]]:
        """
        The bandwidth of the circuit when the circuit is provisioned on an ExpressRoutePort resource.
        """
        return pulumi.get(self, "bandwidth_in_gbps")

    @property
    @pulumi.getter(name="circuitProvisioningState")
    def circuit_provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The CircuitProvisioningState state of the resource.
        """
        return pulumi.get(self, "circuit_provisioning_state")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="expressRoutePort")
    def express_route_port(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The reference to the ExpressRoutePort resource when the circuit is provisioned on an ExpressRoutePort resource.
        """
        return pulumi.get(self, "express_route_port")

    @property
    @pulumi.getter(name="gatewayManagerEtag")
    def gateway_manager_etag(self) -> pulumi.Output[Optional[str]]:
        """
        The GatewayManager Etag.
        """
        return pulumi.get(self, "gateway_manager_etag")

    @property
    @pulumi.getter(name="globalReachEnabled")
    def global_reach_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Flag denoting global reach status.
        """
        return pulumi.get(self, "global_reach_enabled")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def peerings(self) -> pulumi.Output[Optional[Sequence['outputs.ExpressRouteCircuitPeeringResponse']]]:
        """
        The list of peerings.
        """
        return pulumi.get(self, "peerings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the express route circuit resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> pulumi.Output[Optional[str]]:
        """
        The ServiceKey.
        """
        return pulumi.get(self, "service_key")

    @property
    @pulumi.getter(name="serviceProviderNotes")
    def service_provider_notes(self) -> pulumi.Output[Optional[str]]:
        """
        The ServiceProviderNotes.
        """
        return pulumi.get(self, "service_provider_notes")

    @property
    @pulumi.getter(name="serviceProviderProperties")
    def service_provider_properties(self) -> pulumi.Output[Optional['outputs.ExpressRouteCircuitServiceProviderPropertiesResponse']]:
        """
        The ServiceProviderProperties.
        """
        return pulumi.get(self, "service_provider_properties")

    @property
    @pulumi.getter(name="serviceProviderProvisioningState")
    def service_provider_provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The ServiceProviderProvisioningState state of the resource.
        """
        return pulumi.get(self, "service_provider_provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ExpressRouteCircuitSkuResponse']]:
        """
        The SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def stag(self) -> pulumi.Output[int]:
        """
        The identifier of the circuit traffic. Outer tag for QinQ encapsulation.
        """
        return pulumi.get(self, "stag")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

