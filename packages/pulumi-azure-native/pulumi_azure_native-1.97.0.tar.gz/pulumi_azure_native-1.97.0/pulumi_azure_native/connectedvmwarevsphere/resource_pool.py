# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ResourcePoolArgs', 'ResourcePool']

@pulumi.input_type
class ResourcePoolArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 extended_location: Optional[pulumi.Input['ExtendedLocationArgs']] = None,
                 inventory_item_id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mo_ref_id: Optional[pulumi.Input[str]] = None,
                 resource_pool_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 v_center_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ResourcePool resource.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name.
        :param pulumi.Input['ExtendedLocationArgs'] extended_location: Gets or sets the extended location.
        :param pulumi.Input[str] inventory_item_id: Gets or sets the inventory Item ID for the resource pool.
        :param pulumi.Input[str] kind: Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        :param pulumi.Input[str] location: Gets or sets the location.
        :param pulumi.Input[str] mo_ref_id: Gets or sets the vCenter MoRef (Managed Object Reference) ID for the resource pool.
        :param pulumi.Input[str] resource_pool_name: Name of the resourcePool.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets the Resource tags.
        :param pulumi.Input[str] v_center_id: Gets or sets the ARM Id of the vCenter resource in which this resource pool resides.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if extended_location is not None:
            pulumi.set(__self__, "extended_location", extended_location)
        if inventory_item_id is not None:
            pulumi.set(__self__, "inventory_item_id", inventory_item_id)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if mo_ref_id is not None:
            pulumi.set(__self__, "mo_ref_id", mo_ref_id)
        if resource_pool_name is not None:
            pulumi.set(__self__, "resource_pool_name", resource_pool_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if v_center_id is not None:
            pulumi.set(__self__, "v_center_id", v_center_id)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The Resource Group Name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> Optional[pulumi.Input['ExtendedLocationArgs']]:
        """
        Gets or sets the extended location.
        """
        return pulumi.get(self, "extended_location")

    @extended_location.setter
    def extended_location(self, value: Optional[pulumi.Input['ExtendedLocationArgs']]):
        pulumi.set(self, "extended_location", value)

    @property
    @pulumi.getter(name="inventoryItemId")
    def inventory_item_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the inventory Item ID for the resource pool.
        """
        return pulumi.get(self, "inventory_item_id")

    @inventory_item_id.setter
    def inventory_item_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "inventory_item_id", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="moRefId")
    def mo_ref_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the vCenter MoRef (Managed Object Reference) ID for the resource pool.
        """
        return pulumi.get(self, "mo_ref_id")

    @mo_ref_id.setter
    def mo_ref_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mo_ref_id", value)

    @property
    @pulumi.getter(name="resourcePoolName")
    def resource_pool_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resourcePool.
        """
        return pulumi.get(self, "resource_pool_name")

    @resource_pool_name.setter
    def resource_pool_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_pool_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Gets or sets the Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="vCenterId")
    def v_center_id(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the ARM Id of the vCenter resource in which this resource pool resides.
        """
        return pulumi.get(self, "v_center_id")

    @v_center_id.setter
    def v_center_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "v_center_id", value)


