# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['SiteRelayServiceConnectionSlotArgs', 'SiteRelayServiceConnectionSlot']

@pulumi.input_type
class SiteRelayServiceConnectionSlotArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 slot: pulumi.Input[str],
                 biztalk_uri: Optional[pulumi.Input[str]] = None,
                 entity_connection_string: Optional[pulumi.Input[str]] = None,
                 entity_name: Optional[pulumi.Input[str]] = None,
                 hostname: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_connection_string: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SiteRelayServiceConnectionSlot resource.
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] resource_group_name: The resource group name
        :param pulumi.Input[str] slot: The name of the slot for the web app.
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "slot", slot)
        if biztalk_uri is not None:
            pulumi.set(__self__, "biztalk_uri", biztalk_uri)
        if entity_connection_string is not None:
            pulumi.set(__self__, "entity_connection_string", entity_connection_string)
        if entity_name is not None:
            pulumi.set(__self__, "entity_name", entity_name)
        if hostname is not None:
            pulumi.set(__self__, "hostname", hostname)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if resource_connection_string is not None:
            pulumi.set(__self__, "resource_connection_string", resource_connection_string)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def slot(self) -> pulumi.Input[str]:
        """
        The name of the slot for the web app.
        """
        return pulumi.get(self, "slot")

    @slot.setter
    def slot(self, value: pulumi.Input[str]):
        pulumi.set(self, "slot", value)

    @property
    @pulumi.getter(name="biztalkUri")
    def biztalk_uri(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "biztalk_uri")

    @biztalk_uri.setter
    def biztalk_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "biztalk_uri", value)

    @property
    @pulumi.getter(name="entityConnectionString")
    def entity_connection_string(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "entity_connection_string")

    @entity_connection_string.setter
    def entity_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entity_connection_string", value)

    @property
    @pulumi.getter(name="entityName")
    def entity_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "entity_name")

    @entity_name.setter
    def entity_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "entity_name", value)

    @property
    @pulumi.getter
    def hostname(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "hostname")

    @hostname.setter
    def hostname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hostname", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="resourceConnectionString")
    def resource_connection_string(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_connection_string")

    @resource_connection_string.setter
    def resource_connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_connection_string", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


warnings.warn("""Version 2015-08-01 will be removed in v2 of the provider.""", DeprecationWarning)


class SiteRelayServiceConnectionSlot(pulumi.CustomResource):
    warnings.warn("""Version 2015-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 biztalk_uri: Optional[pulumi.Input[str]] = None,
                 entity_connection_string: Optional[pulumi.Input[str]] = None,
                 entity_name: Optional[pulumi.Input[str]] = None,
                 hostname: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_connection_string: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Class that represents a BizTalk Hybrid Connection

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] resource_group_name: The resource group name
        :param pulumi.Input[str] slot: The name of the slot for the web app.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SiteRelayServiceConnectionSlotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Class that represents a BizTalk Hybrid Connection

        :param str resource_name: The name of the resource.
        :param SiteRelayServiceConnectionSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SiteRelayServiceConnectionSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 biztalk_uri: Optional[pulumi.Input[str]] = None,
                 entity_connection_string: Optional[pulumi.Input[str]] = None,
                 entity_name: Optional[pulumi.Input[str]] = None,
                 hostname: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_connection_string: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""SiteRelayServiceConnectionSlot is deprecated: Version 2015-08-01 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SiteRelayServiceConnectionSlotArgs.__new__(SiteRelayServiceConnectionSlotArgs)

            __props__.__dict__["biztalk_uri"] = biztalk_uri
            __props__.__dict__["entity_connection_string"] = entity_connection_string
            __props__.__dict__["entity_name"] = entity_name
            __props__.__dict__["hostname"] = hostname
            __props__.__dict__["id"] = id
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["port"] = port
            __props__.__dict__["resource_connection_string"] = resource_connection_string
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_type"] = resource_type
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__.__dict__["slot"] = slot
            __props__.__dict__["tags"] = tags
            __props__.__dict__["type"] = type
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20160801:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20180201:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20181101:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20190801:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20200601:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20200901:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20201001:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20201201:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20210101:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20210115:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20210201:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20210301:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20220301:SiteRelayServiceConnectionSlot"), pulumi.Alias(type_="azure-native:web/v20220901:SiteRelayServiceConnectionSlot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SiteRelayServiceConnectionSlot, __self__).__init__(
            'azure-native:web/v20150801:SiteRelayServiceConnectionSlot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SiteRelayServiceConnectionSlot':
        """
        Get an existing SiteRelayServiceConnectionSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SiteRelayServiceConnectionSlotArgs.__new__(SiteRelayServiceConnectionSlotArgs)

        __props__.__dict__["biztalk_uri"] = None
        __props__.__dict__["entity_connection_string"] = None
        __props__.__dict__["entity_name"] = None
        __props__.__dict__["hostname"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["resource_connection_string"] = None
        __props__.__dict__["resource_type"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return SiteRelayServiceConnectionSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="biztalkUri")
    def biztalk_uri(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "biztalk_uri")

    @property
    @pulumi.getter(name="entityConnectionString")
    def entity_connection_string(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "entity_connection_string")

    @property
    @pulumi.getter(name="entityName")
    def entity_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "entity_name")

    @property
    @pulumi.getter
    def hostname(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="resourceConnectionString")
    def resource_connection_string(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "resource_connection_string")

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "resource_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

