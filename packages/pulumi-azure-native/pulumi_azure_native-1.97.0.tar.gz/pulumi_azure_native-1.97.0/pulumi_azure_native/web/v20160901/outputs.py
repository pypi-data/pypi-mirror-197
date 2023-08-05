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
    'CapabilityResponse',
    'HostingEnvironmentProfileResponse',
    'NameValuePairResponse',
    'NetworkAccessControlEntryResponse',
    'SkuCapacityResponse',
    'SkuDescriptionResponse',
    'StampCapacityResponse',
    'VirtualIPMappingResponse',
    'VirtualNetworkProfileResponse',
    'WorkerPoolResponse',
]

@pulumi.output_type
class CapabilityResponse(dict):
    """
    Describes the capabilities/features allowed for a specific SKU.
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 reason: Optional[str] = None,
                 value: Optional[str] = None):
        """
        Describes the capabilities/features allowed for a specific SKU.
        :param str name: Name of the SKU capability.
        :param str reason: Reason of the SKU capability.
        :param str value: Value of the SKU capability.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reason is not None:
            pulumi.set(__self__, "reason", reason)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the SKU capability.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        """
        Reason of the SKU capability.
        """
        return pulumi.get(self, "reason")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Value of the SKU capability.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class HostingEnvironmentProfileResponse(dict):
    """
    Specification for an App Service Environment to use for this resource.
    """
    def __init__(__self__, *,
                 name: str,
                 type: str,
                 id: Optional[str] = None):
        """
        Specification for an App Service Environment to use for this resource.
        :param str name: Name of the App Service Environment.
        :param str type: Resource type of the App Service Environment.
        :param str id: Resource ID of the App Service Environment.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the App Service Environment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type of the App Service Environment.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID of the App Service Environment.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class NameValuePairResponse(dict):
    """
    Name value pair.
    """
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 value: Optional[str] = None):
        """
        Name value pair.
        :param str name: Pair name.
        :param str value: Pair value.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Pair name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        Pair value.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class NetworkAccessControlEntryResponse(dict):
    """
    Network access control entry.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "remoteSubnet":
            suggest = "remote_subnet"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in NetworkAccessControlEntryResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        NetworkAccessControlEntryResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        NetworkAccessControlEntryResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 action: Optional[str] = None,
                 description: Optional[str] = None,
                 order: Optional[int] = None,
                 remote_subnet: Optional[str] = None):
        """
        Network access control entry.
        :param str action: Action object.
        :param str description: Description of network access control entry.
        :param int order: Order of precedence.
        :param str remote_subnet: Remote subnet.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if order is not None:
            pulumi.set(__self__, "order", order)
        if remote_subnet is not None:
            pulumi.set(__self__, "remote_subnet", remote_subnet)

    @property
    @pulumi.getter
    def action(self) -> Optional[str]:
        """
        Action object.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of network access control entry.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def order(self) -> Optional[int]:
        """
        Order of precedence.
        """
        return pulumi.get(self, "order")

    @property
    @pulumi.getter(name="remoteSubnet")
    def remote_subnet(self) -> Optional[str]:
        """
        Remote subnet.
        """
        return pulumi.get(self, "remote_subnet")


@pulumi.output_type
class SkuCapacityResponse(dict):
    """
    Description of the App Service plan scale options.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "scaleType":
            suggest = "scale_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SkuCapacityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SkuCapacityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SkuCapacityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 default: Optional[int] = None,
                 maximum: Optional[int] = None,
                 minimum: Optional[int] = None,
                 scale_type: Optional[str] = None):
        """
        Description of the App Service plan scale options.
        :param int default: Default number of workers for this App Service plan SKU.
        :param int maximum: Maximum number of workers for this App Service plan SKU.
        :param int minimum: Minimum number of workers for this App Service plan SKU.
        :param str scale_type: Available scale configurations for an App Service plan.
        """
        if default is not None:
            pulumi.set(__self__, "default", default)
        if maximum is not None:
            pulumi.set(__self__, "maximum", maximum)
        if minimum is not None:
            pulumi.set(__self__, "minimum", minimum)
        if scale_type is not None:
            pulumi.set(__self__, "scale_type", scale_type)

    @property
    @pulumi.getter
    def default(self) -> Optional[int]:
        """
        Default number of workers for this App Service plan SKU.
        """
        return pulumi.get(self, "default")

    @property
    @pulumi.getter
    def maximum(self) -> Optional[int]:
        """
        Maximum number of workers for this App Service plan SKU.
        """
        return pulumi.get(self, "maximum")

    @property
    @pulumi.getter
    def minimum(self) -> Optional[int]:
        """
        Minimum number of workers for this App Service plan SKU.
        """
        return pulumi.get(self, "minimum")

    @property
    @pulumi.getter(name="scaleType")
    def scale_type(self) -> Optional[str]:
        """
        Available scale configurations for an App Service plan.
        """
        return pulumi.get(self, "scale_type")


