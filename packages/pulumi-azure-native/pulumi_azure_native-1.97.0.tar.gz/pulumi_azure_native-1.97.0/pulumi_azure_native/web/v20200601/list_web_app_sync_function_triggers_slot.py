# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListWebAppSyncFunctionTriggersSlotResult',
    'AwaitableListWebAppSyncFunctionTriggersSlotResult',
    'list_web_app_sync_function_triggers_slot',
    'list_web_app_sync_function_triggers_slot_output',
]

@pulumi.output_type
class ListWebAppSyncFunctionTriggersSlotResult:
    """
    Function secrets.
    """
    def __init__(__self__, key=None, trigger_url=None):
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if trigger_url and not isinstance(trigger_url, str):
            raise TypeError("Expected argument 'trigger_url' to be a str")
        pulumi.set(__self__, "trigger_url", trigger_url)

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        """
        Secret key.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="triggerUrl")
    def trigger_url(self) -> Optional[str]:
        """
        Trigger URL.
        """
        return pulumi.get(self, "trigger_url")


class AwaitableListWebAppSyncFunctionTriggersSlotResult(ListWebAppSyncFunctionTriggersSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppSyncFunctionTriggersSlotResult(
            key=self.key,
            trigger_url=self.trigger_url)


def list_web_app_sync_function_triggers_slot(name: Optional[str] = None,
                                             resource_group_name: Optional[str] = None,
                                             slot: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppSyncFunctionTriggersSlotResult:
    """
    This is to allow calling via powershell and ARM template.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20200601:listWebAppSyncFunctionTriggersSlot', __args__, opts=opts, typ=ListWebAppSyncFunctionTriggersSlotResult).value

    return AwaitableListWebAppSyncFunctionTriggersSlotResult(
        key=__ret__.key,
        trigger_url=__ret__.trigger_url)


@_utilities.lift_output_func(list_web_app_sync_function_triggers_slot)
def list_web_app_sync_function_triggers_slot_output(name: Optional[pulumi.Input[str]] = None,
                                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                                    slot: Optional[pulumi.Input[str]] = None,
                                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListWebAppSyncFunctionTriggersSlotResult]:
    """
    This is to allow calling via powershell and ARM template.


    :param str name: Name of the app.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: Name of the deployment slot.
    """
    ...
