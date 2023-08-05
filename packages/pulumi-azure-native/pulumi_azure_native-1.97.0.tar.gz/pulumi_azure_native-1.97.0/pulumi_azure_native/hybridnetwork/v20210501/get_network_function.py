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
    'GetNetworkFunctionResult',
    'AwaitableGetNetworkFunctionResult',
    'get_network_function',
    'get_network_function_output',
]

@pulumi.output_type
class GetNetworkFunctionResult:
    """
    Network function resource response.
    """
    def __init__(__self__, device=None, etag=None, id=None, location=None, managed_application=None, managed_application_parameters=None, name=None, network_function_container_configurations=None, network_function_user_configurations=None, provisioning_state=None, service_key=None, sku_name=None, sku_type=None, system_data=None, tags=None, type=None, vendor_name=None, vendor_provisioning_state=None):
        if device and not isinstance(device, dict):
            raise TypeError("Expected argument 'device' to be a dict")
        pulumi.set(__self__, "device", device)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_application and not isinstance(managed_application, dict):
            raise TypeError("Expected argument 'managed_application' to be a dict")
        pulumi.set(__self__, "managed_application", managed_application)
        if managed_application_parameters and not isinstance(managed_application_parameters, dict):
            raise TypeError("Expected argument 'managed_application_parameters' to be a dict")
        pulumi.set(__self__, "managed_application_parameters", managed_application_parameters)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_function_container_configurations and not isinstance(network_function_container_configurations, dict):
            raise TypeError("Expected argument 'network_function_container_configurations' to be a dict")
        pulumi.set(__self__, "network_function_container_configurations", network_function_container_configurations)
        if network_function_user_configurations and not isinstance(network_function_user_configurations, list):
            raise TypeError("Expected argument 'network_function_user_configurations' to be a list")
        pulumi.set(__self__, "network_function_user_configurations", network_function_user_configurations)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if service_key and not isinstance(service_key, str):
            raise TypeError("Expected argument 'service_key' to be a str")
        pulumi.set(__self__, "service_key", service_key)
        if sku_name and not isinstance(sku_name, str):
            raise TypeError("Expected argument 'sku_name' to be a str")
        pulumi.set(__self__, "sku_name", sku_name)
        if sku_type and not isinstance(sku_type, str):
            raise TypeError("Expected argument 'sku_type' to be a str")
        pulumi.set(__self__, "sku_type", sku_type)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vendor_name and not isinstance(vendor_name, str):
            raise TypeError("Expected argument 'vendor_name' to be a str")
        pulumi.set(__self__, "vendor_name", vendor_name)
        if vendor_provisioning_state and not isinstance(vendor_provisioning_state, str):
            raise TypeError("Expected argument 'vendor_provisioning_state' to be a str")
        pulumi.set(__self__, "vendor_provisioning_state", vendor_provisioning_state)

    @property
    @pulumi.getter
    def device(self) -> Optional['outputs.SubResourceResponse']:
        """
        The reference to the device resource. Once set, it cannot be updated.
        """
        return pulumi.get(self, "device")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
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
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedApplication")
    def managed_application(self) -> 'outputs.SubResourceResponse':
        """
        The resource URI of the managed application.
        """
        return pulumi.get(self, "managed_application")

    @property
    @pulumi.getter(name="managedApplicationParameters")
    def managed_application_parameters(self) -> Optional[Any]:
        """
        The parameters for the managed application.
        """
        return pulumi.get(self, "managed_application_parameters")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkFunctionContainerConfigurations")
    def network_function_container_configurations(self) -> Optional[Any]:
        """
        The network function container configurations from the user.
        """
        return pulumi.get(self, "network_function_container_configurations")

    @property
    @pulumi.getter(name="networkFunctionUserConfigurations")
    def network_function_user_configurations(self) -> Optional[Sequence['outputs.NetworkFunctionUserConfigurationResponse']]:
        """
        The network function configurations from the user.
        """
        return pulumi.get(self, "network_function_user_configurations")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the network function resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceKey")
    def service_key(self) -> str:
        """
        The service key for the network function resource.
        """
        return pulumi.get(self, "service_key")

    @property
    @pulumi.getter(name="skuName")
    def sku_name(self) -> Optional[str]:
        """
        The sku name for the network function. Once set, it cannot be updated.
        """
        return pulumi.get(self, "sku_name")

    @property
    @pulumi.getter(name="skuType")
    def sku_type(self) -> str:
        """
        The sku type for the network function.
        """
        return pulumi.get(self, "sku_type")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
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

    @property
    @pulumi.getter(name="vendorName")
    def vendor_name(self) -> Optional[str]:
        """
        The vendor name for the network function. Once set, it cannot be updated.
        """
        return pulumi.get(self, "vendor_name")

    @property
    @pulumi.getter(name="vendorProvisioningState")
    def vendor_provisioning_state(self) -> str:
        """
        The vendor provisioning state for the network function resource.
        """
        return pulumi.get(self, "vendor_provisioning_state")


class AwaitableGetNetworkFunctionResult(GetNetworkFunctionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkFunctionResult(
            device=self.device,
            etag=self.etag,
            id=self.id,
            location=self.location,
            managed_application=self.managed_application,
            managed_application_parameters=self.managed_application_parameters,
            name=self.name,
            network_function_container_configurations=self.network_function_container_configurations,
            network_function_user_configurations=self.network_function_user_configurations,
            provisioning_state=self.provisioning_state,
            service_key=self.service_key,
            sku_name=self.sku_name,
            sku_type=self.sku_type,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            vendor_name=self.vendor_name,
            vendor_provisioning_state=self.vendor_provisioning_state)


def get_network_function(network_function_name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkFunctionResult:
    """
    Gets information about the specified network function resource.


    :param str network_function_name: The name of the network function resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['networkFunctionName'] = network_function_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:hybridnetwork/v20210501:getNetworkFunction', __args__, opts=opts, typ=GetNetworkFunctionResult).value

    return AwaitableGetNetworkFunctionResult(
        device=__ret__.device,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        managed_application=__ret__.managed_application,
        managed_application_parameters=__ret__.managed_application_parameters,
        name=__ret__.name,
        network_function_container_configurations=__ret__.network_function_container_configurations,
        network_function_user_configurations=__ret__.network_function_user_configurations,
        provisioning_state=__ret__.provisioning_state,
        service_key=__ret__.service_key,
        sku_name=__ret__.sku_name,
        sku_type=__ret__.sku_type,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        vendor_name=__ret__.vendor_name,
        vendor_provisioning_state=__ret__.vendor_provisioning_state)


@_utilities.lift_output_func(get_network_function)
def get_network_function_output(network_function_name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkFunctionResult]:
    """
    Gets information about the specified network function resource.


    :param str network_function_name: The name of the network function resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
