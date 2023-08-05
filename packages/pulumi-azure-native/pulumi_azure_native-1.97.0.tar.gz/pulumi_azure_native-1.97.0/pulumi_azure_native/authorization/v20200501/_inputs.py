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
    'ManagementLockOwnerArgs',
    'PrivateLinkAssociationPropertiesArgs',
]

@pulumi.input_type
class ManagementLockOwnerArgs:
    def __init__(__self__, *,
                 application_id: Optional[pulumi.Input[str]] = None):
        """
        Lock owner properties.
        :param pulumi.Input[str] application_id: The application ID of the lock owner.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The application ID of the lock owner.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_id", value)


@pulumi.input_type
class PrivateLinkAssociationPropertiesArgs:
    def __init__(__self__, *,
                 private_link: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccessOptions']]] = None):
        """
        :param pulumi.Input[str] private_link: The rmpl Resource ID.
        """
        if private_link is not None:
            pulumi.set(__self__, "private_link", private_link)
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)

    @property
    @pulumi.getter(name="privateLink")
    def private_link(self) -> Optional[pulumi.Input[str]]:
        """
        The rmpl Resource ID.
        """
        return pulumi.get(self, "private_link")

    @private_link.setter
    def private_link(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_link", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccessOptions']]]:
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccessOptions']]]):
        pulumi.set(self, "public_network_access", value)


