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
    'GetGatewayCertificateAuthorityResult',
    'AwaitableGetGatewayCertificateAuthorityResult',
    'get_gateway_certificate_authority',
    'get_gateway_certificate_authority_output',
]

@pulumi.output_type
class GetGatewayCertificateAuthorityResult:
    """
    Gateway certificate authority details.
    """
    def __init__(__self__, id=None, is_trusted=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_trusted and not isinstance(is_trusted, bool):
            raise TypeError("Expected argument 'is_trusted' to be a bool")
        pulumi.set(__self__, "is_trusted", is_trusted)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
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
    @pulumi.getter(name="isTrusted")
    def is_trusted(self) -> Optional[bool]:
        """
        Determines whether certificate authority is trusted.
        """
        return pulumi.get(self, "is_trusted")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetGatewayCertificateAuthorityResult(GetGatewayCertificateAuthorityResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGatewayCertificateAuthorityResult(
            id=self.id,
            is_trusted=self.is_trusted,
            name=self.name,
            type=self.type)


def get_gateway_certificate_authority(certificate_id: Optional[str] = None,
                                      gateway_id: Optional[str] = None,
                                      resource_group_name: Optional[str] = None,
                                      service_name: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGatewayCertificateAuthorityResult:
    """
    Get assigned Gateway Certificate Authority details.


    :param str certificate_id: Identifier of the certificate entity. Must be unique in the current API Management service instance.
    :param str gateway_id: Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['certificateId'] = certificate_id
    __args__['gatewayId'] = gateway_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20210101preview:getGatewayCertificateAuthority', __args__, opts=opts, typ=GetGatewayCertificateAuthorityResult).value

    return AwaitableGetGatewayCertificateAuthorityResult(
        id=__ret__.id,
        is_trusted=__ret__.is_trusted,
        name=__ret__.name,
        type=__ret__.type)


@_utilities.lift_output_func(get_gateway_certificate_authority)
def get_gateway_certificate_authority_output(certificate_id: Optional[pulumi.Input[str]] = None,
                                             gateway_id: Optional[pulumi.Input[str]] = None,
                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                             service_name: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGatewayCertificateAuthorityResult]:
    """
    Get assigned Gateway Certificate Authority details.


    :param str certificate_id: Identifier of the certificate entity. Must be unique in the current API Management service instance.
    :param str gateway_id: Gateway entity identifier. Must be unique in the current API Management service instance. Must not have value 'managed'
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    ...
