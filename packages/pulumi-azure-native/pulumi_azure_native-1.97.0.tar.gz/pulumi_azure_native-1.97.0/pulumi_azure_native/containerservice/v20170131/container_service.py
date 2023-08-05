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
from ._inputs import *

__all__ = ['ContainerServiceArgs', 'ContainerService']

@pulumi.input_type
class ContainerServiceArgs:
    def __init__(__self__, *,
                 agent_pool_profiles: pulumi.Input[Sequence[pulumi.Input['ContainerServiceAgentPoolProfileArgs']]],
                 linux_profile: pulumi.Input['ContainerServiceLinuxProfileArgs'],
                 master_profile: pulumi.Input['ContainerServiceMasterProfileArgs'],
                 resource_group_name: pulumi.Input[str],
                 container_service_name: Optional[pulumi.Input[str]] = None,
                 custom_profile: Optional[pulumi.Input['ContainerServiceCustomProfileArgs']] = None,
                 diagnostics_profile: Optional[pulumi.Input['ContainerServiceDiagnosticsProfileArgs']] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 orchestrator_profile: Optional[pulumi.Input['ContainerServiceOrchestratorProfileArgs']] = None,
                 service_principal_profile: Optional[pulumi.Input['ContainerServiceServicePrincipalProfileArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 windows_profile: Optional[pulumi.Input['ContainerServiceWindowsProfileArgs']] = None):
        """
        The set of arguments for constructing a ContainerService resource.
        :param pulumi.Input[Sequence[pulumi.Input['ContainerServiceAgentPoolProfileArgs']]] agent_pool_profiles: Properties of the agent pool.
        :param pulumi.Input['ContainerServiceLinuxProfileArgs'] linux_profile: Properties of Linux VMs.
        :param pulumi.Input['ContainerServiceMasterProfileArgs'] master_profile: Properties of master agents.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] container_service_name: The name of the container service in the specified subscription and resource group.
        :param pulumi.Input['ContainerServiceCustomProfileArgs'] custom_profile: Properties for custom clusters.
        :param pulumi.Input['ContainerServiceDiagnosticsProfileArgs'] diagnostics_profile: Properties of the diagnostic agent.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input['ContainerServiceOrchestratorProfileArgs'] orchestrator_profile: Properties of the orchestrator.
        :param pulumi.Input['ContainerServiceServicePrincipalProfileArgs'] service_principal_profile: Properties for cluster service principals.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input['ContainerServiceWindowsProfileArgs'] windows_profile: Properties of Windows VMs.
        """
        pulumi.set(__self__, "agent_pool_profiles", agent_pool_profiles)
        pulumi.set(__self__, "linux_profile", linux_profile)
        pulumi.set(__self__, "master_profile", master_profile)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if container_service_name is not None:
            pulumi.set(__self__, "container_service_name", container_service_name)
        if custom_profile is not None:
            pulumi.set(__self__, "custom_profile", custom_profile)
        if diagnostics_profile is not None:
            pulumi.set(__self__, "diagnostics_profile", diagnostics_profile)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if orchestrator_profile is not None:
            pulumi.set(__self__, "orchestrator_profile", orchestrator_profile)
        if service_principal_profile is not None:
            pulumi.set(__self__, "service_principal_profile", service_principal_profile)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if windows_profile is not None:
            pulumi.set(__self__, "windows_profile", windows_profile)

    @property
    @pulumi.getter(name="agentPoolProfiles")
    def agent_pool_profiles(self) -> pulumi.Input[Sequence[pulumi.Input['ContainerServiceAgentPoolProfileArgs']]]:
        """
        Properties of the agent pool.
        """
        return pulumi.get(self, "agent_pool_profiles")

    @agent_pool_profiles.setter
    def agent_pool_profiles(self, value: pulumi.Input[Sequence[pulumi.Input['ContainerServiceAgentPoolProfileArgs']]]):
        pulumi.set(self, "agent_pool_profiles", value)

    @property
    @pulumi.getter(name="linuxProfile")
    def linux_profile(self) -> pulumi.Input['ContainerServiceLinuxProfileArgs']:
        """
        Properties of Linux VMs.
        """
        return pulumi.get(self, "linux_profile")

    @linux_profile.setter
    def linux_profile(self, value: pulumi.Input['ContainerServiceLinuxProfileArgs']):
        pulumi.set(self, "linux_profile", value)

    @property
    @pulumi.getter(name="masterProfile")
    def master_profile(self) -> pulumi.Input['ContainerServiceMasterProfileArgs']:
        """
        Properties of master agents.
        """
        return pulumi.get(self, "master_profile")

    @master_profile.setter
    def master_profile(self, value: pulumi.Input['ContainerServiceMasterProfileArgs']):
        pulumi.set(self, "master_profile", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="containerServiceName")
    def container_service_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container service in the specified subscription and resource group.
        """
        return pulumi.get(self, "container_service_name")

    @container_service_name.setter
    def container_service_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "container_service_name", value)

    @property
    @pulumi.getter(name="customProfile")
    def custom_profile(self) -> Optional[pulumi.Input['ContainerServiceCustomProfileArgs']]:
        """
        Properties for custom clusters.
        """
        return pulumi.get(self, "custom_profile")

    @custom_profile.setter
    def custom_profile(self, value: Optional[pulumi.Input['ContainerServiceCustomProfileArgs']]):
        pulumi.set(self, "custom_profile", value)

    @property
    @pulumi.getter(name="diagnosticsProfile")
    def diagnostics_profile(self) -> Optional[pulumi.Input['ContainerServiceDiagnosticsProfileArgs']]:
        """
        Properties of the diagnostic agent.
        """
        return pulumi.get(self, "diagnostics_profile")

    @diagnostics_profile.setter
    def diagnostics_profile(self, value: Optional[pulumi.Input['ContainerServiceDiagnosticsProfileArgs']]):
        pulumi.set(self, "diagnostics_profile", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="orchestratorProfile")
    def orchestrator_profile(self) -> Optional[pulumi.Input['ContainerServiceOrchestratorProfileArgs']]:
        """
        Properties of the orchestrator.
        """
        return pulumi.get(self, "orchestrator_profile")

    @orchestrator_profile.setter
    def orchestrator_profile(self, value: Optional[pulumi.Input['ContainerServiceOrchestratorProfileArgs']]):
        pulumi.set(self, "orchestrator_profile", value)

    @property
    @pulumi.getter(name="servicePrincipalProfile")
    def service_principal_profile(self) -> Optional[pulumi.Input['ContainerServiceServicePrincipalProfileArgs']]:
        """
        Properties for cluster service principals.
        """
        return pulumi.get(self, "service_principal_profile")

    @service_principal_profile.setter
    def service_principal_profile(self, value: Optional[pulumi.Input['ContainerServiceServicePrincipalProfileArgs']]):
        pulumi.set(self, "service_principal_profile", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="windowsProfile")
    def windows_profile(self) -> Optional[pulumi.Input['ContainerServiceWindowsProfileArgs']]:
        """
        Properties of Windows VMs.
        """
        return pulumi.get(self, "windows_profile")

    @windows_profile.setter
    def windows_profile(self, value: Optional[pulumi.Input['ContainerServiceWindowsProfileArgs']]):
        pulumi.set(self, "windows_profile", value)


warnings.warn("""Version 2017-01-31 will be removed in v2 of the provider.""", DeprecationWarning)


class ContainerService(pulumi.CustomResource):
    warnings.warn("""Version 2017-01-31 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_pool_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceAgentPoolProfileArgs']]]]] = None,
                 container_service_name: Optional[pulumi.Input[str]] = None,
                 custom_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceCustomProfileArgs']]] = None,
                 diagnostics_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceDiagnosticsProfileArgs']]] = None,
                 linux_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceLinuxProfileArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 master_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceMasterProfileArgs']]] = None,
                 orchestrator_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceOrchestratorProfileArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_principal_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceServicePrincipalProfileArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 windows_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceWindowsProfileArgs']]] = None,
                 __props__=None):
        """
        Container service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceAgentPoolProfileArgs']]]] agent_pool_profiles: Properties of the agent pool.
        :param pulumi.Input[str] container_service_name: The name of the container service in the specified subscription and resource group.
        :param pulumi.Input[pulumi.InputType['ContainerServiceCustomProfileArgs']] custom_profile: Properties for custom clusters.
        :param pulumi.Input[pulumi.InputType['ContainerServiceDiagnosticsProfileArgs']] diagnostics_profile: Properties of the diagnostic agent.
        :param pulumi.Input[pulumi.InputType['ContainerServiceLinuxProfileArgs']] linux_profile: Properties of Linux VMs.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[pulumi.InputType['ContainerServiceMasterProfileArgs']] master_profile: Properties of master agents.
        :param pulumi.Input[pulumi.InputType['ContainerServiceOrchestratorProfileArgs']] orchestrator_profile: Properties of the orchestrator.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['ContainerServiceServicePrincipalProfileArgs']] service_principal_profile: Properties for cluster service principals.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[pulumi.InputType['ContainerServiceWindowsProfileArgs']] windows_profile: Properties of Windows VMs.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerServiceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Container service.

        :param str resource_name: The name of the resource.
        :param ContainerServiceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerServiceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_pool_profiles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerServiceAgentPoolProfileArgs']]]]] = None,
                 container_service_name: Optional[pulumi.Input[str]] = None,
                 custom_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceCustomProfileArgs']]] = None,
                 diagnostics_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceDiagnosticsProfileArgs']]] = None,
                 linux_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceLinuxProfileArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 master_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceMasterProfileArgs']]] = None,
                 orchestrator_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceOrchestratorProfileArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_principal_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceServicePrincipalProfileArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 windows_profile: Optional[pulumi.Input[pulumi.InputType['ContainerServiceWindowsProfileArgs']]] = None,
                 __props__=None):
        pulumi.log.warn("""ContainerService is deprecated: Version 2017-01-31 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContainerServiceArgs.__new__(ContainerServiceArgs)

            if agent_pool_profiles is None and not opts.urn:
                raise TypeError("Missing required property 'agent_pool_profiles'")
            __props__.__dict__["agent_pool_profiles"] = agent_pool_profiles
            __props__.__dict__["container_service_name"] = container_service_name
            __props__.__dict__["custom_profile"] = custom_profile
            __props__.__dict__["diagnostics_profile"] = diagnostics_profile
            if linux_profile is None and not opts.urn:
                raise TypeError("Missing required property 'linux_profile'")
            __props__.__dict__["linux_profile"] = linux_profile
            __props__.__dict__["location"] = location
            if master_profile is None and not opts.urn:
                raise TypeError("Missing required property 'master_profile'")
            __props__.__dict__["master_profile"] = master_profile
            __props__.__dict__["orchestrator_profile"] = orchestrator_profile
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["service_principal_profile"] = service_principal_profile
            __props__.__dict__["tags"] = tags
            __props__.__dict__["windows_profile"] = windows_profile
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:containerservice/v20151101preview:ContainerService"), pulumi.Alias(type_="azure-native:containerservice/v20160330:ContainerService"), pulumi.Alias(type_="azure-native:containerservice/v20160930:ContainerService")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ContainerService, __self__).__init__(
            'azure-native:containerservice/v20170131:ContainerService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ContainerService':
        """
        Get an existing ContainerService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ContainerServiceArgs.__new__(ContainerServiceArgs)

        __props__.__dict__["agent_pool_profiles"] = None
        __props__.__dict__["custom_profile"] = None
        __props__.__dict__["diagnostics_profile"] = None
        __props__.__dict__["linux_profile"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["master_profile"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["orchestrator_profile"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["service_principal_profile"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["windows_profile"] = None
        return ContainerService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentPoolProfiles")
    def agent_pool_profiles(self) -> pulumi.Output[Sequence['outputs.ContainerServiceAgentPoolProfileResponse']]:
        """
        Properties of the agent pool.
        """
        return pulumi.get(self, "agent_pool_profiles")

    @property
    @pulumi.getter(name="customProfile")
    def custom_profile(self) -> pulumi.Output[Optional['outputs.ContainerServiceCustomProfileResponse']]:
        """
        Properties for custom clusters.
        """
        return pulumi.get(self, "custom_profile")

    @property
    @pulumi.getter(name="diagnosticsProfile")
    def diagnostics_profile(self) -> pulumi.Output[Optional['outputs.ContainerServiceDiagnosticsProfileResponse']]:
        """
        Properties of the diagnostic agent.
        """
        return pulumi.get(self, "diagnostics_profile")

    @property
    @pulumi.getter(name="linuxProfile")
    def linux_profile(self) -> pulumi.Output['outputs.ContainerServiceLinuxProfileResponse']:
        """
        Properties of Linux VMs.
        """
        return pulumi.get(self, "linux_profile")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="masterProfile")
    def master_profile(self) -> pulumi.Output['outputs.ContainerServiceMasterProfileResponse']:
        """
        Properties of master agents.
        """
        return pulumi.get(self, "master_profile")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="orchestratorProfile")
    def orchestrator_profile(self) -> pulumi.Output[Optional['outputs.ContainerServiceOrchestratorProfileResponse']]:
        """
        Properties of the orchestrator.
        """
        return pulumi.get(self, "orchestrator_profile")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        the current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="servicePrincipalProfile")
    def service_principal_profile(self) -> pulumi.Output[Optional['outputs.ContainerServiceServicePrincipalProfileResponse']]:
        """
        Properties for cluster service principals.
        """
        return pulumi.get(self, "service_principal_profile")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="windowsProfile")
    def windows_profile(self) -> pulumi.Output[Optional['outputs.ContainerServiceWindowsProfileResponse']]:
        """
        Properties of Windows VMs.
        """
        return pulumi.get(self, "windows_profile")

