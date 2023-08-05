# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = ['VideoArgs', 'Video']

@pulumi.input_type
class VideoArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 video_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Video resource.
        :param pulumi.Input[str] account_name: The Azure Video Analyzer account name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] description: Optional video description provided by the user. Value can be up to 2048 characters long.
        :param pulumi.Input[str] title: Optional video title provided by the user. Value can be up to 256 characters long.
        :param pulumi.Input[str] video_name: The name of the video to create or update.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if title is not None:
            pulumi.set(__self__, "title", title)
        if video_name is not None:
            pulumi.set(__self__, "video_name", video_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The Azure Video Analyzer account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Optional video description provided by the user. Value can be up to 2048 characters long.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def title(self) -> Optional[pulumi.Input[str]]:
        """
        Optional video title provided by the user. Value can be up to 256 characters long.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "title", value)

    @property
    @pulumi.getter(name="videoName")
    def video_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the video to create or update.
        """
        return pulumi.get(self, "video_name")

    @video_name.setter
    def video_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "video_name", value)


class Video(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 video_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The representation of a single video in a Video Analyzer account.
        API Version: 2021-05-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Azure Video Analyzer account name.
        :param pulumi.Input[str] description: Optional video description provided by the user. Value can be up to 2048 characters long.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] title: Optional video title provided by the user. Value can be up to 256 characters long.
        :param pulumi.Input[str] video_name: The name of the video to create or update.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VideoArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The representation of a single video in a Video Analyzer account.
        API Version: 2021-05-01-preview.

        :param str resource_name: The name of the resource.
        :param VideoArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VideoArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 video_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VideoArgs.__new__(VideoArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["description"] = description
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["title"] = title
            __props__.__dict__["video_name"] = video_name
            __props__.__dict__["flags"] = None
            __props__.__dict__["media_info"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["streaming"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:videoanalyzer/v20210501preview:Video"), pulumi.Alias(type_="azure-native:videoanalyzer/v20211101preview:Video")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Video, __self__).__init__(
            'azure-native:videoanalyzer:Video',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Video':
        """
        Get an existing Video resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VideoArgs.__new__(VideoArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["flags"] = None
        __props__.__dict__["media_info"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["streaming"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["title"] = None
        __props__.__dict__["type"] = None
        return Video(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Optional video description provided by the user. Value can be up to 2048 characters long.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def flags(self) -> pulumi.Output['outputs.VideoFlagsResponse']:
        """
        Video flags contain information about the available video actions and its dynamic properties based on the current video state.
        """
        return pulumi.get(self, "flags")

    @property
    @pulumi.getter(name="mediaInfo")
    def media_info(self) -> pulumi.Output['outputs.VideoMediaInfoResponse']:
        """
        Contains information about the video and audio content.
        """
        return pulumi.get(self, "media_info")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def streaming(self) -> pulumi.Output['outputs.VideoStreamingResponse']:
        """
        Video streaming holds information about video streaming URLs.
        """
        return pulumi.get(self, "streaming")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[Optional[str]]:
        """
        Optional video title provided by the user. Value can be up to 256 characters long.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