@pulumi.output_type
class SkuDescriptionResponse(dict):
    """
    Description of a SKU for a scalable resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "skuCapacity":
            suggest = "sku_capacity"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SkuDescriptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SkuDescriptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SkuDescriptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 capabilities: Optional[Sequence['outputs.CapabilityResponse']] = None,
                 capacity: Optional[int] = None,
                 family: Optional[str] = None,
                 locations: Optional[Sequence[str]] = None,
                 name: Optional[str] = None,
                 size: Optional[str] = None,
                 sku_capacity: Optional['outputs.SkuCapacityResponse'] = None,
                 tier: Optional[str] = None):
        """
        Description of a SKU for a scalable resource.
        :param Sequence['CapabilityResponse'] capabilities: Capabilities of the SKU, e.g., is traffic manager enabled?
        :param int capacity: Current number of instances assigned to the resource.
        :param str family: Family code of the resource SKU.
        :param Sequence[str] locations: Locations of the SKU.
        :param str name: Name of the resource SKU.
        :param str size: Size specifier of the resource SKU.
        :param 'SkuCapacityResponse' sku_capacity: Min, max, and default scale values of the SKU.
        :param str tier: Service tier of the resource SKU.
        """
        if capabilities is not None:
            pulumi.set(__self__, "capabilities", capabilities)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if locations is not None:
            pulumi.set(__self__, "locations", locations)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if sku_capacity is not None:
            pulumi.set(__self__, "sku_capacity", sku_capacity)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def capabilities(self) -> Optional[Sequence['outputs.CapabilityResponse']]:
        """
        Capabilities of the SKU, e.g., is traffic manager enabled?
        """
        return pulumi.get(self, "capabilities")

    @property
    @pulumi.getter
    def capacity(self) -> Optional[int]:
        """
        Current number of instances assigned to the resource.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter
    def family(self) -> Optional[str]:
        """
        Family code of the resource SKU.
        """
        return pulumi.get(self, "family")

    @property
    @pulumi.getter
    def locations(self) -> Optional[Sequence[str]]:
        """
        Locations of the SKU.
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the resource SKU.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def size(self) -> Optional[str]:
        """
        Size specifier of the resource SKU.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="skuCapacity")
    def sku_capacity(self) -> Optional['outputs.SkuCapacityResponse']:
        """
        Min, max, and default scale values of the SKU.
        """
        return pulumi.get(self, "sku_capacity")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        Service tier of the resource SKU.
        """
        return pulumi.get(self, "tier")


@pulumi.output_type
class StampCapacityResponse(dict):
    """
    Stamp capacity information.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "availableCapacity":
            suggest = "available_capacity"
        elif key == "computeMode":
            suggest = "compute_mode"
        elif key == "excludeFromCapacityAllocation":
            suggest = "exclude_from_capacity_allocation"
        elif key == "isApplicableForAllComputeModes":
            suggest = "is_applicable_for_all_compute_modes"
        elif key == "siteMode":
            suggest = "site_mode"
        elif key == "totalCapacity":
            suggest = "total_capacity"
        elif key == "workerSize":
            suggest = "worker_size"
        elif key == "workerSizeId":
            suggest = "worker_size_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in StampCapacityResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        StampCapacityResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        StampCapacityResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 available_capacity: Optional[float] = None,
                 compute_mode: Optional[str] = None,
                 exclude_from_capacity_allocation: Optional[bool] = None,
                 is_applicable_for_all_compute_modes: Optional[bool] = None,
                 name: Optional[str] = None,
                 site_mode: Optional[str] = None,
                 total_capacity: Optional[float] = None,
                 unit: Optional[str] = None,
                 worker_size: Optional[str] = None,
                 worker_size_id: Optional[int] = None):
        """
        Stamp capacity information.
        :param float available_capacity: Available capacity (# of machines, bytes of storage etc...).
        :param str compute_mode: Shared/dedicated workers.
        :param bool exclude_from_capacity_allocation: If <code>true</code>, it includes basic apps.
               Basic apps are not used for capacity allocation.
        :param bool is_applicable_for_all_compute_modes: <code>true</code> if capacity is applicable for all apps; otherwise, <code>false</code>.
        :param str name: Name of the stamp.
        :param str site_mode: Shared or Dedicated.
        :param float total_capacity: Total capacity (# of machines, bytes of storage etc...).
        :param str unit: Name of the unit.
        :param str worker_size: Size of the machines.
        :param int worker_size_id: Size ID of machines: 
               0 - Small
               1 - Medium
               2 - Large
        """
        if available_capacity is not None:
            pulumi.set(__self__, "available_capacity", available_capacity)
        if compute_mode is not None:
            pulumi.set(__self__, "compute_mode", compute_mode)
        if exclude_from_capacity_allocation is not None:
            pulumi.set(__self__, "exclude_from_capacity_allocation", exclude_from_capacity_allocation)
        if is_applicable_for_all_compute_modes is not None:
            pulumi.set(__self__, "is_applicable_for_all_compute_modes", is_applicable_for_all_compute_modes)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if site_mode is not None:
            pulumi.set(__self__, "site_mode", site_mode)
        if total_capacity is not None:
            pulumi.set(__self__, "total_capacity", total_capacity)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)
        if worker_size is not None:
            pulumi.set(__self__, "worker_size", worker_size)
        if worker_size_id is not None:
            pulumi.set(__self__, "worker_size_id", worker_size_id)

    @property
    @pulumi.getter(name="availableCapacity")
    def available_capacity(self) -> Optional[float]:
        """
        Available capacity (# of machines, bytes of storage etc...).
        """
        return pulumi.get(self, "available_capacity")

    @property
    @pulumi.getter(name="computeMode")
    def compute_mode(self) -> Optional[str]:
        """
        Shared/dedicated workers.
        """
        return pulumi.get(self, "compute_mode")

    @property
    @pulumi.getter(name="excludeFromCapacityAllocation")
    def exclude_from_capacity_allocation(self) -> Optional[bool]:
        """
        If <code>true</code>, it includes basic apps.
        Basic apps are not used for capacity allocation.
        """
        return pulumi.get(self, "exclude_from_capacity_allocation")

    @property
    @pulumi.getter(name="isApplicableForAllComputeModes")
    def is_applicable_for_all_compute_modes(self) -> Optional[bool]:
        """
        <code>true</code> if capacity is applicable for all apps; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "is_applicable_for_all_compute_modes")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of the stamp.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="siteMode")
    def site_mode(self) -> Optional[str]:
        """
        Shared or Dedicated.
        """
        return pulumi.get(self, "site_mode")

    @property
    @pulumi.getter(name="totalCapacity")
    def total_capacity(self) -> Optional[float]:
        """
        Total capacity (# of machines, bytes of storage etc...).
        """
        return pulumi.get(self, "total_capacity")

    @property
    @pulumi.getter
    def unit(self) -> Optional[str]:
        """
        Name of the unit.
        """
        return pulumi.get(self, "unit")

    @property
    @pulumi.getter(name="workerSize")
    def worker_size(self) -> Optional[str]:
        """
        Size of the machines.
        """
        return pulumi.get(self, "worker_size")

    @property
    @pulumi.getter(name="workerSizeId")
    def worker_size_id(self) -> Optional[int]:
        """
        Size ID of machines: 
        0 - Small
        1 - Medium
        2 - Large
        """
        return pulumi.get(self, "worker_size_id")


@pulumi.output_type
class VirtualIPMappingResponse(dict):
    """
    Virtual IP mapping.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "inUse":
            suggest = "in_use"
        elif key == "internalHttpPort":
            suggest = "internal_http_port"
        elif key == "internalHttpsPort":
            suggest = "internal_https_port"
        elif key == "virtualIP":
            suggest = "virtual_ip"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VirtualIPMappingResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VirtualIPMappingResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VirtualIPMappingResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 in_use: Optional[bool] = None,
                 internal_http_port: Optional[int] = None,
                 internal_https_port: Optional[int] = None,
                 virtual_ip: Optional[str] = None):
        """
        Virtual IP mapping.
        :param bool in_use: Is virtual IP mapping in use.
        :param int internal_http_port: Internal HTTP port.
        :param int internal_https_port: Internal HTTPS port.
        :param str virtual_ip: Virtual IP address.
        """
        if in_use is not None:
            pulumi.set(__self__, "in_use", in_use)
        if internal_http_port is not None:
            pulumi.set(__self__, "internal_http_port", internal_http_port)
        if internal_https_port is not None:
            pulumi.set(__self__, "internal_https_port", internal_https_port)
        if virtual_ip is not None:
            pulumi.set(__self__, "virtual_ip", virtual_ip)

    @property
    @pulumi.getter(name="inUse")
    def in_use(self) -> Optional[bool]:
        """
        Is virtual IP mapping in use.
        """
        return pulumi.get(self, "in_use")

    @property
    @pulumi.getter(name="internalHttpPort")
    def internal_http_port(self) -> Optional[int]:
        """
        Internal HTTP port.
        """
        return pulumi.get(self, "internal_http_port")

    @property
    @pulumi.getter(name="internalHttpsPort")
    def internal_https_port(self) -> Optional[int]:
        """
        Internal HTTPS port.
        """
        return pulumi.get(self, "internal_https_port")

    @property
    @pulumi.getter(name="virtualIP")
    def virtual_ip(self) -> Optional[str]:
        """
        Virtual IP address.
        """
        return pulumi.get(self, "virtual_ip")


