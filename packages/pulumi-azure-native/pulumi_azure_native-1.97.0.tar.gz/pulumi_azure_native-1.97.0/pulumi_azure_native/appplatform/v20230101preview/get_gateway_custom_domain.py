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
    'GetGatewayCustomDomainResult',
    'AwaitableGetGatewayCustomDomainResult',
    'get_gateway_custom_domain',
    'get_gateway_custom_domain_output',
]

@pulumi.output_type
class GetGatewayCustomDomainResult:
    """
    Custom domain of the Spring Cloud Gateway
    """
    def __init__(__self__, id=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
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
        Fully qualified resource Id for the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.GatewayCustomDomainPropertiesResponse':
        """
        The properties of custom domain for Spring Cloud Gateway
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetGatewayCustomDomainResult(GetGatewayCustomDomainResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGatewayCustomDomainResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def get_gateway_custom_domain(domain_name: Optional[str] = None,
                              gateway_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              service_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGatewayCustomDomainResult:
    """
    Get the Spring Cloud Gateway custom domain.


    :param str domain_name: The name of the Spring Cloud Gateway custom domain.
    :param str gateway_name: The name of Spring Cloud Gateway.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str service_name: The name of the Service resource.
    """
    __args__ = dict()
    __args__['domainName'] = domain_name
    __args__['gatewayName'] = gateway_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:appplatform/v20230101preview:getGatewayCustomDomain', __args__, opts=opts, typ=GetGatewayCustomDomainResult).value

    return AwaitableGetGatewayCustomDomainResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_gateway_custom_domain)
def get_gateway_custom_domain_output(domain_name: Optional[pulumi.Input[str]] = None,
                                     gateway_name: Optional[pulumi.Input[str]] = None,
                                     resource_group_name: Optional[pulumi.Input[str]] = None,
                                     service_name: Optional[pulumi.Input[str]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGatewayCustomDomainResult]:
    """
    Get the Spring Cloud Gateway custom domain.


    :param str domain_name: The name of the Spring Cloud Gateway custom domain.
    :param str gateway_name: The name of Spring Cloud Gateway.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str service_name: The name of the Service resource.
    """
    ...
