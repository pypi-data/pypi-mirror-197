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
    'GetIoMAMPolicyByNameResult',
    'AwaitableGetIoMAMPolicyByNameResult',
    'get_io_mam_policy_by_name',
    'get_io_mam_policy_by_name_output',
]

@pulumi.output_type
class GetIoMAMPolicyByNameResult:
    """
    iOS Policy entity for Intune MAM.
    """
    def __init__(__self__, access_recheck_offline_timeout=None, access_recheck_online_timeout=None, app_sharing_from_level=None, app_sharing_to_level=None, authentication=None, clipboard_sharing_level=None, data_backup=None, description=None, device_compliance=None, file_encryption_level=None, file_sharing_save_as=None, friendly_name=None, group_status=None, id=None, last_modified_time=None, location=None, managed_browser=None, name=None, num_of_apps=None, offline_wipe_timeout=None, pin=None, pin_num_retry=None, tags=None, touch_id=None, type=None):
        if access_recheck_offline_timeout and not isinstance(access_recheck_offline_timeout, str):
            raise TypeError("Expected argument 'access_recheck_offline_timeout' to be a str")
        pulumi.set(__self__, "access_recheck_offline_timeout", access_recheck_offline_timeout)
        if access_recheck_online_timeout and not isinstance(access_recheck_online_timeout, str):
            raise TypeError("Expected argument 'access_recheck_online_timeout' to be a str")
        pulumi.set(__self__, "access_recheck_online_timeout", access_recheck_online_timeout)
        if app_sharing_from_level and not isinstance(app_sharing_from_level, str):
            raise TypeError("Expected argument 'app_sharing_from_level' to be a str")
        pulumi.set(__self__, "app_sharing_from_level", app_sharing_from_level)
        if app_sharing_to_level and not isinstance(app_sharing_to_level, str):
            raise TypeError("Expected argument 'app_sharing_to_level' to be a str")
        pulumi.set(__self__, "app_sharing_to_level", app_sharing_to_level)
        if authentication and not isinstance(authentication, str):
            raise TypeError("Expected argument 'authentication' to be a str")
        pulumi.set(__self__, "authentication", authentication)
        if clipboard_sharing_level and not isinstance(clipboard_sharing_level, str):
            raise TypeError("Expected argument 'clipboard_sharing_level' to be a str")
        pulumi.set(__self__, "clipboard_sharing_level", clipboard_sharing_level)
        if data_backup and not isinstance(data_backup, str):
            raise TypeError("Expected argument 'data_backup' to be a str")
        pulumi.set(__self__, "data_backup", data_backup)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if device_compliance and not isinstance(device_compliance, str):
            raise TypeError("Expected argument 'device_compliance' to be a str")
        pulumi.set(__self__, "device_compliance", device_compliance)
        if file_encryption_level and not isinstance(file_encryption_level, str):
            raise TypeError("Expected argument 'file_encryption_level' to be a str")
        pulumi.set(__self__, "file_encryption_level", file_encryption_level)
        if file_sharing_save_as and not isinstance(file_sharing_save_as, str):
            raise TypeError("Expected argument 'file_sharing_save_as' to be a str")
        pulumi.set(__self__, "file_sharing_save_as", file_sharing_save_as)
        if friendly_name and not isinstance(friendly_name, str):
            raise TypeError("Expected argument 'friendly_name' to be a str")
        pulumi.set(__self__, "friendly_name", friendly_name)
        if group_status and not isinstance(group_status, str):
            raise TypeError("Expected argument 'group_status' to be a str")
        pulumi.set(__self__, "group_status", group_status)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_browser and not isinstance(managed_browser, str):
            raise TypeError("Expected argument 'managed_browser' to be a str")
        pulumi.set(__self__, "managed_browser", managed_browser)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if num_of_apps and not isinstance(num_of_apps, int):
            raise TypeError("Expected argument 'num_of_apps' to be a int")
        pulumi.set(__self__, "num_of_apps", num_of_apps)
        if offline_wipe_timeout and not isinstance(offline_wipe_timeout, str):
            raise TypeError("Expected argument 'offline_wipe_timeout' to be a str")
        pulumi.set(__self__, "offline_wipe_timeout", offline_wipe_timeout)
        if pin and not isinstance(pin, str):
            raise TypeError("Expected argument 'pin' to be a str")
        pulumi.set(__self__, "pin", pin)
        if pin_num_retry and not isinstance(pin_num_retry, int):
            raise TypeError("Expected argument 'pin_num_retry' to be a int")
        pulumi.set(__self__, "pin_num_retry", pin_num_retry)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if touch_id and not isinstance(touch_id, str):
            raise TypeError("Expected argument 'touch_id' to be a str")
        pulumi.set(__self__, "touch_id", touch_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accessRecheckOfflineTimeout")
    def access_recheck_offline_timeout(self) -> Optional[str]:
        return pulumi.get(self, "access_recheck_offline_timeout")

    @property
    @pulumi.getter(name="accessRecheckOnlineTimeout")
    def access_recheck_online_timeout(self) -> Optional[str]:
        return pulumi.get(self, "access_recheck_online_timeout")

    @property
    @pulumi.getter(name="appSharingFromLevel")
    def app_sharing_from_level(self) -> Optional[str]:
        return pulumi.get(self, "app_sharing_from_level")

    @property
    @pulumi.getter(name="appSharingToLevel")
    def app_sharing_to_level(self) -> Optional[str]:
        return pulumi.get(self, "app_sharing_to_level")

    @property
    @pulumi.getter
    def authentication(self) -> Optional[str]:
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter(name="clipboardSharingLevel")
    def clipboard_sharing_level(self) -> Optional[str]:
        return pulumi.get(self, "clipboard_sharing_level")

    @property
    @pulumi.getter(name="dataBackup")
    def data_backup(self) -> Optional[str]:
        return pulumi.get(self, "data_backup")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="deviceCompliance")
    def device_compliance(self) -> Optional[str]:
        return pulumi.get(self, "device_compliance")

    @property
    @pulumi.getter(name="fileEncryptionLevel")
    def file_encryption_level(self) -> Optional[str]:
        return pulumi.get(self, "file_encryption_level")

    @property
    @pulumi.getter(name="fileSharingSaveAs")
    def file_sharing_save_as(self) -> Optional[str]:
        return pulumi.get(self, "file_sharing_save_as")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> str:
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="groupStatus")
    def group_status(self) -> str:
        return pulumi.get(self, "group_status")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> str:
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedBrowser")
    def managed_browser(self) -> Optional[str]:
        return pulumi.get(self, "managed_browser")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="numOfApps")
    def num_of_apps(self) -> int:
        return pulumi.get(self, "num_of_apps")

    @property
    @pulumi.getter(name="offlineWipeTimeout")
    def offline_wipe_timeout(self) -> Optional[str]:
        return pulumi.get(self, "offline_wipe_timeout")

    @property
    @pulumi.getter
    def pin(self) -> Optional[str]:
        return pulumi.get(self, "pin")

    @property
    @pulumi.getter(name="pinNumRetry")
    def pin_num_retry(self) -> Optional[int]:
        return pulumi.get(self, "pin_num_retry")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource Tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="touchId")
    def touch_id(self) -> Optional[str]:
        return pulumi.get(self, "touch_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetIoMAMPolicyByNameResult(GetIoMAMPolicyByNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIoMAMPolicyByNameResult(
            access_recheck_offline_timeout=self.access_recheck_offline_timeout,
            access_recheck_online_timeout=self.access_recheck_online_timeout,
            app_sharing_from_level=self.app_sharing_from_level,
            app_sharing_to_level=self.app_sharing_to_level,
            authentication=self.authentication,
            clipboard_sharing_level=self.clipboard_sharing_level,
            data_backup=self.data_backup,
            description=self.description,
            device_compliance=self.device_compliance,
            file_encryption_level=self.file_encryption_level,
            file_sharing_save_as=self.file_sharing_save_as,
            friendly_name=self.friendly_name,
            group_status=self.group_status,
            id=self.id,
            last_modified_time=self.last_modified_time,
            location=self.location,
            managed_browser=self.managed_browser,
            name=self.name,
            num_of_apps=self.num_of_apps,
            offline_wipe_timeout=self.offline_wipe_timeout,
            pin=self.pin,
            pin_num_retry=self.pin_num_retry,
            tags=self.tags,
            touch_id=self.touch_id,
            type=self.type)


