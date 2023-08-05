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

__all__ = ['MediaServiceArgs', 'MediaService']

@pulumi.input_type
class MediaServiceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 account_name: Optional[pulumi.Input[str]] = None,
                 encryption: Optional[pulumi.Input['AccountEncryptionArgs']] = None,
                 identity: Optional[pulumi.Input['MediaServiceIdentityArgs']] = None,
                 key_delivery: Optional[pulumi.Input['KeyDeliveryArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]]] = None,
                 storage_authentication: Optional[pulumi.Input[Union[str, 'StorageAuthentication']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a MediaService resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input['AccountEncryptionArgs'] encryption: The account encryption properties.
        :param pulumi.Input['MediaServiceIdentityArgs'] identity: The Managed Identity for the Media Services account.
        :param pulumi.Input['KeyDeliveryArgs'] key_delivery: The Key Delivery properties for Media Services account.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public network access is allowed for resources under the Media Services account.
        :param pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]] storage_accounts: The storage accounts for this resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if account_name is not None:
            pulumi.set(__self__, "account_name", account_name)
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if key_delivery is not None:
            pulumi.set(__self__, "key_delivery", key_delivery)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)
        if storage_accounts is not None:
            pulumi.set(__self__, "storage_accounts", storage_accounts)
        if storage_authentication is not None:
            pulumi.set(__self__, "storage_authentication", storage_authentication)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the Azure subscription.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Media Services account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter
    def encryption(self) -> Optional[pulumi.Input['AccountEncryptionArgs']]:
        """
        The account encryption properties.
        """
        return pulumi.get(self, "encryption")

    @encryption.setter
    def encryption(self, value: Optional[pulumi.Input['AccountEncryptionArgs']]):
        pulumi.set(self, "encryption", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['MediaServiceIdentityArgs']]:
        """
        The Managed Identity for the Media Services account.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['MediaServiceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="keyDelivery")
    def key_delivery(self) -> Optional[pulumi.Input['KeyDeliveryArgs']]:
        """
        The Key Delivery properties for Media Services account.
        """
        return pulumi.get(self, "key_delivery")

    @key_delivery.setter
    def key_delivery(self, value: Optional[pulumi.Input['KeyDeliveryArgs']]):
        pulumi.set(self, "key_delivery", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]:
        """
        Whether or not public network access is allowed for resources under the Media Services account.
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]):
        pulumi.set(self, "public_network_access", value)

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]]]:
        """
        The storage accounts for this resource.
        """
        return pulumi.get(self, "storage_accounts")

    @storage_accounts.setter
    def storage_accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StorageAccountArgs']]]]):
        pulumi.set(self, "storage_accounts", value)

    @property
    @pulumi.getter(name="storageAuthentication")
    def storage_authentication(self) -> Optional[pulumi.Input[Union[str, 'StorageAuthentication']]]:
        return pulumi.get(self, "storage_authentication")

    @storage_authentication.setter
    def storage_authentication(self, value: Optional[pulumi.Input[Union[str, 'StorageAuthentication']]]):
        pulumi.set(self, "storage_authentication", value)

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


class MediaService(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['AccountEncryptionArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['MediaServiceIdentityArgs']]] = None,
                 key_delivery: Optional[pulumi.Input[pulumi.InputType['KeyDeliveryArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StorageAccountArgs']]]]] = None,
                 storage_authentication: Optional[pulumi.Input[Union[str, 'StorageAuthentication']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A Media Services account.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[pulumi.InputType['AccountEncryptionArgs']] encryption: The account encryption properties.
        :param pulumi.Input[pulumi.InputType['MediaServiceIdentityArgs']] identity: The Managed Identity for the Media Services account.
        :param pulumi.Input[pulumi.InputType['KeyDeliveryArgs']] key_delivery: The Key Delivery properties for Media Services account.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public network access is allowed for resources under the Media Services account.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StorageAccountArgs']]]] storage_accounts: The storage accounts for this resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MediaServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A Media Services account.

        :param str resource_name: The name of the resource.
        :param MediaServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MediaServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 encryption: Optional[pulumi.Input[pulumi.InputType['AccountEncryptionArgs']]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['MediaServiceIdentityArgs']]] = None,
                 key_delivery: Optional[pulumi.Input[pulumi.InputType['KeyDeliveryArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_accounts: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StorageAccountArgs']]]]] = None,
                 storage_authentication: Optional[pulumi.Input[Union[str, 'StorageAuthentication']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MediaServiceArgs.__new__(MediaServiceArgs)

            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["encryption"] = encryption
            __props__.__dict__["identity"] = identity
            __props__.__dict__["key_delivery"] = key_delivery
            __props__.__dict__["location"] = location
            __props__.__dict__["public_network_access"] = public_network_access
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["storage_accounts"] = storage_accounts
            __props__.__dict__["storage_authentication"] = storage_authentication
            __props__.__dict__["tags"] = tags
            __props__.__dict__["media_service_id"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:media:MediaService"), pulumi.Alias(type_="azure-native:media/v20151001:MediaService"), pulumi.Alias(type_="azure-native:media/v20180330preview:MediaService"), pulumi.Alias(type_="azure-native:media/v20180601preview:MediaService"), pulumi.Alias(type_="azure-native:media/v20180701:MediaService"), pulumi.Alias(type_="azure-native:media/v20200501:MediaService"), pulumi.Alias(type_="azure-native:media/v20210501:MediaService"), pulumi.Alias(type_="azure-native:media/v20210601:MediaService"), pulumi.Alias(type_="azure-native:media/v20230101:MediaService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MediaService, __self__).__init__(
            'azure-native:media/v20211101:MediaService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MediaService':
        """
        Get an existing MediaService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MediaServiceArgs.__new__(MediaServiceArgs)

        __props__.__dict__["encryption"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["key_delivery"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["media_service_id"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_network_access"] = None
        __props__.__dict__["storage_accounts"] = None
        __props__.__dict__["storage_authentication"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return MediaService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def encryption(self) -> pulumi.Output[Optional['outputs.AccountEncryptionResponse']]:
        """
        The account encryption properties.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.MediaServiceIdentityResponse']]:
        """
        The Managed Identity for the Media Services account.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="keyDelivery")
    def key_delivery(self) -> pulumi.Output[Optional['outputs.KeyDeliveryResponse']]:
        """
        The Key Delivery properties for Media Services account.
        """
        return pulumi.get(self, "key_delivery")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mediaServiceId")
    def media_service_id(self) -> pulumi.Output[str]:
        """
        The Media Services account ID.
        """
        return pulumi.get(self, "media_service_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        The Private Endpoint Connections created for the Media Service account.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the Media Services account.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not public network access is allowed for resources under the Media Services account.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="storageAccounts")
    def storage_accounts(self) -> pulumi.Output[Optional[Sequence['outputs.StorageAccountResponse']]]:
        """
        The storage accounts for this resource.
        """
        return pulumi.get(self, "storage_accounts")

    @property
    @pulumi.getter(name="storageAuthentication")
    def storage_authentication(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "storage_authentication")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
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

