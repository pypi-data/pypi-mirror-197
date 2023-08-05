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
    'GetVirtualMachineScaleSetResult',
    'AwaitableGetVirtualMachineScaleSetResult',
    'get_virtual_machine_scale_set',
    'get_virtual_machine_scale_set_output',
]

warnings.warn("""Version 2015-06-15 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetVirtualMachineScaleSetResult:
    """
    Describes a Virtual Machine Scale Set.
    """
    def __init__(__self__, id=None, location=None, name=None, over_provision=None, provisioning_state=None, sku=None, tags=None, type=None, upgrade_policy=None, virtual_machine_profile=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if over_provision and not isinstance(over_provision, bool):
            raise TypeError("Expected argument 'over_provision' to be a bool")
        pulumi.set(__self__, "over_provision", over_provision)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if upgrade_policy and not isinstance(upgrade_policy, dict):
            raise TypeError("Expected argument 'upgrade_policy' to be a dict")
        pulumi.set(__self__, "upgrade_policy", upgrade_policy)
        if virtual_machine_profile and not isinstance(virtual_machine_profile, dict):
            raise TypeError("Expected argument 'virtual_machine_profile' to be a dict")
        pulumi.set(__self__, "virtual_machine_profile", virtual_machine_profile)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="overProvision")
    def over_provision(self) -> Optional[bool]:
        """
        Specifies whether the Virtual Machine Scale Set should be overprovisioned.
        """
        return pulumi.get(self, "over_provision")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The virtual machine scale set sku.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="upgradePolicy")
    def upgrade_policy(self) -> Optional['outputs.UpgradePolicyResponse']:
        """
        The upgrade policy.
        """
        return pulumi.get(self, "upgrade_policy")

    @property
    @pulumi.getter(name="virtualMachineProfile")
    def virtual_machine_profile(self) -> Optional['outputs.VirtualMachineScaleSetVMProfileResponse']:
        """
        The virtual machine profile.
        """
        return pulumi.get(self, "virtual_machine_profile")


class AwaitableGetVirtualMachineScaleSetResult(GetVirtualMachineScaleSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualMachineScaleSetResult(
            id=self.id,
            location=self.location,
            name=self.name,
            over_provision=self.over_provision,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            upgrade_policy=self.upgrade_policy,
            virtual_machine_profile=self.virtual_machine_profile)


def get_virtual_machine_scale_set(resource_group_name: Optional[str] = None,
                                  vm_scale_set_name: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualMachineScaleSetResult:
    """
    Display information about a virtual machine scale set.


    :param str resource_group_name: The name of the resource group.
    :param str vm_scale_set_name: The name of the VM scale set.
    """
    pulumi.log.warn("""get_virtual_machine_scale_set is deprecated: Version 2015-06-15 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['vmScaleSetName'] = vm_scale_set_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20150615:getVirtualMachineScaleSet', __args__, opts=opts, typ=GetVirtualMachineScaleSetResult).value

    return AwaitableGetVirtualMachineScaleSetResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        over_provision=__ret__.over_provision,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        upgrade_policy=__ret__.upgrade_policy,
        virtual_machine_profile=__ret__.virtual_machine_profile)


@_utilities.lift_output_func(get_virtual_machine_scale_set)
def get_virtual_machine_scale_set_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                         vm_scale_set_name: Optional[pulumi.Input[str]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualMachineScaleSetResult]:
    """
    Display information about a virtual machine scale set.


    :param str resource_group_name: The name of the resource group.
    :param str vm_scale_set_name: The name of the VM scale set.
    """
    pulumi.log.warn("""get_virtual_machine_scale_set is deprecated: Version 2015-06-15 will be removed in v2 of the provider.""")
    ...
