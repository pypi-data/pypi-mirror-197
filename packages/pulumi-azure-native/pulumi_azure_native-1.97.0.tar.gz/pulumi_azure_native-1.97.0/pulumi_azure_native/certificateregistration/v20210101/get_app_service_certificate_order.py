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
    'GetAppServiceCertificateOrderResult',
    'AwaitableGetAppServiceCertificateOrderResult',
    'get_app_service_certificate_order',
    'get_app_service_certificate_order_output',
]

@pulumi.output_type
class GetAppServiceCertificateOrderResult:
    """
    SSL certificate purchase order.
    """
    def __init__(__self__, app_service_certificate_not_renewable_reasons=None, auto_renew=None, certificates=None, contact=None, csr=None, distinguished_name=None, domain_verification_token=None, expiration_time=None, id=None, intermediate=None, is_private_key_external=None, key_size=None, kind=None, last_certificate_issuance_time=None, location=None, name=None, next_auto_renewal_time_stamp=None, product_type=None, provisioning_state=None, root=None, serial_number=None, signed_certificate=None, status=None, tags=None, type=None, validity_in_years=None):
        if app_service_certificate_not_renewable_reasons and not isinstance(app_service_certificate_not_renewable_reasons, list):
            raise TypeError("Expected argument 'app_service_certificate_not_renewable_reasons' to be a list")
        pulumi.set(__self__, "app_service_certificate_not_renewable_reasons", app_service_certificate_not_renewable_reasons)
        if auto_renew and not isinstance(auto_renew, bool):
            raise TypeError("Expected argument 'auto_renew' to be a bool")
        pulumi.set(__self__, "auto_renew", auto_renew)
        if certificates and not isinstance(certificates, dict):
            raise TypeError("Expected argument 'certificates' to be a dict")
        pulumi.set(__self__, "certificates", certificates)
        if contact and not isinstance(contact, dict):
            raise TypeError("Expected argument 'contact' to be a dict")
        pulumi.set(__self__, "contact", contact)
        if csr and not isinstance(csr, str):
            raise TypeError("Expected argument 'csr' to be a str")
        pulumi.set(__self__, "csr", csr)
        if distinguished_name and not isinstance(distinguished_name, str):
            raise TypeError("Expected argument 'distinguished_name' to be a str")
        pulumi.set(__self__, "distinguished_name", distinguished_name)
        if domain_verification_token and not isinstance(domain_verification_token, str):
            raise TypeError("Expected argument 'domain_verification_token' to be a str")
        pulumi.set(__self__, "domain_verification_token", domain_verification_token)
        if expiration_time and not isinstance(expiration_time, str):
            raise TypeError("Expected argument 'expiration_time' to be a str")
        pulumi.set(__self__, "expiration_time", expiration_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if intermediate and not isinstance(intermediate, dict):
            raise TypeError("Expected argument 'intermediate' to be a dict")
        pulumi.set(__self__, "intermediate", intermediate)
        if is_private_key_external and not isinstance(is_private_key_external, bool):
            raise TypeError("Expected argument 'is_private_key_external' to be a bool")
        pulumi.set(__self__, "is_private_key_external", is_private_key_external)
        if key_size and not isinstance(key_size, int):
            raise TypeError("Expected argument 'key_size' to be a int")
        pulumi.set(__self__, "key_size", key_size)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if last_certificate_issuance_time and not isinstance(last_certificate_issuance_time, str):
            raise TypeError("Expected argument 'last_certificate_issuance_time' to be a str")
        pulumi.set(__self__, "last_certificate_issuance_time", last_certificate_issuance_time)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if next_auto_renewal_time_stamp and not isinstance(next_auto_renewal_time_stamp, str):
            raise TypeError("Expected argument 'next_auto_renewal_time_stamp' to be a str")
        pulumi.set(__self__, "next_auto_renewal_time_stamp", next_auto_renewal_time_stamp)
        if product_type and not isinstance(product_type, str):
            raise TypeError("Expected argument 'product_type' to be a str")
        pulumi.set(__self__, "product_type", product_type)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if root and not isinstance(root, dict):
            raise TypeError("Expected argument 'root' to be a dict")
        pulumi.set(__self__, "root", root)
        if serial_number and not isinstance(serial_number, str):
            raise TypeError("Expected argument 'serial_number' to be a str")
        pulumi.set(__self__, "serial_number", serial_number)
        if signed_certificate and not isinstance(signed_certificate, dict):
            raise TypeError("Expected argument 'signed_certificate' to be a dict")
        pulumi.set(__self__, "signed_certificate", signed_certificate)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if validity_in_years and not isinstance(validity_in_years, int):
            raise TypeError("Expected argument 'validity_in_years' to be a int")
        pulumi.set(__self__, "validity_in_years", validity_in_years)

    @property
    @pulumi.getter(name="appServiceCertificateNotRenewableReasons")
    def app_service_certificate_not_renewable_reasons(self) -> Sequence[str]:
        """
        Reasons why App Service Certificate is not renewable at the current moment.
        """
        return pulumi.get(self, "app_service_certificate_not_renewable_reasons")

    @property
    @pulumi.getter(name="autoRenew")
    def auto_renew(self) -> Optional[bool]:
        """
        <code>true</code> if the certificate should be automatically renewed when it expires; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "auto_renew")

    @property
    @pulumi.getter
    def certificates(self) -> Optional[Mapping[str, 'outputs.AppServiceCertificateResponse']]:
        """
        State of the Key Vault secret.
        """
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter
    def contact(self) -> 'outputs.CertificateOrderContactResponse':
        """
        Contact info
        """
        return pulumi.get(self, "contact")

    @property
    @pulumi.getter
    def csr(self) -> Optional[str]:
        """
        Last CSR that was created for this order.
        """
        return pulumi.get(self, "csr")

    @property
    @pulumi.getter(name="distinguishedName")
    def distinguished_name(self) -> Optional[str]:
        """
        Certificate distinguished name.
        """
        return pulumi.get(self, "distinguished_name")

    @property
    @pulumi.getter(name="domainVerificationToken")
    def domain_verification_token(self) -> str:
        """
        Domain verification token.
        """
        return pulumi.get(self, "domain_verification_token")

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> str:
        """
        Certificate expiration time.
        """
        return pulumi.get(self, "expiration_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def intermediate(self) -> 'outputs.CertificateDetailsResponse':
        """
        Intermediate certificate.
        """
        return pulumi.get(self, "intermediate")

    @property
    @pulumi.getter(name="isPrivateKeyExternal")
    def is_private_key_external(self) -> bool:
        """
        <code>true</code> if private key is external; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "is_private_key_external")

    @property
    @pulumi.getter(name="keySize")
    def key_size(self) -> Optional[int]:
        """
        Certificate key size.
        """
        return pulumi.get(self, "key_size")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastCertificateIssuanceTime")
    def last_certificate_issuance_time(self) -> str:
        """
        Certificate last issuance time.
        """
        return pulumi.get(self, "last_certificate_issuance_time")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nextAutoRenewalTimeStamp")
    def next_auto_renewal_time_stamp(self) -> str:
        """
        Time stamp when the certificate would be auto renewed next
        """
        return pulumi.get(self, "next_auto_renewal_time_stamp")

    @property
    @pulumi.getter(name="productType")
    def product_type(self) -> str:
        """
        Certificate product type.
        """
        return pulumi.get(self, "product_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Status of certificate order.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def root(self) -> 'outputs.CertificateDetailsResponse':
        """
        Root certificate.
        """
        return pulumi.get(self, "root")

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> str:
        """
        Current serial number of the certificate.
        """
        return pulumi.get(self, "serial_number")

    @property
    @pulumi.getter(name="signedCertificate")
    def signed_certificate(self) -> 'outputs.CertificateDetailsResponse':
        """
        Signed certificate.
        """
        return pulumi.get(self, "signed_certificate")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Current order status.
        """
        return pulumi.get(self, "status")

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
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="validityInYears")
    def validity_in_years(self) -> Optional[int]:
        """
        Duration in years (must be 1).
        """
        return pulumi.get(self, "validity_in_years")


class AwaitableGetAppServiceCertificateOrderResult(GetAppServiceCertificateOrderResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppServiceCertificateOrderResult(
            app_service_certificate_not_renewable_reasons=self.app_service_certificate_not_renewable_reasons,
            auto_renew=self.auto_renew,
            certificates=self.certificates,
            contact=self.contact,
            csr=self.csr,
            distinguished_name=self.distinguished_name,
            domain_verification_token=self.domain_verification_token,
            expiration_time=self.expiration_time,
            id=self.id,
            intermediate=self.intermediate,
            is_private_key_external=self.is_private_key_external,
            key_size=self.key_size,
            kind=self.kind,
            last_certificate_issuance_time=self.last_certificate_issuance_time,
            location=self.location,
            name=self.name,
            next_auto_renewal_time_stamp=self.next_auto_renewal_time_stamp,
            product_type=self.product_type,
            provisioning_state=self.provisioning_state,
            root=self.root,
            serial_number=self.serial_number,
            signed_certificate=self.signed_certificate,
            status=self.status,
            tags=self.tags,
            type=self.type,
            validity_in_years=self.validity_in_years)


def get_app_service_certificate_order(certificate_order_name: Optional[str] = None,
                                      resource_group_name: Optional[str] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAppServiceCertificateOrderResult:
    """
    Get a certificate order.


    :param str certificate_order_name: Name of the certificate order..
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    __args__ = dict()
    __args__['certificateOrderName'] = certificate_order_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:certificateregistration/v20210101:getAppServiceCertificateOrder', __args__, opts=opts, typ=GetAppServiceCertificateOrderResult).value

    return AwaitableGetAppServiceCertificateOrderResult(
        app_service_certificate_not_renewable_reasons=__ret__.app_service_certificate_not_renewable_reasons,
        auto_renew=__ret__.auto_renew,
        certificates=__ret__.certificates,
        contact=__ret__.contact,
        csr=__ret__.csr,
        distinguished_name=__ret__.distinguished_name,
        domain_verification_token=__ret__.domain_verification_token,
        expiration_time=__ret__.expiration_time,
        id=__ret__.id,
        intermediate=__ret__.intermediate,
        is_private_key_external=__ret__.is_private_key_external,
        key_size=__ret__.key_size,
        kind=__ret__.kind,
        last_certificate_issuance_time=__ret__.last_certificate_issuance_time,
        location=__ret__.location,
        name=__ret__.name,
        next_auto_renewal_time_stamp=__ret__.next_auto_renewal_time_stamp,
        product_type=__ret__.product_type,
        provisioning_state=__ret__.provisioning_state,
        root=__ret__.root,
        serial_number=__ret__.serial_number,
        signed_certificate=__ret__.signed_certificate,
        status=__ret__.status,
        tags=__ret__.tags,
        type=__ret__.type,
        validity_in_years=__ret__.validity_in_years)


@_utilities.lift_output_func(get_app_service_certificate_order)
def get_app_service_certificate_order_output(certificate_order_name: Optional[pulumi.Input[str]] = None,
                                             resource_group_name: Optional[pulumi.Input[str]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAppServiceCertificateOrderResult]:
    """
    Get a certificate order.


    :param str certificate_order_name: Name of the certificate order..
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    """
    ...
