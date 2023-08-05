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
from ._inputs import *

__all__ = ['ConnectedClusterArgs', 'ConnectedCluster']

@pulumi.input_type
class ConnectedClusterArgs:
    def __init__(__self__, *,
                 agent_public_key_certificate: pulumi.Input[str],
                 identity: pulumi.Input['ConnectedClusterIdentityArgs'],
                 resource_group_name: pulumi.Input[str],
                 azure_hybrid_benefit: Optional[pulumi.Input[Union[str, 'AzureHybridBenefit']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 distribution: Optional[pulumi.Input[str]] = None,
                 distribution_version: Optional[pulumi.Input[str]] = None,
                 infrastructure: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_link_scope_resource_id: Optional[pulumi.Input[str]] = None,
                 private_link_state: Optional[pulumi.Input[Union[str, 'PrivateLinkState']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningState']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ConnectedCluster resource.
        :param pulumi.Input[str] agent_public_key_certificate: Base64 encoded public certificate used by the agent to do the initial handshake to the backend services in Azure.
        :param pulumi.Input['ConnectedClusterIdentityArgs'] identity: The identity of the connected cluster.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Union[str, 'AzureHybridBenefit']] azure_hybrid_benefit: Indicates whether Azure Hybrid Benefit is opted in
        :param pulumi.Input[str] cluster_name: The name of the Kubernetes cluster on which get is called.
        :param pulumi.Input[str] distribution: The Kubernetes distribution running on this connected cluster.
        :param pulumi.Input[str] distribution_version: The Kubernetes distribution version on this connected cluster.
        :param pulumi.Input[str] infrastructure: The infrastructure on which the Kubernetes cluster represented by this connected cluster is running on.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] private_link_scope_resource_id: The resource id of the private link scope this connected cluster is assigned to, if any.
        :param pulumi.Input[Union[str, 'PrivateLinkState']] private_link_state: Property which describes the state of private link on a connected cluster resource.
        :param pulumi.Input[Union[str, 'ProvisioningState']] provisioning_state: Provisioning state of the connected cluster resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "agent_public_key_certificate", agent_public_key_certificate)
        pulumi.set(__self__, "identity", identity)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if azure_hybrid_benefit is None:
            azure_hybrid_benefit = 'NotApplicable'
        if azure_hybrid_benefit is not None:
            pulumi.set(__self__, "azure_hybrid_benefit", azure_hybrid_benefit)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if distribution is not None:
            pulumi.set(__self__, "distribution", distribution)
        if distribution_version is not None:
            pulumi.set(__self__, "distribution_version", distribution_version)
        if infrastructure is not None:
            pulumi.set(__self__, "infrastructure", infrastructure)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if private_link_scope_resource_id is not None:
            pulumi.set(__self__, "private_link_scope_resource_id", private_link_scope_resource_id)
        if private_link_state is None:
            private_link_state = 'Disabled'
        if private_link_state is not None:
            pulumi.set(__self__, "private_link_state", private_link_state)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="agentPublicKeyCertificate")
    def agent_public_key_certificate(self) -> pulumi.Input[str]:
        """
        Base64 encoded public certificate used by the agent to do the initial handshake to the backend services in Azure.
        """
        return pulumi.get(self, "agent_public_key_certificate")

    @agent_public_key_certificate.setter
    def agent_public_key_certificate(self, value: pulumi.Input[str]):
        pulumi.set(self, "agent_public_key_certificate", value)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Input['ConnectedClusterIdentityArgs']:
        """
        The identity of the connected cluster.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: pulumi.Input['ConnectedClusterIdentityArgs']):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="azureHybridBenefit")
    def azure_hybrid_benefit(self) -> Optional[pulumi.Input[Union[str, 'AzureHybridBenefit']]]:
        """
        Indicates whether Azure Hybrid Benefit is opted in
        """
        return pulumi.get(self, "azure_hybrid_benefit")

    @azure_hybrid_benefit.setter
    def azure_hybrid_benefit(self, value: Optional[pulumi.Input[Union[str, 'AzureHybridBenefit']]]):
        pulumi.set(self, "azure_hybrid_benefit", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Kubernetes cluster on which get is called.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter
    def distribution(self) -> Optional[pulumi.Input[str]]:
        """
        The Kubernetes distribution running on this connected cluster.
        """
        return pulumi.get(self, "distribution")

    @distribution.setter
    def distribution(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "distribution", value)

    @property
    @pulumi.getter(name="distributionVersion")
    def distribution_version(self) -> Optional[pulumi.Input[str]]:
        """
        The Kubernetes distribution version on this connected cluster.
        """
        return pulumi.get(self, "distribution_version")

    @distribution_version.setter
    def distribution_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "distribution_version", value)

    @property
    @pulumi.getter
    def infrastructure(self) -> Optional[pulumi.Input[str]]:
        """
        The infrastructure on which the Kubernetes cluster represented by this connected cluster is running on.
        """
        return pulumi.get(self, "infrastructure")

    @infrastructure.setter
    def infrastructure(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "infrastructure", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="privateLinkScopeResourceId")
    def private_link_scope_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource id of the private link scope this connected cluster is assigned to, if any.
        """
        return pulumi.get(self, "private_link_scope_resource_id")

    @private_link_scope_resource_id.setter
    def private_link_scope_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_link_scope_resource_id", value)

    @property
    @pulumi.getter(name="privateLinkState")
    def private_link_state(self) -> Optional[pulumi.Input[Union[str, 'PrivateLinkState']]]:
        """
        Property which describes the state of private link on a connected cluster resource.
        """
        return pulumi.get(self, "private_link_state")

    @private_link_state.setter
    def private_link_state(self, value: Optional[pulumi.Input[Union[str, 'PrivateLinkState']]]):
        pulumi.set(self, "private_link_state", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[Union[str, 'ProvisioningState']]]:
        """
        Provisioning state of the connected cluster resource.
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[Union[str, 'ProvisioningState']]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ConnectedCluster(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_public_key_certificate: Optional[pulumi.Input[str]] = None,
                 azure_hybrid_benefit: Optional[pulumi.Input[Union[str, 'AzureHybridBenefit']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 distribution: Optional[pulumi.Input[str]] = None,
                 distribution_version: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ConnectedClusterIdentityArgs']]] = None,
                 infrastructure: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_link_scope_resource_id: Optional[pulumi.Input[str]] = None,
                 private_link_state: Optional[pulumi.Input[Union[str, 'PrivateLinkState']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningState']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Represents a connected cluster.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_public_key_certificate: Base64 encoded public certificate used by the agent to do the initial handshake to the backend services in Azure.
        :param pulumi.Input[Union[str, 'AzureHybridBenefit']] azure_hybrid_benefit: Indicates whether Azure Hybrid Benefit is opted in
        :param pulumi.Input[str] cluster_name: The name of the Kubernetes cluster on which get is called.
        :param pulumi.Input[str] distribution: The Kubernetes distribution running on this connected cluster.
        :param pulumi.Input[str] distribution_version: The Kubernetes distribution version on this connected cluster.
        :param pulumi.Input[pulumi.InputType['ConnectedClusterIdentityArgs']] identity: The identity of the connected cluster.
        :param pulumi.Input[str] infrastructure: The infrastructure on which the Kubernetes cluster represented by this connected cluster is running on.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] private_link_scope_resource_id: The resource id of the private link scope this connected cluster is assigned to, if any.
        :param pulumi.Input[Union[str, 'PrivateLinkState']] private_link_state: Property which describes the state of private link on a connected cluster resource.
        :param pulumi.Input[Union[str, 'ProvisioningState']] provisioning_state: Provisioning state of the connected cluster resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConnectedClusterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a connected cluster.

        :param str resource_name: The name of the resource.
        :param ConnectedClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConnectedClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_public_key_certificate: Optional[pulumi.Input[str]] = None,
                 azure_hybrid_benefit: Optional[pulumi.Input[Union[str, 'AzureHybridBenefit']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 distribution: Optional[pulumi.Input[str]] = None,
                 distribution_version: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ConnectedClusterIdentityArgs']]] = None,
                 infrastructure: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 private_link_scope_resource_id: Optional[pulumi.Input[str]] = None,
                 private_link_state: Optional[pulumi.Input[Union[str, 'PrivateLinkState']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningState']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ConnectedClusterArgs.__new__(ConnectedClusterArgs)

            if agent_public_key_certificate is None and not opts.urn:
                raise TypeError("Missing required property 'agent_public_key_certificate'")
            __props__.__dict__["agent_public_key_certificate"] = agent_public_key_certificate
            if azure_hybrid_benefit is None:
                azure_hybrid_benefit = 'NotApplicable'
            __props__.__dict__["azure_hybrid_benefit"] = azure_hybrid_benefit
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["distribution"] = distribution
            __props__.__dict__["distribution_version"] = distribution_version
            if identity is None and not opts.urn:
                raise TypeError("Missing required property 'identity'")
            __props__.__dict__["identity"] = identity
            __props__.__dict__["infrastructure"] = infrastructure
            __props__.__dict__["location"] = location
            __props__.__dict__["private_link_scope_resource_id"] = private_link_scope_resource_id
            if private_link_state is None:
                private_link_state = 'Disabled'
            __props__.__dict__["private_link_state"] = private_link_state
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["agent_version"] = None
            __props__.__dict__["connectivity_status"] = None
            __props__.__dict__["kubernetes_version"] = None
            __props__.__dict__["last_connectivity_time"] = None
            __props__.__dict__["managed_identity_certificate_expiration_time"] = None
            __props__.__dict__["miscellaneous_properties"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["offering"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["total_core_count"] = None
            __props__.__dict__["total_node_count"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:kubernetes:ConnectedCluster"), pulumi.Alias(type_="azure-native:kubernetes/v20200101preview:ConnectedCluster"), pulumi.Alias(type_="azure-native:kubernetes/v20210301:ConnectedCluster"), pulumi.Alias(type_="azure-native:kubernetes/v20210401preview:ConnectedCluster"), pulumi.Alias(type_="azure-native:kubernetes/v20211001:ConnectedCluster"), pulumi.Alias(type_="azure-native:kubernetes/v20220501preview:ConnectedCluster")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ConnectedCluster, __self__).__init__(
            'azure-native:kubernetes/v20221001preview:ConnectedCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ConnectedCluster':
        """
        Get an existing ConnectedCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ConnectedClusterArgs.__new__(ConnectedClusterArgs)

        __props__.__dict__["agent_public_key_certificate"] = None
        __props__.__dict__["agent_version"] = None
        __props__.__dict__["azure_hybrid_benefit"] = None
        __props__.__dict__["connectivity_status"] = None
        __props__.__dict__["distribution"] = None
        __props__.__dict__["distribution_version"] = None
        __props__.__dict__["identity"] = None
        __props__.__dict__["infrastructure"] = None
        __props__.__dict__["kubernetes_version"] = None
        __props__.__dict__["last_connectivity_time"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["managed_identity_certificate_expiration_time"] = None
        __props__.__dict__["miscellaneous_properties"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["offering"] = None
        __props__.__dict__["private_link_scope_resource_id"] = None
        __props__.__dict__["private_link_state"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["total_core_count"] = None
        __props__.__dict__["total_node_count"] = None
        __props__.__dict__["type"] = None
        return ConnectedCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentPublicKeyCertificate")
    def agent_public_key_certificate(self) -> pulumi.Output[str]:
        """
        Base64 encoded public certificate used by the agent to do the initial handshake to the backend services in Azure.
        """
        return pulumi.get(self, "agent_public_key_certificate")

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> pulumi.Output[str]:
        """
        Version of the agent running on the connected cluster resource
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter(name="azureHybridBenefit")
    def azure_hybrid_benefit(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates whether Azure Hybrid Benefit is opted in
        """
        return pulumi.get(self, "azure_hybrid_benefit")

    @property
    @pulumi.getter(name="connectivityStatus")
    def connectivity_status(self) -> pulumi.Output[str]:
        """
        Represents the connectivity status of the connected cluster.
        """
        return pulumi.get(self, "connectivity_status")

    @property
    @pulumi.getter
    def distribution(self) -> pulumi.Output[Optional[str]]:
        """
        The Kubernetes distribution running on this connected cluster.
        """
        return pulumi.get(self, "distribution")

    @property
    @pulumi.getter(name="distributionVersion")
    def distribution_version(self) -> pulumi.Output[Optional[str]]:
        """
        The Kubernetes distribution version on this connected cluster.
        """
        return pulumi.get(self, "distribution_version")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output['outputs.ConnectedClusterIdentityResponse']:
        """
        The identity of the connected cluster.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def infrastructure(self) -> pulumi.Output[Optional[str]]:
        """
        The infrastructure on which the Kubernetes cluster represented by this connected cluster is running on.
        """
        return pulumi.get(self, "infrastructure")

    @property
    @pulumi.getter(name="kubernetesVersion")
    def kubernetes_version(self) -> pulumi.Output[str]:
        """
        The Kubernetes version of the connected cluster resource
        """
        return pulumi.get(self, "kubernetes_version")

    @property
    @pulumi.getter(name="lastConnectivityTime")
    def last_connectivity_time(self) -> pulumi.Output[str]:
        """
        Time representing the last instance when heart beat was received from the cluster
        """
        return pulumi.get(self, "last_connectivity_time")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedIdentityCertificateExpirationTime")
    def managed_identity_certificate_expiration_time(self) -> pulumi.Output[str]:
        """
        Expiration time of the managed identity certificate
        """
        return pulumi.get(self, "managed_identity_certificate_expiration_time")

    @property
    @pulumi.getter(name="miscellaneousProperties")
    def miscellaneous_properties(self) -> pulumi.Output[Mapping[str, str]]:
        """
        More properties related to the Connected Cluster
        """
        return pulumi.get(self, "miscellaneous_properties")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def offering(self) -> pulumi.Output[str]:
        """
        Connected cluster offering
        """
        return pulumi.get(self, "offering")

    @property
    @pulumi.getter(name="privateLinkScopeResourceId")
    def private_link_scope_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource id of the private link scope this connected cluster is assigned to, if any.
        """
        return pulumi.get(self, "private_link_scope_resource_id")

    @property
    @pulumi.getter(name="privateLinkState")
    def private_link_state(self) -> pulumi.Output[Optional[str]]:
        """
        Property which describes the state of private link on a connected cluster resource.
        """
        return pulumi.get(self, "private_link_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Provisioning state of the connected cluster resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Metadata pertaining to creation and last modification of the resource
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="totalCoreCount")
    def total_core_count(self) -> pulumi.Output[int]:
        """
        Number of CPU cores present in the connected cluster resource
        """
        return pulumi.get(self, "total_core_count")

    @property
    @pulumi.getter(name="totalNodeCount")
    def total_node_count(self) -> pulumi.Output[int]:
        """
        Number of nodes present in the connected cluster resource
        """
        return pulumi.get(self, "total_node_count")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

