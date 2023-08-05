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

__all__ = [
    'ConnectionStateArgs',
    'PrivateEndpointConnectionArgs',
    'PrivateEndpointArgs',
]

@pulumi.input_type
class ConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PersistedConnectionStatus']]] = None):
        """
        ConnectionState information.
        :param pulumi.Input[str] actions_required: Actions required (if any).
        :param pulumi.Input[str] description: Description of the connection state.
        :param pulumi.Input[Union[str, 'PersistedConnectionStatus']] status: Status of the connection.
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
        Actions required (if any).
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the connection state.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PersistedConnectionStatus']]]:
        """
        Status of the connection.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PersistedConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class PrivateEndpointConnectionArgs:
    def __init__(__self__, *,
                 private_endpoint: Optional[pulumi.Input['PrivateEndpointArgs']] = None,
                 private_link_service_connection_state: Optional[pulumi.Input['ConnectionStateArgs']] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ResourceProvisioningState']]] = None):
        """
        :param pulumi.Input['PrivateEndpointArgs'] private_endpoint: Specifies the private endpoint.
        :param pulumi.Input['ConnectionStateArgs'] private_link_service_connection_state: Specifies the connection state.
        :param pulumi.Input[Union[str, 'ResourceProvisioningState']] provisioning_state: Provisioning state of the Private Endpoint Connection.
        """
        if private_endpoint is not None:
            pulumi.set(__self__, "private_endpoint", private_endpoint)
        if private_link_service_connection_state is not None:
            pulumi.set(__self__, "private_link_service_connection_state", private_link_service_connection_state)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> Optional[pulumi.Input['PrivateEndpointArgs']]:
        """
        Specifies the private endpoint.
        """
        return pulumi.get(self, "private_endpoint")

    @private_endpoint.setter
    def private_endpoint(self, value: Optional[pulumi.Input['PrivateEndpointArgs']]):
        pulumi.set(self, "private_endpoint", value)

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> Optional[pulumi.Input['ConnectionStateArgs']]:
        """
        Specifies the connection state.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @private_link_service_connection_state.setter
    def private_link_service_connection_state(self, value: Optional[pulumi.Input['ConnectionStateArgs']]):
        pulumi.set(self, "private_link_service_connection_state", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[Union[str, 'ResourceProvisioningState']]]:
        """
        Provisioning state of the Private Endpoint Connection.
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[Union[str, 'ResourceProvisioningState']]]):
        pulumi.set(self, "provisioning_state", value)


@pulumi.input_type
class PrivateEndpointArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] id: Specifies the id of private endpoint.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the id of private endpoint.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


