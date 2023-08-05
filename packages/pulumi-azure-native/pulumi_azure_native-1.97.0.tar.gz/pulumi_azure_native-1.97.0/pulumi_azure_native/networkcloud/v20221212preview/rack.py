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
from ._inputs import *

__all__ = ['RackArgs', 'Rack']

@pulumi.input_type
class RackArgs:
    def __init__(__self__, *,
                 availability_zone: pulumi.Input[str],
                 extended_location: pulumi.Input['ExtendedLocationArgs'],
                 rack_location: pulumi.Input[str],
                 rack_serial_number: pulumi.Input[str],
                 rack_sku_id: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 rack_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Rack resource.
        :param pulumi.Input[str] availability_zone: The value that will be used for machines in this rack to represent the availability zones that can be referenced by Hybrid AKS Clusters for node arrangement.
        :param pulumi.Input['ExtendedLocationArgs'] extended_location: The extended location of the cluster associated with the resource.
        :param pulumi.Input[str] rack_location: The free-form description of the rack location. (e.g. “DTN Datacenter, Floor 3, Isle 9, Rack 2B”)
        :param pulumi.Input[str] rack_serial_number: The unique identifier for the rack within Network Cloud cluster. An alternate unique alphanumeric value other than a serial number may be provided if desired.
        :param pulumi.Input[str] rack_sku_id: The SKU for the rack.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] rack_name: The name of the rack.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "availability_zone", availability_zone)
        pulumi.set(__self__, "extended_location", extended_location)
        pulumi.set(__self__, "rack_location", rack_location)
        pulumi.set(__self__, "rack_serial_number", rack_serial_number)
        pulumi.set(__self__, "rack_sku_id", rack_sku_id)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if rack_name is not None:
            pulumi.set(__self__, "rack_name", rack_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> pulumi.Input[str]:
        """
        The value that will be used for machines in this rack to represent the availability zones that can be referenced by Hybrid AKS Clusters for node arrangement.
        """
        return pulumi.get(self, "availability_zone")

    @availability_zone.setter
    def availability_zone(self, value: pulumi.Input[str]):
        pulumi.set(self, "availability_zone", value)

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> pulumi.Input['ExtendedLocationArgs']:
        """
        The extended location of the cluster associated with the resource.
        """
        return pulumi.get(self, "extended_location")

    @extended_location.setter
    def extended_location(self, value: pulumi.Input['ExtendedLocationArgs']):
        pulumi.set(self, "extended_location", value)

    @property
    @pulumi.getter(name="rackLocation")
    def rack_location(self) -> pulumi.Input[str]:
        """
        The free-form description of the rack location. (e.g. “DTN Datacenter, Floor 3, Isle 9, Rack 2B”)
        """
        return pulumi.get(self, "rack_location")

    @rack_location.setter
    def rack_location(self, value: pulumi.Input[str]):
        pulumi.set(self, "rack_location", value)

    @property
    @pulumi.getter(name="rackSerialNumber")
    def rack_serial_number(self) -> pulumi.Input[str]:
        """
        The unique identifier for the rack within Network Cloud cluster. An alternate unique alphanumeric value other than a serial number may be provided if desired.
        """
        return pulumi.get(self, "rack_serial_number")

    @rack_serial_number.setter
    def rack_serial_number(self, value: pulumi.Input[str]):
        pulumi.set(self, "rack_serial_number", value)

    @property
    @pulumi.getter(name="rackSkuId")
    def rack_sku_id(self) -> pulumi.Input[str]:
        """
        The SKU for the rack.
        """
        return pulumi.get(self, "rack_sku_id")

    @rack_sku_id.setter
    def rack_sku_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "rack_sku_id", value)

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
    @pulumi.getter(name="rackName")
    def rack_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the rack.
        """
        return pulumi.get(self, "rack_name")

    @rack_name.setter
    def rack_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rack_name", value)

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


class Rack(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 rack_location: Optional[pulumi.Input[str]] = None,
                 rack_name: Optional[pulumi.Input[str]] = None,
                 rack_serial_number: Optional[pulumi.Input[str]] = None,
                 rack_sku_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Create a Rack resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_zone: The value that will be used for machines in this rack to represent the availability zones that can be referenced by Hybrid AKS Clusters for node arrangement.
        :param pulumi.Input[pulumi.InputType['ExtendedLocationArgs']] extended_location: The extended location of the cluster associated with the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] rack_location: The free-form description of the rack location. (e.g. “DTN Datacenter, Floor 3, Isle 9, Rack 2B”)
        :param pulumi.Input[str] rack_name: The name of the rack.
        :param pulumi.Input[str] rack_serial_number: The unique identifier for the rack within Network Cloud cluster. An alternate unique alphanumeric value other than a serial number may be provided if desired.
        :param pulumi.Input[str] rack_sku_id: The SKU for the rack.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RackArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Rack resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param RackArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RackArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 rack_location: Optional[pulumi.Input[str]] = None,
                 rack_name: Optional[pulumi.Input[str]] = None,
                 rack_serial_number: Optional[pulumi.Input[str]] = None,
                 rack_sku_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RackArgs.__new__(RackArgs)

            if availability_zone is None and not opts.urn:
                raise TypeError("Missing required property 'availability_zone'")
            __props__.__dict__["availability_zone"] = availability_zone
            if extended_location is None and not opts.urn:
                raise TypeError("Missing required property 'extended_location'")
            __props__.__dict__["extended_location"] = extended_location
            __props__.__dict__["location"] = location
            if rack_location is None and not opts.urn:
                raise TypeError("Missing required property 'rack_location'")
            __props__.__dict__["rack_location"] = rack_location
            __props__.__dict__["rack_name"] = rack_name
            if rack_serial_number is None and not opts.urn:
                raise TypeError("Missing required property 'rack_serial_number'")
            __props__.__dict__["rack_serial_number"] = rack_serial_number
            if rack_sku_id is None and not opts.urn:
                raise TypeError("Missing required property 'rack_sku_id'")
            __props__.__dict__["rack_sku_id"] = rack_sku_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["cluster_id"] = None
            __props__.__dict__["detailed_status"] = None
            __props__.__dict__["detailed_status_message"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:networkcloud:Rack")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Rack, __self__).__init__(
            'azure-native:networkcloud/v20221212preview:Rack',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Rack':
        """
        Get an existing Rack resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RackArgs.__new__(RackArgs)

        __props__.__dict__["availability_zone"] = None
        __props__.__dict__["cluster_id"] = None
        __props__.__dict__["detailed_status"] = None
        __props__.__dict__["detailed_status_message"] = None
        __props__.__dict__["extended_location"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["rack_location"] = None
        __props__.__dict__["rack_serial_number"] = None
        __props__.__dict__["rack_sku_id"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Rack(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> pulumi.Output[str]:
        """
        The value that will be used for machines in this rack to represent the availability zones that can be referenced by Hybrid AKS Clusters for node arrangement.
        """
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Output[str]:
        """
        The resource ID of the cluster the rack is created for. This value is set when the rack is created by the cluster.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="detailedStatus")
    def detailed_status(self) -> pulumi.Output[str]:
        """
        The more detailed status of the rack.
        """
        return pulumi.get(self, "detailed_status")

    @property
    @pulumi.getter(name="detailedStatusMessage")
    def detailed_status_message(self) -> pulumi.Output[str]:
        """
        The descriptive message about the current detailed status.
        """
        return pulumi.get(self, "detailed_status_message")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> pulumi.Output['outputs.ExtendedLocationResponse']:
        """
        The extended location of the cluster associated with the resource.
        """
        return pulumi.get(self, "extended_location")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the rack resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="rackLocation")
    def rack_location(self) -> pulumi.Output[str]:
        """
        The free-form description of the rack location. (e.g. “DTN Datacenter, Floor 3, Isle 9, Rack 2B”)
        """
        return pulumi.get(self, "rack_location")

    @property
    @pulumi.getter(name="rackSerialNumber")
    def rack_serial_number(self) -> pulumi.Output[str]:
        """
        The unique identifier for the rack within Network Cloud cluster. An alternate unique alphanumeric value other than a serial number may be provided if desired.
        """
        return pulumi.get(self, "rack_serial_number")

    @property
    @pulumi.getter(name="rackSkuId")
    def rack_sku_id(self) -> pulumi.Output[str]:
        """
        The SKU for the rack.
        """
        return pulumi.get(self, "rack_sku_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
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

