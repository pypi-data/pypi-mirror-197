# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetGatewayHostnameConfigurationResult',
    'AwaitableGetGatewayHostnameConfigurationResult',
    'get_gateway_hostname_configuration',
    'get_gateway_hostname_configuration_output',
]

@pulumi.output_type
class GetGatewayHostnameConfigurationResult:
    """
    Gateway hostname configuration details.
    """
    def __init__(__self__, certificate_id=None, hostname=None, id=None, name=None, negotiate_client_certificate=None, type=None):
        if certificate_id and not isinstance(certificate_id, str):
            raise TypeError("Expected argument 'certificate_id' to be a str")
        pulumi.set(__self__, "certificate_id", certificate_id)
        if hostname and not isinstance(hostname, str):
            raise TypeError("Expected argument 'hostname' to be a str")
        pulumi.set(__self__, "hostname", hostname)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if negotiate_client_certificate and not isinstance(negotiate_client_certificate, bool):
            raise TypeError("Expected argument 'negotiate_client_certificate' to be a bool")
        pulumi.set(__self__, "negotiate_client_certificate", negotiate_client_certificate)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="certificateId")
    def certificate_id(self) -> Optional[str]:
        """
        Identifier of Certificate entity that will be used for TLS connection establishment
        """
        return pulumi.get(self, "certificate_id")

    @property
    @pulumi.getter
    def hostname(self) -> Optional[str]:
        """
        Hostname value. Supports valid domain name, partial or full wildcard
        """
        return pulumi.get(self, "hostname")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="negotiateClientCertificate")
    def negotiate_client_certificate(self) -> Optional[bool]:
        """
        Determines whether gateway requests client certificate
        """
        return pulumi.get(self, "negotiate_client_certificate")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetGatewayHostnameConfigurationResult(GetGatewayHostnameConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGatewayHostnameConfigurationResult(
            certificate_id=self.certificate_id,
            hostname=self.hostname,
            id=self.id,
            name=self.name,
            negotiate_client_certificate=self.negotiate_client_certificate,
            type=self.type)


def get_gateway_hostname_configuration(gateway_id: Optional[str] = None,
                                       hc_id: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       service_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGatewayHostnameConfigurationResult:
    """
    Gets the details of the Gateway hostname configuration specified by its identifier.


    :param str gateway_id: Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
    :param str hc_id: Gateway hostname configuration identifier. Must be unique in the scope of parent Gateway entity.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['gatewayId'] = gateway_id
    __args__['hcId'] = hc_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20191201preview:getGatewayHostnameConfiguration', __args__, opts=opts, typ=GetGatewayHostnameConfigurationResult).value

    return AwaitableGetGatewayHostnameConfigurationResult(
        certificate_id=__ret__.certificate_id,
        hostname=__ret__.hostname,
        id=__ret__.id,
        name=__ret__.name,
        negotiate_client_certificate=__ret__.negotiate_client_certificate,
        type=__ret__.type)


@_utilities.lift_output_func(get_gateway_hostname_configuration)
def get_gateway_hostname_configuration_output(gateway_id: Optional[pulumi.Input[str]] = None,
                                              hc_id: Optional[pulumi.Input[str]] = None,
                                              resource_group_name: Optional[pulumi.Input[str]] = None,
                                              service_name: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGatewayHostnameConfigurationResult]:
    """
    Gets the details of the Gateway hostname configuration specified by its identifier.


    :param str gateway_id: Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
    :param str hc_id: Gateway hostname configuration identifier. Must be unique in the scope of parent Gateway entity.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    ...
