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

__all__ = [
    'ActionsArgs',
    'ConditionFailingPeriodsArgs',
    'ConditionArgs',
    'DimensionArgs',
    'HeaderFieldArgs',
    'ScheduledQueryRuleCriteriaArgs',
    'WebTestGeolocationArgs',
    'WebTestPropertiesConfigurationArgs',
    'WebTestPropertiesContentValidationArgs',
    'WebTestPropertiesRequestArgs',
    'WebTestPropertiesValidationRulesArgs',
]

@pulumi.input_type
class ActionsArgs:
    def __init__(__self__, *,
                 action_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 custom_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Actions to invoke when the alert fires.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] action_groups: Action Group resource Ids to invoke when the alert fires.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] custom_properties: The properties of an alert payload.
        """
        if action_groups is not None:
            pulumi.set(__self__, "action_groups", action_groups)
        if custom_properties is not None:
            pulumi.set(__self__, "custom_properties", custom_properties)

    @property
    @pulumi.getter(name="actionGroups")
    def action_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Action Group resource Ids to invoke when the alert fires.
        """
        return pulumi.get(self, "action_groups")

    @action_groups.setter
    def action_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "action_groups", value)

    @property
    @pulumi.getter(name="customProperties")
    def custom_properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The properties of an alert payload.
        """
        return pulumi.get(self, "custom_properties")

    @custom_properties.setter
    def custom_properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "custom_properties", value)


@pulumi.input_type
class ConditionFailingPeriodsArgs:
    def __init__(__self__, *,
                 min_failing_periods_to_alert: Optional[pulumi.Input[float]] = None,
                 number_of_evaluation_periods: Optional[pulumi.Input[float]] = None):
        """
        The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
        :param pulumi.Input[float] min_failing_periods_to_alert: The number of violations to trigger an alert. Should be smaller or equal to numberOfEvaluationPeriods. Default value is 1
        :param pulumi.Input[float] number_of_evaluation_periods: The number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (windowSize) and the selected number of aggregated points. Default value is 1
        """
        if min_failing_periods_to_alert is None:
            min_failing_periods_to_alert = 1
        if min_failing_periods_to_alert is not None:
            pulumi.set(__self__, "min_failing_periods_to_alert", min_failing_periods_to_alert)
        if number_of_evaluation_periods is None:
            number_of_evaluation_periods = 1
        if number_of_evaluation_periods is not None:
            pulumi.set(__self__, "number_of_evaluation_periods", number_of_evaluation_periods)

    @property
    @pulumi.getter(name="minFailingPeriodsToAlert")
    def min_failing_periods_to_alert(self) -> Optional[pulumi.Input[float]]:
        """
        The number of violations to trigger an alert. Should be smaller or equal to numberOfEvaluationPeriods. Default value is 1
        """
        return pulumi.get(self, "min_failing_periods_to_alert")

    @min_failing_periods_to_alert.setter
    def min_failing_periods_to_alert(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "min_failing_periods_to_alert", value)

    @property
    @pulumi.getter(name="numberOfEvaluationPeriods")
    def number_of_evaluation_periods(self) -> Optional[pulumi.Input[float]]:
        """
        The number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (windowSize) and the selected number of aggregated points. Default value is 1
        """
        return pulumi.get(self, "number_of_evaluation_periods")

    @number_of_evaluation_periods.setter
    def number_of_evaluation_periods(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "number_of_evaluation_periods", value)


@pulumi.input_type
class ConditionArgs:
    def __init__(__self__, *,
                 dimensions: Optional[pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]]] = None,
                 failing_periods: Optional[pulumi.Input['ConditionFailingPeriodsArgs']] = None,
                 metric_measure_column: Optional[pulumi.Input[str]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 operator: Optional[pulumi.Input[Union[str, 'ConditionOperator']]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_id_column: Optional[pulumi.Input[str]] = None,
                 threshold: Optional[pulumi.Input[float]] = None,
                 time_aggregation: Optional[pulumi.Input[Union[str, 'TimeAggregation']]] = None):
        """
        A condition of the scheduled query rule.
        :param pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]] dimensions: List of Dimensions conditions
        :param pulumi.Input['ConditionFailingPeriodsArgs'] failing_periods: The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
        :param pulumi.Input[str] metric_measure_column: The column containing the metric measure number. Relevant only for rules of the kind LogAlert.
        :param pulumi.Input[str] metric_name: The name of the metric to be sent. Relevant and required only for rules of the kind LogToMetric.
        :param pulumi.Input[Union[str, 'ConditionOperator']] operator: The criteria operator. Relevant and required only for rules of the kind LogAlert.
        :param pulumi.Input[str] query: Log query alert
        :param pulumi.Input[str] resource_id_column: The column containing the resource id. The content of the column must be a uri formatted as resource id. Relevant only for rules of the kind LogAlert.
        :param pulumi.Input[float] threshold: the criteria threshold value that activates the alert. Relevant and required only for rules of the kind LogAlert.
        :param pulumi.Input[Union[str, 'TimeAggregation']] time_aggregation: Aggregation type. Relevant and required only for rules of the kind LogAlert.
        """
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if failing_periods is not None:
            pulumi.set(__self__, "failing_periods", failing_periods)
        if metric_measure_column is not None:
            pulumi.set(__self__, "metric_measure_column", metric_measure_column)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if operator is not None:
            pulumi.set(__self__, "operator", operator)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if resource_id_column is not None:
            pulumi.set(__self__, "resource_id_column", resource_id_column)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)
        if time_aggregation is not None:
            pulumi.set(__self__, "time_aggregation", time_aggregation)

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]]]:
        """
        List of Dimensions conditions
        """
        return pulumi.get(self, "dimensions")

    @dimensions.setter
    def dimensions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DimensionArgs']]]]):
        pulumi.set(self, "dimensions", value)

    @property
    @pulumi.getter(name="failingPeriods")
    def failing_periods(self) -> Optional[pulumi.Input['ConditionFailingPeriodsArgs']]:
        """
        The minimum number of violations required within the selected lookback time window required to raise an alert. Relevant only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "failing_periods")

    @failing_periods.setter
    def failing_periods(self, value: Optional[pulumi.Input['ConditionFailingPeriodsArgs']]):
        pulumi.set(self, "failing_periods", value)

    @property
    @pulumi.getter(name="metricMeasureColumn")
    def metric_measure_column(self) -> Optional[pulumi.Input[str]]:
        """
        The column containing the metric measure number. Relevant only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "metric_measure_column")

    @metric_measure_column.setter
    def metric_measure_column(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_measure_column", value)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the metric to be sent. Relevant and required only for rules of the kind LogToMetric.
        """
        return pulumi.get(self, "metric_name")

    @metric_name.setter
    def metric_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_name", value)

    @property
    @pulumi.getter
    def operator(self) -> Optional[pulumi.Input[Union[str, 'ConditionOperator']]]:
        """
        The criteria operator. Relevant and required only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "operator")

    @operator.setter
    def operator(self, value: Optional[pulumi.Input[Union[str, 'ConditionOperator']]]):
        pulumi.set(self, "operator", value)

    @property
    @pulumi.getter
    def query(self) -> Optional[pulumi.Input[str]]:
        """
        Log query alert
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter(name="resourceIdColumn")
    def resource_id_column(self) -> Optional[pulumi.Input[str]]:
        """
        The column containing the resource id. The content of the column must be a uri formatted as resource id. Relevant only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "resource_id_column")

    @resource_id_column.setter
    def resource_id_column(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id_column", value)

    @property
    @pulumi.getter
    def threshold(self) -> Optional[pulumi.Input[float]]:
        """
        the criteria threshold value that activates the alert. Relevant and required only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "threshold")

    @threshold.setter
    def threshold(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "threshold", value)

    @property
    @pulumi.getter(name="timeAggregation")
    def time_aggregation(self) -> Optional[pulumi.Input[Union[str, 'TimeAggregation']]]:
        """
        Aggregation type. Relevant and required only for rules of the kind LogAlert.
        """
        return pulumi.get(self, "time_aggregation")

    @time_aggregation.setter
    def time_aggregation(self, value: Optional[pulumi.Input[Union[str, 'TimeAggregation']]]):
        pulumi.set(self, "time_aggregation", value)


