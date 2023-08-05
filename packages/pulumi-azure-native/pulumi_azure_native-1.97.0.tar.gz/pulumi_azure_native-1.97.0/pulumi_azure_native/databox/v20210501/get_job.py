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
    'GetJobResult',
    'AwaitableGetJobResult',
    'get_job',
    'get_job_output',
]

@pulumi.output_type
class GetJobResult:
    """
    Job Resource.
    """
    def __init__(__self__, cancellation_reason=None, delivery_info=None, delivery_type=None, details=None, error=None, id=None, identity=None, is_cancellable=None, is_cancellable_without_fee=None, is_deletable=None, is_prepare_to_ship_enabled=None, is_shipping_address_editable=None, location=None, name=None, sku=None, start_time=None, status=None, system_data=None, tags=None, transfer_type=None, type=None):
        if cancellation_reason and not isinstance(cancellation_reason, str):
            raise TypeError("Expected argument 'cancellation_reason' to be a str")
        pulumi.set(__self__, "cancellation_reason", cancellation_reason)
        if delivery_info and not isinstance(delivery_info, dict):
            raise TypeError("Expected argument 'delivery_info' to be a dict")
        pulumi.set(__self__, "delivery_info", delivery_info)
        if delivery_type and not isinstance(delivery_type, str):
            raise TypeError("Expected argument 'delivery_type' to be a str")
        pulumi.set(__self__, "delivery_type", delivery_type)
        if details and not isinstance(details, dict):
            raise TypeError("Expected argument 'details' to be a dict")
        pulumi.set(__self__, "details", details)
        if error and not isinstance(error, dict):
            raise TypeError("Expected argument 'error' to be a dict")
        pulumi.set(__self__, "error", error)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if is_cancellable and not isinstance(is_cancellable, bool):
            raise TypeError("Expected argument 'is_cancellable' to be a bool")
        pulumi.set(__self__, "is_cancellable", is_cancellable)
        if is_cancellable_without_fee and not isinstance(is_cancellable_without_fee, bool):
            raise TypeError("Expected argument 'is_cancellable_without_fee' to be a bool")
        pulumi.set(__self__, "is_cancellable_without_fee", is_cancellable_without_fee)
        if is_deletable and not isinstance(is_deletable, bool):
            raise TypeError("Expected argument 'is_deletable' to be a bool")
        pulumi.set(__self__, "is_deletable", is_deletable)
        if is_prepare_to_ship_enabled and not isinstance(is_prepare_to_ship_enabled, bool):
            raise TypeError("Expected argument 'is_prepare_to_ship_enabled' to be a bool")
        pulumi.set(__self__, "is_prepare_to_ship_enabled", is_prepare_to_ship_enabled)
        if is_shipping_address_editable and not isinstance(is_shipping_address_editable, bool):
            raise TypeError("Expected argument 'is_shipping_address_editable' to be a bool")
        pulumi.set(__self__, "is_shipping_address_editable", is_shipping_address_editable)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if transfer_type and not isinstance(transfer_type, str):
            raise TypeError("Expected argument 'transfer_type' to be a str")
        pulumi.set(__self__, "transfer_type", transfer_type)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="cancellationReason")
    def cancellation_reason(self) -> str:
        """
        Reason for cancellation.
        """
        return pulumi.get(self, "cancellation_reason")

    @property
    @pulumi.getter(name="deliveryInfo")
    def delivery_info(self) -> Optional['outputs.JobDeliveryInfoResponse']:
        """
        Delivery Info of Job.
        """
        return pulumi.get(self, "delivery_info")

    @property
    @pulumi.getter(name="deliveryType")
    def delivery_type(self) -> Optional[str]:
        """
        Delivery type of Job.
        """
        return pulumi.get(self, "delivery_type")

    @property
    @pulumi.getter
    def details(self) -> Optional[Any]:
        """
        Details of a job run. This field will only be sent for expand details filter.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def error(self) -> 'outputs.CloudErrorResponse':
        """
        Top level error for the job.
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Id of the object.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ResourceIdentityResponse']:
        """
        Msi identity of the resource
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="isCancellable")
    def is_cancellable(self) -> bool:
        """
        Describes whether the job is cancellable or not.
        """
        return pulumi.get(self, "is_cancellable")

    @property
    @pulumi.getter(name="isCancellableWithoutFee")
    def is_cancellable_without_fee(self) -> bool:
        """
        Flag to indicate cancellation of scheduled job.
        """
        return pulumi.get(self, "is_cancellable_without_fee")

    @property
    @pulumi.getter(name="isDeletable")
    def is_deletable(self) -> bool:
        """
        Describes whether the job is deletable or not.
        """
        return pulumi.get(self, "is_deletable")

    @property
    @pulumi.getter(name="isPrepareToShipEnabled")
    def is_prepare_to_ship_enabled(self) -> bool:
        """
        Is Prepare To Ship Enabled on this job
        """
        return pulumi.get(self, "is_prepare_to_ship_enabled")

    @property
    @pulumi.getter(name="isShippingAddressEditable")
    def is_shipping_address_editable(self) -> bool:
        """
        Describes whether the shipping address is editable or not.
        """
        return pulumi.get(self, "is_shipping_address_editable")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the object.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The sku type.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        Time at which the job was started in UTC ISO 8601 format.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Name of the stage which is in progress.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transferType")
    def transfer_type(self) -> str:
        """
        Type of the data transfer.
        """
        return pulumi.get(self, "transfer_type")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the object.
        """
        return pulumi.get(self, "type")


