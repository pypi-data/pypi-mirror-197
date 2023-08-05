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
    'GetSpatialAnchorsAccountResult',
    'AwaitableGetSpatialAnchorsAccountResult',
    'get_spatial_anchors_account',
    'get_spatial_anchors_account_output',
]

warnings.warn("""Version 2019-12-02-preview will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetSpatialAnchorsAccountResult:
    """
    SpatialAnchorsAccount Response.
    """
    def __init__(__self__, account_domain=None, account_id=None, id=None, identity=None, location=None, name=None, tags=None, type=None):
        if account_domain and not isinstance(account_domain, str):
            raise TypeError("Expected argument 'account_domain' to be a str")
        pulumi.set(__self__, "account_domain", account_domain)
        if account_id and not isinstance(account_id, str):
            raise TypeError("Expected argument 'account_id' to be a str")
        pulumi.set(__self__, "account_id", account_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accountDomain")
    def account_domain(self) -> str:
        """
        Correspond domain name of certain Spatial Anchors Account
        """
        return pulumi.get(self, "account_domain")

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> str:
        """
        unique id of certain account.
        """
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity associated with this account
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSpatialAnchorsAccountResult(GetSpatialAnchorsAccountResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSpatialAnchorsAccountResult(
            account_domain=self.account_domain,
            account_id=self.account_id,
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            tags=self.tags,
            type=self.type)


def get_spatial_anchors_account(account_name: Optional[str] = None,
                                resource_group_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSpatialAnchorsAccountResult:
    """
    Retrieve a Spatial Anchors Account.


    :param str account_name: Name of an Mixed Reality Account.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_spatial_anchors_account is deprecated: Version 2019-12-02-preview will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:mixedreality/v20191202preview:getSpatialAnchorsAccount', __args__, opts=opts, typ=GetSpatialAnchorsAccountResult).value

    return AwaitableGetSpatialAnchorsAccountResult(
        account_domain=__ret__.account_domain,
        account_id=__ret__.account_id,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_spatial_anchors_account)
def get_spatial_anchors_account_output(account_name: Optional[pulumi.Input[str]] = None,
                                       resource_group_name: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSpatialAnchorsAccountResult]:
    """
    Retrieve a Spatial Anchors Account.


    :param str account_name: Name of an Mixed Reality Account.
    :param str resource_group_name: Name of an Azure resource group.
    """
    pulumi.log.warn("""get_spatial_anchors_account is deprecated: Version 2019-12-02-preview will be removed in v2 of the provider.""")
    ...
