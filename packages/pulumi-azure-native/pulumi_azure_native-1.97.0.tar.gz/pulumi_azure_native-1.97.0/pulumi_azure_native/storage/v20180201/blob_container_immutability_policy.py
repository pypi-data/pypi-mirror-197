# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['BlobContainerImmutabilityPolicyArgs', 'BlobContainerImmutabilityPolicy']

@pulumi.input_type
class BlobContainerImmutabilityPolicyArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 container_name: pulumi.Input[str],
                 immutability_period_since_creation_in_days: pulumi.Input[int],
                 resource_group_name: pulumi.Input[str],
                 immutability_policy_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a BlobContainerImmutabilityPolicy resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] container_name: The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
        :param pulumi.Input[int] immutability_period_since_creation_in_days: The immutability period for the blobs in the container since the policy creation, in days.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] immutability_policy_name: The name of the blob container immutabilityPolicy within the specified storage account. ImmutabilityPolicy Name must be 'default'
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "container_name", container_name)
        pulumi.set(__self__, "immutability_period_since_creation_in_days", immutability_period_since_creation_in_days)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if immutability_policy_name is not None:
            pulumi.set(__self__, "immutability_policy_name", immutability_policy_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Input[str]:
        """
        The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="immutabilityPeriodSinceCreationInDays")
    def immutability_period_since_creation_in_days(self) -> pulumi.Input[int]:
        """
        The immutability period for the blobs in the container since the policy creation, in days.
        """
        return pulumi.get(self, "immutability_period_since_creation_in_days")

    @immutability_period_since_creation_in_days.setter
    def immutability_period_since_creation_in_days(self, value: pulumi.Input[int]):
        pulumi.set(self, "immutability_period_since_creation_in_days", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the user's subscription. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="immutabilityPolicyName")
    def immutability_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the blob container immutabilityPolicy within the specified storage account. ImmutabilityPolicy Name must be 'default'
        """
        return pulumi.get(self, "immutability_policy_name")

    @immutability_policy_name.setter
    def immutability_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "immutability_policy_name", value)


warnings.warn("""Version 2018-02-01 will be removed in v2 of the provider.""", DeprecationWarning)


class BlobContainerImmutabilityPolicy(pulumi.CustomResource):
    warnings.warn("""Version 2018-02-01 will be removed in v2 of the provider.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 immutability_period_since_creation_in_days: Optional[pulumi.Input[int]] = None,
                 immutability_policy_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ImmutabilityPolicy property of a blob container, including Id, resource name, resource type, Etag.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] container_name: The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
        :param pulumi.Input[int] immutability_period_since_creation_in_days: The immutability period for the blobs in the container since the policy creation, in days.
        :param pulumi.Input[str] immutability_policy_name: The name of the blob container immutabilityPolicy within the specified storage account. ImmutabilityPolicy Name must be 'default'
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BlobContainerImmutabilityPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ImmutabilityPolicy property of a blob container, including Id, resource name, resource type, Etag.

        :param str resource_name: The name of the resource.
        :param BlobContainerImmutabilityPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BlobContainerImmutabilityPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 immutability_period_since_creation_in_days: Optional[pulumi.Input[int]] = None,
                 immutability_policy_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""BlobContainerImmutabilityPolicy is deprecated: Version 2018-02-01 will be removed in v2 of the provider.""")
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BlobContainerImmutabilityPolicyArgs.__new__(BlobContainerImmutabilityPolicyArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            if container_name is None and not opts.urn:
                raise TypeError("Missing required property 'container_name'")
            __props__.__dict__["container_name"] = container_name
            if immutability_period_since_creation_in_days is None and not opts.urn:
                raise TypeError("Missing required property 'immutability_period_since_creation_in_days'")
            __props__.__dict__["immutability_period_since_creation_in_days"] = immutability_period_since_creation_in_days
            __props__.__dict__["immutability_policy_name"] = immutability_policy_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:storage:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20180301preview:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20180701:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20181101:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20190401:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20190601:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20200801preview:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20210101:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20210201:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20210401:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20210601:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20210801:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20210901:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20220501:BlobContainerImmutabilityPolicy"), pulumi.Alias(type_="azure-native:storage/v20220901:BlobContainerImmutabilityPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BlobContainerImmutabilityPolicy, __self__).__init__(
            'azure-native:storage/v20180201:BlobContainerImmutabilityPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BlobContainerImmutabilityPolicy':
        """
        Get an existing BlobContainerImmutabilityPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BlobContainerImmutabilityPolicyArgs.__new__(BlobContainerImmutabilityPolicyArgs)

        __props__.__dict__["etag"] = None
        __props__.__dict__["immutability_period_since_creation_in_days"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["state"] = None
        __props__.__dict__["type"] = None
        return BlobContainerImmutabilityPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Resource Etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="immutabilityPeriodSinceCreationInDays")
    def immutability_period_since_creation_in_days(self) -> pulumi.Output[int]:
        """
        The immutability period for the blobs in the container since the policy creation, in days.
        """
        return pulumi.get(self, "immutability_period_since_creation_in_days")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The ImmutabilityPolicy state of a blob container, possible values include: Locked and Unlocked.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

