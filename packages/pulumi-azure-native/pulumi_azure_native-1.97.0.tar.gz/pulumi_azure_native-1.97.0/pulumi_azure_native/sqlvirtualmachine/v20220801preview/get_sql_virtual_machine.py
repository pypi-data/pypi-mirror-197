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
    'GetSqlVirtualMachineResult',
    'AwaitableGetSqlVirtualMachineResult',
    'get_sql_virtual_machine',
    'get_sql_virtual_machine_output',
]

@pulumi.output_type
class GetSqlVirtualMachineResult:
    """
    A SQL virtual machine.
    """
    def __init__(__self__, assessment_settings=None, auto_backup_settings=None, auto_patching_settings=None, enable_automatic_upgrade=None, id=None, identity=None, key_vault_credential_settings=None, least_privilege_mode=None, location=None, name=None, provisioning_state=None, server_configurations_management_settings=None, sql_image_offer=None, sql_image_sku=None, sql_management=None, sql_server_license_type=None, sql_virtual_machine_group_resource_id=None, storage_configuration_settings=None, system_data=None, tags=None, troubleshooting_status=None, type=None, virtual_machine_resource_id=None, wsfc_domain_credentials=None, wsfc_static_ip=None):
        if assessment_settings and not isinstance(assessment_settings, dict):
            raise TypeError("Expected argument 'assessment_settings' to be a dict")
        pulumi.set(__self__, "assessment_settings", assessment_settings)
        if auto_backup_settings and not isinstance(auto_backup_settings, dict):
            raise TypeError("Expected argument 'auto_backup_settings' to be a dict")
        pulumi.set(__self__, "auto_backup_settings", auto_backup_settings)
        if auto_patching_settings and not isinstance(auto_patching_settings, dict):
            raise TypeError("Expected argument 'auto_patching_settings' to be a dict")
        pulumi.set(__self__, "auto_patching_settings", auto_patching_settings)
        if enable_automatic_upgrade and not isinstance(enable_automatic_upgrade, bool):
            raise TypeError("Expected argument 'enable_automatic_upgrade' to be a bool")
        pulumi.set(__self__, "enable_automatic_upgrade", enable_automatic_upgrade)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if key_vault_credential_settings and not isinstance(key_vault_credential_settings, dict):
            raise TypeError("Expected argument 'key_vault_credential_settings' to be a dict")
        pulumi.set(__self__, "key_vault_credential_settings", key_vault_credential_settings)
        if least_privilege_mode and not isinstance(least_privilege_mode, str):
            raise TypeError("Expected argument 'least_privilege_mode' to be a str")
        pulumi.set(__self__, "least_privilege_mode", least_privilege_mode)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if server_configurations_management_settings and not isinstance(server_configurations_management_settings, dict):
            raise TypeError("Expected argument 'server_configurations_management_settings' to be a dict")
        pulumi.set(__self__, "server_configurations_management_settings", server_configurations_management_settings)
        if sql_image_offer and not isinstance(sql_image_offer, str):
            raise TypeError("Expected argument 'sql_image_offer' to be a str")
        pulumi.set(__self__, "sql_image_offer", sql_image_offer)
        if sql_image_sku and not isinstance(sql_image_sku, str):
            raise TypeError("Expected argument 'sql_image_sku' to be a str")
        pulumi.set(__self__, "sql_image_sku", sql_image_sku)
        if sql_management and not isinstance(sql_management, str):
            raise TypeError("Expected argument 'sql_management' to be a str")
        pulumi.set(__self__, "sql_management", sql_management)
        if sql_server_license_type and not isinstance(sql_server_license_type, str):
            raise TypeError("Expected argument 'sql_server_license_type' to be a str")
        pulumi.set(__self__, "sql_server_license_type", sql_server_license_type)
        if sql_virtual_machine_group_resource_id and not isinstance(sql_virtual_machine_group_resource_id, str):
            raise TypeError("Expected argument 'sql_virtual_machine_group_resource_id' to be a str")
        pulumi.set(__self__, "sql_virtual_machine_group_resource_id", sql_virtual_machine_group_resource_id)
        if storage_configuration_settings and not isinstance(storage_configuration_settings, dict):
            raise TypeError("Expected argument 'storage_configuration_settings' to be a dict")
        pulumi.set(__self__, "storage_configuration_settings", storage_configuration_settings)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if troubleshooting_status and not isinstance(troubleshooting_status, dict):
            raise TypeError("Expected argument 'troubleshooting_status' to be a dict")
        pulumi.set(__self__, "troubleshooting_status", troubleshooting_status)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if virtual_machine_resource_id and not isinstance(virtual_machine_resource_id, str):
            raise TypeError("Expected argument 'virtual_machine_resource_id' to be a str")
        pulumi.set(__self__, "virtual_machine_resource_id", virtual_machine_resource_id)
        if wsfc_domain_credentials and not isinstance(wsfc_domain_credentials, dict):
            raise TypeError("Expected argument 'wsfc_domain_credentials' to be a dict")
        pulumi.set(__self__, "wsfc_domain_credentials", wsfc_domain_credentials)
        if wsfc_static_ip and not isinstance(wsfc_static_ip, str):
            raise TypeError("Expected argument 'wsfc_static_ip' to be a str")
        pulumi.set(__self__, "wsfc_static_ip", wsfc_static_ip)

    @property
    @pulumi.getter(name="assessmentSettings")
    def assessment_settings(self) -> Optional['outputs.AssessmentSettingsResponse']:
        """
        SQL best practices Assessment Settings.
        """
        return pulumi.get(self, "assessment_settings")

    @property
    @pulumi.getter(name="autoBackupSettings")
    def auto_backup_settings(self) -> Optional['outputs.AutoBackupSettingsResponse']:
        """
        Auto backup settings for SQL Server.
        """
        return pulumi.get(self, "auto_backup_settings")

    @property
    @pulumi.getter(name="autoPatchingSettings")
    def auto_patching_settings(self) -> Optional['outputs.AutoPatchingSettingsResponse']:
        """
        Auto patching settings for applying critical security updates to SQL virtual machine.
        """
        return pulumi.get(self, "auto_patching_settings")

    @property
    @pulumi.getter(name="enableAutomaticUpgrade")
    def enable_automatic_upgrade(self) -> Optional[bool]:
        """
        Enable automatic upgrade of Sql IaaS extension Agent.
        """
        return pulumi.get(self, "enable_automatic_upgrade")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ResourceIdentityResponse']:
        """
        Azure Active Directory identity of the server.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="keyVaultCredentialSettings")
    def key_vault_credential_settings(self) -> Optional['outputs.KeyVaultCredentialSettingsResponse']:
        """
        Key vault credential settings.
        """
        return pulumi.get(self, "key_vault_credential_settings")

    @property
    @pulumi.getter(name="leastPrivilegeMode")
    def least_privilege_mode(self) -> Optional[str]:
        """
        SQL IaaS Agent least privilege mode.
        """
        return pulumi.get(self, "least_privilege_mode")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state to track the async operation status.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serverConfigurationsManagementSettings")
    def server_configurations_management_settings(self) -> Optional['outputs.ServerConfigurationsManagementSettingsResponse']:
        """
        SQL Server configuration management settings.
        """
        return pulumi.get(self, "server_configurations_management_settings")

    @property
    @pulumi.getter(name="sqlImageOffer")
    def sql_image_offer(self) -> Optional[str]:
        """
        SQL image offer. Examples include SQL2016-WS2016, SQL2017-WS2016.
        """
        return pulumi.get(self, "sql_image_offer")

    @property
    @pulumi.getter(name="sqlImageSku")
    def sql_image_sku(self) -> Optional[str]:
        """
        SQL Server edition type.
        """
        return pulumi.get(self, "sql_image_sku")

    @property
    @pulumi.getter(name="sqlManagement")
    def sql_management(self) -> Optional[str]:
        """
        SQL Server Management type.
        """
        return pulumi.get(self, "sql_management")

    @property
    @pulumi.getter(name="sqlServerLicenseType")
    def sql_server_license_type(self) -> Optional[str]:
        """
        SQL Server license type.
        """
        return pulumi.get(self, "sql_server_license_type")

    @property
    @pulumi.getter(name="sqlVirtualMachineGroupResourceId")
    def sql_virtual_machine_group_resource_id(self) -> Optional[str]:
        """
        ARM resource id of the SQL virtual machine group this SQL virtual machine is or will be part of.
        """
        return pulumi.get(self, "sql_virtual_machine_group_resource_id")

    @property
    @pulumi.getter(name="storageConfigurationSettings")
    def storage_configuration_settings(self) -> Optional['outputs.StorageConfigurationSettingsResponse']:
        """
        Storage Configuration Settings.
        """
        return pulumi.get(self, "storage_configuration_settings")

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
    @pulumi.getter(name="troubleshootingStatus")
    def troubleshooting_status(self) -> 'outputs.TroubleshootingStatusResponse':
        """
        Troubleshooting status
        """
        return pulumi.get(self, "troubleshooting_status")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="virtualMachineResourceId")
    def virtual_machine_resource_id(self) -> Optional[str]:
        """
        ARM Resource id of underlying virtual machine created from SQL marketplace image.
        """
        return pulumi.get(self, "virtual_machine_resource_id")

    @property
    @pulumi.getter(name="wsfcDomainCredentials")
    def wsfc_domain_credentials(self) -> Optional['outputs.WsfcDomainCredentialsResponse']:
        """
        Domain credentials for setting up Windows Server Failover Cluster for SQL availability group.
        """
        return pulumi.get(self, "wsfc_domain_credentials")

    @property
    @pulumi.getter(name="wsfcStaticIp")
    def wsfc_static_ip(self) -> Optional[str]:
        """
        Domain credentials for setting up Windows Server Failover Cluster for SQL availability group.
        """
        return pulumi.get(self, "wsfc_static_ip")


class AwaitableGetSqlVirtualMachineResult(GetSqlVirtualMachineResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlVirtualMachineResult(
            assessment_settings=self.assessment_settings,
            auto_backup_settings=self.auto_backup_settings,
            auto_patching_settings=self.auto_patching_settings,
            enable_automatic_upgrade=self.enable_automatic_upgrade,
            id=self.id,
            identity=self.identity,
            key_vault_credential_settings=self.key_vault_credential_settings,
            least_privilege_mode=self.least_privilege_mode,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            server_configurations_management_settings=self.server_configurations_management_settings,
            sql_image_offer=self.sql_image_offer,
            sql_image_sku=self.sql_image_sku,
            sql_management=self.sql_management,
            sql_server_license_type=self.sql_server_license_type,
            sql_virtual_machine_group_resource_id=self.sql_virtual_machine_group_resource_id,
            storage_configuration_settings=self.storage_configuration_settings,
            system_data=self.system_data,
            tags=self.tags,
            troubleshooting_status=self.troubleshooting_status,
            type=self.type,
            virtual_machine_resource_id=self.virtual_machine_resource_id,
            wsfc_domain_credentials=self.wsfc_domain_credentials,
            wsfc_static_ip=self.wsfc_static_ip)


def get_sql_virtual_machine(expand: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            sql_virtual_machine_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlVirtualMachineResult:
    """
    Gets a SQL virtual machine.


    :param str expand: The child resources to include in the response.
    :param str resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str sql_virtual_machine_name: Name of the SQL virtual machine.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlVirtualMachineName'] = sql_virtual_machine_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sqlvirtualmachine/v20220801preview:getSqlVirtualMachine', __args__, opts=opts, typ=GetSqlVirtualMachineResult).value

    return AwaitableGetSqlVirtualMachineResult(
        assessment_settings=__ret__.assessment_settings,
        auto_backup_settings=__ret__.auto_backup_settings,
        auto_patching_settings=__ret__.auto_patching_settings,
        enable_automatic_upgrade=__ret__.enable_automatic_upgrade,
        id=__ret__.id,
        identity=__ret__.identity,
        key_vault_credential_settings=__ret__.key_vault_credential_settings,
        least_privilege_mode=__ret__.least_privilege_mode,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        server_configurations_management_settings=__ret__.server_configurations_management_settings,
        sql_image_offer=__ret__.sql_image_offer,
        sql_image_sku=__ret__.sql_image_sku,
        sql_management=__ret__.sql_management,
        sql_server_license_type=__ret__.sql_server_license_type,
        sql_virtual_machine_group_resource_id=__ret__.sql_virtual_machine_group_resource_id,
        storage_configuration_settings=__ret__.storage_configuration_settings,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        troubleshooting_status=__ret__.troubleshooting_status,
        type=__ret__.type,
        virtual_machine_resource_id=__ret__.virtual_machine_resource_id,
        wsfc_domain_credentials=__ret__.wsfc_domain_credentials,
        wsfc_static_ip=__ret__.wsfc_static_ip)


@_utilities.lift_output_func(get_sql_virtual_machine)
def get_sql_virtual_machine_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   sql_virtual_machine_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSqlVirtualMachineResult]:
    """
    Gets a SQL virtual machine.


    :param str expand: The child resources to include in the response.
    :param str resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str sql_virtual_machine_name: Name of the SQL virtual machine.
    """
    ...
