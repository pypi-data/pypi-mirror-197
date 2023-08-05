# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'AzureFileVolumeArgs',
    'ContainerPortArgs',
    'ContainerArgs',
    'EnvironmentVariableArgs',
    'GitRepoVolumeArgs',
    'ImageRegistryCredentialArgs',
    'IpAddressArgs',
    'PortArgs',
    'ResourceLimitsArgs',
    'ResourceRequestsArgs',
    'ResourceRequirementsArgs',
    'VolumeMountArgs',
    'VolumeArgs',
]

@pulumi.input_type
class AzureFileVolumeArgs:
    def __init__(__self__, *,
                 share_name: pulumi.Input[str],
                 storage_account_name: pulumi.Input[str],
                 read_only: Optional[pulumi.Input[bool]] = None,
                 storage_account_key: Optional[pulumi.Input[str]] = None):
        """
        The properties of the Azure File volume. Azure File shares are mounted as volumes.
        :param pulumi.Input[str] share_name: The name of the Azure File share to be mounted as a volume.
        :param pulumi.Input[str] storage_account_name: The name of the storage account that contains the Azure File share.
        :param pulumi.Input[bool] read_only: The flag indicating whether the Azure File shared mounted as a volume is read-only.
        :param pulumi.Input[str] storage_account_key: The storage account access key used to access the Azure File share.
        """
        pulumi.set(__self__, "share_name", share_name)
        pulumi.set(__self__, "storage_account_name", storage_account_name)
        if read_only is not None:
            pulumi.set(__self__, "read_only", read_only)
        if storage_account_key is not None:
            pulumi.set(__self__, "storage_account_key", storage_account_key)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> pulumi.Input[str]:
        """
        The name of the Azure File share to be mounted as a volume.
        """
        return pulumi.get(self, "share_name")

    @share_name.setter
    def share_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "share_name", value)

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> pulumi.Input[str]:
        """
        The name of the storage account that contains the Azure File share.
        """
        return pulumi.get(self, "storage_account_name")

    @storage_account_name.setter
    def storage_account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_name", value)

    @property
    @pulumi.getter(name="readOnly")
    def read_only(self) -> Optional[pulumi.Input[bool]]:
        """
        The flag indicating whether the Azure File shared mounted as a volume is read-only.
        """
        return pulumi.get(self, "read_only")

    @read_only.setter
    def read_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "read_only", value)

    @property
    @pulumi.getter(name="storageAccountKey")
    def storage_account_key(self) -> Optional[pulumi.Input[str]]:
        """
        The storage account access key used to access the Azure File share.
        """
        return pulumi.get(self, "storage_account_key")

    @storage_account_key.setter
    def storage_account_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_key", value)


