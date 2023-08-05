# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ContainerGroupIpAddressType',
    'ContainerGroupNetworkProtocol',
    'ContainerGroupRestartPolicy',
    'ContainerGroupSku',
    'ContainerNetworkProtocol',
    'DnsNameLabelReusePolicy',
    'GpuSku',
    'LogAnalyticsLogType',
    'OperatingSystemTypes',
    'ResourceIdentityType',
    'Scheme',
]


class ContainerGroupIpAddressType(str, Enum):
    """
    Specifies if the IP is exposed to the public internet or private VNET.
    """
    PUBLIC = "Public"
    PRIVATE = "Private"


class ContainerGroupNetworkProtocol(str, Enum):
    """
    The protocol associated with the port.
    """
    TCP = "TCP"
    UDP = "UDP"


class ContainerGroupRestartPolicy(str, Enum):
    """
    Restart policy for all containers within the container group. 
    - `Always` Always restart
    - `OnFailure` Restart on failure
    - `Never` Never restart
    """
    ALWAYS = "Always"
    ON_FAILURE = "OnFailure"
    NEVER = "Never"


class ContainerGroupSku(str, Enum):
    """
    The SKU for a container group.
    """
    STANDARD = "Standard"
    DEDICATED = "Dedicated"


class ContainerNetworkProtocol(str, Enum):
    """
    The protocol associated with the port.
    """
    TCP = "TCP"
    UDP = "UDP"


class DnsNameLabelReusePolicy(str, Enum):
    """
    The value representing the security enum. The 'Unsecure' value is the default value if not selected and means the object's domain name label is not secured against subdomain takeover. The 'TenantReuse' value is the default value if selected and means the object's domain name label can be reused within the same tenant. The 'SubscriptionReuse' value means the object's domain name label can be reused within the same subscription. The 'ResourceGroupReuse' value means the object's domain name label can be reused within the same resource group. The 'NoReuse' value means the object's domain name label cannot be reused within the same resource group, subscription, or tenant.
    """
    UNSECURE = "Unsecure"
    TENANT_REUSE = "TenantReuse"
    SUBSCRIPTION_REUSE = "SubscriptionReuse"
    RESOURCE_GROUP_REUSE = "ResourceGroupReuse"
    NOREUSE = "Noreuse"


class GpuSku(str, Enum):
    """
    The SKU of the GPU resource.
    """
    K80 = "K80"
    P100 = "P100"
    V100 = "V100"


class LogAnalyticsLogType(str, Enum):
    """
    The log type to be used.
    """
    CONTAINER_INSIGHTS = "ContainerInsights"
    CONTAINER_INSTANCE_LOGS = "ContainerInstanceLogs"


class OperatingSystemTypes(str, Enum):
    """
    The operating system type required by the containers in the container group.
    """
    WINDOWS = "Windows"
    LINUX = "Linux"


class ResourceIdentityType(str, Enum):
    """
    The type of identity used for the container group. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user assigned identities. The type 'None' will remove any identities from the container group.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"
    NONE = "None"


class Scheme(str, Enum):
    """
    The scheme.
    """
    HTTP = "http"
    HTTPS = "https"
