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

__all__ = ['MachineExtensionArgs', 'MachineExtension']

@pulumi.input_type
class MachineExtensionArgs:
    def __init__(__self__, *,
                 machine_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 extension_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['MachineExtensionPropertiesArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a MachineExtension resource.
        :param pulumi.Input[str] machine_name: The name of the machine where the extension should be created or updated.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] extension_name: The name of the machine extension.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input['MachineExtensionPropertiesArgs'] properties: Describes Machine Extension Properties.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "machine_name", machine_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if extension_name is not None:
            pulumi.set(__self__, "extension_name", extension_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="machineName")
    def machine_name(self) -> pulumi.Input[str]:
        """
        The name of the machine where the extension should be created or updated.
        """
        return pulumi.get(self, "machine_name")

    @machine_name.setter
    def machine_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "machine_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="extensionName")
    def extension_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the machine extension.
        """
        return pulumi.get(self, "extension_name")

    @extension_name.setter
    def extension_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "extension_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['MachineExtensionPropertiesArgs']]:
        """
        Describes Machine Extension Properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['MachineExtensionPropertiesArgs']]):
        pulumi.set(self, "properties", value)

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


class MachineExtension(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 extension_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 machine_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['MachineExtensionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Describes a Machine Extension.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] extension_name: The name of the machine extension.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] machine_name: The name of the machine where the extension should be created or updated.
        :param pulumi.Input[pulumi.InputType['MachineExtensionPropertiesArgs']] properties: Describes Machine Extension Properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MachineExtensionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a Machine Extension.

        :param str resource_name: The name of the resource.
        :param MachineExtensionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MachineExtensionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 extension_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 machine_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['MachineExtensionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MachineExtensionArgs.__new__(MachineExtensionArgs)

            __props__.__dict__["extension_name"] = extension_name
            __props__.__dict__["location"] = location
            if machine_name is None and not opts.urn:
                raise TypeError("Missing required property 'machine_name'")
            __props__.__dict__["machine_name"] = machine_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:hybridcompute:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20190802preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20191212:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20200730preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20200802:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20200815preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20210128preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20210325preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20210517preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20210520:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20210610preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20211210preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20220310:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20220510preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20220811preview:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20221110:MachineExtension"), pulumi.Alias(type_="azure-native:hybridcompute/v20221227preview:MachineExtension")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MachineExtension, __self__).__init__(
            'azure-native:hybridcompute/v20210422preview:MachineExtension',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MachineExtension':
        """
        Get an existing MachineExtension resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MachineExtensionArgs.__new__(MachineExtensionArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return MachineExtension(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.MachineExtensionPropertiesResponse']:
        """
        Describes Machine Extension Properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

