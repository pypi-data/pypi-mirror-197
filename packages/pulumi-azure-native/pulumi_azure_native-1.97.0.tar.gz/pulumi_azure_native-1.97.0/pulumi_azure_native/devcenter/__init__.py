# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .attached_network_by_dev_center import *
from .catalog import *
from .dev_box_definition import *
from .dev_center import *
from .environment_type import *
from .gallery import *
from .get_attached_network_by_dev_center import *
from .get_catalog import *
from .get_dev_box_definition import *
from .get_dev_center import *
from .get_environment_type import *
from .get_gallery import *
from .get_network_connection import *
from .get_pool import *
from .get_project import *
from .get_project_environment_type import *
from .get_schedule import *
from .network_connection import *
from .pool import *
from .project import *
from .project_environment_type import *
from .schedule import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.devcenter.v20220801preview as __v20220801preview
    v20220801preview = __v20220801preview
    import pulumi_azure_native.devcenter.v20220901preview as __v20220901preview
    v20220901preview = __v20220901preview
    import pulumi_azure_native.devcenter.v20221012preview as __v20221012preview
    v20221012preview = __v20221012preview
    import pulumi_azure_native.devcenter.v20221111preview as __v20221111preview
    v20221111preview = __v20221111preview
else:
    v20220801preview = _utilities.lazy_import('pulumi_azure_native.devcenter.v20220801preview')
    v20220901preview = _utilities.lazy_import('pulumi_azure_native.devcenter.v20220901preview')
    v20221012preview = _utilities.lazy_import('pulumi_azure_native.devcenter.v20221012preview')
    v20221111preview = _utilities.lazy_import('pulumi_azure_native.devcenter.v20221111preview')