@pulumi.output_type
class VirtualNetworkProfileResponse(dict):
    """
    Specification for using a Virtual Network.
    """
    def __init__(__self__, *,
                 name: str,
                 type: str,
                 id: Optional[str] = None,
                 subnet: Optional[str] = None):
        """
        Specification for using a Virtual Network.
        :param str name: Name of the Virtual Network (read-only).
        :param str type: Resource type of the Virtual Network (read-only).
        :param str id: Resource id of the Virtual Network.
        :param str subnet: Subnet within the Virtual Network.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Virtual Network (read-only).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type of the Virtual Network (read-only).
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource id of the Virtual Network.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def subnet(self) -> Optional[str]:
        """
        Subnet within the Virtual Network.
        """
        return pulumi.get(self, "subnet")


@pulumi.output_type
class WorkerPoolResponse(dict):
    """
    Worker pool of an App Service Environment.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "instanceNames":
            suggest = "instance_names"
        elif key == "computeMode":
            suggest = "compute_mode"
        elif key == "workerCount":
            suggest = "worker_count"
        elif key == "workerSize":
            suggest = "worker_size"
        elif key == "workerSizeId":
            suggest = "worker_size_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkerPoolResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkerPoolResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkerPoolResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 instance_names: Sequence[str],
                 compute_mode: Optional[str] = None,
                 worker_count: Optional[int] = None,
                 worker_size: Optional[str] = None,
                 worker_size_id: Optional[int] = None):
        """
        Worker pool of an App Service Environment.
        :param Sequence[str] instance_names: Names of all instances in the worker pool (read only).
        :param str compute_mode: Shared or dedicated app hosting.
        :param int worker_count: Number of instances in the worker pool.
        :param str worker_size: VM size of the worker pool instances.
        :param int worker_size_id: Worker size ID for referencing this worker pool.
        """
        pulumi.set(__self__, "instance_names", instance_names)
        if compute_mode is not None:
            pulumi.set(__self__, "compute_mode", compute_mode)
        if worker_count is not None:
            pulumi.set(__self__, "worker_count", worker_count)
        if worker_size is not None:
            pulumi.set(__self__, "worker_size", worker_size)
        if worker_size_id is not None:
            pulumi.set(__self__, "worker_size_id", worker_size_id)

    @property
    @pulumi.getter(name="instanceNames")
    def instance_names(self) -> Sequence[str]:
        """
        Names of all instances in the worker pool (read only).
        """
        return pulumi.get(self, "instance_names")

    @property
    @pulumi.getter(name="computeMode")
    def compute_mode(self) -> Optional[str]:
        """
        Shared or dedicated app hosting.
        """
        return pulumi.get(self, "compute_mode")

    @property
    @pulumi.getter(name="workerCount")
    def worker_count(self) -> Optional[int]:
        """
        Number of instances in the worker pool.
        """
        return pulumi.get(self, "worker_count")

    @property
    @pulumi.getter(name="workerSize")
    def worker_size(self) -> Optional[str]:
        """
        VM size of the worker pool instances.
        """
        return pulumi.get(self, "worker_size")

    @property
    @pulumi.getter(name="workerSizeId")
    def worker_size_id(self) -> Optional[int]:
        """
        Worker size ID for referencing this worker pool.
        """
        return pulumi.get(self, "worker_size_id")


