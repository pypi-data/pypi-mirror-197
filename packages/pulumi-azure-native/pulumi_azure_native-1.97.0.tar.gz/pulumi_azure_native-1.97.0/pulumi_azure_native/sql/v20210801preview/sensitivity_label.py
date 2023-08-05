# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['SensitivityLabelArgs', 'SensitivityLabel']

@pulumi.input_type
class SensitivityLabelArgs:
    def __init__(__self__, *,
                 column_name: pulumi.Input[str],
                 database_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 schema_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 table_name: pulumi.Input[str],
                 information_type: Optional[pulumi.Input[str]] = None,
                 information_type_id: Optional[pulumi.Input[str]] = None,
                 label_id: Optional[pulumi.Input[str]] = None,
                 label_name: Optional[pulumi.Input[str]] = None,
                 rank: Optional[pulumi.Input['SensitivityLabelRank']] = None,
                 sensitivity_label_source: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SensitivityLabel resource.
        :param pulumi.Input[str] column_name: The name of the column.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] schema_name: The name of the schema.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] table_name: The name of the table.
        :param pulumi.Input[str] information_type: The information type.
        :param pulumi.Input[str] information_type_id: The information type ID.
        :param pulumi.Input[str] label_id: The label ID.
        :param pulumi.Input[str] label_name: The label name.
        :param pulumi.Input[str] sensitivity_label_source: The source of the sensitivity label.
        """
        pulumi.set(__self__, "column_name", column_name)
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "schema_name", schema_name)
        pulumi.set(__self__, "server_name", server_name)
        pulumi.set(__self__, "table_name", table_name)
        if information_type is not None:
            pulumi.set(__self__, "information_type", information_type)
        if information_type_id is not None:
            pulumi.set(__self__, "information_type_id", information_type_id)
        if label_id is not None:
            pulumi.set(__self__, "label_id", label_id)
        if label_name is not None:
            pulumi.set(__self__, "label_name", label_name)
        if rank is not None:
            pulumi.set(__self__, "rank", rank)
        if sensitivity_label_source is not None:
            pulumi.set(__self__, "sensitivity_label_source", sensitivity_label_source)

    @property
    @pulumi.getter(name="columnName")
    def column_name(self) -> pulumi.Input[str]:
        """
        The name of the column.
        """
        return pulumi.get(self, "column_name")

    @column_name.setter
    def column_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "column_name", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Input[str]:
        """
        The name of the database.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_name", value)

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
    @pulumi.getter(name="schemaName")
    def schema_name(self) -> pulumi.Input[str]:
        """
        The name of the schema.
        """
        return pulumi.get(self, "schema_name")

    @schema_name.setter
    def schema_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "schema_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Input[str]:
        """
        The name of the table.
        """
        return pulumi.get(self, "table_name")

    @table_name.setter
    def table_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "table_name", value)

    @property
    @pulumi.getter(name="informationType")
    def information_type(self) -> Optional[pulumi.Input[str]]:
        """
        The information type.
        """
        return pulumi.get(self, "information_type")

    @information_type.setter
    def information_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "information_type", value)

    @property
    @pulumi.getter(name="informationTypeId")
    def information_type_id(self) -> Optional[pulumi.Input[str]]:
        """
        The information type ID.
        """
        return pulumi.get(self, "information_type_id")

    @information_type_id.setter
    def information_type_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "information_type_id", value)

    @property
    @pulumi.getter(name="labelId")
    def label_id(self) -> Optional[pulumi.Input[str]]:
        """
        The label ID.
        """
        return pulumi.get(self, "label_id")

    @label_id.setter
    def label_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label_id", value)

    @property
    @pulumi.getter(name="labelName")
    def label_name(self) -> Optional[pulumi.Input[str]]:
        """
        The label name.
        """
        return pulumi.get(self, "label_name")

    @label_name.setter
    def label_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "label_name", value)

    @property
    @pulumi.getter
    def rank(self) -> Optional[pulumi.Input['SensitivityLabelRank']]:
        return pulumi.get(self, "rank")

    @rank.setter
    def rank(self, value: Optional[pulumi.Input['SensitivityLabelRank']]):
        pulumi.set(self, "rank", value)

    @property
    @pulumi.getter(name="sensitivityLabelSource")
    def sensitivity_label_source(self) -> Optional[pulumi.Input[str]]:
        """
        The source of the sensitivity label.
        """
        return pulumi.get(self, "sensitivity_label_source")

    @sensitivity_label_source.setter
    def sensitivity_label_source(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sensitivity_label_source", value)


class SensitivityLabel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 column_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 information_type: Optional[pulumi.Input[str]] = None,
                 information_type_id: Optional[pulumi.Input[str]] = None,
                 label_id: Optional[pulumi.Input[str]] = None,
                 label_name: Optional[pulumi.Input[str]] = None,
                 rank: Optional[pulumi.Input['SensitivityLabelRank']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_name: Optional[pulumi.Input[str]] = None,
                 sensitivity_label_source: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A sensitivity label.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] column_name: The name of the column.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] information_type: The information type.
        :param pulumi.Input[str] information_type_id: The information type ID.
        :param pulumi.Input[str] label_id: The label ID.
        :param pulumi.Input[str] label_name: The label name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] schema_name: The name of the schema.
        :param pulumi.Input[str] sensitivity_label_source: The source of the sensitivity label.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] table_name: The name of the table.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SensitivityLabelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A sensitivity label.

        :param str resource_name: The name of the resource.
        :param SensitivityLabelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SensitivityLabelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 column_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 information_type: Optional[pulumi.Input[str]] = None,
                 information_type_id: Optional[pulumi.Input[str]] = None,
                 label_id: Optional[pulumi.Input[str]] = None,
                 label_name: Optional[pulumi.Input[str]] = None,
                 rank: Optional[pulumi.Input['SensitivityLabelRank']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schema_name: Optional[pulumi.Input[str]] = None,
                 sensitivity_label_source: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SensitivityLabelArgs.__new__(SensitivityLabelArgs)

            if column_name is None and not opts.urn:
                raise TypeError("Missing required property 'column_name'")
            __props__.__dict__["column_name"] = column_name
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["information_type"] = information_type
            __props__.__dict__["information_type_id"] = information_type_id
            __props__.__dict__["label_id"] = label_id
            __props__.__dict__["label_name"] = label_name
            __props__.__dict__["rank"] = rank
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if schema_name is None and not opts.urn:
                raise TypeError("Missing required property 'schema_name'")
            __props__.__dict__["schema_name"] = schema_name
            __props__.__dict__["sensitivity_label_source"] = sensitivity_label_source
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            if table_name is None and not opts.urn:
                raise TypeError("Missing required property 'table_name'")
            __props__.__dict__["table_name"] = table_name
            __props__.__dict__["is_disabled"] = None
            __props__.__dict__["managed_by"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20170301preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20200202preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20200801preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20201101preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20210201preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20210501preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20211101:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20211101preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20220201preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20220501preview:SensitivityLabel"), pulumi.Alias(type_="azure-native:sql/v20220801preview:SensitivityLabel")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SensitivityLabel, __self__).__init__(
            'azure-native:sql/v20210801preview:SensitivityLabel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SensitivityLabel':
        """
        Get an existing SensitivityLabel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SensitivityLabelArgs.__new__(SensitivityLabelArgs)

        __props__.__dict__["column_name"] = None
        __props__.__dict__["information_type"] = None
        __props__.__dict__["information_type_id"] = None
        __props__.__dict__["is_disabled"] = None
        __props__.__dict__["label_id"] = None
        __props__.__dict__["label_name"] = None
        __props__.__dict__["managed_by"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["rank"] = None
        __props__.__dict__["schema_name"] = None
        __props__.__dict__["table_name"] = None
        __props__.__dict__["type"] = None
        return SensitivityLabel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="columnName")
    def column_name(self) -> pulumi.Output[str]:
        """
        The column name.
        """
        return pulumi.get(self, "column_name")

    @property
    @pulumi.getter(name="informationType")
    def information_type(self) -> pulumi.Output[Optional[str]]:
        """
        The information type.
        """
        return pulumi.get(self, "information_type")

    @property
    @pulumi.getter(name="informationTypeId")
    def information_type_id(self) -> pulumi.Output[Optional[str]]:
        """
        The information type ID.
        """
        return pulumi.get(self, "information_type_id")

    @property
    @pulumi.getter(name="isDisabled")
    def is_disabled(self) -> pulumi.Output[bool]:
        """
        Is sensitivity recommendation disabled. Applicable for recommended sensitivity label only. Specifies whether the sensitivity recommendation on this column is disabled (dismissed) or not.
        """
        return pulumi.get(self, "is_disabled")

    @property
    @pulumi.getter(name="labelId")
    def label_id(self) -> pulumi.Output[Optional[str]]:
        """
        The label ID.
        """
        return pulumi.get(self, "label_id")

    @property
    @pulumi.getter(name="labelName")
    def label_name(self) -> pulumi.Output[Optional[str]]:
        """
        The label name.
        """
        return pulumi.get(self, "label_name")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> pulumi.Output[str]:
        """
        Resource that manages the sensitivity label.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rank(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "rank")

    @property
    @pulumi.getter(name="schemaName")
    def schema_name(self) -> pulumi.Output[str]:
        """
        The schema name.
        """
        return pulumi.get(self, "schema_name")

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Output[str]:
        """
        The table name.
        """
        return pulumi.get(self, "table_name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

