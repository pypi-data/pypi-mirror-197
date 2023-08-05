# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSerialPortResult',
    'AwaitableGetSerialPortResult',
    'get_serial_port',
    'get_serial_port_output',
]

@pulumi.output_type
class GetSerialPortResult:
    """
    Represents the serial port of the parent resource.
    """
    def __init__(__self__, id=None, name=None, state=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        Specifies whether the port is enabled for a serial console connection.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetSerialPortResult(GetSerialPortResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSerialPortResult(
            id=self.id,
            name=self.name,
            state=self.state,
            type=self.type)


def get_serial_port(parent_resource: Optional[str] = None,
                    parent_resource_type: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    resource_provider_namespace: Optional[str] = None,
                    serial_port: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSerialPortResult:
    """
    Gets the configured settings for a serial port
    API Version: 2018-05-01.


    :param str parent_resource: The resource name, or subordinate path, for the parent of the serial port. For example: the name of the virtual machine.
    :param str parent_resource_type: The resource type of the parent resource.  For example: 'virtualMachines' or 'virtualMachineScaleSets'
    :param str resource_group_name: The name of the resource group.
    :param str resource_provider_namespace: The namespace of the resource provider.
    :param str serial_port: The name of the serial port to connect to.
    """
    __args__ = dict()
    __args__['parentResource'] = parent_resource
    __args__['parentResourceType'] = parent_resource_type
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceProviderNamespace'] = resource_provider_namespace
    __args__['serialPort'] = serial_port
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:serialconsole:getSerialPort', __args__, opts=opts, typ=GetSerialPortResult).value

    return AwaitableGetSerialPortResult(
        id=__ret__.id,
        name=__ret__.name,
        state=__ret__.state,
        type=__ret__.type)


@_utilities.lift_output_func(get_serial_port)
def get_serial_port_output(parent_resource: Optional[pulumi.Input[str]] = None,
                           parent_resource_type: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           resource_provider_namespace: Optional[pulumi.Input[str]] = None,
                           serial_port: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSerialPortResult]:
    """
    Gets the configured settings for a serial port
    API Version: 2018-05-01.


    :param str parent_resource: The resource name, or subordinate path, for the parent of the serial port. For example: the name of the virtual machine.
    :param str parent_resource_type: The resource type of the parent resource.  For example: 'virtualMachines' or 'virtualMachineScaleSets'
    :param str resource_group_name: The name of the resource group.
    :param str resource_provider_namespace: The namespace of the resource provider.
    :param str serial_port: The name of the serial port to connect to.
    """
    ...
