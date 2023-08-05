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
    'GetRoleAssignmentResult',
    'AwaitableGetRoleAssignmentResult',
    'get_role_assignment',
    'get_role_assignment_output',
]

@pulumi.output_type
class GetRoleAssignmentResult:
    """
    Role Assignments
    """
    def __init__(__self__, condition=None, condition_version=None, created_by=None, created_on=None, delegated_managed_identity_resource_id=None, description=None, id=None, name=None, principal_id=None, principal_type=None, role_definition_id=None, scope=None, type=None, updated_by=None, updated_on=None):
        if condition and not isinstance(condition, str):
            raise TypeError("Expected argument 'condition' to be a str")
        pulumi.set(__self__, "condition", condition)
        if condition_version and not isinstance(condition_version, str):
            raise TypeError("Expected argument 'condition_version' to be a str")
        pulumi.set(__self__, "condition_version", condition_version)
        if created_by and not isinstance(created_by, str):
            raise TypeError("Expected argument 'created_by' to be a str")
        pulumi.set(__self__, "created_by", created_by)
        if created_on and not isinstance(created_on, str):
            raise TypeError("Expected argument 'created_on' to be a str")
        pulumi.set(__self__, "created_on", created_on)
        if delegated_managed_identity_resource_id and not isinstance(delegated_managed_identity_resource_id, str):
            raise TypeError("Expected argument 'delegated_managed_identity_resource_id' to be a str")
        pulumi.set(__self__, "delegated_managed_identity_resource_id", delegated_managed_identity_resource_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if principal_id and not isinstance(principal_id, str):
            raise TypeError("Expected argument 'principal_id' to be a str")
        pulumi.set(__self__, "principal_id", principal_id)
        if principal_type and not isinstance(principal_type, str):
            raise TypeError("Expected argument 'principal_type' to be a str")
        pulumi.set(__self__, "principal_type", principal_type)
        if role_definition_id and not isinstance(role_definition_id, str):
            raise TypeError("Expected argument 'role_definition_id' to be a str")
        pulumi.set(__self__, "role_definition_id", role_definition_id)
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, "scope", scope)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if updated_by and not isinstance(updated_by, str):
            raise TypeError("Expected argument 'updated_by' to be a str")
        pulumi.set(__self__, "updated_by", updated_by)
        if updated_on and not isinstance(updated_on, str):
            raise TypeError("Expected argument 'updated_on' to be a str")
        pulumi.set(__self__, "updated_on", updated_on)

    @property
    @pulumi.getter
    def condition(self) -> Optional[str]:
        """
        The conditions on the role assignment. This limits the resources it can be assigned to. e.g.: @Resource[Microsoft.Storage/storageAccounts/blobServices/containers:ContainerName] StringEqualsIgnoreCase 'foo_storage_container'
        """
        return pulumi.get(self, "condition")

    @property
    @pulumi.getter(name="conditionVersion")
    def condition_version(self) -> Optional[str]:
        """
        Version of the condition. Currently accepted value is '2.0'
        """
        return pulumi.get(self, "condition_version")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> str:
        """
        Id of the user who created the assignment
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdOn")
    def created_on(self) -> str:
        """
        Time it was created
        """
        return pulumi.get(self, "created_on")

    @property
    @pulumi.getter(name="delegatedManagedIdentityResourceId")
    def delegated_managed_identity_resource_id(self) -> Optional[str]:
        """
        Id of the delegated managed identity resource
        """
        return pulumi.get(self, "delegated_managed_identity_resource_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of role assignment
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The role assignment ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The role assignment name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The principal ID.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="principalType")
    def principal_type(self) -> Optional[str]:
        """
        The principal type of the assigned principal ID.
        """
        return pulumi.get(self, "principal_type")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> str:
        """
        The role definition ID.
        """
        return pulumi.get(self, "role_definition_id")

    @property
    @pulumi.getter
    def scope(self) -> str:
        """
        The role assignment scope.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The role assignment type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> str:
        """
        Id of the user who updated the assignment
        """
        return pulumi.get(self, "updated_by")

    @property
    @pulumi.getter(name="updatedOn")
    def updated_on(self) -> str:
        """
        Time it was updated
        """
        return pulumi.get(self, "updated_on")


class AwaitableGetRoleAssignmentResult(GetRoleAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoleAssignmentResult(
            condition=self.condition,
            condition_version=self.condition_version,
            created_by=self.created_by,
            created_on=self.created_on,
            delegated_managed_identity_resource_id=self.delegated_managed_identity_resource_id,
            description=self.description,
            id=self.id,
            name=self.name,
            principal_id=self.principal_id,
            principal_type=self.principal_type,
            role_definition_id=self.role_definition_id,
            scope=self.scope,
            type=self.type,
            updated_by=self.updated_by,
            updated_on=self.updated_on)


def get_role_assignment(role_assignment_name: Optional[str] = None,
                        scope: Optional[str] = None,
                        tenant_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoleAssignmentResult:
    """
    Get a role assignment by scope and name.


    :param str role_assignment_name: The name of the role assignment. It can be any valid GUID.
    :param str scope: The scope of the operation or resource. Valid scopes are: subscription (format: '/subscriptions/{subscriptionId}'), resource group (format: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}', or resource (format: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/[{parentResourcePath}/]{resourceType}/{resourceName}'
    :param str tenant_id: Tenant ID for cross-tenant request
    """
    __args__ = dict()
    __args__['roleAssignmentName'] = role_assignment_name
    __args__['scope'] = scope
    __args__['tenantId'] = tenant_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:authorization/v20201001preview:getRoleAssignment', __args__, opts=opts, typ=GetRoleAssignmentResult).value

    return AwaitableGetRoleAssignmentResult(
        condition=__ret__.condition,
        condition_version=__ret__.condition_version,
        created_by=__ret__.created_by,
        created_on=__ret__.created_on,
        delegated_managed_identity_resource_id=__ret__.delegated_managed_identity_resource_id,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        principal_id=__ret__.principal_id,
        principal_type=__ret__.principal_type,
        role_definition_id=__ret__.role_definition_id,
        scope=__ret__.scope,
        type=__ret__.type,
        updated_by=__ret__.updated_by,
        updated_on=__ret__.updated_on)


@_utilities.lift_output_func(get_role_assignment)
def get_role_assignment_output(role_assignment_name: Optional[pulumi.Input[str]] = None,
                               scope: Optional[pulumi.Input[str]] = None,
                               tenant_id: Optional[pulumi.Input[Optional[str]]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoleAssignmentResult]:
    """
    Get a role assignment by scope and name.


    :param str role_assignment_name: The name of the role assignment. It can be any valid GUID.
    :param str scope: The scope of the operation or resource. Valid scopes are: subscription (format: '/subscriptions/{subscriptionId}'), resource group (format: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}', or resource (format: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/[{parentResourcePath}/]{resourceType}/{resourceName}'
    :param str tenant_id: Tenant ID for cross-tenant request
    """
    ...
