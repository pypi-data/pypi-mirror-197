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
    'GetConfigurationProfileHCRPAssignmentResult',
    'AwaitableGetConfigurationProfileHCRPAssignmentResult',
    'get_configuration_profile_hcrpassignment',
    'get_configuration_profile_hcrpassignment_output',
]

@pulumi.output_type
class GetConfigurationProfileHCRPAssignmentResult:
    """
    Configuration profile assignment is an association between a VM and automanage profile configuration.
    """
    def __init__(__self__, id=None, managed_by=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if managed_by and not isinstance(managed_by, str):
            raise TypeError("Expected argument 'managed_by' to be a str")
        pulumi.set(__self__, "managed_by", managed_by)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> str:
        """
        Azure resource id. Indicates if this resource is managed by another Azure resource.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.ConfigurationProfileAssignmentPropertiesResponse':
        """
        Properties of the configuration profile assignment.
        """
        return pulumi.get(self, "properties")

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


class AwaitableGetConfigurationProfileHCRPAssignmentResult(GetConfigurationProfileHCRPAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConfigurationProfileHCRPAssignmentResult(
            id=self.id,
            managed_by=self.managed_by,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def get_configuration_profile_hcrpassignment(configuration_profile_assignment_name: Optional[str] = None,
                                             machine_name: Optional[str] = None,
                                             resource_group_name: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConfigurationProfileHCRPAssignmentResult:
    """
    Get information about a configuration profile assignment


    :param str configuration_profile_assignment_name: The configuration profile assignment name.
    :param str machine_name: The name of the Arc machine.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['configurationProfileAssignmentName'] = configuration_profile_assignment_name
    __args__['machineName'] = machine_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:automanage/v20220504:getConfigurationProfileHCRPAssignment', __args__, opts=opts, typ=GetConfigurationProfileHCRPAssignmentResult).value

    return AwaitableGetConfigurationProfileHCRPAssignmentResult(
        id=__ret__.id,
        managed_by=__ret__.managed_by,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_configuration_profile_hcrpassignment)
def get_configuration_profile_hcrpassignment_output(configuration_profile_assignment_name: Optional[pulumi.Input[str]] = None,
                                                    machine_name: Optional[pulumi.Input[str]] = None,
                                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConfigurationProfileHCRPAssignmentResult]:
    """
    Get information about a configuration profile assignment


    :param str configuration_profile_assignment_name: The configuration profile assignment name.
    :param str machine_name: The name of the Arc machine.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
