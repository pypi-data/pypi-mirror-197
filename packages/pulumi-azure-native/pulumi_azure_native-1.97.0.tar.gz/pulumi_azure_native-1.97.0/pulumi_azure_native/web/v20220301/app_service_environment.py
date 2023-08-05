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

__all__ = ['AppServiceEnvironmentArgs', 'AppServiceEnvironment']

@pulumi.input_type
class AppServiceEnvironmentArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 virtual_network: pulumi.Input['VirtualNetworkProfileArgs'],
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input['NameValuePairArgs']]]] = None,
                 custom_dns_suffix_configuration: Optional[pulumi.Input['CustomDnsSuffixConfigurationArgs']] = None,
                 dedicated_host_count: Optional[pulumi.Input[int]] = None,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 front_end_scale_factor: Optional[pulumi.Input[int]] = None,
                 internal_load_balancing_mode: Optional[pulumi.Input[Union[str, 'LoadBalancingMode']]] = None,
                 ipssl_address_count: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 multi_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networking_configuration: Optional[pulumi.Input['AseV3NetworkingConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 upgrade_preference: Optional[pulumi.Input[Union[str, 'UpgradePreference']]] = None,
                 user_whitelisted_ip_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a AppServiceEnvironment resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input['VirtualNetworkProfileArgs'] virtual_network: Description of the Virtual Network.
        :param pulumi.Input[Sequence[pulumi.Input['NameValuePairArgs']]] cluster_settings: Custom settings for changing the behavior of the App Service Environment.
        :param pulumi.Input['CustomDnsSuffixConfigurationArgs'] custom_dns_suffix_configuration: Full view of the custom domain suffix configuration for ASEv3.
        :param pulumi.Input[int] dedicated_host_count: Dedicated Host Count
        :param pulumi.Input[str] dns_suffix: DNS suffix of the App Service Environment.
        :param pulumi.Input[int] front_end_scale_factor: Scale factor for front-ends.
        :param pulumi.Input[Union[str, 'LoadBalancingMode']] internal_load_balancing_mode: Specifies which endpoints to serve internally in the Virtual Network for the App Service Environment.
        :param pulumi.Input[int] ipssl_address_count: Number of IP SSL addresses reserved for the App Service Environment.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] multi_size: Front-end VM size, e.g. "Medium", "Large".
        :param pulumi.Input[str] name: Name of the App Service Environment.
        :param pulumi.Input['AseV3NetworkingConfigurationArgs'] networking_configuration: Full view of networking configuration for an ASE.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'UpgradePreference']] upgrade_preference: Upgrade Preference
        :param pulumi.Input[Sequence[pulumi.Input[str]]] user_whitelisted_ip_ranges: User added list of IP Ranges allowed on ASE db
        :param pulumi.Input[bool] zone_redundant: Whether or not this App Service Environment is zone-redundant.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_network", virtual_network)
        if cluster_settings is not None:
            pulumi.set(__self__, "cluster_settings", cluster_settings)
        if custom_dns_suffix_configuration is not None:
            pulumi.set(__self__, "custom_dns_suffix_configuration", custom_dns_suffix_configuration)
        if dedicated_host_count is not None:
            pulumi.set(__self__, "dedicated_host_count", dedicated_host_count)
        if dns_suffix is not None:
            pulumi.set(__self__, "dns_suffix", dns_suffix)
        if front_end_scale_factor is not None:
            pulumi.set(__self__, "front_end_scale_factor", front_end_scale_factor)
        if internal_load_balancing_mode is not None:
            pulumi.set(__self__, "internal_load_balancing_mode", internal_load_balancing_mode)
        if ipssl_address_count is not None:
            pulumi.set(__self__, "ipssl_address_count", ipssl_address_count)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if multi_size is not None:
            pulumi.set(__self__, "multi_size", multi_size)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if networking_configuration is not None:
            pulumi.set(__self__, "networking_configuration", networking_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if upgrade_preference is None:
            upgrade_preference = 'None'
        if upgrade_preference is not None:
            pulumi.set(__self__, "upgrade_preference", upgrade_preference)
        if user_whitelisted_ip_ranges is not None:
            pulumi.set(__self__, "user_whitelisted_ip_ranges", user_whitelisted_ip_ranges)
        if zone_redundant is not None:
            pulumi.set(__self__, "zone_redundant", zone_redundant)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="virtualNetwork")
    def virtual_network(self) -> pulumi.Input['VirtualNetworkProfileArgs']:
        """
        Description of the Virtual Network.
        """
        return pulumi.get(self, "virtual_network")

    @virtual_network.setter
    def virtual_network(self, value: pulumi.Input['VirtualNetworkProfileArgs']):
        pulumi.set(self, "virtual_network", value)

    @property
    @pulumi.getter(name="clusterSettings")
    def cluster_settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NameValuePairArgs']]]]:
        """
        Custom settings for changing the behavior of the App Service Environment.
        """
        return pulumi.get(self, "cluster_settings")

    @cluster_settings.setter
    def cluster_settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NameValuePairArgs']]]]):
        pulumi.set(self, "cluster_settings", value)

    @property
    @pulumi.getter(name="customDnsSuffixConfiguration")
    def custom_dns_suffix_configuration(self) -> Optional[pulumi.Input['CustomDnsSuffixConfigurationArgs']]:
        """
        Full view of the custom domain suffix configuration for ASEv3.
        """
        return pulumi.get(self, "custom_dns_suffix_configuration")

    @custom_dns_suffix_configuration.setter
    def custom_dns_suffix_configuration(self, value: Optional[pulumi.Input['CustomDnsSuffixConfigurationArgs']]):
        pulumi.set(self, "custom_dns_suffix_configuration", value)

    @property
    @pulumi.getter(name="dedicatedHostCount")
    def dedicated_host_count(self) -> Optional[pulumi.Input[int]]:
        """
        Dedicated Host Count
        """
        return pulumi.get(self, "dedicated_host_count")

    @dedicated_host_count.setter
    def dedicated_host_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "dedicated_host_count", value)

    @property
    @pulumi.getter(name="dnsSuffix")
    def dns_suffix(self) -> Optional[pulumi.Input[str]]:
        """
        DNS suffix of the App Service Environment.
        """
        return pulumi.get(self, "dns_suffix")

    @dns_suffix.setter
    def dns_suffix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_suffix", value)

    @property
    @pulumi.getter(name="frontEndScaleFactor")
    def front_end_scale_factor(self) -> Optional[pulumi.Input[int]]:
        """
        Scale factor for front-ends.
        """
        return pulumi.get(self, "front_end_scale_factor")

    @front_end_scale_factor.setter
    def front_end_scale_factor(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "front_end_scale_factor", value)

    @property
    @pulumi.getter(name="internalLoadBalancingMode")
    def internal_load_balancing_mode(self) -> Optional[pulumi.Input[Union[str, 'LoadBalancingMode']]]:
        """
        Specifies which endpoints to serve internally in the Virtual Network for the App Service Environment.
        """
        return pulumi.get(self, "internal_load_balancing_mode")

    @internal_load_balancing_mode.setter
    def internal_load_balancing_mode(self, value: Optional[pulumi.Input[Union[str, 'LoadBalancingMode']]]):
        pulumi.set(self, "internal_load_balancing_mode", value)

    @property
    @pulumi.getter(name="ipsslAddressCount")
    def ipssl_address_count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of IP SSL addresses reserved for the App Service Environment.
        """
        return pulumi.get(self, "ipssl_address_count")

    @ipssl_address_count.setter
    def ipssl_address_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ipssl_address_count", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="multiSize")
    def multi_size(self) -> Optional[pulumi.Input[str]]:
        """
        Front-end VM size, e.g. "Medium", "Large".
        """
        return pulumi.get(self, "multi_size")

    @multi_size.setter
    def multi_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "multi_size", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the App Service Environment.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkingConfiguration")
    def networking_configuration(self) -> Optional[pulumi.Input['AseV3NetworkingConfigurationArgs']]:
        """
        Full view of networking configuration for an ASE.
        """
        return pulumi.get(self, "networking_configuration")

    @networking_configuration.setter
    def networking_configuration(self, value: Optional[pulumi.Input['AseV3NetworkingConfigurationArgs']]):
        pulumi.set(self, "networking_configuration", value)

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

    @property
    @pulumi.getter(name="upgradePreference")
    def upgrade_preference(self) -> Optional[pulumi.Input[Union[str, 'UpgradePreference']]]:
        """
        Upgrade Preference
        """
        return pulumi.get(self, "upgrade_preference")

    @upgrade_preference.setter
    def upgrade_preference(self, value: Optional[pulumi.Input[Union[str, 'UpgradePreference']]]):
        pulumi.set(self, "upgrade_preference", value)

    @property
    @pulumi.getter(name="userWhitelistedIpRanges")
    def user_whitelisted_ip_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        User added list of IP Ranges allowed on ASE db
        """
        return pulumi.get(self, "user_whitelisted_ip_ranges")

    @user_whitelisted_ip_ranges.setter
    def user_whitelisted_ip_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "user_whitelisted_ip_ranges", value)

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not this App Service Environment is zone-redundant.
        """
        return pulumi.get(self, "zone_redundant")

    @zone_redundant.setter
    def zone_redundant(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "zone_redundant", value)


class AppServiceEnvironment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NameValuePairArgs']]]]] = None,
                 custom_dns_suffix_configuration: Optional[pulumi.Input[pulumi.InputType['CustomDnsSuffixConfigurationArgs']]] = None,
                 dedicated_host_count: Optional[pulumi.Input[int]] = None,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 front_end_scale_factor: Optional[pulumi.Input[int]] = None,
                 internal_load_balancing_mode: Optional[pulumi.Input[Union[str, 'LoadBalancingMode']]] = None,
                 ipssl_address_count: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 multi_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networking_configuration: Optional[pulumi.Input[pulumi.InputType['AseV3NetworkingConfigurationArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 upgrade_preference: Optional[pulumi.Input[Union[str, 'UpgradePreference']]] = None,
                 user_whitelisted_ip_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 virtual_network: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkProfileArgs']]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        App Service Environment ARM resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NameValuePairArgs']]]] cluster_settings: Custom settings for changing the behavior of the App Service Environment.
        :param pulumi.Input[pulumi.InputType['CustomDnsSuffixConfigurationArgs']] custom_dns_suffix_configuration: Full view of the custom domain suffix configuration for ASEv3.
        :param pulumi.Input[int] dedicated_host_count: Dedicated Host Count
        :param pulumi.Input[str] dns_suffix: DNS suffix of the App Service Environment.
        :param pulumi.Input[int] front_end_scale_factor: Scale factor for front-ends.
        :param pulumi.Input[Union[str, 'LoadBalancingMode']] internal_load_balancing_mode: Specifies which endpoints to serve internally in the Virtual Network for the App Service Environment.
        :param pulumi.Input[int] ipssl_address_count: Number of IP SSL addresses reserved for the App Service Environment.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] multi_size: Front-end VM size, e.g. "Medium", "Large".
        :param pulumi.Input[str] name: Name of the App Service Environment.
        :param pulumi.Input[pulumi.InputType['AseV3NetworkingConfigurationArgs']] networking_configuration: Full view of networking configuration for an ASE.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'UpgradePreference']] upgrade_preference: Upgrade Preference
        :param pulumi.Input[Sequence[pulumi.Input[str]]] user_whitelisted_ip_ranges: User added list of IP Ranges allowed on ASE db
        :param pulumi.Input[pulumi.InputType['VirtualNetworkProfileArgs']] virtual_network: Description of the Virtual Network.
        :param pulumi.Input[bool] zone_redundant: Whether or not this App Service Environment is zone-redundant.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppServiceEnvironmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        App Service Environment ARM resource.

        :param str resource_name: The name of the resource.
        :param AppServiceEnvironmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppServiceEnvironmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_settings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NameValuePairArgs']]]]] = None,
                 custom_dns_suffix_configuration: Optional[pulumi.Input[pulumi.InputType['CustomDnsSuffixConfigurationArgs']]] = None,
                 dedicated_host_count: Optional[pulumi.Input[int]] = None,
                 dns_suffix: Optional[pulumi.Input[str]] = None,
                 front_end_scale_factor: Optional[pulumi.Input[int]] = None,
                 internal_load_balancing_mode: Optional[pulumi.Input[Union[str, 'LoadBalancingMode']]] = None,
                 ipssl_address_count: Optional[pulumi.Input[int]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 multi_size: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 networking_configuration: Optional[pulumi.Input[pulumi.InputType['AseV3NetworkingConfigurationArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 upgrade_preference: Optional[pulumi.Input[Union[str, 'UpgradePreference']]] = None,
                 user_whitelisted_ip_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 virtual_network: Optional[pulumi.Input[pulumi.InputType['VirtualNetworkProfileArgs']]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppServiceEnvironmentArgs.__new__(AppServiceEnvironmentArgs)

            __props__.__dict__["cluster_settings"] = cluster_settings
            __props__.__dict__["custom_dns_suffix_configuration"] = custom_dns_suffix_configuration
            __props__.__dict__["dedicated_host_count"] = dedicated_host_count
            __props__.__dict__["dns_suffix"] = dns_suffix
            __props__.__dict__["front_end_scale_factor"] = front_end_scale_factor
            __props__.__dict__["internal_load_balancing_mode"] = internal_load_balancing_mode
            __props__.__dict__["ipssl_address_count"] = ipssl_address_count
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["multi_size"] = multi_size
            __props__.__dict__["name"] = name
            __props__.__dict__["networking_configuration"] = networking_configuration
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            if upgrade_preference is None:
                upgrade_preference = 'None'
            __props__.__dict__["upgrade_preference"] = upgrade_preference
            __props__.__dict__["user_whitelisted_ip_ranges"] = user_whitelisted_ip_ranges
            if virtual_network is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_network'")
            __props__.__dict__["virtual_network"] = virtual_network
            __props__.__dict__["zone_redundant"] = zone_redundant
            __props__.__dict__["has_linux_workers"] = None
            __props__.__dict__["maximum_number_of_machines"] = None
            __props__.__dict__["multi_role_count"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["suspended"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["upgrade_availability"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20150801:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20160901:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20180201:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20190801:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20200601:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20200901:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20201001:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20201201:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20210101:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20210115:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20210201:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20210301:AppServiceEnvironment"), pulumi.Alias(type_="azure-native:web/v20220901:AppServiceEnvironment")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AppServiceEnvironment, __self__).__init__(
            'azure-native:web/v20220301:AppServiceEnvironment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AppServiceEnvironment':
        """
        Get an existing AppServiceEnvironment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AppServiceEnvironmentArgs.__new__(AppServiceEnvironmentArgs)

        __props__.__dict__["cluster_settings"] = None
        __props__.__dict__["custom_dns_suffix_configuration"] = None
        __props__.__dict__["dedicated_host_count"] = None
        __props__.__dict__["dns_suffix"] = None
        __props__.__dict__["front_end_scale_factor"] = None
        __props__.__dict__["has_linux_workers"] = None
        __props__.__dict__["internal_load_balancing_mode"] = None
        __props__.__dict__["ipssl_address_count"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["maximum_number_of_machines"] = None
        __props__.__dict__["multi_role_count"] = None
        __props__.__dict__["multi_size"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["networking_configuration"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["suspended"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["upgrade_availability"] = None
        __props__.__dict__["upgrade_preference"] = None
        __props__.__dict__["user_whitelisted_ip_ranges"] = None
        __props__.__dict__["virtual_network"] = None
        __props__.__dict__["zone_redundant"] = None
        return AppServiceEnvironment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterSettings")
    def cluster_settings(self) -> pulumi.Output[Optional[Sequence['outputs.NameValuePairResponse']]]:
        """
        Custom settings for changing the behavior of the App Service Environment.
        """
        return pulumi.get(self, "cluster_settings")

    @property
    @pulumi.getter(name="customDnsSuffixConfiguration")
    def custom_dns_suffix_configuration(self) -> pulumi.Output[Optional['outputs.CustomDnsSuffixConfigurationResponse']]:
        """
        Full view of the custom domain suffix configuration for ASEv3.
        """
        return pulumi.get(self, "custom_dns_suffix_configuration")

    @property
    @pulumi.getter(name="dedicatedHostCount")
    def dedicated_host_count(self) -> pulumi.Output[Optional[int]]:
        """
        Dedicated Host Count
        """
        return pulumi.get(self, "dedicated_host_count")

    @property
    @pulumi.getter(name="dnsSuffix")
    def dns_suffix(self) -> pulumi.Output[Optional[str]]:
        """
        DNS suffix of the App Service Environment.
        """
        return pulumi.get(self, "dns_suffix")

    @property
    @pulumi.getter(name="frontEndScaleFactor")
    def front_end_scale_factor(self) -> pulumi.Output[Optional[int]]:
        """
        Scale factor for front-ends.
        """
        return pulumi.get(self, "front_end_scale_factor")

    @property
    @pulumi.getter(name="hasLinuxWorkers")
    def has_linux_workers(self) -> pulumi.Output[bool]:
        """
        Flag that displays whether an ASE has linux workers or not
        """
        return pulumi.get(self, "has_linux_workers")

    @property
    @pulumi.getter(name="internalLoadBalancingMode")
    def internal_load_balancing_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies which endpoints to serve internally in the Virtual Network for the App Service Environment.
        """
        return pulumi.get(self, "internal_load_balancing_mode")

    @property
    @pulumi.getter(name="ipsslAddressCount")
    def ipssl_address_count(self) -> pulumi.Output[Optional[int]]:
        """
        Number of IP SSL addresses reserved for the App Service Environment.
        """
        return pulumi.get(self, "ipssl_address_count")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maximumNumberOfMachines")
    def maximum_number_of_machines(self) -> pulumi.Output[int]:
        """
        Maximum number of VMs in the App Service Environment.
        """
        return pulumi.get(self, "maximum_number_of_machines")

    @property
    @pulumi.getter(name="multiRoleCount")
    def multi_role_count(self) -> pulumi.Output[int]:
        """
        Number of front-end instances.
        """
        return pulumi.get(self, "multi_role_count")

    @property
    @pulumi.getter(name="multiSize")
    def multi_size(self) -> pulumi.Output[Optional[str]]:
        """
        Front-end VM size, e.g. "Medium", "Large".
        """
        return pulumi.get(self, "multi_size")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkingConfiguration")
    def networking_configuration(self) -> pulumi.Output[Optional['outputs.AseV3NetworkingConfigurationResponse']]:
        """
        Full view of networking configuration for an ASE.
        """
        return pulumi.get(self, "networking_configuration")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the App Service Environment.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Current status of the App Service Environment.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def suspended(self) -> pulumi.Output[bool]:
        """
        <code>true</code> if the App Service Environment is suspended; otherwise, <code>false</code>. The environment can be suspended, e.g. when the management endpoint is no longer available
         (most likely because NSG blocked the incoming traffic).
        """
        return pulumi.get(self, "suspended")

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

    @property
    @pulumi.getter(name="upgradeAvailability")
    def upgrade_availability(self) -> pulumi.Output[str]:
        """
        Whether an upgrade is available for this App Service Environment.
        """
        return pulumi.get(self, "upgrade_availability")

    @property
    @pulumi.getter(name="upgradePreference")
    def upgrade_preference(self) -> pulumi.Output[Optional[str]]:
        """
        Upgrade Preference
        """
        return pulumi.get(self, "upgrade_preference")

    @property
    @pulumi.getter(name="userWhitelistedIpRanges")
    def user_whitelisted_ip_ranges(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        User added list of IP Ranges allowed on ASE db
        """
        return pulumi.get(self, "user_whitelisted_ip_ranges")

    @property
    @pulumi.getter(name="virtualNetwork")
    def virtual_network(self) -> pulumi.Output['outputs.VirtualNetworkProfileResponse']:
        """
        Description of the Virtual Network.
        """
        return pulumi.get(self, "virtual_network")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not this App Service Environment is zone-redundant.
        """
        return pulumi.get(self, "zone_redundant")

