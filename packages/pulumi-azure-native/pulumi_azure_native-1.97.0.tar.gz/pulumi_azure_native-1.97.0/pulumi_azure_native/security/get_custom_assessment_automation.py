# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetCustomAssessmentAutomationResult',
    'AwaitableGetCustomAssessmentAutomationResult',
    'get_custom_assessment_automation',
    'get_custom_assessment_automation_output',
]

@pulumi.output_type
class GetCustomAssessmentAutomationResult:
    """
    Custom Assessment Automation
    """
    def __init__(__self__, assessment_key=None, compressed_query=None, description=None, display_name=None, id=None, name=None, remediation_description=None, severity=None, supported_cloud=None, system_data=None, type=None):
        if assessment_key and not isinstance(assessment_key, str):
            raise TypeError("Expected argument 'assessment_key' to be a str")
        pulumi.set(__self__, "assessment_key", assessment_key)
        if compressed_query and not isinstance(compressed_query, str):
            raise TypeError("Expected argument 'compressed_query' to be a str")
        pulumi.set(__self__, "compressed_query", compressed_query)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if remediation_description and not isinstance(remediation_description, str):
            raise TypeError("Expected argument 'remediation_description' to be a str")
        pulumi.set(__self__, "remediation_description", remediation_description)
        if severity and not isinstance(severity, str):
            raise TypeError("Expected argument 'severity' to be a str")
        pulumi.set(__self__, "severity", severity)
        if supported_cloud and not isinstance(supported_cloud, str):
            raise TypeError("Expected argument 'supported_cloud' to be a str")
        pulumi.set(__self__, "supported_cloud", supported_cloud)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="assessmentKey")
    def assessment_key(self) -> Optional[str]:
        """
        The assessment metadata key used when an assessment is generated for this assessment automation.
        """
        return pulumi.get(self, "assessment_key")

    @property
    @pulumi.getter(name="compressedQuery")
    def compressed_query(self) -> Optional[str]:
        """
        GZip encoded KQL query representing the assessment automation results required.
        """
        return pulumi.get(self, "compressed_query")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description to relate to the assessments generated by this assessment automation.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the assessments generated by this assessment automation.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="remediationDescription")
    def remediation_description(self) -> Optional[str]:
        """
        The remediation description to relate to the assessments generated by this assessment automation.
        """
        return pulumi.get(self, "remediation_description")

    @property
    @pulumi.getter
    def severity(self) -> Optional[str]:
        """
        The severity to relate to the assessments generated by this assessment automation.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="supportedCloud")
    def supported_cloud(self) -> Optional[str]:
        """
        Relevant cloud for the custom assessment automation.
        """
        return pulumi.get(self, "supported_cloud")

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
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetCustomAssessmentAutomationResult(GetCustomAssessmentAutomationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomAssessmentAutomationResult(
            assessment_key=self.assessment_key,
            compressed_query=self.compressed_query,
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            remediation_description=self.remediation_description,
            severity=self.severity,
            supported_cloud=self.supported_cloud,
            system_data=self.system_data,
            type=self.type)


def get_custom_assessment_automation(custom_assessment_automation_name: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCustomAssessmentAutomationResult:
    """
    Gets a single custom assessment automation by name for the provided subscription and resource group.
    API Version: 2021-07-01-preview.


    :param str custom_assessment_automation_name: Name of the Custom Assessment Automation.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['customAssessmentAutomationName'] = custom_assessment_automation_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:security:getCustomAssessmentAutomation', __args__, opts=opts, typ=GetCustomAssessmentAutomationResult).value

    return AwaitableGetCustomAssessmentAutomationResult(
        assessment_key=__ret__.assessment_key,
        compressed_query=__ret__.compressed_query,
        description=__ret__.description,
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        remediation_description=__ret__.remediation_description,
        severity=__ret__.severity,
        supported_cloud=__ret__.supported_cloud,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_custom_assessment_automation)
def get_custom_assessment_automation_output(custom_assessment_automation_name: Optional[pulumi.Input[str]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCustomAssessmentAutomationResult]:
    """
    Gets a single custom assessment automation by name for the provided subscription and resource group.
    API Version: 2021-07-01-preview.


    :param str custom_assessment_automation_name: Name of the Custom Assessment Automation.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    ...
