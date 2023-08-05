# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'APIServerProfileArgs',
    'ClusterProfileArgs',
    'ConsoleProfileArgs',
    'IngressProfileArgs',
    'MasterProfileArgs',
    'NetworkProfileArgs',
    'ServicePrincipalProfileArgs',
    'WorkerProfileArgs',
]

@pulumi.input_type
class APIServerProfileArgs:
    def __init__(__self__, *,
                 ip: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 visibility: Optional[pulumi.Input[str]] = None):
        """
        APIServerProfile represents an API server profile.
        :param pulumi.Input[str] ip: The IP of the cluster API server (immutable).
        :param pulumi.Input[str] url: The URL to access the cluster API server (immutable).
        :param pulumi.Input[str] visibility: API server visibility (immutable).
        """
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if visibility is not None:
            pulumi.set(__self__, "visibility", visibility)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP of the cluster API server (immutable).
        """
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL to access the cluster API server (immutable).
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def visibility(self) -> Optional[pulumi.Input[str]]:
        """
        API server visibility (immutable).
        """
        return pulumi.get(self, "visibility")

    @visibility.setter
    def visibility(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "visibility", value)


@pulumi.input_type
class ClusterProfileArgs:
    def __init__(__self__, *,
                 domain: Optional[pulumi.Input[str]] = None,
                 pull_secret: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        ClusterProfile represents a cluster profile.
        :param pulumi.Input[str] domain: The domain for the cluster (immutable).
        :param pulumi.Input[str] pull_secret: The pull secret for the cluster (immutable).
        :param pulumi.Input[str] resource_group_id: The ID of the cluster resource group (immutable).
        :param pulumi.Input[str] version: The version of the cluster (immutable).
        """
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if pull_secret is not None:
            pulumi.set(__self__, "pull_secret", pull_secret)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The domain for the cluster (immutable).
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="pullSecret")
    def pull_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The pull secret for the cluster (immutable).
        """
        return pulumi.get(self, "pull_secret")

    @pull_secret.setter
    def pull_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pull_secret", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the cluster resource group (immutable).
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the cluster (immutable).
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class ConsoleProfileArgs:
    def __init__(__self__, *,
                 url: Optional[pulumi.Input[str]] = None):
        """
        ConsoleProfile represents a console profile.
        :param pulumi.Input[str] url: The URL to access the cluster console (immutable).
        """
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The URL to access the cluster console (immutable).
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


@pulumi.input_type
class IngressProfileArgs:
    def __init__(__self__, *,
                 ip: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 visibility: Optional[pulumi.Input[str]] = None):
        """
        IngressProfile represents an ingress profile.
        :param pulumi.Input[str] ip: The IP of the ingress (immutable).
        :param pulumi.Input[str] name: The ingress profile name.  Must be "default" (immutable).
        :param pulumi.Input[str] visibility: Ingress visibility (immutable).
        """
        if ip is not None:
            pulumi.set(__self__, "ip", ip)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if visibility is not None:
            pulumi.set(__self__, "visibility", visibility)

    @property
    @pulumi.getter
    def ip(self) -> Optional[pulumi.Input[str]]:
        """
        The IP of the ingress (immutable).
        """
        return pulumi.get(self, "ip")

    @ip.setter
    def ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The ingress profile name.  Must be "default" (immutable).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def visibility(self) -> Optional[pulumi.Input[str]]:
        """
        Ingress visibility (immutable).
        """
        return pulumi.get(self, "visibility")

    @visibility.setter
    def visibility(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "visibility", value)


@pulumi.input_type
class MasterProfileArgs:
    def __init__(__self__, *,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 vm_size: Optional[pulumi.Input[str]] = None):
        """
        MasterProfile represents a master profile.
        :param pulumi.Input[str] subnet_id: The Azure resource ID of the master subnet (immutable).
        :param pulumi.Input[str] vm_size: The size of the master VMs (immutable).
        """
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if vm_size is not None:
            pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure resource ID of the master subnet (immutable).
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> Optional[pulumi.Input[str]]:
        """
        The size of the master VMs (immutable).
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vm_size", value)


@pulumi.input_type
class NetworkProfileArgs:
    def __init__(__self__, *,
                 pod_cidr: Optional[pulumi.Input[str]] = None,
                 service_cidr: Optional[pulumi.Input[str]] = None):
        """
        NetworkProfile represents a network profile.
        :param pulumi.Input[str] pod_cidr: The CIDR used for OpenShift/Kubernetes Pods (immutable).
        :param pulumi.Input[str] service_cidr: The CIDR used for OpenShift/Kubernetes Services (immutable).
        """
        if pod_cidr is not None:
            pulumi.set(__self__, "pod_cidr", pod_cidr)
        if service_cidr is not None:
            pulumi.set(__self__, "service_cidr", service_cidr)

    @property
    @pulumi.getter(name="podCidr")
    def pod_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR used for OpenShift/Kubernetes Pods (immutable).
        """
        return pulumi.get(self, "pod_cidr")

    @pod_cidr.setter
    def pod_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pod_cidr", value)

    @property
    @pulumi.getter(name="serviceCidr")
    def service_cidr(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR used for OpenShift/Kubernetes Services (immutable).
        """
        return pulumi.get(self, "service_cidr")

    @service_cidr.setter
    def service_cidr(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_cidr", value)


@pulumi.input_type
class ServicePrincipalProfileArgs:
    def __init__(__self__, *,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None):
        """
        ServicePrincipalProfile represents a service principal profile.
        :param pulumi.Input[str] client_id: The client ID used for the cluster (immutable).
        :param pulumi.Input[str] client_secret: The client secret used for the cluster (immutable).
        """
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The client ID used for the cluster (immutable).
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The client secret used for the cluster (immutable).
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)


@pulumi.input_type
class WorkerProfileArgs:
    def __init__(__self__, *,
                 count: Optional[pulumi.Input[int]] = None,
                 disk_size_gb: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 vm_size: Optional[pulumi.Input[str]] = None):
        """
        WorkerProfile represents a worker profile.
        :param pulumi.Input[int] count: The number of worker VMs.  Must be between 3 and 20 (immutable).
        :param pulumi.Input[int] disk_size_gb: The disk size of the worker VMs.  Must be 128 or greater (immutable).
        :param pulumi.Input[str] name: The worker profile name.  Must be "worker" (immutable).
        :param pulumi.Input[str] subnet_id: The Azure resource ID of the worker subnet (immutable).
        :param pulumi.Input[str] vm_size: The size of the worker VMs (immutable).
        """
        if count is not None:
            pulumi.set(__self__, "count", count)
        if disk_size_gb is not None:
            pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if vm_size is not None:
            pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter
    def count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of worker VMs.  Must be between 3 and 20 (immutable).
        """
        return pulumi.get(self, "count")

    @count.setter
    def count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "count", value)

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> Optional[pulumi.Input[int]]:
        """
        The disk size of the worker VMs.  Must be 128 or greater (immutable).
        """
        return pulumi.get(self, "disk_size_gb")

    @disk_size_gb.setter
    def disk_size_gb(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "disk_size_gb", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The worker profile name.  Must be "worker" (immutable).
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure resource ID of the worker subnet (immutable).
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> Optional[pulumi.Input[str]]:
        """
        The size of the worker VMs (immutable).
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vm_size", value)