@pulumi.input_type
class ContainerPortArgs:
    def __init__(__self__, *,
                 port: pulumi.Input[int],
                 protocol: Optional[pulumi.Input[Union[str, 'ContainerNetworkProtocol']]] = None):
        """
        The port exposed on the container instance.
        :param pulumi.Input[int] port: The port number exposed within the container group.
        :param pulumi.Input[Union[str, 'ContainerNetworkProtocol']] protocol: The protocol associated with the port.
        """
        pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port number exposed within the container group.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[Union[str, 'ContainerNetworkProtocol']]]:
        """
        The protocol associated with the port.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[Union[str, 'ContainerNetworkProtocol']]]):
        pulumi.set(self, "protocol", value)


@pulumi.input_type
class ContainerArgs:
    def __init__(__self__, *,
                 image: pulumi.Input[str],
                 name: pulumi.Input[str],
                 resources: pulumi.Input['ResourceRequirementsArgs'],
                 command: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 environment_variables: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentVariableArgs']]]] = None,
                 ports: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerPortArgs']]]] = None,
                 volume_mounts: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeMountArgs']]]] = None):
        """
        A container instance.
        :param pulumi.Input[str] image: The name of the image used to create the container instance.
        :param pulumi.Input[str] name: The user-provided name of the container instance.
        :param pulumi.Input['ResourceRequirementsArgs'] resources: The resource requirements of the container instance.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] command: The commands to execute within the container instance in exec form.
        :param pulumi.Input[Sequence[pulumi.Input['EnvironmentVariableArgs']]] environment_variables: The environment variables to set in the container instance.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerPortArgs']]] ports: The exposed ports on the container instance.
        :param pulumi.Input[Sequence[pulumi.Input['VolumeMountArgs']]] volume_mounts: The volume mounts available to the container instance.
        """
        pulumi.set(__self__, "image", image)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resources", resources)
        if command is not None:
            pulumi.set(__self__, "command", command)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if ports is not None:
            pulumi.set(__self__, "ports", ports)
        if volume_mounts is not None:
            pulumi.set(__self__, "volume_mounts", volume_mounts)

    @property
    @pulumi.getter
    def image(self) -> pulumi.Input[str]:
        """
        The name of the image used to create the container instance.
        """
        return pulumi.get(self, "image")

    @image.setter
    def image(self, value: pulumi.Input[str]):
        pulumi.set(self, "image", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The user-provided name of the container instance.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Input['ResourceRequirementsArgs']:
        """
        The resource requirements of the container instance.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: pulumi.Input['ResourceRequirementsArgs']):
        pulumi.set(self, "resources", value)

    @property
    @pulumi.getter
    def command(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The commands to execute within the container instance in exec form.
        """
        return pulumi.get(self, "command")

    @command.setter
    def command(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "command", value)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentVariableArgs']]]]:
        """
        The environment variables to set in the container instance.
        """
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EnvironmentVariableArgs']]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter
    def ports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ContainerPortArgs']]]]:
        """
        The exposed ports on the container instance.
        """
        return pulumi.get(self, "ports")

    @ports.setter
    def ports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ContainerPortArgs']]]]):
        pulumi.set(self, "ports", value)

    @property
    @pulumi.getter(name="volumeMounts")
    def volume_mounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VolumeMountArgs']]]]:
        """
        The volume mounts available to the container instance.
        """
        return pulumi.get(self, "volume_mounts")

    @volume_mounts.setter
    def volume_mounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeMountArgs']]]]):
        pulumi.set(self, "volume_mounts", value)


@pulumi.input_type
class EnvironmentVariableArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        The environment variable to set within the container instance.
        :param pulumi.Input[str] name: The name of the environment variable.
        :param pulumi.Input[str] value: The value of the environment variable.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the environment variable.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the environment variable.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class GitRepoVolumeArgs:
    def __init__(__self__, *,
                 repository: pulumi.Input[str],
                 directory: Optional[pulumi.Input[str]] = None,
                 revision: Optional[pulumi.Input[str]] = None):
        """
        Represents a volume that is populated with the contents of a git repository
        :param pulumi.Input[str] repository: Repository URL
        :param pulumi.Input[str] directory: Target directory name. Must not contain or start with '..'.  If '.' is supplied, the volume directory will be the git repository.  Otherwise, if specified, the volume will contain the git repository in the subdirectory with the given name.
        :param pulumi.Input[str] revision: Commit hash for the specified revision.
        """
        pulumi.set(__self__, "repository", repository)
        if directory is not None:
            pulumi.set(__self__, "directory", directory)
        if revision is not None:
            pulumi.set(__self__, "revision", revision)

    @property
    @pulumi.getter
    def repository(self) -> pulumi.Input[str]:
        """
        Repository URL
        """
        return pulumi.get(self, "repository")

    @repository.setter
    def repository(self, value: pulumi.Input[str]):
        pulumi.set(self, "repository", value)

    @property
    @pulumi.getter
    def directory(self) -> Optional[pulumi.Input[str]]:
        """
        Target directory name. Must not contain or start with '..'.  If '.' is supplied, the volume directory will be the git repository.  Otherwise, if specified, the volume will contain the git repository in the subdirectory with the given name.
        """
        return pulumi.get(self, "directory")

    @directory.setter
    def directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory", value)

    @property
    @pulumi.getter
    def revision(self) -> Optional[pulumi.Input[str]]:
        """
        Commit hash for the specified revision.
        """
        return pulumi.get(self, "revision")

    @revision.setter
    def revision(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "revision", value)


@pulumi.input_type
class ImageRegistryCredentialArgs:
    def __init__(__self__, *,
                 server: pulumi.Input[str],
                 username: pulumi.Input[str],
                 password: Optional[pulumi.Input[str]] = None):
        """
        Image registry credential.
        :param pulumi.Input[str] server: The Docker image registry server without a protocol such as "http" and "https".
        :param pulumi.Input[str] username: The username for the private registry.
        :param pulumi.Input[str] password: The password for the private registry.
        """
        pulumi.set(__self__, "server", server)
        pulumi.set(__self__, "username", username)
        if password is not None:
            pulumi.set(__self__, "password", password)

    @property
    @pulumi.getter
    def server(self) -> pulumi.Input[str]:
        """
        The Docker image registry server without a protocol such as "http" and "https".
        """
        return pulumi.get(self, "server")

    @server.setter
    def server(self, value: pulumi.Input[str]):
        pulumi.set(self, "server", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        """
        The username for the private registry.
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password for the private registry.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)


