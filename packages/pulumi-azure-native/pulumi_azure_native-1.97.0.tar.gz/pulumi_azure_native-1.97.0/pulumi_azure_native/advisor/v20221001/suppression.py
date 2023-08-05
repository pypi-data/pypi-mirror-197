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

__all__ = ['SuppressionArgs', 'Suppression']

@pulumi.input_type
class SuppressionArgs:
    def __init__(__self__, *,
                 recommendation_id: pulumi.Input[str],
                 resource_uri: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 suppression_id: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Suppression resource.
        :param pulumi.Input[str] recommendation_id: The recommendation ID.
        :param pulumi.Input[str] resource_uri: The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
        :param pulumi.Input[str] name: The name of the suppression.
        :param pulumi.Input[str] suppression_id: The GUID of the suppression.
        :param pulumi.Input[str] ttl: The duration for which the suppression is valid.
        """
        pulumi.set(__self__, "recommendation_id", recommendation_id)
        pulumi.set(__self__, "resource_uri", resource_uri)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if suppression_id is not None:
            pulumi.set(__self__, "suppression_id", suppression_id)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter(name="recommendationId")
    def recommendation_id(self) -> pulumi.Input[str]:
        """
        The recommendation ID.
        """
        return pulumi.get(self, "recommendation_id")

    @recommendation_id.setter
    def recommendation_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "recommendation_id", value)

    @property
    @pulumi.getter(name="resourceUri")
    def resource_uri(self) -> pulumi.Input[str]:
        """
        The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
        """
        return pulumi.get(self, "resource_uri")

    @resource_uri.setter
    def resource_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_uri", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the suppression.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="suppressionId")
    def suppression_id(self) -> Optional[pulumi.Input[str]]:
        """
        The GUID of the suppression.
        """
        return pulumi.get(self, "suppression_id")

    @suppression_id.setter
    def suppression_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "suppression_id", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[str]]:
        """
        The duration for which the suppression is valid.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ttl", value)


class Suppression(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recommendation_id: Optional[pulumi.Input[str]] = None,
                 resource_uri: Optional[pulumi.Input[str]] = None,
                 suppression_id: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The details of the snoozed or dismissed rule; for example, the duration, name, and GUID associated with the rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the suppression.
        :param pulumi.Input[str] recommendation_id: The recommendation ID.
        :param pulumi.Input[str] resource_uri: The fully qualified Azure Resource Manager identifier of the resource to which the recommendation applies.
        :param pulumi.Input[str] suppression_id: The GUID of the suppression.
        :param pulumi.Input[str] ttl: The duration for which the suppression is valid.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SuppressionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The details of the snoozed or dismissed rule; for example, the duration, name, and GUID associated with the rule.

        :param str resource_name: The name of the resource.
        :param SuppressionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SuppressionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recommendation_id: Optional[pulumi.Input[str]] = None,
                 resource_uri: Optional[pulumi.Input[str]] = None,
                 suppression_id: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SuppressionArgs.__new__(SuppressionArgs)

            __props__.__dict__["name"] = name
            if recommendation_id is None and not opts.urn:
                raise TypeError("Missing required property 'recommendation_id'")
            __props__.__dict__["recommendation_id"] = recommendation_id
            if resource_uri is None and not opts.urn:
                raise TypeError("Missing required property 'resource_uri'")
            __props__.__dict__["resource_uri"] = resource_uri
            __props__.__dict__["suppression_id"] = suppression_id
            __props__.__dict__["ttl"] = ttl
            __props__.__dict__["expiration_time_stamp"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:advisor:Suppression"), pulumi.Alias(type_="azure-native:advisor/v20160712preview:Suppression"), pulumi.Alias(type_="azure-native:advisor/v20170331:Suppression"), pulumi.Alias(type_="azure-native:advisor/v20170419:Suppression"), pulumi.Alias(type_="azure-native:advisor/v20200101:Suppression"), pulumi.Alias(type_="azure-native:advisor/v20220901:Suppression")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Suppression, __self__).__init__(
            'azure-native:advisor/v20221001:Suppression',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Suppression':
        """
        Get an existing Suppression resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SuppressionArgs.__new__(SuppressionArgs)

        __props__.__dict__["expiration_time_stamp"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["suppression_id"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["ttl"] = None
        __props__.__dict__["type"] = None
        return Suppression(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="expirationTimeStamp")
    def expiration_time_stamp(self) -> pulumi.Output[str]:
        """
        Gets or sets the expiration time stamp.
        """
        return pulumi.get(self, "expiration_time_stamp")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="suppressionId")
    def suppression_id(self) -> pulumi.Output[Optional[str]]:
        """
        The GUID of the suppression.
        """
        return pulumi.get(self, "suppression_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional[str]]:
        """
        The duration for which the suppression is valid.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

