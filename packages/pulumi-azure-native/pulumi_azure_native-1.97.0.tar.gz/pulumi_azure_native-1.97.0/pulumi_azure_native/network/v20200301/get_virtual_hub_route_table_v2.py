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
    'GetVirtualHubRouteTableV2Result',
    'AwaitableGetVirtualHubRouteTableV2Result',
    'get_virtual_hub_route_table_v2',
    'get_virtual_hub_route_table_v2_output',
]

@pulumi.output_type
class GetVirtualHubRouteTableV2Result:
    """
    VirtualHubRouteTableV2 Resource.
    """
    def __init__(__self__, attached_connections=None, etag=None, id=None, name=None, provisioning_state=None, routes=None):
        if attached_connections and not isinstance(attached_connections, list):
            raise TypeError("Expected argument 'attached_connections' to be a list")
        pulumi.set(__self__, "attached_connections", attached_connections)
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
        if routes and not isinstance(routes, list):
            raise TypeError("Expected argument 'routes' to be a list")
        pulumi.set(__self__, "routes", routes)

    @property
    @pulumi.getter(name="attachedConnections")
    def attached_connections(self) -> Optional[Sequence[str]]:
        """
        List of all connections attached to this route table v2.
        """
        return pulumi.get(self, "attached_connections")

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
        The provisioning state of the virtual hub route table v2 resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def routes(self) -> Optional[Sequence['outputs.VirtualHubRouteV2Response']]:
        """
        List of all routes.
        """
        return pulumi.get(self, "routes")


class AwaitableGetVirtualHubRouteTableV2Result(GetVirtualHubRouteTableV2Result):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualHubRouteTableV2Result(
            attached_connections=self.attached_connections,
            etag=self.etag,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            routes=self.routes)


def get_virtual_hub_route_table_v2(resource_group_name: Optional[str] = None,
                                   route_table_name: Optional[str] = None,
                                   virtual_hub_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualHubRouteTableV2Result:
    """
    Retrieves the details of a VirtualHubRouteTableV2.


    :param str resource_group_name: The resource group name of the VirtualHubRouteTableV2.
    :param str route_table_name: The name of the VirtualHubRouteTableV2.
    :param str virtual_hub_name: The name of the VirtualHub.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['routeTableName'] = route_table_name
    __args__['virtualHubName'] = virtual_hub_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200301:getVirtualHubRouteTableV2', __args__, opts=opts, typ=GetVirtualHubRouteTableV2Result).value

    return AwaitableGetVirtualHubRouteTableV2Result(
        attached_connections=__ret__.attached_connections,
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        routes=__ret__.routes)


@_utilities.lift_output_func(get_virtual_hub_route_table_v2)
def get_virtual_hub_route_table_v2_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                          route_table_name: Optional[pulumi.Input[str]] = None,
                                          virtual_hub_name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualHubRouteTableV2Result]:
    """
    Retrieves the details of a VirtualHubRouteTableV2.


    :param str resource_group_name: The resource group name of the VirtualHubRouteTableV2.
    :param str route_table_name: The name of the VirtualHubRouteTableV2.
    :param str virtual_hub_name: The name of the VirtualHub.
    """
    ...
