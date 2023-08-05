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
    'GetJobStepResult',
    'AwaitableGetJobStepResult',
    'get_job_step',
    'get_job_step_output',
]

@pulumi.output_type
class GetJobStepResult:
    """
    A job step.
    """
    def __init__(__self__, action=None, credential=None, execution_options=None, id=None, name=None, output=None, step_id=None, target_group=None, type=None):
        if action and not isinstance(action, dict):
            raise TypeError("Expected argument 'action' to be a dict")
        pulumi.set(__self__, "action", action)
        if credential and not isinstance(credential, str):
            raise TypeError("Expected argument 'credential' to be a str")
        pulumi.set(__self__, "credential", credential)
        if execution_options and not isinstance(execution_options, dict):
            raise TypeError("Expected argument 'execution_options' to be a dict")
        pulumi.set(__self__, "execution_options", execution_options)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if output and not isinstance(output, dict):
            raise TypeError("Expected argument 'output' to be a dict")
        pulumi.set(__self__, "output", output)
        if step_id and not isinstance(step_id, int):
            raise TypeError("Expected argument 'step_id' to be a int")
        pulumi.set(__self__, "step_id", step_id)
        if target_group and not isinstance(target_group, str):
            raise TypeError("Expected argument 'target_group' to be a str")
        pulumi.set(__self__, "target_group", target_group)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def action(self) -> 'outputs.JobStepActionResponse':
        """
        The action payload of the job step.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def credential(self) -> str:
        """
        The resource ID of the job credential that will be used to connect to the targets.
        """
        return pulumi.get(self, "credential")

    @property
    @pulumi.getter(name="executionOptions")
    def execution_options(self) -> Optional['outputs.JobStepExecutionOptionsResponse']:
        """
        Execution options for the job step.
        """
        return pulumi.get(self, "execution_options")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def output(self) -> Optional['outputs.JobStepOutputResponse']:
        """
        Output destination properties of the job step.
        """
        return pulumi.get(self, "output")

    @property
    @pulumi.getter(name="stepId")
    def step_id(self) -> Optional[int]:
        """
        The job step's index within the job. If not specified when creating the job step, it will be created as the last step. If not specified when updating the job step, the step id is not modified.
        """
        return pulumi.get(self, "step_id")

    @property
    @pulumi.getter(name="targetGroup")
    def target_group(self) -> str:
        """
        The resource ID of the target group that the job step will be executed on.
        """
        return pulumi.get(self, "target_group")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetJobStepResult(GetJobStepResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetJobStepResult(
            action=self.action,
            credential=self.credential,
            execution_options=self.execution_options,
            id=self.id,
            name=self.name,
            output=self.output,
            step_id=self.step_id,
            target_group=self.target_group,
            type=self.type)


def get_job_step(job_agent_name: Optional[str] = None,
                 job_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 server_name: Optional[str] = None,
                 step_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetJobStepResult:
    """
    Gets a job step in a job's current version.


    :param str job_agent_name: The name of the job agent.
    :param str job_name: The name of the job.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str step_name: The name of the job step.
    """
    __args__ = dict()
    __args__['jobAgentName'] = job_agent_name
    __args__['jobName'] = job_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['serverName'] = server_name
    __args__['stepName'] = step_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:sql/v20211101preview:getJobStep', __args__, opts=opts, typ=GetJobStepResult).value

    return AwaitableGetJobStepResult(
        action=__ret__.action,
        credential=__ret__.credential,
        execution_options=__ret__.execution_options,
        id=__ret__.id,
        name=__ret__.name,
        output=__ret__.output,
        step_id=__ret__.step_id,
        target_group=__ret__.target_group,
        type=__ret__.type)


@_utilities.lift_output_func(get_job_step)
def get_job_step_output(job_agent_name: Optional[pulumi.Input[str]] = None,
                        job_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        server_name: Optional[pulumi.Input[str]] = None,
                        step_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetJobStepResult]:
    """
    Gets a job step in a job's current version.


    :param str job_agent_name: The name of the job agent.
    :param str job_name: The name of the job.
    :param str resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str server_name: The name of the server.
    :param str step_name: The name of the job step.
    """
    ...
