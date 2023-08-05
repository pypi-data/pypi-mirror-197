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
    'GetVolumeGroupResult',
    'AwaitableGetVolumeGroupResult',
    'get_volume_group',
    'get_volume_group_output',
]

@pulumi.output_type
class GetVolumeGroupResult:
    """
    Response for Volume Group request.
    """
    def __init__(__self__, encryption=None, id=None, name=None, network_acls=None, protocol_type=None, provisioning_state=None, system_data=None, tags=None, type=None):
        if encryption and not isinstance(encryption, str):
            raise TypeError("Expected argument 'encryption' to be a str")
        pulumi.set(__self__, "encryption", encryption)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_acls and not isinstance(network_acls, dict):
            raise TypeError("Expected argument 'network_acls' to be a dict")
        pulumi.set(__self__, "network_acls", network_acls)
        if protocol_type and not isinstance(protocol_type, str):
            raise TypeError("Expected argument 'protocol_type' to be a str")
        pulumi.set(__self__, "protocol_type", protocol_type)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def encryption(self) -> Optional[str]:
        """
        Type of encryption
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkAcls")
    def network_acls(self) -> Optional['outputs.NetworkRuleSetResponse']:
        """
        A collection of rules governing the accessibility from specific network locations.
        """
        return pulumi.get(self, "network_acls")

    @property
    @pulumi.getter(name="protocolType")
    def protocol_type(self) -> Optional[str]:
        """
        Type of storage target
        """
        return pulumi.get(self, "protocol_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        State of the operation on the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Resource metadata required by ARM RPC
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Azure resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetVolumeGroupResult(GetVolumeGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVolumeGroupResult(
            encryption=self.encryption,
            id=self.id,
            name=self.name,
            network_acls=self.network_acls,
            protocol_type=self.protocol_type,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type)


def get_volume_group(elastic_san_name: Optional[str] = None,
                     resource_group_name: Optional[str] = None,
                     volume_group_name: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVolumeGroupResult:
    """
    Get an VolumeGroups.
    API Version: 2021-11-20-preview.


    :param str elastic_san_name: The name of the ElasticSan.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str volume_group_name: The name of the VolumeGroup.
    """
    __args__ = dict()
    __args__['elasticSanName'] = elastic_san_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['volumeGroupName'] = volume_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:elasticsan:getVolumeGroup', __args__, opts=opts, typ=GetVolumeGroupResult).value

    return AwaitableGetVolumeGroupResult(
        encryption=__ret__.encryption,
        id=__ret__.id,
        name=__ret__.name,
        network_acls=__ret__.network_acls,
        protocol_type=__ret__.protocol_type,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_volume_group)
def get_volume_group_output(elastic_san_name: Optional[pulumi.Input[str]] = None,
                            resource_group_name: Optional[pulumi.Input[str]] = None,
                            volume_group_name: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVolumeGroupResult]:
    """
    Get an VolumeGroups.
    API Version: 2021-11-20-preview.


    :param str elastic_san_name: The name of the ElasticSan.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str volume_group_name: The name of the VolumeGroup.
    """
    ...
