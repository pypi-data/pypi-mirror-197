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
    'GetManagementAssociationResult',
    'AwaitableGetManagementAssociationResult',
    'get_management_association',
    'get_management_association_output',
]

@pulumi.output_type
class GetManagementAssociationResult:
    """
    The container for solution.
    """
    def __init__(__self__, id=None, location=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ManagementAssociationPropertiesResponse':
        """
        Properties for ManagementAssociation object supported by the OperationsManagement resource provider.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetManagementAssociationResult(GetManagementAssociationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagementAssociationResult(
            id=self.id,
            location=self.location,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_management_association(management_association_name: Optional[str] = None,
                               provider_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               resource_name: Optional[str] = None,
                               resource_type: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagementAssociationResult:
    """
    Retrieves the user ManagementAssociation.


    :param str management_association_name: User ManagementAssociation Name.
    :param str provider_name: Provider name for the parent resource.
    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    :param str resource_name: Parent resource name.
    :param str resource_type: Resource type for the parent resource
    """
    __args__ = dict()
    __args__['managementAssociationName'] = management_association_name
    __args__['providerName'] = provider_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    __args__['resourceType'] = resource_type
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:operationsmanagement/v20151101preview:getManagementAssociation', __args__, opts=opts, typ=GetManagementAssociationResult).value

    return AwaitableGetManagementAssociationResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)


@_utilities.lift_output_func(get_management_association)
def get_management_association_output(management_association_name: Optional[pulumi.Input[str]] = None,
                                      provider_name: Optional[pulumi.Input[str]] = None,
                                      resource_group_name: Optional[pulumi.Input[str]] = None,
                                      resource_name: Optional[pulumi.Input[str]] = None,
                                      resource_type: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagementAssociationResult]:
    """
    Retrieves the user ManagementAssociation.


    :param str management_association_name: User ManagementAssociation Name.
    :param str provider_name: Provider name for the parent resource.
    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    :param str resource_name: Parent resource name.
    :param str resource_type: Resource type for the parent resource
    """
    ...
