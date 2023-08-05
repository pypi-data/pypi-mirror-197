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
    'ConfigurationProfileAssignmentPropertiesResponse',
    'ConfigurationProfilePropertiesResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class ConfigurationProfileAssignmentPropertiesResponse(dict):
    """
    Automanage configuration profile assignment properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "targetId":
            suggest = "target_id"
        elif key == "configurationProfile":
            suggest = "configuration_profile"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ConfigurationProfileAssignmentPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ConfigurationProfileAssignmentPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ConfigurationProfileAssignmentPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 status: str,
                 target_id: str,
                 configuration_profile: Optional[str] = None):
        """
        Automanage configuration profile assignment properties.
        :param str status: The status of onboarding, which only appears in the response.
        :param str target_id: The target VM resource URI
        :param str configuration_profile: The Automanage configurationProfile ARM Resource URI.
        """
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "target_id", target_id)
        if configuration_profile is not None:
            pulumi.set(__self__, "configuration_profile", configuration_profile)

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of onboarding, which only appears in the response.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> str:
        """
        The target VM resource URI
        """
        return pulumi.get(self, "target_id")

    @property
    @pulumi.getter(name="configurationProfile")
    def configuration_profile(self) -> Optional[str]:
        """
        The Automanage configurationProfile ARM Resource URI.
        """
        return pulumi.get(self, "configuration_profile")


@pulumi.output_type
class ConfigurationProfilePropertiesResponse(dict):
    """
    Automanage configuration profile properties.
    """
    def __init__(__self__, *,
                 configuration: Optional[Any] = None):
        """
        Automanage configuration profile properties.
        :param Any configuration: configuration dictionary of the configuration profile.
        """
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)

    @property
    @pulumi.getter
    def configuration(self) -> Optional[Any]:
        """
        configuration dictionary of the configuration profile.
        """
        return pulumi.get(self, "configuration")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


