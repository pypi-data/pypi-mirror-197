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
    'GetCustomLocationResult',
    'AwaitableGetCustomLocationResult',
    'get_custom_location',
    'get_custom_location_output',
]

@pulumi.output_type
class GetCustomLocationResult:
    """
    Custom Locations definition.
    """
    def __init__(__self__, authentication=None, cluster_extension_ids=None, display_name=None, host_resource_id=None, host_type=None, id=None, identity=None, location=None, name=None, namespace=None, provisioning_state=None, system_data=None, tags=None, type=None):
        if authentication and not isinstance(authentication, dict):
            raise TypeError("Expected argument 'authentication' to be a dict")
        pulumi.set(__self__, "authentication", authentication)
        if cluster_extension_ids and not isinstance(cluster_extension_ids, list):
            raise TypeError("Expected argument 'cluster_extension_ids' to be a list")
        pulumi.set(__self__, "cluster_extension_ids", cluster_extension_ids)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if host_resource_id and not isinstance(host_resource_id, str):
            raise TypeError("Expected argument 'host_resource_id' to be a str")
        pulumi.set(__self__, "host_resource_id", host_resource_id)
        if host_type and not isinstance(host_type, str):
            raise TypeError("Expected argument 'host_type' to be a str")
        pulumi.set(__self__, "host_type", host_type)
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
        if namespace and not isinstance(namespace, str):
            raise TypeError("Expected argument 'namespace' to be a str")
        pulumi.set(__self__, "namespace", namespace)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
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
    def authentication(self) -> Optional['outputs.CustomLocationPropertiesResponseAuthentication']:
        """
        This is optional input that contains the authentication that should be used to generate the namespace.
        """
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter(name="clusterExtensionIds")
    def cluster_extension_ids(self) -> Optional[Sequence[str]]:
        """
        Contains the reference to the add-on that contains charts to deploy CRDs and operators.
        """
        return pulumi.get(self, "cluster_extension_ids")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Display name for the Custom Locations location.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="hostResourceId")
    def host_resource_id(self) -> Optional[str]:
        """
        Connected Cluster or AKS Cluster. The Custom Locations RP will perform a checkAccess API for listAdminCredentials permissions.
        """
        return pulumi.get(self, "host_resource_id")

    @property
    @pulumi.getter(name="hostType")
    def host_type(self) -> Optional[str]:
        """
        Type of host the Custom Locations is referencing (Kubernetes, etc...).
        """
        return pulumi.get(self, "host_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        Identity for the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        """
        Kubernetes namespace that will be created on the specified cluster.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        Provisioning State for the Custom Location.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource
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


class AwaitableGetCustomLocationResult(GetCustomLocationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCustomLocationResult(
            authentication=self.authentication,
            cluster_extension_ids=self.cluster_extension_ids,
            display_name=self.display_name,
            host_resource_id=self.host_resource_id,
            host_type=self.host_type,
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            namespace=self.namespace,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_custom_location(resource_group_name: Optional[str] = None,
                        resource_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCustomLocationResult:
    """
    Gets the details of the customLocation with a specified resource group and name.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: Custom Locations name.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:extendedlocation/v20210831preview:getCustomLocation', __args__, opts=opts, typ=GetCustomLocationResult).value

    return AwaitableGetCustomLocationResult(
        authentication=__ret__.authentication,
        cluster_extension_ids=__ret__.cluster_extension_ids,
        display_name=__ret__.display_name,
        host_resource_id=__ret__.host_resource_id,
        host_type=__ret__.host_type,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        namespace=__ret__.namespace,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_custom_location)
def get_custom_location_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                               resource_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCustomLocationResult]:
    """
    Gets the details of the customLocation with a specified resource group and name.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: Custom Locations name.
    """
    ...
