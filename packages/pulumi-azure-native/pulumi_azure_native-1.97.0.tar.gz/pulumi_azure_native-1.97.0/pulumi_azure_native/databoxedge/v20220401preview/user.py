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

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 device_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 user_type: pulumi.Input[Union[str, 'UserType']],
                 encrypted_password: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'UserType']] user_type: Type of the user.
        :param pulumi.Input['AsymmetricEncryptedSecretArgs'] encrypted_password: The password details.
        :param pulumi.Input[str] name: The user name.
        """
        pulumi.set(__self__, "device_name", device_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "user_type", user_type)
        if encrypted_password is not None:
            pulumi.set(__self__, "encrypted_password", encrypted_password)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="deviceName")
    def device_name(self) -> pulumi.Input[str]:
        """
        The device name.
        """
        return pulumi.get(self, "device_name")

    @device_name.setter
    def device_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="userType")
    def user_type(self) -> pulumi.Input[Union[str, 'UserType']]:
        """
        Type of the user.
        """
        return pulumi.get(self, "user_type")

    @user_type.setter
    def user_type(self, value: pulumi.Input[Union[str, 'UserType']]):
        pulumi.set(self, "user_type", value)

    @property
    @pulumi.getter(name="encryptedPassword")
    def encrypted_password(self) -> Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]:
        """
        The password details.
        """
        return pulumi.get(self, "encrypted_password")

    @encrypted_password.setter
    def encrypted_password(self, value: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]):
        pulumi.set(self, "encrypted_password", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The user name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 encrypted_password: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 user_type: Optional[pulumi.Input[Union[str, 'UserType']]] = None,
                 __props__=None):
        """
        Represents a user who has access to one or more shares on the Data Box Edge/Gateway device.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']] encrypted_password: The password details.
        :param pulumi.Input[str] name: The user name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'UserType']] user_type: Type of the user.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a user who has access to one or more shares on the Data Box Edge/Gateway device.

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 encrypted_password: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 user_type: Optional[pulumi.Input[Union[str, 'UserType']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)

            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__.__dict__["device_name"] = device_name
            __props__.__dict__["encrypted_password"] = encrypted_password
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if user_type is None and not opts.urn:
                raise TypeError("Missing required property 'user_type'")
            __props__.__dict__["user_type"] = user_type
            __props__.__dict__["share_access_rights"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:databoxedge:User"), pulumi.Alias(type_="azure-native:databoxedge/v20190301:User"), pulumi.Alias(type_="azure-native:databoxedge/v20190701:User"), pulumi.Alias(type_="azure-native:databoxedge/v20190801:User"), pulumi.Alias(type_="azure-native:databoxedge/v20200501preview:User"), pulumi.Alias(type_="azure-native:databoxedge/v20200901:User"), pulumi.Alias(type_="azure-native:databoxedge/v20200901preview:User"), pulumi.Alias(type_="azure-native:databoxedge/v20201201:User"), pulumi.Alias(type_="azure-native:databoxedge/v20210201:User"), pulumi.Alias(type_="azure-native:databoxedge/v20210201preview:User"), pulumi.Alias(type_="azure-native:databoxedge/v20210601:User"), pulumi.Alias(type_="azure-native:databoxedge/v20210601preview:User"), pulumi.Alias(type_="azure-native:databoxedge/v20220301:User"), pulumi.Alias(type_="azure-native:databoxedge/v20221201preview:User"), pulumi.Alias(type_="azure-native:databoxedge/v20230101preview:User")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(User, __self__).__init__(
            'azure-native:databoxedge/v20220401preview:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = UserArgs.__new__(UserArgs)

        __props__.__dict__["encrypted_password"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["share_access_rights"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["user_type"] = None
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="encryptedPassword")
    def encrypted_password(self) -> pulumi.Output[Optional['outputs.AsymmetricEncryptedSecretResponse']]:
        """
        The password details.
        """
        return pulumi.get(self, "encrypted_password")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="shareAccessRights")
    def share_access_rights(self) -> pulumi.Output[Sequence['outputs.ShareAccessRightResponse']]:
        """
        List of shares that the user has rights on. This field should not be specified during user creation.
        """
        return pulumi.get(self, "share_access_rights")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of User
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userType")
    def user_type(self) -> pulumi.Output[str]:
        """
        Type of the user.
        """
        return pulumi.get(self, "user_type")

