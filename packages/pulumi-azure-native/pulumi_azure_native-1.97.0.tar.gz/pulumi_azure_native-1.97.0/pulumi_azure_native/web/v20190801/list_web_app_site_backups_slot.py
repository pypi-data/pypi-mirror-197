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
    'ListWebAppSiteBackupsSlotResult',
    'AwaitableListWebAppSiteBackupsSlotResult',
    'list_web_app_site_backups_slot',
    'list_web_app_site_backups_slot_output',
]

@pulumi.output_type
class ListWebAppSiteBackupsSlotResult:
    """
    Collection of backup items.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> str:
        """
        Link to next page of resources.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Sequence['outputs.BackupItemResponse']:
        """
        Collection of resources.
        """
        return pulumi.get(self, "value")


class AwaitableListWebAppSiteBackupsSlotResult(ListWebAppSiteBackupsSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppSiteBackupsSlotResult(
            next_link=self.next_link,
            value=self.value)


def list_web_app_site_backups_slot(name: Optional[str] = None,
                                   resource_group_name: Optional[str] = None,
                                   slot: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppSiteBackupsSlotResult:
    """
    Gets existing backups of an app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get backups of the production slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20190801:listWebAppSiteBackupsSlot', __args__, opts=opts, typ=ListWebAppSiteBackupsSlotResult).value

    return AwaitableListWebAppSiteBackupsSlotResult(
        next_link=__ret__.next_link,
        value=__ret__.value)


@_utilities.lift_output_func(list_web_app_site_backups_slot)
def list_web_app_site_backups_slot_output(name: Optional[pulumi.Input[str]] = None,
                                          resource_group_name: Optional[pulumi.Input[str]] = None,
                                          slot: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListWebAppSiteBackupsSlotResult]:
    """
    Gets existing backups of an app.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot. If a slot is not specified, the API will get backups of the production slot.
    """
    ...
