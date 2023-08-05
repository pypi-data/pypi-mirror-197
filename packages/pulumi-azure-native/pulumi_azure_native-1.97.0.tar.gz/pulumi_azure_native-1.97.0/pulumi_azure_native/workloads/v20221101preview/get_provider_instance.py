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
    'GetProviderInstanceResult',
    'AwaitableGetProviderInstanceResult',
    'get_provider_instance',
    'get_provider_instance_output',
]

@pulumi.output_type
class GetProviderInstanceResult:
    """
    A provider instance associated with SAP monitor.
    """
    def __init__(__self__, errors=None, id=None, identity=None, name=None, provider_settings=None, provisioning_state=None, system_data=None, type=None):
        if errors and not isinstance(errors, dict):
            raise TypeError("Expected argument 'errors' to be a dict")
        pulumi.set(__self__, "errors", errors)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provider_settings and not isinstance(provider_settings, dict):
            raise TypeError("Expected argument 'provider_settings' to be a dict")
        pulumi.set(__self__, "provider_settings", provider_settings)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def errors(self) -> 'outputs.ProviderInstancePropertiesResponseErrors':
        """
        Defines the provider instance errors.
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.UserAssignedServiceIdentityResponse']:
        """
        Managed service identity (user assigned identities)
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="providerSettings")
    def provider_settings(self) -> Optional[Any]:
        """
        Defines the provider instance errors.
        """
        return pulumi.get(self, "provider_settings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        State of provisioning of the provider instance
        """
        return pulumi.get(self, "provisioning_state")

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


class AwaitableGetProviderInstanceResult(GetProviderInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProviderInstanceResult(
            errors=self.errors,
            id=self.id,
            identity=self.identity,
            name=self.name,
            provider_settings=self.provider_settings,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            type=self.type)


def get_provider_instance(monitor_name: Optional[str] = None,
                          provider_instance_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProviderInstanceResult:
    """
    Gets properties of a provider instance for the specified subscription, resource group, SAP monitor name, and resource name.


    :param str monitor_name: Name of the SAP monitor resource.
    :param str provider_instance_name: Name of the provider instance.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['monitorName'] = monitor_name
    __args__['providerInstanceName'] = provider_instance_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:workloads/v20221101preview:getProviderInstance', __args__, opts=opts, typ=GetProviderInstanceResult).value

    return AwaitableGetProviderInstanceResult(
        errors=__ret__.errors,
        id=__ret__.id,
        identity=__ret__.identity,
        name=__ret__.name,
        provider_settings=__ret__.provider_settings,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_provider_instance)
def get_provider_instance_output(monitor_name: Optional[pulumi.Input[str]] = None,
                                 provider_instance_name: Optional[pulumi.Input[str]] = None,
                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProviderInstanceResult]:
    """
    Gets properties of a provider instance for the specified subscription, resource group, SAP monitor name, and resource name.


    :param str monitor_name: Name of the SAP monitor resource.
    :param str provider_instance_name: Name of the provider instance.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
