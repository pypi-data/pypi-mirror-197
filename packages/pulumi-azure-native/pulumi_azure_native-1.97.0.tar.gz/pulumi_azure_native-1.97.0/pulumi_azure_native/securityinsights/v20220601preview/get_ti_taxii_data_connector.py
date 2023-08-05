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
    'GetTiTaxiiDataConnectorResult',
    'AwaitableGetTiTaxiiDataConnectorResult',
    'get_ti_taxii_data_connector',
    'get_ti_taxii_data_connector_output',
]

@pulumi.output_type
class GetTiTaxiiDataConnectorResult:
    """
    Data connector to pull Threat intelligence data from TAXII 2.0/2.1 server
    """
    def __init__(__self__, collection_id=None, data_types=None, etag=None, friendly_name=None, id=None, kind=None, name=None, password=None, polling_frequency=None, system_data=None, taxii_lookback_period=None, taxii_server=None, tenant_id=None, type=None, user_name=None, workspace_id=None):
        if collection_id and not isinstance(collection_id, str):
            raise TypeError("Expected argument 'collection_id' to be a str")
        pulumi.set(__self__, "collection_id", collection_id)
        if data_types and not isinstance(data_types, dict):
            raise TypeError("Expected argument 'data_types' to be a dict")
        pulumi.set(__self__, "data_types", data_types)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if friendly_name and not isinstance(friendly_name, str):
            raise TypeError("Expected argument 'friendly_name' to be a str")
        pulumi.set(__self__, "friendly_name", friendly_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if password and not isinstance(password, str):
            raise TypeError("Expected argument 'password' to be a str")
        pulumi.set(__self__, "password", password)
        if polling_frequency and not isinstance(polling_frequency, str):
            raise TypeError("Expected argument 'polling_frequency' to be a str")
        pulumi.set(__self__, "polling_frequency", polling_frequency)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if taxii_lookback_period and not isinstance(taxii_lookback_period, str):
            raise TypeError("Expected argument 'taxii_lookback_period' to be a str")
        pulumi.set(__self__, "taxii_lookback_period", taxii_lookback_period)
        if taxii_server and not isinstance(taxii_server, str):
            raise TypeError("Expected argument 'taxii_server' to be a str")
        pulumi.set(__self__, "taxii_server", taxii_server)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_name and not isinstance(user_name, str):
            raise TypeError("Expected argument 'user_name' to be a str")
        pulumi.set(__self__, "user_name", user_name)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="collectionId")
    def collection_id(self) -> Optional[str]:
        """
        The collection id of the TAXII server.
        """
        return pulumi.get(self, "collection_id")

    @property
    @pulumi.getter(name="dataTypes")
    def data_types(self) -> 'outputs.TiTaxiiDataConnectorDataTypesResponse':
        """
        The available data types for Threat Intelligence TAXII data connector.
        """
        return pulumi.get(self, "data_types")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[str]:
        """
        The friendly name for the TAXII server.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        The kind of the data connector
        Expected value is 'ThreatIntelligenceTaxii'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> Optional[str]:
        """
        The password for the TAXII server.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="pollingFrequency")
    def polling_frequency(self) -> str:
        """
        The polling frequency for the TAXII server.
        """
        return pulumi.get(self, "polling_frequency")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="taxiiLookbackPeriod")
    def taxii_lookback_period(self) -> Optional[str]:
        """
        The lookback period for the TAXII server.
        """
        return pulumi.get(self, "taxii_lookback_period")

    @property
    @pulumi.getter(name="taxiiServer")
    def taxii_server(self) -> Optional[str]:
        """
        The API root for the TAXII server.
        """
        return pulumi.get(self, "taxii_server")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant id to connect to, and get the data from.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[str]:
        """
        The userName for the TAXII server.
        """
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[str]:
        """
        The workspace id.
        """
        return pulumi.get(self, "workspace_id")


class AwaitableGetTiTaxiiDataConnectorResult(GetTiTaxiiDataConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTiTaxiiDataConnectorResult(
            collection_id=self.collection_id,
            data_types=self.data_types,
            etag=self.etag,
            friendly_name=self.friendly_name,
            id=self.id,
            kind=self.kind,
            name=self.name,
            password=self.password,
            polling_frequency=self.polling_frequency,
            system_data=self.system_data,
            taxii_lookback_period=self.taxii_lookback_period,
            taxii_server=self.taxii_server,
            tenant_id=self.tenant_id,
            type=self.type,
            user_name=self.user_name,
            workspace_id=self.workspace_id)


def get_ti_taxii_data_connector(data_connector_id: Optional[str] = None,
                                resource_group_name: Optional[str] = None,
                                workspace_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTiTaxiiDataConnectorResult:
    """
    Gets a data connector.


    :param str data_connector_id: Connector ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    __args__ = dict()
    __args__['dataConnectorId'] = data_connector_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:securityinsights/v20220601preview:getTiTaxiiDataConnector', __args__, opts=opts, typ=GetTiTaxiiDataConnectorResult).value

    return AwaitableGetTiTaxiiDataConnectorResult(
        collection_id=__ret__.collection_id,
        data_types=__ret__.data_types,
        etag=__ret__.etag,
        friendly_name=__ret__.friendly_name,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        password=__ret__.password,
        polling_frequency=__ret__.polling_frequency,
        system_data=__ret__.system_data,
        taxii_lookback_period=__ret__.taxii_lookback_period,
        taxii_server=__ret__.taxii_server,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type,
        user_name=__ret__.user_name,
        workspace_id=__ret__.workspace_id)


@_utilities.lift_output_func(get_ti_taxii_data_connector)
def get_ti_taxii_data_connector_output(data_connector_id: Optional[pulumi.Input[str]] = None,
                                       resource_group_name: Optional[pulumi.Input[str]] = None,
                                       workspace_name: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTiTaxiiDataConnectorResult]:
    """
    Gets a data connector.


    :param str data_connector_id: Connector ID
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str workspace_name: The name of the workspace.
    """
    ...
