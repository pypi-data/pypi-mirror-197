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
    'GetSiteLogsConfigResult',
    'AwaitableGetSiteLogsConfigResult',
    'get_site_logs_config',
    'get_site_logs_config_output',
]

warnings.warn("""Version 2015-08-01 will be removed in v2 of the provider.""", DeprecationWarning)

@pulumi.output_type
class GetSiteLogsConfigResult:
    """
    Configuration of Azure web site
    """
    def __init__(__self__, application_logs=None, detailed_error_messages=None, failed_requests_tracing=None, http_logs=None, id=None, kind=None, location=None, name=None, tags=None, type=None):
        if application_logs and not isinstance(application_logs, dict):
            raise TypeError("Expected argument 'application_logs' to be a dict")
        pulumi.set(__self__, "application_logs", application_logs)
        if detailed_error_messages and not isinstance(detailed_error_messages, dict):
            raise TypeError("Expected argument 'detailed_error_messages' to be a dict")
        pulumi.set(__self__, "detailed_error_messages", detailed_error_messages)
        if failed_requests_tracing and not isinstance(failed_requests_tracing, dict):
            raise TypeError("Expected argument 'failed_requests_tracing' to be a dict")
        pulumi.set(__self__, "failed_requests_tracing", failed_requests_tracing)
        if http_logs and not isinstance(http_logs, dict):
            raise TypeError("Expected argument 'http_logs' to be a dict")
        pulumi.set(__self__, "http_logs", http_logs)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="applicationLogs")
    def application_logs(self) -> Optional['outputs.ApplicationLogsConfigResponse']:
        """
        Application logs configuration
        """
        return pulumi.get(self, "application_logs")

    @property
    @pulumi.getter(name="detailedErrorMessages")
    def detailed_error_messages(self) -> Optional['outputs.EnabledConfigResponse']:
        """
        Detailed error messages configuration
        """
        return pulumi.get(self, "detailed_error_messages")

    @property
    @pulumi.getter(name="failedRequestsTracing")
    def failed_requests_tracing(self) -> Optional['outputs.EnabledConfigResponse']:
        """
        Failed requests tracing configuration
        """
        return pulumi.get(self, "failed_requests_tracing")

    @property
    @pulumi.getter(name="httpLogs")
    def http_logs(self) -> Optional['outputs.HttpLogsConfigResponse']:
        """
        Http logs configuration
        """
        return pulumi.get(self, "http_logs")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetSiteLogsConfigResult(GetSiteLogsConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSiteLogsConfigResult(
            application_logs=self.application_logs,
            detailed_error_messages=self.detailed_error_messages,
            failed_requests_tracing=self.failed_requests_tracing,
            http_logs=self.http_logs,
            id=self.id,
            kind=self.kind,
            location=self.location,
            name=self.name,
            tags=self.tags,
            type=self.type)


def get_site_logs_config(name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSiteLogsConfigResult:
    """
    Configuration of Azure web site


    :param str name: Name of web app
    :param str resource_group_name: Name of resource group
    """
    pulumi.log.warn("""get_site_logs_config is deprecated: Version 2015-08-01 will be removed in v2 of the provider.""")
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20150801:getSiteLogsConfig', __args__, opts=opts, typ=GetSiteLogsConfigResult).value

    return AwaitableGetSiteLogsConfigResult(
        application_logs=__ret__.application_logs,
        detailed_error_messages=__ret__.detailed_error_messages,
        failed_requests_tracing=__ret__.failed_requests_tracing,
        http_logs=__ret__.http_logs,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        name=__ret__.name,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_site_logs_config)
def get_site_logs_config_output(name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSiteLogsConfigResult]:
    """
    Configuration of Azure web site


    :param str name: Name of web app
    :param str resource_group_name: Name of resource group
    """
    pulumi.log.warn("""get_site_logs_config is deprecated: Version 2015-08-01 will be removed in v2 of the provider.""")
    ...
