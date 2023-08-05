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

__all__ = [
    'DnsRecordResponse',
    'DomainPropertiesResponseVerificationRecords',
    'DomainPropertiesResponseVerificationStates',
    'SystemDataResponse',
    'VerificationStatusRecordResponse',
]

@pulumi.output_type
class DnsRecordResponse(dict):
    """
    A class that represents a VerificationStatus record.
    """
    def __init__(__self__, *,
                 name: str,
                 ttl: int,
                 type: str,
                 value: str):
        """
        A class that represents a VerificationStatus record.
        :param str name: Name of the DNS record.
        :param int ttl: Represents an expiry time in seconds to represent how long this entry can be cached by the resolver, default = 3600sec.
        :param str type: Type of the DNS record. Example: TXT
        :param str value: Value of the DNS record.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "ttl", ttl)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the DNS record.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def ttl(self) -> int:
        """
        Represents an expiry time in seconds to represent how long this entry can be cached by the resolver, default = 3600sec.
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the DNS record. Example: TXT
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the DNS record.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class DomainPropertiesResponseVerificationRecords(dict):
    """
    List of DnsRecord
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dKIM":
            suggest = "d_kim"
        elif key == "dKIM2":
            suggest = "d_kim2"
        elif key == "dMARC":
            suggest = "d_marc"
        elif key == "sPF":
            suggest = "s_pf"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainPropertiesResponseVerificationRecords. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainPropertiesResponseVerificationRecords.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainPropertiesResponseVerificationRecords.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 d_kim: Optional['outputs.DnsRecordResponse'] = None,
                 d_kim2: Optional['outputs.DnsRecordResponse'] = None,
                 d_marc: Optional['outputs.DnsRecordResponse'] = None,
                 domain: Optional['outputs.DnsRecordResponse'] = None,
                 s_pf: Optional['outputs.DnsRecordResponse'] = None):
        """
        List of DnsRecord
        :param 'DnsRecordResponse' d_kim: A class that represents a VerificationStatus record.
        :param 'DnsRecordResponse' d_kim2: A class that represents a VerificationStatus record.
        :param 'DnsRecordResponse' d_marc: A class that represents a VerificationStatus record.
        :param 'DnsRecordResponse' domain: A class that represents a VerificationStatus record.
        :param 'DnsRecordResponse' s_pf: A class that represents a VerificationStatus record.
        """
        if d_kim is not None:
            pulumi.set(__self__, "d_kim", d_kim)
        if d_kim2 is not None:
            pulumi.set(__self__, "d_kim2", d_kim2)
        if d_marc is not None:
            pulumi.set(__self__, "d_marc", d_marc)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if s_pf is not None:
            pulumi.set(__self__, "s_pf", s_pf)

    @property
    @pulumi.getter(name="dKIM")
    def d_kim(self) -> Optional['outputs.DnsRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "d_kim")

    @property
    @pulumi.getter(name="dKIM2")
    def d_kim2(self) -> Optional['outputs.DnsRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "d_kim2")

    @property
    @pulumi.getter(name="dMARC")
    def d_marc(self) -> Optional['outputs.DnsRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "d_marc")

    @property
    @pulumi.getter
    def domain(self) -> Optional['outputs.DnsRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="sPF")
    def s_pf(self) -> Optional['outputs.DnsRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "s_pf")


@pulumi.output_type
class DomainPropertiesResponseVerificationStates(dict):
    """
    List of VerificationStatusRecord
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dKIM":
            suggest = "d_kim"
        elif key == "dKIM2":
            suggest = "d_kim2"
        elif key == "dMARC":
            suggest = "d_marc"
        elif key == "sPF":
            suggest = "s_pf"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DomainPropertiesResponseVerificationStates. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DomainPropertiesResponseVerificationStates.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DomainPropertiesResponseVerificationStates.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 d_kim: Optional['outputs.VerificationStatusRecordResponse'] = None,
                 d_kim2: Optional['outputs.VerificationStatusRecordResponse'] = None,
                 d_marc: Optional['outputs.VerificationStatusRecordResponse'] = None,
                 domain: Optional['outputs.VerificationStatusRecordResponse'] = None,
                 s_pf: Optional['outputs.VerificationStatusRecordResponse'] = None):
        """
        List of VerificationStatusRecord
        :param 'VerificationStatusRecordResponse' d_kim: A class that represents a VerificationStatus record.
        :param 'VerificationStatusRecordResponse' d_kim2: A class that represents a VerificationStatus record.
        :param 'VerificationStatusRecordResponse' d_marc: A class that represents a VerificationStatus record.
        :param 'VerificationStatusRecordResponse' domain: A class that represents a VerificationStatus record.
        :param 'VerificationStatusRecordResponse' s_pf: A class that represents a VerificationStatus record.
        """
        if d_kim is not None:
            pulumi.set(__self__, "d_kim", d_kim)
        if d_kim2 is not None:
            pulumi.set(__self__, "d_kim2", d_kim2)
        if d_marc is not None:
            pulumi.set(__self__, "d_marc", d_marc)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if s_pf is not None:
            pulumi.set(__self__, "s_pf", s_pf)

    @property
    @pulumi.getter(name="dKIM")
    def d_kim(self) -> Optional['outputs.VerificationStatusRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "d_kim")

    @property
    @pulumi.getter(name="dKIM2")
    def d_kim2(self) -> Optional['outputs.VerificationStatusRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "d_kim2")

    @property
    @pulumi.getter(name="dMARC")
    def d_marc(self) -> Optional['outputs.VerificationStatusRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "d_marc")

    @property
    @pulumi.getter
    def domain(self) -> Optional['outputs.VerificationStatusRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="sPF")
    def s_pf(self) -> Optional['outputs.VerificationStatusRecordResponse']:
        """
        A class that represents a VerificationStatus record.
        """
        return pulumi.get(self, "s_pf")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


@pulumi.output_type
class VerificationStatusRecordResponse(dict):
    """
    A class that represents a VerificationStatus record.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "errorCode":
            suggest = "error_code"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in VerificationStatusRecordResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        VerificationStatusRecordResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        VerificationStatusRecordResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 error_code: str,
                 status: str):
        """
        A class that represents a VerificationStatus record.
        :param str error_code: Error code. This property will only be present if the status is UnableToVerify.
        :param str status: Status of the verification operation.
        """
        pulumi.set(__self__, "error_code", error_code)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="errorCode")
    def error_code(self) -> str:
        """
        Error code. This property will only be present if the status is UnableToVerify.
        """
        return pulumi.get(self, "error_code")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the verification operation.
        """
        return pulumi.get(self, "status")


