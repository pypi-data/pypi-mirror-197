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

__all__ = ['ReplicationRecoveryPlanArgs', 'ReplicationRecoveryPlan']

@pulumi.input_type
class ReplicationRecoveryPlanArgs:
    def __init__(__self__, *,
                 properties: pulumi.Input['CreateRecoveryPlanInputPropertiesArgs'],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 recovery_plan_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ReplicationRecoveryPlan resource.
        :param pulumi.Input['CreateRecoveryPlanInputPropertiesArgs'] properties: Recovery plan creation properties.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name: The name of the recovery services vault.
        :param pulumi.Input[str] recovery_plan_name: Recovery plan name.
        """
        pulumi.set(__self__, "properties", properties)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if recovery_plan_name is not None:
            pulumi.set(__self__, "recovery_plan_name", recovery_plan_name)

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Input['CreateRecoveryPlanInputPropertiesArgs']:
        """
        Recovery plan creation properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: pulumi.Input['CreateRecoveryPlanInputPropertiesArgs']):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the recovery services vault is present.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the recovery services vault.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter(name="recoveryPlanName")
    def recovery_plan_name(self) -> Optional[pulumi.Input[str]]:
        """
        Recovery plan name.
        """
        return pulumi.get(self, "recovery_plan_name")

    @recovery_plan_name.setter
    def recovery_plan_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "recovery_plan_name", value)


class ReplicationRecoveryPlan(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CreateRecoveryPlanInputPropertiesArgs']]] = None,
                 recovery_plan_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Recovery plan details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['CreateRecoveryPlanInputPropertiesArgs']] properties: Recovery plan creation properties.
        :param pulumi.Input[str] recovery_plan_name: Recovery plan name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name_: The name of the recovery services vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationRecoveryPlanArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Recovery plan details.

        :param str resource_name: The name of the resource.
        :param ReplicationRecoveryPlanArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationRecoveryPlanArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CreateRecoveryPlanInputPropertiesArgs']]] = None,
                 recovery_plan_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationRecoveryPlanArgs.__new__(ReplicationRecoveryPlanArgs)

            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__.__dict__["properties"] = properties
            __props__.__dict__["recovery_plan_name"] = recovery_plan_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20160810:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20180110:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20180710:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20210210:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20210601:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20210701:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20211101:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220101:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220201:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220301:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220401:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220501:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220801:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20220910:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20221001:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20230101:ReplicationRecoveryPlan"), pulumi.Alias(type_="azure-native:recoveryservices/v20230201:ReplicationRecoveryPlan")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ReplicationRecoveryPlan, __self__).__init__(
            'azure-native:recoveryservices/v20211001:ReplicationRecoveryPlan',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ReplicationRecoveryPlan':
        """
        Get an existing ReplicationRecoveryPlan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ReplicationRecoveryPlanArgs.__new__(ReplicationRecoveryPlanArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return ReplicationRecoveryPlan(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.RecoveryPlanPropertiesResponse']:
        """
        The custom details.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource Type
        """
        return pulumi.get(self, "type")

