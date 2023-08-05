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

__all__ = ['VariableArgs', 'Variable']

@pulumi.input_type
class VariableArgs:
    def __init__(__self__, *,
                 columns: pulumi.Input[Sequence[pulumi.Input['PolicyVariableColumnArgs']]],
                 variable_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Variable resource.
        :param pulumi.Input[Sequence[pulumi.Input['PolicyVariableColumnArgs']]] columns: Variable column definitions.
        :param pulumi.Input[str] variable_name: The name of the variable to operate on.
        """
        pulumi.set(__self__, "columns", columns)
        if variable_name is not None:
            pulumi.set(__self__, "variable_name", variable_name)

    @property
    @pulumi.getter
    def columns(self) -> pulumi.Input[Sequence[pulumi.Input['PolicyVariableColumnArgs']]]:
        """
        Variable column definitions.
        """
        return pulumi.get(self, "columns")

    @columns.setter
    def columns(self, value: pulumi.Input[Sequence[pulumi.Input['PolicyVariableColumnArgs']]]):
        pulumi.set(self, "columns", value)

    @property
    @pulumi.getter(name="variableName")
    def variable_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the variable to operate on.
        """
        return pulumi.get(self, "variable_name")

    @variable_name.setter
    def variable_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "variable_name", value)


class Variable(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 columns: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyVariableColumnArgs']]]]] = None,
                 variable_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The variable.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyVariableColumnArgs']]]] columns: Variable column definitions.
        :param pulumi.Input[str] variable_name: The name of the variable to operate on.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VariableArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The variable.

        :param str resource_name: The name of the resource.
        :param VariableArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VariableArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 columns: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PolicyVariableColumnArgs']]]]] = None,
                 variable_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VariableArgs.__new__(VariableArgs)

            if columns is None and not opts.urn:
                raise TypeError("Missing required property 'columns'")
            __props__.__dict__["columns"] = columns
            __props__.__dict__["variable_name"] = variable_name
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        super(Variable, __self__).__init__(
            'azure-native:authorization/v20220801preview:Variable',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Variable':
        """
        Get an existing Variable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VariableArgs.__new__(VariableArgs)

        __props__.__dict__["columns"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return Variable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def columns(self) -> pulumi.Output[Sequence['outputs.PolicyVariableColumnResponse']]:
        """
        Variable column definitions.
        """
        return pulumi.get(self, "columns")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the variable.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource (Microsoft.Authorization/variables).
        """
        return pulumi.get(self, "type")