def get_io_mam_policy_by_name(host_name: Optional[str] = None,
                              policy_name: Optional[str] = None,
                              select: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIoMAMPolicyByNameResult:
    """
    Returns Intune iOS policies.


    :param str host_name: Location hostName for the tenant
    :param str policy_name: Unique name for the policy
    :param str select: select specific fields in entity.
    """
    __args__ = dict()
    __args__['hostName'] = host_name
    __args__['policyName'] = policy_name
    __args__['select'] = select
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:intune/v20150114preview:getIoMAMPolicyByName', __args__, opts=opts, typ=GetIoMAMPolicyByNameResult).value

    return AwaitableGetIoMAMPolicyByNameResult(
        access_recheck_offline_timeout=__ret__.access_recheck_offline_timeout,
        access_recheck_online_timeout=__ret__.access_recheck_online_timeout,
        app_sharing_from_level=__ret__.app_sharing_from_level,
        app_sharing_to_level=__ret__.app_sharing_to_level,
        authentication=__ret__.authentication,
        clipboard_sharing_level=__ret__.clipboard_sharing_level,
        data_backup=__ret__.data_backup,
        description=__ret__.description,
        device_compliance=__ret__.device_compliance,
        file_encryption_level=__ret__.file_encryption_level,
        file_sharing_save_as=__ret__.file_sharing_save_as,
        friendly_name=__ret__.friendly_name,
        group_status=__ret__.group_status,
        id=__ret__.id,
        last_modified_time=__ret__.last_modified_time,
        location=__ret__.location,
        managed_browser=__ret__.managed_browser,
        name=__ret__.name,
        num_of_apps=__ret__.num_of_apps,
        offline_wipe_timeout=__ret__.offline_wipe_timeout,
        pin=__ret__.pin,
        pin_num_retry=__ret__.pin_num_retry,
        tags=__ret__.tags,
        touch_id=__ret__.touch_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_io_mam_policy_by_name)
def get_io_mam_policy_by_name_output(host_name: Optional[pulumi.Input[str]] = None,
                                     policy_name: Optional[pulumi.Input[str]] = None,
                                     select: Optional[pulumi.Input[Optional[str]]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIoMAMPolicyByNameResult]:
    """
    Returns Intune iOS policies.


    :param str host_name: Location hostName for the tenant
    :param str policy_name: Unique name for the policy
    :param str select: select specific fields in entity.
    """
    ...
