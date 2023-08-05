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
from ._enums import *
from ._inputs import *

__all__ = ['DomainArgs', 'Domain']

@pulumi.input_type
class DomainArgs:
    def __init__(__self__, *,
                 consent: pulumi.Input['DomainPurchaseConsentArgs'],
                 contact_admin: pulumi.Input['ContactArgs'],
                 contact_billing: pulumi.Input['ContactArgs'],
                 contact_registrant: pulumi.Input['ContactArgs'],
                 contact_tech: pulumi.Input['ContactArgs'],
                 resource_group_name: pulumi.Input[str],
                 auth_code: Optional[pulumi.Input[str]] = None,
                 auto_renew: Optional[pulumi.Input[bool]] = None,
                 dns_type: Optional[pulumi.Input['DnsType']] = None,
                 dns_zone_id: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 privacy: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_dns_type: Optional[pulumi.Input['DnsType']] = None):
        """
        The set of arguments for constructing a Domain resource.
        :param pulumi.Input['DomainPurchaseConsentArgs'] consent: Legal agreement consent.
        :param pulumi.Input['ContactArgs'] contact_admin: Administrative contact.
        :param pulumi.Input['ContactArgs'] contact_billing: Billing contact.
        :param pulumi.Input['ContactArgs'] contact_registrant: Registrant contact.
        :param pulumi.Input['ContactArgs'] contact_tech: Technical contact.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[bool] auto_renew: <code>true</code> if the domain should be automatically renewed; otherwise, <code>false</code>.
        :param pulumi.Input['DnsType'] dns_type: Current DNS type
        :param pulumi.Input[str] dns_zone_id: Azure DNS Zone to use
        :param pulumi.Input[str] domain_name: Name of the domain.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[bool] privacy: <code>true</code> if domain privacy is enabled for this domain; otherwise, <code>false</code>.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input['DnsType'] target_dns_type: Target DNS type (would be used for migration)
        """
        pulumi.set(__self__, "consent", consent)
        pulumi.set(__self__, "contact_admin", contact_admin)
        pulumi.set(__self__, "contact_billing", contact_billing)
        pulumi.set(__self__, "contact_registrant", contact_registrant)
        pulumi.set(__self__, "contact_tech", contact_tech)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if auth_code is not None:
            pulumi.set(__self__, "auth_code", auth_code)
        if auto_renew is None:
            auto_renew = True
        if auto_renew is not None:
            pulumi.set(__self__, "auto_renew", auto_renew)
        if dns_type is not None:
            pulumi.set(__self__, "dns_type", dns_type)
        if dns_zone_id is not None:
            pulumi.set(__self__, "dns_zone_id", dns_zone_id)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if privacy is not None:
            pulumi.set(__self__, "privacy", privacy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if target_dns_type is not None:
            pulumi.set(__self__, "target_dns_type", target_dns_type)

    @property
    @pulumi.getter
    def consent(self) -> pulumi.Input['DomainPurchaseConsentArgs']:
        """
        Legal agreement consent.
        """
        return pulumi.get(self, "consent")

    @consent.setter
    def consent(self, value: pulumi.Input['DomainPurchaseConsentArgs']):
        pulumi.set(self, "consent", value)

    @property
    @pulumi.getter(name="contactAdmin")
    def contact_admin(self) -> pulumi.Input['ContactArgs']:
        """
        Administrative contact.
        """
        return pulumi.get(self, "contact_admin")

    @contact_admin.setter
    def contact_admin(self, value: pulumi.Input['ContactArgs']):
        pulumi.set(self, "contact_admin", value)

    @property
    @pulumi.getter(name="contactBilling")
    def contact_billing(self) -> pulumi.Input['ContactArgs']:
        """
        Billing contact.
        """
        return pulumi.get(self, "contact_billing")

    @contact_billing.setter
    def contact_billing(self, value: pulumi.Input['ContactArgs']):
        pulumi.set(self, "contact_billing", value)

    @property
    @pulumi.getter(name="contactRegistrant")
    def contact_registrant(self) -> pulumi.Input['ContactArgs']:
        """
        Registrant contact.
        """
        return pulumi.get(self, "contact_registrant")

    @contact_registrant.setter
    def contact_registrant(self, value: pulumi.Input['ContactArgs']):
        pulumi.set(self, "contact_registrant", value)

    @property
    @pulumi.getter(name="contactTech")
    def contact_tech(self) -> pulumi.Input['ContactArgs']:
        """
        Technical contact.
        """
        return pulumi.get(self, "contact_tech")

    @contact_tech.setter
    def contact_tech(self, value: pulumi.Input['ContactArgs']):
        pulumi.set(self, "contact_tech", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="authCode")
    def auth_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "auth_code")

    @auth_code.setter
    def auth_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "auth_code", value)

    @property
    @pulumi.getter(name="autoRenew")
    def auto_renew(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> if the domain should be automatically renewed; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "auto_renew")

    @auto_renew.setter
    def auto_renew(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_renew", value)

    @property
    @pulumi.getter(name="dnsType")
    def dns_type(self) -> Optional[pulumi.Input['DnsType']]:
        """
        Current DNS type
        """
        return pulumi.get(self, "dns_type")

    @dns_type.setter
    def dns_type(self, value: Optional[pulumi.Input['DnsType']]):
        pulumi.set(self, "dns_type", value)

    @property
    @pulumi.getter(name="dnsZoneId")
    def dns_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        Azure DNS Zone to use
        """
        return pulumi.get(self, "dns_zone_id")

    @dns_zone_id.setter
    def dns_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_zone_id", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the domain.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def privacy(self) -> Optional[pulumi.Input[bool]]:
        """
        <code>true</code> if domain privacy is enabled for this domain; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "privacy")

    @privacy.setter
    def privacy(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "privacy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="targetDnsType")
    def target_dns_type(self) -> Optional[pulumi.Input['DnsType']]:
        """
        Target DNS type (would be used for migration)
        """
        return pulumi.get(self, "target_dns_type")

    @target_dns_type.setter
    def target_dns_type(self, value: Optional[pulumi.Input['DnsType']]):
        pulumi.set(self, "target_dns_type", value)


class Domain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_code: Optional[pulumi.Input[str]] = None,
                 auto_renew: Optional[pulumi.Input[bool]] = None,
                 consent: Optional[pulumi.Input[pulumi.InputType['DomainPurchaseConsentArgs']]] = None,
                 contact_admin: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 contact_billing: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 contact_registrant: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 contact_tech: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 dns_type: Optional[pulumi.Input['DnsType']] = None,
                 dns_zone_id: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 privacy: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_dns_type: Optional[pulumi.Input['DnsType']] = None,
                 __props__=None):
        """
        Information about a domain.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_renew: <code>true</code> if the domain should be automatically renewed; otherwise, <code>false</code>.
        :param pulumi.Input[pulumi.InputType['DomainPurchaseConsentArgs']] consent: Legal agreement consent.
        :param pulumi.Input[pulumi.InputType['ContactArgs']] contact_admin: Administrative contact.
        :param pulumi.Input[pulumi.InputType['ContactArgs']] contact_billing: Billing contact.
        :param pulumi.Input[pulumi.InputType['ContactArgs']] contact_registrant: Registrant contact.
        :param pulumi.Input[pulumi.InputType['ContactArgs']] contact_tech: Technical contact.
        :param pulumi.Input['DnsType'] dns_type: Current DNS type
        :param pulumi.Input[str] dns_zone_id: Azure DNS Zone to use
        :param pulumi.Input[str] domain_name: Name of the domain.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[bool] privacy: <code>true</code> if domain privacy is enabled for this domain; otherwise, <code>false</code>.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input['DnsType'] target_dns_type: Target DNS type (would be used for migration)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DomainArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Information about a domain.

        :param str resource_name: The name of the resource.
        :param DomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auth_code: Optional[pulumi.Input[str]] = None,
                 auto_renew: Optional[pulumi.Input[bool]] = None,
                 consent: Optional[pulumi.Input[pulumi.InputType['DomainPurchaseConsentArgs']]] = None,
                 contact_admin: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 contact_billing: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 contact_registrant: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 contact_tech: Optional[pulumi.Input[pulumi.InputType['ContactArgs']]] = None,
                 dns_type: Optional[pulumi.Input['DnsType']] = None,
                 dns_zone_id: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 privacy: Optional[pulumi.Input[bool]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_dns_type: Optional[pulumi.Input['DnsType']] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainArgs.__new__(DomainArgs)

            __props__.__dict__["auth_code"] = auth_code
            if auto_renew is None:
                auto_renew = True
            __props__.__dict__["auto_renew"] = auto_renew
            if consent is None and not opts.urn:
                raise TypeError("Missing required property 'consent'")
            __props__.__dict__["consent"] = consent
            if contact_admin is None and not opts.urn:
                raise TypeError("Missing required property 'contact_admin'")
            __props__.__dict__["contact_admin"] = contact_admin
            if contact_billing is None and not opts.urn:
                raise TypeError("Missing required property 'contact_billing'")
            __props__.__dict__["contact_billing"] = contact_billing
            if contact_registrant is None and not opts.urn:
                raise TypeError("Missing required property 'contact_registrant'")
            __props__.__dict__["contact_registrant"] = contact_registrant
            if contact_tech is None and not opts.urn:
                raise TypeError("Missing required property 'contact_tech'")
            __props__.__dict__["contact_tech"] = contact_tech
            __props__.__dict__["dns_type"] = dns_type
            __props__.__dict__["dns_zone_id"] = dns_zone_id
            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["privacy"] = privacy
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["target_dns_type"] = target_dns_type
            __props__.__dict__["created_time"] = None
            __props__.__dict__["domain_not_renewable_reasons"] = None
            __props__.__dict__["expiration_time"] = None
            __props__.__dict__["last_renewed_time"] = None
            __props__.__dict__["managed_host_names"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["name_servers"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["ready_for_dns_record_management"] = None
            __props__.__dict__["registration_status"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:domainregistration:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20150401:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20180201:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20190801:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20200601:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20200901:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20201201:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20210101:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20210115:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20210201:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20210301:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20220301:Domain"), pulumi.Alias(type_="azure-native:domainregistration/v20220901:Domain")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Domain, __self__).__init__(
            'azure-native:domainregistration/v20201001:Domain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Domain':
        """
        Get an existing Domain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DomainArgs.__new__(DomainArgs)

        __props__.__dict__["auth_code"] = None
        __props__.__dict__["auto_renew"] = None
        __props__.__dict__["created_time"] = None
        __props__.__dict__["dns_type"] = None
        __props__.__dict__["dns_zone_id"] = None
        __props__.__dict__["domain_not_renewable_reasons"] = None
        __props__.__dict__["expiration_time"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["last_renewed_time"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["managed_host_names"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["name_servers"] = None
        __props__.__dict__["privacy"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["ready_for_dns_record_management"] = None
        __props__.__dict__["registration_status"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["target_dns_type"] = None
        __props__.__dict__["type"] = None
        return Domain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authCode")
    def auth_code(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "auth_code")

    @property
    @pulumi.getter(name="autoRenew")
    def auto_renew(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> if the domain should be automatically renewed; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "auto_renew")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> pulumi.Output[str]:
        """
        Domain creation timestamp.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="dnsType")
    def dns_type(self) -> pulumi.Output[Optional[str]]:
        """
        Current DNS type
        """
        return pulumi.get(self, "dns_type")

    @property
    @pulumi.getter(name="dnsZoneId")
    def dns_zone_id(self) -> pulumi.Output[Optional[str]]:
        """
        Azure DNS Zone to use
        """
        return pulumi.get(self, "dns_zone_id")

    @property
    @pulumi.getter(name="domainNotRenewableReasons")
    def domain_not_renewable_reasons(self) -> pulumi.Output[Sequence[str]]:
        """
        Reasons why domain is not renewable.
        """
        return pulumi.get(self, "domain_not_renewable_reasons")

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> pulumi.Output[str]:
        """
        Domain expiration timestamp.
        """
        return pulumi.get(self, "expiration_time")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="lastRenewedTime")
    def last_renewed_time(self) -> pulumi.Output[str]:
        """
        Timestamp when the domain was renewed last time.
        """
        return pulumi.get(self, "last_renewed_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedHostNames")
    def managed_host_names(self) -> pulumi.Output[Sequence['outputs.HostNameResponse']]:
        """
        All hostnames derived from the domain and assigned to Azure resources.
        """
        return pulumi.get(self, "managed_host_names")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameServers")
    def name_servers(self) -> pulumi.Output[Sequence[str]]:
        """
        Name servers.
        """
        return pulumi.get(self, "name_servers")

    @property
    @pulumi.getter
    def privacy(self) -> pulumi.Output[Optional[bool]]:
        """
        <code>true</code> if domain privacy is enabled for this domain; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "privacy")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Domain provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="readyForDnsRecordManagement")
    def ready_for_dns_record_management(self) -> pulumi.Output[bool]:
        """
        <code>true</code> if Azure can assign this domain to App Service apps; otherwise, <code>false</code>. This value will be <code>true</code> if domain registration status is active and 
         it is hosted on name servers Azure has programmatic access to.
        """
        return pulumi.get(self, "ready_for_dns_record_management")

    @property
    @pulumi.getter(name="registrationStatus")
    def registration_status(self) -> pulumi.Output[str]:
        """
        Domain registration status.
        """
        return pulumi.get(self, "registration_status")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetDnsType")
    def target_dns_type(self) -> pulumi.Output[Optional[str]]:
        """
        Target DNS type (would be used for migration)
        """
        return pulumi.get(self, "target_dns_type")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

