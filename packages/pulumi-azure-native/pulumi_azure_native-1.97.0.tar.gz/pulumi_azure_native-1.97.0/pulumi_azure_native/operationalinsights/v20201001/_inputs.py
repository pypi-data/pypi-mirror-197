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
    'ClusterSkuArgs',
    'IdentityArgs',
    'KeyVaultPropertiesArgs',
    'WorkspaceCappingArgs',
    'WorkspaceFeaturesArgs',
    'WorkspaceSkuArgs',
]

@pulumi.input_type
class ClusterSkuArgs:
    def __init__(__self__, *,
                 capacity: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[Union[str, 'ClusterSkuNameEnum']]] = None):
        """
        The cluster sku definition.
        :param pulumi.Input[float] capacity: The capacity value
        :param pulumi.Input[Union[str, 'ClusterSkuNameEnum']] name: The name of the SKU.
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[float]]:
        """
        The capacity value
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[Union[str, 'ClusterSkuNameEnum']]]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[Union[str, 'ClusterSkuNameEnum']]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input['IdentityType'],
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Identity for the resource.
        :param pulumi.Input['IdentityType'] type: Type of managed service identity.
        :param pulumi.Input[Mapping[str, Any]] user_assigned_identities: The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input['IdentityType']:
        """
        Type of managed service identity.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input['IdentityType']):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The list of user identities associated with the resource. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class KeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 key_name: Optional[pulumi.Input[str]] = None,
                 key_rsa_size: Optional[pulumi.Input[int]] = None,
                 key_vault_uri: Optional[pulumi.Input[str]] = None,
                 key_version: Optional[pulumi.Input[str]] = None):
        """
        The key vault properties.
        :param pulumi.Input[str] key_name: The name of the key associated with the Log Analytics cluster.
        :param pulumi.Input[int] key_rsa_size: Selected key minimum required size.
        :param pulumi.Input[str] key_vault_uri: The Key Vault uri which holds they key associated with the Log Analytics cluster.
        :param pulumi.Input[str] key_version: The version of the key associated with the Log Analytics cluster.
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_rsa_size is not None:
            pulumi.set(__self__, "key_rsa_size", key_rsa_size)
        if key_vault_uri is not None:
            pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_name")

    @key_name.setter
    def key_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_name", value)

    @property
    @pulumi.getter(name="keyRsaSize")
    def key_rsa_size(self) -> Optional[pulumi.Input[int]]:
        """
        Selected key minimum required size.
        """
        return pulumi.get(self, "key_rsa_size")

    @key_rsa_size.setter
    def key_rsa_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "key_rsa_size", value)

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The Key Vault uri which holds they key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_vault_uri")

    @key_vault_uri.setter
    def key_vault_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_uri", value)

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the key associated with the Log Analytics cluster.
        """
        return pulumi.get(self, "key_version")

    @key_version.setter
    def key_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_version", value)


@pulumi.input_type
class WorkspaceCappingArgs:
    def __init__(__self__, *,
                 daily_quota_gb: Optional[pulumi.Input[float]] = None):
        """
        The daily volume cap for ingestion.
        :param pulumi.Input[float] daily_quota_gb: The workspace daily quota for ingestion.
        """
        if daily_quota_gb is not None:
            pulumi.set(__self__, "daily_quota_gb", daily_quota_gb)

    @property
    @pulumi.getter(name="dailyQuotaGb")
    def daily_quota_gb(self) -> Optional[pulumi.Input[float]]:
        """
        The workspace daily quota for ingestion.
        """
        return pulumi.get(self, "daily_quota_gb")

    @daily_quota_gb.setter
    def daily_quota_gb(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "daily_quota_gb", value)


@pulumi.input_type
class WorkspaceFeaturesArgs:
    def __init__(__self__, *,
                 cluster_resource_id: Optional[pulumi.Input[str]] = None,
                 disable_local_auth: Optional[pulumi.Input[bool]] = None,
                 enable_data_export: Optional[pulumi.Input[bool]] = None,
                 enable_log_access_using_only_resource_permissions: Optional[pulumi.Input[bool]] = None,
                 immediate_purge_data_on30_days: Optional[pulumi.Input[bool]] = None):
        """
        Workspace features.
        :param pulumi.Input[str] cluster_resource_id: Dedicated LA cluster resourceId that is linked to the workspaces.
        :param pulumi.Input[bool] disable_local_auth: Disable Non-AAD based Auth.
        :param pulumi.Input[bool] enable_data_export: Flag that indicate if data should be exported.
        :param pulumi.Input[bool] enable_log_access_using_only_resource_permissions: Flag that indicate which permission to use - resource or workspace or both.
        :param pulumi.Input[bool] immediate_purge_data_on30_days: Flag that describes if we want to remove the data after 30 days.
        """
        if cluster_resource_id is not None:
            pulumi.set(__self__, "cluster_resource_id", cluster_resource_id)
        if disable_local_auth is not None:
            pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if enable_data_export is not None:
            pulumi.set(__self__, "enable_data_export", enable_data_export)
        if enable_log_access_using_only_resource_permissions is not None:
            pulumi.set(__self__, "enable_log_access_using_only_resource_permissions", enable_log_access_using_only_resource_permissions)
        if immediate_purge_data_on30_days is not None:
            pulumi.set(__self__, "immediate_purge_data_on30_days", immediate_purge_data_on30_days)

    @property
    @pulumi.getter(name="clusterResourceId")
    def cluster_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Dedicated LA cluster resourceId that is linked to the workspaces.
        """
        return pulumi.get(self, "cluster_resource_id")

    @cluster_resource_id.setter
    def cluster_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_resource_id", value)

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        Disable Non-AAD based Auth.
        """
        return pulumi.get(self, "disable_local_auth")

    @disable_local_auth.setter
    def disable_local_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disable_local_auth", value)

    @property
    @pulumi.getter(name="enableDataExport")
    def enable_data_export(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that indicate if data should be exported.
        """
        return pulumi.get(self, "enable_data_export")

    @enable_data_export.setter
    def enable_data_export(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_data_export", value)

    @property
    @pulumi.getter(name="enableLogAccessUsingOnlyResourcePermissions")
    def enable_log_access_using_only_resource_permissions(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that indicate which permission to use - resource or workspace or both.
        """
        return pulumi.get(self, "enable_log_access_using_only_resource_permissions")

    @enable_log_access_using_only_resource_permissions.setter
    def enable_log_access_using_only_resource_permissions(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_log_access_using_only_resource_permissions", value)

    @property
    @pulumi.getter(name="immediatePurgeDataOn30Days")
    def immediate_purge_data_on30_days(self) -> Optional[pulumi.Input[bool]]:
        """
        Flag that describes if we want to remove the data after 30 days.
        """
        return pulumi.get(self, "immediate_purge_data_on30_days")

    @immediate_purge_data_on30_days.setter
    def immediate_purge_data_on30_days(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "immediate_purge_data_on30_days", value)


@pulumi.input_type
class WorkspaceSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'WorkspaceSkuNameEnum']],
                 capacity_reservation_level: Optional[pulumi.Input[int]] = None):
        """
        The SKU (tier) of a workspace.
        :param pulumi.Input[Union[str, 'WorkspaceSkuNameEnum']] name: The name of the SKU.
        :param pulumi.Input[int] capacity_reservation_level: The capacity reservation level for this workspace, when CapacityReservation sku is selected.
        """
        pulumi.set(__self__, "name", name)
        if capacity_reservation_level is not None:
            pulumi.set(__self__, "capacity_reservation_level", capacity_reservation_level)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'WorkspaceSkuNameEnum']]:
        """
        The name of the SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'WorkspaceSkuNameEnum']]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="capacityReservationLevel")
    def capacity_reservation_level(self) -> Optional[pulumi.Input[int]]:
        """
        The capacity reservation level for this workspace, when CapacityReservation sku is selected.
        """
        return pulumi.get(self, "capacity_reservation_level")

    @capacity_reservation_level.setter
    def capacity_reservation_level(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity_reservation_level", value)


