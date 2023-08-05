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
    'ListAccountKeysResult',
    'AwaitableListAccountKeysResult',
    'list_account_keys',
    'list_account_keys_output',
]

@pulumi.output_type
class ListAccountKeysResult:
    """
    The set of keys which can be used to access the Maps REST APIs. Two keys are provided for key rotation without interruption.
    """
    def __init__(__self__, primary_key=None, primary_key_last_updated=None, secondary_key=None, secondary_key_last_updated=None):
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if primary_key_last_updated and not isinstance(primary_key_last_updated, str):
            raise TypeError("Expected argument 'primary_key_last_updated' to be a str")
        pulumi.set(__self__, "primary_key_last_updated", primary_key_last_updated)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)
        if secondary_key_last_updated and not isinstance(secondary_key_last_updated, str):
            raise TypeError("Expected argument 'secondary_key_last_updated' to be a str")
        pulumi.set(__self__, "secondary_key_last_updated", secondary_key_last_updated)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> str:
        """
        The primary key for accessing the Maps REST APIs.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="primaryKeyLastUpdated")
    def primary_key_last_updated(self) -> str:
        """
        The last updated date and time of the primary key.
        """
        return pulumi.get(self, "primary_key_last_updated")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> str:
        """
        The secondary key for accessing the Maps REST APIs.
        """
        return pulumi.get(self, "secondary_key")

    @property
    @pulumi.getter(name="secondaryKeyLastUpdated")
    def secondary_key_last_updated(self) -> str:
        """
        The last updated date and time of the secondary key.
        """
        return pulumi.get(self, "secondary_key_last_updated")


class AwaitableListAccountKeysResult(ListAccountKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListAccountKeysResult(
            primary_key=self.primary_key,
            primary_key_last_updated=self.primary_key_last_updated,
            secondary_key=self.secondary_key,
            secondary_key_last_updated=self.secondary_key_last_updated)


def list_account_keys(account_name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListAccountKeysResult:
    """
    Get the keys to use with the Maps APIs. A key is used to authenticate and authorize access to the Maps REST APIs. Only one key is needed at a time; two are given to provide seamless key regeneration.


    :param str account_name: The name of the Maps Account.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:maps/v20211201preview:listAccountKeys', __args__, opts=opts, typ=ListAccountKeysResult).value

    return AwaitableListAccountKeysResult(
        primary_key=__ret__.primary_key,
        primary_key_last_updated=__ret__.primary_key_last_updated,
        secondary_key=__ret__.secondary_key,
        secondary_key_last_updated=__ret__.secondary_key_last_updated)


@_utilities.lift_output_func(list_account_keys)
def list_account_keys_output(account_name: Optional[pulumi.Input[str]] = None,
                             resource_group_name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListAccountKeysResult]:
    """
    Get the keys to use with the Maps APIs. A key is used to authenticate and authorize access to the Maps REST APIs. Only one key is needed at a time; two are given to provide seamless key regeneration.


    :param str account_name: The name of the Maps Account.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
