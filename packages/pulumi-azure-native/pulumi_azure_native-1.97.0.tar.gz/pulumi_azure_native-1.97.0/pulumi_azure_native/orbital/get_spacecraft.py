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
    'GetSpacecraftResult',
    'AwaitableGetSpacecraftResult',
    'get_spacecraft',
    'get_spacecraft_output',
]

@pulumi.output_type
class GetSpacecraftResult:
    """
    Customer creates a spacecraft resource to schedule a contact.
    """
    def __init__(__self__, authorization_status=None, authorization_status_extended=None, etag=None, id=None, links=None, location=None, name=None, norad_id=None, system_data=None, tags=None, title_line=None, tle_line1=None, tle_line2=None, type=None):
        if authorization_status and not isinstance(authorization_status, str):
            raise TypeError("Expected argument 'authorization_status' to be a str")
        pulumi.set(__self__, "authorization_status", authorization_status)
        if authorization_status_extended and not isinstance(authorization_status_extended, str):
            raise TypeError("Expected argument 'authorization_status_extended' to be a str")
        pulumi.set(__self__, "authorization_status_extended", authorization_status_extended)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if links and not isinstance(links, list):
            raise TypeError("Expected argument 'links' to be a list")
        pulumi.set(__self__, "links", links)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if norad_id and not isinstance(norad_id, str):
            raise TypeError("Expected argument 'norad_id' to be a str")
        pulumi.set(__self__, "norad_id", norad_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if title_line and not isinstance(title_line, str):
            raise TypeError("Expected argument 'title_line' to be a str")
        pulumi.set(__self__, "title_line", title_line)
        if tle_line1 and not isinstance(tle_line1, str):
            raise TypeError("Expected argument 'tle_line1' to be a str")
        pulumi.set(__self__, "tle_line1", tle_line1)
        if tle_line2 and not isinstance(tle_line2, str):
            raise TypeError("Expected argument 'tle_line2' to be a str")
        pulumi.set(__self__, "tle_line2", tle_line2)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="authorizationStatus")
    def authorization_status(self) -> str:
        """
        Authorization status of spacecraft.
        """
        return pulumi.get(self, "authorization_status")

    @property
    @pulumi.getter(name="authorizationStatusExtended")
    def authorization_status_extended(self) -> str:
        """
        Details of the authorization status.
        """
        return pulumi.get(self, "authorization_status_extended")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def links(self) -> Optional[Sequence['outputs.SpacecraftLinkResponse']]:
        """
        Links of the Spacecraft
        """
        return pulumi.get(self, "links")

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
    @pulumi.getter(name="noradId")
    def norad_id(self) -> str:
        """
        NORAD ID of the spacecraft.
        """
        return pulumi.get(self, "norad_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="titleLine")
    def title_line(self) -> Optional[str]:
        """
        Title line of Two Line Element (TLE).
        """
        return pulumi.get(self, "title_line")

    @property
    @pulumi.getter(name="tleLine1")
    def tle_line1(self) -> Optional[str]:
        """
        Line 1 of Two Line Element (TLE).
        """
        return pulumi.get(self, "tle_line1")

    @property
    @pulumi.getter(name="tleLine2")
    def tle_line2(self) -> Optional[str]:
        """
        Line 2 of Two Line Element (TLE).
        """
        return pulumi.get(self, "tle_line2")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetSpacecraftResult(GetSpacecraftResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSpacecraftResult(
            authorization_status=self.authorization_status,
            authorization_status_extended=self.authorization_status_extended,
            etag=self.etag,
            id=self.id,
            links=self.links,
            location=self.location,
            name=self.name,
            norad_id=self.norad_id,
            system_data=self.system_data,
            tags=self.tags,
            title_line=self.title_line,
            tle_line1=self.tle_line1,
            tle_line2=self.tle_line2,
            type=self.type)


def get_spacecraft(resource_group_name: Optional[str] = None,
                   spacecraft_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSpacecraftResult:
    """
    Gets the specified spacecraft in a specified resource group
    API Version: 2021-04-04-preview.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str spacecraft_name: Spacecraft ID
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['spacecraftName'] = spacecraft_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:orbital:getSpacecraft', __args__, opts=opts, typ=GetSpacecraftResult).value

    return AwaitableGetSpacecraftResult(
        authorization_status=__ret__.authorization_status,
        authorization_status_extended=__ret__.authorization_status_extended,
        etag=__ret__.etag,
        id=__ret__.id,
        links=__ret__.links,
        location=__ret__.location,
        name=__ret__.name,
        norad_id=__ret__.norad_id,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        title_line=__ret__.title_line,
        tle_line1=__ret__.tle_line1,
        tle_line2=__ret__.tle_line2,
        type=__ret__.type)


@_utilities.lift_output_func(get_spacecraft)
def get_spacecraft_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                          spacecraft_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSpacecraftResult]:
    """
    Gets the specified spacecraft in a specified resource group
    API Version: 2021-04-04-preview.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str spacecraft_name: Spacecraft ID
    """
    ...
