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
    'DnsConfigResponse',
    'EndpointResponse',
    'MonitorConfigResponse',
]

@pulumi.output_type
class DnsConfigResponse(dict):
    """
    Class containing DNS settings in a Traffic Manager profile.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "relativeName":
            suggest = "relative_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DnsConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DnsConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DnsConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 fqdn: str,
                 relative_name: Optional[str] = None,
                 ttl: Optional[float] = None):
        """
        Class containing DNS settings in a Traffic Manager profile.
        :param str fqdn: The fully-qualified domain name (FQDN) of the Traffic Manager profile. This is formed from the concatenation of the RelativeName with the DNS domain used by Azure Traffic Manager.
        :param str relative_name: The relative DNS name provided by this Traffic Manager profile. This value is combined with the DNS domain name used by Azure Traffic Manager to form the fully-qualified domain name (FQDN) of the profile.
        :param float ttl: The DNS Time-To-Live (TTL), in seconds. This informs the local DNS resolvers and DNS clients how long to cache DNS responses provided by this Traffic Manager profile.
        """
        pulumi.set(__self__, "fqdn", fqdn)
        if relative_name is not None:
            pulumi.set(__self__, "relative_name", relative_name)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)

    @property
    @pulumi.getter
    def fqdn(self) -> str:
        """
        The fully-qualified domain name (FQDN) of the Traffic Manager profile. This is formed from the concatenation of the RelativeName with the DNS domain used by Azure Traffic Manager.
        """
        return pulumi.get(self, "fqdn")

    @property
    @pulumi.getter(name="relativeName")
    def relative_name(self) -> Optional[str]:
        """
        The relative DNS name provided by this Traffic Manager profile. This value is combined with the DNS domain name used by Azure Traffic Manager to form the fully-qualified domain name (FQDN) of the profile.
        """
        return pulumi.get(self, "relative_name")

    @property
    @pulumi.getter
    def ttl(self) -> Optional[float]:
        """
        The DNS Time-To-Live (TTL), in seconds. This informs the local DNS resolvers and DNS clients how long to cache DNS responses provided by this Traffic Manager profile.
        """
        return pulumi.get(self, "ttl")


@pulumi.output_type
class EndpointResponse(dict):
    """
    Class representing a Traffic Manager endpoint.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "endpointLocation":
            suggest = "endpoint_location"
        elif key == "endpointMonitorStatus":
            suggest = "endpoint_monitor_status"
        elif key == "endpointStatus":
            suggest = "endpoint_status"
        elif key == "geoMapping":
            suggest = "geo_mapping"
        elif key == "minChildEndpoints":
            suggest = "min_child_endpoints"
        elif key == "targetResourceId":
            suggest = "target_resource_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EndpointResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EndpointResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EndpointResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 name: str,
                 type: str,
                 endpoint_location: Optional[str] = None,
                 endpoint_monitor_status: Optional[str] = None,
                 endpoint_status: Optional[str] = None,
                 geo_mapping: Optional[Sequence[str]] = None,
                 min_child_endpoints: Optional[float] = None,
                 priority: Optional[float] = None,
                 target: Optional[str] = None,
                 target_resource_id: Optional[str] = None,
                 weight: Optional[float] = None):
        """
        Class representing a Traffic Manager endpoint.
        :param str id: Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}
        :param str name: The name of the resource
        :param str type: The type of the resource. Ex- Microsoft.Network/trafficManagerProfiles.
        :param str endpoint_location: Specifies the location of the external or nested endpoints when using the ‘Performance’ traffic routing method.
        :param str endpoint_monitor_status: The monitoring status of the endpoint.
        :param str endpoint_status: The status of the endpoint. If the endpoint is Enabled, it is probed for endpoint health and is included in the traffic routing method.
        :param Sequence[str] geo_mapping: The list of countries/regions mapped to this endpoint when using the ‘Geographic’ traffic routing method. Please consult Traffic Manager Geographic documentation for a full list of accepted values.
        :param float min_child_endpoints: The minimum number of endpoints that must be available in the child profile in order for the parent profile to be considered available. Only applicable to endpoint of type 'NestedEndpoints'.
        :param float priority: The priority of this endpoint when using the ‘Priority’ traffic routing method. Possible values are from 1 to 1000, lower values represent higher priority. This is an optional parameter.  If specified, it must be specified on all endpoints, and no two endpoints can share the same priority value.
        :param str target: The fully-qualified DNS name of the endpoint. Traffic Manager returns this value in DNS responses to direct traffic to this endpoint.
        :param str target_resource_id: The Azure Resource URI of the of the endpoint. Not applicable to endpoints of type 'ExternalEndpoints'.
        :param float weight: The weight of this endpoint when using the 'Weighted' traffic routing method. Possible values are from 1 to 1000.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if endpoint_location is not None:
            pulumi.set(__self__, "endpoint_location", endpoint_location)
        if endpoint_monitor_status is not None:
            pulumi.set(__self__, "endpoint_monitor_status", endpoint_monitor_status)
        if endpoint_status is not None:
            pulumi.set(__self__, "endpoint_status", endpoint_status)
        if geo_mapping is not None:
            pulumi.set(__self__, "geo_mapping", geo_mapping)
        if min_child_endpoints is not None:
            pulumi.set(__self__, "min_child_endpoints", min_child_endpoints)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if target_resource_id is not None:
            pulumi.set(__self__, "target_resource_id", target_resource_id)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/trafficManagerProfiles/{resourceName}
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
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Network/trafficManagerProfiles.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="endpointLocation")
    def endpoint_location(self) -> Optional[str]:
        """
        Specifies the location of the external or nested endpoints when using the ‘Performance’ traffic routing method.
        """
        return pulumi.get(self, "endpoint_location")

    @property
    @pulumi.getter(name="endpointMonitorStatus")
    def endpoint_monitor_status(self) -> Optional[str]:
        """
        The monitoring status of the endpoint.
        """
        return pulumi.get(self, "endpoint_monitor_status")

    @property
    @pulumi.getter(name="endpointStatus")
    def endpoint_status(self) -> Optional[str]:
        """
        The status of the endpoint. If the endpoint is Enabled, it is probed for endpoint health and is included in the traffic routing method.
        """
        return pulumi.get(self, "endpoint_status")

    @property
    @pulumi.getter(name="geoMapping")
    def geo_mapping(self) -> Optional[Sequence[str]]:
        """
        The list of countries/regions mapped to this endpoint when using the ‘Geographic’ traffic routing method. Please consult Traffic Manager Geographic documentation for a full list of accepted values.
        """
        return pulumi.get(self, "geo_mapping")

    @property
    @pulumi.getter(name="minChildEndpoints")
    def min_child_endpoints(self) -> Optional[float]:
        """
        The minimum number of endpoints that must be available in the child profile in order for the parent profile to be considered available. Only applicable to endpoint of type 'NestedEndpoints'.
        """
        return pulumi.get(self, "min_child_endpoints")

    @property
    @pulumi.getter
    def priority(self) -> Optional[float]:
        """
        The priority of this endpoint when using the ‘Priority’ traffic routing method. Possible values are from 1 to 1000, lower values represent higher priority. This is an optional parameter.  If specified, it must be specified on all endpoints, and no two endpoints can share the same priority value.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def target(self) -> Optional[str]:
        """
        The fully-qualified DNS name of the endpoint. Traffic Manager returns this value in DNS responses to direct traffic to this endpoint.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter(name="targetResourceId")
    def target_resource_id(self) -> Optional[str]:
        """
        The Azure Resource URI of the of the endpoint. Not applicable to endpoints of type 'ExternalEndpoints'.
        """
        return pulumi.get(self, "target_resource_id")

    @property
    @pulumi.getter
    def weight(self) -> Optional[float]:
        """
        The weight of this endpoint when using the 'Weighted' traffic routing method. Possible values are from 1 to 1000.
        """
        return pulumi.get(self, "weight")


@pulumi.output_type
class MonitorConfigResponse(dict):
    """
    Class containing endpoint monitoring settings in a Traffic Manager profile.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "intervalInSeconds":
            suggest = "interval_in_seconds"
        elif key == "profileMonitorStatus":
            suggest = "profile_monitor_status"
        elif key == "timeoutInSeconds":
            suggest = "timeout_in_seconds"
        elif key == "toleratedNumberOfFailures":
            suggest = "tolerated_number_of_failures"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorConfigResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorConfigResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorConfigResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 interval_in_seconds: Optional[float] = None,
                 path: Optional[str] = None,
                 port: Optional[float] = None,
                 profile_monitor_status: Optional[str] = None,
                 protocol: Optional[str] = None,
                 timeout_in_seconds: Optional[float] = None,
                 tolerated_number_of_failures: Optional[float] = None):
        """
        Class containing endpoint monitoring settings in a Traffic Manager profile.
        :param float interval_in_seconds: The monitor interval for endpoints in this profile. This is the interval at which Traffic Manager will check the health of each endpoint in this profile.
        :param str path: The path relative to the endpoint domain name used to probe for endpoint health.
        :param float port: The TCP port used to probe for endpoint health.
        :param str profile_monitor_status: The profile-level monitoring status of the Traffic Manager profile.
        :param str protocol: The protocol (HTTP, HTTPS or TCP) used to probe for endpoint health.
        :param float timeout_in_seconds: The monitor timeout for endpoints in this profile. This is the time that Traffic Manager allows endpoints in this profile to response to the health check.
        :param float tolerated_number_of_failures: The number of consecutive failed health check that Traffic Manager tolerates before declaring an endpoint in this profile Degraded after the next failed health check.
        """
        if interval_in_seconds is not None:
            pulumi.set(__self__, "interval_in_seconds", interval_in_seconds)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if profile_monitor_status is not None:
            pulumi.set(__self__, "profile_monitor_status", profile_monitor_status)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if timeout_in_seconds is not None:
            pulumi.set(__self__, "timeout_in_seconds", timeout_in_seconds)
        if tolerated_number_of_failures is not None:
            pulumi.set(__self__, "tolerated_number_of_failures", tolerated_number_of_failures)

    @property
    @pulumi.getter(name="intervalInSeconds")
    def interval_in_seconds(self) -> Optional[float]:
        """
        The monitor interval for endpoints in this profile. This is the interval at which Traffic Manager will check the health of each endpoint in this profile.
        """
        return pulumi.get(self, "interval_in_seconds")

    @property
    @pulumi.getter
    def path(self) -> Optional[str]:
        """
        The path relative to the endpoint domain name used to probe for endpoint health.
        """
        return pulumi.get(self, "path")

    @property
    @pulumi.getter
    def port(self) -> Optional[float]:
        """
        The TCP port used to probe for endpoint health.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="profileMonitorStatus")
    def profile_monitor_status(self) -> Optional[str]:
        """
        The profile-level monitoring status of the Traffic Manager profile.
        """
        return pulumi.get(self, "profile_monitor_status")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        """
        The protocol (HTTP, HTTPS or TCP) used to probe for endpoint health.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="timeoutInSeconds")
    def timeout_in_seconds(self) -> Optional[float]:
        """
        The monitor timeout for endpoints in this profile. This is the time that Traffic Manager allows endpoints in this profile to response to the health check.
        """
        return pulumi.get(self, "timeout_in_seconds")

    @property
    @pulumi.getter(name="toleratedNumberOfFailures")
    def tolerated_number_of_failures(self) -> Optional[float]:
        """
        The number of consecutive failed health check that Traffic Manager tolerates before declaring an endpoint in this profile Degraded after the next failed health check.
        """
        return pulumi.get(self, "tolerated_number_of_failures")


