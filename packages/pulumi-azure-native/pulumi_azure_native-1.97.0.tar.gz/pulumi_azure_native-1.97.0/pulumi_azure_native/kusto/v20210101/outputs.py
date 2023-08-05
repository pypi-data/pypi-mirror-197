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

__all__ = [
    'AzureSkuResponse',
    'DatabasePrincipalResponse',
    'DatabaseStatisticsResponse',
    'FollowerDatabaseDefinitionResponse',
    'IdentityResponse',
    'IdentityResponseUserAssignedIdentities',
    'KeyVaultPropertiesResponse',
    'LanguageExtensionResponse',
    'LanguageExtensionsListResponse',
    'OptimizedAutoscaleResponse',
    'SystemDataResponse',
    'TableLevelSharingPropertiesResponse',
    'TrustedExternalTenantResponse',
    'VirtualNetworkConfigurationResponse',
]

@pulumi.output_type
class AzureSkuResponse(dict):
    """
    Azure SKU definition.
    """
    def __init__(__self__, *,
                 name: str,
                 tier: str,
                 capacity: Optional[int] = None):
        """
        Azure SKU definition.
        :param str name: SKU name.
        :param str tier: SKU tier.
        :param int capacity: The number of instances of the cluster.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "tier", tier)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        SKU name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tier(self) -> str:
        """
        SKU tier.
        """
        return pulumi.get(self, "tier")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        The number of instances of the cluster.
        """
        return pulumi.get(self, "capacity")


@pulumi.output_type
class DatabasePrincipalResponse(dict):
    """
    A class representing database principal entity.
    """
    def __init__(__self__, *,
                 name: str,
                 role: str,
                 tenant_name: str,
                 type: str,
                 app_id: Optional[str] = None,
                 email: Optional[str] = None,
                 fqn: Optional[str] = None):
        """
        A class representing database principal entity.
        :param str name: Database principal name.
        :param str role: Database principal role.
        :param str tenant_name: The tenant name of the principal
        :param str type: Database principal type.
        :param str app_id: Application id - relevant only for application principal type.
        :param str email: Database principal email if exists.
        :param str fqn: Database principal fully qualified name.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "role", role)
        pulumi.set(__self__, "tenant_name", tenant_name)
        pulumi.set(__self__, "type", type)
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if fqn is not None:
            pulumi.set(__self__, "fqn", fqn)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Database principal name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        Database principal role.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="tenantName")
    def tenant_name(self) -> str:
        """
        The tenant name of the principal
        """
        return pulumi.get(self, "tenant_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Database principal type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[str]:
        """
        Application id - relevant only for application principal type.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter
    def email(self) -> Optional[str]:
        """
        Database principal email if exists.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def fqn(self) -> Optional[str]:
        """
        Database principal fully qualified name.
        """
        return pulumi.get(self, "fqn")


@pulumi.output_type
class DatabaseStatisticsResponse(dict):
    """
    A class that contains database statistics information.
    """
    def __init__(__self__, *,
                 size: Optional[float] = None):
        """
        A class that contains database statistics information.
        :param float size: The database size - the total size of compressed data and index in bytes.
        """
        if size is not None:
            pulumi.set(__self__, "size", size)

    @property
    @pulumi.getter
    def size(self) -> Optional[float]:
        """
        The database size - the total size of compressed data and index in bytes.
        """
        return pulumi.get(self, "size")


@pulumi.output_type
class FollowerDatabaseDefinitionResponse(dict):
    """
    A class representing follower database request.
    """
    def __init__(__self__, *,
                 attached_database_configuration_name: str,
                 cluster_resource_id: str,
                 database_name: str):
        """
        A class representing follower database request.
        :param str attached_database_configuration_name: Resource name of the attached database configuration in the follower cluster.
        :param str cluster_resource_id: Resource id of the cluster that follows a database owned by this cluster.
        :param str database_name: The database name owned by this cluster that was followed. * in case following all databases.
        """
        pulumi.set(__self__, "attached_database_configuration_name", attached_database_configuration_name)
        pulumi.set(__self__, "cluster_resource_id", cluster_resource_id)
        pulumi.set(__self__, "database_name", database_name)

    @property
    @pulumi.getter(name="attachedDatabaseConfigurationName")
    def attached_database_configuration_name(self) -> str:
        """
        Resource name of the attached database configuration in the follower cluster.
        """
        return pulumi.get(self, "attached_database_configuration_name")

    @property
    @pulumi.getter(name="clusterResourceId")
    def cluster_resource_id(self) -> str:
        """
        Resource id of the cluster that follows a database owned by this cluster.
        """
        return pulumi.get(self, "cluster_resource_id")

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> str:
        """
        The database name owned by this cluster that was followed. * in case following all databases.
        """
        return pulumi.get(self, "database_name")


@pulumi.output_type
class IdentityResponse(dict):
    """
    Identity for the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"
        elif key == "userAssignedIdentities":
            suggest = "user_assigned_identities"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str,
                 user_assigned_identities: Optional[Mapping[str, 'outputs.IdentityResponseUserAssignedIdentities']] = None):
        """
        Identity for the resource.
        :param str principal_id: The principal ID of resource identity.
        :param str tenant_id: The tenant ID of resource.
        :param str type: The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove all identities.
        :param Mapping[str, 'IdentityResponseUserAssignedIdentities'] user_assigned_identities: The list of user identities associated with the Kusto cluster. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID of resource identity.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove all identities.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[Mapping[str, 'outputs.IdentityResponseUserAssignedIdentities']]:
        """
        The list of user identities associated with the Kusto cluster. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")


