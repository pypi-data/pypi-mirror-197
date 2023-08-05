# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['WorkloadNetworkPublicIPArgs', 'WorkloadNetworkPublicIP']

@pulumi.input_type
class WorkloadNetworkPublicIPArgs:
    def __init__(__self__, *,
                 private_cloud_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 display_name: Optional[pulumi.Input[str]] = None,
                 number_of_public_ips: Optional[pulumi.Input[float]] = None,
                 public_ip_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WorkloadNetworkPublicIP resource.
        :param pulumi.Input[str] private_cloud_name: Name of the private cloud
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] display_name: Display name of the Public IP Block.
        :param pulumi.Input[float] number_of_public_ips: Number of Public IPs requested.
        :param pulumi.Input[str] public_ip_id: NSX Public IP Block identifier. Generally the same as the Public IP Block's display name
        """
        pulumi.set(__self__, "private_cloud_name", private_cloud_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if number_of_public_ips is not None:
            pulumi.set(__self__, "number_of_public_ips", number_of_public_ips)
        if public_ip_id is not None:
            pulumi.set(__self__, "public_ip_id", public_ip_id)

    @property
    @pulumi.getter(name="privateCloudName")
    def private_cloud_name(self) -> pulumi.Input[str]:
        """
        Name of the private cloud
        """
        return pulumi.get(self, "private_cloud_name")

    @private_cloud_name.setter
    def private_cloud_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_cloud_name", value)

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
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Display name of the Public IP Block.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="numberOfPublicIPs")
    def number_of_public_ips(self) -> Optional[pulumi.Input[float]]:
        """
        Number of Public IPs requested.
        """
        return pulumi.get(self, "number_of_public_ips")

    @number_of_public_ips.setter
    def number_of_public_ips(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "number_of_public_ips", value)

    @property
    @pulumi.getter(name="publicIPId")
    def public_ip_id(self) -> Optional[pulumi.Input[str]]:
        """
        NSX Public IP Block identifier. Generally the same as the Public IP Block's display name
        """
        return pulumi.get(self, "public_ip_id")

    @public_ip_id.setter
    def public_ip_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ip_id", value)


class WorkloadNetworkPublicIP(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 number_of_public_ips: Optional[pulumi.Input[float]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 public_ip_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        NSX Public IP Block
        API Version: 2021-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] display_name: Display name of the Public IP Block.
        :param pulumi.Input[float] number_of_public_ips: Number of Public IPs requested.
        :param pulumi.Input[str] private_cloud_name: Name of the private cloud
        :param pulumi.Input[str] public_ip_id: NSX Public IP Block identifier. Generally the same as the Public IP Block's display name
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkloadNetworkPublicIPArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        NSX Public IP Block
        API Version: 2021-06-01.

        :param str resource_name: The name of the resource.
        :param WorkloadNetworkPublicIPArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkloadNetworkPublicIPArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 number_of_public_ips: Optional[pulumi.Input[float]] = None,
                 private_cloud_name: Optional[pulumi.Input[str]] = None,
                 public_ip_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkloadNetworkPublicIPArgs.__new__(WorkloadNetworkPublicIPArgs)

            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["number_of_public_ips"] = number_of_public_ips
            if private_cloud_name is None and not opts.urn:
                raise TypeError("Missing required property 'private_cloud_name'")
            __props__.__dict__["private_cloud_name"] = private_cloud_name
            __props__.__dict__["public_ip_id"] = public_ip_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["public_ip_block"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:avs/v20210601:WorkloadNetworkPublicIP"), pulumi.Alias(type_="azure-native:avs/v20211201:WorkloadNetworkPublicIP"), pulumi.Alias(type_="azure-native:avs/v20220501:WorkloadNetworkPublicIP")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WorkloadNetworkPublicIP, __self__).__init__(
            'azure-native:avs:WorkloadNetworkPublicIP',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WorkloadNetworkPublicIP':
        """
        Get an existing WorkloadNetworkPublicIP resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WorkloadNetworkPublicIPArgs.__new__(WorkloadNetworkPublicIPArgs)

        __props__.__dict__["display_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["number_of_public_ips"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_ip_block"] = None
        __props__.__dict__["type"] = None
        return WorkloadNetworkPublicIP(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        Display name of the Public IP Block.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numberOfPublicIPs")
    def number_of_public_ips(self) -> pulumi.Output[Optional[float]]:
        """
        Number of Public IPs requested.
        """
        return pulumi.get(self, "number_of_public_ips")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicIPBlock")
    def public_ip_block(self) -> pulumi.Output[str]:
        """
        CIDR Block of the Public IP Block.
        """
        return pulumi.get(self, "public_ip_block")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

