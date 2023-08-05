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
    'EncryptionPropertyArgs',
    'ExportPolicyArgs',
    'IPRuleArgs',
    'IdentityPropertiesArgs',
    'KeyVaultPropertiesArgs',
    'NetworkRuleSetArgs',
    'PoliciesArgs',
    'PrivateEndpointArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'QuarantinePolicyArgs',
    'RetentionPolicyArgs',
    'SkuArgs',
    'TrustPolicyArgs',
    'UserIdentityPropertiesArgs',
]

@pulumi.input_type
class EncryptionPropertyArgs:
    def __init__(__self__, *,
                 key_vault_properties: Optional[pulumi.Input['KeyVaultPropertiesArgs']] = None,
                 status: Optional[pulumi.Input[Union[str, 'EncryptionStatus']]] = None):
        """
        :param pulumi.Input['KeyVaultPropertiesArgs'] key_vault_properties: Key vault properties.
        :param pulumi.Input[Union[str, 'EncryptionStatus']] status: Indicates whether or not the encryption is enabled for container registry.
        """
        if key_vault_properties is not None:
            pulumi.set(__self__, "key_vault_properties", key_vault_properties)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="keyVaultProperties")
    def key_vault_properties(self) -> Optional[pulumi.Input['KeyVaultPropertiesArgs']]:
        """
        Key vault properties.
        """
        return pulumi.get(self, "key_vault_properties")

    @key_vault_properties.setter
    def key_vault_properties(self, value: Optional[pulumi.Input['KeyVaultPropertiesArgs']]):
        pulumi.set(self, "key_vault_properties", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'EncryptionStatus']]]:
        """
        Indicates whether or not the encryption is enabled for container registry.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'EncryptionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ExportPolicyArgs:
    def __init__(__self__, *,
                 status: Optional[pulumi.Input[Union[str, 'ExportPolicyStatus']]] = None):
        """
        The export policy for a container registry.
        :param pulumi.Input[Union[str, 'ExportPolicyStatus']] status: The value that indicates whether the policy is enabled or not.
        """
        if status is None:
            status = 'enabled'
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'ExportPolicyStatus']]]:
        """
        The value that indicates whether the policy is enabled or not.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'ExportPolicyStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class IPRuleArgs:
    def __init__(__self__, *,
                 i_p_address_or_range: pulumi.Input[str],
                 action: Optional[pulumi.Input[Union[str, 'Action']]] = None):
        """
        IP rule with specific IP or IP range in CIDR format.
        :param pulumi.Input[str] i_p_address_or_range: Specifies the IP or IP range in CIDR format. Only IPV4 address is allowed.
        :param pulumi.Input[Union[str, 'Action']] action: The action of IP ACL rule.
        """
        pulumi.set(__self__, "i_p_address_or_range", i_p_address_or_range)
        if action is None:
            action = 'Allow'
        if action is not None:
            pulumi.set(__self__, "action", action)

    @property
    @pulumi.getter(name="iPAddressOrRange")
    def i_p_address_or_range(self) -> pulumi.Input[str]:
        """
        Specifies the IP or IP range in CIDR format. Only IPV4 address is allowed.
        """
        return pulumi.get(self, "i_p_address_or_range")

    @i_p_address_or_range.setter
    def i_p_address_or_range(self, value: pulumi.Input[str]):
        pulumi.set(self, "i_p_address_or_range", value)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[Union[str, 'Action']]]:
        """
        The action of IP ACL rule.
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[Union[str, 'Action']]]):
        pulumi.set(self, "action", value)


@pulumi.input_type
class IdentityPropertiesArgs:
    def __init__(__self__, *,
                 principal_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None,
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, pulumi.Input['UserIdentityPropertiesArgs']]]] = None):
        """
        Managed identity for the resource.
        :param pulumi.Input[str] principal_id: The principal ID of resource identity.
        :param pulumi.Input[str] tenant_id: The tenant ID of resource.
        :param pulumi.Input['ResourceIdentityType'] type: The identity type.
        :param pulumi.Input[Mapping[str, pulumi.Input['UserIdentityPropertiesArgs']]] user_assigned_identities: The list of user identities associated with the resource. The user identity 
               dictionary key references will be ARM resource ids in the form: 
               '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/
                   providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input['UserIdentityPropertiesArgs']]]]:
        """
        The list of user identities associated with the resource. The user identity 
        dictionary key references will be ARM resource ids in the form: 
        '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/
            providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input['UserIdentityPropertiesArgs']]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class KeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 identity: Optional[pulumi.Input[str]] = None,
                 key_identifier: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] identity: The client id of the identity which will be used to access key vault.
        :param pulumi.Input[str] key_identifier: Key vault uri to access the encryption key.
        """
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if key_identifier is not None:
            pulumi.set(__self__, "key_identifier", key_identifier)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input[str]]:
        """
        The client id of the identity which will be used to access key vault.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="keyIdentifier")
    def key_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        Key vault uri to access the encryption key.
        """
        return pulumi.get(self, "key_identifier")

    @key_identifier.setter
    def key_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_identifier", value)


