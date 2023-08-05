# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'AddressArgs',
    'AsymmetricEncryptedSecretArgs',
    'AuthenticationArgs',
    'AzureContainerInfoArgs',
    'ClientAccessRightArgs',
    'ContactDetailsArgs',
    'FileSourceInfoArgs',
    'IoTDeviceInfoArgs',
    'MountPointMapArgs',
    'OrderStatusArgs',
    'PeriodicTimerSourceInfoArgs',
    'RefreshDetailsArgs',
    'RoleSinkInfoArgs',
    'ShareAccessRightArgs',
    'SkuArgs',
    'SymmetricKeyArgs',
    'UserAccessRightArgs',
]

@pulumi.input_type
class AddressArgs:
    def __init__(__self__, *,
                 address_line1: pulumi.Input[str],
                 city: pulumi.Input[str],
                 country: pulumi.Input[str],
                 postal_code: pulumi.Input[str],
                 state: pulumi.Input[str],
                 address_line2: Optional[pulumi.Input[str]] = None,
                 address_line3: Optional[pulumi.Input[str]] = None):
        """
        The shipping address of the customer.
        :param pulumi.Input[str] address_line1: The address line1.
        :param pulumi.Input[str] city: The city name.
        :param pulumi.Input[str] country: The country name.
        :param pulumi.Input[str] postal_code: The postal code.
        :param pulumi.Input[str] state: The state name.
        :param pulumi.Input[str] address_line2: The address line2.
        :param pulumi.Input[str] address_line3: The address line3.
        """
        pulumi.set(__self__, "address_line1", address_line1)
        pulumi.set(__self__, "city", city)
        pulumi.set(__self__, "country", country)
        pulumi.set(__self__, "postal_code", postal_code)
        pulumi.set(__self__, "state", state)
        if address_line2 is not None:
            pulumi.set(__self__, "address_line2", address_line2)
        if address_line3 is not None:
            pulumi.set(__self__, "address_line3", address_line3)

    @property
    @pulumi.getter(name="addressLine1")
    def address_line1(self) -> pulumi.Input[str]:
        """
        The address line1.
        """
        return pulumi.get(self, "address_line1")

    @address_line1.setter
    def address_line1(self, value: pulumi.Input[str]):
        pulumi.set(self, "address_line1", value)

    @property
    @pulumi.getter
    def city(self) -> pulumi.Input[str]:
        """
        The city name.
        """
        return pulumi.get(self, "city")

    @city.setter
    def city(self, value: pulumi.Input[str]):
        pulumi.set(self, "city", value)

    @property
    @pulumi.getter
    def country(self) -> pulumi.Input[str]:
        """
        The country name.
        """
        return pulumi.get(self, "country")

    @country.setter
    def country(self, value: pulumi.Input[str]):
        pulumi.set(self, "country", value)

    @property
    @pulumi.getter(name="postalCode")
    def postal_code(self) -> pulumi.Input[str]:
        """
        The postal code.
        """
        return pulumi.get(self, "postal_code")

    @postal_code.setter
    def postal_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "postal_code", value)

    @property
    @pulumi.getter
    def state(self) -> pulumi.Input[str]:
        """
        The state name.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: pulumi.Input[str]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="addressLine2")
    def address_line2(self) -> Optional[pulumi.Input[str]]:
        """
        The address line2.
        """
        return pulumi.get(self, "address_line2")

    @address_line2.setter
    def address_line2(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_line2", value)

    @property
    @pulumi.getter(name="addressLine3")
    def address_line3(self) -> Optional[pulumi.Input[str]]:
        """
        The address line3.
        """
        return pulumi.get(self, "address_line3")

    @address_line3.setter
    def address_line3(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_line3", value)


@pulumi.input_type
class AsymmetricEncryptedSecretArgs:
    def __init__(__self__, *,
                 encryption_algorithm: pulumi.Input[Union[str, 'EncryptionAlgorithm']],
                 value: pulumi.Input[str],
                 encryption_cert_thumbprint: Optional[pulumi.Input[str]] = None):
        """
        Represent the secrets intended for encryption with asymmetric key pair.
        :param pulumi.Input[Union[str, 'EncryptionAlgorithm']] encryption_algorithm: The algorithm used to encrypt "Value".
        :param pulumi.Input[str] value: The value of the secret.
        :param pulumi.Input[str] encryption_cert_thumbprint: Thumbprint certificate used to encrypt \\"Value\\". If the value is unencrypted, it will be null.
        """
        pulumi.set(__self__, "encryption_algorithm", encryption_algorithm)
        pulumi.set(__self__, "value", value)
        if encryption_cert_thumbprint is not None:
            pulumi.set(__self__, "encryption_cert_thumbprint", encryption_cert_thumbprint)

    @property
    @pulumi.getter(name="encryptionAlgorithm")
    def encryption_algorithm(self) -> pulumi.Input[Union[str, 'EncryptionAlgorithm']]:
        """
        The algorithm used to encrypt "Value".
        """
        return pulumi.get(self, "encryption_algorithm")

    @encryption_algorithm.setter
    def encryption_algorithm(self, value: pulumi.Input[Union[str, 'EncryptionAlgorithm']]):
        pulumi.set(self, "encryption_algorithm", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the secret.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="encryptionCertThumbprint")
    def encryption_cert_thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        Thumbprint certificate used to encrypt \\"Value\\". If the value is unencrypted, it will be null.
        """
        return pulumi.get(self, "encryption_cert_thumbprint")

    @encryption_cert_thumbprint.setter
    def encryption_cert_thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encryption_cert_thumbprint", value)


