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

__all__ = ['ClusterArgs', 'Cluster']

@pulumi.input_type
class ClusterArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['ClusterSkuArgs']] = None,
                 supports_scaling: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Cluster resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[str] cluster_name: The name of the Event Hubs Cluster.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input['ClusterSkuArgs'] sku: Properties of the cluster SKU.
        :param pulumi.Input[bool] supports_scaling: A value that indicates whether Scaling is Supported.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if supports_scaling is not None:
            pulumi.set(__self__, "supports_scaling", supports_scaling)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group within the azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Event Hubs Cluster.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

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
    def sku(self) -> Optional[pulumi.Input['ClusterSkuArgs']]:
        """
        Properties of the cluster SKU.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['ClusterSkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="supportsScaling")
    def supports_scaling(self) -> Optional[pulumi.Input[bool]]:
        """
        A value that indicates whether Scaling is Supported.
        """
        return pulumi.get(self, "supports_scaling")

    @supports_scaling.setter
    def supports_scaling(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "supports_scaling", value)

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


class Cluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ClusterSkuArgs']]] = None,
                 supports_scaling: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Single Event Hubs Cluster resource in List or Get operations.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: The name of the Event Hubs Cluster.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: Name of the resource group within the azure subscription.
        :param pulumi.Input[pulumi.InputType['ClusterSkuArgs']] sku: Properties of the cluster SKU.
        :param pulumi.Input[bool] supports_scaling: A value that indicates whether Scaling is Supported.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Single Event Hubs Cluster resource in List or Get operations.

        :param str resource_name: The name of the resource.
        :param ClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['ClusterSkuArgs']]] = None,
                 supports_scaling: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterArgs.__new__(ClusterArgs)

            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["supports_scaling"] = supports_scaling
            __props__.__dict__["tags"] = tags
            __props__.__dict__["created_at"] = None
            __props__.__dict__["metric_id"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["updated_at"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:eventhub:Cluster"), pulumi.Alias(type_="azure-native:eventhub/v20180101preview:Cluster"), pulumi.Alias(type_="azure-native:eventhub/v20210601preview:Cluster"), pulumi.Alias(type_="azure-native:eventhub/v20211101:Cluster"), pulumi.Alias(type_="azure-native:eventhub/v20221001preview:Cluster")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Cluster, __self__).__init__(
            'azure-native:eventhub/v20220101preview:Cluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Cluster':
        """
        Get an existing Cluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ClusterArgs.__new__(ClusterArgs)

        __props__.__dict__["created_at"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["metric_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["supports_scaling"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["updated_at"] = None
        return Cluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The UTC time when the Event Hubs Cluster was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="metricId")
    def metric_id(self) -> pulumi.Output[str]:
        """
        The metric ID of the cluster resource. Provided by the service and not modifiable by the user.
        """
        return pulumi.get(self, "metric_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.ClusterSkuResponse']]:
        """
        Properties of the cluster SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the Cluster resource
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="supportsScaling")
    def supports_scaling(self) -> pulumi.Output[Optional[bool]]:
        """
        A value that indicates whether Scaling is Supported.
        """
        return pulumi.get(self, "supports_scaling")

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

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The UTC time when the Event Hubs Cluster was last updated.
        """
        return pulumi.get(self, "updated_at")

