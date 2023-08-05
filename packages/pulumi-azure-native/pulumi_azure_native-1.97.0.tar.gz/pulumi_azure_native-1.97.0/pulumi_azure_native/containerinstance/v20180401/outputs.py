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
from ._enums import *

__all__ = [
    'AzureFileVolumeResponse',
    'ContainerGroupResponseInstanceView',
    'ContainerPortResponse',
    'ContainerPropertiesResponseInstanceView',
    'ContainerResponse',
    'ContainerStateResponse',
    'EnvironmentVariableResponse',
    'EventResponse',
    'GitRepoVolumeResponse',
    'ImageRegistryCredentialResponse',
    'IpAddressResponse',
    'PortResponse',
    'ResourceLimitsResponse',
    'ResourceRequestsResponse',
    'ResourceRequirementsResponse',
    'VolumeMountResponse',
    'VolumeResponse',
]

@pulumi.output_type
class AzureFileVolumeResponse(dict):
    """
    The properties of the Azure File volume. Azure File shares are mounted as volumes.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "shareName":
            suggest = "share_name"
        elif key == "storageAccountName":
            suggest = "storage_account_name"
        elif key == "readOnly":
            suggest = "read_only"
        elif key == "storageAccountKey":
            suggest = "storage_account_key"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AzureFileVolumeResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AzureFileVolumeResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AzureFileVolumeResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 share_name: str,
                 storage_account_name: str,
                 read_only: Optional[bool] = None,
                 storage_account_key: Optional[str] = None):
        """
        The properties of the Azure File volume. Azure File shares are mounted as volumes.
        :param str share_name: The name of the Azure File share to be mounted as a volume.
        :param str storage_account_name: The name of the storage account that contains the Azure File share.
        :param bool read_only: The flag indicating whether the Azure File shared mounted as a volume is read-only.
        :param str storage_account_key: The storage account access key used to access the Azure File share.
        """
        pulumi.set(__self__, "share_name", share_name)
        pulumi.set(__self__, "storage_account_name", storage_account_name)
        if read_only is not None:
            pulumi.set(__self__, "read_only", read_only)
        if storage_account_key is not None:
            pulumi.set(__self__, "storage_account_key", storage_account_key)

    @property
    @pulumi.getter(name="shareName")
    def share_name(self) -> str:
        """
        The name of the Azure File share to be mounted as a volume.
        """
        return pulumi.get(self, "share_name")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> str:
        """
        The name of the storage account that contains the Azure File share.
        """
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="readOnly")
    def read_only(self) -> Optional[bool]:
        """
        The flag indicating whether the Azure File shared mounted as a volume is read-only.
        """
        return pulumi.get(self, "read_only")

    @property
    @pulumi.getter(name="storageAccountKey")
    def storage_account_key(self) -> Optional[str]:
        """
        The storage account access key used to access the Azure File share.
        """
        return pulumi.get(self, "storage_account_key")


@pulumi.output_type
class ContainerGroupResponseInstanceView(dict):
    """
    The instance view of the container group. Only valid in response.
    """
    def __init__(__self__, *,
                 events: Sequence['outputs.EventResponse'],
                 state: str):
        """
        The instance view of the container group. Only valid in response.
        :param Sequence['EventResponse'] events: The events of this container group.
        :param str state: The state of the container group. Only valid in response.
        """
        pulumi.set(__self__, "events", events)
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def events(self) -> Sequence['outputs.EventResponse']:
        """
        The events of this container group.
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the container group. Only valid in response.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class ContainerPortResponse(dict):
    """
    The port exposed on the container instance.
    """
    def __init__(__self__, *,
                 port: int,
                 protocol: Optional[str] = None):
        """
        The port exposed on the container instance.
        :param int port: The port number exposed within the container group.
        :param str protocol: The protocol associated with the port.
        """
        pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port number exposed within the container group.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        """
        The protocol associated with the port.
        """
        return pulumi.get(self, "protocol")


