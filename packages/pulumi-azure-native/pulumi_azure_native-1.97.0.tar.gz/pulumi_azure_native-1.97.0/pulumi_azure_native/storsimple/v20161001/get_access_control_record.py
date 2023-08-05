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
    'GetAccessControlRecordResult',
    'AwaitableGetAccessControlRecordResult',
    'get_access_control_record',
    'get_access_control_record_output',
]

warnings.warn("""Version 2016-10-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetAccessControlRecordResult:
    """
    The access control record
    """
    def __init__(__self__, id=None, initiator_name=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if initiator_name and not isinstance(initiator_name, str):
            raise TypeError("Expected argument 'initiator_name' to be a str")
        pulumi.set(__self__, "initiator_name", initiator_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="initiatorName")
    def initiator_name(self) -> str:
        """
        The Iscsi initiator name (IQN)
        """
        return pulumi.get(self, "initiator_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type.
        """
        return pulumi.get(self, "type")


class AwaitableGetAccessControlRecordResult(GetAccessControlRecordResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAccessControlRecordResult(
            id=self.id,
            initiator_name=self.initiator_name,
            name=self.name,
            type=self.type)


def get_access_control_record(access_control_record_name: Optional[str] = None,
                              manager_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAccessControlRecordResult:
    """
    Returns the properties of the specified access control record name.


    :param str access_control_record_name: Name of access control record to be fetched.
    :param str manager_name: The manager name
    :param str resource_group_name: The resource group name
    """
    pulumi.log.warn("""get_access_control_record is deprecated: Version 2016-10-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accessControlRecordName'] = access_control_record_name
    __args__['managerName'] = manager_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:storsimple/v20161001:getAccessControlRecord', __args__, opts=opts, typ=GetAccessControlRecordResult).value

    return AwaitableGetAccessControlRecordResult(
        id=__ret__.id,
        initiator_name=__ret__.initiator_name,
        name=__ret__.name,
        type=__ret__.type)


@_utilities.lift_output_func(get_access_control_record)
def get_access_control_record_output(access_control_record_name: Optional[pulumi.Input[str]] = None,
                                     manager_name: Optional[pulumi.Input[str]] = None,
                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAccessControlRecordResult]:
    """
    Returns the properties of the specified access control record name.


    :param str access_control_record_name: Name of access control record to be fetched.
    :param str manager_name: The manager name
    :param str resource_group_name: The resource group name
    """
    pulumi.log.warn("""get_access_control_record is deprecated: Version 2016-10-01 will be removed in v2 of the provider.""")
    ...
