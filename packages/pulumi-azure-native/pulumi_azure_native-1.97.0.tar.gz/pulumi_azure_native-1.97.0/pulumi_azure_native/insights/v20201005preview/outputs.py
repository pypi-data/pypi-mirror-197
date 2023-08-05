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
    'HeaderFieldResponse',
    'WebTestGeolocationResponse',
    'WebTestPropertiesResponseConfiguration',
    'WebTestPropertiesResponseContentValidation',
    'WebTestPropertiesResponseRequest',
    'WebTestPropertiesResponseValidationRules',
]

@pulumi.output_type
class HeaderFieldResponse(dict):
    """
    A header to add to the WebTest.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "headerFieldName":
            suggest = "header_field_name"
        elif key == "headerFieldValue":
            suggest = "header_field_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in HeaderFieldResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        HeaderFieldResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        HeaderFieldResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 header_field_name: Optional[str] = None,
                 header_field_value: Optional[str] = None):
        """
        A header to add to the WebTest.
        :param str header_field_name: The name of the header.
        :param str header_field_value: The value of the header.
        """
        if header_field_name is not None:
            pulumi.set(__self__, "header_field_name", header_field_name)
        if header_field_value is not None:
            pulumi.set(__self__, "header_field_value", header_field_value)

    @property
    @pulumi.getter(name="headerFieldName")
    def header_field_name(self) -> Optional[str]:
        """
        The name of the header.
        """
        return pulumi.get(self, "header_field_name")

    @property
    @pulumi.getter(name="headerFieldValue")
    def header_field_value(self) -> Optional[str]:
        """
        The value of the header.
        """
        return pulumi.get(self, "header_field_value")


@pulumi.output_type
class WebTestGeolocationResponse(dict):
    """
    Geo-physical location to run a WebTest from. You must specify one or more locations for the test to run from.
    """
    def __init__(__self__, *,
                 location: Optional[str] = None):
        """
        Geo-physical location to run a WebTest from. You must specify one or more locations for the test to run from.
        :param str location: Location ID for the WebTest to run from.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Location ID for the WebTest to run from.
        """
        return pulumi.get(self, "location")


@pulumi.output_type
class WebTestPropertiesResponseConfiguration(dict):
    """
    An XML configuration specification for a WebTest.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "webTest":
            suggest = "web_test"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebTestPropertiesResponseConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebTestPropertiesResponseConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WebTestPropertiesResponseConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 web_test: Optional[str] = None):
        """
        An XML configuration specification for a WebTest.
        :param str web_test: The XML specification of a WebTest to run against an application.
        """
        if web_test is not None:
            pulumi.set(__self__, "web_test", web_test)

    @property
    @pulumi.getter(name="webTest")
    def web_test(self) -> Optional[str]:
        """
        The XML specification of a WebTest to run against an application.
        """
        return pulumi.get(self, "web_test")


@pulumi.output_type
class WebTestPropertiesResponseContentValidation(dict):
    """
    The collection of content validation properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "contentMatch":
            suggest = "content_match"
        elif key == "ignoreCase":
            suggest = "ignore_case"
        elif key == "passIfTextFound":
            suggest = "pass_if_text_found"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebTestPropertiesResponseContentValidation. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebTestPropertiesResponseContentValidation.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WebTestPropertiesResponseContentValidation.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 content_match: Optional[str] = None,
                 ignore_case: Optional[bool] = None,
                 pass_if_text_found: Optional[bool] = None):
        """
        The collection of content validation properties
        :param str content_match: Content to look for in the return of the WebTest.  Must not be null or empty.
        :param bool ignore_case: When set, this value makes the ContentMatch validation case insensitive.
        :param bool pass_if_text_found: When true, validation will pass if there is a match for the ContentMatch string.  If false, validation will fail if there is a match
        """
        if content_match is not None:
            pulumi.set(__self__, "content_match", content_match)
        if ignore_case is not None:
            pulumi.set(__self__, "ignore_case", ignore_case)
        if pass_if_text_found is not None:
            pulumi.set(__self__, "pass_if_text_found", pass_if_text_found)

    @property
    @pulumi.getter(name="contentMatch")
    def content_match(self) -> Optional[str]:
        """
        Content to look for in the return of the WebTest.  Must not be null or empty.
        """
        return pulumi.get(self, "content_match")

    @property
    @pulumi.getter(name="ignoreCase")
    def ignore_case(self) -> Optional[bool]:
        """
        When set, this value makes the ContentMatch validation case insensitive.
        """
        return pulumi.get(self, "ignore_case")

    @property
    @pulumi.getter(name="passIfTextFound")
    def pass_if_text_found(self) -> Optional[bool]:
        """
        When true, validation will pass if there is a match for the ContentMatch string.  If false, validation will fail if there is a match
        """
        return pulumi.get(self, "pass_if_text_found")


@pulumi.output_type
class WebTestPropertiesResponseRequest(dict):
    """
    The collection of request properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "followRedirects":
            suggest = "follow_redirects"
        elif key == "httpVerb":
            suggest = "http_verb"
        elif key == "parseDependentRequests":
            suggest = "parse_dependent_requests"
        elif key == "requestBody":
            suggest = "request_body"
        elif key == "requestUrl":
            suggest = "request_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebTestPropertiesResponseRequest. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebTestPropertiesResponseRequest.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WebTestPropertiesResponseRequest.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 follow_redirects: Optional[bool] = None,
                 headers: Optional[Sequence['outputs.HeaderFieldResponse']] = None,
                 http_verb: Optional[str] = None,
                 parse_dependent_requests: Optional[bool] = None,
                 request_body: Optional[str] = None,
                 request_url: Optional[str] = None):
        """
        The collection of request properties
        :param bool follow_redirects: Follow redirects for this web test.
        :param Sequence['HeaderFieldResponse'] headers: List of headers and their values to add to the WebTest call.
        :param str http_verb: Http verb to use for this web test.
        :param bool parse_dependent_requests: Parse Dependent request for this WebTest.
        :param str request_body: Base64 encoded string body to send with this web test.
        :param str request_url: Url location to test.
        """
        if follow_redirects is not None:
            pulumi.set(__self__, "follow_redirects", follow_redirects)
        if headers is not None:
            pulumi.set(__self__, "headers", headers)
        if http_verb is not None:
            pulumi.set(__self__, "http_verb", http_verb)
        if parse_dependent_requests is not None:
            pulumi.set(__self__, "parse_dependent_requests", parse_dependent_requests)
        if request_body is not None:
            pulumi.set(__self__, "request_body", request_body)
        if request_url is not None:
            pulumi.set(__self__, "request_url", request_url)

    @property
    @pulumi.getter(name="followRedirects")
    def follow_redirects(self) -> Optional[bool]:
        """
        Follow redirects for this web test.
        """
        return pulumi.get(self, "follow_redirects")

    @property
    @pulumi.getter
    def headers(self) -> Optional[Sequence['outputs.HeaderFieldResponse']]:
        """
        List of headers and their values to add to the WebTest call.
        """
        return pulumi.get(self, "headers")

    @property
    @pulumi.getter(name="httpVerb")
    def http_verb(self) -> Optional[str]:
        """
        Http verb to use for this web test.
        """
        return pulumi.get(self, "http_verb")

    @property
    @pulumi.getter(name="parseDependentRequests")
    def parse_dependent_requests(self) -> Optional[bool]:
        """
        Parse Dependent request for this WebTest.
        """
        return pulumi.get(self, "parse_dependent_requests")

    @property
    @pulumi.getter(name="requestBody")
    def request_body(self) -> Optional[str]:
        """
        Base64 encoded string body to send with this web test.
        """
        return pulumi.get(self, "request_body")

    @property
    @pulumi.getter(name="requestUrl")
    def request_url(self) -> Optional[str]:
        """
        Url location to test.
        """
        return pulumi.get(self, "request_url")


