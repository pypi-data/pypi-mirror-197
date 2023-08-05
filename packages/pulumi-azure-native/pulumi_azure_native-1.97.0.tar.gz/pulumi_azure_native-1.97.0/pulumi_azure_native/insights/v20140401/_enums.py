# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ComparisonOperationType',
    'ConditionOperator',
    'MetricStatisticType',
    'OperationType',
    'RecurrenceFrequency',
    'ScaleDirection',
    'ScaleRuleMetricDimensionOperationType',
    'ScaleType',
    'TimeAggregationOperator',
    'TimeAggregationType',
]


class ComparisonOperationType(str, Enum):
    """
    the operator that is used to compare the metric data and the threshold.
    """
    EQUALS = "Equals"
    NOT_EQUALS = "NotEquals"
    GREATER_THAN = "GreaterThan"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    LESS_THAN = "LessThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"


class ConditionOperator(str, Enum):
    """
    the operator used to compare the data and the threshold.
    """
    GREATER_THAN = "GreaterThan"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    LESS_THAN = "LessThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"


class MetricStatisticType(str, Enum):
    """
    the metric statistic type. How the metrics from multiple instances are combined.
    """
    AVERAGE = "Average"
    MIN = "Min"
    MAX = "Max"
    SUM = "Sum"
    COUNT = "Count"


class OperationType(str, Enum):
    """
    the operation associated with the notification and its value must be "scale"
    """
    SCALE = "Scale"


class RecurrenceFrequency(str, Enum):
    """
    the recurrence frequency. How often the schedule profile should take effect. This value must be Week, meaning each week will have the same set of profiles. For example, to set a daily schedule, set **schedule** to every day of the week. The frequency property specifies that the schedule is repeated weekly.
    """
    NONE = "None"
    SECOND = "Second"
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"


class ScaleDirection(str, Enum):
    """
    the scale direction. Whether the scaling action increases or decreases the number of instances.
    """
    NONE = "None"
    INCREASE = "Increase"
    DECREASE = "Decrease"


class ScaleRuleMetricDimensionOperationType(str, Enum):
    """
    the dimension operator. Only 'Equals' and 'NotEquals' are supported. 'Equals' being equal to any of the values. 'NotEquals' being not equal to all of the values
    """
    EQUALS = "Equals"
    NOT_EQUALS = "NotEquals"


class ScaleType(str, Enum):
    """
    the type of action that should occur when the scale rule fires.
    """
    CHANGE_COUNT = "ChangeCount"
    PERCENT_CHANGE_COUNT = "PercentChangeCount"
    EXACT_COUNT = "ExactCount"
    SERVICE_ALLOWED_NEXT_VALUE = "ServiceAllowedNextValue"


class TimeAggregationOperator(str, Enum):
    """
    the time aggregation operator. How the data that are collected should be combined over time. The default value is the PrimaryAggregationType of the Metric.
    """
    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    LAST = "Last"


class TimeAggregationType(str, Enum):
    """
    time aggregation type. How the data that is collected should be combined over time. The default value is Average.
    """
    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    COUNT = "Count"
    LAST = "Last"
