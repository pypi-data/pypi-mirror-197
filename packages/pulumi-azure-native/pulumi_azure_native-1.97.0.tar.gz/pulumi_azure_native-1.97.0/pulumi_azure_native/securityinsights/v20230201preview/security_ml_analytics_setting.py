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

__all__ = ['SecurityMLAnalyticsSettingArgs', 'SecurityMLAnalyticsSetting']

@pulumi.input_type
class SecurityMLAnalyticsSettingArgs:
    def __init__(__self__, *,
                 kind: pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 settings_resource_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SecurityMLAnalyticsSetting resource.
        :param pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']] kind: The kind of security ML Analytics Settings
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] settings_resource_name: Security ML Analytics Settings resource name
        """
        pulumi.set(__self__, "kind", kind)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if settings_resource_name is not None:
            pulumi.set(__self__, "settings_resource_name", settings_resource_name)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']]:
        """
        The kind of security ML Analytics Settings
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="settingsResourceName")
    def settings_resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Security ML Analytics Settings resource name
        """
        return pulumi.get(self, "settings_resource_name")

    @settings_resource_name.setter
    def settings_resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "settings_resource_name", value)


warnings.warn("""Please use one of the variants: AnomalySecurityMLAnalyticsSettings.""", DeprecationWarning)


class SecurityMLAnalyticsSetting(pulumi.CustomResource):
    warnings.warn("""Please use one of the variants: AnomalySecurityMLAnalyticsSettings.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kind: Optional[pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 settings_resource_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Security ML Analytics Setting

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']] kind: The kind of security ML Analytics Settings
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] settings_resource_name: Security ML Analytics Settings resource name
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecurityMLAnalyticsSettingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Security ML Analytics Setting

        :param str resource_name: The name of the resource.
        :param SecurityMLAnalyticsSettingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityMLAnalyticsSettingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 kind: Optional[pulumi.Input[Union[str, 'SecurityMLAnalyticsSettingsKind']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 settings_resource_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""SecurityMLAnalyticsSetting is deprecated: Please use one of the variants: AnomalySecurityMLAnalyticsSettings.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecurityMLAnalyticsSettingArgs.__new__(SecurityMLAnalyticsSettingArgs)

            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = kind
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["settings_resource_name"] = settings_resource_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:securityinsights:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20220501preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20220601preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20220701preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20220801preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20220901preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20221001preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20221101:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20221101preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20221201preview:SecurityMLAnalyticsSetting"), pulumi.Alias(type_="azure-native:securityinsights/v20230201:SecurityMLAnalyticsSetting")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SecurityMLAnalyticsSetting, __self__).__init__(
            'azure-native:securityinsights/v20230201preview:SecurityMLAnalyticsSetting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SecurityMLAnalyticsSetting':
        """
        Get an existing SecurityMLAnalyticsSetting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SecurityMLAnalyticsSettingArgs.__new__(SecurityMLAnalyticsSettingArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return SecurityMLAnalyticsSetting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of security ML Analytics Settings
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

