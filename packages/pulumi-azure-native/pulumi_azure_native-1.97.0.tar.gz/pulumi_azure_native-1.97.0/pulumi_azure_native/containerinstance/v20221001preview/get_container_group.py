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
    'GetContainerGroupResult',
    'AwaitableGetContainerGroupResult',
    'get_container_group',
    'get_container_group_output',
]

@pulumi.output_type
class GetContainerGroupResult:
    """
    A container group.
    """
    def __init__(__self__, confidential_compute_properties=None, containers=None, diagnostics=None, dns_config=None, encryption_properties=None, extensions=None, id=None, identity=None, image_registry_credentials=None, init_containers=None, instance_view=None, ip_address=None, location=None, name=None, os_type=None, priority=None, provisioning_state=None, restart_policy=None, sku=None, subnet_ids=None, tags=None, type=None, volumes=None, zones=None):
        if confidential_compute_properties and not isinstance(confidential_compute_properties, dict):
            raise TypeError("Expected argument 'confidential_compute_properties' to be a dict")
        pulumi.set(__self__, "confidential_compute_properties", confidential_compute_properties)
        if containers and not isinstance(containers, list):
            raise TypeError("Expected argument 'containers' to be a list")
        pulumi.set(__self__, "containers", containers)
        if diagnostics and not isinstance(diagnostics, dict):
            raise TypeError("Expected argument 'diagnostics' to be a dict")
        pulumi.set(__self__, "diagnostics", diagnostics)
        if dns_config and not isinstance(dns_config, dict):
            raise TypeError("Expected argument 'dns_config' to be a dict")
        pulumi.set(__self__, "dns_config", dns_config)
        if encryption_properties and not isinstance(encryption_properties, dict):
            raise TypeError("Expected argument 'encryption_properties' to be a dict")
        pulumi.set(__self__, "encryption_properties", encryption_properties)
        if extensions and not isinstance(extensions, list):
            raise TypeError("Expected argument 'extensions' to be a list")
        pulumi.set(__self__, "extensions", extensions)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if image_registry_credentials and not isinstance(image_registry_credentials, list):
            raise TypeError("Expected argument 'image_registry_credentials' to be a list")
        pulumi.set(__self__, "image_registry_credentials", image_registry_credentials)
        if init_containers and not isinstance(init_containers, list):
            raise TypeError("Expected argument 'init_containers' to be a list")
        pulumi.set(__self__, "init_containers", init_containers)
        if instance_view and not isinstance(instance_view, dict):
            raise TypeError("Expected argument 'instance_view' to be a dict")
        pulumi.set(__self__, "instance_view", instance_view)
        if ip_address and not isinstance(ip_address, dict):
            raise TypeError("Expected argument 'ip_address' to be a dict")
        pulumi.set(__self__, "ip_address", ip_address)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if priority and not isinstance(priority, str):
            raise TypeError("Expected argument 'priority' to be a str")
        pulumi.set(__self__, "priority", priority)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if restart_policy and not isinstance(restart_policy, str):
            raise TypeError("Expected argument 'restart_policy' to be a str")
        pulumi.set(__self__, "restart_policy", restart_policy)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if volumes and not isinstance(volumes, list):
            raise TypeError("Expected argument 'volumes' to be a list")
        pulumi.set(__self__, "volumes", volumes)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="confidentialComputeProperties")
    def confidential_compute_properties(self) -> Optional['outputs.ConfidentialComputePropertiesResponse']:
        """
        The properties for confidential container group
        """
        return pulumi.get(self, "confidential_compute_properties")

    @property
    @pulumi.getter
    def containers(self) -> Sequence['outputs.ContainerResponse']:
        """
        The containers within the container group.
        """
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter
    def diagnostics(self) -> Optional['outputs.ContainerGroupDiagnosticsResponse']:
        """
        The diagnostic information for a container group.
        """
        return pulumi.get(self, "diagnostics")

    @property
    @pulumi.getter(name="dnsConfig")
    def dns_config(self) -> Optional['outputs.DnsConfigurationResponse']:
        """
        The DNS config information for a container group.
        """
        return pulumi.get(self, "dns_config")

    @property
    @pulumi.getter(name="encryptionProperties")
    def encryption_properties(self) -> Optional['outputs.EncryptionPropertiesResponse']:
        """
        The encryption properties for a container group.
        """
        return pulumi.get(self, "encryption_properties")

    @property
    @pulumi.getter
    def extensions(self) -> Optional[Sequence['outputs.DeploymentExtensionSpecResponse']]:
        """
        extensions used by virtual kubelet
        """
        return pulumi.get(self, "extensions")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ContainerGroupIdentityResponse']:
        """
        The identity of the container group, if configured.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="imageRegistryCredentials")
    def image_registry_credentials(self) -> Optional[Sequence['outputs.ImageRegistryCredentialResponse']]:
        """
        The image registry credentials by which the container group is created from.
        """
        return pulumi.get(self, "image_registry_credentials")

    @property
    @pulumi.getter(name="initContainers")
    def init_containers(self) -> Optional[Sequence['outputs.InitContainerDefinitionResponse']]:
        """
        The init containers for a container group.
        """
        return pulumi.get(self, "init_containers")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> 'outputs.ContainerGroupPropertiesResponseInstanceView':
        """
        The instance view of the container group. Only valid in response.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional['outputs.IpAddressResponse']:
        """
        The IP address type of the container group.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> str:
        """
        The operating system type required by the containers in the container group.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter
    def priority(self) -> Optional[str]:
        """
        The priority of the container group.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the container group. This only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> Optional[str]:
        """
        Restart policy for all containers within the container group. 
        - `Always` Always restart
        - `OnFailure` Restart on failure
        - `Never` Never restart
        """
        return pulumi.get(self, "restart_policy")

    @property
    @pulumi.getter
    def sku(self) -> Optional[str]:
        """
        The SKU for a container group.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[Sequence['outputs.ContainerGroupSubnetIdResponse']]:
        """
        The subnet resource IDs for a container group.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def volumes(self) -> Optional[Sequence['outputs.VolumeResponse']]:
        """
        The list of volumes that can be mounted by containers in this container group.
        """
        return pulumi.get(self, "volumes")

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        The zones for the container group.
        """
        return pulumi.get(self, "zones")


