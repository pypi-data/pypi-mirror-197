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
    'GetAKSServiceResult',
    'AwaitableGetAKSServiceResult',
    'get_aks_service',
    'get_aks_service_output',
]

@pulumi.output_type
class GetAKSServiceResult:
    """
    Machine Learning service object wrapped into ARM resource envelope.
    """
    def __init__(__self__, id=None, identity=None, location=None, name=None, properties=None, sku=None, system_data=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Specifies the resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Specifies the location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Specifies the name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> Any:
        """
        Service properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The sku of the workspace.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Contains resource tags defined as key/value pairs.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetAKSServiceResult(GetAKSServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAKSServiceResult(
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            properties=self.properties,
            sku=self.sku,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_aks_service(expand: Optional[bool] = None,
                    resource_group_name: Optional[str] = None,
                    service_name: Optional[str] = None,
                    workspace_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAKSServiceResult:
    """
    Get a Service by name.
    API Version: 2021-01-01.


    :param bool expand: Set to True to include Model details.
    :param str resource_group_name: Name of the resource group in which workspace is located.
    :param str service_name: Name of the Azure Machine Learning service.
    :param str workspace_name: Name of Azure Machine Learning workspace.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearningservices:getAKSService', __args__, opts=opts, typ=GetAKSServiceResult).value

    return AwaitableGetAKSServiceResult(
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        properties=__ret__.properties,
        sku=__ret__.sku,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_aks_service)
def get_aks_service_output(expand: Optional[pulumi.Input[Optional[bool]]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           service_name: Optional[pulumi.Input[str]] = None,
                           workspace_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAKSServiceResult]:
    """
    Get a Service by name.
    API Version: 2021-01-01.


    :param bool expand: Set to True to include Model details.
    :param str resource_group_name: Name of the resource group in which workspace is located.
    :param str service_name: Name of the Azure Machine Learning service.
    :param str workspace_name: Name of Azure Machine Learning workspace.
    """
    ...