@pulumi.input_type
class AuthenticationArgs:
    def __init__(__self__, *,
                 symmetric_key: Optional[pulumi.Input['SymmetricKeyArgs']] = None):
        """
        Authentication mechanism for IoT devices.
        :param pulumi.Input['SymmetricKeyArgs'] symmetric_key: Symmetric key for authentication.
        """
        if symmetric_key is not None:
            pulumi.set(__self__, "symmetric_key", symmetric_key)

    @property
    @pulumi.getter(name="symmetricKey")
    def symmetric_key(self) -> Optional[pulumi.Input['SymmetricKeyArgs']]:
        """
        Symmetric key for authentication.
        """
        return pulumi.get(self, "symmetric_key")

    @symmetric_key.setter
    def symmetric_key(self, value: Optional[pulumi.Input['SymmetricKeyArgs']]):
        pulumi.set(self, "symmetric_key", value)


@pulumi.input_type
class AzureContainerInfoArgs:
    def __init__(__self__, *,
                 container_name: pulumi.Input[str],
                 data_format: pulumi.Input[Union[str, 'AzureContainerDataFormat']],
                 storage_account_credential_id: pulumi.Input[str]):
        """
        Azure container mapping of the endpoint.
        :param pulumi.Input[str] container_name: Container name (Based on the data format specified, this represents the name of Azure Files/Page blob/Block blob).
        :param pulumi.Input[Union[str, 'AzureContainerDataFormat']] data_format: Storage format used for the file represented by the share.
        :param pulumi.Input[str] storage_account_credential_id: ID of the storage account credential used to access storage.
        """
        pulumi.set(__self__, "container_name", container_name)
        pulumi.set(__self__, "data_format", data_format)
        pulumi.set(__self__, "storage_account_credential_id", storage_account_credential_id)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Input[str]:
        """
        Container name (Based on the data format specified, this represents the name of Azure Files/Page blob/Block blob).
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="dataFormat")
    def data_format(self) -> pulumi.Input[Union[str, 'AzureContainerDataFormat']]:
        """
        Storage format used for the file represented by the share.
        """
        return pulumi.get(self, "data_format")

    @data_format.setter
    def data_format(self, value: pulumi.Input[Union[str, 'AzureContainerDataFormat']]):
        pulumi.set(self, "data_format", value)

    @property
    @pulumi.getter(name="storageAccountCredentialId")
    def storage_account_credential_id(self) -> pulumi.Input[str]:
        """
        ID of the storage account credential used to access storage.
        """
        return pulumi.get(self, "storage_account_credential_id")

    @storage_account_credential_id.setter
    def storage_account_credential_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_credential_id", value)


@pulumi.input_type
class ClientAccessRightArgs:
    def __init__(__self__, *,
                 access_permission: pulumi.Input[Union[str, 'ClientPermissionType']],
                 client: pulumi.Input[str]):
        """
        The mapping between a particular client IP and the type of access client has on the NFS share.
        :param pulumi.Input[Union[str, 'ClientPermissionType']] access_permission: Type of access to be allowed for the client.
        :param pulumi.Input[str] client: IP of the client.
        """
        pulumi.set(__self__, "access_permission", access_permission)
        pulumi.set(__self__, "client", client)

    @property
    @pulumi.getter(name="accessPermission")
    def access_permission(self) -> pulumi.Input[Union[str, 'ClientPermissionType']]:
        """
        Type of access to be allowed for the client.
        """
        return pulumi.get(self, "access_permission")

    @access_permission.setter
    def access_permission(self, value: pulumi.Input[Union[str, 'ClientPermissionType']]):
        pulumi.set(self, "access_permission", value)

    @property
    @pulumi.getter
    def client(self) -> pulumi.Input[str]:
        """
        IP of the client.
        """
        return pulumi.get(self, "client")

    @client.setter
    def client(self, value: pulumi.Input[str]):
        pulumi.set(self, "client", value)


@pulumi.input_type
class ContactDetailsArgs:
    def __init__(__self__, *,
                 company_name: pulumi.Input[str],
                 contact_person: pulumi.Input[str],
                 email_list: pulumi.Input[Sequence[pulumi.Input[str]]],
                 phone: pulumi.Input[str]):
        """
        Contains all the contact details of the customer.
        :param pulumi.Input[str] company_name: The name of the company.
        :param pulumi.Input[str] contact_person: The contact person name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] email_list: The email list.
        :param pulumi.Input[str] phone: The phone number.
        """
        pulumi.set(__self__, "company_name", company_name)
        pulumi.set(__self__, "contact_person", contact_person)
        pulumi.set(__self__, "email_list", email_list)
        pulumi.set(__self__, "phone", phone)

    @property
    @pulumi.getter(name="companyName")
    def company_name(self) -> pulumi.Input[str]:
        """
        The name of the company.
        """
        return pulumi.get(self, "company_name")

    @company_name.setter
    def company_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "company_name", value)

    @property
    @pulumi.getter(name="contactPerson")
    def contact_person(self) -> pulumi.Input[str]:
        """
        The contact person name.
        """
        return pulumi.get(self, "contact_person")

    @contact_person.setter
    def contact_person(self, value: pulumi.Input[str]):
        pulumi.set(self, "contact_person", value)

    @property
    @pulumi.getter(name="emailList")
    def email_list(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The email list.
        """
        return pulumi.get(self, "email_list")

    @email_list.setter
    def email_list(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "email_list", value)

    @property
    @pulumi.getter
    def phone(self) -> pulumi.Input[str]:
        """
        The phone number.
        """
        return pulumi.get(self, "phone")

    @phone.setter
    def phone(self, value: pulumi.Input[str]):
        pulumi.set(self, "phone", value)


