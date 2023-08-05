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
    'GetSimResult',
    'AwaitableGetSimResult',
    'get_sim',
    'get_sim_output',
]

@pulumi.output_type
class GetSimResult:
    """
    SIM resource.
    """
    def __init__(__self__, device_type=None, id=None, integrated_circuit_card_identifier=None, international_mobile_subscriber_identity=None, name=None, provisioning_state=None, sim_policy=None, sim_state=None, site_provisioning_state=None, static_ip_configuration=None, system_data=None, type=None, vendor_key_fingerprint=None, vendor_name=None):
        if device_type and not isinstance(device_type, str):
            raise TypeError("Expected argument 'device_type' to be a str")
        pulumi.set(__self__, "device_type", device_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if integrated_circuit_card_identifier and not isinstance(integrated_circuit_card_identifier, str):
            raise TypeError("Expected argument 'integrated_circuit_card_identifier' to be a str")
        pulumi.set(__self__, "integrated_circuit_card_identifier", integrated_circuit_card_identifier)
        if international_mobile_subscriber_identity and not isinstance(international_mobile_subscriber_identity, str):
            raise TypeError("Expected argument 'international_mobile_subscriber_identity' to be a str")
        pulumi.set(__self__, "international_mobile_subscriber_identity", international_mobile_subscriber_identity)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sim_policy and not isinstance(sim_policy, dict):
            raise TypeError("Expected argument 'sim_policy' to be a dict")
        pulumi.set(__self__, "sim_policy", sim_policy)
        if sim_state and not isinstance(sim_state, str):
            raise TypeError("Expected argument 'sim_state' to be a str")
        pulumi.set(__self__, "sim_state", sim_state)
        if site_provisioning_state and not isinstance(site_provisioning_state, dict):
            raise TypeError("Expected argument 'site_provisioning_state' to be a dict")
        pulumi.set(__self__, "site_provisioning_state", site_provisioning_state)
        if static_ip_configuration and not isinstance(static_ip_configuration, list):
            raise TypeError("Expected argument 'static_ip_configuration' to be a list")
        pulumi.set(__self__, "static_ip_configuration", static_ip_configuration)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vendor_key_fingerprint and not isinstance(vendor_key_fingerprint, str):
            raise TypeError("Expected argument 'vendor_key_fingerprint' to be a str")
        pulumi.set(__self__, "vendor_key_fingerprint", vendor_key_fingerprint)
        if vendor_name and not isinstance(vendor_name, str):
            raise TypeError("Expected argument 'vendor_name' to be a str")
        pulumi.set(__self__, "vendor_name", vendor_name)

    @property
    @pulumi.getter(name="deviceType")
    def device_type(self) -> Optional[str]:
        """
        An optional free-form text field that can be used to record the device type this SIM is associated with, for example 'Video camera'. The Azure portal allows SIMs to be grouped and filtered based on this value.
        """
        return pulumi.get(self, "device_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="integratedCircuitCardIdentifier")
    def integrated_circuit_card_identifier(self) -> Optional[str]:
        """
        The integrated circuit card ID (ICCID) for the SIM.
        """
        return pulumi.get(self, "integrated_circuit_card_identifier")

    @property
    @pulumi.getter(name="internationalMobileSubscriberIdentity")
    def international_mobile_subscriber_identity(self) -> str:
        """
        The international mobile subscriber identity (IMSI) for the SIM.
        """
        return pulumi.get(self, "international_mobile_subscriber_identity")

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
        The provisioning state of the SIM resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="simPolicy")
    def sim_policy(self) -> Optional['outputs.SimPolicyResourceIdResponse']:
        """
        The SIM policy used by this SIM. The SIM policy must be in the same location as the SIM.
        """
        return pulumi.get(self, "sim_policy")

    @property
    @pulumi.getter(name="simState")
    def sim_state(self) -> str:
        """
        The state of the SIM resource.
        """
        return pulumi.get(self, "sim_state")

    @property
    @pulumi.getter(name="siteProvisioningState")
    def site_provisioning_state(self) -> Mapping[str, str]:
        """
        A dictionary of sites to the provisioning state of this SIM on that site.
        """
        return pulumi.get(self, "site_provisioning_state")

    @property
    @pulumi.getter(name="staticIpConfiguration")
    def static_ip_configuration(self) -> Optional[Sequence['outputs.SimStaticIpPropertiesResponse']]:
        """
        A list of static IP addresses assigned to this SIM. Each address is assigned at a defined network scope, made up of {attached data network, slice}.
        """
        return pulumi.get(self, "static_ip_configuration")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vendorKeyFingerprint")
    def vendor_key_fingerprint(self) -> str:
        """
        The public key fingerprint of the SIM vendor who provided this SIM, if any.
        """
        return pulumi.get(self, "vendor_key_fingerprint")

    @property
    @pulumi.getter(name="vendorName")
    def vendor_name(self) -> str:
        """
        The name of the SIM vendor who provided this SIM, if any.
        """
        return pulumi.get(self, "vendor_name")


class AwaitableGetSimResult(GetSimResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSimResult(
            device_type=self.device_type,
            id=self.id,
            integrated_circuit_card_identifier=self.integrated_circuit_card_identifier,
            international_mobile_subscriber_identity=self.international_mobile_subscriber_identity,
            name=self.name,
            provisioning_state=self.provisioning_state,
            sim_policy=self.sim_policy,
            sim_state=self.sim_state,
            site_provisioning_state=self.site_provisioning_state,
            static_ip_configuration=self.static_ip_configuration,
            system_data=self.system_data,
            type=self.type,
            vendor_key_fingerprint=self.vendor_key_fingerprint,
            vendor_name=self.vendor_name)


def get_sim(resource_group_name: Optional[str] = None,
            sim_group_name: Optional[str] = None,
            sim_name: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSimResult:
    """
    Gets information about the specified SIM.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sim_group_name: The name of the SIM Group.
    :param str sim_name: The name of the SIM.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['simGroupName'] = sim_group_name
    __args__['simName'] = sim_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:mobilenetwork/v20221101:getSim', __args__, opts=opts, typ=GetSimResult).value

    return AwaitableGetSimResult(
        device_type=__ret__.device_type,
        id=__ret__.id,
        integrated_circuit_card_identifier=__ret__.integrated_circuit_card_identifier,
        international_mobile_subscriber_identity=__ret__.international_mobile_subscriber_identity,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        sim_policy=__ret__.sim_policy,
        sim_state=__ret__.sim_state,
        site_provisioning_state=__ret__.site_provisioning_state,
        static_ip_configuration=__ret__.static_ip_configuration,
        system_data=__ret__.system_data,
        type=__ret__.type,
        vendor_key_fingerprint=__ret__.vendor_key_fingerprint,
        vendor_name=__ret__.vendor_name)


@_utilities.lift_output_func(get_sim)
def get_sim_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                   sim_group_name: Optional[pulumi.Input[str]] = None,
                   sim_name: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSimResult]:
    """
    Gets information about the specified SIM.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str sim_group_name: The name of the SIM Group.
    :param str sim_name: The name of the SIM.
    """
    ...