@pulumi.output_type
class ContainerPropertiesResponseInstanceView(dict):
    """
    The instance view of the container instance. Only valid in response.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "currentState":
            suggest = "current_state"
        elif key == "previousState":
            suggest = "previous_state"
        elif key == "restartCount":
            suggest = "restart_count"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerPropertiesResponseInstanceView. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerPropertiesResponseInstanceView.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerPropertiesResponseInstanceView.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 current_state: 'outputs.ContainerStateResponse',
                 events: Sequence['outputs.EventResponse'],
                 previous_state: 'outputs.ContainerStateResponse',
                 restart_count: int):
        """
        The instance view of the container instance. Only valid in response.
        :param 'ContainerStateResponse' current_state: Current container instance state.
        :param Sequence['EventResponse'] events: The events of the container instance.
        :param 'ContainerStateResponse' previous_state: Previous container instance state.
        :param int restart_count: The number of times that the container instance has been restarted.
        """
        pulumi.set(__self__, "current_state", current_state)
        pulumi.set(__self__, "events", events)
        pulumi.set(__self__, "previous_state", previous_state)
        pulumi.set(__self__, "restart_count", restart_count)

    @property
    @pulumi.getter(name="currentState")
    def current_state(self) -> 'outputs.ContainerStateResponse':
        """
        Current container instance state.
        """
        return pulumi.get(self, "current_state")

    @property
    @pulumi.getter
    def events(self) -> Sequence['outputs.EventResponse']:
        """
        The events of the container instance.
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter(name="previousState")
    def previous_state(self) -> 'outputs.ContainerStateResponse':
        """
        Previous container instance state.
        """
        return pulumi.get(self, "previous_state")

    @property
    @pulumi.getter(name="restartCount")
    def restart_count(self) -> int:
        """
        The number of times that the container instance has been restarted.
        """
        return pulumi.get(self, "restart_count")


@pulumi.output_type
class ContainerResponse(dict):
    """
    A container instance.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "instanceView":
            suggest = "instance_view"
        elif key == "environmentVariables":
            suggest = "environment_variables"
        elif key == "volumeMounts":
            suggest = "volume_mounts"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 image: str,
                 instance_view: 'outputs.ContainerPropertiesResponseInstanceView',
                 name: str,
                 resources: 'outputs.ResourceRequirementsResponse',
                 command: Optional[Sequence[str]] = None,
                 environment_variables: Optional[Sequence['outputs.EnvironmentVariableResponse']] = None,
                 ports: Optional[Sequence['outputs.ContainerPortResponse']] = None,
                 volume_mounts: Optional[Sequence['outputs.VolumeMountResponse']] = None):
        """
        A container instance.
        :param str image: The name of the image used to create the container instance.
        :param 'ContainerPropertiesResponseInstanceView' instance_view: The instance view of the container instance. Only valid in response.
        :param str name: The user-provided name of the container instance.
        :param 'ResourceRequirementsResponse' resources: The resource requirements of the container instance.
        :param Sequence[str] command: The commands to execute within the container instance in exec form.
        :param Sequence['EnvironmentVariableResponse'] environment_variables: The environment variables to set in the container instance.
        :param Sequence['ContainerPortResponse'] ports: The exposed ports on the container instance.
        :param Sequence['VolumeMountResponse'] volume_mounts: The volume mounts available to the container instance.
        """
        pulumi.set(__self__, "image", image)
        pulumi.set(__self__, "instance_view", instance_view)
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
    def image(self) -> str:
        """
        The name of the image used to create the container instance.
        """
        return pulumi.get(self, "image")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> 'outputs.ContainerPropertiesResponseInstanceView':
        """
        The instance view of the container instance. Only valid in response.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The user-provided name of the container instance.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def resources(self) -> 'outputs.ResourceRequirementsResponse':
        """
        The resource requirements of the container instance.
        """
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter
    def command(self) -> Optional[Sequence[str]]:
        """
        The commands to execute within the container instance in exec form.
        """
        return pulumi.get(self, "command")

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[Sequence['outputs.EnvironmentVariableResponse']]:
        """
        The environment variables to set in the container instance.
        """
        return pulumi.get(self, "environment_variables")

    @property
    @pulumi.getter
    def ports(self) -> Optional[Sequence['outputs.ContainerPortResponse']]:
        """
        The exposed ports on the container instance.
        """
        return pulumi.get(self, "ports")

    @property
    @pulumi.getter(name="volumeMounts")
    def volume_mounts(self) -> Optional[Sequence['outputs.VolumeMountResponse']]:
        """
        The volume mounts available to the container instance.
        """
        return pulumi.get(self, "volume_mounts")