@pulumi.input_type
class FileSourceInfoArgs:
    def __init__(__self__, *,
                 share_id: pulumi.Input[str]):
        """
        File source details.
        :param pulumi.Input[str] share_id: File share ID.
        """
        pulumi.set(__self__, "share_id", share_id)

    @property
    @pulumi.getter(name="shareId")
    def share_id(self) -> pulumi.Input[str]:
        """
        File share ID.
        """
        return pulumi.get(self, "share_id")

    @share_id.setter
    def share_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "share_id", value)


@pulumi.input_type
class IoTDeviceInfoArgs:
    def __init__(__self__, *,
                 device_id: pulumi.Input[str],
                 io_t_host_hub: pulumi.Input[str],
                 authentication: Optional[pulumi.Input['AuthenticationArgs']] = None):
        """
        Metadata of IoT device/IoT Edge device to be configured.
        :param pulumi.Input[str] device_id: ID of the IoT device/edge device.
        :param pulumi.Input[str] io_t_host_hub: Host name for the IoT hub associated to the device.
        :param pulumi.Input['AuthenticationArgs'] authentication: IoT device authentication info.
        """
        pulumi.set(__self__, "device_id", device_id)
        pulumi.set(__self__, "io_t_host_hub", io_t_host_hub)
        if authentication is not None:
            pulumi.set(__self__, "authentication", authentication)

    @property
    @pulumi.getter(name="deviceId")
    def device_id(self) -> pulumi.Input[str]:
        """
        ID of the IoT device/edge device.
        """
        return pulumi.get(self, "device_id")

    @device_id.setter
    def device_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "device_id", value)

    @property
    @pulumi.getter(name="ioTHostHub")
    def io_t_host_hub(self) -> pulumi.Input[str]:
        """
        Host name for the IoT hub associated to the device.
        """
        return pulumi.get(self, "io_t_host_hub")

    @io_t_host_hub.setter
    def io_t_host_hub(self, value: pulumi.Input[str]):
        pulumi.set(self, "io_t_host_hub", value)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[pulumi.Input['AuthenticationArgs']]:
        """
        IoT device authentication info.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: Optional[pulumi.Input['AuthenticationArgs']]):
        pulumi.set(self, "authentication", value)


@pulumi.input_type
class MountPointMapArgs:
    def __init__(__self__, *,
                 share_id: pulumi.Input[str]):
        """
        The share mount point.
        :param pulumi.Input[str] share_id: ID of the share mounted to the role VM.
        """
        pulumi.set(__self__, "share_id", share_id)

    @property
    @pulumi.getter(name="shareId")
    def share_id(self) -> pulumi.Input[str]:
        """
        ID of the share mounted to the role VM.
        """
        return pulumi.get(self, "share_id")

    @share_id.setter
    def share_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "share_id", value)


@pulumi.input_type
class OrderStatusArgs:
    def __init__(__self__, *,
                 status: pulumi.Input[Union[str, 'OrderState']],
                 comments: Optional[pulumi.Input[str]] = None):
        """
        Represents a single status change.
        :param pulumi.Input[Union[str, 'OrderState']] status: Status of the order as per the allowed status types.
        :param pulumi.Input[str] comments: Comments related to this status change.
        """
        pulumi.set(__self__, "status", status)
        if comments is not None:
            pulumi.set(__self__, "comments", comments)

    @property
    @pulumi.getter
    def status(self) -> pulumi.Input[Union[str, 'OrderState']]:
        """
        Status of the order as per the allowed status types.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: pulumi.Input[Union[str, 'OrderState']]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def comments(self) -> Optional[pulumi.Input[str]]:
        """
        Comments related to this status change.
        """
        return pulumi.get(self, "comments")

    @comments.setter
    def comments(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comments", value)


@pulumi.input_type
class PeriodicTimerSourceInfoArgs:
    def __init__(__self__, *,
                 schedule: pulumi.Input[str],
                 start_time: pulumi.Input[str],
                 topic: Optional[pulumi.Input[str]] = None):
        """
        Periodic timer event source.
        :param pulumi.Input[str] schedule: Periodic frequency at which timer event needs to be raised. Supports daily, hourly, minutes, and seconds.
        :param pulumi.Input[str] start_time: The time of the day that results in a valid trigger. Schedule is computed with reference to the time specified up to seconds. If timezone is not specified the time will considered to be in device timezone. The value will always be returned as UTC time.
        :param pulumi.Input[str] topic: Topic where periodic events are published to IoT device.
        """
        pulumi.set(__self__, "schedule", schedule)
        pulumi.set(__self__, "start_time", start_time)
        if topic is not None:
            pulumi.set(__self__, "topic", topic)

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Input[str]:
        """
        Periodic frequency at which timer event needs to be raised. Supports daily, hourly, minutes, and seconds.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule", value)

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Input[str]:
        """
        The time of the day that results in a valid trigger. Schedule is computed with reference to the time specified up to seconds. If timezone is not specified the time will considered to be in device timezone. The value will always be returned as UTC time.
        """
        return pulumi.get(self, "start_time")

    @start_time.setter
    def start_time(self, value: pulumi.Input[str]):
        pulumi.set(self, "start_time", value)

    @property
    @pulumi.getter
    def topic(self) -> Optional[pulumi.Input[str]]:
        """
        Topic where periodic events are published to IoT device.
        """
        return pulumi.get(self, "topic")

    @topic.setter
    def topic(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "topic", value)


@pulumi.input_type
class RefreshDetailsArgs:
    def __init__(__self__, *,
                 error_manifest_file: Optional[pulumi.Input[str]] = None,
                 in_progress_refresh_job_id: Optional[pulumi.Input[str]] = None,
                 last_completed_refresh_job_time_in_utc: Optional[pulumi.Input[str]] = None,
                 last_job: Optional[pulumi.Input[str]] = None):
        """
        Fields for tracking refresh job on the share.
        :param pulumi.Input[str] error_manifest_file: Indicates the relative path of the error xml for the last refresh job on this particular share, if any. This could be a failed job or a successful job.
        :param pulumi.Input[str] in_progress_refresh_job_id: If a refresh share job is currently in progress on this share, this field indicates the ARM resource ID of that job. The field is empty if no job is in progress.
        :param pulumi.Input[str] last_completed_refresh_job_time_in_utc: Indicates the completed time for the last refresh job on this particular share, if any.This could be a failed job or a successful job.
        :param pulumi.Input[str] last_job: Indicates the id of the last refresh job on this particular share,if any. This could be a failed job or a successful job.
        """
        if error_manifest_file is not None:
            pulumi.set(__self__, "error_manifest_file", error_manifest_file)
        if in_progress_refresh_job_id is not None:
            pulumi.set(__self__, "in_progress_refresh_job_id", in_progress_refresh_job_id)
        if last_completed_refresh_job_time_in_utc is not None:
            pulumi.set(__self__, "last_completed_refresh_job_time_in_utc", last_completed_refresh_job_time_in_utc)
        if last_job is not None:
            pulumi.set(__self__, "last_job", last_job)

    @property
    @pulumi.getter(name="errorManifestFile")
    def error_manifest_file(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the relative path of the error xml for the last refresh job on this particular share, if any. This could be a failed job or a successful job.
        """
        return pulumi.get(self, "error_manifest_file")

    @error_manifest_file.setter
    def error_manifest_file(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "error_manifest_file", value)

    @property
    @pulumi.getter(name="inProgressRefreshJobId")
    def in_progress_refresh_job_id(self) -> Optional[pulumi.Input[str]]:
        """
        If a refresh share job is currently in progress on this share, this field indicates the ARM resource ID of that job. The field is empty if no job is in progress.
        """
        return pulumi.get(self, "in_progress_refresh_job_id")

    @in_progress_refresh_job_id.setter
    def in_progress_refresh_job_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "in_progress_refresh_job_id", value)

    @property
    @pulumi.getter(name="lastCompletedRefreshJobTimeInUTC")
    def last_completed_refresh_job_time_in_utc(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the completed time for the last refresh job on this particular share, if any.This could be a failed job or a successful job.
        """
        return pulumi.get(self, "last_completed_refresh_job_time_in_utc")

    @last_completed_refresh_job_time_in_utc.setter
    def last_completed_refresh_job_time_in_utc(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_completed_refresh_job_time_in_utc", value)

    @property
    @pulumi.getter(name="lastJob")
    def last_job(self) -> Optional[pulumi.Input[str]]:
        """
        Indicates the id of the last refresh job on this particular share,if any. This could be a failed job or a successful job.
        """
        return pulumi.get(self, "last_job")

    @last_job.setter
    def last_job(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_job", value)


@pulumi.input_type
class RoleSinkInfoArgs:
    def __init__(__self__, *,
                 role_id: pulumi.Input[str]):
        """
        Compute role against which events will be raised.
        :param pulumi.Input[str] role_id: Compute role ID.
        """
        pulumi.set(__self__, "role_id", role_id)

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> pulumi.Input[str]:
        """
        Compute role ID.
        """
        return pulumi.get(self, "role_id")

    @role_id.setter
    def role_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_id", value)


@pulumi.input_type
class ShareAccessRightArgs:
    def __init__(__self__, *,
                 access_type: pulumi.Input[Union[str, 'ShareAccessType']],
                 share_id: pulumi.Input[str]):
        """
        Specifies the mapping between this particular user and the type of access he has on shares on this device.
        :param pulumi.Input[Union[str, 'ShareAccessType']] access_type: Type of access to be allowed on the share for this user.
        :param pulumi.Input[str] share_id: The share ID.
        """
        pulumi.set(__self__, "access_type", access_type)
        pulumi.set(__self__, "share_id", share_id)

    @property
    @pulumi.getter(name="accessType")
    def access_type(self) -> pulumi.Input[Union[str, 'ShareAccessType']]:
        """
        Type of access to be allowed on the share for this user.
        """
        return pulumi.get(self, "access_type")

    @access_type.setter
    def access_type(self, value: pulumi.Input[Union[str, 'ShareAccessType']]):
        pulumi.set(self, "access_type", value)

    @property
    @pulumi.getter(name="shareId")
    def share_id(self) -> pulumi.Input[str]:
        """
        The share ID.
        """
        return pulumi.get(self, "share_id")

    @share_id.setter
    def share_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "share_id", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[Union[str, 'SkuName']]] = None,
                 tier: Optional[pulumi.Input[Union[str, 'SkuTier']]] = None):
        """
        The SKU type.
        :param pulumi.Input[Union[str, 'SkuName']] name: SKU name.
        :param pulumi.Input[Union[str, 'SkuTier']] tier: The SKU tier. This is based on the SKU name.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[Union[str, 'SkuName']]]:
        """
        SKU name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[Union[str, 'SkuName']]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[Union[str, 'SkuTier']]]:
        """
        The SKU tier. This is based on the SKU name.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[Union[str, 'SkuTier']]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class SymmetricKeyArgs:
    def __init__(__self__, *,
                 connection_string: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']] = None):
        """
        Symmetric key for authentication.
        :param pulumi.Input['AsymmetricEncryptedSecretArgs'] connection_string: Connection string based on the symmetric key.
        """
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]:
        """
        Connection string based on the symmetric key.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input['AsymmetricEncryptedSecretArgs']]):
        pulumi.set(self, "connection_string", value)


@pulumi.input_type
class UserAccessRightArgs:
    def __init__(__self__, *,
                 access_type: pulumi.Input[Union[str, 'ShareAccessType']],
                 user_id: pulumi.Input[str]):
        """
        The mapping between a particular user and the access type on the SMB share.
        :param pulumi.Input[Union[str, 'ShareAccessType']] access_type: Type of access to be allowed for the user.
        :param pulumi.Input[str] user_id: User ID (already existing in the device).
        """
        pulumi.set(__self__, "access_type", access_type)
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter(name="accessType")
    def access_type(self) -> pulumi.Input[Union[str, 'ShareAccessType']]:
        """
        Type of access to be allowed for the user.
        """
        return pulumi.get(self, "access_type")

    @access_type.setter
    def access_type(self, value: pulumi.Input[Union[str, 'ShareAccessType']]):
        pulumi.set(self, "access_type", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        User ID (already existing in the device).
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)


