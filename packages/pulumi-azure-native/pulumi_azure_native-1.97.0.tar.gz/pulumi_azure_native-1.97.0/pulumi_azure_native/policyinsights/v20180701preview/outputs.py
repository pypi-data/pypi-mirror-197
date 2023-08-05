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
    'ErrorDefinitionResponse',
    'RemediationDeploymentResponse',
    'RemediationDeploymentSummaryResponse',
    'RemediationFiltersResponse',
    'TypedErrorInfoResponse',
]

@pulumi.output_type
class ErrorDefinitionResponse(dict):
    """
    Error definition.
    """
    def __init__(__self__, *,
                 additional_info: Sequence['outputs.TypedErrorInfoResponse'],
                 code: str,
                 details: Sequence['outputs.ErrorDefinitionResponse'],
                 message: str,
                 target: str):
        """
        Error definition.
        :param Sequence['TypedErrorInfoResponse'] additional_info: Additional scenario specific error details.
        :param str code: Service specific error code which serves as the substatus for the HTTP error code.
        :param Sequence['ErrorDefinitionResponse'] details: Internal error details.
        :param str message: Description of the error.
        :param str target: The target of the error.
        """
        pulumi.set(__self__, "additional_info", additional_info)
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "details", details)
        pulumi.set(__self__, "message", message)
        pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter(name="additionalInfo")
    def additional_info(self) -> Sequence['outputs.TypedErrorInfoResponse']:
        """
        Additional scenario specific error details.
        """
        return pulumi.get(self, "additional_info")

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        Service specific error code which serves as the substatus for the HTTP error code.
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter
    def details(self) -> Sequence['outputs.ErrorDefinitionResponse']:
        """
        Internal error details.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def message(self) -> str:
        """
        Description of the error.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def target(self) -> str:
        """
        The target of the error.
        """
        return pulumi.get(self, "target")


@pulumi.output_type
class RemediationDeploymentResponse(dict):
    """
    Details of a single deployment created by the remediation.
    """
    def __init__(__self__, *,
                 created_on: str,
                 deployment_id: str,
                 error: 'outputs.ErrorDefinitionResponse',
                 last_updated_on: str,
                 remediated_resource_id: str,
                 resource_location: str,
                 status: str):
        """
        Details of a single deployment created by the remediation.
        :param str created_on: The time at which the remediation was created.
        :param str deployment_id: Resource ID of the template deployment that will remediate the resource.
        :param 'ErrorDefinitionResponse' error: Error encountered while remediated the resource.
        :param str last_updated_on: The time at which the remediation deployment was last updated.
        :param str remediated_resource_id: Resource ID of the resource that is being remediated by the deployment.
        :param str resource_location: Location of the resource that is being remediated.
        :param str status: Status of the remediation deployment.
        """
        pulumi.set(__self__, "created_on", created_on)
        pulumi.set(__self__, "deployment_id", deployment_id)
        pulumi.set(__self__, "error", error)
        pulumi.set(__self__, "last_updated_on", last_updated_on)
        pulumi.set(__self__, "remediated_resource_id", remediated_resource_id)
        pulumi.set(__self__, "resource_location", resource_location)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> str:
        """
        The time at which the remediation was created.
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> str:
        """
        Resource ID of the template deployment that will remediate the resource.
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter
    def error(self) -> 'outputs.ErrorDefinitionResponse':
        """
        Error encountered while remediated the resource.
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter(name="lastUpdatedOn")
    def last_updated_on(self) -> str:
        """
        The time at which the remediation deployment was last updated.
        """
        return pulumi.get(self, "last_updated_on")

    @property
    @pulumi.getter(name="remediatedResourceId")
    def remediated_resource_id(self) -> str:
        """
        Resource ID of the resource that is being remediated by the deployment.
        """
        return pulumi.get(self, "remediated_resource_id")

    @property
    @pulumi.getter(name="resourceLocation")
    def resource_location(self) -> str:
        """
        Location of the resource that is being remediated.
        """
        return pulumi.get(self, "resource_location")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the remediation deployment.
        """
        return pulumi.get(self, "status")


@pulumi.output_type
class RemediationDeploymentSummaryResponse(dict):
    """
    The deployment status summary for all deployments created by the remediation.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "failedDeployments":
            suggest = "failed_deployments"
        elif key == "successfulDeployments":
            suggest = "successful_deployments"
        elif key == "totalDeployments":
            suggest = "total_deployments"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RemediationDeploymentSummaryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RemediationDeploymentSummaryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RemediationDeploymentSummaryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 failed_deployments: Optional[int] = None,
                 successful_deployments: Optional[int] = None,
                 total_deployments: Optional[int] = None):
        """
        The deployment status summary for all deployments created by the remediation.
        :param int failed_deployments: The number of deployments required by the remediation that have failed.
        :param int successful_deployments: The number of deployments required by the remediation that have succeeded.
        :param int total_deployments: The number of deployments required by the remediation.
        """
        if failed_deployments is not None:
            pulumi.set(__self__, "failed_deployments", failed_deployments)
        if successful_deployments is not None:
            pulumi.set(__self__, "successful_deployments", successful_deployments)
        if total_deployments is not None:
            pulumi.set(__self__, "total_deployments", total_deployments)

    @property
    @pulumi.getter(name="failedDeployments")
    def failed_deployments(self) -> Optional[int]:
        """
        The number of deployments required by the remediation that have failed.
        """
        return pulumi.get(self, "failed_deployments")

    @property
    @pulumi.getter(name="successfulDeployments")
    def successful_deployments(self) -> Optional[int]:
        """
        The number of deployments required by the remediation that have succeeded.
        """
        return pulumi.get(self, "successful_deployments")

    @property
    @pulumi.getter(name="totalDeployments")
    def total_deployments(self) -> Optional[int]:
        """
        The number of deployments required by the remediation.
        """
        return pulumi.get(self, "total_deployments")


@pulumi.output_type
class RemediationFiltersResponse(dict):
    """
    The filters that will be applied to determine which resources to remediate.
    """
    def __init__(__self__, *,
                 locations: Optional[Sequence[str]] = None):
        """
        The filters that will be applied to determine which resources to remediate.
        :param Sequence[str] locations: The resource locations that will be remediated.
        """
        if locations is not None:
            pulumi.set(__self__, "locations", locations)

    @property
    @pulumi.getter
    def locations(self) -> Optional[Sequence[str]]:
        """
        The resource locations that will be remediated.
        """
        return pulumi.get(self, "locations")


@pulumi.output_type
class TypedErrorInfoResponse(dict):
    """
    Scenario specific error details.
    """
    def __init__(__self__, *,
                 info: Any,
                 type: str):
        """
        Scenario specific error details.
        :param Any info: The scenario specific error details.
        :param str type: The type of included error details.
        """
        pulumi.set(__self__, "info", info)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def info(self) -> Any:
        """
        The scenario specific error details.
        """
        return pulumi.get(self, "info")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of included error details.
        """
        return pulumi.get(self, "type")