@pulumi.input_type
class NetworkRuleSetArgs:
    def __init__(__self__, *,
                 default_action: pulumi.Input[Union[str, 'DefaultAction']],
                 ip_rules: Optional[pulumi.Input[Sequence[pulumi.Input['IPRuleArgs']]]] = None):
        """
        The network rule set for a container registry.
        :param pulumi.Input[Union[str, 'DefaultAction']] default_action: The default action of allow or deny when no other rules match.
        :param pulumi.Input[Sequence[pulumi.Input['IPRuleArgs']]] ip_rules: The IP ACL rules.
        """
        if default_action is None:
            default_action = 'Allow'
        pulumi.set(__self__, "default_action", default_action)
        if ip_rules is not None:
            pulumi.set(__self__, "ip_rules", ip_rules)

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> pulumi.Input[Union[str, 'DefaultAction']]:
        """
        The default action of allow or deny when no other rules match.
        """
        return pulumi.get(self, "default_action")

    @default_action.setter
    def default_action(self, value: pulumi.Input[Union[str, 'DefaultAction']]):
        pulumi.set(self, "default_action", value)

    @property
    @pulumi.getter(name="ipRules")
    def ip_rules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IPRuleArgs']]]]:
        """
        The IP ACL rules.
        """
        return pulumi.get(self, "ip_rules")

    @ip_rules.setter
    def ip_rules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IPRuleArgs']]]]):
        pulumi.set(self, "ip_rules", value)


@pulumi.input_type
class PoliciesArgs:
    def __init__(__self__, *,
                 export_policy: Optional[pulumi.Input['ExportPolicyArgs']] = None,
                 quarantine_policy: Optional[pulumi.Input['QuarantinePolicyArgs']] = None,
                 retention_policy: Optional[pulumi.Input['RetentionPolicyArgs']] = None,
                 trust_policy: Optional[pulumi.Input['TrustPolicyArgs']] = None):
        """
        The policies for a container registry.
        :param pulumi.Input['ExportPolicyArgs'] export_policy: The export policy for a container registry.
        :param pulumi.Input['QuarantinePolicyArgs'] quarantine_policy: The quarantine policy for a container registry.
        :param pulumi.Input['RetentionPolicyArgs'] retention_policy: The retention policy for a container registry.
        :param pulumi.Input['TrustPolicyArgs'] trust_policy: The content trust policy for a container registry.
        """
        if export_policy is not None:
            pulumi.set(__self__, "export_policy", export_policy)
        if quarantine_policy is not None:
            pulumi.set(__self__, "quarantine_policy", quarantine_policy)
        if retention_policy is not None:
            pulumi.set(__self__, "retention_policy", retention_policy)
        if trust_policy is not None:
            pulumi.set(__self__, "trust_policy", trust_policy)

    @property
    @pulumi.getter(name="exportPolicy")
    def export_policy(self) -> Optional[pulumi.Input['ExportPolicyArgs']]:
        """
        The export policy for a container registry.
        """
        return pulumi.get(self, "export_policy")

    @export_policy.setter
    def export_policy(self, value: Optional[pulumi.Input['ExportPolicyArgs']]):
        pulumi.set(self, "export_policy", value)

    @property
    @pulumi.getter(name="quarantinePolicy")
    def quarantine_policy(self) -> Optional[pulumi.Input['QuarantinePolicyArgs']]:
        """
        The quarantine policy for a container registry.
        """
        return pulumi.get(self, "quarantine_policy")

    @quarantine_policy.setter
    def quarantine_policy(self, value: Optional[pulumi.Input['QuarantinePolicyArgs']]):
        pulumi.set(self, "quarantine_policy", value)

    @property
    @pulumi.getter(name="retentionPolicy")
    def retention_policy(self) -> Optional[pulumi.Input['RetentionPolicyArgs']]:
        """
        The retention policy for a container registry.
        """
        return pulumi.get(self, "retention_policy")

    @retention_policy.setter
    def retention_policy(self, value: Optional[pulumi.Input['RetentionPolicyArgs']]):
        pulumi.set(self, "retention_policy", value)

    @property
    @pulumi.getter(name="trustPolicy")
    def trust_policy(self) -> Optional[pulumi.Input['TrustPolicyArgs']]:
        """
        The content trust policy for a container registry.
        """
        return pulumi.get(self, "trust_policy")

    @trust_policy.setter
    def trust_policy(self, value: Optional[pulumi.Input['TrustPolicyArgs']]):
        pulumi.set(self, "trust_policy", value)


