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
    'GetAddressByNameResult',
    'AwaitableGetAddressByNameResult',
    'get_address_by_name',
    'get_address_by_name_output',
]

@pulumi.output_type
class GetAddressByNameResult:
    """
    Address Resource.
    """
    def __init__(__self__, address_validation_status=None, contact_details=None, id=None, location=None, name=None, shipping_address=None, system_data=None, tags=None, type=None):
        if address_validation_status and not isinstance(address_validation_status, str):
            raise TypeError("Expected argument 'address_validation_status' to be a str")
        pulumi.set(__self__, "address_validation_status", address_validation_status)
        if contact_details and not isinstance(contact_details, dict):
            raise TypeError("Expected argument 'contact_details' to be a dict")
        pulumi.set(__self__, "contact_details", contact_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if shipping_address and not isinstance(shipping_address, dict):
            raise TypeError("Expected argument 'shipping_address' to be a dict")
        pulumi.set(__self__, "shipping_address", shipping_address)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="addressValidationStatus")
    def address_validation_status(self) -> str:
        """
        Status of address validation
        """
        return pulumi.get(self, "address_validation_status")

    @property
    @pulumi.getter(name="contactDetails")
    def contact_details(self) -> 'outputs.ContactDetailsResponse':
        """
        Contact details for the address
        """
        return pulumi.get(self, "contact_details")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="shippingAddress")
    def shipping_address(self) -> Optional['outputs.ShippingAddressResponse']:
        """
        Shipping details for the address
        """
        return pulumi.get(self, "shipping_address")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Represents resource creation and update time
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetAddressByNameResult(GetAddressByNameResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAddressByNameResult(
            address_validation_status=self.address_validation_status,
            contact_details=self.contact_details,
            id=self.id,
            location=self.location,
            name=self.name,
            shipping_address=self.shipping_address,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_address_by_name(address_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAddressByNameResult:
    """
    Gets information about the specified address.
    API Version: 2021-12-01.


    :param str address_name: The name of the address Resource within the specified resource group. address names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['addressName'] = address_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:edgeorder:getAddressByName', __args__, opts=opts, typ=GetAddressByNameResult).value

    return AwaitableGetAddressByNameResult(
        address_validation_status=__ret__.address_validation_status,
        contact_details=__ret__.contact_details,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        shipping_address=__ret__.shipping_address,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_address_by_name)
def get_address_by_name_output(address_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAddressByNameResult]:
    """
    Gets information about the specified address.
    API Version: 2021-12-01.


    :param str address_name: The name of the address Resource within the specified resource group. address names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
