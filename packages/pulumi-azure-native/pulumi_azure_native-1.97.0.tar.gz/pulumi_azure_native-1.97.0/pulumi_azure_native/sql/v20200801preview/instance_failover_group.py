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

__all__ = ['InstanceFailoverGroupArgs', 'InstanceFailoverGroup']

@pulumi.input_type
class InstanceFailoverGroupArgs:
    def __init__(__self__, *,
                 location_name: pulumi.Input[str],
                 managed_instance_pairs: pulumi.Input[Sequence[pulumi.Input['ManagedInstancePairInfoArgs']]],
                 partner_regions: pulumi.Input[Sequence[pulumi.Input['PartnerRegionInfoArgs']]],
                 read_write_endpoint: pulumi.Input['InstanceFailoverGroupReadWriteEndpointArgs'],
                 resource_group_name: pulumi.Input[str],
                 failover_group_name: Optional[pulumi.Input[str]] = None,
                 read_only_endpoint: Optional[pulumi.Input['InstanceFailoverGroupReadOnlyEndpointArgs']] = None):
        """
        The set of arguments for constructing a InstanceFailoverGroup resource.
        :param pulumi.Input[str] location_name: The name of the region where the resource is located.
        :param pulumi.Input[Sequence[pulumi.Input['ManagedInstancePairInfoArgs']]] managed_instance_pairs: List of managed instance pairs in the failover group.
        :param pulumi.Input[Sequence[pulumi.Input['PartnerRegionInfoArgs']]] partner_regions: Partner region information for the failover group.
        :param pulumi.Input['InstanceFailoverGroupReadWriteEndpointArgs'] read_write_endpoint: Read-write endpoint of the failover group instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] failover_group_name: The name of the failover group.
        :param pulumi.Input['InstanceFailoverGroupReadOnlyEndpointArgs'] read_only_endpoint: Read-only endpoint of the failover group instance.
        """
        pulumi.set(__self__, "location_name", location_name)
        pulumi.set(__self__, "managed_instance_pairs", managed_instance_pairs)
        pulumi.set(__self__, "partner_regions", partner_regions)
        pulumi.set(__self__, "read_write_endpoint", read_write_endpoint)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if failover_group_name is not None:
            pulumi.set(__self__, "failover_group_name", failover_group_name)
        if read_only_endpoint is not None:
            pulumi.set(__self__, "read_only_endpoint", read_only_endpoint)

    @property
    @pulumi.getter(name="locationName")
    def location_name(self) -> pulumi.Input[str]:
        """
        The name of the region where the resource is located.
        """
        return pulumi.get(self, "location_name")

    @location_name.setter
    def location_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "location_name", value)

    @property
    @pulumi.getter(name="managedInstancePairs")
    def managed_instance_pairs(self) -> pulumi.Input[Sequence[pulumi.Input['ManagedInstancePairInfoArgs']]]:
        """
        List of managed instance pairs in the failover group.
        """
        return pulumi.get(self, "managed_instance_pairs")

    @managed_instance_pairs.setter
    def managed_instance_pairs(self, value: pulumi.Input[Sequence[pulumi.Input['ManagedInstancePairInfoArgs']]]):
        pulumi.set(self, "managed_instance_pairs", value)

    @property
    @pulumi.getter(name="partnerRegions")
    def partner_regions(self) -> pulumi.Input[Sequence[pulumi.Input['PartnerRegionInfoArgs']]]:
        """
        Partner region information for the failover group.
        """
        return pulumi.get(self, "partner_regions")

    @partner_regions.setter
    def partner_regions(self, value: pulumi.Input[Sequence[pulumi.Input['PartnerRegionInfoArgs']]]):
        pulumi.set(self, "partner_regions", value)

    @property
    @pulumi.getter(name="readWriteEndpoint")
    def read_write_endpoint(self) -> pulumi.Input['InstanceFailoverGroupReadWriteEndpointArgs']:
        """
        Read-write endpoint of the failover group instance.
        """
        return pulumi.get(self, "read_write_endpoint")

    @read_write_endpoint.setter
    def read_write_endpoint(self, value: pulumi.Input['InstanceFailoverGroupReadWriteEndpointArgs']):
        pulumi.set(self, "read_write_endpoint", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="failoverGroupName")
    def failover_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the failover group.
        """
        return pulumi.get(self, "failover_group_name")

    @failover_group_name.setter
    def failover_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "failover_group_name", value)

    @property
    @pulumi.getter(name="readOnlyEndpoint")
    def read_only_endpoint(self) -> Optional[pulumi.Input['InstanceFailoverGroupReadOnlyEndpointArgs']]:
        """
        Read-only endpoint of the failover group instance.
        """
        return pulumi.get(self, "read_only_endpoint")

    @read_only_endpoint.setter
    def read_only_endpoint(self, value: Optional[pulumi.Input['InstanceFailoverGroupReadOnlyEndpointArgs']]):
        pulumi.set(self, "read_only_endpoint", value)


class InstanceFailoverGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 failover_group_name: Optional[pulumi.Input[str]] = None,
                 location_name: Optional[pulumi.Input[str]] = None,
                 managed_instance_pairs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ManagedInstancePairInfoArgs']]]]] = None,
                 partner_regions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PartnerRegionInfoArgs']]]]] = None,
                 read_only_endpoint: Optional[pulumi.Input[pulumi.InputType['InstanceFailoverGroupReadOnlyEndpointArgs']]] = None,
                 read_write_endpoint: Optional[pulumi.Input[pulumi.InputType['InstanceFailoverGroupReadWriteEndpointArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An instance failover group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] failover_group_name: The name of the failover group.
        :param pulumi.Input[str] location_name: The name of the region where the resource is located.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ManagedInstancePairInfoArgs']]]] managed_instance_pairs: List of managed instance pairs in the failover group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PartnerRegionInfoArgs']]]] partner_regions: Partner region information for the failover group.
        :param pulumi.Input[pulumi.InputType['InstanceFailoverGroupReadOnlyEndpointArgs']] read_only_endpoint: Read-only endpoint of the failover group instance.
        :param pulumi.Input[pulumi.InputType['InstanceFailoverGroupReadWriteEndpointArgs']] read_write_endpoint: Read-write endpoint of the failover group instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceFailoverGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An instance failover group.

        :param str resource_name: The name of the resource.
        :param InstanceFailoverGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceFailoverGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 failover_group_name: Optional[pulumi.Input[str]] = None,
                 location_name: Optional[pulumi.Input[str]] = None,
                 managed_instance_pairs: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ManagedInstancePairInfoArgs']]]]] = None,
                 partner_regions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PartnerRegionInfoArgs']]]]] = None,
                 read_only_endpoint: Optional[pulumi.Input[pulumi.InputType['InstanceFailoverGroupReadOnlyEndpointArgs']]] = None,
                 read_write_endpoint: Optional[pulumi.Input[pulumi.InputType['InstanceFailoverGroupReadWriteEndpointArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = InstanceFailoverGroupArgs.__new__(InstanceFailoverGroupArgs)

            __props__.__dict__["failover_group_name"] = failover_group_name
            if location_name is None and not opts.urn:
                raise TypeError("Missing required property 'location_name'")
            __props__.__dict__["location_name"] = location_name
            if managed_instance_pairs is None and not opts.urn:
                raise TypeError("Missing required property 'managed_instance_pairs'")
            __props__.__dict__["managed_instance_pairs"] = managed_instance_pairs
            if partner_regions is None and not opts.urn:
                raise TypeError("Missing required property 'partner_regions'")
            __props__.__dict__["partner_regions"] = partner_regions
            __props__.__dict__["read_only_endpoint"] = read_only_endpoint
            if read_write_endpoint is None and not opts.urn:
                raise TypeError("Missing required property 'read_write_endpoint'")
            __props__.__dict__["read_write_endpoint"] = read_write_endpoint
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["replication_role"] = None
            __props__.__dict__["replication_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20171001preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20200202preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20201101preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20210201preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20210501preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20210801preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20211101:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20211101preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20220201preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20220501preview:InstanceFailoverGroup"), pulumi.Alias(type_="azure-native:sql/v20220801preview:InstanceFailoverGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(InstanceFailoverGroup, __self__).__init__(
            'azure-native:sql/v20200801preview:InstanceFailoverGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'InstanceFailoverGroup':
        """
        Get an existing InstanceFailoverGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = InstanceFailoverGroupArgs.__new__(InstanceFailoverGroupArgs)

        __props__.__dict__["managed_instance_pairs"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["partner_regions"] = None
        __props__.__dict__["read_only_endpoint"] = None
        __props__.__dict__["read_write_endpoint"] = None
        __props__.__dict__["replication_role"] = None
        __props__.__dict__["replication_state"] = None
        __props__.__dict__["type"] = None
        return InstanceFailoverGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="managedInstancePairs")
    def managed_instance_pairs(self) -> pulumi.Output[Sequence['outputs.ManagedInstancePairInfoResponse']]:
        """
        List of managed instance pairs in the failover group.
        """
        return pulumi.get(self, "managed_instance_pairs")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partnerRegions")
    def partner_regions(self) -> pulumi.Output[Sequence['outputs.PartnerRegionInfoResponse']]:
        """
        Partner region information for the failover group.
        """
        return pulumi.get(self, "partner_regions")

    @property
    @pulumi.getter(name="readOnlyEndpoint")
    def read_only_endpoint(self) -> pulumi.Output[Optional['outputs.InstanceFailoverGroupReadOnlyEndpointResponse']]:
        """
        Read-only endpoint of the failover group instance.
        """
        return pulumi.get(self, "read_only_endpoint")

    @property
    @pulumi.getter(name="readWriteEndpoint")
    def read_write_endpoint(self) -> pulumi.Output['outputs.InstanceFailoverGroupReadWriteEndpointResponse']:
        """
        Read-write endpoint of the failover group instance.
        """
        return pulumi.get(self, "read_write_endpoint")

    @property
    @pulumi.getter(name="replicationRole")
    def replication_role(self) -> pulumi.Output[str]:
        """
        Local replication role of the failover group instance.
        """
        return pulumi.get(self, "replication_role")

    @property
    @pulumi.getter(name="replicationState")
    def replication_state(self) -> pulumi.Output[str]:
        """
        Replication state of the failover group instance.
        """
        return pulumi.get(self, "replication_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

