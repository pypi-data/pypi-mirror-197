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
    'GetMicrosoftSecurityIncidentCreationAlertRuleResult',
    'AwaitableGetMicrosoftSecurityIncidentCreationAlertRuleResult',
    'get_microsoft_security_incident_creation_alert_rule',
    'get_microsoft_security_incident_creation_alert_rule_output',
]

@pulumi.output_type
class GetMicrosoftSecurityIncidentCreationAlertRuleResult:
    """
    Represents MicrosoftSecurityIncidentCreation rule.
    """
    def __init__(__self__, alert_rule_template_name=None, description=None, display_name=None, display_names_exclude_filter=None, display_names_filter=None, enabled=None, etag=None, id=None, kind=None, last_modified_utc=None, name=None, product_filter=None, severities_filter=None, system_data=None, type=None):
        if alert_rule_template_name and not isinstance(alert_rule_template_name, str):
            raise TypeError("Expected argument 'alert_rule_template_name' to be a str")
        pulumi.set(__self__, "alert_rule_template_name", alert_rule_template_name)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if display_names_exclude_filter and not isinstance(display_names_exclude_filter, list):
            raise TypeError("Expected argument 'display_names_exclude_filter' to be a list")
        pulumi.set(__self__, "display_names_exclude_filter", display_names_exclude_filter)
        if display_names_filter and not isinstance(display_names_filter, list):
            raise TypeError("Expected argument 'display_names_filter' to be a list")
        pulumi.set(__self__, "display_names_filter", display_names_filter)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_modified_utc and not isinstance(last_modified_utc, str):
            raise TypeError("Expected argument 'last_modified_utc' to be a str")
        pulumi.set(__self__, "last_modified_utc", last_modified_utc)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if product_filter and not isinstance(product_filter, str):
            raise TypeError("Expected argument 'product_filter' to be a str")
        pulumi.set(__self__, "product_filter", product_filter)
        if severities_filter and not isinstance(severities_filter, list):
            raise TypeError("Expected argument 'severities_filter' to be a list")
        pulumi.set(__self__, "severities_filter", severities_filter)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="alertRuleTemplateName")
    def alert_rule_template_name(self) -> Optional[str]:
        """
        The Name of the alert rule template used to create this rule.
        """
        return pulumi.get(self, "alert_rule_template_name")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the alert rule.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        The display name for alerts created by this alert rule.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="displayNamesExcludeFilter")
    def display_names_exclude_filter(self) -> Optional[Sequence[str]]:
        """
        the alerts' displayNames on which the cases will not be generated
        """
        return pulumi.get(self, "display_names_exclude_filter")

    @property
    @pulumi.getter(name="displayNamesFilter")
    def display_names_filter(self) -> Optional[Sequence[str]]:
        """
        the alerts' displayNames on which the cases will be generated
        """
        return pulumi.get(self, "display_names_filter")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Determines whether this alert rule is enabled or disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the alert rule
        Expected value is 'MicrosoftSecurityIncidentCreation'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastModifiedUtc")
    def last_modified_utc(self) -> str:
        """
        The last time that this alert has been modified.
        """
        return pulumi.get(self, "last_modified_utc")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="productFilter")
    def product_filter(self) -> str:
        """
        The alerts' productName on which the cases will be generated
        """
        return pulumi.get(self, "product_filter")

    @property
    @pulumi.getter(name="severitiesFilter")
    def severities_filter(self) -> Optional[Sequence[str]]:
        """
        the alerts' severities on which the cases will be generated
        """
        return pulumi.get(self, "severities_filter")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetMicrosoftSecurityIncidentCreationAlertRuleResult(GetMicrosoftSecurityIncidentCreationAlertRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMicrosoftSecurityIncidentCreationAlertRuleResult(
            alert_rule_template_name=self.alert_rule_template_name,
            description=self.description,
            display_name=self.display_name,
            display_names_exclude_filter=self.display_names_exclude_filter,
            display_names_filter=self.display_names_filter,
            enabled=self.enabled,
            etag=self.etag,
            id=self.id,
            kind=self.kind,
            last_modified_utc=self.last_modified_utc,
            name=self.name,
            product_filter=self.product_filter,
            severities_filter=self.severities_filter,
            system_data=self.system_data,
            type=self.type)


def get_microsoft_security_incident_creation_alert_rule(resource_group_name: Optional[str] = None,
                                                        rule_id: Optional[str] = None,
                                                        workspace_name: Optional[str] = None,
                                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMicrosoftSecurityIncidentCreationAlertRuleResult:
    """
    Gets the alert rule.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleId'] = rule_id
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20211001preview:getMicrosoftSecurityIncidentCreationAlertRule', __args__, opts=opts, typ=GetMicrosoftSecurityIncidentCreationAlertRuleResult).value

    return AwaitableGetMicrosoftSecurityIncidentCreationAlertRuleResult(
        alert_rule_template_name=__ret__.alert_rule_template_name,
        description=__ret__.description,
        display_name=__ret__.display_name,
        display_names_exclude_filter=__ret__.display_names_exclude_filter,
        display_names_filter=__ret__.display_names_filter,
        enabled=__ret__.enabled,
        etag=__ret__.etag,
        id=__ret__.id,
        kind=__ret__.kind,
        last_modified_utc=__ret__.last_modified_utc,
        name=__ret__.name,
        product_filter=__ret__.product_filter,
        severities_filter=__ret__.severities_filter,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_microsoft_security_incident_creation_alert_rule)
def get_microsoft_security_incident_creation_alert_rule_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                                               rule_id: Optional[pulumi.Input[str]] = None,
                                                               workspace_name: Optional[pulumi.Input[str]] = None,
                                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMicrosoftSecurityIncidentCreationAlertRuleResult]:
    """
    Gets the alert rule.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str rule_id: Alert rule ID
    :param str workspace_name: The name of the workspace.
    """
    ...