@pulumi.output_type
class ContainerStateResponse(dict):
    """
    The container instance state.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "detailStatus":
            suggest = "detail_status"
        elif key == "exitCode":
            suggest = "exit_code"
        elif key == "finishTime":
            suggest = "finish_time"
        elif key == "startTime":
            suggest = "start_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerStateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerStateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerStateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 detail_status: str,
                 exit_code: int,
                 finish_time: str,
                 start_time: str,
                 state: str):
        """
        The container instance state.
        :param str detail_status: The human-readable status of the container instance state.
        :param int exit_code: The container instance exit codes correspond to those from the `docker run` command.
        :param str finish_time: The date-time when the container instance state finished.
        :param str start_time: The date-time when the container instance state started.
        :param str state: The state of the container instance.
        """
        pulumi.set(__self__, "detail_status", detail_status)
        pulumi.set(__self__, "exit_code", exit_code)
        pulumi.set(__self__, "finish_time", finish_time)
        pulumi.set(__self__, "start_time", start_time)
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter(name="detailStatus")
    def detail_status(self) -> str:
        """
        The human-readable status of the container instance state.
        """
        return pulumi.get(self, "detail_status")

    @property
    @pulumi.getter(name="exitCode")
    def exit_code(self) -> int:
        """
        The container instance exit codes correspond to those from the `docker run` command.
        """
        return pulumi.get(self, "exit_code")

    @property
    @pulumi.getter(name="finishTime")
    def finish_time(self) -> str:
        """
        The date-time when the container instance state finished.
        """
        return pulumi.get(self, "finish_time")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> str:
        """
        The date-time when the container instance state started.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the container instance.
        """
        return pulumi.get(self, "state")


@pulumi.output_type
class EnvironmentVariableResponse(dict):
    """
    The environment variable to set within the container instance.
    """
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        The environment variable to set within the container instance.
        :param str name: The name of the environment variable.
        :param str value: The value of the environment variable.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the environment variable.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the environment variable.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class EventResponse(dict):
    """
    A container group or container instance event.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "firstTimestamp":
            suggest = "first_timestamp"
        elif key == "lastTimestamp":
            suggest = "last_timestamp"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EventResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EventResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EventResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 count: int,
                 first_timestamp: str,
                 last_timestamp: str,
                 message: str,
                 name: str,
                 type: str):
        """
        A container group or container instance event.
        :param int count: The count of the event.
        :param str first_timestamp: The date-time of the earliest logged event.
        :param str last_timestamp: The date-time of the latest logged event.
        :param str message: The event message.
        :param str name: The event name.
        :param str type: The event type.
        """
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "first_timestamp", first_timestamp)
        pulumi.set(__self__, "last_timestamp", last_timestamp)
        pulumi.set(__self__, "message", message)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        The count of the event.
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter(name="firstTimestamp")
    def first_timestamp(self) -> str:
        """
        The date-time of the earliest logged event.
        """
        return pulumi.get(self, "first_timestamp")

    @property
    @pulumi.getter(name="lastTimestamp")
    def last_timestamp(self) -> str:
        """
        The date-time of the latest logged event.
        """
        return pulumi.get(self, "last_timestamp")

    @property
    @pulumi.getter
    def message(self) -> str:
        """
        The event message.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The event name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The event type.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class GitRepoVolumeResponse(dict):
    """
    Represents a volume that is populated with the contents of a git repository
    """
    def __init__(__self__, *,
                 repository: str,
                 directory: Optional[str] = None,
                 revision: Optional[str] = None):
        """
        Represents a volume that is populated with the contents of a git repository
        :param str repository: Repository URL
        :param str directory: Target directory name. Must not contain or start with '..'.  If '.' is supplied, the volume directory will be the git repository.  Otherwise, if specified, the volume will contain the git repository in the subdirectory with the given name.
        :param str revision: Commit hash for the specified revision.
        """
        pulumi.set(__self__, "repository", repository)
        if directory is not None:
            pulumi.set(__self__, "directory", directory)
        if revision is not None:
            pulumi.set(__self__, "revision", revision)

    @property
    @pulumi.getter
    def repository(self) -> str:
        """
        Repository URL
        """
        return pulumi.get(self, "repository")

    @property
    @pulumi.getter
    def directory(self) -> Optional[str]:
        """
        Target directory name. Must not contain or start with '..'.  If '.' is supplied, the volume directory will be the git repository.  Otherwise, if specified, the volume will contain the git repository in the subdirectory with the given name.
        """
        return pulumi.get(self, "directory")

    @property
    @pulumi.getter
    def revision(self) -> Optional[str]:
        """
        Commit hash for the specified revision.
        """
        return pulumi.get(self, "revision")


@pulumi.output_type
class ImageRegistryCredentialResponse(dict):
    """
    Image registry credential.
    """
    def __init__(__self__, *,
                 server: str,
                 username: str,
                 password: Optional[str] = None):
        """
        Image registry credential.
        :param str server: The Docker image registry server without a protocol such as "http" and "https".
        :param str username: The username for the private registry.
        :param str password: The password for the private registry.
        """
        pulumi.set(__self__, "server", server)
        pulumi.set(__self__, "username", username)
        if password is not None:
            pulumi.set(__self__, "password", password)

    @property
    @pulumi.getter
    def server(self) -> str:
        """
        The Docker image registry server without a protocol such as "http" and "https".
        """
        return pulumi.get(self, "server")

    @property
    @pulumi.getter
    def username(self) -> str:
        """
        The username for the private registry.
        """
        return pulumi.get(self, "username")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        The password for the private registry.
        """
        return pulumi.get(self, "password")


