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
    'GetExpressRoutePortAuthorizationResult',
    'AwaitableGetExpressRoutePortAuthorizationResult',
    'get_express_route_port_authorization',
    'get_express_route_port_authorization_output',
]

@pulumi.output_type
class GetExpressRoutePortAuthorizationResult:
    """
    ExpressRoutePort Authorization resource definition.
    """
    def __init__(__self__, authorization_key=None, authorization_use_status=None, circuit_resource_uri=None, etag=None, id=None, name=None, provisioning_state=None, type=None):
        if authorization_key and not isinstance(authorization_key, str):
            raise TypeError("Expected argument 'authorization_key' to be a str")
        pulumi.set(__self__, "authorization_key", authorization_key)
        if authorization_use_status and not isinstance(authorization_use_status, str):
            raise TypeError("Expected argument 'authorization_use_status' to be a str")
        pulumi.set(__self__, "authorization_use_status", authorization_use_status)
        if circuit_resource_uri and not isinstance(circuit_resource_uri, str):
            raise TypeError("Expected argument 'circuit_resource_uri' to be a str")
        pulumi.set(__self__, "circuit_resource_uri", circuit_resource_uri)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="authorizationKey")
    def authorization_key(self) -> str:
        """
        The authorization key.
        """
        return pulumi.get(self, "authorization_key")

    @property
    @pulumi.getter(name="authorizationUseStatus")
    def authorization_use_status(self) -> str:
        """
        The authorization use status.
        """
        return pulumi.get(self, "authorization_use_status")

    @property
    @pulumi.getter(name="circuitResourceUri")
    def circuit_resource_uri(self) -> str:
        """
        The reference to the ExpressRoute circuit resource using the authorization.
        """
        return pulumi.get(self, "circuit_resource_uri")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the authorization resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetExpressRoutePortAuthorizationResult(GetExpressRoutePortAuthorizationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetExpressRoutePortAuthorizationResult(
            authorization_key=self.authorization_key,
            authorization_use_status=self.authorization_use_status,
            circuit_resource_uri=self.circuit_resource_uri,
            etag=self.etag,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_express_route_port_authorization(authorization_name: Optional[str] = None,
                                         express_route_port_name: Optional[str] = None,
                                         resource_group_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetExpressRoutePortAuthorizationResult:
    """
    Gets the specified authorization from the specified express route port.


    :param str authorization_name: The name of the authorization.
    :param str express_route_port_name: The name of the express route port.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['authorizationName'] = authorization_name
    __args__['expressRoutePortName'] = express_route_port_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20220701:getExpressRoutePortAuthorization', __args__, opts=opts, typ=GetExpressRoutePortAuthorizationResult).value

    return AwaitableGetExpressRoutePortAuthorizationResult(
        authorization_key=__ret__.authorization_key,
        authorization_use_status=__ret__.authorization_use_status,
        circuit_resource_uri=__ret__.circuit_resource_uri,
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)


@_utilities.lift_output_func(get_express_route_port_authorization)
def get_express_route_port_authorization_output(authorization_name: Optional[pulumi.Input[str]] = None,
                                                express_route_port_name: Optional[pulumi.Input[str]] = None,
                                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetExpressRoutePortAuthorizationResult]:
    """
    Gets the specified authorization from the specified express route port.


    :param str authorization_name: The name of the authorization.
    :param str express_route_port_name: The name of the express route port.
    :param str resource_group_name: The name of the resource group.
    """
    ...
