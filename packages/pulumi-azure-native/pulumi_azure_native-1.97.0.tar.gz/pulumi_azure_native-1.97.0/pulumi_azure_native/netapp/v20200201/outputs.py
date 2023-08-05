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
    'ActiveDirectoryResponse',
    'ExportPolicyRuleResponse',
    'MountTargetPropertiesResponse',
    'ReplicationObjectResponse',
    'VolumePropertiesResponseDataProtection',
    'VolumePropertiesResponseExportPolicy',
    'VolumeSnapshotPropertiesResponse',
]

@pulumi.output_type
class ActiveDirectoryResponse(dict):
    """
    Active Directory
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "activeDirectoryId":
            suggest = "active_directory_id"
        elif key == "backupOperators":
            suggest = "backup_operators"
        elif key == "organizationalUnit":
            suggest = "organizational_unit"
        elif key == "smbServerName":
            suggest = "smb_server_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ActiveDirectoryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ActiveDirectoryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ActiveDirectoryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 active_directory_id: Optional[str] = None,
                 backup_operators: Optional[Sequence[str]] = None,
                 dns: Optional[str] = None,
                 domain: Optional[str] = None,
                 organizational_unit: Optional[str] = None,
                 password: Optional[str] = None,
                 site: Optional[str] = None,
                 smb_server_name: Optional[str] = None,
                 status: Optional[str] = None,
                 username: Optional[str] = None):
        """
        Active Directory
        :param str active_directory_id: Id of the Active Directory
        :param Sequence[str] backup_operators: Users to be added to the Built-in Backup Operator active directory group. A list of unique usernames without domain specifier
        :param str dns: Comma separated list of DNS server IP addresses (IPv4 only) for the Active Directory domain
        :param str domain: Name of the Active Directory domain
        :param str organizational_unit: The Organizational Unit (OU) within the Windows Active Directory
        :param str password: Plain text password of Active Directory domain administrator
        :param str site: The Active Directory site the service will limit Domain Controller discovery to
        :param str smb_server_name: NetBIOS name of the SMB server. This name will be registered as a computer account in the AD and used to mount volumes
        :param str status: Status of the Active Directory
        :param str username: Username of Active Directory domain administrator
        """
        if active_directory_id is None:
            active_directory_id = 'guid id'
        if active_directory_id is not None:
            pulumi.set(__self__, "active_directory_id", active_directory_id)
        if backup_operators is not None:
            pulumi.set(__self__, "backup_operators", backup_operators)
        if dns is not None:
            pulumi.set(__self__, "dns", dns)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if organizational_unit is None:
            organizational_unit = 'CN=Computers'
        if organizational_unit is not None:
            pulumi.set(__self__, "organizational_unit", organizational_unit)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if site is not None:
            pulumi.set(__self__, "site", site)
        if smb_server_name is not None:
            pulumi.set(__self__, "smb_server_name", smb_server_name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="activeDirectoryId")
    def active_directory_id(self) -> Optional[str]:
        """
        Id of the Active Directory
        """
        return pulumi.get(self, "active_directory_id")

    @property
    @pulumi.getter(name="backupOperators")
    def backup_operators(self) -> Optional[Sequence[str]]:
        """
        Users to be added to the Built-in Backup Operator active directory group. A list of unique usernames without domain specifier
        """
        return pulumi.get(self, "backup_operators")

    @property
    @pulumi.getter
    def dns(self) -> Optional[str]:
        """
        Comma separated list of DNS server IP addresses (IPv4 only) for the Active Directory domain
        """
        return pulumi.get(self, "dns")

    @property
    @pulumi.getter
    def domain(self) -> Optional[str]:
        """
        Name of the Active Directory domain
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="organizationalUnit")
    def organizational_unit(self) -> Optional[str]:
        """
        The Organizational Unit (OU) within the Windows Active Directory
        """
        return pulumi.get(self, "organizational_unit")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        Plain text password of Active Directory domain administrator
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def site(self) -> Optional[str]:
        """
        The Active Directory site the service will limit Domain Controller discovery to
        """
        return pulumi.get(self, "site")

    @property
    @pulumi.getter(name="smbServerName")
    def smb_server_name(self) -> Optional[str]:
        """
        NetBIOS name of the SMB server. This name will be registered as a computer account in the AD and used to mount volumes
        """
        return pulumi.get(self, "smb_server_name")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Status of the Active Directory
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def username(self) -> Optional[str]:
        """
        Username of Active Directory domain administrator
        """
        return pulumi.get(self, "username")


