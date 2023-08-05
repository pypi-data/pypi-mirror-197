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
    'GetAssetEncryptionKeyResult',
    'AwaitableGetAssetEncryptionKeyResult',
    'get_asset_encryption_key',
    'get_asset_encryption_key_output',
]

@pulumi.output_type
class GetAssetEncryptionKeyResult:
    """
    Data needed to decrypt asset files encrypted with legacy storage encryption.
    """
    def __init__(__self__, asset_file_encryption_metadata=None, key=None):
        if asset_file_encryption_metadata and not isinstance(asset_file_encryption_metadata, list):
            raise TypeError("Expected argument 'asset_file_encryption_metadata' to be a list")
        pulumi.set(__self__, "asset_file_encryption_metadata", asset_file_encryption_metadata)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter(name="assetFileEncryptionMetadata")
    def asset_file_encryption_metadata(self) -> Optional[Sequence['outputs.AssetFileEncryptionMetadataResponse']]:
        """
        Asset File encryption metadata.
        """
        return pulumi.get(self, "asset_file_encryption_metadata")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        The Asset File storage encryption key.
        """
        return pulumi.get(self, "key")


class AwaitableGetAssetEncryptionKeyResult(GetAssetEncryptionKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAssetEncryptionKeyResult(
            asset_file_encryption_metadata=self.asset_file_encryption_metadata,
            key=self.key)


def get_asset_encryption_key(account_name: Optional[str] = None,
                             asset_name: Optional[str] = None,
                             resource_group_name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAssetEncryptionKeyResult:
    """
    Gets the Asset storage encryption keys used to decrypt content created by version 2 of the Media Services API


    :param str account_name: The Media Services account name.
    :param str asset_name: The Asset name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['assetName'] = asset_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:media/v20200501:getAssetEncryptionKey', __args__, opts=opts, typ=GetAssetEncryptionKeyResult).value

    return AwaitableGetAssetEncryptionKeyResult(
        asset_file_encryption_metadata=__ret__.asset_file_encryption_metadata,
        key=__ret__.key)


@_utilities.lift_output_func(get_asset_encryption_key)
def get_asset_encryption_key_output(account_name: Optional[pulumi.Input[str]] = None,
                                    asset_name: Optional[pulumi.Input[str]] = None,
                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAssetEncryptionKeyResult]:
    """
    Gets the Asset storage encryption keys used to decrypt content created by version 2 of the Media Services API


    :param str account_name: The Media Services account name.
    :param str asset_name: The Asset name.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    ...
