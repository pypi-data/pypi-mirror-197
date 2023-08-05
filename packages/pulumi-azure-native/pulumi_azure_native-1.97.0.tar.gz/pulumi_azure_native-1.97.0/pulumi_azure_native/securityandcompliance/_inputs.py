# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'PrivateEndpointConnectionArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'ServiceAccessPolicyEntryArgs',
    'ServiceAuthenticationConfigurationInfoArgs',
    'ServiceCorsConfigurationInfoArgs',
    'ServiceCosmosDbConfigurationInfoArgs',
    'ServiceExportConfigurationInfoArgs',
    'ServicesPropertiesArgs',
    'ServicesResourceIdentityArgs',
]

@pulumi.input_type
class PrivateEndpointConnectionArgs:
    def __init__(__self__, *,
                 private_link_service_connection_state: pulumi.Input['PrivateLinkServiceConnectionStateArgs']):
        """
        The Private Endpoint Connection resource.
        :param pulumi.Input['PrivateLinkServiceConnectionStateArgs'] private_link_service_connection_state: A collection of information about the state of the connection between service consumer and provider.
        """
        pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> pulumi.Input['PrivateLinkServiceConnectionStateArgs']:
        """
        A collection of information about the state of the connection between service consumer and provider.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: pulumi.Input['PrivateLinkServiceConnectionStateArgs']):
        pulumi.set(self, "private_link_service_connection_state", value)


@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ServiceAccessPolicyEntryArgs:
    def __init__(__self__, *,
                 object_id: pulumi.Input[str]):
        """
        An access policy entry.
        :param pulumi.Input[str] object_id: An Azure AD object ID (User or Apps) that is allowed access to the FHIR service.
        """
        pulumi.set(__self__, "object_id", object_id)

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> pulumi.Input[str]:
        """
        An Azure AD object ID (User or Apps) that is allowed access to the FHIR service.
        """
        return pulumi.get(self, "object_id")

    @object_id.setter
    def object_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "object_id", value)


@pulumi.input_type
class ServiceAuthenticationConfigurationInfoArgs:
    def __init__(__self__, *,
                 audience: Optional[pulumi.Input[str]] = None,
                 authority: Optional[pulumi.Input[str]] = None,
                 smart_proxy_enabled: Optional[pulumi.Input[bool]] = None):
        """
        Authentication configuration information
        :param pulumi.Input[str] audience: The audience url for the service
        :param pulumi.Input[str] authority: The authority url for the service
        :param pulumi.Input[bool] smart_proxy_enabled: If the SMART on FHIR proxy is enabled
        """
        if audience is not None:
            pulumi.set(__self__, "audience", audience)
        if authority is not None:
            pulumi.set(__self__, "authority", authority)
        if smart_proxy_enabled is not None:
            pulumi.set(__self__, "smart_proxy_enabled", smart_proxy_enabled)

    @property
    @pulumi.getter
    def audience(self) -> Optional[pulumi.Input[str]]:
        """
        The audience url for the service
        """
        return pulumi.get(self, "audience")

    @audience.setter
    def audience(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "audience", value)

    @property
    @pulumi.getter
    def authority(self) -> Optional[pulumi.Input[str]]:
        """
        The authority url for the service
        """
        return pulumi.get(self, "authority")

    @authority.setter
    def authority(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authority", value)

    @property
    @pulumi.getter(name="smartProxyEnabled")
    def smart_proxy_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If the SMART on FHIR proxy is enabled
        """
        return pulumi.get(self, "smart_proxy_enabled")

    @smart_proxy_enabled.setter
    def smart_proxy_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "smart_proxy_enabled", value)


