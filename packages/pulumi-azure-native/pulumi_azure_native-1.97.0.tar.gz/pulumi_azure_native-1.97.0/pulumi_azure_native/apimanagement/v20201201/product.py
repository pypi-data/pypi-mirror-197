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

__all__ = ['ProductArgs', 'Product']

@pulumi.input_type
class ProductArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 service_name: pulumi.Input[str],
                 approval_required: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input['ProductState']] = None,
                 subscription_required: Optional[pulumi.Input[bool]] = None,
                 subscriptions_limit: Optional[pulumi.Input[int]] = None,
                 terms: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Product resource.
        :param pulumi.Input[str] display_name: Product name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input[bool] approval_required: whether subscription approval is required. If false, new subscriptions will be approved automatically enabling developers to call the product’s APIs immediately after subscribing. If true, administrators must manually approve the subscription before the developer can any of the product’s APIs. Can be present only if subscriptionRequired property is present and has a value of false.
        :param pulumi.Input[str] description: Product description. May include HTML formatting tags.
        :param pulumi.Input[str] product_id: Product identifier. Must be unique in the current API Management service instance.
        :param pulumi.Input['ProductState'] state: whether product is published or not. Published products are discoverable by users of developer portal. Non published products are visible only to administrators. Default state of Product is notPublished.
        :param pulumi.Input[bool] subscription_required: Whether a product subscription is required for accessing APIs included in this product. If true, the product is referred to as "protected" and a valid subscription key is required for a request to an API included in the product to succeed. If false, the product is referred to as "open" and requests to an API included in the product can be made without a subscription key. If property is omitted when creating a new product it's value is assumed to be true.
        :param pulumi.Input[int] subscriptions_limit: Whether the number of subscriptions a user can have to this product at the same time. Set to null or omit to allow unlimited per user subscriptions. Can be present only if subscriptionRequired property is present and has a value of false.
        :param pulumi.Input[str] terms: Product terms of use. Developers trying to subscribe to the product will be presented and required to accept these terms before they can complete the subscription process.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "service_name", service_name)
        if approval_required is not None:
            pulumi.set(__self__, "approval_required", approval_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if product_id is not None:
            pulumi.set(__self__, "product_id", product_id)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if subscription_required is not None:
            pulumi.set(__self__, "subscription_required", subscription_required)
        if subscriptions_limit is not None:
            pulumi.set(__self__, "subscriptions_limit", subscriptions_limit)
        if terms is not None:
            pulumi.set(__self__, "terms", terms)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Product name.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serviceName")
    def service_name(self) -> pulumi.Input[str]:
        """
        The name of the API Management service.
        """
        return pulumi.get(self, "service_name")

    @service_name.setter
    def service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "service_name", value)

    @property
    @pulumi.getter(name="approvalRequired")
    def approval_required(self) -> Optional[pulumi.Input[bool]]:
        """
        whether subscription approval is required. If false, new subscriptions will be approved automatically enabling developers to call the product’s APIs immediately after subscribing. If true, administrators must manually approve the subscription before the developer can any of the product’s APIs. Can be present only if subscriptionRequired property is present and has a value of false.
        """
        return pulumi.get(self, "approval_required")

    @approval_required.setter
    def approval_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "approval_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Product description. May include HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> Optional[pulumi.Input[str]]:
        """
        Product identifier. Must be unique in the current API Management service instance.
        """
        return pulumi.get(self, "product_id")

    @product_id.setter
    def product_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product_id", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input['ProductState']]:
        """
        whether product is published or not. Published products are discoverable by users of developer portal. Non published products are visible only to administrators. Default state of Product is notPublished.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input['ProductState']]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter(name="subscriptionRequired")
    def subscription_required(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether a product subscription is required for accessing APIs included in this product. If true, the product is referred to as "protected" and a valid subscription key is required for a request to an API included in the product to succeed. If false, the product is referred to as "open" and requests to an API included in the product can be made without a subscription key. If property is omitted when creating a new product it's value is assumed to be true.
        """
        return pulumi.get(self, "subscription_required")

    @subscription_required.setter
    def subscription_required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "subscription_required", value)

    @property
    @pulumi.getter(name="subscriptionsLimit")
    def subscriptions_limit(self) -> Optional[pulumi.Input[int]]:
        """
        Whether the number of subscriptions a user can have to this product at the same time. Set to null or omit to allow unlimited per user subscriptions. Can be present only if subscriptionRequired property is present and has a value of false.
        """
        return pulumi.get(self, "subscriptions_limit")

    @subscriptions_limit.setter
    def subscriptions_limit(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "subscriptions_limit", value)

    @property
    @pulumi.getter
    def terms(self) -> Optional[pulumi.Input[str]]:
        """
        Product terms of use. Developers trying to subscribe to the product will be presented and required to accept these terms before they can complete the subscription process.
        """
        return pulumi.get(self, "terms")

    @terms.setter
    def terms(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "terms", value)