class AwaitableGetContainerGroupResult(GetContainerGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetContainerGroupResult(
            confidential_compute_properties=self.confidential_compute_properties,
            containers=self.containers,
            diagnostics=self.diagnostics,
            dns_config=self.dns_config,
            encryption_properties=self.encryption_properties,
            extensions=self.extensions,
            id=self.id,
            identity=self.identity,
            image_registry_credentials=self.image_registry_credentials,
            init_containers=self.init_containers,
            instance_view=self.instance_view,
            ip_address=self.ip_address,
            location=self.location,
            name=self.name,
            os_type=self.os_type,
            priority=self.priority,
            provisioning_state=self.provisioning_state,
            restart_policy=self.restart_policy,
            sku=self.sku,
            subnet_ids=self.subnet_ids,
            tags=self.tags,
            type=self.type,
            volumes=self.volumes,
            zones=self.zones)


def get_container_group(container_group_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetContainerGroupResult:
    """
    Gets the properties of the specified container group in the specified subscription and resource group. The operation returns the properties of each container group including containers, image registry credentials, restart policy, IP address type, OS type, state, and volumes.


    :param str container_group_name: The name of the container group.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['containerGroupName'] = container_group_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:containerinstance/v20221001preview:getContainerGroup', __args__, opts=opts, typ=GetContainerGroupResult).value

    return AwaitableGetContainerGroupResult(
        confidential_compute_properties=__ret__.confidential_compute_properties,
        containers=__ret__.containers,
        diagnostics=__ret__.diagnostics,
        dns_config=__ret__.dns_config,
        encryption_properties=__ret__.encryption_properties,
        extensions=__ret__.extensions,
        id=__ret__.id,
        identity=__ret__.identity,
        image_registry_credentials=__ret__.image_registry_credentials,
        init_containers=__ret__.init_containers,
        instance_view=__ret__.instance_view,
        ip_address=__ret__.ip_address,
        location=__ret__.location,
        name=__ret__.name,
        os_type=__ret__.os_type,
        priority=__ret__.priority,
        provisioning_state=__ret__.provisioning_state,
        restart_policy=__ret__.restart_policy,
        sku=__ret__.sku,
        subnet_ids=__ret__.subnet_ids,
        tags=__ret__.tags,
        type=__ret__.type,
        volumes=__ret__.volumes,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_container_group)
def get_container_group_output(container_group_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetContainerGroupResult]:
    """
    Gets the properties of the specified container group in the specified subscription and resource group. The operation returns the properties of each container group including containers, image registry credentials, restart policy, IP address type, OS type, state, and volumes.


    :param str container_group_name: The name of the container group.
    :param str resource_group_name: The name of the resource group.
    """
    ...
