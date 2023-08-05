# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetPipelineTopologyResult',
    'AwaitableGetPipelineTopologyResult',
    'get_pipeline_topology',
    'get_pipeline_topology_output',
]

@pulumi.output_type
class GetPipelineTopologyResult:
    """
    Pipeline topology describes the processing steps to be applied when processing content for a particular outcome. The topology should be defined according to the scenario to be achieved and can be reused across many pipeline instances which share the same processing characteristics. For instance, a pipeline topology which captures content from a RTSP camera and archives the content can be reused across many different cameras, as long as the same processing is to be applied across all the cameras. Individual instance properties can be defined through the use of user-defined parameters, which allow for a topology to be parameterized. This allows  individual pipelines refer to different values, such as individual cameras' RTSP endpoints and credentials. Overall a topology is composed of the following:
    
      - Parameters: list of user defined parameters that can be references across the topology nodes.
      - Sources: list of one or more data sources nodes such as an RTSP source which allows for content to be ingested from cameras.
      - Processors: list of nodes which perform data analysis or transformations.
      - Sinks: list of one or more data sinks which allow for data to be stored or exported to other destinations.
    """
    def __init__(__self__, description=None, id=None, kind=None, name=None, parameters=None, processors=None, sinks=None, sku=None, sources=None, system_data=None, type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters and not isinstance(parameters, list):
            raise TypeError("Expected argument 'parameters' to be a list")
        pulumi.set(__self__, "parameters", parameters)
        if processors and not isinstance(processors, list):
            raise TypeError("Expected argument 'processors' to be a list")
        pulumi.set(__self__, "processors", processors)
        if sinks and not isinstance(sinks, list):
            raise TypeError("Expected argument 'sinks' to be a list")
        pulumi.set(__self__, "sinks", sinks)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if sources and not isinstance(sources, list):
            raise TypeError("Expected argument 'sources' to be a list")
        pulumi.set(__self__, "sources", sources)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        An optional description of the pipeline topology. It is recommended that the expected use of the topology to be described here.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Topology kind.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Sequence['outputs.ParameterDeclarationResponse']]:
        """
        List of the topology parameter declarations. Parameters declared here can be referenced throughout the topology nodes through the use of "${PARAMETER_NAME}" string pattern. Parameters can have optional default values and can later be defined in individual instances of the pipeline.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def processors(self) -> Optional[Sequence['outputs.EncoderProcessorResponse']]:
        """
        List of the topology processor nodes. Processor nodes enable pipeline data to be analyzed, processed or transformed.
        """
        return pulumi.get(self, "processors")

    @property
    @pulumi.getter
    def sinks(self) -> Sequence['outputs.VideoSinkResponse']:
        """
        List of the topology sink nodes. Sink nodes allow pipeline data to be stored or exported.
        """
        return pulumi.get(self, "sinks")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        Describes the properties of a SKU.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def sources(self) -> Sequence[Any]:
        """
        List of the topology source nodes. Source nodes enable external data to be ingested by the pipeline.
        """
        return pulumi.get(self, "sources")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetPipelineTopologyResult(GetPipelineTopologyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPipelineTopologyResult(
            description=self.description,
            id=self.id,
            kind=self.kind,
            name=self.name,
            parameters=self.parameters,
            processors=self.processors,
            sinks=self.sinks,
            sku=self.sku,
            sources=self.sources,
            system_data=self.system_data,
            type=self.type)


def get_pipeline_topology(account_name: Optional[str] = None,
                          pipeline_topology_name: Optional[str] = None,
                          resource_group_name: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPipelineTopologyResult:
    """
    Retrieves a specific pipeline topology by name. If a topology with that name has been previously created, the call will return the JSON representation of that topology.
    API Version: 2021-11-01-preview.


    :param str account_name: The Azure Video Analyzer account name.
    :param str pipeline_topology_name: Pipeline topology unique identifier.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['pipelineTopologyName'] = pipeline_topology_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:videoanalyzer:getPipelineTopology', __args__, opts=opts, typ=GetPipelineTopologyResult).value

    return AwaitableGetPipelineTopologyResult(
        description=__ret__.description,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        parameters=__ret__.parameters,
        processors=__ret__.processors,
        sinks=__ret__.sinks,
        sku=__ret__.sku,
        sources=__ret__.sources,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_pipeline_topology)
def get_pipeline_topology_output(account_name: Optional[pulumi.Input[str]] = None,
                                 pipeline_topology_name: Optional[pulumi.Input[str]] = None,
                                 resource_group_name: Optional[pulumi.Input[str]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPipelineTopologyResult]:
    """
    Retrieves a specific pipeline topology by name. If a topology with that name has been previously created, the call will return the JSON representation of that topology.
    API Version: 2021-11-01-preview.


    :param str account_name: The Azure Video Analyzer account name.
    :param str pipeline_topology_name: Pipeline topology unique identifier.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
