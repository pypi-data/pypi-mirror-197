# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'StorageAccountPropertiesResponse',
]

@pulumi.output_type
class StorageAccountPropertiesResponse(dict):
    """
    The properties of a storage account for a machine learning team account.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "accessKey":
            suggest = "access_key"
        elif key == "storageAccountId":
            suggest = "storage_account_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StorageAccountPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StorageAccountPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StorageAccountPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 access_key: str,
                 storage_account_id: str):
        """
        The properties of a storage account for a machine learning team account.
        :param str access_key: The access key to the storage account.
        :param str storage_account_id: The fully qualified arm Id of the storage account.
        """
        pulumi.set(__self__, "access_key", access_key)
        pulumi.set(__self__, "storage_account_id", storage_account_id)

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> str:
        """
        The access key to the storage account.
        """
        return pulumi.get(self, "access_key")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> str:
        """
        The fully qualified arm Id of the storage account.
        """
        return pulumi.get(self, "storage_account_id")


