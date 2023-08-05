# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ListVideoStreamingTokenResult',
    'AwaitableListVideoStreamingTokenResult',
    'list_video_streaming_token',
    'list_video_streaming_token_output',
]

@pulumi.output_type
class ListVideoStreamingTokenResult:
    """
    Video streaming token grants access to the video streaming URLs which can be used by an compatible HLS or DASH player.
    """
    def __init__(__self__, expiration_date=None, token=None):
        if expiration_date and not isinstance(expiration_date, str):
            raise TypeError("Expected argument 'expiration_date' to be a str")
        pulumi.set(__self__, "expiration_date", expiration_date)
        if token and not isinstance(token, str):
            raise TypeError("Expected argument 'token' to be a str")
        pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> str:
        """
        The streaming token expiration date in ISO8601 format (eg. 2021-01-01T00:00:00Z).
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter
    def token(self) -> str:
        """
        The streaming token value to be added to the video streaming URL as the value for a "token" query string parameter. The token is specific to a single video.
        """
        return pulumi.get(self, "token")


class AwaitableListVideoStreamingTokenResult(ListVideoStreamingTokenResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListVideoStreamingTokenResult(
            expiration_date=self.expiration_date,
            token=self.token)


def list_video_streaming_token(account_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               video_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListVideoStreamingTokenResult:
    """
    Generates a streaming token used for authenticating video playback.
    API Version: 2021-05-01-preview.


    :param str account_name: The Azure Video Analyzer account name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str video_name: The name of the video to generate a token for playback.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['videoName'] = video_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:videoanalyzer:listVideoStreamingToken', __args__, opts=opts, typ=ListVideoStreamingTokenResult).value

    return AwaitableListVideoStreamingTokenResult(
        expiration_date=__ret__.expiration_date,
        token=__ret__.token)


@_utilities.lift_output_func(list_video_streaming_token)
def list_video_streaming_token_output(account_name: Optional[pulumi.Input[str]] = None,
                                      resource_group_name: Optional[pulumi.Input[str]] = None,
                                      video_name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListVideoStreamingTokenResult]:
    """
    Generates a streaming token used for authenticating video playback.
    API Version: 2021-05-01-preview.


    :param str account_name: The Azure Video Analyzer account name.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str video_name: The name of the video to generate a token for playback.
    """
    ...
