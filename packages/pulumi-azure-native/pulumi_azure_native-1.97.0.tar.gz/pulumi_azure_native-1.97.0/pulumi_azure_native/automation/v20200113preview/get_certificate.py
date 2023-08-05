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
    'GetCertificateResult',
    'AwaitableGetCertificateResult',
    'get_certificate',
    'get_certificate_output',
]

@pulumi.output_type
class GetCertificateResult:
    """
    Definition of the certificate.
    """
    def __init__(__self__, creation_time=None, description=None, expiry_time=None, id=None, is_exportable=None, last_modified_time=None, name=None, thumbprint=None, type=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if expiry_time and not isinstance(expiry_time, str):
            raise TypeError("Expected argument 'expiry_time' to be a str")
        pulumi.set(__self__, "expiry_time", expiry_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_exportable and not isinstance(is_exportable, bool):
            raise TypeError("Expected argument 'is_exportable' to be a bool")
        pulumi.set(__self__, "is_exportable", is_exportable)
        if last_modified_time and not isinstance(last_modified_time, str):
            raise TypeError("Expected argument 'last_modified_time' to be a str")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if thumbprint and not isinstance(thumbprint, str):
            raise TypeError("Expected argument 'thumbprint' to be a str")
        pulumi.set(__self__, "thumbprint", thumbprint)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Gets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="expiryTime")
    def expiry_time(self) -> str:
        """
        Gets the expiry time of the certificate.
        """
        return pulumi.get(self, "expiry_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isExportable")
    def is_exportable(self) -> bool:
        """
        Gets the is exportable flag of the certificate.
        """
        return pulumi.get(self, "is_exportable")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> str:
        """
        Gets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def thumbprint(self) -> str:
        """
        Gets the thumbprint of the certificate.
        """
        return pulumi.get(self, "thumbprint")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetCertificateResult(GetCertificateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCertificateResult(
            creation_time=self.creation_time,
            description=self.description,
            expiry_time=self.expiry_time,
            id=self.id,
            is_exportable=self.is_exportable,
            last_modified_time=self.last_modified_time,
            name=self.name,
            thumbprint=self.thumbprint,
            type=self.type)


def get_certificate(automation_account_name: Optional[str] = None,
                    certificate_name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCertificateResult:
    """
    Retrieve the certificate identified by certificate name.


    :param str automation_account_name: The name of the automation account.
    :param str certificate_name: The name of certificate.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    __args__ = dict()
    __args__['automationAccountName'] = automation_account_name
    __args__['certificateName'] = certificate_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:automation/v20200113preview:getCertificate', __args__, opts=opts, typ=GetCertificateResult).value

    return AwaitableGetCertificateResult(
        creation_time=__ret__.creation_time,
        description=__ret__.description,
        expiry_time=__ret__.expiry_time,
        id=__ret__.id,
        is_exportable=__ret__.is_exportable,
        last_modified_time=__ret__.last_modified_time,
        name=__ret__.name,
        thumbprint=__ret__.thumbprint,
        type=__ret__.type)


@_utilities.lift_output_func(get_certificate)
def get_certificate_output(automation_account_name: Optional[pulumi.Input[str]] = None,
                           certificate_name: Optional[pulumi.Input[str]] = None,
                           resource_group_name: Optional[pulumi.Input[str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCertificateResult]:
    """
    Retrieve the certificate identified by certificate name.


    :param str automation_account_name: The name of the automation account.
    :param str certificate_name: The name of certificate.
    :param str resource_group_name: Name of an Azure Resource group.
    """
    ...
