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
    'GetManagedEnvironmentResult',
    'AwaitableGetManagedEnvironmentResult',
    'get_managed_environment',
    'get_managed_environment_output',
]

@pulumi.output_type
class GetManagedEnvironmentResult:
    """
    An environment for hosting container apps
    """
    def __init__(__self__, app_logs_configuration=None, dapr_ai_connection_string=None, dapr_ai_instrumentation_key=None, default_domain=None, deployment_errors=None, id=None, location=None, name=None, provisioning_state=None, static_ip=None, system_data=None, tags=None, type=None, vnet_configuration=None, zone_redundant=None):
        if app_logs_configuration and not isinstance(app_logs_configuration, dict):
            raise TypeError("Expected argument 'app_logs_configuration' to be a dict")
        pulumi.set(__self__, "app_logs_configuration", app_logs_configuration)
        if dapr_ai_connection_string and not isinstance(dapr_ai_connection_string, str):
            raise TypeError("Expected argument 'dapr_ai_connection_string' to be a str")
        pulumi.set(__self__, "dapr_ai_connection_string", dapr_ai_connection_string)
        if dapr_ai_instrumentation_key and not isinstance(dapr_ai_instrumentation_key, str):
            raise TypeError("Expected argument 'dapr_ai_instrumentation_key' to be a str")
        pulumi.set(__self__, "dapr_ai_instrumentation_key", dapr_ai_instrumentation_key)
        if default_domain and not isinstance(default_domain, str):
            raise TypeError("Expected argument 'default_domain' to be a str")
        pulumi.set(__self__, "default_domain", default_domain)
        if deployment_errors and not isinstance(deployment_errors, str):
            raise TypeError("Expected argument 'deployment_errors' to be a str")
        pulumi.set(__self__, "deployment_errors", deployment_errors)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if static_ip and not isinstance(static_ip, str):
            raise TypeError("Expected argument 'static_ip' to be a str")
        pulumi.set(__self__, "static_ip", static_ip)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vnet_configuration and not isinstance(vnet_configuration, dict):
            raise TypeError("Expected argument 'vnet_configuration' to be a dict")
        pulumi.set(__self__, "vnet_configuration", vnet_configuration)
        if zone_redundant and not isinstance(zone_redundant, bool):
            raise TypeError("Expected argument 'zone_redundant' to be a bool")
        pulumi.set(__self__, "zone_redundant", zone_redundant)

    @property
    @pulumi.getter(name="appLogsConfiguration")
    def app_logs_configuration(self) -> Optional['outputs.AppLogsConfigurationResponse']:
        """
        Cluster configuration which enables the log daemon to export
        app logs to a destination. Currently only "log-analytics" is
        supported
        """
        return pulumi.get(self, "app_logs_configuration")

    @property
    @pulumi.getter(name="daprAIConnectionString")
    def dapr_ai_connection_string(self) -> Optional[str]:
        """
        Application Insights connection string used by Dapr to export Service to Service communication telemetry
        """
        return pulumi.get(self, "dapr_ai_connection_string")

    @property
    @pulumi.getter(name="daprAIInstrumentationKey")
    def dapr_ai_instrumentation_key(self) -> Optional[str]:
        """
        Azure Monitor instrumentation key used by Dapr to export Service to Service communication telemetry
        """
        return pulumi.get(self, "dapr_ai_instrumentation_key")

    @property
    @pulumi.getter(name="defaultDomain")
    def default_domain(self) -> str:
        """
        Default Domain Name for the cluster
        """
        return pulumi.get(self, "default_domain")

    @property
    @pulumi.getter(name="deploymentErrors")
    def deployment_errors(self) -> str:
        """
        Any errors that occurred during deployment or deployment validation
        """
        return pulumi.get(self, "deployment_errors")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

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
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Environment.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="staticIp")
    def static_ip(self) -> str:
        """
        Static IP of the Environment
        """
        return pulumi.get(self, "static_ip")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
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

    @property
    @pulumi.getter(name="vnetConfiguration")
    def vnet_configuration(self) -> Optional['outputs.VnetConfigurationResponse']:
        """
        Vnet configuration for the environment
        """
        return pulumi.get(self, "vnet_configuration")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> Optional[bool]:
        """
        Whether or not this Managed Environment is zone-redundant.
        """
        return pulumi.get(self, "zone_redundant")


class AwaitableGetManagedEnvironmentResult(GetManagedEnvironmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetManagedEnvironmentResult(
            app_logs_configuration=self.app_logs_configuration,
            dapr_ai_connection_string=self.dapr_ai_connection_string,
            dapr_ai_instrumentation_key=self.dapr_ai_instrumentation_key,
            default_domain=self.default_domain,
            deployment_errors=self.deployment_errors,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            static_ip=self.static_ip,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            vnet_configuration=self.vnet_configuration,
            zone_redundant=self.zone_redundant)


def get_managed_environment(environment_name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetManagedEnvironmentResult:
    """
    Get the properties of a Managed Environment used to host container apps.
    API Version: 2022-03-01.


    :param str environment_name: Name of the Environment.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['environmentName'] = environment_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:app:getManagedEnvironment', __args__, opts=opts, typ=GetManagedEnvironmentResult).value

    return AwaitableGetManagedEnvironmentResult(
        app_logs_configuration=__ret__.app_logs_configuration,
        dapr_ai_connection_string=__ret__.dapr_ai_connection_string,
        dapr_ai_instrumentation_key=__ret__.dapr_ai_instrumentation_key,
        default_domain=__ret__.default_domain,
        deployment_errors=__ret__.deployment_errors,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        static_ip=__ret__.static_ip,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        vnet_configuration=__ret__.vnet_configuration,
        zone_redundant=__ret__.zone_redundant)


@_utilities.lift_output_func(get_managed_environment)
def get_managed_environment_output(environment_name: Optional[pulumi.Input[str]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetManagedEnvironmentResult]:
    """
    Get the properties of a Managed Environment used to host container apps.
    API Version: 2022-03-01.


    :param str environment_name: Name of the Environment.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