@pulumi.output_type
class WebTestPropertiesResponseValidationRules(dict):
    """
    The collection of validation rule properties
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "contentValidation":
            suggest = "content_validation"
        elif key == "expectedHttpStatusCode":
            suggest = "expected_http_status_code"
        elif key == "ignoreHttpsStatusCode":
            suggest = "ignore_https_status_code"
        elif key == "sSLCertRemainingLifetimeCheck":
            suggest = "s_sl_cert_remaining_lifetime_check"
        elif key == "sSLCheck":
            suggest = "s_sl_check"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WebTestPropertiesResponseValidationRules. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WebTestPropertiesResponseValidationRules.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WebTestPropertiesResponseValidationRules.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 content_validation: Optional['outputs.WebTestPropertiesResponseContentValidation'] = None,
                 expected_http_status_code: Optional[int] = None,
                 ignore_https_status_code: Optional[bool] = None,
                 s_sl_cert_remaining_lifetime_check: Optional[int] = None,
                 s_sl_check: Optional[bool] = None):
        """
        The collection of validation rule properties
        :param 'WebTestPropertiesResponseContentValidation' content_validation: The collection of content validation properties
        :param int expected_http_status_code: Validate that the WebTest returns the http status code provided.
        :param bool ignore_https_status_code: When set, validation will ignore the status code.
        :param int s_sl_cert_remaining_lifetime_check: A number of days to check still remain before the the existing SSL cert expires.  Value must be positive and the SSLCheck must be set to true.
        :param bool s_sl_check: Checks to see if the SSL cert is still valid.
        """
        if content_validation is not None:
            pulumi.set(__self__, "content_validation", content_validation)
        if expected_http_status_code is not None:
            pulumi.set(__self__, "expected_http_status_code", expected_http_status_code)
        if ignore_https_status_code is not None:
            pulumi.set(__self__, "ignore_https_status_code", ignore_https_status_code)
        if s_sl_cert_remaining_lifetime_check is not None:
            pulumi.set(__self__, "s_sl_cert_remaining_lifetime_check", s_sl_cert_remaining_lifetime_check)
        if s_sl_check is not None:
            pulumi.set(__self__, "s_sl_check", s_sl_check)

    @property
    @pulumi.getter(name="contentValidation")
    def content_validation(self) -> Optional['outputs.WebTestPropertiesResponseContentValidation']:
        """
        The collection of content validation properties
        """
        return pulumi.get(self, "content_validation")

    @property
    @pulumi.getter(name="expectedHttpStatusCode")
    def expected_http_status_code(self) -> Optional[int]:
        """
        Validate that the WebTest returns the http status code provided.
        """
        return pulumi.get(self, "expected_http_status_code")

    @property
    @pulumi.getter(name="ignoreHttpsStatusCode")
    def ignore_https_status_code(self) -> Optional[bool]:
        """
        When set, validation will ignore the status code.
        """
        return pulumi.get(self, "ignore_https_status_code")

    @property
    @pulumi.getter(name="sSLCertRemainingLifetimeCheck")
    def s_sl_cert_remaining_lifetime_check(self) -> Optional[int]:
        """
        A number of days to check still remain before the the existing SSL cert expires.  Value must be positive and the SSLCheck must be set to true.
        """
        return pulumi.get(self, "s_sl_cert_remaining_lifetime_check")

    @property
    @pulumi.getter(name="sSLCheck")
    def s_sl_check(self) -> Optional[bool]:
        """
        Checks to see if the SSL cert is still valid.
        """
        return pulumi.get(self, "s_sl_check")


