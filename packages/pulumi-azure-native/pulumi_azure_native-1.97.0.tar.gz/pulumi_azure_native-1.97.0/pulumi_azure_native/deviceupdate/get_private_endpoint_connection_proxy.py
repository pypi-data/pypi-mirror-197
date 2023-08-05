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
    'GetPrivateEndpointConnectionProxyResult',
    'AwaitableGetPrivateEndpointConnectionProxyResult',
    'get_private_endpoint_connection_proxy',
    'get_private_endpoint_connection_proxy_output',
]

@pulumi.output_type
class GetPrivateEndpointConnectionProxyResult:
    """
    Private endpoint connection proxy details.
    """
    def __init__(__self__, e_tag=None, id=None, name=None, provisioning_state=None, remote_private_endpoint=None, status=None, system_data=None, type=None):
        if e_tag and not isinstance(e_tag, str):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, "e_tag", e_tag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if remote_private_endpoint and not isinstance(remote_private_endpoint, dict):
            raise TypeError("Expected argument 'remote_private_endpoint' to be a dict")
        pulumi.set(__self__, "remote_private_endpoint", remote_private_endpoint)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> str:
        """
        ETag from NRP.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the private endpoint connection proxy resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="remotePrivateEndpoint")
    def remote_private_endpoint(self) -> Optional['outputs.RemotePrivateEndpointResponse']:
        """
        Remote private endpoint details.
        """
        return pulumi.get(self, "remote_private_endpoint")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Operation status.
        """
        return pulumi.get(self, "status")

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


class AwaitableGetPrivateEndpointConnectionProxyResult(GetPrivateEndpointConnectionProxyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateEndpointConnectionProxyResult(
            e_tag=self.e_tag,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            remote_private_endpoint=self.remote_private_endpoint,
            status=self.status,
            system_data=self.system_data,
            type=self.type)


def get_private_endpoint_connection_proxy(account_name: Optional[str] = None,
                                          private_endpoint_connection_proxy_id: Optional[str] = None,
                                          resource_group_name: Optional[str] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateEndpointConnectionProxyResult:
    """
    (INTERNAL - DO NOT USE) Get the specified private endpoint connection proxy associated with the device update account.
    API Version: 2020-03-01-preview.


    :param str account_name: Account name.
    :param str private_endpoint_connection_proxy_id: The ID of the private endpoint connection proxy object.
    :param str resource_group_name: The resource group name.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['privateEndpointConnectionProxyId'] = private_endpoint_connection_proxy_id
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:deviceupdate:getPrivateEndpointConnectionProxy', __args__, opts=opts, typ=GetPrivateEndpointConnectionProxyResult).value

    return AwaitableGetPrivateEndpointConnectionProxyResult(
        e_tag=__ret__.e_tag,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        remote_private_endpoint=__ret__.remote_private_endpoint,
        status=__ret__.status,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_private_endpoint_connection_proxy)
def get_private_endpoint_connection_proxy_output(account_name: Optional[pulumi.Input[str]] = None,
                                                 private_endpoint_connection_proxy_id: Optional[pulumi.Input[str]] = None,
                                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPrivateEndpointConnectionProxyResult]:
    """
    (INTERNAL - DO NOT USE) Get the specified private endpoint connection proxy associated with the device update account.
    API Version: 2020-03-01-preview.


    :param str account_name: Account name.
    :param str private_endpoint_connection_proxy_id: The ID of the private endpoint connection proxy object.
    :param str resource_group_name: The resource group name.
    """
    ...