@pulumi.output_type
class ExportPolicyRuleResponse(dict):
    """
    Volume Export Policy Rule
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "allowedClients":
            suggest = "allowed_clients"
        elif key == "ruleIndex":
            suggest = "rule_index"
        elif key == "unixReadOnly":
            suggest = "unix_read_only"
        elif key == "unixReadWrite":
            suggest = "unix_read_write"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ExportPolicyRuleResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ExportPolicyRuleResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ExportPolicyRuleResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allowed_clients: Optional[str] = None,
                 cifs: Optional[bool] = None,
                 nfsv3: Optional[bool] = None,
                 nfsv41: Optional[bool] = None,
                 rule_index: Optional[int] = None,
                 unix_read_only: Optional[bool] = None,
                 unix_read_write: Optional[bool] = None):
        """
        Volume Export Policy Rule
        :param str allowed_clients: Client ingress specification as comma separated string with IPv4 CIDRs, IPv4 host addresses and host names
        :param bool cifs: Allows CIFS protocol
        :param bool nfsv3: Allows NFSv3 protocol. Enable only for NFSv3 type volumes
        :param bool nfsv41: Allows NFSv4.1 protocol. Enable only for NFSv4.1 type volumes
        :param int rule_index: Order index
        :param bool unix_read_only: Read only access
        :param bool unix_read_write: Read and write access
        """
        if allowed_clients is not None:
            pulumi.set(__self__, "allowed_clients", allowed_clients)
        if cifs is None:
            cifs = False
        if cifs is not None:
            pulumi.set(__self__, "cifs", cifs)
        if nfsv3 is not None:
            pulumi.set(__self__, "nfsv3", nfsv3)
        if nfsv41 is not None:
            pulumi.set(__self__, "nfsv41", nfsv41)
        if rule_index is not None:
            pulumi.set(__self__, "rule_index", rule_index)
        if unix_read_only is not None:
            pulumi.set(__self__, "unix_read_only", unix_read_only)
        if unix_read_write is not None:
            pulumi.set(__self__, "unix_read_write", unix_read_write)

    @property
    @pulumi.getter(name="allowedClients")
    def allowed_clients(self) -> Optional[str]:
        """
        Client ingress specification as comma separated string with IPv4 CIDRs, IPv4 host addresses and host names
        """
        return pulumi.get(self, "allowed_clients")

    @property
    @pulumi.getter
    def cifs(self) -> Optional[bool]:
        """
        Allows CIFS protocol
        """
        return pulumi.get(self, "cifs")

    @property
    @pulumi.getter
    def nfsv3(self) -> Optional[bool]:
        """
        Allows NFSv3 protocol. Enable only for NFSv3 type volumes
        """
        return pulumi.get(self, "nfsv3")

    @property
    @pulumi.getter
    def nfsv41(self) -> Optional[bool]:
        """
        Allows NFSv4.1 protocol. Enable only for NFSv4.1 type volumes
        """
        return pulumi.get(self, "nfsv41")

    @property
    @pulumi.getter(name="ruleIndex")
    def rule_index(self) -> Optional[int]:
        """
        Order index
        """
        return pulumi.get(self, "rule_index")

    @property
    @pulumi.getter(name="unixReadOnly")
    def unix_read_only(self) -> Optional[bool]:
        """
        Read only access
        """
        return pulumi.get(self, "unix_read_only")

    @property
    @pulumi.getter(name="unixReadWrite")
    def unix_read_write(self) -> Optional[bool]:
        """
        Read and write access
        """
        return pulumi.get(self, "unix_read_write")


@pulumi.output_type
class MountTargetPropertiesResponse(dict):
    """
    Mount target properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "fileSystemId":
            suggest = "file_system_id"
        elif key == "ipAddress":
            suggest = "ip_address"
        elif key == "mountTargetId":
            suggest = "mount_target_id"
        elif key == "endIp":
            suggest = "end_ip"
        elif key == "smbServerFqdn":
            suggest = "smb_server_fqdn"
        elif key == "startIp":
            suggest = "start_ip"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MountTargetPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MountTargetPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MountTargetPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 file_system_id: str,
                 ip_address: str,
                 mount_target_id: str,
                 end_ip: Optional[str] = None,
                 gateway: Optional[str] = None,
                 netmask: Optional[str] = None,
                 smb_server_fqdn: Optional[str] = None,
                 start_ip: Optional[str] = None,
                 subnet: Optional[str] = None):
        """
        Mount target properties
        :param str file_system_id: UUID v4 used to identify the MountTarget
        :param str ip_address: The mount target's IPv4 address
        :param str mount_target_id: UUID v4 used to identify the MountTarget
        :param str end_ip: The end of IPv4 address range to use when creating a new mount target
        :param str gateway: The gateway of the IPv4 address range to use when creating a new mount target
        :param str netmask: The netmask of the IPv4 address range to use when creating a new mount target
        :param str smb_server_fqdn: The SMB server's Fully Qualified Domain Name, FQDN
        :param str start_ip: The start of IPv4 address range to use when creating a new mount target
        :param str subnet: The subnet
        """
        pulumi.set(__self__, "file_system_id", file_system_id)
        pulumi.set(__self__, "ip_address", ip_address)
        pulumi.set(__self__, "mount_target_id", mount_target_id)
        if end_ip is not None:
            pulumi.set(__self__, "end_ip", end_ip)
        if gateway is not None:
            pulumi.set(__self__, "gateway", gateway)
        if netmask is not None:
            pulumi.set(__self__, "netmask", netmask)
        if smb_server_fqdn is not None:
            pulumi.set(__self__, "smb_server_fqdn", smb_server_fqdn)
        if start_ip is not None:
            pulumi.set(__self__, "start_ip", start_ip)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> str:
        """
        UUID v4 used to identify the MountTarget
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> str:
        """
        The mount target's IPv4 address
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="mountTargetId")
    def mount_target_id(self) -> str:
        """
        UUID v4 used to identify the MountTarget
        """
        return pulumi.get(self, "mount_target_id")

    @property
    @pulumi.getter(name="endIp")
    def end_ip(self) -> Optional[str]:
        """
        The end of IPv4 address range to use when creating a new mount target
        """
        return pulumi.get(self, "end_ip")

    @property
    @pulumi.getter
    def gateway(self) -> Optional[str]:
        """
        The gateway of the IPv4 address range to use when creating a new mount target
        """
        return pulumi.get(self, "gateway")

    @property
    @pulumi.getter
    def netmask(self) -> Optional[str]:
        """
        The netmask of the IPv4 address range to use when creating a new mount target
        """
        return pulumi.get(self, "netmask")

    @property
    @pulumi.getter(name="smbServerFqdn")
    def smb_server_fqdn(self) -> Optional[str]:
        """
        The SMB server's Fully Qualified Domain Name, FQDN
        """
        return pulumi.get(self, "smb_server_fqdn")

    @property
    @pulumi.getter(name="startIp")
    def start_ip(self) -> Optional[str]:
        """
        The start of IPv4 address range to use when creating a new mount target
        """
        return pulumi.get(self, "start_ip")

    @property
    @pulumi.getter
    def subnet(self) -> Optional[str]:
        """
        The subnet
        """
        return pulumi.get(self, "subnet")


