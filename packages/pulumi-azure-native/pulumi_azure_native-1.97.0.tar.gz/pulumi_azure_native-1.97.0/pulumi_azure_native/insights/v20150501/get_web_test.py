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
    'GetWebTestResult',
    'AwaitableGetWebTestResult',
    'get_web_test',
    'get_web_test_output',
]

@pulumi.output_type
class GetWebTestResult:
    """
    An Application Insights web test definition.
    """
    def __init__(__self__, configuration=None, description=None, enabled=None, frequency=None, id=None, kind=None, location=None, locations=None, name=None, provisioning_state=None, retry_enabled=None, synthetic_monitor_id=None, tags=None, timeout=None, type=None, web_test_kind=None, web_test_name=None):
        if configuration and not isinstance(configuration, dict):
            raise TypeError("Expected argument 'configuration' to be a dict")
        pulumi.set(__self__, "configuration", configuration)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if frequency and not isinstance(frequency, int):
            raise TypeError("Expected argument 'frequency' to be a int")
        pulumi.set(__self__, "frequency", frequency)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if locations and not isinstance(locations, list):
            raise TypeError("Expected argument 'locations' to be a list")
        pulumi.set(__self__, "locations", locations)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if retry_enabled and not isinstance(retry_enabled, bool):
            raise TypeError("Expected argument 'retry_enabled' to be a bool")
        pulumi.set(__self__, "retry_enabled", retry_enabled)
        if synthetic_monitor_id and not isinstance(synthetic_monitor_id, str):
            raise TypeError("Expected argument 'synthetic_monitor_id' to be a str")
        pulumi.set(__self__, "synthetic_monitor_id", synthetic_monitor_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if timeout and not isinstance(timeout, int):
            raise TypeError("Expected argument 'timeout' to be a int")
        pulumi.set(__self__, "timeout", timeout)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if web_test_kind and not isinstance(web_test_kind, str):
            raise TypeError("Expected argument 'web_test_kind' to be a str")
        pulumi.set(__self__, "web_test_kind", web_test_kind)
        if web_test_name and not isinstance(web_test_name, str):
            raise TypeError("Expected argument 'web_test_name' to be a str")
        pulumi.set(__self__, "web_test_name", web_test_name)

    @property
    @pulumi.getter
    def configuration(self) -> Optional['outputs.WebTestPropertiesResponseConfiguration']:
        """
        An XML configuration specification for a WebTest.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Purpose/user defined descriptive test for this WebTest.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Is the test actively being monitored.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def frequency(self) -> Optional[int]:
        """
        Interval in seconds between test runs for this WebTest. Default value is 300.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        The kind of web test that this web test watches. Choices are ping and multistep.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def locations(self) -> Sequence['outputs.WebTestGeolocationResponse']:
        """
        A list of where to physically run the tests from to give global coverage for accessibility of your application.
        """
        return pulumi.get(self, "locations")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Current state of this component, whether or not is has been provisioned within the resource group it is defined. Users cannot change this value but are able to read from it. Values will include Succeeded, Deploying, Canceled, and Failed.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="retryEnabled")
    def retry_enabled(self) -> Optional[bool]:
        """
        Allow for retries should this WebTest fail.
        """
        return pulumi.get(self, "retry_enabled")

    @property
    @pulumi.getter(name="syntheticMonitorId")
    def synthetic_monitor_id(self) -> str:
        """
        Unique ID of this WebTest. This is typically the same value as the Name field.
        """
        return pulumi.get(self, "synthetic_monitor_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> Optional[int]:
        """
        Seconds until this WebTest will timeout and fail. Default value is 30.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="webTestKind")
    def web_test_kind(self) -> str:
        """
        The kind of web test this is, valid choices are ping and multistep.
        """
        return pulumi.get(self, "web_test_kind")

    @property
    @pulumi.getter(name="webTestName")
    def web_test_name(self) -> str:
        """
        User defined name if this WebTest.
        """
        return pulumi.get(self, "web_test_name")


class AwaitableGetWebTestResult(GetWebTestResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebTestResult(
            configuration=self.configuration,
            description=self.description,
            enabled=self.enabled,
            frequency=self.frequency,
            id=self.id,
            kind=self.kind,
            location=self.location,
            locations=self.locations,
            name=self.name,
            provisioning_state=self.provisioning_state,
            retry_enabled=self.retry_enabled,
            synthetic_monitor_id=self.synthetic_monitor_id,
            tags=self.tags,
            timeout=self.timeout,
            type=self.type,
            web_test_kind=self.web_test_kind,
            web_test_name=self.web_test_name)


def get_web_test(resource_group_name: Optional[str] = None,
                 web_test_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebTestResult:
    """
    Get a specific Application Insights web test definition.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str web_test_name: The name of the Application Insights webtest resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['webTestName'] = web_test_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:insights/v20150501:getWebTest', __args__, opts=opts, typ=GetWebTestResult).value

    return AwaitableGetWebTestResult(
        configuration=__ret__.configuration,
        description=__ret__.description,
        enabled=__ret__.enabled,
        frequency=__ret__.frequency,
        id=__ret__.id,
        kind=__ret__.kind,
        location=__ret__.location,
        locations=__ret__.locations,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        retry_enabled=__ret__.retry_enabled,
        synthetic_monitor_id=__ret__.synthetic_monitor_id,
        tags=__ret__.tags,
        timeout=__ret__.timeout,
        type=__ret__.type,
        web_test_kind=__ret__.web_test_kind,
        web_test_name=__ret__.web_test_name)


@_utilities.lift_output_func(get_web_test)
def get_web_test_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                        web_test_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebTestResult]:
    """
    Get a specific Application Insights web test definition.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str web_test_name: The name of the Application Insights webtest resource.
    """
    ...