@pulumi.output_type
class IdentityResponseUserAssignedIdentities(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"
        elif key == "principalId":
            suggest = "principal_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityResponseUserAssignedIdentities. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityResponseUserAssignedIdentities.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityResponseUserAssignedIdentities.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 principal_id: str):
        """
        :param str client_id: The client id of user assigned identity.
        :param str principal_id: The principal id of user assigned identity.
        """
        pulumi.set(__self__, "client_id", client_id)
        pulumi.set(__self__, "principal_id", principal_id)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The client id of user assigned identity.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal id of user assigned identity.
        """
        return pulumi.get(self, "principal_id")


@pulumi.output_type
class KeyVaultPropertiesResponse(dict):
    """
    Properties of the key vault.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyName":
            suggest = "key_name"
        elif key == "keyVaultUri":
            suggest = "key_vault_uri"
        elif key == "keyVersion":
            suggest = "key_version"
        elif key == "userIdentity":
            suggest = "user_identity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in KeyVaultPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        KeyVaultPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        KeyVaultPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_name: str,
                 key_vault_uri: str,
                 key_version: Optional[str] = None,
                 user_identity: Optional[str] = None):
        """
        Properties of the key vault.
        :param str key_name: The name of the key vault key.
        :param str key_vault_uri: The Uri of the key vault.
        :param str key_version: The version of the key vault key.
        :param str user_identity: The user assigned identity (ARM resource id) that has access to the key.
        """
        pulumi.set(__self__, "key_name", key_name)
        pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)
        if user_identity is not None:
            pulumi.set(__self__, "user_identity", user_identity)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> str:
        """
        The name of the key vault key.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> str:
        """
        The Uri of the key vault.
        """
        return pulumi.get(self, "key_vault_uri")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[str]:
        """
        The version of the key vault key.
        """
        return pulumi.get(self, "key_version")

    @property
    @pulumi.getter(name="userIdentity")
    def user_identity(self) -> Optional[str]:
        """
        The user assigned identity (ARM resource id) that has access to the key.
        """
        return pulumi.get(self, "user_identity")


@pulumi.output_type
class LanguageExtensionResponse(dict):
    """
    The language extension object.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "languageExtensionName":
            suggest = "language_extension_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LanguageExtensionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LanguageExtensionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LanguageExtensionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 language_extension_name: Optional[str] = None):
        """
        The language extension object.
        :param str language_extension_name: The language extension name.
        """
        if language_extension_name is not None:
            pulumi.set(__self__, "language_extension_name", language_extension_name)

    @property
    @pulumi.getter(name="languageExtensionName")
    def language_extension_name(self) -> Optional[str]:
        """
        The language extension name.
        """
        return pulumi.get(self, "language_extension_name")


