# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetSecurityUserConfigurationResult',
    'AwaitableGetSecurityUserConfigurationResult',
    'get_security_user_configuration',
    'get_security_user_configuration_output',
]

@pulumi.output_type
class GetSecurityUserConfigurationResult:
    """
    Defines the security configuration
    """
    def __init__(__self__, delete_existing_nsgs=None, description=None, display_name=None, etag=None, id=None, name=None, provisioning_state=None, security_type=None, system_data=None, type=None):
        if delete_existing_nsgs and not isinstance(delete_existing_nsgs, str):
            raise TypeError("Expected argument 'delete_existing_nsgs' to be a str")
        pulumi.set(__self__, "delete_existing_nsgs", delete_existing_nsgs)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if security_type and not isinstance(security_type, str):
            raise TypeError("Expected argument 'security_type' to be a str")
        pulumi.set(__self__, "security_type", security_type)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="deleteExistingNSGs")
    def delete_existing_nsgs(self) -> Optional[str]:
        """
        Flag if need to delete existing network security groups.
        """
        return pulumi.get(self, "delete_existing_nsgs")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description of the security configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        A display name of the security configuration.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="securityType")
    def security_type(self) -> Optional[str]:
        """
        Security Type.
        """
        return pulumi.get(self, "security_type")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system metadata related to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetSecurityUserConfigurationResult(GetSecurityUserConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityUserConfigurationResult(
            delete_existing_nsgs=self.delete_existing_nsgs,
            description=self.description,
            display_name=self.display_name,
            etag=self.etag,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            security_type=self.security_type,
            system_data=self.system_data,
            type=self.type)


def get_security_user_configuration(configuration_name: Optional[str] = None,
                                    network_manager_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityUserConfigurationResult:
    """
    Retrieves a network manager security user configuration.
    API Version: 2021-02-01-preview.


    :param str configuration_name: The name of the network manager security Configuration.
    :param str network_manager_name: The name of the network manager.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['configurationName'] = configuration_name
    __args__['networkManagerName'] = network_manager_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:network:getSecurityUserConfiguration', __args__, opts=opts, typ=GetSecurityUserConfigurationResult).value

    return AwaitableGetSecurityUserConfigurationResult(
        delete_existing_nsgs=__ret__.delete_existing_nsgs,
        description=__ret__.description,
        display_name=__ret__.display_name,
        etag=__ret__.etag,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        security_type=__ret__.security_type,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_security_user_configuration)
def get_security_user_configuration_output(configuration_name: Optional[pulumi.Input[str]] = None,
                                           network_manager_name: Optional[pulumi.Input[str]] = None,
                                           resource_group_name: Optional[pulumi.Input[str]] = None,
                                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecurityUserConfigurationResult]:
    """
    Retrieves a network manager security user configuration.
    API Version: 2021-02-01-preview.


    :param str configuration_name: The name of the network manager security Configuration.
    :param str network_manager_name: The name of the network manager.
    :param str resource_group_name: The name of the resource group.
    """
    ...
