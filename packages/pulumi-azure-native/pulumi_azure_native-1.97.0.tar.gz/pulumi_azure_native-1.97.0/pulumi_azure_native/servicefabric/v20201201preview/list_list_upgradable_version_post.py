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
    'ListListUpgradableVersionPostResult',
    'AwaitableListListUpgradableVersionPostResult',
    'list_list_upgradable_version_post',
    'list_list_upgradable_version_post_output',
]

@pulumi.output_type
class ListListUpgradableVersionPostResult:
    """
    The list of intermediate cluster code versions for an upgrade or downgrade. Or minimum and maximum upgradable version if no target was given
    """
    def __init__(__self__, supported_path=None):
        if supported_path and not isinstance(supported_path, list):
            raise TypeError("Expected argument 'supported_path' to be a list")
        pulumi.set(__self__, "supported_path", supported_path)

    @property
    @pulumi.getter(name="supportedPath")
    def supported_path(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "supported_path")


class AwaitableListListUpgradableVersionPostResult(ListListUpgradableVersionPostResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListListUpgradableVersionPostResult(
            supported_path=self.supported_path)


def list_list_upgradable_version_post(cluster_name: Optional[str] = None,
                                      resource_group_name: Optional[str] = None,
                                      target_version: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListListUpgradableVersionPostResult:
    """
    If a target is not provided, it will get the minimum and maximum versions available from the current cluster version. If a target is given, it will provide the required path to get from the current cluster version to the target version.


    :param str cluster_name: The name of the cluster resource.
    :param str resource_group_name: The name of the resource group.
    :param str target_version: The target code version.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['targetVersion'] = target_version
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:servicefabric/v20201201preview:listListUpgradableVersionPost', __args__, opts=opts, typ=ListListUpgradableVersionPostResult).value

    return AwaitableListListUpgradableVersionPostResult(
        supported_path=__ret__.supported_path)


@_utilities.lift_output_func(list_list_upgradable_version_post)
def list_list_upgradable_version_post_output(cluster_name: Optional[pulumi.Input[str]] = None,
                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                             target_version: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListListUpgradableVersionPostResult]:
    """
    If a target is not provided, it will get the minimum and maximum versions available from the current cluster version. If a target is given, it will provide the required path to get from the current cluster version to the target version.


    :param str cluster_name: The name of the cluster resource.
    :param str resource_group_name: The name of the resource group.
    :param str target_version: The target code version.
    """
    ...
