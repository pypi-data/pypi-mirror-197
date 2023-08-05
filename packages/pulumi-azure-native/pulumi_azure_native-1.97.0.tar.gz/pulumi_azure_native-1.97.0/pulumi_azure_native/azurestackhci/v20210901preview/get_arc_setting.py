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
    'GetArcSettingResult',
    'AwaitableGetArcSettingResult',
    'get_arc_setting',
    'get_arc_setting_output',
]

@pulumi.output_type
class GetArcSettingResult:
    """
    ArcSetting details.
    """
    def __init__(__self__, aggregate_state=None, arc_instance_resource_group=None, created_at=None, created_by=None, created_by_type=None, id=None, last_modified_at=None, last_modified_by=None, last_modified_by_type=None, name=None, per_node_details=None, provisioning_state=None, type=None):
        if aggregate_state and not isinstance(aggregate_state, str):
            raise TypeError("Expected argument 'aggregate_state' to be a str")
        pulumi.set(__self__, "aggregate_state", aggregate_state)
        if arc_instance_resource_group and not isinstance(arc_instance_resource_group, str):
            raise TypeError("Expected argument 'arc_instance_resource_group' to be a str")
        pulumi.set(__self__, "arc_instance_resource_group", arc_instance_resource_group)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if created_by and not isinstance(created_by, str):
            raise TypeError("Expected argument 'created_by' to be a str")
        pulumi.set(__self__, "created_by", created_by)
        if created_by_type and not isinstance(created_by_type, str):
            raise TypeError("Expected argument 'created_by_type' to be a str")
        pulumi.set(__self__, "created_by_type", created_by_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_modified_at and not isinstance(last_modified_at, str):
            raise TypeError("Expected argument 'last_modified_at' to be a str")
        pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by and not isinstance(last_modified_by, str):
            raise TypeError("Expected argument 'last_modified_by' to be a str")
        pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type and not isinstance(last_modified_by_type, str):
            raise TypeError("Expected argument 'last_modified_by_type' to be a str")
        pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if per_node_details and not isinstance(per_node_details, list):
            raise TypeError("Expected argument 'per_node_details' to be a list")
        pulumi.set(__self__, "per_node_details", per_node_details)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="aggregateState")
    def aggregate_state(self) -> str:
        """
        Aggregate state of Arc agent across the nodes in this HCI cluster.
        """
        return pulumi.get(self, "aggregate_state")

    @property
    @pulumi.getter(name="arcInstanceResourceGroup")
    def arc_instance_resource_group(self) -> str:
        """
        The resource group that hosts the Arc agents, ie. Hybrid Compute Machine resources.
        """
        return pulumi.get(self, "arc_instance_resource_group")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="perNodeDetails")
    def per_node_details(self) -> Sequence['outputs.PerNodeStateResponse']:
        """
        State of Arc agent in each of the nodes.
        """
        return pulumi.get(self, "per_node_details")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the ArcSetting proxy resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetArcSettingResult(GetArcSettingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetArcSettingResult(
            aggregate_state=self.aggregate_state,
            arc_instance_resource_group=self.arc_instance_resource_group,
            created_at=self.created_at,
            created_by=self.created_by,
            created_by_type=self.created_by_type,
            id=self.id,
            last_modified_at=self.last_modified_at,
            last_modified_by=self.last_modified_by,
            last_modified_by_type=self.last_modified_by_type,
            name=self.name,
            per_node_details=self.per_node_details,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_arc_setting(arc_setting_name: Optional[str] = None,
                    cluster_name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetArcSettingResult:
    """
    Get ArcSetting resource details of HCI Cluster.


    :param str arc_setting_name: The name of the proxy resource holding details of HCI ArcSetting information.
    :param str cluster_name: The name of the cluster.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['arcSettingName'] = arc_setting_name
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:azurestackhci/v20210901preview:getArcSetting', __args__, opts=opts, typ=GetArcSettingResult).value

    return AwaitableGetArcSettingResult(
        aggregate_state=__ret__.aggregate_state,
        arc_instance_resource_group=__ret__.arc_instance_resource_group,
        created_at=__ret__.created_at,
        created_by=__ret__.created_by,
        created_by_type=__ret__.created_by_type,
        id=__ret__.id,
        last_modified_at=__ret__.last_modified_at,
        last_modified_by=__ret__.last_modified_by,
        last_modified_by_type=__ret__.last_modified_by_type,
        name=__ret__.name,
        per_node_details=__ret__.per_node_details,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)


@_utilities.lift_output_func(get_arc_setting)
def get_arc_setting_output(arc_setting_name: Optional[pulumi.Input[str]] = None,
                           cluster_name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetArcSettingResult]:
    """
    Get ArcSetting resource details of HCI Cluster.


    :param str arc_setting_name: The name of the proxy resource holding details of HCI ArcSetting information.
    :param str cluster_name: The name of the cluster.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
