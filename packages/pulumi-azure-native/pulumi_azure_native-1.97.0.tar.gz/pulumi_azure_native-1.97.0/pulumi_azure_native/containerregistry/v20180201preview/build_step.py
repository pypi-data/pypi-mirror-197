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

__all__ = ['BuildStepArgs', 'BuildStep']

@pulumi.input_type
class BuildStepArgs:
    def __init__(__self__, *,
                 build_task_name: pulumi.Input[str],
                 registry_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 step_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BuildStep resource.
        :param pulumi.Input[str] build_task_name: The name of the container registry build task.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[str] step_name: The name of a build step for a container registry build task.
        """
        pulumi.set(__self__, "build_task_name", build_task_name)
        pulumi.set(__self__, "registry_name", registry_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if step_name is not None:
            pulumi.set(__self__, "step_name", step_name)

    @property
    @pulumi.getter(name="buildTaskName")
    def build_task_name(self) -> pulumi.Input[str]:
        """
        The name of the container registry build task.
        """
        return pulumi.get(self, "build_task_name")

    @build_task_name.setter
    def build_task_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "build_task_name", value)

    @property
    @pulumi.getter(name="registryName")
    def registry_name(self) -> pulumi.Input[str]:
        """
        The name of the container registry.
        """
        return pulumi.get(self, "registry_name")

    @registry_name.setter
    def registry_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "registry_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group to which the container registry belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="stepName")
    def step_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of a build step for a container registry build task.
        """
        return pulumi.get(self, "step_name")

    @step_name.setter
    def step_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "step_name", value)


class BuildStep(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 build_task_name: Optional[pulumi.Input[str]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 step_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Build step resource properties

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] build_task_name: The name of the container registry build task.
        :param pulumi.Input[str] registry_name: The name of the container registry.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the container registry belongs.
        :param pulumi.Input[str] step_name: The name of a build step for a container registry build task.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BuildStepArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Build step resource properties

        :param str resource_name: The name of the resource.
        :param BuildStepArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BuildStepArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 build_task_name: Optional[pulumi.Input[str]] = None,
                 registry_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 step_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BuildStepArgs.__new__(BuildStepArgs)

            if build_task_name is None and not opts.urn:
                raise TypeError("Missing required property 'build_task_name'")
            __props__.__dict__["build_task_name"] = build_task_name
            if registry_name is None and not opts.urn:
                raise TypeError("Missing required property 'registry_name'")
            __props__.__dict__["registry_name"] = registry_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["step_name"] = step_name
            __props__.__dict__["name"] = None
            __props__.__dict__["properties"] = None
            __props__.__dict__["type"] = None
        super(BuildStep, __self__).__init__(
            'azure-native:containerregistry/v20180201preview:BuildStep',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BuildStep':
        """
        Get an existing BuildStep resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BuildStepArgs.__new__(BuildStepArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return BuildStep(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.DockerBuildStepResponse']:
        """
        The properties of a build step.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

