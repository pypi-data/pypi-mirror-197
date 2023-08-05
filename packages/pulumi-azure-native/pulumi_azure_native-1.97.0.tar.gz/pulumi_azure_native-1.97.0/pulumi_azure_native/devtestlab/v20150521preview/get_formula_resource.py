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
    'GetFormulaResourceResult',
    'AwaitableGetFormulaResourceResult',
    'get_formula_resource',
    'get_formula_resource_output',
]

warnings.warn("""Version 2015-05-21-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetFormulaResourceResult:
    """
    A formula.
    """
    def __init__(__self__, author=None, creation_date=None, description=None, formula_content=None, id=None, location=None, name=None, os_type=None, provisioning_state=None, tags=None, type=None, vm=None):
        if author and not isinstance(author, str):
            raise TypeError("Expected argument 'author' to be a str")
        pulumi.set(__self__, "author", author)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if formula_content and not isinstance(formula_content, dict):
            raise TypeError("Expected argument 'formula_content' to be a dict")
        pulumi.set(__self__, "formula_content", formula_content)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vm and not isinstance(vm, dict):
            raise TypeError("Expected argument 'vm' to be a dict")
        pulumi.set(__self__, "vm", vm)

    @property
    @pulumi.getter
    def author(self) -> Optional[str]:
        """
        The author of the formula.
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> Optional[str]:
        """
        The creation date of the formula.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the formula.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="formulaContent")
    def formula_content(self) -> Optional['outputs.LabVirtualMachineResponse']:
        """
        The content of the formula.
        """
        return pulumi.get(self, "formula_content")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[str]:
        """
        The OS type of the formula.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def vm(self) -> Optional['outputs.FormulaPropertiesFromVmResponse']:
        """
        Information about a VM from which a formula is to be created.
        """
        return pulumi.get(self, "vm")


class AwaitableGetFormulaResourceResult(GetFormulaResourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFormulaResourceResult(
            author=self.author,
            creation_date=self.creation_date,
            description=self.description,
            formula_content=self.formula_content,
            id=self.id,
            location=self.location,
            name=self.name,
            os_type=self.os_type,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type,
            vm=self.vm)


def get_formula_resource(lab_name: Optional[str] = None,
                         name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFormulaResourceResult:
    """
    Get formula.


    :param str lab_name: The name of the lab.
    :param str name: The name of the formula.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_formula_resource is deprecated: Version 2015-05-21-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:devtestlab/v20150521preview:getFormulaResource', __args__, opts=opts, typ=GetFormulaResourceResult).value

    return AwaitableGetFormulaResourceResult(
        author=__ret__.author,
        creation_date=__ret__.creation_date,
        description=__ret__.description,
        formula_content=__ret__.formula_content,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        os_type=__ret__.os_type,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type,
        vm=__ret__.vm)


@_utilities.lift_output_func(get_formula_resource)
def get_formula_resource_output(lab_name: Optional[pulumi.Input[str]] = None,
                                name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFormulaResourceResult]:
    """
    Get formula.


    :param str lab_name: The name of the lab.
    :param str name: The name of the formula.
    :param str resource_group_name: The name of the resource group.
    """
    pulumi.log.warn("""get_formula_resource is deprecated: Version 2015-05-21-preview will be removed in v2 of the provider.""")
    ...