class AwaitableGetJobResult(GetJobResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobResult(
            cancellation_reason=self.cancellation_reason,
            delivery_info=self.delivery_info,
            delivery_type=self.delivery_type,
            details=self.details,
            error=self.error,
            id=self.id,
            identity=self.identity,
            is_cancellable=self.is_cancellable,
            is_cancellable_without_fee=self.is_cancellable_without_fee,
            is_deletable=self.is_deletable,
            is_prepare_to_ship_enabled=self.is_prepare_to_ship_enabled,
            is_shipping_address_editable=self.is_shipping_address_editable,
            location=self.location,
            name=self.name,
            sku=self.sku,
            start_time=self.start_time,
            status=self.status,
            system_data=self.system_data,
            tags=self.tags,
            transfer_type=self.transfer_type,
            type=self.type)


def get_job(expand: Optional[str] = None,
            job_name: Optional[str] = None,
            resource_group_name: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobResult:
    """
    Gets information about the specified job.


    :param str expand: $expand is supported on details parameter for job, which provides details on the job stages.
    :param str job_name: The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
    :param str resource_group_name: The Resource Group Name
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['jobName'] = job_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:databox/v20210501:getJob', __args__, opts=opts, typ=GetJobResult).value

    return AwaitableGetJobResult(
        cancellation_reason=__ret__.cancellation_reason,
        delivery_info=__ret__.delivery_info,
        delivery_type=__ret__.delivery_type,
        details=__ret__.details,
        error=__ret__.error,
        id=__ret__.id,
        identity=__ret__.identity,
        is_cancellable=__ret__.is_cancellable,
        is_cancellable_without_fee=__ret__.is_cancellable_without_fee,
        is_deletable=__ret__.is_deletable,
        is_prepare_to_ship_enabled=__ret__.is_prepare_to_ship_enabled,
        is_shipping_address_editable=__ret__.is_shipping_address_editable,
        location=__ret__.location,
        name=__ret__.name,
        sku=__ret__.sku,
        start_time=__ret__.start_time,
        status=__ret__.status,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        transfer_type=__ret__.transfer_type,
        type=__ret__.type)


@_utilities.lift_output_func(get_job)
def get_job_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                   job_name: Optional[pulumi.Input[str]] = None,
                   resource_group_name: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetJobResult]:
    """
    Gets information about the specified job.


    :param str expand: $expand is supported on details parameter for job, which provides details on the job stages.
    :param str job_name: The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
    :param str resource_group_name: The Resource Group Name
    """
    ...
