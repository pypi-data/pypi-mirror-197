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
    'GetSqlResourceSqlTriggerResult',
    'AwaitableGetSqlResourceSqlTriggerResult',
    'get_sql_resource_sql_trigger',
    'get_sql_resource_sql_trigger_output',
]

warnings.warn("""Version 2019-12-12 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetSqlResourceSqlTriggerResult:
    """
    An Azure Cosmos DB trigger.
    """
    def __init__(__self__, id=None, location=None, name=None, resource=None, tags=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource and not isinstance(resource, dict):
            raise TypeError("Expected argument 'resource' to be a dict")
        pulumi.set(__self__, "resource", resource)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique resource identifier of the ARM resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the ARM resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def resource(self) -> Optional['outputs.SqlTriggerGetPropertiesResponseResource']:
        return pulumi.get(self, "resource")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetSqlResourceSqlTriggerResult(GetSqlResourceSqlTriggerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSqlResourceSqlTriggerResult(
            id=self.id,
            location=self.location,
            name=self.name,
            resource=self.resource,
            tags=self.tags,
            type=self.type)


def get_sql_resource_sql_trigger(account_name: Optional[str] = None,
                                 container_name: Optional[str] = None,
                                 database_name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 trigger_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSqlResourceSqlTriggerResult:
    """
    Gets the SQL trigger under an existing Azure Cosmos DB database account.


    :param str account_name: Cosmos DB database account name.
    :param str container_name: Cosmos DB container name.
    :param str database_name: Cosmos DB database name.
    :param str resource_group_name: Name of an Azure resource group.
    :param str trigger_name: Cosmos DB trigger name.
    """
    pulumi.log.warn("""get_sql_resource_sql_trigger is deprecated: Version 2019-12-12 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['containerName'] = container_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['triggerName'] = trigger_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:documentdb/v20191212:getSqlResourceSqlTrigger', __args__, opts=opts, typ=GetSqlResourceSqlTriggerResult).value

    return AwaitableGetSqlResourceSqlTriggerResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        resource=__ret__.resource,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_sql_resource_sql_trigger)
def get_sql_resource_sql_trigger_output(account_name: Optional[pulumi.Input[str]] = None,
                                        container_name: Optional[pulumi.Input[str]] = None,
                                        database_name: Optional[pulumi.Input[str]] = None,
                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                        trigger_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSqlResourceSqlTriggerResult]:
    """
    Gets the SQL trigger under an existing Azure Cosmos DB database account.


    :param str account_name: Cosmos DB database account name.
    :param str container_name: Cosmos DB container name.
    :param str database_name: Cosmos DB database name.
    :param str resource_group_name: Name of an Azure resource group.
    :param str trigger_name: Cosmos DB trigger name.
    """
    pulumi.log.warn("""get_sql_resource_sql_trigger is deprecated: Version 2019-12-12 will be removed in v2 of the provider.""")
    ...
