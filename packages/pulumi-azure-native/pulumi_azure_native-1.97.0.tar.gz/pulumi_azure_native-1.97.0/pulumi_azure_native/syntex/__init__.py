# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from .document_processor import *
from .get_document_processor import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.syntex.v20220915preview as __v20220915preview
    v20220915preview = __v20220915preview
else:
    v20220915preview = _utilities.lazy_import('pulumi_azure_native.syntex.v20220915preview')