@pulumi.input_type
class DimensionArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 operator: pulumi.Input[Union[str, 'DimensionOperator']],
                 values: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        Dimension splitting and filtering definition
        :param pulumi.Input[str] name: Name of the dimension
        :param pulumi.Input[Union[str, 'DimensionOperator']] operator: Operator for dimension values
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: List of dimension values
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the dimension
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def operator(self) -> pulumi.Input[Union[str, 'DimensionOperator']]:
        """
        Operator for dimension values
        """
        return pulumi.get(self, "operator")

    @operator.setter
    def operator(self, value: pulumi.Input[Union[str, 'DimensionOperator']]):
        pulumi.set(self, "operator", value)

    @property
    @pulumi.getter
    def values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of dimension values
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class HeaderFieldArgs:
    def __init__(__self__, *,
                 header_field_name: Optional[pulumi.Input[str]] = None,
                 header_field_value: Optional[pulumi.Input[str]] = None):
        """
        A header to add to the WebTest.
        :param pulumi.Input[str] header_field_name: The name of the header.
        :param pulumi.Input[str] header_field_value: The value of the header.
        """
        if header_field_name is not None:
            pulumi.set(__self__, "header_field_name", header_field_name)
        if header_field_value is not None:
            pulumi.set(__self__, "header_field_value", header_field_value)

    @property
    @pulumi.getter(name="headerFieldName")
    def header_field_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the header.
        """
        return pulumi.get(self, "header_field_name")

    @header_field_name.setter
    def header_field_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "header_field_name", value)

    @property
    @pulumi.getter(name="headerFieldValue")
    def header_field_value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the header.
        """
        return pulumi.get(self, "header_field_value")

    @header_field_value.setter
    def header_field_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "header_field_value", value)


