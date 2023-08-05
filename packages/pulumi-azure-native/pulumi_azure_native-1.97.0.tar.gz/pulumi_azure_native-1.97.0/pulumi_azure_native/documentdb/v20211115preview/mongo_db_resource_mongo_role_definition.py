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

__all__ = ['MongoDBResourceMongoRoleDefinitionArgs', 'MongoDBResourceMongoRoleDefinition']

@pulumi.input_type
class MongoDBResourceMongoRoleDefinitionArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 database_name: Optional[pulumi.Input[str]] = None,
                 mongo_role_definition_id: Optional[pulumi.Input[str]] = None,
                 privileges: Optional[pulumi.Input[Sequence[pulumi.Input['PrivilegeArgs']]]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input['RoleArgs']]]] = None,
                 type: Optional[pulumi.Input['MongoRoleDefinitionType']] = None):
        """
        The set of arguments for constructing a MongoDBResourceMongoRoleDefinition resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] database_name: The database name for which access is being granted for this Role Definition.
        :param pulumi.Input[str] mongo_role_definition_id: The ID for the Role Definition {dbName.roleName}.
        :param pulumi.Input[Sequence[pulumi.Input['PrivilegeArgs']]] privileges: A set of privileges contained by the Role Definition. This will allow application of this Role Definition on the entire database account or any underlying Database / Collection. Scopes higher than Database are not enforceable as privilege.
        :param pulumi.Input[str] role_name: A user-friendly name for the Role Definition. Must be unique for the database account.
        :param pulumi.Input[Sequence[pulumi.Input['RoleArgs']]] roles: The set of roles inherited by this Role Definition.
        :param pulumi.Input['MongoRoleDefinitionType'] type: Indicates whether the Role Definition was built-in or user created.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if mongo_role_definition_id is not None:
            pulumi.set(__self__, "mongo_role_definition_id", mongo_role_definition_id)
        if privileges is not None:
            pulumi.set(__self__, "privileges", privileges)
        if role_name is not None:
            pulumi.set(__self__, "role_name", role_name)
        if roles is not None:
            pulumi.set(__self__, "roles", roles)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        Cosmos DB database account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

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
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        The database name for which access is being granted for this Role Definition.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="mongoRoleDefinitionId")
    def mongo_role_definition_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID for the Role Definition {dbName.roleName}.
        """
        return pulumi.get(self, "mongo_role_definition_id")

    @mongo_role_definition_id.setter
    def mongo_role_definition_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mongo_role_definition_id", value)

    @property
    @pulumi.getter
    def privileges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivilegeArgs']]]]:
        """
        A set of privileges contained by the Role Definition. This will allow application of this Role Definition on the entire database account or any underlying Database / Collection. Scopes higher than Database are not enforceable as privilege.
        """
        return pulumi.get(self, "privileges")

    @privileges.setter
    def privileges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivilegeArgs']]]]):
        pulumi.set(self, "privileges", value)

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> Optional[pulumi.Input[str]]:
        """
        A user-friendly name for the Role Definition. Must be unique for the database account.
        """
        return pulumi.get(self, "role_name")

    @role_name.setter
    def role_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_name", value)

    @property
    @pulumi.getter
    def roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['RoleArgs']]]]:
        """
        The set of roles inherited by this Role Definition.
        """
        return pulumi.get(self, "roles")

    @roles.setter
    def roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['RoleArgs']]]]):
        pulumi.set(self, "roles", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['MongoRoleDefinitionType']]:
        """
        Indicates whether the Role Definition was built-in or user created.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['MongoRoleDefinitionType']]):
        pulumi.set(self, "type", value)


class MongoDBResourceMongoRoleDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 mongo_role_definition_id: Optional[pulumi.Input[str]] = None,
                 privileges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivilegeArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RoleArgs']]]]] = None,
                 type: Optional[pulumi.Input['MongoRoleDefinitionType']] = None,
                 __props__=None):
        """
        An Azure Cosmos DB Mongo Role Definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] database_name: The database name for which access is being granted for this Role Definition.
        :param pulumi.Input[str] mongo_role_definition_id: The ID for the Role Definition {dbName.roleName}.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivilegeArgs']]]] privileges: A set of privileges contained by the Role Definition. This will allow application of this Role Definition on the entire database account or any underlying Database / Collection. Scopes higher than Database are not enforceable as privilege.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] role_name: A user-friendly name for the Role Definition. Must be unique for the database account.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RoleArgs']]]] roles: The set of roles inherited by this Role Definition.
        :param pulumi.Input['MongoRoleDefinitionType'] type: Indicates whether the Role Definition was built-in or user created.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MongoDBResourceMongoRoleDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Azure Cosmos DB Mongo Role Definition.

        :param str resource_name: The name of the resource.
        :param MongoDBResourceMongoRoleDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MongoDBResourceMongoRoleDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 mongo_role_definition_id: Optional[pulumi.Input[str]] = None,
                 privileges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['PrivilegeArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 role_name: Optional[pulumi.Input[str]] = None,
                 roles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['RoleArgs']]]]] = None,
                 type: Optional[pulumi.Input['MongoRoleDefinitionType']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MongoDBResourceMongoRoleDefinitionArgs.__new__(MongoDBResourceMongoRoleDefinitionArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["mongo_role_definition_id"] = mongo_role_definition_id
            __props__.__dict__["privileges"] = privileges
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["role_name"] = role_name
            __props__.__dict__["roles"] = roles
            __props__.__dict__["type"] = type
            __props__.__dict__["name"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:documentdb:MongoDBResourceMongoRoleDefinition"), pulumi.Alias(type_="azure-native:documentdb/v20211015preview:MongoDBResourceMongoRoleDefinition"), pulumi.Alias(type_="azure-native:documentdb/v20220215preview:MongoDBResourceMongoRoleDefinition"), pulumi.Alias(type_="azure-native:documentdb/v20220515preview:MongoDBResourceMongoRoleDefinition"), pulumi.Alias(type_="azure-native:documentdb/v20220815:MongoDBResourceMongoRoleDefinition"), pulumi.Alias(type_="azure-native:documentdb/v20220815preview:MongoDBResourceMongoRoleDefinition"), pulumi.Alias(type_="azure-native:documentdb/v20221115:MongoDBResourceMongoRoleDefinition")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MongoDBResourceMongoRoleDefinition, __self__).__init__(
            'azure-native:documentdb/v20211115preview:MongoDBResourceMongoRoleDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MongoDBResourceMongoRoleDefinition':
        """
        Get an existing MongoDBResourceMongoRoleDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MongoDBResourceMongoRoleDefinitionArgs.__new__(MongoDBResourceMongoRoleDefinitionArgs)

        __props__.__dict__["database_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["privileges"] = None
        __props__.__dict__["role_name"] = None
        __props__.__dict__["roles"] = None
        __props__.__dict__["type"] = None
        return MongoDBResourceMongoRoleDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Output[Optional[str]]:
        """
        The database name for which access is being granted for this Role Definition.
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the database account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def privileges(self) -> pulumi.Output[Optional[Sequence['outputs.PrivilegeResponse']]]:
        """
        A set of privileges contained by the Role Definition. This will allow application of this Role Definition on the entire database account or any underlying Database / Collection. Scopes higher than Database are not enforceable as privilege.
        """
        return pulumi.get(self, "privileges")

    @property
    @pulumi.getter(name="roleName")
    def role_name(self) -> pulumi.Output[Optional[str]]:
        """
        A user-friendly name for the Role Definition. Must be unique for the database account.
        """
        return pulumi.get(self, "role_name")

    @property
    @pulumi.getter
    def roles(self) -> pulumi.Output[Optional[Sequence['outputs.RoleResponse']]]:
        """
        The set of roles inherited by this Role Definition.
        """
        return pulumi.get(self, "roles")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")

