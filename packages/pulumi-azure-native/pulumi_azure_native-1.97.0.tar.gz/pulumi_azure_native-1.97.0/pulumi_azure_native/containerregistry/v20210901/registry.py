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

__all__ = ['RegistryArgs', 'Registry']

@pulumi.input_type
class RegistryArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sku: pulumi.Input['SkuArgs'],
                 admin_user_enabled: Optional[pulumi.Input[bool]] = None,
                 data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 encryption: Optional[pulumi.Input['EncryptionPropertyArgs']] = None,
                 identity: Optional[pulumi.Input['IdentityPropertiesArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_rule_bypass_options: Optional[pulumi.Input[Union[str, 'NetworkRuleBypassOptions']]] = None,
                 network_rule_set: Optional[pulumi.Input['NetworkRuleSetArgs']] = None,
                 policies: Optional[pulumi.Input['PoliciesArgs']] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundancy: Optional[pulumi.Input[Union[str, 'ZoneRedundancy']]] = None):
        """
        The set of arguments for constructing a Registry resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input['SkuArgs'] sku: The SKU of the container registry.
        :param pulumi.Input[bool] admin_user_enabled: The value that indicates whether the admin user is enabled.
        :param pulumi.Input[bool] data_endpoint_enabled: Enable a single data endpoint per region for serving data.
        :param pulumi.Input['EncryptionPropertyArgs'] encryption: The encryption settings of container registry.
        :param pulumi.Input['IdentityPropertiesArgs'] identity: The identity of the container registry.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[Union[str, 'NetworkRuleBypassOptions']] network_rule_bypass_options: Whether to allow trusted Azure services to access a network restricted registry.
        :param pulumi.Input['NetworkRuleSetArgs'] network_rule_set: The network rule set for a container registry.
        :param pulumi.Input['PoliciesArgs'] policies: The policies for a container registry.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public network access is allowed for the container registry.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[Union[str, 'ZoneRedundancy']] zone_redundancy: Whether or not zone redundancy is enabled for this container registry
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku", sku)
        if admin_user_enabled is None:
            admin_user_enabled = False
        if admin_user_enabled is not None:
            pulumi.set(__self__, "admin_user_enabled", admin_user_enabled)
        if data_endpoint_enabled is not None:
            pulumi.set(__self__, "data_endpoint_enabled", data_endpoint_enabled)
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_rule_bypass_options is None:
            network_rule_bypass_options = 'AzureServices'
        if network_rule_bypass_options is not None:
            pulumi.set(__self__, "network_rule_bypass_options", network_rule_bypass_options)
        if network_rule_set is not None:
            pulumi.set(__self__, "network_rule_set", network_rule_set)
        if policies is not None:
            pulumi.set(__self__, "policies", policies)
        if public_network_access is None:
            public_network_access = 'Enabled'
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)
        if registry_name is not None:
            pulumi.set(__self__, "registry_name", registry_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if zone_redundancy is None:
            zone_redundancy = 'Disabled'
        if zone_redundancy is not None:
            pulumi.set(__self__, "zone_redundancy", zone_redundancy)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group to which the container registry belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        The SKU of the container registry.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="adminUserEnabled")
    def admin_user_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        The value that indicates whether the admin user is enabled.
        """
        return pulumi.get(self, "admin_user_enabled")

    @admin_user_enabled.setter
    def admin_user_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "admin_user_enabled", value)

    @property
    @pulumi.getter(name="dataEndpointEnabled")
    def data_endpoint_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable a single data endpoint per region for serving data.
        """
        return pulumi.get(self, "data_endpoint_enabled")

    @data_endpoint_enabled.setter
    def data_endpoint_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "data_endpoint_enabled", value)

    @property
    @pulumi.getter
    def encryption(self) -> Optional[pulumi.Input['EncryptionPropertyArgs']]:
        """
        The encryption settings of container registry.
        """
        return pulumi.get(self, "encryption")

    @encryption.setter
    def encryption(self, value: Optional[pulumi.Input['EncryptionPropertyArgs']]):
        pulumi.set(self, "encryption", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['IdentityPropertiesArgs']]:
        """
        The identity of the container registry.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['IdentityPropertiesArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkRuleBypassOptions")
    def network_rule_bypass_options(self) -> Optional[pulumi.Input[Union[str, 'NetworkRuleBypassOptions']]]:
        """
        Whether to allow trusted Azure services to access a network restricted registry.
        """
        return pulumi.get(self, "network_rule_bypass_options")

    @network_rule_bypass_options.setter
    def network_rule_bypass_options(self, value: Optional[pulumi.Input[Union[str, 'NetworkRuleBypassOptions']]]):
        pulumi.set(self, "network_rule_bypass_options", value)

    @property
    @pulumi.getter(name="networkRuleSet")
    def network_rule_set(self) -> Optional[pulumi.Input['NetworkRuleSetArgs']]:
        """
        The network rule set for a container registry.
        """
        return pulumi.get(self, "network_rule_set")

    @network_rule_set.setter
    def network_rule_set(self, value: Optional[pulumi.Input['NetworkRuleSetArgs']]):
        pulumi.set(self, "network_rule_set", value)

    @property
    @pulumi.getter
    def policies(self) -> Optional[pulumi.Input['PoliciesArgs']]:
        """
        The policies for a container registry.
        """
        return pulumi.get(self, "policies")

    @policies.setter
    def policies(self, value: Optional[pulumi.Input['PoliciesArgs']]):
        pulumi.set(self, "policies", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]:
        """
        Whether or not public network access is allowed for the container registry.
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]):
        pulumi.set(self, "public_network_access", value)

    @property
    @pulumi.getter(name="registryName")
    def registry_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container registry.
        """
        return pulumi.get(self, "registry_name")

    @registry_name.setter
    def registry_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "registry_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="zoneRedundancy")
    def zone_redundancy(self) -> Optional[pulumi.Input[Union[str, 'ZoneRedundancy']]]:
        """
        Whether or not zone redundancy is enabled for this container registry
        """
        return pulumi.get(self, "zone_redundancy")

    @zone_redundancy.setter
    def zone_redundancy(self, value: Optional[pulumi.Input[Union[str, 'ZoneRedundancy']]]):
        pulumi.set(self, "zone_redundancy", value)


class Registry(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_user_enabled: Optional[pulumi.Input[bool]] = None,
                 data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['EncryptionPropertyArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_rule_bypass_options: Optional[pulumi.Input[Union[str, 'NetworkRuleBypassOptions']]] = None,
                 network_rule_set: Optional[pulumi.Input[pulumi.InputType['NetworkRuleSetArgs']]] = None,
                 policies: Optional[pulumi.Input[pulumi.InputType['PoliciesArgs']]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundancy: Optional[pulumi.Input[Union[str, 'ZoneRedundancy']]] = None,
                 __props__=None):
        """
        An object that represents a container registry.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] admin_user_enabled: The value that indicates whether the admin user is enabled.
        :param pulumi.Input[bool] data_endpoint_enabled: Enable a single data endpoint per region for serving data.
        :param pulumi.Input[pulumi.InputType['EncryptionPropertyArgs']] encryption: The encryption settings of container registry.
        :param pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']] identity: The identity of the container registry.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[Union[str, 'NetworkRuleBypassOptions']] network_rule_bypass_options: Whether to allow trusted Azure services to access a network restricted registry.
        :param pulumi.Input[pulumi.InputType['NetworkRuleSetArgs']] network_rule_set: The network rule set for a container registry.
        :param pulumi.Input[pulumi.InputType['PoliciesArgs']] policies: The policies for a container registry.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public network access is allowed for the container registry.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The SKU of the container registry.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[Union[str, 'ZoneRedundancy']] zone_redundancy: Whether or not zone redundancy is enabled for this container registry
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegistryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An object that represents a container registry.

        :param str resource_name: The name of the resource.
        :param RegistryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegistryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_user_enabled: Optional[pulumi.Input[bool]] = None,
                 data_endpoint_enabled: Optional[pulumi.Input[bool]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['EncryptionPropertyArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityPropertiesArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_rule_bypass_options: Optional[pulumi.Input[Union[str, 'NetworkRuleBypassOptions']]] = None,
                 network_rule_set: Optional[pulumi.Input[pulumi.InputType['NetworkRuleSetArgs']]] = None,
                 policies: Optional[pulumi.Input[pulumi.InputType['PoliciesArgs']]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundancy: Optional[pulumi.Input[Union[str, 'ZoneRedundancy']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RegistryArgs.__new__(RegistryArgs)

            if admin_user_enabled is None:
                admin_user_enabled = False
            __props__.__dict__["admin_user_enabled"] = admin_user_enabled
            __props__.__dict__["data_endpoint_enabled"] = data_endpoint_enabled
            __props__.__dict__["encryption"] = encryption
            __props__.__dict__["identity"] = identity
            __props__.__dict__["location"] = location
            if network_rule_bypass_options is None:
                network_rule_bypass_options = 'AzureServices'
            __props__.__dict__["network_rule_bypass_options"] = network_rule_bypass_options
            __props__.__dict__["network_rule_set"] = network_rule_set
            __props__.__dict__["policies"] = policies
            if public_network_access is None:
                public_network_access = 'Enabled'
            __props__.__dict__["public_network_access"] = public_network_access
            __props__.__dict__["registry_name"] = registry_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            if zone_redundancy is None:
                zone_redundancy = 'Disabled'
            __props__.__dict__["zone_redundancy"] = zone_redundancy
            __props__.__dict__["creation_date"] = None
            __props__.__dict__["data_endpoint_host_names"] = None
            __props__.__dict__["login_server"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerregistry:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20160627preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20170301:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20170601preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20171001:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20190501:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20191201preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20201101preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20210601preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20210801preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20211201preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20220201preview:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20221201:Registry"), pulumi.Alias(type_="azure-native:containerregistry/v20230101preview:Registry")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Registry, __self__).__init__(
            'azure-native:containerregistry/v20210901:Registry',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Registry':
        """
        Get an existing Registry resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RegistryArgs.__new__(RegistryArgs)

        __props__.__dict__["admin_user_enabled"] = None
        __props__.__dict__["creation_date"] = None
        __props__.__dict__["data_endpoint_enabled"] = None
        __props__.__dict__["data_endpoint_host_names"] = None
        __props__.__dict__["encryption"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["login_server"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_rule_bypass_options"] = None
        __props__.__dict__["network_rule_set"] = None
        __props__.__dict__["policies"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_network_access"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["zone_redundancy"] = None
        return Registry(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="adminUserEnabled")
    def admin_user_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        The value that indicates whether the admin user is enabled.
        """
        return pulumi.get(self, "admin_user_enabled")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of the container registry in ISO8601 format.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="dataEndpointEnabled")
    def data_endpoint_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable a single data endpoint per region for serving data.
        """
        return pulumi.get(self, "data_endpoint_enabled")

    @property
    @pulumi.getter(name="dataEndpointHostNames")
    def data_endpoint_host_names(self) -> pulumi.Output[Sequence[str]]:
        """
        List of host names that will serve data when dataEndpointEnabled is true.
        """
        return pulumi.get(self, "data_endpoint_host_names")

    @property
    @pulumi.getter
    def encryption(self) -> pulumi.Output[Optional['outputs.EncryptionPropertyResponse']]:
        """
        The encryption settings of container registry.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityPropertiesResponse']]:
        """
        The identity of the container registry.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="loginServer")
    def login_server(self) -> pulumi.Output[str]:
        """
        The URL that can be used to log into the container registry.
        """
        return pulumi.get(self, "login_server")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkRuleBypassOptions")
    def network_rule_bypass_options(self) -> pulumi.Output[Optional[str]]:
        """
        Whether to allow trusted Azure services to access a network restricted registry.
        """
        return pulumi.get(self, "network_rule_bypass_options")

    @property
    @pulumi.getter(name="networkRuleSet")
    def network_rule_set(self) -> pulumi.Output[Optional['outputs.NetworkRuleSetResponse']]:
        """
        The network rule set for a container registry.
        """
        return pulumi.get(self, "network_rule_set")

    @property
    @pulumi.getter
    def policies(self) -> pulumi.Output[Optional['outputs.PoliciesResponse']]:
        """
        The policies for a container registry.
        """
        return pulumi.get(self, "policies")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        List of private endpoint connections for a container registry.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the container registry at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not public network access is allowed for the container registry.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        The SKU of the container registry.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.StatusResponse']:
        """
        The status of the container registry at the time the operation was called.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneRedundancy")
    def zone_redundancy(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not zone redundancy is enabled for this container registry
        """
        return pulumi.get(self, "zone_redundancy")