@pulumi.input_type
class ScheduledQueryRuleCriteriaArgs:
    def __init__(__self__, *,
                 all_of: Optional[pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]]] = None):
        """
        The rule criteria that defines the conditions of the scheduled query rule.
        :param pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]] all_of: A list of conditions to evaluate against the specified scopes
        """
        if all_of is not None:
            pulumi.set(__self__, "all_of", all_of)

    @property
    @pulumi.getter(name="allOf")
    def all_of(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]]]:
        """
        A list of conditions to evaluate against the specified scopes
        """
        return pulumi.get(self, "all_of")

    @all_of.setter
    def all_of(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConditionArgs']]]]):
        pulumi.set(self, "all_of", value)


@pulumi.input_type
class WebTestGeolocationArgs:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None):
        """
        Geo-physical location to run a WebTest from. You must specify one or more locations for the test to run from.
        :param pulumi.Input[str] location: Location ID for the WebTest to run from.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Location ID for the WebTest to run from.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)


@pulumi.input_type
class WebTestPropertiesConfigurationArgs:
    def __init__(__self__, *,
                 web_test: Optional[pulumi.Input[str]] = None):
        """
        An XML configuration specification for a WebTest.
        :param pulumi.Input[str] web_test: The XML specification of a WebTest to run against an application.
        """
        if web_test is not None:
            pulumi.set(__self__, "web_test", web_test)

    @property
    @pulumi.getter(name="webTest")
    def web_test(self) -> Optional[pulumi.Input[str]]:
        """
        The XML specification of a WebTest to run against an application.
        """
        return pulumi.get(self, "web_test")

    @web_test.setter
    def web_test(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "web_test", value)


@pulumi.input_type
class WebTestPropertiesContentValidationArgs:
    def __init__(__self__, *,
                 content_match: Optional[pulumi.Input[str]] = None,
                 ignore_case: Optional[pulumi.Input[bool]] = None,
                 pass_if_text_found: Optional[pulumi.Input[bool]] = None):
        """
        The collection of content validation properties
        :param pulumi.Input[str] content_match: Content to look for in the return of the WebTest.  Must not be null or empty.
        :param pulumi.Input[bool] ignore_case: When set, this value makes the ContentMatch validation case insensitive.
        :param pulumi.Input[bool] pass_if_text_found: When true, validation will pass if there is a match for the ContentMatch string.  If false, validation will fail if there is a match
        """
        if content_match is not None:
            pulumi.set(__self__, "content_match", content_match)
        if ignore_case is not None:
            pulumi.set(__self__, "ignore_case", ignore_case)
        if pass_if_text_found is not None:
            pulumi.set(__self__, "pass_if_text_found", pass_if_text_found)

    @property
    @pulumi.getter(name="contentMatch")
    def content_match(self) -> Optional[pulumi.Input[str]]:
        """
        Content to look for in the return of the WebTest.  Must not be null or empty.
        """
        return pulumi.get(self, "content_match")

    @content_match.setter
    def content_match(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_match", value)

    @property
    @pulumi.getter(name="ignoreCase")
    def ignore_case(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, this value makes the ContentMatch validation case insensitive.
        """
        return pulumi.get(self, "ignore_case")

    @ignore_case.setter
    def ignore_case(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ignore_case", value)

    @property
    @pulumi.getter(name="passIfTextFound")
    def pass_if_text_found(self) -> Optional[pulumi.Input[bool]]:
        """
        When true, validation will pass if there is a match for the ContentMatch string.  If false, validation will fail if there is a match
        """
        return pulumi.get(self, "pass_if_text_found")

    @pass_if_text_found.setter
    def pass_if_text_found(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "pass_if_text_found", value)


@pulumi.input_type
class WebTestPropertiesRequestArgs:
    def __init__(__self__, *,
                 follow_redirects: Optional[pulumi.Input[bool]] = None,
                 headers: Optional[pulumi.Input[Sequence[pulumi.Input['HeaderFieldArgs']]]] = None,
                 http_verb: Optional[pulumi.Input[str]] = None,
                 parse_dependent_requests: Optional[pulumi.Input[bool]] = None,
                 request_body: Optional[pulumi.Input[str]] = None,
                 request_url: Optional[pulumi.Input[str]] = None):
        """
        The collection of request properties
        :param pulumi.Input[bool] follow_redirects: Follow redirects for this web test.
        :param pulumi.Input[Sequence[pulumi.Input['HeaderFieldArgs']]] headers: List of headers and their values to add to the WebTest call.
        :param pulumi.Input[str] http_verb: Http verb to use for this web test.
        :param pulumi.Input[bool] parse_dependent_requests: Parse Dependent request for this WebTest.
        :param pulumi.Input[str] request_body: Base64 encoded string body to send with this web test.
        :param pulumi.Input[str] request_url: Url location to test.
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
    def follow_redirects(self) -> Optional[pulumi.Input[bool]]:
        """
        Follow redirects for this web test.
        """
        return pulumi.get(self, "follow_redirects")

    @follow_redirects.setter
    def follow_redirects(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "follow_redirects", value)

    @property
    @pulumi.getter
    def headers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HeaderFieldArgs']]]]:
        """
        List of headers and their values to add to the WebTest call.
        """
        return pulumi.get(self, "headers")

    @headers.setter
    def headers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HeaderFieldArgs']]]]):
        pulumi.set(self, "headers", value)

    @property
    @pulumi.getter(name="httpVerb")
    def http_verb(self) -> Optional[pulumi.Input[str]]:
        """
        Http verb to use for this web test.
        """
        return pulumi.get(self, "http_verb")

    @http_verb.setter
    def http_verb(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "http_verb", value)

    @property
    @pulumi.getter(name="parseDependentRequests")
    def parse_dependent_requests(self) -> Optional[pulumi.Input[bool]]:
        """
        Parse Dependent request for this WebTest.
        """
        return pulumi.get(self, "parse_dependent_requests")

    @parse_dependent_requests.setter
    def parse_dependent_requests(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "parse_dependent_requests", value)

    @property
    @pulumi.getter(name="requestBody")
    def request_body(self) -> Optional[pulumi.Input[str]]:
        """
        Base64 encoded string body to send with this web test.
        """
        return pulumi.get(self, "request_body")

    @request_body.setter
    def request_body(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_body", value)

    @property
    @pulumi.getter(name="requestUrl")
    def request_url(self) -> Optional[pulumi.Input[str]]:
        """
        Url location to test.
        """
        return pulumi.get(self, "request_url")

    @request_url.setter
    def request_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_url", value)


@pulumi.input_type
class WebTestPropertiesValidationRulesArgs:
    def __init__(__self__, *,
                 content_validation: Optional[pulumi.Input['WebTestPropertiesContentValidationArgs']] = None,
                 expected_http_status_code: Optional[pulumi.Input[int]] = None,
                 ignore_http_status_code: Optional[pulumi.Input[bool]] = None,
                 s_sl_cert_remaining_lifetime_check: Optional[pulumi.Input[int]] = None,
                 s_sl_check: Optional[pulumi.Input[bool]] = None):
        """
        The collection of validation rule properties
        :param pulumi.Input['WebTestPropertiesContentValidationArgs'] content_validation: The collection of content validation properties
        :param pulumi.Input[int] expected_http_status_code: Validate that the WebTest returns the http status code provided.
        :param pulumi.Input[bool] ignore_http_status_code: When set, validation will ignore the status code.
        :param pulumi.Input[int] s_sl_cert_remaining_lifetime_check: A number of days to check still remain before the the existing SSL cert expires.  Value must be positive and the SSLCheck must be set to true.
        :param pulumi.Input[bool] s_sl_check: Checks to see if the SSL cert is still valid.
        """
        if content_validation is not None:
            pulumi.set(__self__, "content_validation", content_validation)
        if expected_http_status_code is not None:
            pulumi.set(__self__, "expected_http_status_code", expected_http_status_code)
        if ignore_http_status_code is not None:
            pulumi.set(__self__, "ignore_http_status_code", ignore_http_status_code)
        if s_sl_cert_remaining_lifetime_check is not None:
            pulumi.set(__self__, "s_sl_cert_remaining_lifetime_check", s_sl_cert_remaining_lifetime_check)
        if s_sl_check is not None:
            pulumi.set(__self__, "s_sl_check", s_sl_check)

    @property
    @pulumi.getter(name="contentValidation")
    def content_validation(self) -> Optional[pulumi.Input['WebTestPropertiesContentValidationArgs']]:
        """
        The collection of content validation properties
        """
        return pulumi.get(self, "content_validation")

    @content_validation.setter
    def content_validation(self, value: Optional[pulumi.Input['WebTestPropertiesContentValidationArgs']]):
        pulumi.set(self, "content_validation", value)

    @property
    @pulumi.getter(name="expectedHttpStatusCode")
    def expected_http_status_code(self) -> Optional[pulumi.Input[int]]:
        """
        Validate that the WebTest returns the http status code provided.
        """
        return pulumi.get(self, "expected_http_status_code")

    @expected_http_status_code.setter
    def expected_http_status_code(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "expected_http_status_code", value)

    @property
    @pulumi.getter(name="ignoreHttpStatusCode")
    def ignore_http_status_code(self) -> Optional[pulumi.Input[bool]]:
        """
        When set, validation will ignore the status code.
        """
        return pulumi.get(self, "ignore_http_status_code")

    @ignore_http_status_code.setter
    def ignore_http_status_code(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ignore_http_status_code", value)

    @property
    @pulumi.getter(name="sSLCertRemainingLifetimeCheck")
    def s_sl_cert_remaining_lifetime_check(self) -> Optional[pulumi.Input[int]]:
        """
        A number of days to check still remain before the the existing SSL cert expires.  Value must be positive and the SSLCheck must be set to true.
        """
        return pulumi.get(self, "s_sl_cert_remaining_lifetime_check")

    @s_sl_cert_remaining_lifetime_check.setter
    def s_sl_cert_remaining_lifetime_check(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "s_sl_cert_remaining_lifetime_check", value)

    @property
    @pulumi.getter(name="sSLCheck")
    def s_sl_check(self) -> Optional[pulumi.Input[bool]]:
        """
        Checks to see if the SSL cert is still valid.
        """
        return pulumi.get(self, "s_sl_check")

    @s_sl_check.setter
    def s_sl_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "s_sl_check", value)


