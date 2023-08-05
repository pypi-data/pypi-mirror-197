# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .get_guest_configuration_assignment import *
from .get_guest_configuration_connected_v_mwarev_sphere_assignment import *
from .get_guest_configuration_hcrpassignment import *
from .guest_configuration_assignment import *
from .guest_configuration_connected_v_mwarev_sphere_assignment import *
from .guest_configuration_hcrpassignment import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.guestconfiguration.v20180630preview as __v20180630preview
    v20180630preview = __v20180630preview
    import pulumi_azure_native.guestconfiguration.v20181120 as __v20181120
    v20181120 = __v20181120
    import pulumi_azure_native.guestconfiguration.v20200625 as __v20200625
    v20200625 = __v20200625
    import pulumi_azure_native.guestconfiguration.v20210125 as __v20210125
    v20210125 = __v20210125
    import pulumi_azure_native.guestconfiguration.v20220125 as __v20220125
    v20220125 = __v20220125
else:
    v20180630preview = _utilities.lazy_import('pulumi_azure_native.guestconfiguration.v20180630preview')
    v20181120 = _utilities.lazy_import('pulumi_azure_native.guestconfiguration.v20181120')
    v20200625 = _utilities.lazy_import('pulumi_azure_native.guestconfiguration.v20200625')
    v20210125 = _utilities.lazy_import('pulumi_azure_native.guestconfiguration.v20210125')
    v20220125 = _utilities.lazy_import('pulumi_azure_native.guestconfiguration.v20220125')