@pulumi.input_type
class PrivateEndpointArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None):
        """
        The Private Endpoint resource.
        :param pulumi.Input[str] id: This is private endpoint resource created with Microsoft.Network resource provider.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        This is private endpoint resource created with Microsoft.Network resource provider.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[Union[str, 'ActionsRequired']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'ConnectionStatus']]] = None):
        """
        The state of a private link service connection.
        :param pulumi.Input[Union[str, 'ActionsRequired']] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The description for connection status. For example if connection is rejected it can indicate reason for rejection.
        :param pulumi.Input[Union[str, 'ConnectionStatus']] status: The private link service connection status.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[Union[str, 'ActionsRequired']]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[Union[str, 'ActionsRequired']]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description for connection status. For example if connection is rejected it can indicate reason for rejection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'ConnectionStatus']]]:
        """
        The private link service connection status.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'ConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class QuarantinePolicyArgs:
    def __init__(__self__, *,
                 status: Optional[pulumi.Input[Union[str, 'PolicyStatus']]] = None):
        """
        The quarantine policy for a container registry.
        :param pulumi.Input[Union[str, 'PolicyStatus']] status: The value that indicates whether the policy is enabled or not.
        """
        if status is None:
            status = 'disabled'
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PolicyStatus']]]:
        """
        The value that indicates whether the policy is enabled or not.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PolicyStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class RetentionPolicyArgs:
    def __init__(__self__, *,
                 days: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PolicyStatus']]] = None):
        """
        The retention policy for a container registry.
        :param pulumi.Input[int] days: The number of days to retain an untagged manifest after which it gets purged.
        :param pulumi.Input[Union[str, 'PolicyStatus']] status: The value that indicates whether the policy is enabled or not.
        """
        if days is None:
            days = 7
        if days is not None:
            pulumi.set(__self__, "days", days)
        if status is None:
            status = 'disabled'
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def days(self) -> Optional[pulumi.Input[int]]:
        """
        The number of days to retain an untagged manifest after which it gets purged.
        """
        return pulumi.get(self, "days")

    @days.setter
    def days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "days", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PolicyStatus']]]:
        """
        The value that indicates whether the policy is enabled or not.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PolicyStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'SkuName']]):
        """
        The SKU of a container registry.
        :param pulumi.Input[Union[str, 'SkuName']] name: The SKU name of the container registry. Required for registry creation.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        The SKU name of the container registry. Required for registry creation.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class TrustPolicyArgs:
    def __init__(__self__, *,
                 status: Optional[pulumi.Input[Union[str, 'PolicyStatus']]] = None,
                 type: Optional[pulumi.Input[Union[str, 'TrustPolicyType']]] = None):
        """
        The content trust policy for a container registry.
        :param pulumi.Input[Union[str, 'PolicyStatus']] status: The value that indicates whether the policy is enabled or not.
        :param pulumi.Input[Union[str, 'TrustPolicyType']] type: The type of trust policy.
        """
        if status is None:
            status = 'disabled'
        if status is not None:
            pulumi.set(__self__, "status", status)
        if type is None:
            type = 'Notary'
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PolicyStatus']]]:
        """
        The value that indicates whether the policy is enabled or not.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PolicyStatus']]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'TrustPolicyType']]]:
        """
        The type of trust policy.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'TrustPolicyType']]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class UserIdentityPropertiesArgs:
    def __init__(__self__, *,
                 client_id: Optional[pulumi.Input[str]] = None,
                 principal_id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] client_id: The client id of user assigned identity.
        :param pulumi.Input[str] principal_id: The principal id of user assigned identity.
        """
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if principal_id is not None:
            pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> Optional[pulumi.Input[str]]:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")

    @principal_id.setter
    def principal_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal_id", value)


