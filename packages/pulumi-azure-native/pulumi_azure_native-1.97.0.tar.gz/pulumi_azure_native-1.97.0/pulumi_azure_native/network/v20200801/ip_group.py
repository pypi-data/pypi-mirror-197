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

__all__ = ['IpGroupArgs', 'IpGroup']

@pulumi.input_type
class IpGroupArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_groups_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a IpGroup resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: IpAddresses/IpAddressPrefixes in the IpGroups resource.
        :param pulumi.Input[str] ip_groups_name: The name of the ipGroups.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if ip_groups_name is not None:
            pulumi.set(__self__, "ip_groups_name", ip_groups_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
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
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        IpAddresses/IpAddressPrefixes in the IpGroups resource.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter(name="ipGroupsName")
    def ip_groups_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the ipGroups.
        """
        return pulumi.get(self, "ip_groups_name")

    @ip_groups_name.setter
    def ip_groups_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_groups_name", value)

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
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class IpGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_groups_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The IpGroups resource information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_addresses: IpAddresses/IpAddressPrefixes in the IpGroups resource.
        :param pulumi.Input[str] ip_groups_name: The name of the ipGroups.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IpGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The IpGroups resource information.

        :param str resource_name: The name of the resource.
        :param IpGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IpGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 ip_groups_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IpGroupArgs.__new__(IpGroupArgs)

            __props__.__dict__["id"] = id
            __props__.__dict__["ip_addresses"] = ip_addresses
            __props__.__dict__["ip_groups_name"] = ip_groups_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["etag"] = None
            __props__.__dict__["firewall_policies"] = None
            __props__.__dict__["firewalls"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:IpGroup"), pulumi.Alias(type_="azure-native:network/v20190901:IpGroup"), pulumi.Alias(type_="azure-native:network/v20191101:IpGroup"), pulumi.Alias(type_="azure-native:network/v20191201:IpGroup"), pulumi.Alias(type_="azure-native:network/v20200301:IpGroup"), pulumi.Alias(type_="azure-native:network/v20200401:IpGroup"), pulumi.Alias(type_="azure-native:network/v20200501:IpGroup"), pulumi.Alias(type_="azure-native:network/v20200601:IpGroup"), pulumi.Alias(type_="azure-native:network/v20200701:IpGroup"), pulumi.Alias(type_="azure-native:network/v20201101:IpGroup"), pulumi.Alias(type_="azure-native:network/v20210201:IpGroup"), pulumi.Alias(type_="azure-native:network/v20210301:IpGroup"), pulumi.Alias(type_="azure-native:network/v20210501:IpGroup"), pulumi.Alias(type_="azure-native:network/v20210801:IpGroup"), pulumi.Alias(type_="azure-native:network/v20220101:IpGroup"), pulumi.Alias(type_="azure-native:network/v20220501:IpGroup"), pulumi.Alias(type_="azure-native:network/v20220701:IpGroup"), pulumi.Alias(type_="azure-native:network/v20220901:IpGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IpGroup, __self__).__init__(
            'azure-native:network/v20200801:IpGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IpGroup':
        """
        Get an existing IpGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IpGroupArgs.__new__(IpGroupArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["firewall_policies"] = None
        __props__.__dict__["firewalls"] = None
        __props__.__dict__["ip_addresses"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return IpGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="firewallPolicies")
    def firewall_policies(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to Firewall Policies resources that this IpGroups is associated with.
        """
        return pulumi.get(self, "firewall_policies")

    @property
    @pulumi.getter
    def firewalls(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to Firewall resources that this IpGroups is associated with.
        """
        return pulumi.get(self, "firewalls")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        IpAddresses/IpAddressPrefixes in the IpGroups resource.
        """
        return pulumi.get(self, "ip_addresses")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the IpGroups resource.
        """
        return pulumi.get(self, "provisioning_state")

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

