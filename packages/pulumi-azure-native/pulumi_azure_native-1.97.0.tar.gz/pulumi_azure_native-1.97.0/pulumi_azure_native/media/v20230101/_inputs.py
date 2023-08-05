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

__all__ = [
    'AccessControlArgs',
    'AccountEncryptionArgs',
    'KeyDeliveryArgs',
    'KeyVaultPropertiesArgs',
    'MediaServiceIdentityArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'ResourceIdentityArgs',
    'StorageAccountArgs',
]

@pulumi.input_type
class AccessControlArgs:
    def __init__(__self__, *,
                 default_action: Optional[pulumi.Input[Union[str, 'DefaultAction']]] = None,
                 ip_allow_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Union[str, 'DefaultAction']] default_action: The behavior for IP access control in Key Delivery.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] ip_allow_list: The IP allow list for access control in Key Delivery. If the default action is set to 'Allow', the IP allow list must be empty.
        """
        if default_action is not None:
            pulumi.set(__self__, "default_action", default_action)
        if ip_allow_list is not None:
            pulumi.set(__self__, "ip_allow_list", ip_allow_list)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> Optional[pulumi.Input[Union[str, 'DefaultAction']]]:
        """
        The behavior for IP access control in Key Delivery.
        """
        return pulumi.get(self, "default_action")

    @default_action.setter
    def default_action(self, value: Optional[pulumi.Input[Union[str, 'DefaultAction']]]):
        pulumi.set(self, "default_action", value)

    @property
    @pulumi.getter(name="ipAllowList")
    def ip_allow_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IP allow list for access control in Key Delivery. If the default action is set to 'Allow', the IP allow list must be empty.
        """
        return pulumi.get(self, "ip_allow_list")

    @ip_allow_list.setter
    def ip_allow_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_allow_list", value)


@pulumi.input_type
class AccountEncryptionArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[Union[str, 'AccountEncryptionKeyType']],
                 identity: Optional[pulumi.Input['ResourceIdentityArgs']] = None,
                 key_vault_properties: Optional[pulumi.Input['KeyVaultPropertiesArgs']] = None):
        """
        :param pulumi.Input[Union[str, 'AccountEncryptionKeyType']] type: The type of key used to encrypt the Account Key.
        :param pulumi.Input['ResourceIdentityArgs'] identity: The Key Vault identity.
        :param pulumi.Input['KeyVaultPropertiesArgs'] key_vault_properties: The properties of the key used to encrypt the account.
        """
        pulumi.set(__self__, "type", type)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'AccountEncryptionKeyType']]:
        """
        The type of key used to encrypt the Account Key.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'AccountEncryptionKeyType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ResourceIdentityArgs']]:
        """
        The Key Vault identity.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ResourceIdentityArgs']]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional[pulumi.Input['KeyVaultPropertiesArgs']]:
        """
        The properties of the key used to encrypt the account.
        """
        return pulumi.get(self, "key_vault_properties")

    @key_vault_properties.setter
    def key_vault_properties(self, value: Optional[pulumi.Input['KeyVaultPropertiesArgs']]):
        pulumi.set(self, "key_vault_properties", value)


@pulumi.input_type
class KeyDeliveryArgs:
    def __init__(__self__, *,
                 access_control: Optional[pulumi.Input['AccessControlArgs']] = None):
        """
        :param pulumi.Input['AccessControlArgs'] access_control: The access control properties for Key Delivery.
        """
        if access_control is not None:
            pulumi.set(__self__, "access_control", access_control)

    @property
    @pulumi.getter(name="accessControl")
    def access_control(self) -> Optional[pulumi.Input['AccessControlArgs']]:
        """
        The access control properties for Key Delivery.
        """
        return pulumi.get(self, "access_control")

    @access_control.setter
    def access_control(self, value: Optional[pulumi.Input['AccessControlArgs']]):
        pulumi.set(self, "access_control", value)


@pulumi.input_type
class KeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 key_identifier: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] key_identifier: The URL of the Key Vault key used to encrypt the account. The key may either be versioned (for example https://vault/keys/mykey/version1) or reference a key without a version (for example https://vault/keys/mykey).
        """
        if key_identifier is not None:
            pulumi.set(__self__, "key_identifier", key_identifier)

    @property
    @pulumi.getter(name="keyIdentifier")
    def key_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The URL of the Key Vault key used to encrypt the account. The key may either be versioned (for example https://vault/keys/mykey/version1) or reference a key without a version (for example https://vault/keys/mykey).
        """
        return pulumi.get(self, "key_identifier")

    @key_identifier.setter
    def key_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_identifier", value)


@pulumi.input_type
class MediaServiceIdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        :param pulumi.Input[str] type: The identity type.
        :param pulumi.Input[Mapping[str, Any]] user_assigned_identities: The user assigned managed identities.
        """
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The user assigned managed identities.
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ResourceIdentityArgs:
    def __init__(__self__, *,
                 use_system_assigned_identity: pulumi.Input[bool],
                 user_assigned_identity: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[bool] use_system_assigned_identity: Indicates whether to use System Assigned Managed Identity. Mutual exclusive with User Assigned Managed Identity.
        :param pulumi.Input[str] user_assigned_identity: The user assigned managed identity's ARM ID to use when accessing a resource.
        """
        pulumi.set(__self__, "use_system_assigned_identity", use_system_assigned_identity)
        if user_assigned_identity is not None:
            pulumi.set(__self__, "user_assigned_identity", user_assigned_identity)

    @property
    @pulumi.getter(name="useSystemAssignedIdentity")
    def use_system_assigned_identity(self) -> pulumi.Input[bool]:
        """
        Indicates whether to use System Assigned Managed Identity. Mutual exclusive with User Assigned Managed Identity.
        """
        return pulumi.get(self, "use_system_assigned_identity")

    @use_system_assigned_identity.setter
    def use_system_assigned_identity(self, value: pulumi.Input[bool]):
        pulumi.set(self, "use_system_assigned_identity", value)

    @property
    @pulumi.getter(name="userAssignedIdentity")
    def user_assigned_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The user assigned managed identity's ARM ID to use when accessing a resource.
        """
        return pulumi.get(self, "user_assigned_identity")

    @user_assigned_identity.setter
    def user_assigned_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_assigned_identity", value)


@pulumi.input_type
class StorageAccountArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[Union[str, 'StorageAccountType']],
                 id: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input['ResourceIdentityArgs']] = None):
        """
        The storage account details.
        :param pulumi.Input[Union[str, 'StorageAccountType']] type: The type of the storage account.
        :param pulumi.Input[str] id: The ID of the storage account resource. Media Services relies on tables and queues as well as blobs, so the primary storage account must be a Standard Storage account (either Microsoft.ClassicStorage or Microsoft.Storage). Blob only storage accounts can be added as secondary storage accounts.
        :param pulumi.Input['ResourceIdentityArgs'] identity: The storage account identity.
        """
        pulumi.set(__self__, "type", type)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'StorageAccountType']]:
        """
        The type of the storage account.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'StorageAccountType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the storage account resource. Media Services relies on tables and queues as well as blobs, so the primary storage account must be a Standard Storage account (either Microsoft.ClassicStorage or Microsoft.Storage). Blob only storage accounts can be added as secondary storage accounts.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input['ResourceIdentityArgs']]:
        """
        The storage account identity.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input['ResourceIdentityArgs']]):
        pulumi.set(self, "identity", value)