@pulumi.output_type
class IpAddressResponse(dict):
    """
    IP address for the container group.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dnsNameLabel":
            suggest = "dns_name_label"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IpAddressResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IpAddressResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IpAddressResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 fqdn: str,
                 ports: Sequence['outputs.PortResponse'],
                 type: str,
                 dns_name_label: Optional[str] = None,
                 ip: Optional[str] = None):
        """
        IP address for the container group.
        :param str fqdn: The FQDN for the IP.
        :param Sequence['PortResponse'] ports: The list of ports exposed on the container group.
        :param str type: Specifies if the IP is exposed to the public internet.
        :param str dns_name_label: The Dns name label for the IP.
        :param str ip: The IP exposed to the public internet.
        """
        pulumi.set(__self__, "fqdn", fqdn)
        pulumi.set(__self__, "ports", ports)
        pulumi.set(__self__, "type", type)
        if dns_name_label is not None:
            pulumi.set(__self__, "dns_name_label", dns_name_label)
        if ip is not None:
            pulumi.set(__self__, "ip", ip)

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        The FQDN for the IP.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter
    def ports(self) -> Sequence['outputs.PortResponse']:
        """
        The list of ports exposed on the container group.
        """
        return pulumi.get(self, "ports")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies if the IP is exposed to the public internet.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="dnsNameLabel")
    def dns_name_label(self) -> Optional[str]:
        """
        The Dns name label for the IP.
        """
        return pulumi.get(self, "dns_name_label")

    @property
    @pulumi.getter
    def ip(self) -> Optional[str]:
        """
        The IP exposed to the public internet.
        """
        return pulumi.get(self, "ip")


@pulumi.output_type
class PortResponse(dict):
    """
    The port exposed on the container group.
    """
    def __init__(__self__, *,
                 port: int,
                 protocol: Optional[str] = None):
        """
        The port exposed on the container group.
        :param int port: The port number.
        :param str protocol: The protocol associated with the port.
        """
        pulumi.set(__self__, "port", port)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)

    @property
    @pulumi.getter
    def port(self) -> int:
        """
        The port number.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        """
        The protocol associated with the port.
        """
        return pulumi.get(self, "protocol")


@pulumi.output_type
class ResourceLimitsResponse(dict):
    """
    The resource limits.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "memoryInGB":
            suggest = "memory_in_gb"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResourceLimitsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceLimitsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceLimitsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cpu: Optional[float] = None,
                 memory_in_gb: Optional[float] = None):
        """
        The resource limits.
        :param float cpu: The CPU limit of this container instance.
        :param float memory_in_gb: The memory limit in GB of this container instance.
        """
        if cpu is not None:
            pulumi.set(__self__, "cpu", cpu)
        if memory_in_gb is not None:
            pulumi.set(__self__, "memory_in_gb", memory_in_gb)

    @property
    @pulumi.getter
    def cpu(self) -> Optional[float]:
        """
        The CPU limit of this container instance.
        """
        return pulumi.get(self, "cpu")

    @property
    @pulumi.getter(name="memoryInGB")
    def memory_in_gb(self) -> Optional[float]:
        """
        The memory limit in GB of this container instance.
        """
        return pulumi.get(self, "memory_in_gb")


@pulumi.output_type
class ResourceRequestsResponse(dict):
    """
    The resource requests.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "memoryInGB":
            suggest = "memory_in_gb"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ResourceRequestsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ResourceRequestsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ResourceRequestsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cpu: float,
                 memory_in_gb: float):
        """
        The resource requests.
        :param float cpu: The CPU request of this container instance.
        :param float memory_in_gb: The memory request in GB of this container instance.
        """
        pulumi.set(__self__, "cpu", cpu)
        pulumi.set(__self__, "memory_in_gb", memory_in_gb)

    @property
    @pulumi.getter
    def cpu(self) -> float:
        """
        The CPU request of this container instance.
        """
        return pulumi.get(self, "cpu")

    @property
    @pulumi.getter(name="memoryInGB")
    def memory_in_gb(self) -> float:
        """
        The memory request in GB of this container instance.
        """
        return pulumi.get(self, "memory_in_gb")


