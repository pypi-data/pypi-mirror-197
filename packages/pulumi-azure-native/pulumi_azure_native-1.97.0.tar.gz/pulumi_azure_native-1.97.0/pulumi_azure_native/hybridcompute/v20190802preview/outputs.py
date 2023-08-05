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
from ._enums import *

__all__ = [
    'ErrorDetailResponse',
    'MachineExtensionInstanceViewResponse',
    'MachineExtensionInstanceViewResponseStatus',
    'OSProfileResponse',
]

@pulumi.output_type
class ErrorDetailResponse(dict):
    def __init__(__self__, *,
                 code: str,
                 message: str,
                 details: Optional[Sequence['outputs.ErrorDetailResponse']] = None,
                 target: Optional[str] = None):
        """
        :param str code: The error's code.
        :param str message: A human readable error message.
        :param Sequence['ErrorDetailResponse'] details: Additional error details.
        :param str target: Indicates which property in the request is responsible for the error.
        """
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "message", message)
        if details is not None:
            pulumi.set(__self__, "details", details)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        The error's code.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def message(self) -> str:
        """
        A human readable error message.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def details(self) -> Optional[Sequence['outputs.ErrorDetailResponse']]:
        """
        Additional error details.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def target(self) -> Optional[str]:
        """
        Indicates which property in the request is responsible for the error.
        """
        return pulumi.get(self, "target")


@pulumi.output_type
class MachineExtensionInstanceViewResponse(dict):
    """
    Describes the Machine Extension Instance View.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "typeHandlerVersion":
            suggest = "type_handler_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MachineExtensionInstanceViewResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MachineExtensionInstanceViewResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MachineExtensionInstanceViewResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: Optional[str] = None,
                 status: Optional['outputs.MachineExtensionInstanceViewResponseStatus'] = None,
                 type: Optional[str] = None,
                 type_handler_version: Optional[str] = None):
        """
        Describes the Machine Extension Instance View.
        :param str name: The machine extension name.
        :param 'MachineExtensionInstanceViewResponseStatus' status: Instance view status.
        :param str type: Specifies the type of the extension; an example is "CustomScriptExtension".
        :param str type_handler_version: Specifies the version of the script handler.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if type_handler_version is not None:
            pulumi.set(__self__, "type_handler_version", type_handler_version)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The machine extension name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> Optional['outputs.MachineExtensionInstanceViewResponseStatus']:
        """
        Instance view status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Specifies the type of the extension; an example is "CustomScriptExtension".
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="typeHandlerVersion")
    def type_handler_version(self) -> Optional[str]:
        """
        Specifies the version of the script handler.
        """
        return pulumi.get(self, "type_handler_version")


@pulumi.output_type
class MachineExtensionInstanceViewResponseStatus(dict):
    """
    Instance view status.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "displayStatus":
            suggest = "display_status"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MachineExtensionInstanceViewResponseStatus. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MachineExtensionInstanceViewResponseStatus.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MachineExtensionInstanceViewResponseStatus.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 code: Optional[str] = None,
                 display_status: Optional[str] = None,
                 level: Optional[str] = None,
                 message: Optional[str] = None,
                 time: Optional[str] = None):
        """
        Instance view status.
        :param str code: The status code.
        :param str display_status: The short localizable label for the status.
        :param str level: The level code.
        :param str message: The detailed status message, including for alerts and error messages.
        :param str time: The time of the status.
        """
        if code is not None:
            pulumi.set(__self__, "code", code)
        if display_status is not None:
            pulumi.set(__self__, "display_status", display_status)
        if level is not None:
            pulumi.set(__self__, "level", level)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if time is not None:
            pulumi.set(__self__, "time", time)

    @property
    @pulumi.getter
    def code(self) -> Optional[str]:
        """
        The status code.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter(name="displayStatus")
    def display_status(self) -> Optional[str]:
        """
        The short localizable label for the status.
        """
        return pulumi.get(self, "display_status")

    @property
    @pulumi.getter
    def level(self) -> Optional[str]:
        """
        The level code.
        """
        return pulumi.get(self, "level")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        The detailed status message, including for alerts and error messages.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def time(self) -> Optional[str]:
        """
        The time of the status.
        """
        return pulumi.get(self, "time")


@pulumi.output_type
class OSProfileResponse(dict):
    """
    Specifies the operating system settings for the hybrid machine.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "computerName":
            suggest = "computer_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OSProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OSProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OSProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 computer_name: str):
        """
        Specifies the operating system settings for the hybrid machine.
        :param str computer_name: Specifies the host OS name of the hybrid machine.
        """
        pulumi.set(__self__, "computer_name", computer_name)

    @property
    @pulumi.getter(name="computerName")
    def computer_name(self) -> str:
        """
        Specifies the host OS name of the hybrid machine.
        """
        return pulumi.get(self, "computer_name")


