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

__all__ = ['HybridUseBenefitArgs', 'HybridUseBenefit']

@pulumi.input_type
class HybridUseBenefitArgs:
    def __init__(__self__, *,
                 scope: pulumi.Input[str],
                 sku: pulumi.Input['SkuArgs'],
                 plan_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a HybridUseBenefit resource.
        :param pulumi.Input[str] scope: The scope at which the operation is performed. This is limited to Microsoft.Compute/virtualMachines and Microsoft.Compute/hostGroups/hosts for now
        :param pulumi.Input['SkuArgs'] sku: Hybrid use benefit SKU
        :param pulumi.Input[str] plan_id: This is a unique identifier for a plan. Should be a guid.
        """
        pulumi.set(__self__, "scope", scope)
        pulumi.set(__self__, "sku", sku)
        if plan_id is not None:
            pulumi.set(__self__, "plan_id", plan_id)

    @property
    @pulumi.getter
    def scope(self) -> pulumi.Input[str]:
        """
        The scope at which the operation is performed. This is limited to Microsoft.Compute/virtualMachines and Microsoft.Compute/hostGroups/hosts for now
        """
        return pulumi.get(self, "scope")

    @scope.setter
    def scope(self, value: pulumi.Input[str]):
        pulumi.set(self, "scope", value)

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        Hybrid use benefit SKU
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> Optional[pulumi.Input[str]]:
        """
        This is a unique identifier for a plan. Should be a guid.
        """
        return pulumi.get(self, "plan_id")

    @plan_id.setter
    def plan_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "plan_id", value)


class HybridUseBenefit(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 __props__=None):
        """
        Response on GET of a hybrid use benefit

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] plan_id: This is a unique identifier for a plan. Should be a guid.
        :param pulumi.Input[str] scope: The scope at which the operation is performed. This is limited to Microsoft.Compute/virtualMachines and Microsoft.Compute/hostGroups/hosts for now
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Hybrid use benefit SKU
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HybridUseBenefitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Response on GET of a hybrid use benefit

        :param str resource_name: The name of the resource.
        :param HybridUseBenefitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HybridUseBenefitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 plan_id: Optional[pulumi.Input[str]] = None,
                 scope: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HybridUseBenefitArgs.__new__(HybridUseBenefitArgs)

            __props__.__dict__["plan_id"] = plan_id
            if scope is None and not opts.urn:
                raise TypeError("Missing required property 'scope'")
            __props__.__dict__["scope"] = scope
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["created_date"] = None
            __props__.__dict__["etag"] = None
            __props__.__dict__["last_updated_date"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:softwareplan:HybridUseBenefit"), pulumi.Alias(type_="azure-native:softwareplan/v20190601preview:HybridUseBenefit")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(HybridUseBenefit, __self__).__init__(
            'azure-native:softwareplan/v20191201:HybridUseBenefit',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'HybridUseBenefit':
        """
        Get an existing HybridUseBenefit resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = HybridUseBenefitArgs.__new__(HybridUseBenefitArgs)

        __props__.__dict__["created_date"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["last_updated_date"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["type"] = None
        return HybridUseBenefit(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        Created date
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[int]:
        """
        Indicates the revision of the hybrid use benefit
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> pulumi.Output[str]:
        """
        Last updated date
        """
        return pulumi.get(self, "last_updated_date")

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
        Provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        Hybrid use benefit SKU
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

