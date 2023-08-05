# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['DataConnectorArgs', 'DataConnector']

@pulumi.input_type
class DataConnectorArgs:
    def __init__(__self__, *,
                 kind: pulumi.Input[Union[str, 'DataConnectorKind']],
                 operational_insights_resource_provider: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 workspace_name: pulumi.Input[str],
                 data_connector_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DataConnector resource.
        :param pulumi.Input[Union[str, 'DataConnectorKind']] kind: The kind of the data connector
        :param pulumi.Input[str] operational_insights_resource_provider: The namespace of workspaces resource provider- Microsoft.OperationalInsights.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        :param pulumi.Input[str] data_connector_id: Connector ID
        """
        pulumi.set(__self__, "kind", kind)
        pulumi.set(__self__, "operational_insights_resource_provider", operational_insights_resource_provider)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "workspace_name", workspace_name)
        if data_connector_id is not None:
            pulumi.set(__self__, "data_connector_id", data_connector_id)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[Union[str, 'DataConnectorKind']]:
        """
        The kind of the data connector
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[Union[str, 'DataConnectorKind']]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="operationalInsightsResourceProvider")
    def operational_insights_resource_provider(self) -> pulumi.Input[str]:
        """
        The namespace of workspaces resource provider- Microsoft.OperationalInsights.
        """
        return pulumi.get(self, "operational_insights_resource_provider")

    @operational_insights_resource_provider.setter
    def operational_insights_resource_provider(self, value: pulumi.Input[str]):
        pulumi.set(self, "operational_insights_resource_provider", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the user's subscription. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> pulumi.Input[str]:
        """
        The name of the workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_name", value)

    @property
    @pulumi.getter(name="dataConnectorId")
    def data_connector_id(self) -> Optional[pulumi.Input[str]]:
        """
        Connector ID
        """
        return pulumi.get(self, "data_connector_id")

    @data_connector_id.setter
    def data_connector_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_connector_id", value)


warnings.warn("""Please use one of the variants: AADDataConnector, AATPDataConnector, ASCDataConnector, AwsCloudTrailDataConnector, Dynamics365DataConnector, MCASDataConnector, MDATPDataConnector, MSTIDataConnector, MTPDataConnector, OfficeATPDataConnector, OfficeDataConnector, TIDataConnector, TiTaxiiDataConnector.""", DeprecationWarning)


class DataConnector(pulumi.CustomResource):
    warnings.warn("""Please use one of the variants: AADDataConnector, AATPDataConnector, ASCDataConnector, AwsCloudTrailDataConnector, Dynamics365DataConnector, MCASDataConnector, MDATPDataConnector, MSTIDataConnector, MTPDataConnector, OfficeATPDataConnector, OfficeDataConnector, TIDataConnector, TiTaxiiDataConnector.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_connector_id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'DataConnectorKind']]] = None,
                 operational_insights_resource_provider: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Data connector.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] data_connector_id: Connector ID
        :param pulumi.Input[Union[str, 'DataConnectorKind']] kind: The kind of the data connector
        :param pulumi.Input[str] operational_insights_resource_provider: The namespace of workspaces resource provider- Microsoft.OperationalInsights.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DataConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Data connector.

        :param str resource_name: The name of the resource.
        :param DataConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DataConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 data_connector_id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'DataConnectorKind']]] = None,
                 operational_insights_resource_provider: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""DataConnector is deprecated: Please use one of the variants: AADDataConnector, AATPDataConnector, ASCDataConnector, AwsCloudTrailDataConnector, Dynamics365DataConnector, MCASDataConnector, MDATPDataConnector, MSTIDataConnector, MTPDataConnector, OfficeATPDataConnector, OfficeDataConnector, TIDataConnector, TiTaxiiDataConnector.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DataConnectorArgs.__new__(DataConnectorArgs)

            __props__.__dict__["data_connector_id"] = data_connector_id
            if kind is None and not opts.urn:
                raise TypeError("Missing required property 'kind'")
            __props__.__dict__["kind"] = kind
            if operational_insights_resource_provider is None and not opts.urn:
                raise TypeError("Missing required property 'operational_insights_resource_provider'")
            __props__.__dict__["operational_insights_resource_provider"] = operational_insights_resource_provider
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:securityinsights:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20200101:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20210301preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20210901preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20211001:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20211001preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220101preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220401preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220501preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220601preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220701preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220801:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220801preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20220901preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20221001preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20221101:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20221101preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20221201preview:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20230201:DataConnector"), pulumi.Alias(type_="azure-native:securityinsights/v20230201preview:DataConnector")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DataConnector, __self__).__init__(
            'azure-native:securityinsights/v20190101preview:DataConnector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DataConnector':
        """
        Get an existing DataConnector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DataConnectorArgs.__new__(DataConnectorArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["type"] = None
        return DataConnector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Etag of the azure resource
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        The kind of the data connector
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

