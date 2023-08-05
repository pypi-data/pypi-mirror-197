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

__all__ = ['IotDpsResourcePrivateEndpointConnectionArgs', 'IotDpsResourcePrivateEndpointConnection']

@pulumi.input_type
class IotDpsResourcePrivateEndpointConnectionArgs:
    def __init__(__self__, *,
                 properties: pulumi.Input['PrivateEndpointConnectionPropertiesArgs'],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IotDpsResourcePrivateEndpointConnection resource.
        :param pulumi.Input['PrivateEndpointConnectionPropertiesArgs'] properties: The properties of a private endpoint connection
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the provisioning service.
        :param pulumi.Input[str] resource_name: The name of the provisioning service.
        :param pulumi.Input[str] private_endpoint_connection_name: The name of the private endpoint connection
        """
        pulumi.set(__self__, "properties", properties)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if private_endpoint_connection_name is not None:
            pulumi.set(__self__, "private_endpoint_connection_name", private_endpoint_connection_name)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['PrivateEndpointConnectionPropertiesArgs']:
        """
        The properties of a private endpoint connection
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: pulumi.Input['PrivateEndpointConnectionPropertiesArgs']):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the provisioning service.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the provisioning service.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="privateEndpointConnectionName")
    def private_endpoint_connection_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the private endpoint connection
        """
        return pulumi.get(self, "private_endpoint_connection_name")

    @private_endpoint_connection_name.setter
    def private_endpoint_connection_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_endpoint_connection_name", value)


class IotDpsResourcePrivateEndpointConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointConnectionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The private endpoint connection of a provisioning service

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] private_endpoint_connection_name: The name of the private endpoint connection
        :param pulumi.Input[pulumi.InputType['PrivateEndpointConnectionPropertiesArgs']] properties: The properties of a private endpoint connection
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the provisioning service.
        :param pulumi.Input[str] resource_name_: The name of the provisioning service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IotDpsResourcePrivateEndpointConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The private endpoint connection of a provisioning service

        :param str resource_name: The name of the resource.
        :param IotDpsResourcePrivateEndpointConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IotDpsResourcePrivateEndpointConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointConnectionPropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IotDpsResourcePrivateEndpointConnectionArgs.__new__(IotDpsResourcePrivateEndpointConnectionArgs)

            __props__.__dict__["private_endpoint_connection_name"] = private_endpoint_connection_name
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:devices:IotDpsResourcePrivateEndpointConnection"), pulumi.Alias(type_="azure-native:devices/v20200301:IotDpsResourcePrivateEndpointConnection"), pulumi.Alias(type_="azure-native:devices/v20211015:IotDpsResourcePrivateEndpointConnection"), pulumi.Alias(type_="azure-native:devices/v20220205:IotDpsResourcePrivateEndpointConnection"), pulumi.Alias(type_="azure-native:devices/v20221212:IotDpsResourcePrivateEndpointConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(IotDpsResourcePrivateEndpointConnection, __self__).__init__(
            'azure-native:devices/v20200901preview:IotDpsResourcePrivateEndpointConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'IotDpsResourcePrivateEndpointConnection':
        """
        Get an existing IotDpsResourcePrivateEndpointConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = IotDpsResourcePrivateEndpointConnectionArgs.__new__(IotDpsResourcePrivateEndpointConnectionArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return IotDpsResourcePrivateEndpointConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.PrivateEndpointConnectionPropertiesResponse']:
        """
        The properties of a private endpoint connection
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

