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
    'GetEventGridDataConnectionResult',
    'AwaitableGetEventGridDataConnectionResult',
    'get_event_grid_data_connection',
    'get_event_grid_data_connection_output',
]

@pulumi.output_type
class GetEventGridDataConnectionResult:
    """
    Class representing an Event Grid data connection.
    """
    def __init__(__self__, blob_storage_event_type=None, consumer_group=None, data_format=None, database_routing=None, event_grid_resource_id=None, event_hub_resource_id=None, id=None, ignore_first_record=None, kind=None, location=None, managed_identity_object_id=None, managed_identity_resource_id=None, mapping_rule_name=None, name=None, provisioning_state=None, storage_account_resource_id=None, table_name=None, type=None):
        if blob_storage_event_type and not isinstance(blob_storage_event_type, str):
            raise TypeError("Expected argument 'blob_storage_event_type' to be a str")
        pulumi.set(__self__, "blob_storage_event_type", blob_storage_event_type)
        if consumer_group and not isinstance(consumer_group, str):
            raise TypeError("Expected argument 'consumer_group' to be a str")
        pulumi.set(__self__, "consumer_group", consumer_group)
        if data_format and not isinstance(data_format, str):
            raise TypeError("Expected argument 'data_format' to be a str")
        pulumi.set(__self__, "data_format", data_format)
        if database_routing and not isinstance(database_routing, str):
            raise TypeError("Expected argument 'database_routing' to be a str")
        pulumi.set(__self__, "database_routing", database_routing)
        if event_grid_resource_id and not isinstance(event_grid_resource_id, str):
            raise TypeError("Expected argument 'event_grid_resource_id' to be a str")
        pulumi.set(__self__, "event_grid_resource_id", event_grid_resource_id)
        if event_hub_resource_id and not isinstance(event_hub_resource_id, str):
            raise TypeError("Expected argument 'event_hub_resource_id' to be a str")
        pulumi.set(__self__, "event_hub_resource_id", event_hub_resource_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ignore_first_record and not isinstance(ignore_first_record, bool):
            raise TypeError("Expected argument 'ignore_first_record' to be a bool")
        pulumi.set(__self__, "ignore_first_record", ignore_first_record)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_identity_object_id and not isinstance(managed_identity_object_id, str):
            raise TypeError("Expected argument 'managed_identity_object_id' to be a str")
        pulumi.set(__self__, "managed_identity_object_id", managed_identity_object_id)
        if managed_identity_resource_id and not isinstance(managed_identity_resource_id, str):
            raise TypeError("Expected argument 'managed_identity_resource_id' to be a str")
        pulumi.set(__self__, "managed_identity_resource_id", managed_identity_resource_id)
        if mapping_rule_name and not isinstance(mapping_rule_name, str):
            raise TypeError("Expected argument 'mapping_rule_name' to be a str")
        pulumi.set(__self__, "mapping_rule_name", mapping_rule_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if storage_account_resource_id and not isinstance(storage_account_resource_id, str):
            raise TypeError("Expected argument 'storage_account_resource_id' to be a str")
        pulumi.set(__self__, "storage_account_resource_id", storage_account_resource_id)
        if table_name and not isinstance(table_name, str):
            raise TypeError("Expected argument 'table_name' to be a str")
        pulumi.set(__self__, "table_name", table_name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="blobStorageEventType")
    def blob_storage_event_type(self) -> Optional[str]:
        """
        The name of blob storage event type to process.
        """
        return pulumi.get(self, "blob_storage_event_type")

    @property
    @pulumi.getter(name="consumerGroup")
    def consumer_group(self) -> str:
        """
        The event hub consumer group.
        """
        return pulumi.get(self, "consumer_group")

    @property
    @pulumi.getter(name="dataFormat")
    def data_format(self) -> Optional[str]:
        """
        The data format of the message. Optionally the data format can be added to each message.
        """
        return pulumi.get(self, "data_format")

    @property
    @pulumi.getter(name="databaseRouting")
    def database_routing(self) -> Optional[str]:
        """
        Indication for database routing information from the data connection, by default only database routing information is allowed
        """
        return pulumi.get(self, "database_routing")

    @property
    @pulumi.getter(name="eventGridResourceId")
    def event_grid_resource_id(self) -> Optional[str]:
        """
        The resource ID of the event grid that is subscribed to the storage account events.
        """
        return pulumi.get(self, "event_grid_resource_id")

    @property
    @pulumi.getter(name="eventHubResourceId")
    def event_hub_resource_id(self) -> str:
        """
        The resource ID where the event grid is configured to send events.
        """
        return pulumi.get(self, "event_hub_resource_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ignoreFirstRecord")
    def ignore_first_record(self) -> Optional[bool]:
        """
        A Boolean value that, if set to true, indicates that ingestion should ignore the first record of every file
        """
        return pulumi.get(self, "ignore_first_record")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Kind of the endpoint for the data connection
        Expected value is 'EventGrid'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedIdentityObjectId")
    def managed_identity_object_id(self) -> str:
        """
        The object ID of managedIdentityResourceId
        """
        return pulumi.get(self, "managed_identity_object_id")

    @property
    @pulumi.getter(name="managedIdentityResourceId")
    def managed_identity_resource_id(self) -> Optional[str]:
        """
        The resource ID of a managed identity (system or user assigned) to be used to authenticate with event hub and storage account.
        """
        return pulumi.get(self, "managed_identity_resource_id")

    @property
    @pulumi.getter(name="mappingRuleName")
    def mapping_rule_name(self) -> Optional[str]:
        """
        The mapping rule to be used to ingest the data. Optionally the mapping information can be added to each message.
        """
        return pulumi.get(self, "mapping_rule_name")

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
        The provisioned state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="storageAccountResourceId")
    def storage_account_resource_id(self) -> str:
        """
        The resource ID of the storage account where the data resides.
        """
        return pulumi.get(self, "storage_account_resource_id")

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> Optional[str]:
        """
        The table where the data should be ingested. Optionally the table information can be added to each message.
        """
        return pulumi.get(self, "table_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetEventGridDataConnectionResult(GetEventGridDataConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventGridDataConnectionResult(
            blob_storage_event_type=self.blob_storage_event_type,
            consumer_group=self.consumer_group,
            data_format=self.data_format,
            database_routing=self.database_routing,
            event_grid_resource_id=self.event_grid_resource_id,
            event_hub_resource_id=self.event_hub_resource_id,
            id=self.id,
            ignore_first_record=self.ignore_first_record,
            kind=self.kind,
            location=self.location,
            managed_identity_object_id=self.managed_identity_object_id,
            managed_identity_resource_id=self.managed_identity_resource_id,
            mapping_rule_name=self.mapping_rule_name,
            name=self.name,
            provisioning_state=self.provisioning_state,
            storage_account_resource_id=self.storage_account_resource_id,
            table_name=self.table_name,
            type=self.type)


def get_event_grid_data_connection(cluster_name: Optional[str] = None,
                                   data_connection_name: Optional[str] = None,
                                   database_name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventGridDataConnectionResult:
    """
    Returns a data connection.


    :param str cluster_name: The name of the Kusto cluster.
    :param str data_connection_name: The name of the data connection.
    :param str database_name: The name of the database in the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['dataConnectionName'] = data_connection_name
    __args__['databaseName'] = database_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:kusto/v20221229:getEventGridDataConnection', __args__, opts=opts, typ=GetEventGridDataConnectionResult).value

    return AwaitableGetEventGridDataConnectionResult(
        blob_storage_event_type=__ret__.blob_storage_event_type,
        consumer_group=__ret__.consumer_group,
        data_format=__ret__.data_format,
        database_routing=__ret__.database_routing,
        event_grid_resource_id=__ret__.event_grid_resource_id,
        event_hub_resource_id=__ret__.event_hub_resource_id,
        id=__ret__.id,
        ignore_first_record=__ret__.ignore_first_record,
        kind=__ret__.kind,
        location=__ret__.location,
        managed_identity_object_id=__ret__.managed_identity_object_id,
        managed_identity_resource_id=__ret__.managed_identity_resource_id,
        mapping_rule_name=__ret__.mapping_rule_name,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        storage_account_resource_id=__ret__.storage_account_resource_id,
        table_name=__ret__.table_name,
        type=__ret__.type)


@_utilities.lift_output_func(get_event_grid_data_connection)
def get_event_grid_data_connection_output(cluster_name: Optional[pulumi.Input[str]] = None,
                                          data_connection_name: Optional[pulumi.Input[str]] = None,
                                          database_name: Optional[pulumi.Input[str]] = None,
                                          resource_group_name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventGridDataConnectionResult]:
    """
    Returns a data connection.


    :param str cluster_name: The name of the Kusto cluster.
    :param str data_connection_name: The name of the data connection.
    :param str database_name: The name of the database in the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    ...
