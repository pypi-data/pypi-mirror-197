# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'ApplicationPackageResponse',
    'AutoStoragePropertiesResponse',
    'KeyVaultReferenceResponse',
]

@pulumi.output_type
class ApplicationPackageResponse(dict):
    """
    An application package which represents a particular version of an application.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastActivationTime":
            suggest = "last_activation_time"
        elif key == "storageUrl":
            suggest = "storage_url"
        elif key == "storageUrlExpiry":
            suggest = "storage_url_expiry"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ApplicationPackageResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ApplicationPackageResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ApplicationPackageResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 format: str,
                 id: str,
                 last_activation_time: str,
                 state: str,
                 storage_url: str,
                 storage_url_expiry: str,
                 version: str):
        """
        An application package which represents a particular version of an application.
        :param str format: The format of the application package, if the package is active.
        :param str id: The ID of the application.
        :param str last_activation_time: The time at which the package was last activated, if the package is active.
        :param str state: The current state of the application package.
        :param str storage_url: The URL for the application package in Azure Storage.
        :param str storage_url_expiry: The UTC time at which the Azure Storage URL will expire.
        :param str version: The version of the application package. 
        """
        pulumi.set(__self__, "format", format)
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "last_activation_time", last_activation_time)
        pulumi.set(__self__, "state", state)
        pulumi.set(__self__, "storage_url", storage_url)
        pulumi.set(__self__, "storage_url_expiry", storage_url_expiry)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def format(self) -> str:
        """
        The format of the application package, if the package is active.
        """
        return pulumi.get(self, "format")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the application.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastActivationTime")
    def last_activation_time(self) -> str:
        """
        The time at which the package was last activated, if the package is active.
        """
        return pulumi.get(self, "last_activation_time")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The current state of the application package.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="storageUrl")
    def storage_url(self) -> str:
        """
        The URL for the application package in Azure Storage.
        """
        return pulumi.get(self, "storage_url")

    @property
    @pulumi.getter(name="storageUrlExpiry")
    def storage_url_expiry(self) -> str:
        """
        The UTC time at which the Azure Storage URL will expire.
        """
        return pulumi.get(self, "storage_url_expiry")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The version of the application package. 
        """
        return pulumi.get(self, "version")


@pulumi.output_type
class AutoStoragePropertiesResponse(dict):
    """
    Contains information about the auto-storage account associated with a Batch account.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "lastKeySync":
            suggest = "last_key_sync"
        elif key == "storageAccountId":
            suggest = "storage_account_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AutoStoragePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AutoStoragePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AutoStoragePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 last_key_sync: str,
                 storage_account_id: str):
        """
        Contains information about the auto-storage account associated with a Batch account.
        :param str last_key_sync: The UTC time at which storage keys were last synchronized with the Batch account.
        :param str storage_account_id: The resource ID of the storage account to be used for auto-storage account.
        """
        pulumi.set(__self__, "last_key_sync", last_key_sync)
        pulumi.set(__self__, "storage_account_id", storage_account_id)

    @property
    @pulumi.getter(name="lastKeySync")
    def last_key_sync(self) -> str:
        """
        The UTC time at which storage keys were last synchronized with the Batch account.
        """
        return pulumi.get(self, "last_key_sync")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> str:
        """
        The resource ID of the storage account to be used for auto-storage account.
        """
        return pulumi.get(self, "storage_account_id")


@pulumi.output_type
class KeyVaultReferenceResponse(dict):
    """
    Identifies the Azure key vault associated with a Batch account.
    """
    def __init__(__self__, *,
                 id: str,
                 url: str):
        """
        Identifies the Azure key vault associated with a Batch account.
        :param str id: The resource ID of the Azure key vault associated with the Batch account.
        :param str url: The URL of the Azure key vault associated with the Batch account.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID of the Azure key vault associated with the Batch account.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        The URL of the Azure key vault associated with the Batch account.
        """
        return pulumi.get(self, "url")