@pulumi.input_type
class ServiceCorsConfigurationInfoArgs:
    def __init__(__self__, *,
                 allow_credentials: Optional[pulumi.Input[bool]] = None,
                 headers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 max_age: Optional[pulumi.Input[float]] = None,
                 methods: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 origins: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The settings for the CORS configuration of the service instance.
        :param pulumi.Input[bool] allow_credentials: If credentials are allowed via CORS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] headers: The headers to be allowed via CORS.
        :param pulumi.Input[float] max_age: The max age to be allowed via CORS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] methods: The methods to be allowed via CORS.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] origins: The origins to be allowed via CORS.
        """
        if allow_credentials is not None:
            pulumi.set(__self__, "allow_credentials", allow_credentials)
        if headers is not None:
            pulumi.set(__self__, "headers", headers)
        if max_age is not None:
            pulumi.set(__self__, "max_age", max_age)
        if methods is not None:
            pulumi.set(__self__, "methods", methods)
        if origins is not None:
            pulumi.set(__self__, "origins", origins)

    @property
    @pulumi.getter(name="allowCredentials")
    def allow_credentials(self) -> Optional[pulumi.Input[bool]]:
        """
        If credentials are allowed via CORS.
        """
        return pulumi.get(self, "allow_credentials")

    @allow_credentials.setter
    def allow_credentials(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_credentials", value)

    @property
    @pulumi.getter
    def headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The headers to be allowed via CORS.
        """
        return pulumi.get(self, "headers")

    @headers.setter
    def headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "headers", value)

    @property
    @pulumi.getter(name="maxAge")
    def max_age(self) -> Optional[pulumi.Input[float]]:
        """
        The max age to be allowed via CORS.
        """
        return pulumi.get(self, "max_age")

    @max_age.setter
    def max_age(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_age", value)

    @property
    @pulumi.getter
    def methods(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The methods to be allowed via CORS.
        """
        return pulumi.get(self, "methods")

    @methods.setter
    def methods(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "methods", value)

    @property
    @pulumi.getter
    def origins(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The origins to be allowed via CORS.
        """
        return pulumi.get(self, "origins")

    @origins.setter
    def origins(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "origins", value)


@pulumi.input_type
class ServiceCosmosDbConfigurationInfoArgs:
    def __init__(__self__, *,
                 key_vault_key_uri: Optional[pulumi.Input[str]] = None,
                 offer_throughput: Optional[pulumi.Input[float]] = None):
        """
        The settings for the Cosmos DB database backing the service.
        :param pulumi.Input[str] key_vault_key_uri: The URI of the customer-managed key for the backing database.
        :param pulumi.Input[float] offer_throughput: The provisioned throughput for the backing database.
        """
        if key_vault_key_uri is not None:
            pulumi.set(__self__, "key_vault_key_uri", key_vault_key_uri)
        if offer_throughput is not None:
            pulumi.set(__self__, "offer_throughput", offer_throughput)

    @property
    @pulumi.getter(name="keyVaultKeyUri")
    def key_vault_key_uri(self) -> Optional[pulumi.Input[str]]:
        """
        The URI of the customer-managed key for the backing database.
        """
        return pulumi.get(self, "key_vault_key_uri")

    @key_vault_key_uri.setter
    def key_vault_key_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_key_uri", value)

    @property
    @pulumi.getter(name="offerThroughput")
    def offer_throughput(self) -> Optional[pulumi.Input[float]]:
        """
        The provisioned throughput for the backing database.
        """
        return pulumi.get(self, "offer_throughput")

    @offer_throughput.setter
    def offer_throughput(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "offer_throughput", value)


@pulumi.input_type
class ServiceExportConfigurationInfoArgs:
    def __init__(__self__, *,
                 storage_account_name: Optional[pulumi.Input[str]] = None):
        """
        Export operation configuration information
        :param pulumi.Input[str] storage_account_name: The name of the default export storage account.
        """
        if storage_account_name is not None:
            pulumi.set(__self__, "storage_account_name", storage_account_name)

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the default export storage account.
        """
        return pulumi.get(self, "storage_account_name")

    @storage_account_name.setter
    def storage_account_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_account_name", value)


@pulumi.input_type
class ServicesPropertiesArgs:
    def __init__(__self__, *,
                 access_policies: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceAccessPolicyEntryArgs']]]] = None,
                 authentication_configuration: Optional[pulumi.Input['ServiceAuthenticationConfigurationInfoArgs']] = None,
                 cors_configuration: Optional[pulumi.Input['ServiceCorsConfigurationInfoArgs']] = None,
                 cosmos_db_configuration: Optional[pulumi.Input['ServiceCosmosDbConfigurationInfoArgs']] = None,
                 export_configuration: Optional[pulumi.Input['ServiceExportConfigurationInfoArgs']] = None,
                 private_endpoint_connections: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None):
        """
        The properties of a service instance.
        :param pulumi.Input[Sequence[pulumi.Input['ServiceAccessPolicyEntryArgs']]] access_policies: The access policies of the service instance.
        :param pulumi.Input['ServiceAuthenticationConfigurationInfoArgs'] authentication_configuration: The authentication configuration for the service instance.
        :param pulumi.Input['ServiceCorsConfigurationInfoArgs'] cors_configuration: The settings for the CORS configuration of the service instance.
        :param pulumi.Input['ServiceCosmosDbConfigurationInfoArgs'] cosmos_db_configuration: The settings for the Cosmos DB database backing the service.
        :param pulumi.Input['ServiceExportConfigurationInfoArgs'] export_configuration: The settings for the export operation of the service instance.
        :param pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]] private_endpoint_connections: The list of private endpoint connections that are set up for this resource.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Control permission for data plane traffic coming from public networks while private endpoint is enabled.
        """
        if access_policies is not None:
            pulumi.set(__self__, "access_policies", access_policies)
        if authentication_configuration is not None:
            pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if cors_configuration is not None:
            pulumi.set(__self__, "cors_configuration", cors_configuration)
        if cosmos_db_configuration is not None:
            pulumi.set(__self__, "cosmos_db_configuration", cosmos_db_configuration)
        if export_configuration is not None:
            pulumi.set(__self__, "export_configuration", export_configuration)
        if private_endpoint_connections is not None:
            pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)

    @property
    @pulumi.getter(name="accessPolicies")
    def access_policies(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceAccessPolicyEntryArgs']]]]:
        """
        The access policies of the service instance.
        """
        return pulumi.get(self, "access_policies")

    @access_policies.setter
    def access_policies(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceAccessPolicyEntryArgs']]]]):
        pulumi.set(self, "access_policies", value)

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional[pulumi.Input['ServiceAuthenticationConfigurationInfoArgs']]:
        """
        The authentication configuration for the service instance.
        """
        return pulumi.get(self, "authentication_configuration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: Optional[pulumi.Input['ServiceAuthenticationConfigurationInfoArgs']]):
        pulumi.set(self, "authentication_configuration", value)

    @property
    @pulumi.getter(name="corsConfiguration")
    def cors_configuration(self) -> Optional[pulumi.Input['ServiceCorsConfigurationInfoArgs']]:
        """
        The settings for the CORS configuration of the service instance.
        """
        return pulumi.get(self, "cors_configuration")

    @cors_configuration.setter
    def cors_configuration(self, value: Optional[pulumi.Input['ServiceCorsConfigurationInfoArgs']]):
        pulumi.set(self, "cors_configuration", value)

    @property
    @pulumi.getter(name="cosmosDbConfiguration")
    def cosmos_db_configuration(self) -> Optional[pulumi.Input['ServiceCosmosDbConfigurationInfoArgs']]:
        """
        The settings for the Cosmos DB database backing the service.
        """
        return pulumi.get(self, "cosmos_db_configuration")

    @cosmos_db_configuration.setter
    def cosmos_db_configuration(self, value: Optional[pulumi.Input['ServiceCosmosDbConfigurationInfoArgs']]):
        pulumi.set(self, "cosmos_db_configuration", value)

    @property
    @pulumi.getter(name="exportConfiguration")
    def export_configuration(self) -> Optional[pulumi.Input['ServiceExportConfigurationInfoArgs']]:
        """
        The settings for the export operation of the service instance.
        """
        return pulumi.get(self, "export_configuration")

    @export_configuration.setter
    def export_configuration(self, value: Optional[pulumi.Input['ServiceExportConfigurationInfoArgs']]):
        pulumi.set(self, "export_configuration", value)

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]]]:
        """
        The list of private endpoint connections that are set up for this resource.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @private_endpoint_connections.setter
    def private_endpoint_connections(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['PrivateEndpointConnectionArgs']]]]):
        pulumi.set(self, "private_endpoint_connections", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]:
        """
        Control permission for data plane traffic coming from public networks while private endpoint is enabled.
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]):
        pulumi.set(self, "public_network_access", value)


@pulumi.input_type
class ServicesResourceIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input[Union[str, 'ManagedServiceIdentityType']]] = None):
        """
        Setting indicating whether the service has a managed identity associated with it.
        :param pulumi.Input[Union[str, 'ManagedServiceIdentityType']] type: Type of identity being specified, currently SystemAssigned and None are allowed.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ManagedServiceIdentityType']]]:
        """
        Type of identity being specified, currently SystemAssigned and None are allowed.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ManagedServiceIdentityType']]]):
        pulumi.set(self, "type", value)


