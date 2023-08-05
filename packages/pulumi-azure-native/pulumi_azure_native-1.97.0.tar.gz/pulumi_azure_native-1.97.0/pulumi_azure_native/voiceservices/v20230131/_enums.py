# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AutoGeneratedDomainNameLabelScope',
    'CommunicationsPlatform',
    'Connectivity',
    'E911Type',
    'TeamsCodecs',
    'TestLinePurpose',
]


class AutoGeneratedDomainNameLabelScope(str, Enum):
    """
    The scope at which the auto-generated domain name can be re-used
    """
    TENANT_REUSE = "TenantReuse"
    SUBSCRIPTION_REUSE = "SubscriptionReuse"
    RESOURCE_GROUP_REUSE = "ResourceGroupReuse"
    NO_REUSE = "NoReuse"


class CommunicationsPlatform(str, Enum):
    """
    Available platform types.
    """
    OPERATOR_CONNECT = "OperatorConnect"
    TEAMS_PHONE_MOBILE = "TeamsPhoneMobile"


class Connectivity(str, Enum):
    """
    How to connect back to the operator network, e.g. MAPS
    """
    PUBLIC_ADDRESS = "PublicAddress"
    """
    This deployment connects to the operator network using a Public IP address, e.g. when using MAPS
    """


class E911Type(str, Enum):
    """
    How to handle 911 calls
    """
    STANDARD = "Standard"
    """
    Emergency calls are not handled different from other calls
    """
    DIRECT_TO_ESRP = "DirectToEsrp"
    """
    Emergency calls are routed directly to the ESRP
    """


class TeamsCodecs(str, Enum):
    """
    The voice codecs expected for communication with Teams.
    """
    PCMA = "PCMA"
    PCMU = "PCMU"
    G722 = "G722"
    G722_2 = "G722_2"
    SIL_K_8 = "SILK_8"
    SIL_K_16 = "SILK_16"


class TestLinePurpose(str, Enum):
    """
    Purpose of this test line, e.g. automated or manual testing
    """
    MANUAL = "Manual"
    AUTOMATED = "Automated"