@pulumi.output_type
class LanguageExtensionsListResponse(dict):
    """
    The list of language extension objects.
    """
    def __init__(__self__, *,
                 value: Optional[Sequence['outputs.LanguageExtensionResponse']] = None):
        """
        The list of language extension objects.
        :param Sequence['LanguageExtensionResponse'] value: The list of language extensions.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.LanguageExtensionResponse']]:
        """
        The list of language extensions.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class OptimizedAutoscaleResponse(dict):
    """
    A class that contains the optimized auto scale definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "isEnabled":
            suggest = "is_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OptimizedAutoscaleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OptimizedAutoscaleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OptimizedAutoscaleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 is_enabled: bool,
                 maximum: int,
                 minimum: int,
                 version: int):
        """
        A class that contains the optimized auto scale definition.
        :param bool is_enabled: A boolean value that indicate if the optimized autoscale feature is enabled or not.
        :param int maximum: Maximum allowed instances count.
        :param int minimum: Minimum allowed instances count.
        :param int version: The version of the template defined, for instance 1.
        """
        pulumi.set(__self__, "is_enabled", is_enabled)
        pulumi.set(__self__, "maximum", maximum)
        pulumi.set(__self__, "minimum", minimum)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> bool:
        """
        A boolean value that indicate if the optimized autoscale feature is enabled or not.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter
    def maximum(self) -> int:
        """
        Maximum allowed instances count.
        """
        return pulumi.get(self, "maximum")

    @property
    @pulumi.getter
    def minimum(self) -> int:
        """
        Minimum allowed instances count.
        """
        return pulumi.get(self, "minimum")

    @property
    @pulumi.getter
    def version(self) -> int:
        """
        The version of the template defined, for instance 1.
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


@pulumi.output_type
class TableLevelSharingPropertiesResponse(dict):
    """
    Tables that will be included and excluded in the follower database
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "externalTablesToExclude":
            suggest = "external_tables_to_exclude"
        elif key == "externalTablesToInclude":
            suggest = "external_tables_to_include"
        elif key == "materializedViewsToExclude":
            suggest = "materialized_views_to_exclude"
        elif key == "materializedViewsToInclude":
            suggest = "materialized_views_to_include"
        elif key == "tablesToExclude":
            suggest = "tables_to_exclude"
        elif key == "tablesToInclude":
            suggest = "tables_to_include"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableLevelSharingPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableLevelSharingPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableLevelSharingPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 external_tables_to_exclude: Optional[Sequence[str]] = None,
                 external_tables_to_include: Optional[Sequence[str]] = None,
                 materialized_views_to_exclude: Optional[Sequence[str]] = None,
                 materialized_views_to_include: Optional[Sequence[str]] = None,
                 tables_to_exclude: Optional[Sequence[str]] = None,
                 tables_to_include: Optional[Sequence[str]] = None):
        """
        Tables that will be included and excluded in the follower database
        :param Sequence[str] external_tables_to_exclude: List of external tables exclude from the follower database
        :param Sequence[str] external_tables_to_include: List of external tables to include in the follower database
        :param Sequence[str] materialized_views_to_exclude: List of materialized views exclude from the follower database
        :param Sequence[str] materialized_views_to_include: List of materialized views to include in the follower database
        :param Sequence[str] tables_to_exclude: List of tables to exclude from the follower database
        :param Sequence[str] tables_to_include: List of tables to include in the follower database
        """
        if external_tables_to_exclude is not None:
            pulumi.set(__self__, "external_tables_to_exclude", external_tables_to_exclude)
        if external_tables_to_include is not None:
            pulumi.set(__self__, "external_tables_to_include", external_tables_to_include)
        if materialized_views_to_exclude is not None:
            pulumi.set(__self__, "materialized_views_to_exclude", materialized_views_to_exclude)
        if materialized_views_to_include is not None:
            pulumi.set(__self__, "materialized_views_to_include", materialized_views_to_include)
        if tables_to_exclude is not None:
            pulumi.set(__self__, "tables_to_exclude", tables_to_exclude)
        if tables_to_include is not None:
            pulumi.set(__self__, "tables_to_include", tables_to_include)

    @property
    @pulumi.getter(name="externalTablesToExclude")
    def external_tables_to_exclude(self) -> Optional[Sequence[str]]:
        """
        List of external tables exclude from the follower database
        """
        return pulumi.get(self, "external_tables_to_exclude")

    @property
    @pulumi.getter(name="externalTablesToInclude")
    def external_tables_to_include(self) -> Optional[Sequence[str]]:
        """
        List of external tables to include in the follower database
        """
        return pulumi.get(self, "external_tables_to_include")

    @property
    @pulumi.getter(name="materializedViewsToExclude")
    def materialized_views_to_exclude(self) -> Optional[Sequence[str]]:
        """
        List of materialized views exclude from the follower database
        """
        return pulumi.get(self, "materialized_views_to_exclude")

    @property
    @pulumi.getter(name="materializedViewsToInclude")
    def materialized_views_to_include(self) -> Optional[Sequence[str]]:
        """
        List of materialized views to include in the follower database
        """
        return pulumi.get(self, "materialized_views_to_include")

    @property
    @pulumi.getter(name="tablesToExclude")
    def tables_to_exclude(self) -> Optional[Sequence[str]]:
        """
        List of tables to exclude from the follower database
        """
        return pulumi.get(self, "tables_to_exclude")

    @property
    @pulumi.getter(name="tablesToInclude")
    def tables_to_include(self) -> Optional[Sequence[str]]:
        """
        List of tables to include in the follower database
        """
        return pulumi.get(self, "tables_to_include")


