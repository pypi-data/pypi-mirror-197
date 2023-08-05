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

__all__ = [
    'GetMigrationResult',
    'AwaitableGetMigrationResult',
    'get_migration',
    'get_migration_output',
]

@pulumi.output_type
class GetMigrationResult:
    """
    Represents a migration resource.
    """
    def __init__(__self__, current_status=None, d_bs_to_migrate=None, id=None, location=None, migration_details_level=None, migration_id=None, migration_name=None, migration_resource_group=None, migration_window_start_time_in_utc=None, name=None, overwrite_dbs_in_target=None, secret_parameters=None, setup_logical_replication_on_source_db_if_needed=None, source_db_server_metadata=None, source_db_server_resource_id=None, start_data_migration=None, system_data=None, tags=None, target_db_server_metadata=None, target_db_server_resource_id=None, trigger_cutover=None, type=None, user_assigned_identity_resource_id=None):
        if current_status and not isinstance(current_status, dict):
            raise TypeError("Expected argument 'current_status' to be a dict")
        pulumi.set(__self__, "current_status", current_status)
        if d_bs_to_migrate and not isinstance(d_bs_to_migrate, list):
            raise TypeError("Expected argument 'd_bs_to_migrate' to be a list")
        pulumi.set(__self__, "d_bs_to_migrate", d_bs_to_migrate)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if migration_details_level and not isinstance(migration_details_level, str):
            raise TypeError("Expected argument 'migration_details_level' to be a str")
        pulumi.set(__self__, "migration_details_level", migration_details_level)
        if migration_id and not isinstance(migration_id, str):
            raise TypeError("Expected argument 'migration_id' to be a str")
        pulumi.set(__self__, "migration_id", migration_id)
        if migration_name and not isinstance(migration_name, str):
            raise TypeError("Expected argument 'migration_name' to be a str")
        pulumi.set(__self__, "migration_name", migration_name)
        if migration_resource_group and not isinstance(migration_resource_group, dict):
            raise TypeError("Expected argument 'migration_resource_group' to be a dict")
        pulumi.set(__self__, "migration_resource_group", migration_resource_group)
        if migration_window_start_time_in_utc and not isinstance(migration_window_start_time_in_utc, str):
            raise TypeError("Expected argument 'migration_window_start_time_in_utc' to be a str")
        pulumi.set(__self__, "migration_window_start_time_in_utc", migration_window_start_time_in_utc)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if overwrite_dbs_in_target and not isinstance(overwrite_dbs_in_target, bool):
            raise TypeError("Expected argument 'overwrite_dbs_in_target' to be a bool")
        pulumi.set(__self__, "overwrite_dbs_in_target", overwrite_dbs_in_target)
        if secret_parameters and not isinstance(secret_parameters, dict):
            raise TypeError("Expected argument 'secret_parameters' to be a dict")
        pulumi.set(__self__, "secret_parameters", secret_parameters)
        if setup_logical_replication_on_source_db_if_needed and not isinstance(setup_logical_replication_on_source_db_if_needed, bool):
            raise TypeError("Expected argument 'setup_logical_replication_on_source_db_if_needed' to be a bool")
        pulumi.set(__self__, "setup_logical_replication_on_source_db_if_needed", setup_logical_replication_on_source_db_if_needed)
        if source_db_server_metadata and not isinstance(source_db_server_metadata, dict):
            raise TypeError("Expected argument 'source_db_server_metadata' to be a dict")
        pulumi.set(__self__, "source_db_server_metadata", source_db_server_metadata)
        if source_db_server_resource_id and not isinstance(source_db_server_resource_id, str):
            raise TypeError("Expected argument 'source_db_server_resource_id' to be a str")
        pulumi.set(__self__, "source_db_server_resource_id", source_db_server_resource_id)
        if start_data_migration and not isinstance(start_data_migration, bool):
            raise TypeError("Expected argument 'start_data_migration' to be a bool")
        pulumi.set(__self__, "start_data_migration", start_data_migration)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if target_db_server_metadata and not isinstance(target_db_server_metadata, dict):
            raise TypeError("Expected argument 'target_db_server_metadata' to be a dict")
        pulumi.set(__self__, "target_db_server_metadata", target_db_server_metadata)
        if target_db_server_resource_id and not isinstance(target_db_server_resource_id, str):
            raise TypeError("Expected argument 'target_db_server_resource_id' to be a str")
        pulumi.set(__self__, "target_db_server_resource_id", target_db_server_resource_id)
        if trigger_cutover and not isinstance(trigger_cutover, bool):
            raise TypeError("Expected argument 'trigger_cutover' to be a bool")
        pulumi.set(__self__, "trigger_cutover", trigger_cutover)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_assigned_identity_resource_id and not isinstance(user_assigned_identity_resource_id, str):
            raise TypeError("Expected argument 'user_assigned_identity_resource_id' to be a str")
        pulumi.set(__self__, "user_assigned_identity_resource_id", user_assigned_identity_resource_id)

    @property
    @pulumi.getter(name="currentStatus")
    def current_status(self) -> 'outputs.MigrationStatusResponse':
        """
        Migration status.
        """
        return pulumi.get(self, "current_status")

    @property
    @pulumi.getter(name="dBsToMigrate")
    def d_bs_to_migrate(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "d_bs_to_migrate")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="migrationDetailsLevel")
    def migration_details_level(self) -> str:
        """
        Migration details level.
        """
        return pulumi.get(self, "migration_details_level")

    @property
    @pulumi.getter(name="migrationId")
    def migration_id(self) -> str:
        return pulumi.get(self, "migration_id")

    @property
    @pulumi.getter(name="migrationName")
    def migration_name(self) -> str:
        return pulumi.get(self, "migration_name")

    @property
    @pulumi.getter(name="migrationResourceGroup")
    def migration_resource_group(self) -> Optional['outputs.MigrationResourceGroupResponse']:
        """
        Migration resource group.
        """
        return pulumi.get(self, "migration_resource_group")

    @property
    @pulumi.getter(name="migrationWindowStartTimeInUtc")
    def migration_window_start_time_in_utc(self) -> Optional[str]:
        return pulumi.get(self, "migration_window_start_time_in_utc")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="overwriteDBsInTarget")
    def overwrite_dbs_in_target(self) -> Optional[bool]:
        return pulumi.get(self, "overwrite_dbs_in_target")

    @property
    @pulumi.getter(name="secretParameters")
    def secret_parameters(self) -> Optional['outputs.MigrationSecretParametersResponse']:
        """
        Migration secret parameters.
        """
        return pulumi.get(self, "secret_parameters")

    @property
    @pulumi.getter(name="setupLogicalReplicationOnSourceDBIfNeeded")
    def setup_logical_replication_on_source_db_if_needed(self) -> Optional[bool]:
        return pulumi.get(self, "setup_logical_replication_on_source_db_if_needed")

    @property
    @pulumi.getter(name="sourceDBServerMetadata")
    def source_db_server_metadata(self) -> 'outputs.DBServerMetadataResponse':
        """
        Database server metadata.
        """
        return pulumi.get(self, "source_db_server_metadata")

    @property
    @pulumi.getter(name="sourceDBServerResourceId")
    def source_db_server_resource_id(self) -> Optional[str]:
        return pulumi.get(self, "source_db_server_resource_id")

    @property
    @pulumi.getter(name="startDataMigration")
    def start_data_migration(self) -> Optional[bool]:
        return pulumi.get(self, "start_data_migration")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetDBServerMetadata")
    def target_db_server_metadata(self) -> 'outputs.DBServerMetadataResponse':
        """
        Database server metadata.
        """
        return pulumi.get(self, "target_db_server_metadata")

    @property
    @pulumi.getter(name="targetDBServerResourceId")
    def target_db_server_resource_id(self) -> str:
        return pulumi.get(self, "target_db_server_resource_id")

    @property
    @pulumi.getter(name="triggerCutover")
    def trigger_cutover(self) -> Optional[bool]:
        return pulumi.get(self, "trigger_cutover")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAssignedIdentityResourceId")
    def user_assigned_identity_resource_id(self) -> Optional[str]:
        return pulumi.get(self, "user_assigned_identity_resource_id")


