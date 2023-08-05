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
    'AzurePlanResponse',
    'InvoiceSectionWithCreateSubPermissionResponse',
]

@pulumi.output_type
class AzurePlanResponse(dict):
    """
    Details of the Azure plan.
    """
    def __init__(__self__, *,
                 sku_description: str,
                 sku_id: Optional[str] = None):
        """
        Details of the Azure plan.
        :param str sku_description: The sku description.
        :param str sku_id: The sku id.
        """
        pulumi.set(__self__, "sku_description", sku_description)
        if sku_id is not None:
            pulumi.set(__self__, "sku_id", sku_id)

    @property
    @pulumi.getter(name="skuDescription")
    def sku_description(self) -> str:
        """
        The sku description.
        """
        return pulumi.get(self, "sku_description")

    @property
    @pulumi.getter(name="skuId")
    def sku_id(self) -> Optional[str]:
        """
        The sku id.
        """
        return pulumi.get(self, "sku_id")


@pulumi.output_type
class InvoiceSectionWithCreateSubPermissionResponse(dict):
    """
    Invoice section properties with create subscription permission.
    """
    def __init__(__self__, *,
                 billing_profile_display_name: str,
                 billing_profile_id: str,
                 billing_profile_spending_limit: str,
                 billing_profile_status: str,
                 billing_profile_status_reason_code: str,
                 billing_profile_system_id: str,
                 invoice_section_display_name: str,
                 invoice_section_id: str,
                 invoice_section_system_id: str,
                 enabled_azure_plans: Optional[Sequence['outputs.AzurePlanResponse']] = None):
        """
        Invoice section properties with create subscription permission.
        :param str billing_profile_display_name: The name of the billing profile for the invoice section.
        :param str billing_profile_id: The ID of the billing profile for the invoice section.
        :param str billing_profile_spending_limit: The billing profile spending limit.
        :param str billing_profile_status: The status of the billing profile.
        :param str billing_profile_status_reason_code: Reason for the specified billing profile status.
        :param str billing_profile_system_id: The system generated unique identifier for a billing profile.
        :param str invoice_section_display_name: The name of the invoice section.
        :param str invoice_section_id: The ID of the invoice section.
        :param str invoice_section_system_id: The system generated unique identifier for an invoice section.
        :param Sequence['AzurePlanResponse'] enabled_azure_plans: Enabled azure plans for the associated billing profile.
        """
        pulumi.set(__self__, "billing_profile_display_name", billing_profile_display_name)
        pulumi.set(__self__, "billing_profile_id", billing_profile_id)
        pulumi.set(__self__, "billing_profile_spending_limit", billing_profile_spending_limit)
        pulumi.set(__self__, "billing_profile_status", billing_profile_status)
        pulumi.set(__self__, "billing_profile_status_reason_code", billing_profile_status_reason_code)
        pulumi.set(__self__, "billing_profile_system_id", billing_profile_system_id)
        pulumi.set(__self__, "invoice_section_display_name", invoice_section_display_name)
        pulumi.set(__self__, "invoice_section_id", invoice_section_id)
        pulumi.set(__self__, "invoice_section_system_id", invoice_section_system_id)
        if enabled_azure_plans is not None:
            pulumi.set(__self__, "enabled_azure_plans", enabled_azure_plans)

    @property
    @pulumi.getter(name="billingProfileDisplayName")
    def billing_profile_display_name(self) -> str:
        """
        The name of the billing profile for the invoice section.
        """
        return pulumi.get(self, "billing_profile_display_name")

    @property
    @pulumi.getter(name="billingProfileId")
    def billing_profile_id(self) -> str:
        """
        The ID of the billing profile for the invoice section.
        """
        return pulumi.get(self, "billing_profile_id")

    @property
    @pulumi.getter(name="billingProfileSpendingLimit")
    def billing_profile_spending_limit(self) -> str:
        """
        The billing profile spending limit.
        """
        return pulumi.get(self, "billing_profile_spending_limit")

    @property
    @pulumi.getter(name="billingProfileStatus")
    def billing_profile_status(self) -> str:
        """
        The status of the billing profile.
        """
        return pulumi.get(self, "billing_profile_status")

    @property
    @pulumi.getter(name="billingProfileStatusReasonCode")
    def billing_profile_status_reason_code(self) -> str:
        """
        Reason for the specified billing profile status.
        """
        return pulumi.get(self, "billing_profile_status_reason_code")

    @property
    @pulumi.getter(name="billingProfileSystemId")
    def billing_profile_system_id(self) -> str:
        """
        The system generated unique identifier for a billing profile.
        """
        return pulumi.get(self, "billing_profile_system_id")

    @property
    @pulumi.getter(name="invoiceSectionDisplayName")
    def invoice_section_display_name(self) -> str:
        """
        The name of the invoice section.
        """
        return pulumi.get(self, "invoice_section_display_name")

    @property
    @pulumi.getter(name="invoiceSectionId")
    def invoice_section_id(self) -> str:
        """
        The ID of the invoice section.
        """
        return pulumi.get(self, "invoice_section_id")

    @property
    @pulumi.getter(name="invoiceSectionSystemId")
    def invoice_section_system_id(self) -> str:
        """
        The system generated unique identifier for an invoice section.
        """
        return pulumi.get(self, "invoice_section_system_id")

    @property
    @pulumi.getter(name="enabledAzurePlans")
    def enabled_azure_plans(self) -> Optional[Sequence['outputs.AzurePlanResponse']]:
        """
        Enabled azure plans for the associated billing profile.
        """
        return pulumi.get(self, "enabled_azure_plans")


