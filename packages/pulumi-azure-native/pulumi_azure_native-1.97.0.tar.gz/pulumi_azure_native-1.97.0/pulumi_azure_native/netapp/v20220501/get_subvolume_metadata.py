# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetSubvolumeMetadataResult',
    'AwaitableGetSubvolumeMetadataResult',
    'get_subvolume_metadata',
    'get_subvolume_metadata_output',
]

@pulumi.output_type
class GetSubvolumeMetadataResult:
    """
    Result of the post subvolume and action is to get metadata of the subvolume.
    """
    def __init__(__self__, accessed_time_stamp=None, bytes_used=None, changed_time_stamp=None, creation_time_stamp=None, id=None, modified_time_stamp=None, name=None, parent_path=None, path=None, permissions=None, provisioning_state=None, size=None, type=None):
        if accessed_time_stamp and not isinstance(accessed_time_stamp, str):
            raise TypeError("Expected argument 'accessed_time_stamp' to be a str")
        pulumi.set(__self__, "accessed_time_stamp", accessed_time_stamp)
        if bytes_used and not isinstance(bytes_used, float):
            raise TypeError("Expected argument 'bytes_used' to be a float")
        pulumi.set(__self__, "bytes_used", bytes_used)
        if changed_time_stamp and not isinstance(changed_time_stamp, str):
            raise TypeError("Expected argument 'changed_time_stamp' to be a str")
        pulumi.set(__self__, "changed_time_stamp", changed_time_stamp)
        if creation_time_stamp and not isinstance(creation_time_stamp, str):
            raise TypeError("Expected argument 'creation_time_stamp' to be a str")
        pulumi.set(__self__, "creation_time_stamp", creation_time_stamp)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if modified_time_stamp and not isinstance(modified_time_stamp, str):
            raise TypeError("Expected argument 'modified_time_stamp' to be a str")
        pulumi.set(__self__, "modified_time_stamp", modified_time_stamp)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parent_path and not isinstance(parent_path, str):
            raise TypeError("Expected argument 'parent_path' to be a str")
        pulumi.set(__self__, "parent_path", parent_path)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if permissions and not isinstance(permissions, str):
            raise TypeError("Expected argument 'permissions' to be a str")
        pulumi.set(__self__, "permissions", permissions)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if size and not isinstance(size, float):
            raise TypeError("Expected argument 'size' to be a float")
        pulumi.set(__self__, "size", size)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accessedTimeStamp")
    def accessed_time_stamp(self) -> Optional[str]:
        """
        Most recent access time and date
        """
        return pulumi.get(self, "accessed_time_stamp")

    @property
    @pulumi.getter(name="bytesUsed")
    def bytes_used(self) -> Optional[float]:
        """
        Bytes used
        """
        return pulumi.get(self, "bytes_used")

    @property
    @pulumi.getter(name="changedTimeStamp")
    def changed_time_stamp(self) -> Optional[str]:
        """
        Most recent change time and date
        """
        return pulumi.get(self, "changed_time_stamp")

    @property
    @pulumi.getter(name="creationTimeStamp")
    def creation_time_stamp(self) -> Optional[str]:
        """
        Creation time and date
        """
        return pulumi.get(self, "creation_time_stamp")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="modifiedTimeStamp")
    def modified_time_stamp(self) -> Optional[str]:
        """
        Most recent modification time and date
        """
        return pulumi.get(self, "modified_time_stamp")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="parentPath")
    def parent_path(self) -> Optional[str]:
        """
        Path to the parent subvolume
        """
        return pulumi.get(self, "parent_path")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        Path to the subvolume
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def permissions(self) -> Optional[str]:
        """
        Permissions of the subvolume
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def size(self) -> Optional[float]:
        """
        Size of subvolume
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetSubvolumeMetadataResult(GetSubvolumeMetadataResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubvolumeMetadataResult(
            accessed_time_stamp=self.accessed_time_stamp,
            bytes_used=self.bytes_used,
            changed_time_stamp=self.changed_time_stamp,
            creation_time_stamp=self.creation_time_stamp,
            id=self.id,
            modified_time_stamp=self.modified_time_stamp,
            name=self.name,
            parent_path=self.parent_path,
            path=self.path,
            permissions=self.permissions,
            provisioning_state=self.provisioning_state,
            size=self.size,
            type=self.type)


def get_subvolume_metadata(account_name: Optional[str] = None,
                           pool_name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           subvolume_name: Optional[str] = None,
                           volume_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubvolumeMetadataResult:
    """
    Get details of the specified subvolume


    :param str account_name: The name of the NetApp account
    :param str pool_name: The name of the capacity pool
    :param str resource_group_name: The name of the resource group.
    :param str subvolume_name: The name of the subvolume.
    :param str volume_name: The name of the volume
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['poolName'] = pool_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['subvolumeName'] = subvolume_name
    __args__['volumeName'] = volume_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:netapp/v20220501:getSubvolumeMetadata', __args__, opts=opts, typ=GetSubvolumeMetadataResult).value

    return AwaitableGetSubvolumeMetadataResult(
        accessed_time_stamp=__ret__.accessed_time_stamp,
        bytes_used=__ret__.bytes_used,
        changed_time_stamp=__ret__.changed_time_stamp,
        creation_time_stamp=__ret__.creation_time_stamp,
        id=__ret__.id,
        modified_time_stamp=__ret__.modified_time_stamp,
        name=__ret__.name,
        parent_path=__ret__.parent_path,
        path=__ret__.path,
        permissions=__ret__.permissions,
        provisioning_state=__ret__.provisioning_state,
        size=__ret__.size,
        type=__ret__.type)


@_utilities.lift_output_func(get_subvolume_metadata)
def get_subvolume_metadata_output(account_name: Optional[pulumi.Input[str]] = None,
                                  pool_name: Optional[pulumi.Input[str]] = None,
                                  resource_group_name: Optional[pulumi.Input[str]] = None,
                                  subvolume_name: Optional[pulumi.Input[str]] = None,
                                  volume_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSubvolumeMetadataResult]:
    """
    Get details of the specified subvolume


    :param str account_name: The name of the NetApp account
    :param str pool_name: The name of the capacity pool
    :param str resource_group_name: The name of the resource group.
    :param str subvolume_name: The name of the subvolume.
    :param str volume_name: The name of the volume
    """
    ...
