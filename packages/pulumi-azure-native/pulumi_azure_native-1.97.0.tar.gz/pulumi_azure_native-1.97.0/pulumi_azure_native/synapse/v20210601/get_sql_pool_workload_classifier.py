# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetSqlPoolWorkloadClassifierResult',
    'AwaitableGetSqlPoolWorkloadClassifierResult',
    'get_sql_pool_workload_classifier',
    'get_sql_pool_workload_classifier_output',
]

@pulumi.output_type
class GetSqlPoolWorkloadClassifierResult:
    """
    Workload classifier operations for a data warehouse
    """
    def __init__(__self__, context=None, end_time=None, id=None, importance=None, label=None, member_name=None, name=None, start_time=None, type=None):
        if context and not isinstance(context, str):
            raise TypeError("Expected argument 'context' to be a str")
        pulumi.set(__self__, "context", context)
        if end_time and not isinstance(end_time, str):
            raise TypeError("Expected argument 'end_time' to be a str")
        pulumi.set(__self__, "end_time", end_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if importance and not isinstance(importance, str):
            raise TypeError("Expected argument 'importance' to be a str")
        pulumi.set(__self__, "importance", importance)
        if label and not isinstance(label, str):
            raise TypeError("Expected argument 'label' to be a str")
        pulumi.set(__self__, "label", label)
        if member_name and not isinstance(member_name, str):
            raise TypeError("Expected argument 'member_name' to be a str")
        pulumi.set(__self__, "member_name", member_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if start_time and not isinstance(start_time, str):
            raise TypeError("Expected argument 'start_time' to be a str")
        pulumi.set(__self__, "start_time", start_time)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def context(self) -> Optional[str]:
        """
        The workload classifier context.
        """
        return pulumi.get(self, "context")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[str]:
        """
        The workload classifier end time for classification.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def importance(self) -> Optional[str]:
        """
        The workload classifier importance.
        """
        return pulumi.get(self, "importance")

    @property
    @pulumi.getter
    def label(self) -> Optional[str]:
        """
        The workload classifier label.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter(name="memberName")
    def member_name(self) -> str:
        """
        The workload classifier member name.
        """
        return pulumi.get(self, "member_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[str]:
        """
        The workload classifier start time for classification.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSqlPoolWorkloadClassifierResult(GetSqlPoolWorkloadClassifierResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlPoolWorkloadClassifierResult(
            context=self.context,
            end_time=self.end_time,
            id=self.id,
            importance=self.importance,
            label=self.label,
            member_name=self.member_name,
            name=self.name,
            start_time=self.start_time,
            type=self.type)


def get_sql_pool_workload_classifier(resource_group_name: Optional[str] = None,
                                     sql_pool_name: Optional[str] = None,
                                     workload_classifier_name: Optional[str] = None,
                                     workload_group_name: Optional[str] = None,
                                     workspace_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlPoolWorkloadClassifierResult:
    """
    Get a workload classifier of Sql pool's workload group.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sql_pool_name: SQL pool name
    :param str workload_classifier_name: The name of the workload classifier.
    :param str workload_group_name: The name of the workload group.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['sqlPoolName'] = sql_pool_name
    __args__['workloadClassifierName'] = workload_classifier_name
    __args__['workloadGroupName'] = workload_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:synapse/v20210601:getSqlPoolWorkloadClassifier', __args__, opts=opts, typ=GetSqlPoolWorkloadClassifierResult).value

    return AwaitableGetSqlPoolWorkloadClassifierResult(
        context=__ret__.context,
        end_time=__ret__.end_time,
        id=__ret__.id,
        importance=__ret__.importance,
        label=__ret__.label,
        member_name=__ret__.member_name,
        name=__ret__.name,
        start_time=__ret__.start_time,
        type=__ret__.type)


@_utilities.lift_output_func(get_sql_pool_workload_classifier)
def get_sql_pool_workload_classifier_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                            sql_pool_name: Optional[pulumi.Input[str]] = None,
                                            workload_classifier_name: Optional[pulumi.Input[str]] = None,
                                            workload_group_name: Optional[pulumi.Input[str]] = None,
                                            workspace_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSqlPoolWorkloadClassifierResult]:
    """
    Get a workload classifier of Sql pool's workload group.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sql_pool_name: SQL pool name
    :param str workload_classifier_name: The name of the workload classifier.
    :param str workload_group_name: The name of the workload group.
    :param str workspace_name: The name of the workspace.
    """
    ...
