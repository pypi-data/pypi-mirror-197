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
    'GetPrivateStoreCollectionOfferResult',
    'AwaitableGetPrivateStoreCollectionOfferResult',
    'get_private_store_collection_offer',
    'get_private_store_collection_offer_output',
]

@pulumi.output_type
class GetPrivateStoreCollectionOfferResult:
    """
    The privateStore offer data structure.
    """
    def __init__(__self__, created_at=None, e_tag=None, icon_file_uris=None, id=None, modified_at=None, name=None, offer_display_name=None, plans=None, private_store_id=None, publisher_display_name=None, specific_plan_ids_limitation=None, system_data=None, type=None, unique_offer_id=None, update_suppressed_due_idempotence=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if e_tag and not isinstance(e_tag, str):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, "e_tag", e_tag)
        if icon_file_uris and not isinstance(icon_file_uris, dict):
            raise TypeError("Expected argument 'icon_file_uris' to be a dict")
        pulumi.set(__self__, "icon_file_uris", icon_file_uris)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if modified_at and not isinstance(modified_at, str):
            raise TypeError("Expected argument 'modified_at' to be a str")
        pulumi.set(__self__, "modified_at", modified_at)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if offer_display_name and not isinstance(offer_display_name, str):
            raise TypeError("Expected argument 'offer_display_name' to be a str")
        pulumi.set(__self__, "offer_display_name", offer_display_name)
        if plans and not isinstance(plans, list):
            raise TypeError("Expected argument 'plans' to be a list")
        pulumi.set(__self__, "plans", plans)
        if private_store_id and not isinstance(private_store_id, str):
            raise TypeError("Expected argument 'private_store_id' to be a str")
        pulumi.set(__self__, "private_store_id", private_store_id)
        if publisher_display_name and not isinstance(publisher_display_name, str):
            raise TypeError("Expected argument 'publisher_display_name' to be a str")
        pulumi.set(__self__, "publisher_display_name", publisher_display_name)
        if specific_plan_ids_limitation and not isinstance(specific_plan_ids_limitation, list):
            raise TypeError("Expected argument 'specific_plan_ids_limitation' to be a list")
        pulumi.set(__self__, "specific_plan_ids_limitation", specific_plan_ids_limitation)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if unique_offer_id and not isinstance(unique_offer_id, str):
            raise TypeError("Expected argument 'unique_offer_id' to be a str")
        pulumi.set(__self__, "unique_offer_id", unique_offer_id)
        if update_suppressed_due_idempotence and not isinstance(update_suppressed_due_idempotence, bool):
            raise TypeError("Expected argument 'update_suppressed_due_idempotence' to be a bool")
        pulumi.set(__self__, "update_suppressed_due_idempotence", update_suppressed_due_idempotence)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Private store offer creation date
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> Optional[str]:
        """
        Identifier for purposes of race condition
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter(name="iconFileUris")
    def icon_file_uris(self) -> Optional[Mapping[str, str]]:
        """
        Icon File Uris
        """
        return pulumi.get(self, "icon_file_uris")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="modifiedAt")
    def modified_at(self) -> str:
        """
        Private store offer modification date
        """
        return pulumi.get(self, "modified_at")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="offerDisplayName")
    def offer_display_name(self) -> str:
        """
        It will be displayed prominently in the marketplace
        """
        return pulumi.get(self, "offer_display_name")

    @property
    @pulumi.getter
    def plans(self) -> Optional[Sequence['outputs.PlanResponse']]:
        """
        Offer plans
        """
        return pulumi.get(self, "plans")

    @property
    @pulumi.getter(name="privateStoreId")
    def private_store_id(self) -> str:
        """
        Private store unique id
        """
        return pulumi.get(self, "private_store_id")

    @property
    @pulumi.getter(name="publisherDisplayName")
    def publisher_display_name(self) -> str:
        """
        Publisher name that will be displayed prominently in the marketplace
        """
        return pulumi.get(self, "publisher_display_name")

    @property
    @pulumi.getter(name="specificPlanIdsLimitation")
    def specific_plan_ids_limitation(self) -> Optional[Sequence[str]]:
        """
        Plan ids limitation for this offer
        """
        return pulumi.get(self, "specific_plan_ids_limitation")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="uniqueOfferId")
    def unique_offer_id(self) -> str:
        """
        Offers unique id
        """
        return pulumi.get(self, "unique_offer_id")

    @property
    @pulumi.getter(name="updateSuppressedDueIdempotence")
    def update_suppressed_due_idempotence(self) -> Optional[bool]:
        """
        Indicating whether the offer was not updated to db (true = not updated). If the allow list is identical to the existed one in db, the offer would not be updated.
        """
        return pulumi.get(self, "update_suppressed_due_idempotence")


class AwaitableGetPrivateStoreCollectionOfferResult(GetPrivateStoreCollectionOfferResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPrivateStoreCollectionOfferResult(
            created_at=self.created_at,
            e_tag=self.e_tag,
            icon_file_uris=self.icon_file_uris,
            id=self.id,
            modified_at=self.modified_at,
            name=self.name,
            offer_display_name=self.offer_display_name,
            plans=self.plans,
            private_store_id=self.private_store_id,
            publisher_display_name=self.publisher_display_name,
            specific_plan_ids_limitation=self.specific_plan_ids_limitation,
            system_data=self.system_data,
            type=self.type,
            unique_offer_id=self.unique_offer_id,
            update_suppressed_due_idempotence=self.update_suppressed_due_idempotence)


def get_private_store_collection_offer(collection_id: Optional[str] = None,
                                       offer_id: Optional[str] = None,
                                       private_store_id: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPrivateStoreCollectionOfferResult:
    """
    Gets information about a specific offer.


    :param str collection_id: The collection ID
    :param str offer_id: The offer ID to update or delete
    :param str private_store_id: The store ID - must use the tenant ID
    """
    __args__ = dict()
    __args__['collectionId'] = collection_id
    __args__['offerId'] = offer_id
    __args__['privateStoreId'] = private_store_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:marketplace/v20210601:getPrivateStoreCollectionOffer', __args__, opts=opts, typ=GetPrivateStoreCollectionOfferResult).value

    return AwaitableGetPrivateStoreCollectionOfferResult(
        created_at=__ret__.created_at,
        e_tag=__ret__.e_tag,
        icon_file_uris=__ret__.icon_file_uris,
        id=__ret__.id,
        modified_at=__ret__.modified_at,
        name=__ret__.name,
        offer_display_name=__ret__.offer_display_name,
        plans=__ret__.plans,
        private_store_id=__ret__.private_store_id,
        publisher_display_name=__ret__.publisher_display_name,
        specific_plan_ids_limitation=__ret__.specific_plan_ids_limitation,
        system_data=__ret__.system_data,
        type=__ret__.type,
        unique_offer_id=__ret__.unique_offer_id,
        update_suppressed_due_idempotence=__ret__.update_suppressed_due_idempotence)


@_utilities.lift_output_func(get_private_store_collection_offer)
def get_private_store_collection_offer_output(collection_id: Optional[pulumi.Input[str]] = None,
                                              offer_id: Optional[pulumi.Input[str]] = None,
                                              private_store_id: Optional[pulumi.Input[str]] = None,
                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPrivateStoreCollectionOfferResult]:
    """
    Gets information about a specific offer.


    :param str collection_id: The collection ID
    :param str offer_id: The offer ID to update or delete
    :param str private_store_id: The store ID - must use the tenant ID
    """
    ...