class AwaitableGetMigrationResult(GetMigrationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMigrationResult(
            current_status=self.current_status,
            d_bs_to_migrate=self.d_bs_to_migrate,
            id=self.id,
            location=self.location,
            migration_details_level=self.migration_details_level,
            migration_id=self.migration_id,
            migration_name=self.migration_name,
            migration_resource_group=self.migration_resource_group,
            migration_window_start_time_in_utc=self.migration_window_start_time_in_utc,
            name=self.name,
            overwrite_dbs_in_target=self.overwrite_dbs_in_target,
            secret_parameters=self.secret_parameters,
            setup_logical_replication_on_source_db_if_needed=self.setup_logical_replication_on_source_db_if_needed,
            source_db_server_metadata=self.source_db_server_metadata,
            source_db_server_resource_id=self.source_db_server_resource_id,
            start_data_migration=self.start_data_migration,
            system_data=self.system_data,
            tags=self.tags,
            target_db_server_metadata=self.target_db_server_metadata,
            target_db_server_resource_id=self.target_db_server_resource_id,
            trigger_cutover=self.trigger_cutover,
            type=self.type,
            user_assigned_identity_resource_id=self.user_assigned_identity_resource_id)


def get_migration(migration_name: Optional[str] = None,
                  target_db_server_name: Optional[str] = None,
                  target_db_server_resource_group_name: Optional[str] = None,
                  target_db_server_subscription_id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMigrationResult:
    """
    Gets details of a migration.


    :param str migration_name: The name of the migration.
    :param str target_db_server_name: The name of the target database server.
    :param str target_db_server_resource_group_name: The resource group name of the target database server.
    :param str target_db_server_subscription_id: The subscription ID of the target database server.
    """
    __args__ = dict()
    __args__['migrationName'] = migration_name
    __args__['targetDBServerName'] = target_db_server_name
    __args__['targetDBServerResourceGroupName'] = target_db_server_resource_group_name
    __args__['targetDBServerSubscriptionId'] = target_db_server_subscription_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:dbforpostgresql/v20210615privatepreview:getMigration', __args__, opts=opts, typ=GetMigrationResult).value

    return AwaitableGetMigrationResult(
        current_status=__ret__.current_status,
        d_bs_to_migrate=__ret__.d_bs_to_migrate,
        id=__ret__.id,
        location=__ret__.location,
        migration_details_level=__ret__.migration_details_level,
        migration_id=__ret__.migration_id,
        migration_name=__ret__.migration_name,
        migration_resource_group=__ret__.migration_resource_group,
        migration_window_start_time_in_utc=__ret__.migration_window_start_time_in_utc,
        name=__ret__.name,
        overwrite_dbs_in_target=__ret__.overwrite_dbs_in_target,
        secret_parameters=__ret__.secret_parameters,
        setup_logical_replication_on_source_db_if_needed=__ret__.setup_logical_replication_on_source_db_if_needed,
        source_db_server_metadata=__ret__.source_db_server_metadata,
        source_db_server_resource_id=__ret__.source_db_server_resource_id,
        start_data_migration=__ret__.start_data_migration,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        target_db_server_metadata=__ret__.target_db_server_metadata,
        target_db_server_resource_id=__ret__.target_db_server_resource_id,
        trigger_cutover=__ret__.trigger_cutover,
        type=__ret__.type,
        user_assigned_identity_resource_id=__ret__.user_assigned_identity_resource_id)


@_utilities.lift_output_func(get_migration)
def get_migration_output(migration_name: Optional[pulumi.Input[str]] = None,
                         target_db_server_name: Optional[pulumi.Input[str]] = None,
                         target_db_server_resource_group_name: Optional[pulumi.Input[str]] = None,
                         target_db_server_subscription_id: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMigrationResult]:
    """
    Gets details of a migration.


    :param str migration_name: The name of the migration.
    :param str target_db_server_name: The name of the target database server.
    :param str target_db_server_resource_group_name: The resource group name of the target database server.
    :param str target_db_server_subscription_id: The subscription ID of the target database server.
    """
    ...
