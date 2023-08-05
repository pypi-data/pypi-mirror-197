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

__all__ = ['ConnectionTypeArgs', 'ConnectionType']

@pulumi.input_type
class ConnectionTypeArgs:
    def __init__(__self__, *,
                 automation_account_name: pulumi.Input[str],
                 field_definitions: pulumi.Input[Mapping[str, pulumi.Input['FieldDefinitionArgs']]],
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 connection_type_name: Optional[pulumi.Input[str]] = None,
                 is_global: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a ConnectionType resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[Mapping[str, pulumi.Input['FieldDefinitionArgs']]] field_definitions: Gets or sets the field definitions of the connection type.
        :param pulumi.Input[str] name: Gets or sets the name of the connection type.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[str] connection_type_name: The parameters supplied to the create or update connection type operation.
        :param pulumi.Input[bool] is_global: Gets or sets a Boolean value to indicate if the connection type is global.
        """
        pulumi.set(__self__, "automation_account_name", automation_account_name)
        pulumi.set(__self__, "field_definitions", field_definitions)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if connection_type_name is not None:
            pulumi.set(__self__, "connection_type_name", connection_type_name)
        if is_global is not None:
            pulumi.set(__self__, "is_global", is_global)

    @property
    @pulumi.getter(name="automationAccountName")
    def automation_account_name(self) -> pulumi.Input[str]:
        """
        The name of the automation account.
        """
        return pulumi.get(self, "automation_account_name")

    @automation_account_name.setter
    def automation_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "automation_account_name", value)

    @property
    @pulumi.getter(name="fieldDefinitions")
    def field_definitions(self) -> pulumi.Input[Mapping[str, pulumi.Input['FieldDefinitionArgs']]]:
        """
        Gets or sets the field definitions of the connection type.
        """
        return pulumi.get(self, "field_definitions")

    @field_definitions.setter
    def field_definitions(self, value: pulumi.Input[Mapping[str, pulumi.Input['FieldDefinitionArgs']]]):
        pulumi.set(self, "field_definitions", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Gets or sets the name of the connection type.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of an Azure Resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="connectionTypeName")
    def connection_type_name(self) -> Optional[pulumi.Input[str]]:
        """
        The parameters supplied to the create or update connection type operation.
        """
        return pulumi.get(self, "connection_type_name")

    @connection_type_name.setter
    def connection_type_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_type_name", value)

    @property
    @pulumi.getter(name="isGlobal")
    def is_global(self) -> Optional[pulumi.Input[bool]]:
        """
        Gets or sets a Boolean value to indicate if the connection type is global.
        """
        return pulumi.get(self, "is_global")

    @is_global.setter
    def is_global(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_global", value)


class ConnectionType(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 connection_type_name: Optional[pulumi.Input[str]] = None,
                 field_definitions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['FieldDefinitionArgs']]]]] = None,
                 is_global: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Definition of the connection type.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] connection_type_name: The parameters supplied to the create or update connection type operation.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['FieldDefinitionArgs']]]] field_definitions: Gets or sets the field definitions of the connection type.
        :param pulumi.Input[bool] is_global: Gets or sets a Boolean value to indicate if the connection type is global.
        :param pulumi.Input[str] name: Gets or sets the name of the connection type.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectionTypeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Definition of the connection type.

        :param str resource_name: The name of the resource.
        :param ConnectionTypeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectionTypeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 connection_type_name: Optional[pulumi.Input[str]] = None,
                 field_definitions: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['FieldDefinitionArgs']]]]] = None,
                 is_global: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectionTypeArgs.__new__(ConnectionTypeArgs)

            if automation_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_name'")
            __props__.__dict__["automation_account_name"] = automation_account_name
            __props__.__dict__["connection_type_name"] = connection_type_name
            if field_definitions is None and not opts.urn:
                raise TypeError("Missing required property 'field_definitions'")
            __props__.__dict__["field_definitions"] = field_definitions
            __props__.__dict__["is_global"] = is_global
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["description"] = None
            __props__.__dict__["last_modified_time"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:automation:ConnectionType"), pulumi.Alias(type_="azure-native:automation/v20190601:ConnectionType"), pulumi.Alias(type_="azure-native:automation/v20200113preview:ConnectionType"), pulumi.Alias(type_="azure-native:automation/v20220808:ConnectionType")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ConnectionType, __self__).__init__(
            'azure-native:automation/v20151031:ConnectionType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConnectionType':
        """
        Get an existing ConnectionType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConnectionTypeArgs.__new__(ConnectionTypeArgs)

        __props__.__dict__["creation_time"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["field_definitions"] = None
        __props__.__dict__["is_global"] = None
        __props__.__dict__["last_modified_time"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return ConnectionType(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        Gets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="fieldDefinitions")
    def field_definitions(self) -> pulumi.Output[Mapping[str, 'outputs.FieldDefinitionResponse']]:
        """
        Gets the field definitions of the connection type.
        """
        return pulumi.get(self, "field_definitions")

    @property
    @pulumi.getter(name="isGlobal")
    def is_global(self) -> pulumi.Output[Optional[bool]]:
        """
        Gets or sets a Boolean value to indicate if the connection type is global.
        """
        return pulumi.get(self, "is_global")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Gets the name of the connection type.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

