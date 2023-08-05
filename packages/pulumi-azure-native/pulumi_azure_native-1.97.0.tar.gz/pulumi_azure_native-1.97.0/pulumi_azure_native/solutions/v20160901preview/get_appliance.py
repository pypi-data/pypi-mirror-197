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
    'GetApplianceResult',
    'AwaitableGetApplianceResult',
    'get_appliance',
    'get_appliance_output',
]

warnings.warn("""Version 2016-09-01-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetApplianceResult:
    """
    Information about appliance.
    """
    def __init__(__self__, appliance_definition_id=None, id=None, identity=None, kind=None, location=None, managed_by=None, managed_resource_group_id=None, name=None, outputs=None, parameters=None, plan=None, provisioning_state=None, sku=None, tags=None, type=None, ui_definition_uri=None):
        if appliance_definition_id and not isinstance(appliance_definition_id, str):
            raise TypeError("Expected argument 'appliance_definition_id' to be a str")
        pulumi.set(__self__, "appliance_definition_id", appliance_definition_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_by and not isinstance(managed_by, str):
            raise TypeError("Expected argument 'managed_by' to be a str")
        pulumi.set(__self__, "managed_by", managed_by)
        if managed_resource_group_id and not isinstance(managed_resource_group_id, str):
            raise TypeError("Expected argument 'managed_resource_group_id' to be a str")
        pulumi.set(__self__, "managed_resource_group_id", managed_resource_group_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if outputs and not isinstance(outputs, dict):
            raise TypeError("Expected argument 'outputs' to be a dict")
        pulumi.set(__self__, "outputs", outputs)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if plan and not isinstance(plan, dict):
            raise TypeError("Expected argument 'plan' to be a dict")
        pulumi.set(__self__, "plan", plan)
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
        if ui_definition_uri and not isinstance(ui_definition_uri, str):
            raise TypeError("Expected argument 'ui_definition_uri' to be a str")
        pulumi.set(__self__, "ui_definition_uri", ui_definition_uri)

    @property
    @pulumi.getter(name="applianceDefinitionId")
    def appliance_definition_id(self) -> Optional[str]:
        """
        The fully qualified path of appliance definition Id.
        """
        return pulumi.get(self, "appliance_definition_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        The kind of the appliance. Allowed values are MarketPlace and ServiceCatalog.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> Optional[str]:
        """
        ID of the resource that manages this resource.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter(name="managedResourceGroupId")
    def managed_resource_group_id(self) -> str:
        """
        The managed resource group Id.
        """
        return pulumi.get(self, "managed_resource_group_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def outputs(self) -> Any:
        """
        Name and value pairs that define the appliance outputs.
        """
        return pulumi.get(self, "outputs")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Any]:
        """
        Name and value pairs that define the appliance parameters. It can be a JObject or a well formed JSON string.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def plan(self) -> Optional['outputs.PlanResponse']:
        """
        The plan information.
        """
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The appliance provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The SKU of the resource.
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
    @pulumi.getter(name="uiDefinitionUri")
    def ui_definition_uri(self) -> Optional[str]:
        """
        The blob URI where the UI definition file is located.
        """
        return pulumi.get(self, "ui_definition_uri")


class AwaitableGetApplianceResult(GetApplianceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplianceResult(
            appliance_definition_id=self.appliance_definition_id,
            id=self.id,
            identity=self.identity,
            kind=self.kind,
            location=self.location,
            managed_by=self.managed_by,
            managed_resource_group_id=self.managed_resource_group_id,
            name=self.name,
            outputs=self.outputs,
            parameters=self.parameters,
            plan=self.plan,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            ui_definition_uri=self.ui_definition_uri)


def get_appliance(appliance_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplianceResult:
    """
    Gets the appliance.


    :param str appliance_name: The name of the appliance.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    pulumi.log.warn("""get_appliance is deprecated: Version 2016-09-01-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['applianceName'] = appliance_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:solutions/v20160901preview:getAppliance', __args__, opts=opts, typ=GetApplianceResult).value

    return AwaitableGetApplianceResult(
        appliance_definition_id=__ret__.appliance_definition_id,
        id=__ret__.id,
        identity=__ret__.identity,
        kind=__ret__.kind,
        location=__ret__.location,
        managed_by=__ret__.managed_by,
        managed_resource_group_id=__ret__.managed_resource_group_id,
        name=__ret__.name,
        outputs=__ret__.outputs,
        parameters=__ret__.parameters,
        plan=__ret__.plan,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        ui_definition_uri=__ret__.ui_definition_uri)


@_utilities.lift_output_func(get_appliance)
def get_appliance_output(appliance_name: Optional[pulumi.Input[str]] = None,
                         resource_group_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetApplianceResult]:
    """
    Gets the appliance.


    :param str appliance_name: The name of the appliance.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    pulumi.log.warn("""get_appliance is deprecated: Version 2016-09-01-preview will be removed in v2 of the provider.""")
    ...