class Product(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 approval_required: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input['ProductState']] = None,
                 subscription_required: Optional[pulumi.Input[bool]] = None,
                 subscriptions_limit: Optional[pulumi.Input[int]] = None,
                 terms: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Product details.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] approval_required: whether subscription approval is required. If false, new subscriptions will be approved automatically enabling developers to call the product’s APIs immediately after subscribing. If true, administrators must manually approve the subscription before the developer can any of the product’s APIs. Can be present only if subscriptionRequired property is present and has a value of false.
        :param pulumi.Input[str] description: Product description. May include HTML formatting tags.
        :param pulumi.Input[str] display_name: Product name.
        :param pulumi.Input[str] product_id: Product identifier. Must be unique in the current API Management service instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] service_name: The name of the API Management service.
        :param pulumi.Input['ProductState'] state: whether product is published or not. Published products are discoverable by users of developer portal. Non published products are visible only to administrators. Default state of Product is notPublished.
        :param pulumi.Input[bool] subscription_required: Whether a product subscription is required for accessing APIs included in this product. If true, the product is referred to as "protected" and a valid subscription key is required for a request to an API included in the product to succeed. If false, the product is referred to as "open" and requests to an API included in the product can be made without a subscription key. If property is omitted when creating a new product it's value is assumed to be true.
        :param pulumi.Input[int] subscriptions_limit: Whether the number of subscriptions a user can have to this product at the same time. Set to null or omit to allow unlimited per user subscriptions. Can be present only if subscriptionRequired property is present and has a value of false.
        :param pulumi.Input[str] terms: Product terms of use. Developers trying to subscribe to the product will be presented and required to accept these terms before they can complete the subscription process.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProductArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Product details.

        :param str resource_name: The name of the resource.
        :param ProductArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProductArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 approval_required: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input['ProductState']] = None,
                 subscription_required: Optional[pulumi.Input[bool]] = None,
                 subscriptions_limit: Optional[pulumi.Input[int]] = None,
                 terms: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProductArgs.__new__(ProductArgs)

            __props__.__dict__["approval_required"] = approval_required
            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["product_id"] = product_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if service_name is None and not opts.urn:
                raise TypeError("Missing required property 'service_name'")
            __props__.__dict__["service_name"] = service_name
            __props__.__dict__["state"] = state
            __props__.__dict__["subscription_required"] = subscription_required
            __props__.__dict__["subscriptions_limit"] = subscriptions_limit
            __props__.__dict__["terms"] = terms
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:apimanagement:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20160707:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20161010:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20170301:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20180101:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20180601preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20190101:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20191201:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20191201preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20200601preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20210101preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20210401preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20210801:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20211201preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20220401preview:Product"), pulumi.Alias(type_="azure-native:apimanagement/v20220801:Product")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Product, __self__).__init__(
            'azure-native:apimanagement/v20201201:Product',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Product':
        """
        Get an existing Product resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ProductArgs.__new__(ProductArgs)

        __props__.__dict__["approval_required"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["subscription_required"] = None
        __props__.__dict__["subscriptions_limit"] = None
        __props__.__dict__["terms"] = None
        __props__.__dict__["type"] = None
        return Product(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="approvalRequired")
    def approval_required(self) -> pulumi.Output[Optional[bool]]:
        """
        whether subscription approval is required. If false, new subscriptions will be approved automatically enabling developers to call the product’s APIs immediately after subscribing. If true, administrators must manually approve the subscription before the developer can any of the product’s APIs. Can be present only if subscriptionRequired property is present and has a value of false.
        """
        return pulumi.get(self, "approval_required")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Product description. May include HTML formatting tags.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Product name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[Optional[str]]:
        """
        whether product is published or not. Published products are discoverable by users of developer portal. Non published products are visible only to administrators. Default state of Product is notPublished.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="subscriptionRequired")
    def subscription_required(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether a product subscription is required for accessing APIs included in this product. If true, the product is referred to as "protected" and a valid subscription key is required for a request to an API included in the product to succeed. If false, the product is referred to as "open" and requests to an API included in the product can be made without a subscription key. If property is omitted when creating a new product it's value is assumed to be true.
        """
        return pulumi.get(self, "subscription_required")

    @property
    @pulumi.getter(name="subscriptionsLimit")
    def subscriptions_limit(self) -> pulumi.Output[Optional[int]]:
        """
        Whether the number of subscriptions a user can have to this product at the same time. Set to null or omit to allow unlimited per user subscriptions. Can be present only if subscriptionRequired property is present and has a value of false.
        """
        return pulumi.get(self, "subscriptions_limit")

    @property
    @pulumi.getter
    def terms(self) -> pulumi.Output[Optional[str]]:
        """
        Product terms of use. Developers trying to subscribe to the product will be presented and required to accept these terms before they can complete the subscription process.
        """
        return pulumi.get(self, "terms")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

