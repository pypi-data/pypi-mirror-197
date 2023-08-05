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
    'GetSAPAvailabilityZoneDetailsResult',
    'AwaitableGetSAPAvailabilityZoneDetailsResult',
    'get_sap_availability_zone_details',
    'get_sap_availability_zone_details_output',
]

@pulumi.output_type
class GetSAPAvailabilityZoneDetailsResult:
    """
    The list of supported availability zone pairs which are part of SAP HA deployment.
    """
    def __init__(__self__, availability_zone_pairs=None):
        if availability_zone_pairs and not isinstance(availability_zone_pairs, list):
            raise TypeError("Expected argument 'availability_zone_pairs' to be a list")
        pulumi.set(__self__, "availability_zone_pairs", availability_zone_pairs)

    @property
    @pulumi.getter(name="availabilityZonePairs")
    def availability_zone_pairs(self) -> Optional[Sequence['outputs.SAPAvailabilityZonePairResponse']]:
        """
        Gets the list of availability zone pairs.
        """
        return pulumi.get(self, "availability_zone_pairs")


class AwaitableGetSAPAvailabilityZoneDetailsResult(GetSAPAvailabilityZoneDetailsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSAPAvailabilityZoneDetailsResult(
            availability_zone_pairs=self.availability_zone_pairs)


def get_sap_availability_zone_details(app_location: Optional[str] = None,
                                      database_type: Optional[Union[str, 'SAPDatabaseType']] = None,
                                      location: Optional[str] = None,
                                      sap_product: Optional[Union[str, 'SAPProductType']] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSAPAvailabilityZoneDetailsResult:
    """
    Get the recommended SAP Availability Zone Pair Details for your region.


    :param str app_location: The geo-location where the SAP resources will be created.
    :param Union[str, 'SAPDatabaseType'] database_type: The database type. Eg: HANA, DB2, etc
    :param str location: The name of Azure region.
    :param Union[str, 'SAPProductType'] sap_product: Defines the SAP Product type.
    """
    __args__ = dict()
    __args__['appLocation'] = app_location
    __args__['databaseType'] = database_type
    __args__['location'] = location
    __args__['sapProduct'] = sap_product
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:workloads/v20221101preview:getSAPAvailabilityZoneDetails', __args__, opts=opts, typ=GetSAPAvailabilityZoneDetailsResult).value

    return AwaitableGetSAPAvailabilityZoneDetailsResult(
        availability_zone_pairs=__ret__.availability_zone_pairs)


@_utilities.lift_output_func(get_sap_availability_zone_details)
def get_sap_availability_zone_details_output(app_location: Optional[pulumi.Input[str]] = None,
                                             database_type: Optional[pulumi.Input[Union[str, 'SAPDatabaseType']]] = None,
                                             location: Optional[pulumi.Input[str]] = None,
                                             sap_product: Optional[pulumi.Input[Union[str, 'SAPProductType']]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSAPAvailabilityZoneDetailsResult]:
    """
    Get the recommended SAP Availability Zone Pair Details for your region.


    :param str app_location: The geo-location where the SAP resources will be created.
    :param Union[str, 'SAPDatabaseType'] database_type: The database type. Eg: HANA, DB2, etc
    :param str location: The name of Azure region.
    :param Union[str, 'SAPProductType'] sap_product: Defines the SAP Product type.
    """
    ...