@pulumi.output_type
class ResourceRequirementsResponse(dict):
    """
    The resource requirements.
    """
    def __init__(__self__, *,
                 requests: 'outputs.ResourceRequestsResponse',
                 limits: Optional['outputs.ResourceLimitsResponse'] = None):
        """
        The resource requirements.
        :param 'ResourceRequestsResponse' requests: The resource requests of this container instance.
        :param 'ResourceLimitsResponse' limits: The resource limits of this container instance.
        """
        pulumi.set(__self__, "requests", requests)
        if limits is not None:
            pulumi.set(__self__, "limits", limits)

    @property
    @pulumi.getter
    def requests(self) -> 'outputs.ResourceRequestsResponse':
        """
        The resource requests of this container instance.
        """
        return pulumi.get(self, "requests")

    @property
    @pulumi.getter
    def limits(self) -> Optional['outputs.ResourceLimitsResponse']:
        """
        The resource limits of this container instance.
        """
        return pulumi.get(self, "limits")


@pulumi.output_type
class VolumeMountResponse(dict):
    """
    The properties of the volume mount.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "mountPath":
            suggest = "mount_path"
        elif key == "readOnly":
            suggest = "read_only"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VolumeMountResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VolumeMountResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VolumeMountResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 mount_path: str,
                 name: str,
                 read_only: Optional[bool] = None):
        """
        The properties of the volume mount.
        :param str mount_path: The path within the container where the volume should be mounted. Must not contain colon (:).
        :param str name: The name of the volume mount.
        :param bool read_only: The flag indicating whether the volume mount is read-only.
        """
        pulumi.set(__self__, "mount_path", mount_path)
        pulumi.set(__self__, "name", name)
        if read_only is not None:
            pulumi.set(__self__, "read_only", read_only)

    @property
    @pulumi.getter(name="mountPath")
    def mount_path(self) -> str:
        """
        The path within the container where the volume should be mounted. Must not contain colon (:).
        """
        return pulumi.get(self, "mount_path")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the volume mount.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="readOnly")
    def read_only(self) -> Optional[bool]:
        """
        The flag indicating whether the volume mount is read-only.
        """
        return pulumi.get(self, "read_only")


@pulumi.output_type
class VolumeResponse(dict):
    """
    The properties of the volume.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "azureFile":
            suggest = "azure_file"
        elif key == "emptyDir":
            suggest = "empty_dir"
        elif key == "gitRepo":
            suggest = "git_repo"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VolumeResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VolumeResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VolumeResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 azure_file: Optional['outputs.AzureFileVolumeResponse'] = None,
                 empty_dir: Optional[Any] = None,
                 git_repo: Optional['outputs.GitRepoVolumeResponse'] = None,
                 secret: Optional[Mapping[str, str]] = None):
        """
        The properties of the volume.
        :param str name: The name of the volume.
        :param 'AzureFileVolumeResponse' azure_file: The Azure File volume.
        :param Any empty_dir: The empty directory volume.
        :param 'GitRepoVolumeResponse' git_repo: The git repo volume.
        :param Mapping[str, str] secret: The secret volume.
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
    def name(self) -> str:
        """
        The name of the volume.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="azureFile")
    def azure_file(self) -> Optional['outputs.AzureFileVolumeResponse']:
        """
        The Azure File volume.
        """
        return pulumi.get(self, "azure_file")

    @property
    @pulumi.getter(name="emptyDir")
    def empty_dir(self) -> Optional[Any]:
        """
        The empty directory volume.
        """
        return pulumi.get(self, "empty_dir")

    @property
    @pulumi.getter(name="gitRepo")
    def git_repo(self) -> Optional['outputs.GitRepoVolumeResponse']:
        """
        The git repo volume.
        """
        return pulumi.get(self, "git_repo")

    @property
    @pulumi.getter
    def secret(self) -> Optional[Mapping[str, str]]:
        """
        The secret volume.
        """
        return pulumi.get(self, "secret")