@pulumi.output_type
class ReplicationObjectResponse(dict):
    """
    Replication properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "remoteVolumeResourceId":
            suggest = "remote_volume_resource_id"
        elif key == "replicationSchedule":
            suggest = "replication_schedule"
        elif key == "endpointType":
            suggest = "endpoint_type"
        elif key == "remoteVolumeRegion":
            suggest = "remote_volume_region"
        elif key == "replicationId":
            suggest = "replication_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ReplicationObjectResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ReplicationObjectResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ReplicationObjectResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 remote_volume_resource_id: str,
                 replication_schedule: str,
                 endpoint_type: Optional[str] = None,
                 remote_volume_region: Optional[str] = None,
                 replication_id: Optional[str] = None):
        """
        Replication properties
        :param str remote_volume_resource_id: The resource ID of the remote volume.
        :param str replication_schedule: Schedule
        :param str endpoint_type: Indicates whether the local volume is the source or destination for the Volume Replication
        :param str remote_volume_region: The remote region for the other end of the Volume Replication.
        :param str replication_id: Id
        """
        pulumi.set(__self__, "remote_volume_resource_id", remote_volume_resource_id)
        pulumi.set(__self__, "replication_schedule", replication_schedule)
        if endpoint_type is not None:
            pulumi.set(__self__, "endpoint_type", endpoint_type)
        if remote_volume_region is not None:
            pulumi.set(__self__, "remote_volume_region", remote_volume_region)
        if replication_id is not None:
            pulumi.set(__self__, "replication_id", replication_id)

    @property
    @pulumi.getter(name="remoteVolumeResourceId")
    def remote_volume_resource_id(self) -> str:
        """
        The resource ID of the remote volume.
        """
        return pulumi.get(self, "remote_volume_resource_id")

    @property
    @pulumi.getter(name="replicationSchedule")
    def replication_schedule(self) -> str:
        """
        Schedule
        """
        return pulumi.get(self, "replication_schedule")

    @property
    @pulumi.getter(name="endpointType")
    def endpoint_type(self) -> Optional[str]:
        """
        Indicates whether the local volume is the source or destination for the Volume Replication
        """
        return pulumi.get(self, "endpoint_type")

    @property
    @pulumi.getter(name="remoteVolumeRegion")
    def remote_volume_region(self) -> Optional[str]:
        """
        The remote region for the other end of the Volume Replication.
        """
        return pulumi.get(self, "remote_volume_region")

    @property
    @pulumi.getter(name="replicationId")
    def replication_id(self) -> Optional[str]:
        """
        Id
        """
        return pulumi.get(self, "replication_id")


@pulumi.output_type
class VolumePropertiesResponseDataProtection(dict):
    """
    DataProtection type volumes include an object containing details of the replication
    """
    def __init__(__self__, *,
                 replication: Optional['outputs.ReplicationObjectResponse'] = None,
                 snapshot: Optional['outputs.VolumeSnapshotPropertiesResponse'] = None):
        """
        DataProtection type volumes include an object containing details of the replication
        :param 'ReplicationObjectResponse' replication: Replication properties
        :param 'VolumeSnapshotPropertiesResponse' snapshot: Snapshot properties.
        """
        if replication is not None:
            pulumi.set(__self__, "replication", replication)
        if snapshot is not None:
            pulumi.set(__self__, "snapshot", snapshot)

    @property
    @pulumi.getter
    def replication(self) -> Optional['outputs.ReplicationObjectResponse']:
        """
        Replication properties
        """
        return pulumi.get(self, "replication")

    @property
    @pulumi.getter
    def snapshot(self) -> Optional['outputs.VolumeSnapshotPropertiesResponse']:
        """
        Snapshot properties.
        """
        return pulumi.get(self, "snapshot")


@pulumi.output_type
class VolumePropertiesResponseExportPolicy(dict):
    """
    Set of export policy rules
    """
    def __init__(__self__, *,
                 rules: Optional[Sequence['outputs.ExportPolicyRuleResponse']] = None):
        """
        Set of export policy rules
        :param Sequence['ExportPolicyRuleResponse'] rules: Export policy rule
        """
        if rules is not None:
            pulumi.set(__self__, "rules", rules)

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.ExportPolicyRuleResponse']]:
        """
        Export policy rule
        """
        return pulumi.get(self, "rules")


@pulumi.output_type
class VolumeSnapshotPropertiesResponse(dict):
    """
    Volume Snapshot Properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "snapshotPolicyId":
            suggest = "snapshot_policy_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VolumeSnapshotPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VolumeSnapshotPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VolumeSnapshotPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 snapshot_policy_id: Optional[str] = None):
        """
        Volume Snapshot Properties
        :param str snapshot_policy_id: Snapshot Policy ResourceId
        """
        if snapshot_policy_id is not None:
            pulumi.set(__self__, "snapshot_policy_id", snapshot_policy_id)

    @property
    @pulumi.getter(name="snapshotPolicyId")
    def snapshot_policy_id(self) -> Optional[str]:
        """
        Snapshot Policy ResourceId
        """
        return pulumi.get(self, "snapshot_policy_id")


