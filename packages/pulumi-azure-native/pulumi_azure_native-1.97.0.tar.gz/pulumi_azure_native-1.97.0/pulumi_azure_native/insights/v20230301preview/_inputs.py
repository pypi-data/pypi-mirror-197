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
    'AzureAppPushReceiverArgs',
    'EmailReceiverArgs',
    'SmsReceiverArgs',
    'VoiceReceiverArgs',
    'WebhookReceiverArgs',
]

@pulumi.input_type
class AzureAppPushReceiverArgs:
    def __init__(__self__, *,
                 email_address: pulumi.Input[str],
                 name: pulumi.Input[str]):
        """
        The Azure mobile App push notification receiver.
        :param pulumi.Input[str] email_address: The email address registered for the Azure mobile app.
        :param pulumi.Input[str] name: The name of the Azure mobile app push receiver. Names must be unique across all receivers within a tenant action group.
        """
        pulumi.set(__self__, "email_address", email_address)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> pulumi.Input[str]:
        """
        The email address registered for the Azure mobile app.
        """
        return pulumi.get(self, "email_address")

    @email_address.setter
    def email_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "email_address", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the Azure mobile app push receiver. Names must be unique across all receivers within a tenant action group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class EmailReceiverArgs:
    def __init__(__self__, *,
                 email_address: pulumi.Input[str],
                 name: pulumi.Input[str],
                 use_common_alert_schema: Optional[pulumi.Input[bool]] = None):
        """
        An email receiver.
        :param pulumi.Input[str] email_address: The email address of this receiver.
        :param pulumi.Input[str] name: The name of the email receiver. Names must be unique across all receivers within a tenant action group.
        :param pulumi.Input[bool] use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "email_address", email_address)
        pulumi.set(__self__, "name", name)
        if use_common_alert_schema is None:
            use_common_alert_schema = False
        if use_common_alert_schema is not None:
            pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> pulumi.Input[str]:
        """
        The email address of this receiver.
        """
        return pulumi.get(self, "email_address")

    @email_address.setter
    def email_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "email_address", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the email receiver. Names must be unique across all receivers within a tenant action group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

    @use_common_alert_schema.setter
    def use_common_alert_schema(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_common_alert_schema", value)


@pulumi.input_type
class SmsReceiverArgs:
    def __init__(__self__, *,
                 country_code: pulumi.Input[str],
                 name: pulumi.Input[str],
                 phone_number: pulumi.Input[str]):
        """
        An SMS receiver.
        :param pulumi.Input[str] country_code: The country code of the SMS receiver.
        :param pulumi.Input[str] name: The name of the SMS receiver. Names must be unique across all receivers within a tenant action group.
        :param pulumi.Input[str] phone_number: The phone number of the SMS receiver.
        """
        pulumi.set(__self__, "country_code", country_code)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter(name="countryCode")
    def country_code(self) -> pulumi.Input[str]:
        """
        The country code of the SMS receiver.
        """
        return pulumi.get(self, "country_code")

    @country_code.setter
    def country_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "country_code", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the SMS receiver. Names must be unique across all receivers within a tenant action group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> pulumi.Input[str]:
        """
        The phone number of the SMS receiver.
        """
        return pulumi.get(self, "phone_number")

    @phone_number.setter
    def phone_number(self, value: pulumi.Input[str]):
        pulumi.set(self, "phone_number", value)


@pulumi.input_type
class VoiceReceiverArgs:
    def __init__(__self__, *,
                 country_code: pulumi.Input[str],
                 name: pulumi.Input[str],
                 phone_number: pulumi.Input[str]):
        """
        A voice receiver.
        :param pulumi.Input[str] country_code: The country code of the voice receiver.
        :param pulumi.Input[str] name: The name of the voice receiver. Names must be unique across all receivers within a tenant action group.
        :param pulumi.Input[str] phone_number: The phone number of the voice receiver.
        """
        pulumi.set(__self__, "country_code", country_code)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter(name="countryCode")
    def country_code(self) -> pulumi.Input[str]:
        """
        The country code of the voice receiver.
        """
        return pulumi.get(self, "country_code")

    @country_code.setter
    def country_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "country_code", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the voice receiver. Names must be unique across all receivers within a tenant action group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> pulumi.Input[str]:
        """
        The phone number of the voice receiver.
        """
        return pulumi.get(self, "phone_number")

    @phone_number.setter
    def phone_number(self, value: pulumi.Input[str]):
        pulumi.set(self, "phone_number", value)


@pulumi.input_type
class WebhookReceiverArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 service_uri: pulumi.Input[str],
                 identifier_uri: Optional[pulumi.Input[str]] = None,
                 object_id: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 use_aad_auth: Optional[pulumi.Input[bool]] = None,
                 use_common_alert_schema: Optional[pulumi.Input[bool]] = None):
        """
        A webhook receiver.
        :param pulumi.Input[str] name: The name of the webhook receiver. Names must be unique across all receivers within a tenant action group.
        :param pulumi.Input[str] service_uri: The URI where webhooks should be sent.
        :param pulumi.Input[str] identifier_uri: Indicates the identifier uri for aad auth.
        :param pulumi.Input[str] object_id: Indicates the webhook app object Id for aad auth.
        :param pulumi.Input[str] tenant_id: Indicates the tenant id for aad auth.
        :param pulumi.Input[bool] use_aad_auth: Indicates whether or not use AAD authentication.
        :param pulumi.Input[bool] use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "service_uri", service_uri)
        if identifier_uri is not None:
            pulumi.set(__self__, "identifier_uri", identifier_uri)
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)
        if use_aad_auth is None:
            use_aad_auth = False
        if use_aad_auth is not None:
            pulumi.set(__self__, "use_aad_auth", use_aad_auth)
        if use_common_alert_schema is None:
            use_common_alert_schema = False
        if use_common_alert_schema is not None:
            pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the webhook receiver. Names must be unique across all receivers within a tenant action group.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serviceUri")
    def service_uri(self) -> pulumi.Input[str]:
        """
        The URI where webhooks should be sent.
        """
        return pulumi.get(self, "service_uri")

    @service_uri.setter
    def service_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_uri", value)

    @property
    @pulumi.getter(name="identifierUri")
    def identifier_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the identifier uri for aad auth.
        """
        return pulumi.get(self, "identifier_uri")

    @identifier_uri.setter
    def identifier_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identifier_uri", value)

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the webhook app object Id for aad auth.
        """
        return pulumi.get(self, "object_id")

    @object_id.setter
    def object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "object_id", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the tenant id for aad auth.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)

    @property
    @pulumi.getter(name="useAadAuth")
    def use_aad_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether or not use AAD authentication.
        """
        return pulumi.get(self, "use_aad_auth")

    @use_aad_auth.setter
    def use_aad_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_aad_auth", value)

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

    @use_common_alert_schema.setter
    def use_common_alert_schema(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_common_alert_schema", value)


