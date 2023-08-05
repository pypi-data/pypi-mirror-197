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
    'GetSynapseWorkspaceSqlPoolTableDataSetResult',
    'AwaitableGetSynapseWorkspaceSqlPoolTableDataSetResult',
    'get_synapse_workspace_sql_pool_table_data_set',
    'get_synapse_workspace_sql_pool_table_data_set_output',
]

@pulumi.output_type
class GetSynapseWorkspaceSqlPoolTableDataSetResult:
    """
    A Synapse Workspace Sql Pool Table data set.
    """
    def __init__(__self__, data_set_id=None, id=None, kind=None, name=None, synapse_workspace_sql_pool_table_resource_id=None, system_data=None, type=None):
        if data_set_id and not isinstance(data_set_id, str):
            raise TypeError("Expected argument 'data_set_id' to be a str")
        pulumi.set(__self__, "data_set_id", data_set_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if synapse_workspace_sql_pool_table_resource_id and not isinstance(synapse_workspace_sql_pool_table_resource_id, str):
            raise TypeError("Expected argument 'synapse_workspace_sql_pool_table_resource_id' to be a str")
        pulumi.set(__self__, "synapse_workspace_sql_pool_table_resource_id", synapse_workspace_sql_pool_table_resource_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dataSetId")
    def data_set_id(self) -> str:
        """
        Unique id for identifying a data set resource
        """
        return pulumi.get(self, "data_set_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource id of the azure resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Kind of data set.
        Expected value is 'SynapseWorkspaceSqlPoolTable'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the azure resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="synapseWorkspaceSqlPoolTableResourceId")
    def synapse_workspace_sql_pool_table_resource_id(self) -> str:
        """
        Resource id of the Synapse Workspace SQL Pool Table
        """
        return pulumi.get(self, "synapse_workspace_sql_pool_table_resource_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        System Data of the Azure resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the azure resource
        """
        return pulumi.get(self, "type")


class AwaitableGetSynapseWorkspaceSqlPoolTableDataSetResult(GetSynapseWorkspaceSqlPoolTableDataSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSynapseWorkspaceSqlPoolTableDataSetResult(
            data_set_id=self.data_set_id,
            id=self.id,
            kind=self.kind,
            name=self.name,
            synapse_workspace_sql_pool_table_resource_id=self.synapse_workspace_sql_pool_table_resource_id,
            system_data=self.system_data,
            type=self.type)


def get_synapse_workspace_sql_pool_table_data_set(account_name: Optional[str] = None,
                                                  data_set_name: Optional[str] = None,
                                                  resource_group_name: Optional[str] = None,
                                                  share_name: Optional[str] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSynapseWorkspaceSqlPoolTableDataSetResult:
    """
    Get a DataSet in a share


    :param str account_name: The name of the share account.
    :param str data_set_name: The name of the dataSet.
    :param str resource_group_name: The resource group name.
    :param str share_name: The name of the share.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['dataSetName'] = data_set_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['shareName'] = share_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:datashare/v20201001preview:getSynapseWorkspaceSqlPoolTableDataSet', __args__, opts=opts, typ=GetSynapseWorkspaceSqlPoolTableDataSetResult).value

    return AwaitableGetSynapseWorkspaceSqlPoolTableDataSetResult(
        data_set_id=__ret__.data_set_id,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        synapse_workspace_sql_pool_table_resource_id=__ret__.synapse_workspace_sql_pool_table_resource_id,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_synapse_workspace_sql_pool_table_data_set)
def get_synapse_workspace_sql_pool_table_data_set_output(account_name: Optional[pulumi.Input[str]] = None,
                                                         data_set_name: Optional[pulumi.Input[str]] = None,
                                                         resource_group_name: Optional[pulumi.Input[str]] = None,
                                                         share_name: Optional[pulumi.Input[str]] = None,
                                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSynapseWorkspaceSqlPoolTableDataSetResult]:
    """
    Get a DataSet in a share


    :param str account_name: The name of the share account.
    :param str data_set_name: The name of the dataSet.
    :param str resource_group_name: The resource group name.
    :param str share_name: The name of the share.
    """
    ...