@pulumi.input_type
class IpAddressArgs:
    def __init__(__self__, *,
                 ports: pulumi.Input[Sequence[pulumi.Input['PortArgs']]],
                 type: pulumi.Input[Union[str, 'ContainerGroupIpAddressType']],
                 dns_name_label: Optional[pulumi.Input[str]] = None,
                 ip: Optional[pulumi.Input[str]] = None):
        """
        IP address for the container group.
        :param pulumi.Input[Sequence[pulumi.Input['PortArgs']]] ports: The list of ports exposed on the container group.
        :param pulumi.Input[Union[str, 'ContainerGroupIpAddressType']] type: Specifies if the IP is exposed to the public internet.
        :param pulumi.Input[str] dns_name_label: The Dns name label for the IP.
        :param pulumi.Input[str] ip: The IP exposed to the public internet.
        """
        pulumi.set(__self__, "ports", ports)
        pulumi.set(__self__, "type", type)
        if dns_name_label is not None:
            pulumi.set(__self__, "dns_name_label", dns_name_label)
        if ip is not None:
            pulumi.set(__self__, "ip", ip)

    @property
    @pulumi.getter
    def ports(self) -> pulumi.Input[Sequence[pulumi.Input['PortArgs']]]:
        """
        The list of ports exposed on the container group.
        """
        return pulumi.get(self, "ports")

    @ports.setter
    def ports(self, value: pulumi.Input[Sequence[pulumi.Input['PortArgs']]]):
        pulumi.set(self, "ports", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'ContainerGroupIpAddressType']]:
        """
        Specifies if the IP is exposed to the public internet.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'ContainerGroupIpAddressType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="dnsNameLabel")
    def dns_name_label(self) -> Optional[pulumi.Input[str]]:
        """
        The Dns name label for the IP.
        """
        return pulumi.get(self, "dns_name_label")

    @dns_name_label.setter
    def dns_name_label(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_name_label", value)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP exposed to the public internet.
        """
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)


