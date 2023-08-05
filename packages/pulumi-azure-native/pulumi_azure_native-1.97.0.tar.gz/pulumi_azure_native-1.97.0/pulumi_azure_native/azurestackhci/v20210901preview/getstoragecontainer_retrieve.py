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
    'GetstoragecontainerRetrieveResult',
    'AwaitableGetstoragecontainerRetrieveResult',
    'getstoragecontainer_retrieve',
    'getstoragecontainer_retrieve_output',
]

@pulumi.output_type
class GetstoragecontainerRetrieveResult:
    """
    The storage container resource definition.
    """
    def __init__(__self__, available_size_mb=None, container_size_mb=None, extended_location=None, id=None, location=None, name=None, path=None, provisioning_state=None, resource_name=None, status=None, system_data=None, tags=None, type=None):
        if available_size_mb and not isinstance(available_size_mb, float):
            raise TypeError("Expected argument 'available_size_mb' to be a float")
        pulumi.set(__self__, "available_size_mb", available_size_mb)
        if container_size_mb and not isinstance(container_size_mb, float):
            raise TypeError("Expected argument 'container_size_mb' to be a float")
        pulumi.set(__self__, "container_size_mb", container_size_mb)
        if extended_location and not isinstance(extended_location, dict):
            raise TypeError("Expected argument 'extended_location' to be a dict")
        pulumi.set(__self__, "extended_location", extended_location)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if path and not isinstance(path, str):
            raise TypeError("Expected argument 'path' to be a str")
        pulumi.set(__self__, "path", path)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_name and not isinstance(resource_name, str):
            raise TypeError("Expected argument 'resource_name' to be a str")
        pulumi.set(__self__, "resource_name", resource_name)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
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
    @pulumi.getter(name="availableSizeMB")
    def available_size_mb(self) -> float:
        """
        Amount of space available on the disk in MB
        """
        return pulumi.get(self, "available_size_mb")

    @property
    @pulumi.getter(name="containerSizeMB")
    def container_size_mb(self) -> float:
        """
        Total size of the disk in MB
        """
        return pulumi.get(self, "container_size_mb")

    @property
    @pulumi.getter(name="extendedLocation")
    def extended_location(self) -> Optional['outputs.StoragecontainersResponseExtendedLocation']:
        return pulumi.get(self, "extended_location")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        Path of the storage container on the disk
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[str]:
        """
        name of the object to be used in moc
        """
        return pulumi.get(self, "resource_name")

    @property
    @pulumi.getter
    def status(self) -> 'outputs.StorageContainerStatusResponse':
        """
        storageContainerStatus defines the observed state of storagecontainers
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource Type
        """
        return pulumi.get(self, "type")


class AwaitableGetstoragecontainerRetrieveResult(GetstoragecontainerRetrieveResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetstoragecontainerRetrieveResult(
            available_size_mb=self.available_size_mb,
            container_size_mb=self.container_size_mb,
            extended_location=self.extended_location,
            id=self.id,
            location=self.location,
            name=self.name,
            path=self.path,
            provisioning_state=self.provisioning_state,
            resource_name=self.resource_name,
            status=self.status,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def getstoragecontainer_retrieve(resource_group_name: Optional[str] = None,
                                 storagecontainers_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetstoragecontainerRetrieveResult:
    """
    Gets storagecontainers by resource name


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['storagecontainersName'] = storagecontainers_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:azurestackhci/v20210901preview:getstoragecontainerRetrieve', __args__, opts=opts, typ=GetstoragecontainerRetrieveResult).value

    return AwaitableGetstoragecontainerRetrieveResult(
        available_size_mb=__ret__.available_size_mb,
        container_size_mb=__ret__.container_size_mb,
        extended_location=__ret__.extended_location,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        path=__ret__.path,
        provisioning_state=__ret__.provisioning_state,
        resource_name=__ret__.resource_name,
        status=__ret__.status,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(getstoragecontainer_retrieve)
def getstoragecontainer_retrieve_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                        storagecontainers_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetstoragecontainerRetrieveResult]:
    """
    Gets storagecontainers by resource name


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
