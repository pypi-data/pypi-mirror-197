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

__all__ = ['ResourceTypeRegistrationInitArgs', 'ResourceTypeRegistration']

@pulumi.input_type
class ResourceTypeRegistrationInitArgs:
    def __init__(__self__, *,
                 provider_namespace: pulumi.Input[str],
                 properties: Optional[pulumi.Input['ResourceTypeRegistrationPropertiesArgs']] = None,
                 resource_type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ResourceTypeRegistration resource.
        :param pulumi.Input[str] provider_namespace: The name of the resource provider hosted within ProviderHub.
        :param pulumi.Input[str] resource_type: The resource type.
        """
        pulumi.set(__self__, "provider_namespace", provider_namespace)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_type is not None:
            pulumi.set(__self__, "resource_type", resource_type)

    @property
    @pulumi.getter(name="providerNamespace")
    def provider_namespace(self) -> pulumi.Input[str]:
        """
        The name of the resource provider hosted within ProviderHub.
        """
        return pulumi.get(self, "provider_namespace")

    @provider_namespace.setter
    def provider_namespace(self, value: pulumi.Input[str]):
        pulumi.set(self, "provider_namespace", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['ResourceTypeRegistrationPropertiesArgs']]:
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['ResourceTypeRegistrationPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> Optional[pulumi.Input[str]]:
        """
        The resource type.
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_type", value)


class ResourceTypeRegistration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ResourceTypeRegistrationPropertiesArgs']]] = None,
                 provider_namespace: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a ResourceTypeRegistration resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] provider_namespace: The name of the resource provider hosted within ProviderHub.
        :param pulumi.Input[str] resource_type: The resource type.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourceTypeRegistrationInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ResourceTypeRegistration resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ResourceTypeRegistrationInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceTypeRegistrationInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ResourceTypeRegistrationPropertiesArgs']]] = None,
                 provider_namespace: Optional[pulumi.Input[str]] = None,
                 resource_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourceTypeRegistrationInitArgs.__new__(ResourceTypeRegistrationInitArgs)

            __props__.__dict__["properties"] = properties
            if provider_namespace is None and not opts.urn:
                raise TypeError("Missing required property 'provider_namespace'")
            __props__.__dict__["provider_namespace"] = provider_namespace
            __props__.__dict__["resource_type"] = resource_type
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:providerhub:ResourceTypeRegistration"), pulumi.Alias(type_="azure-native:providerhub/v20201120:ResourceTypeRegistration"), pulumi.Alias(type_="azure-native:providerhub/v20210501preview:ResourceTypeRegistration"), pulumi.Alias(type_="azure-native:providerhub/v20210601preview:ResourceTypeRegistration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ResourceTypeRegistration, __self__).__init__(
            'azure-native:providerhub/v20210901preview:ResourceTypeRegistration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourceTypeRegistration':
        """
        Get an existing ResourceTypeRegistration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourceTypeRegistrationInitArgs.__new__(ResourceTypeRegistrationInitArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return ResourceTypeRegistration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ResourceTypeRegistrationResponseProperties']:
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