@pulumi.input_type
class PortArgs:
    def __init__(__self__, *,
                 port: pulumi.Input[int],
                 protocol: Optional[pulumi.Input[Union[str, 'ContainerGroupNetworkProtocol']]] = None):
        """
        The port exposed on the container group.
        :param pulumi.Input[int] port: The port number.
        :param pulumi.Input[Union[str, 'ContainerGroupNetworkProtocol']] protocol: The protocol associated with the port.
        """
        pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port number.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[Union[str, 'ContainerGroupNetworkProtocol']]]:
        """
        The protocol associated with the port.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[Union[str, 'ContainerGroupNetworkProtocol']]]):
        pulumi.set(self, "protocol", value)


@pulumi.input_type
class ResourceLimitsArgs:
    def __init__(__self__, *,
                 cpu: Optional[pulumi.Input[float]] = None,
                 memory_in_gb: Optional[pulumi.Input[float]] = None):
        """
        The resource limits.
        :param pulumi.Input[float] cpu: The CPU limit of this container instance.
        :param pulumi.Input[float] memory_in_gb: The memory limit in GB of this container instance.
        """
        if cpu is not None:
            pulumi.set(__self__, "cpu", cpu)
        if memory_in_gb is not None:
            pulumi.set(__self__, "memory_in_gb", memory_in_gb)

    @property
    @pulumi.getter
    def cpu(self) -> Optional[pulumi.Input[float]]:
        """
        The CPU limit of this container instance.
        """
        return pulumi.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "cpu", value)

    @property
    @pulumi.getter(name="memoryInGB")
    def memory_in_gb(self) -> Optional[pulumi.Input[float]]:
        """
        The memory limit in GB of this container instance.
        """
        return pulumi.get(self, "memory_in_gb")

    @memory_in_gb.setter
    def memory_in_gb(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "memory_in_gb", value)


@pulumi.input_type
class ResourceRequestsArgs:
    def __init__(__self__, *,
                 cpu: pulumi.Input[float],
                 memory_in_gb: pulumi.Input[float]):
        """
        The resource requests.
        :param pulumi.Input[float] cpu: The CPU request of this container instance.
        :param pulumi.Input[float] memory_in_gb: The memory request in GB of this container instance.
        """
        pulumi.set(__self__, "cpu", cpu)
        pulumi.set(__self__, "memory_in_gb", memory_in_gb)

    @property
    @pulumi.getter
    def cpu(self) -> pulumi.Input[float]:
        """
        The CPU request of this container instance.
        """
        return pulumi.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: pulumi.Input[float]):
        pulumi.set(self, "cpu", value)

    @property
    @pulumi.getter(name="memoryInGB")
    def memory_in_gb(self) -> pulumi.Input[float]:
        """
        The memory request in GB of this container instance.
        """
        return pulumi.get(self, "memory_in_gb")

    @memory_in_gb.setter
    def memory_in_gb(self, value: pulumi.Input[float]):
        pulumi.set(self, "memory_in_gb", value)


@pulumi.input_type
class ResourceRequirementsArgs:
    def __init__(__self__, *,
                 requests: pulumi.Input['ResourceRequestsArgs'],
                 limits: Optional[pulumi.Input['ResourceLimitsArgs']] = None):
        """
        The resource requirements.
        :param pulumi.Input['ResourceRequestsArgs'] requests: The resource requests of this container instance.
        :param pulumi.Input['ResourceLimitsArgs'] limits: The resource limits of this container instance.
        """
        pulumi.set(__self__, "requests", requests)
        if limits is not None:
            pulumi.set(__self__, "limits", limits)

    @property
    @pulumi.getter
    def requests(self) -> pulumi.Input['ResourceRequestsArgs']:
        """
        The resource requests of this container instance.
        """
        return pulumi.get(self, "requests")

    @requests.setter
    def requests(self, value: pulumi.Input['ResourceRequestsArgs']):
        pulumi.set(self, "requests", value)

    @property
    @pulumi.getter
    def limits(self) -> Optional[pulumi.Input['ResourceLimitsArgs']]:
        """
        The resource limits of this container instance.
        """
        return pulumi.get(self, "limits")

    @limits.setter
    def limits(self, value: Optional[pulumi.Input['ResourceLimitsArgs']]):
        pulumi.set(self, "limits", value)


@pulumi.input_type
class VolumeMountArgs:
    def __init__(__self__, *,
                 mount_path: pulumi.Input[str],
                 name: pulumi.Input[str],
                 read_only: Optional[pulumi.Input[bool]] = None):
        """
        The properties of the volume mount.
        :param pulumi.Input[str] mount_path: The path within the container where the volume should be mounted. Must not contain colon (:).
        :param pulumi.Input[str] name: The name of the volume mount.
        :param pulumi.Input[bool] read_only: The flag indicating whether the volume mount is read-only.
        """
        pulumi.set(__self__, "mount_path", mount_path)
        pulumi.set(__self__, "name", name)
        if read_only is not None:
            pulumi.set(__self__, "read_only", read_only)

    @property
    @pulumi.getter(name="mountPath")
    def mount_path(self) -> pulumi.Input[str]:
        """
        The path within the container where the volume should be mounted. Must not contain colon (:).
        """
        return pulumi.get(self, "mount_path")

    @mount_path.setter
    def mount_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "mount_path", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the volume mount.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="readOnly")
    def read_only(self) -> Optional[pulumi.Input[bool]]:
        """
        The flag indicating whether the volume mount is read-only.
        """
        return pulumi.get(self, "read_only")

    @read_only.setter
    def read_only(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "read_only", value)


@pulumi.input_type
class VolumeArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 azure_file: Optional[pulumi.Input['AzureFileVolumeArgs']] = None,
                 empty_dir: Optional[Any] = None,
                 git_repo: Optional[pulumi.Input['GitRepoVolumeArgs']] = None,
                 secret: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The properties of the volume.
        :param pulumi.Input[str] name: The name of the volume.
        :param pulumi.Input['AzureFileVolumeArgs'] azure_file: The Azure File volume.
        :param Any empty_dir: The empty directory volume.
        :param pulumi.Input['GitRepoVolumeArgs'] git_repo: The git repo volume.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] secret: The secret volume.
        """
        pulumi.set(__self__, "name", name)
        if azure_file is not None:
            pulumi.set(__self__, "azure_file", azure_file)
        if empty_dir is not None:
            pulumi.set(__self__, "empty_dir", empty_dir)
        if git_repo is not None:
            pulumi.set(__self__, "git_repo", git_repo)
        if secret is not None:
            pulumi.set(__self__, "secret", secret)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the volume.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="azureFile")
    def azure_file(self) -> Optional[pulumi.Input['AzureFileVolumeArgs']]:
        """
        The Azure File volume.
        """
        return pulumi.get(self, "azure_file")

    @azure_file.setter
    def azure_file(self, value: Optional[pulumi.Input['AzureFileVolumeArgs']]):
        pulumi.set(self, "azure_file", value)

    @property
    @pulumi.getter(name="emptyDir")
    def empty_dir(self) -> Optional[Any]:
        """
        The empty directory volume.
        """
        return pulumi.get(self, "empty_dir")

    @empty_dir.setter
    def empty_dir(self, value: Optional[Any]):
        pulumi.set(self, "empty_dir", value)

    @property
    @pulumi.getter(name="gitRepo")
    def git_repo(self) -> Optional[pulumi.Input['GitRepoVolumeArgs']]:
        """
        The git repo volume.
        """
        return pulumi.get(self, "git_repo")

    @git_repo.setter
    def git_repo(self, value: Optional[pulumi.Input['GitRepoVolumeArgs']]):
        pulumi.set(self, "git_repo", value)

    @property
    @pulumi.getter
    def secret(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The secret volume.
        """
        return pulumi.get(self, "secret")

    @secret.setter
    def secret(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "secret", value)


