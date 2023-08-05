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
    'GetVolumeResult',
    'AwaitableGetVolumeResult',
    'get_volume',
    'get_volume_output',
]

warnings.warn("""Version 2019-11-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetVolumeResult:
    """
    Volume resource
    """
    def __init__(__self__, baremetal_tenant_id=None, creation_token=None, data_protection=None, export_policy=None, file_system_id=None, id=None, is_restoring=None, location=None, mount_targets=None, name=None, protocol_types=None, provisioning_state=None, service_level=None, snapshot_id=None, subnet_id=None, tags=None, type=None, usage_threshold=None, used_bytes=None, volume_type=None):
        if baremetal_tenant_id and not isinstance(baremetal_tenant_id, str):
            raise TypeError("Expected argument 'baremetal_tenant_id' to be a str")
        pulumi.set(__self__, "baremetal_tenant_id", baremetal_tenant_id)
        if creation_token and not isinstance(creation_token, str):
            raise TypeError("Expected argument 'creation_token' to be a str")
        pulumi.set(__self__, "creation_token", creation_token)
        if data_protection and not isinstance(data_protection, dict):
            raise TypeError("Expected argument 'data_protection' to be a dict")
        pulumi.set(__self__, "data_protection", data_protection)
        if export_policy and not isinstance(export_policy, dict):
            raise TypeError("Expected argument 'export_policy' to be a dict")
        pulumi.set(__self__, "export_policy", export_policy)
        if file_system_id and not isinstance(file_system_id, str):
            raise TypeError("Expected argument 'file_system_id' to be a str")
        pulumi.set(__self__, "file_system_id", file_system_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_restoring and not isinstance(is_restoring, bool):
            raise TypeError("Expected argument 'is_restoring' to be a bool")
        pulumi.set(__self__, "is_restoring", is_restoring)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if mount_targets and not isinstance(mount_targets, list):
            raise TypeError("Expected argument 'mount_targets' to be a list")
        pulumi.set(__self__, "mount_targets", mount_targets)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if protocol_types and not isinstance(protocol_types, list):
            raise TypeError("Expected argument 'protocol_types' to be a list")
        pulumi.set(__self__, "protocol_types", protocol_types)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_level and not isinstance(service_level, str):
            raise TypeError("Expected argument 'service_level' to be a str")
        pulumi.set(__self__, "service_level", service_level)
        if snapshot_id and not isinstance(snapshot_id, str):
            raise TypeError("Expected argument 'snapshot_id' to be a str")
        pulumi.set(__self__, "snapshot_id", snapshot_id)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if usage_threshold and not isinstance(usage_threshold, float):
            raise TypeError("Expected argument 'usage_threshold' to be a float")
        pulumi.set(__self__, "usage_threshold", usage_threshold)
        if used_bytes and not isinstance(used_bytes, float):
            raise TypeError("Expected argument 'used_bytes' to be a float")
        pulumi.set(__self__, "used_bytes", used_bytes)
        if volume_type and not isinstance(volume_type, str):
            raise TypeError("Expected argument 'volume_type' to be a str")
        pulumi.set(__self__, "volume_type", volume_type)

    @property
    @pulumi.getter(name="baremetalTenantId")
    def baremetal_tenant_id(self) -> str:
        """
        Unique Baremetal Tenant Identifier.
        """
        return pulumi.get(self, "baremetal_tenant_id")

    @property
    @pulumi.getter(name="creationToken")
    def creation_token(self) -> str:
        """
        A unique file path for the volume. Used when creating mount targets
        """
        return pulumi.get(self, "creation_token")

    @property
    @pulumi.getter(name="dataProtection")
    def data_protection(self) -> Optional['outputs.VolumePropertiesResponseDataProtection']:
        """
        DataProtection type volumes include an object containing details of the replication
        """
        return pulumi.get(self, "data_protection")

    @property
    @pulumi.getter(name="exportPolicy")
    def export_policy(self) -> Optional['outputs.VolumePropertiesResponseExportPolicy']:
        """
        Set of export policy rules
        """
        return pulumi.get(self, "export_policy")

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> str:
        """
        Unique FileSystem Identifier.
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isRestoring")
    def is_restoring(self) -> Optional[bool]:
        """
        Restoring
        """
        return pulumi.get(self, "is_restoring")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="mountTargets")
    def mount_targets(self) -> Sequence['outputs.MountTargetPropertiesResponse']:
        """
        List of mount targets
        """
        return pulumi.get(self, "mount_targets")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="protocolTypes")
    def protocol_types(self) -> Optional[Sequence[str]]:
        """
        Set of protocol types, default NFSv3, CIFS for SMB protocol
        """
        return pulumi.get(self, "protocol_types")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceLevel")
    def service_level(self) -> Optional[str]:
        """
        The service level of the file system
        """
        return pulumi.get(self, "service_level")

    @property
    @pulumi.getter(name="snapshotId")
    def snapshot_id(self) -> Optional[str]:
        """
        UUID v4 or resource identifier used to identify the Snapshot.
        """
        return pulumi.get(self, "snapshot_id")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        """
        The Azure Resource URI for a delegated subnet. Must have the delegation Microsoft.NetApp/volumes
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usageThreshold")
    def usage_threshold(self) -> float:
        """
        Maximum storage quota allowed for a file system in bytes. This is a soft quota used for alerting only. Minimum size is 100 GiB. Upper limit is 100TiB. Specified in bytes.
        """
        return pulumi.get(self, "usage_threshold")

    @property
    @pulumi.getter(name="usedBytes")
    def used_bytes(self) -> float:
        """
        Resource size in bytes, current storage usage for the volume in bytes
        """
        return pulumi.get(self, "used_bytes")

    @property
    @pulumi.getter(name="volumeType")
    def volume_type(self) -> Optional[str]:
        """
        What type of volume is this
        """
        return pulumi.get(self, "volume_type")


class AwaitableGetVolumeResult(GetVolumeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVolumeResult(
            baremetal_tenant_id=self.baremetal_tenant_id,
            creation_token=self.creation_token,
            data_protection=self.data_protection,
            export_policy=self.export_policy,
            file_system_id=self.file_system_id,
            id=self.id,
            is_restoring=self.is_restoring,
            location=self.location,
            mount_targets=self.mount_targets,
            name=self.name,
            protocol_types=self.protocol_types,
            provisioning_state=self.provisioning_state,
            service_level=self.service_level,
            snapshot_id=self.snapshot_id,
            subnet_id=self.subnet_id,
            tags=self.tags,
            type=self.type,
            usage_threshold=self.usage_threshold,
            used_bytes=self.used_bytes,
            volume_type=self.volume_type)


def get_volume(account_name: Optional[str] = None,
               pool_name: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               volume_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVolumeResult:
    """
    Get the details of the specified volume


    :param str account_name: The name of the NetApp account
    :param str pool_name: The name of the capacity pool
    :param str resource_group_name: The name of the resource group.
    :param str volume_name: The name of the volume
    """
    pulumi.log.warn("""get_volume is deprecated: Version 2019-11-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['poolName'] = pool_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['volumeName'] = volume_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:netapp/v20191101:getVolume', __args__, opts=opts, typ=GetVolumeResult).value

    return AwaitableGetVolumeResult(
        baremetal_tenant_id=__ret__.baremetal_tenant_id,
        creation_token=__ret__.creation_token,
        data_protection=__ret__.data_protection,
        export_policy=__ret__.export_policy,
        file_system_id=__ret__.file_system_id,
        id=__ret__.id,
        is_restoring=__ret__.is_restoring,
        location=__ret__.location,
        mount_targets=__ret__.mount_targets,
        name=__ret__.name,
        protocol_types=__ret__.protocol_types,
        provisioning_state=__ret__.provisioning_state,
        service_level=__ret__.service_level,
        snapshot_id=__ret__.snapshot_id,
        subnet_id=__ret__.subnet_id,
        tags=__ret__.tags,
        type=__ret__.type,
        usage_threshold=__ret__.usage_threshold,
        used_bytes=__ret__.used_bytes,
        volume_type=__ret__.volume_type)


@_utilities.lift_output_func(get_volume)
def get_volume_output(account_name: Optional[pulumi.Input[str]] = None,
                      pool_name: Optional[pulumi.Input[str]] = None,
                      resource_group_name: Optional[pulumi.Input[str]] = None,
                      volume_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVolumeResult]:
    """
    Get the details of the specified volume


    :param str account_name: The name of the NetApp account
    :param str pool_name: The name of the capacity pool
    :param str resource_group_name: The name of the resource group.
    :param str volume_name: The name of the volume
    """
    pulumi.log.warn("""get_volume is deprecated: Version 2019-11-01 will be removed in v2 of the provider.""")
    ...