@pulumi.output_type
class TrustedExternalTenantResponse(dict):
    """
    Represents a tenant ID that is trusted by the cluster.
    """
    def __init__(__self__, *,
                 value: Optional[str] = None):
        """
        Represents a tenant ID that is trusted by the cluster.
        :param str value: GUID representing an external tenant.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        GUID representing an external tenant.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class VirtualNetworkConfigurationResponse(dict):
    """
    A class that contains virtual network definition.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataManagementPublicIpId":
            suggest = "data_management_public_ip_id"
        elif key == "enginePublicIpId":
            suggest = "engine_public_ip_id"
        elif key == "subnetId":
            suggest = "subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VirtualNetworkConfigurationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VirtualNetworkConfigurationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VirtualNetworkConfigurationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_management_public_ip_id: str,
                 engine_public_ip_id: str,
                 subnet_id: str):
        """
        A class that contains virtual network definition.
        :param str data_management_public_ip_id: Data management's service public IP address resource id.
        :param str engine_public_ip_id: Engine service's public IP address resource id.
        :param str subnet_id: The subnet resource id.
        """
        pulumi.set(__self__, "data_management_public_ip_id", data_management_public_ip_id)
        pulumi.set(__self__, "engine_public_ip_id", engine_public_ip_id)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="dataManagementPublicIpId")
    def data_management_public_ip_id(self) -> str:
        """
        Data management's service public IP address resource id.
        """
        return pulumi.get(self, "data_management_public_ip_id")

    @property
    @pulumi.getter(name="enginePublicIpId")
    def engine_public_ip_id(self) -> str:
        """
        Engine service's public IP address resource id.
        """
        return pulumi.get(self, "engine_public_ip_id")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The subnet resource id.
        """
        return pulumi.get(self, "subnet_id")