class ResourcePool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 inventory_item_id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mo_ref_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_pool_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 v_center_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Define the resourcePool.
        API Version: 2020-10-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ExtendedLocationArgs']] extended_location: Gets or sets the extended location.
        :param pulumi.Input[str] inventory_item_id: Gets or sets the inventory Item ID for the resource pool.
        :param pulumi.Input[str] kind: Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        :param pulumi.Input[str] location: Gets or sets the location.
        :param pulumi.Input[str] mo_ref_id: Gets or sets the vCenter MoRef (Managed Object Reference) ID for the resource pool.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name.
        :param pulumi.Input[str] resource_pool_name: Name of the resourcePool.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets the Resource tags.
        :param pulumi.Input[str] v_center_id: Gets or sets the ARM Id of the vCenter resource in which this resource pool resides.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ResourcePoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Define the resourcePool.
        API Version: 2020-10-01-preview.

        :param str resource_name: The name of the resource.
        :param ResourcePoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourcePoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 extended_location: Optional[pulumi.Input[pulumi.InputType['ExtendedLocationArgs']]] = None,
                 inventory_item_id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 mo_ref_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_pool_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 v_center_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ResourcePoolArgs.__new__(ResourcePoolArgs)

            __props__.__dict__["extended_location"] = extended_location
            __props__.__dict__["inventory_item_id"] = inventory_item_id
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["mo_ref_id"] = mo_ref_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_pool_name"] = resource_pool_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["v_center_id"] = v_center_id
            __props__.__dict__["cpu_limit_m_hz"] = None
            __props__.__dict__["cpu_reservation_m_hz"] = None
            __props__.__dict__["cpu_shares_level"] = None
            __props__.__dict__["custom_resource_name"] = None
            __props__.__dict__["mem_limit_mb"] = None
            __props__.__dict__["mem_reservation_mb"] = None
            __props__.__dict__["mem_shares_level"] = None
            __props__.__dict__["mo_name"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["statuses"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["uuid"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:connectedvmwarevsphere/v20201001preview:ResourcePool"), pulumi.Alias(type_="azure-native:connectedvmwarevsphere/v20220110preview:ResourcePool"), pulumi.Alias(type_="azure-native:connectedvmwarevsphere/v20220715preview:ResourcePool")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ResourcePool, __self__).__init__(
            'azure-native:connectedvmwarevsphere:ResourcePool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourcePool':
        """
        Get an existing ResourcePool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourcePoolArgs.__new__(ResourcePoolArgs)

        __props__.__dict__["cpu_limit_m_hz"] = None
        __props__.__dict__["cpu_reservation_m_hz"] = None
        __props__.__dict__["cpu_shares_level"] = None
        __props__.__dict__["custom_resource_name"] = None
        __props__.__dict__["extended_location"] = None
        __props__.__dict__["inventory_item_id"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["mem_limit_mb"] = None
        __props__.__dict__["mem_reservation_mb"] = None
        __props__.__dict__["mem_shares_level"] = None
        __props__.__dict__["mo_name"] = None
        __props__.__dict__["mo_ref_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["statuses"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["uuid"] = None
        __props__.__dict__["v_center_id"] = None
        return ResourcePool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cpuLimitMHz")
    def cpu_limit_m_hz(self) -> pulumi.Output[float]:
        """
        Gets or sets CPULimitMHz which specifies a CPU usage limit in MHz.
        Utilization will not exceed this limit even if there are available resources.
        """
        return pulumi.get(self, "cpu_limit_m_hz")

    @property
    @pulumi.getter(name="cpuReservationMHz")
    def cpu_reservation_m_hz(self) -> pulumi.Output[float]:
        """
        Gets or sets CPUReservationMHz which specifies the CPU size in MHz that is guaranteed
        to be available.
        """
        return pulumi.get(self, "cpu_reservation_m_hz")

    @property
    @pulumi.getter(name="cpuSharesLevel")
    def cpu_shares_level(self) -> pulumi.Output[str]:
        """
        Gets or sets CPUSharesLevel which specifies the CPU allocation level for this pool.
        This property is used in relative allocation between resource consumers.
        """
        return pulumi.get(self, "cpu_shares_level")

    @property
    @pulumi.getter(name="customResourceName")
    def custom_resource_name(self) -> pulumi.Output[str]:
        """
        Gets the name of the corresponding resource in Kubernetes.
        """
        return pulumi.get(self, "custom_resource_name")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> pulumi.Output[Optional['outputs.ExtendedLocationResponse']]:
        """
        Gets or sets the extended location.
        """
        return pulumi.get(self, "extended_location")

    @property
    @pulumi.getter(name="inventoryItemId")
    def inventory_item_id(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the inventory Item ID for the resource pool.
        """
        return pulumi.get(self, "inventory_item_id")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Gets or sets the location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="memLimitMB")
    def mem_limit_mb(self) -> pulumi.Output[float]:
        """
        Gets or sets MemLimitMB specifies a memory usage limit in megabytes.
        Utilization will not exceed the specified limit even if there are available resources.
        """
        return pulumi.get(self, "mem_limit_mb")

    @property
    @pulumi.getter(name="memReservationMB")
    def mem_reservation_mb(self) -> pulumi.Output[float]:
        """
        Gets or sets MemReservationMB which specifies the guaranteed available memory in
        megabytes.
        """
        return pulumi.get(self, "mem_reservation_mb")

    @property
    @pulumi.getter(name="memSharesLevel")
    def mem_shares_level(self) -> pulumi.Output[str]:
        """
        Gets or sets CPUSharesLevel which specifies the memory allocation level for this pool.
        This property is used in relative allocation between resource consumers.
        """
        return pulumi.get(self, "mem_shares_level")

    @property
    @pulumi.getter(name="moName")
    def mo_name(self) -> pulumi.Output[str]:
        """
        Gets or sets the vCenter Managed Object name for the resource pool.
        """
        return pulumi.get(self, "mo_name")

    @property
    @pulumi.getter(name="moRefId")
    def mo_ref_id(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the vCenter MoRef (Managed Object Reference) ID for the resource pool.
        """
        return pulumi.get(self, "mo_ref_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets or sets the name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Gets or sets the provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def statuses(self) -> pulumi.Output[Sequence['outputs.ResourceStatusResponse']]:
        """
        The resource status information.
        """
        return pulumi.get(self, "statuses")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system data.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Gets or sets the Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Gets or sets the type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def uuid(self) -> pulumi.Output[str]:
        """
        Gets or sets a unique identifier for this resource.
        """
        return pulumi.get(self, "uuid")

    @property
    @pulumi.getter(name="vCenterId")
    def v_center_id(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the ARM Id of the vCenter resource in which this resource pool resides.
        """
        return pulumi.get(self, "v_center_id")

