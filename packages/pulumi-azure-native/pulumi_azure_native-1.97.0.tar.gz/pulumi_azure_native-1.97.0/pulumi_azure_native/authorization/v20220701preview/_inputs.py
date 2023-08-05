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
    'ResourceSelectorArgs',
    'SelectorArgs',
]

@pulumi.input_type
class ResourceSelectorArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 selectors: Optional[pulumi.Input[Sequence[pulumi.Input['SelectorArgs']]]] = None):
        """
        The resource selector to filter policies by resource properties.
        :param pulumi.Input[str] name: The name of the resource selector.
        :param pulumi.Input[Sequence[pulumi.Input['SelectorArgs']]] selectors: The list of the selector expressions.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if selectors is not None:
            pulumi.set(__self__, "selectors", selectors)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource selector.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def selectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['SelectorArgs']]]]:
        """
        The list of the selector expressions.
        """
        return pulumi.get(self, "selectors")

    @selectors.setter
    def selectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['SelectorArgs']]]]):
        pulumi.set(self, "selectors", value)


@pulumi.input_type
class SelectorArgs:
    def __init__(__self__, *,
                 in_: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 kind: Optional[pulumi.Input[Union[str, 'SelectorKind']]] = None,
                 not_in: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The selector expression.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] in_: The list of values to filter in.
        :param pulumi.Input[Union[str, 'SelectorKind']] kind: The selector kind.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] not_in: The list of values to filter out.
        """
        if in_ is not None:
            pulumi.set(__self__, "in_", in_)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if not_in is not None:
            pulumi.set(__self__, "not_in", not_in)

    @property
    @pulumi.getter(name="in")
    def in_(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of values to filter in.
        """
        return pulumi.get(self, "in_")

    @in_.setter
    def in_(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "in_", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[Union[str, 'SelectorKind']]]:
        """
        The selector kind.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[Union[str, 'SelectorKind']]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter(name="notIn")
    def not_in(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of values to filter out.
        """
        return pulumi.get(self, "not_in")

    @not_in.setter
    def not_in(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "not_in", value)


