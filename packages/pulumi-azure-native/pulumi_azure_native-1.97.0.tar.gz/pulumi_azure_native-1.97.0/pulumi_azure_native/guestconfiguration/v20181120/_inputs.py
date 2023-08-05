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
    'ConfigurationParameterArgs',
    'ConfigurationSettingArgs',
    'GuestConfigurationAssignmentPropertiesArgs',
    'GuestConfigurationNavigationArgs',
]

@pulumi.input_type
class ConfigurationParameterArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Represents a configuration parameter.
        :param pulumi.Input[str] name: Name of the configuration parameter.
        :param pulumi.Input[str] value: Value of the configuration parameter.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the configuration parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        Value of the configuration parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ConfigurationSettingArgs:
    def __init__(__self__, *,
                 action_after_reboot: Optional[pulumi.Input[Union[str, 'ActionAfterReboot']]] = None,
                 allow_module_overwrite: Optional[pulumi.Input[bool]] = None,
                 configuration_mode: Optional[pulumi.Input[Union[str, 'ConfigurationMode']]] = None,
                 configuration_mode_frequency_mins: Optional[pulumi.Input[float]] = None,
                 reboot_if_needed: Optional[pulumi.Input[bool]] = None,
                 refresh_frequency_mins: Optional[pulumi.Input[float]] = None):
        """
        Configuration setting of LCM (Local Configuration Manager).
        :param pulumi.Input[Union[str, 'ActionAfterReboot']] action_after_reboot: Specifies what happens after a reboot during the application of a configuration. The possible values are ContinueConfiguration and StopConfiguration
        :param pulumi.Input[bool] allow_module_overwrite: If true - new configurations downloaded from the pull service are allowed to overwrite the old ones on the target node. Otherwise, false
        :param pulumi.Input[Union[str, 'ConfigurationMode']] configuration_mode: Specifies how the LCM(Local Configuration Manager) actually applies the configuration to the target nodes. Possible values are ApplyOnly, ApplyAndMonitor, and ApplyAndAutoCorrect.
        :param pulumi.Input[float] configuration_mode_frequency_mins: How often, in minutes, the current configuration is checked and applied. This property is ignored if the ConfigurationMode property is set to ApplyOnly. The default value is 15.
        :param pulumi.Input[bool] reboot_if_needed: Set this to true to automatically reboot the node after a configuration that requires reboot is applied. Otherwise, you will have to manually reboot the node for any configuration that requires it. The default value is false. To use this setting when a reboot condition is enacted by something other than DSC (such as Windows Installer), combine this setting with the xPendingReboot module.
        :param pulumi.Input[float] refresh_frequency_mins: The time interval, in minutes, at which the LCM checks a pull service to get updated configurations. This value is ignored if the LCM is not configured in pull mode. The default value is 30.
        """
        if action_after_reboot is not None:
            pulumi.set(__self__, "action_after_reboot", action_after_reboot)
        if allow_module_overwrite is not None:
            pulumi.set(__self__, "allow_module_overwrite", allow_module_overwrite)
        if configuration_mode is not None:
            pulumi.set(__self__, "configuration_mode", configuration_mode)
        if configuration_mode_frequency_mins is None:
            configuration_mode_frequency_mins = 15
        if configuration_mode_frequency_mins is not None:
            pulumi.set(__self__, "configuration_mode_frequency_mins", configuration_mode_frequency_mins)
        if reboot_if_needed is not None:
            pulumi.set(__self__, "reboot_if_needed", reboot_if_needed)
        if refresh_frequency_mins is None:
            refresh_frequency_mins = 30
        if refresh_frequency_mins is not None:
            pulumi.set(__self__, "refresh_frequency_mins", refresh_frequency_mins)

    @property
    @pulumi.getter(name="actionAfterReboot")
    def action_after_reboot(self) -> Optional[pulumi.Input[Union[str, 'ActionAfterReboot']]]:
        """
        Specifies what happens after a reboot during the application of a configuration. The possible values are ContinueConfiguration and StopConfiguration
        """
        return pulumi.get(self, "action_after_reboot")

    @action_after_reboot.setter
    def action_after_reboot(self, value: Optional[pulumi.Input[Union[str, 'ActionAfterReboot']]]):
        pulumi.set(self, "action_after_reboot", value)

    @property
    @pulumi.getter(name="allowModuleOverwrite")
    def allow_module_overwrite(self) -> Optional[pulumi.Input[bool]]:
        """
        If true - new configurations downloaded from the pull service are allowed to overwrite the old ones on the target node. Otherwise, false
        """
        return pulumi.get(self, "allow_module_overwrite")

    @allow_module_overwrite.setter
    def allow_module_overwrite(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_module_overwrite", value)

    @property
    @pulumi.getter(name="configurationMode")
    def configuration_mode(self) -> Optional[pulumi.Input[Union[str, 'ConfigurationMode']]]:
        """
        Specifies how the LCM(Local Configuration Manager) actually applies the configuration to the target nodes. Possible values are ApplyOnly, ApplyAndMonitor, and ApplyAndAutoCorrect.
        """
        return pulumi.get(self, "configuration_mode")

    @configuration_mode.setter
    def configuration_mode(self, value: Optional[pulumi.Input[Union[str, 'ConfigurationMode']]]):
        pulumi.set(self, "configuration_mode", value)

    @property
    @pulumi.getter(name="configurationModeFrequencyMins")
    def configuration_mode_frequency_mins(self) -> Optional[pulumi.Input[float]]:
        """
        How often, in minutes, the current configuration is checked and applied. This property is ignored if the ConfigurationMode property is set to ApplyOnly. The default value is 15.
        """
        return pulumi.get(self, "configuration_mode_frequency_mins")

    @configuration_mode_frequency_mins.setter
    def configuration_mode_frequency_mins(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "configuration_mode_frequency_mins", value)

    @property
    @pulumi.getter(name="rebootIfNeeded")
    def reboot_if_needed(self) -> Optional[pulumi.Input[bool]]:
        """
        Set this to true to automatically reboot the node after a configuration that requires reboot is applied. Otherwise, you will have to manually reboot the node for any configuration that requires it. The default value is false. To use this setting when a reboot condition is enacted by something other than DSC (such as Windows Installer), combine this setting with the xPendingReboot module.
        """
        return pulumi.get(self, "reboot_if_needed")

    @reboot_if_needed.setter
    def reboot_if_needed(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "reboot_if_needed", value)

    @property
    @pulumi.getter(name="refreshFrequencyMins")
    def refresh_frequency_mins(self) -> Optional[pulumi.Input[float]]:
        """
        The time interval, in minutes, at which the LCM checks a pull service to get updated configurations. This value is ignored if the LCM is not configured in pull mode. The default value is 30.
        """
        return pulumi.get(self, "refresh_frequency_mins")

    @refresh_frequency_mins.setter
    def refresh_frequency_mins(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "refresh_frequency_mins", value)


@pulumi.input_type
class GuestConfigurationAssignmentPropertiesArgs:
    def __init__(__self__, *,
                 context: Optional[pulumi.Input[str]] = None,
                 guest_configuration: Optional[pulumi.Input['GuestConfigurationNavigationArgs']] = None):
        """
        Guest configuration assignment properties.
        :param pulumi.Input[str] context: The source which initiated the guest configuration assignment. Ex: Azure Policy
        :param pulumi.Input['GuestConfigurationNavigationArgs'] guest_configuration: The guest configuration to assign.
        """
        if context is not None:
            pulumi.set(__self__, "context", context)
        if guest_configuration is not None:
            pulumi.set(__self__, "guest_configuration", guest_configuration)

    @property
    @pulumi.getter
    def context(self) -> Optional[pulumi.Input[str]]:
        """
        The source which initiated the guest configuration assignment. Ex: Azure Policy
        """
        return pulumi.get(self, "context")

    @context.setter
    def context(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "context", value)

    @property
    @pulumi.getter(name="guestConfiguration")
    def guest_configuration(self) -> Optional[pulumi.Input['GuestConfigurationNavigationArgs']]:
        """
        The guest configuration to assign.
        """
        return pulumi.get(self, "guest_configuration")

    @guest_configuration.setter
    def guest_configuration(self, value: Optional[pulumi.Input['GuestConfigurationNavigationArgs']]):
        pulumi.set(self, "guest_configuration", value)


@pulumi.input_type
class GuestConfigurationNavigationArgs:
    def __init__(__self__, *,
                 assignment_type: Optional[pulumi.Input[Union[str, 'AssignmentType']]] = None,
                 configuration_parameter: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]]] = None,
                 configuration_protected_parameter: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]]] = None,
                 configuration_setting: Optional[pulumi.Input['ConfigurationSettingArgs']] = None,
                 content_hash: Optional[pulumi.Input[str]] = None,
                 content_uri: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'Kind']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        Guest configuration is an artifact that encapsulates DSC configuration and its dependencies. The artifact is a zip file containing DSC configuration (as MOF) and dependent resources and other dependencies like modules.
        :param pulumi.Input[Union[str, 'AssignmentType']] assignment_type: Specifies the assignment type and execution of the configuration. Possible values are Audit, DeployAndAutoCorrect, ApplyAndAutoCorrect and ApplyAndMonitor.
        :param pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]] configuration_parameter: The configuration parameters for the guest configuration.
        :param pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]] configuration_protected_parameter: The protected configuration parameters for the guest configuration.
        :param pulumi.Input['ConfigurationSettingArgs'] configuration_setting: The configuration setting for the guest configuration.
        :param pulumi.Input[str] content_hash: Combined hash of the guest configuration package and configuration parameters.
        :param pulumi.Input[str] content_uri: Uri of the storage where guest configuration package is uploaded.
        :param pulumi.Input[Union[str, 'Kind']] kind: Kind of the guest configuration. For example:DSC
        :param pulumi.Input[str] name: Name of the guest configuration.
        :param pulumi.Input[str] version: Version of the guest configuration.
        """
        if assignment_type is not None:
            pulumi.set(__self__, "assignment_type", assignment_type)
        if configuration_parameter is not None:
            pulumi.set(__self__, "configuration_parameter", configuration_parameter)
        if configuration_protected_parameter is not None:
            pulumi.set(__self__, "configuration_protected_parameter", configuration_protected_parameter)
        if configuration_setting is not None:
            pulumi.set(__self__, "configuration_setting", configuration_setting)
        if content_hash is not None:
            pulumi.set(__self__, "content_hash", content_hash)
        if content_uri is not None:
            pulumi.set(__self__, "content_uri", content_uri)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="assignmentType")
    def assignment_type(self) -> Optional[pulumi.Input[Union[str, 'AssignmentType']]]:
        """
        Specifies the assignment type and execution of the configuration. Possible values are Audit, DeployAndAutoCorrect, ApplyAndAutoCorrect and ApplyAndMonitor.
        """
        return pulumi.get(self, "assignment_type")

    @assignment_type.setter
    def assignment_type(self, value: Optional[pulumi.Input[Union[str, 'AssignmentType']]]):
        pulumi.set(self, "assignment_type", value)

    @property
    @pulumi.getter(name="configurationParameter")
    def configuration_parameter(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]]]:
        """
        The configuration parameters for the guest configuration.
        """
        return pulumi.get(self, "configuration_parameter")

    @configuration_parameter.setter
    def configuration_parameter(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]]]):
        pulumi.set(self, "configuration_parameter", value)

    @property
    @pulumi.getter(name="configurationProtectedParameter")
    def configuration_protected_parameter(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]]]:
        """
        The protected configuration parameters for the guest configuration.
        """
        return pulumi.get(self, "configuration_protected_parameter")

    @configuration_protected_parameter.setter
    def configuration_protected_parameter(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationParameterArgs']]]]):
        pulumi.set(self, "configuration_protected_parameter", value)

    @property
    @pulumi.getter(name="configurationSetting")
    def configuration_setting(self) -> Optional[pulumi.Input['ConfigurationSettingArgs']]:
        """
        The configuration setting for the guest configuration.
        """
        return pulumi.get(self, "configuration_setting")

    @configuration_setting.setter
    def configuration_setting(self, value: Optional[pulumi.Input['ConfigurationSettingArgs']]):
        pulumi.set(self, "configuration_setting", value)

    @property
    @pulumi.getter(name="contentHash")
    def content_hash(self) -> Optional[pulumi.Input[str]]:
        """
        Combined hash of the guest configuration package and configuration parameters.
        """
        return pulumi.get(self, "content_hash")

    @content_hash.setter
    def content_hash(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_hash", value)

    @property
    @pulumi.getter(name="contentUri")
    def content_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Uri of the storage where guest configuration package is uploaded.
        """
        return pulumi.get(self, "content_uri")

    @content_uri.setter
    def content_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_uri", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[Union[str, 'Kind']]]:
        """
        Kind of the guest configuration. For example:DSC
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[Union[str, 'Kind']]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the guest configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the guest configuration.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


