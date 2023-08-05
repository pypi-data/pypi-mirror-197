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
    'GetGalleryApplicationResult',
    'AwaitableGetGalleryApplicationResult',
    'get_gallery_application',
    'get_gallery_application_output',
]

@pulumi.output_type
class GetGalleryApplicationResult:
    """
    Specifies information about the gallery Application Definition that you want to create or update.
    """
    def __init__(__self__, description=None, end_of_life_date=None, eula=None, id=None, location=None, name=None, privacy_statement_uri=None, release_note_uri=None, supported_os_type=None, tags=None, type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if end_of_life_date and not isinstance(end_of_life_date, str):
            raise TypeError("Expected argument 'end_of_life_date' to be a str")
        pulumi.set(__self__, "end_of_life_date", end_of_life_date)
        if eula and not isinstance(eula, str):
            raise TypeError("Expected argument 'eula' to be a str")
        pulumi.set(__self__, "eula", eula)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if privacy_statement_uri and not isinstance(privacy_statement_uri, str):
            raise TypeError("Expected argument 'privacy_statement_uri' to be a str")
        pulumi.set(__self__, "privacy_statement_uri", privacy_statement_uri)
        if release_note_uri and not isinstance(release_note_uri, str):
            raise TypeError("Expected argument 'release_note_uri' to be a str")
        pulumi.set(__self__, "release_note_uri", release_note_uri)
        if supported_os_type and not isinstance(supported_os_type, str):
            raise TypeError("Expected argument 'supported_os_type' to be a str")
        pulumi.set(__self__, "supported_os_type", supported_os_type)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of this gallery Application Definition resource. This property is updatable.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="endOfLifeDate")
    def end_of_life_date(self) -> Optional[str]:
        """
        The end of life date of the gallery Application Definition. This property can be used for decommissioning purposes. This property is updatable.
        """
        return pulumi.get(self, "end_of_life_date")

    @property
    @pulumi.getter
    def eula(self) -> Optional[str]:
        """
        The Eula agreement for the gallery Application Definition.
        """
        return pulumi.get(self, "eula")

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
    @pulumi.getter(name="privacyStatementUri")
    def privacy_statement_uri(self) -> Optional[str]:
        """
        The privacy statement uri.
        """
        return pulumi.get(self, "privacy_statement_uri")

    @property
    @pulumi.getter(name="releaseNoteUri")
    def release_note_uri(self) -> Optional[str]:
        """
        The release note uri.
        """
        return pulumi.get(self, "release_note_uri")

    @property
    @pulumi.getter(name="supportedOSType")
    def supported_os_type(self) -> str:
        """
        This property allows you to specify the supported type of the OS that application is built for. <br><br> Possible values are: <br><br> **Windows** <br><br> **Linux**
        """
        return pulumi.get(self, "supported_os_type")

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


class AwaitableGetGalleryApplicationResult(GetGalleryApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGalleryApplicationResult(
            description=self.description,
            end_of_life_date=self.end_of_life_date,
            eula=self.eula,
            id=self.id,
            location=self.location,
            name=self.name,
            privacy_statement_uri=self.privacy_statement_uri,
            release_note_uri=self.release_note_uri,
            supported_os_type=self.supported_os_type,
            tags=self.tags,
            type=self.type)


def get_gallery_application(gallery_application_name: Optional[str] = None,
                            gallery_name: Optional[str] = None,
                            resource_group_name: Optional[str] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGalleryApplicationResult:
    """
    Retrieves information about a gallery Application Definition.


    :param str gallery_application_name: The name of the gallery Application Definition to be retrieved.
    :param str gallery_name: The name of the Shared Application Gallery from which the Application Definitions are to be retrieved.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['galleryApplicationName'] = gallery_application_name
    __args__['galleryName'] = gallery_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20210701:getGalleryApplication', __args__, opts=opts, typ=GetGalleryApplicationResult).value

    return AwaitableGetGalleryApplicationResult(
        description=__ret__.description,
        end_of_life_date=__ret__.end_of_life_date,
        eula=__ret__.eula,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        privacy_statement_uri=__ret__.privacy_statement_uri,
        release_note_uri=__ret__.release_note_uri,
        supported_os_type=__ret__.supported_os_type,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_gallery_application)
def get_gallery_application_output(gallery_application_name: Optional[pulumi.Input[str]] = None,
                                   gallery_name: Optional[pulumi.Input[str]] = None,
                                   resource_group_name: Optional[pulumi.Input[str]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGalleryApplicationResult]:
    """
    Retrieves information about a gallery Application Definition.


    :param str gallery_application_name: The name of the gallery Application Definition to be retrieved.
    :param str gallery_name: The name of the Shared Application Gallery from which the Application Definitions are to be retrieved.
    :param str resource_group_name: The name of the resource group.
    """
    ...
