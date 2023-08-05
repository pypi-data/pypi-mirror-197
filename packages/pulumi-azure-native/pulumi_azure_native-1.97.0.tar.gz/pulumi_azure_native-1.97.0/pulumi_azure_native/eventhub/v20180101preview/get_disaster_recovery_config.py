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
    'GetDisasterRecoveryConfigResult',
    'AwaitableGetDisasterRecoveryConfigResult',
    'get_disaster_recovery_config',
    'get_disaster_recovery_config_output',
]

@pulumi.output_type
class GetDisasterRecoveryConfigResult:
    """
    Single item in List or Get Alias(Disaster Recovery configuration) operation
    """
    def __init__(__self__, alternate_name=None, id=None, name=None, partner_namespace=None, pending_replication_operations_count=None, provisioning_state=None, role=None, type=None):
        if alternate_name and not isinstance(alternate_name, str):
            raise TypeError("Expected argument 'alternate_name' to be a str")
        pulumi.set(__self__, "alternate_name", alternate_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if partner_namespace and not isinstance(partner_namespace, str):
            raise TypeError("Expected argument 'partner_namespace' to be a str")
        pulumi.set(__self__, "partner_namespace", partner_namespace)
        if pending_replication_operations_count and not isinstance(pending_replication_operations_count, float):
            raise TypeError("Expected argument 'pending_replication_operations_count' to be a float")
        pulumi.set(__self__, "pending_replication_operations_count", pending_replication_operations_count)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if role and not isinstance(role, str):
            raise TypeError("Expected argument 'role' to be a str")
        pulumi.set(__self__, "role", role)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="alternateName")
    def alternate_name(self) -> Optional[str]:
        """
        Alternate name specified when alias and namespace names are same.
        """
        return pulumi.get(self, "alternate_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
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
    @pulumi.getter(name="partnerNamespace")
    def partner_namespace(self) -> Optional[str]:
        """
        ARM Id of the Primary/Secondary eventhub namespace name, which is part of GEO DR pairing
        """
        return pulumi.get(self, "partner_namespace")

    @property
    @pulumi.getter(name="pendingReplicationOperationsCount")
    def pending_replication_operations_count(self) -> float:
        """
        Number of entities pending to be replicated.
        """
        return pulumi.get(self, "pending_replication_operations_count")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the Alias(Disaster Recovery configuration) - possible values 'Accepted' or 'Succeeded' or 'Failed'
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        role of namespace in GEO DR - possible values 'Primary' or 'PrimaryNotReplicating' or 'Secondary'
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetDisasterRecoveryConfigResult(GetDisasterRecoveryConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDisasterRecoveryConfigResult(
            alternate_name=self.alternate_name,
            id=self.id,
            name=self.name,
            partner_namespace=self.partner_namespace,
            pending_replication_operations_count=self.pending_replication_operations_count,
            provisioning_state=self.provisioning_state,
            role=self.role,
            type=self.type)


def get_disaster_recovery_config(alias: Optional[str] = None,
                                 namespace_name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDisasterRecoveryConfigResult:
    """
    Retrieves Alias(Disaster Recovery configuration) for primary or secondary namespace


    :param str alias: The Disaster Recovery configuration name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    __args__ = dict()
    __args__['alias'] = alias
    __args__['namespaceName'] = namespace_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:eventhub/v20180101preview:getDisasterRecoveryConfig', __args__, opts=opts, typ=GetDisasterRecoveryConfigResult).value

    return AwaitableGetDisasterRecoveryConfigResult(
        alternate_name=__ret__.alternate_name,
        id=__ret__.id,
        name=__ret__.name,
        partner_namespace=__ret__.partner_namespace,
        pending_replication_operations_count=__ret__.pending_replication_operations_count,
        provisioning_state=__ret__.provisioning_state,
        role=__ret__.role,
        type=__ret__.type)


@_utilities.lift_output_func(get_disaster_recovery_config)
def get_disaster_recovery_config_output(alias: Optional[pulumi.Input[str]] = None,
                                        namespace_name: Optional[pulumi.Input[str]] = None,
                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDisasterRecoveryConfigResult]:
    """
    Retrieves Alias(Disaster Recovery configuration) for primary or secondary namespace


    :param str alias: The Disaster Recovery configuration name
    :param str namespace_name: The Namespace name
    :param str resource_group_name: Name of the resource group within the azure subscription.
    """
    ...
