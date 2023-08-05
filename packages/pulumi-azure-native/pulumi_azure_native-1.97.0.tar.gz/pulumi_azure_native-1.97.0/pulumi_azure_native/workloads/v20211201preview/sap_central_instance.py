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

__all__ = ['SAPCentralInstanceArgs', 'SAPCentralInstance']

@pulumi.input_type
class SAPCentralInstanceArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sap_virtual_instance_name: pulumi.Input[str],
                 central_instance_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SAPCentralInstance resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sap_virtual_instance_name: The name of the Virtual Instances for SAP solutions resource
        :param pulumi.Input[str] central_instance_name: Central Services Instance resource name string modeled as parameter for auto generation to work correctly.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sap_virtual_instance_name", sap_virtual_instance_name)
        if central_instance_name is not None:
            pulumi.set(__self__, "central_instance_name", central_instance_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

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
    @pulumi.getter(name="sapVirtualInstanceName")
    def sap_virtual_instance_name(self) -> pulumi.Input[str]:
        """
        The name of the Virtual Instances for SAP solutions resource
        """
        return pulumi.get(self, "sap_virtual_instance_name")

    @sap_virtual_instance_name.setter
    def sap_virtual_instance_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "sap_virtual_instance_name", value)

    @property
    @pulumi.getter(name="centralInstanceName")
    def central_instance_name(self) -> Optional[pulumi.Input[str]]:
        """
        Central Services Instance resource name string modeled as parameter for auto generation to work correctly.
        """
        return pulumi.get(self, "central_instance_name")

    @central_instance_name.setter
    def central_instance_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "central_instance_name", value)

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
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class SAPCentralInstance(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 central_instance_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_virtual_instance_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Define the SAP Central Services Instance resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] central_instance_name: Central Services Instance resource name string modeled as parameter for auto generation to work correctly.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] sap_virtual_instance_name: The name of the Virtual Instances for SAP solutions resource
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SAPCentralInstanceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Define the SAP Central Services Instance resource.

        :param str resource_name: The name of the resource.
        :param SAPCentralInstanceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SAPCentralInstanceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 central_instance_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sap_virtual_instance_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SAPCentralInstanceArgs.__new__(SAPCentralInstanceArgs)

            __props__.__dict__["central_instance_name"] = central_instance_name
            __props__.__dict__["location"] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if sap_virtual_instance_name is None and not opts.urn:
                raise TypeError("Missing required property 'sap_virtual_instance_name'")
            __props__.__dict__["sap_virtual_instance_name"] = sap_virtual_instance_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["enqueue_replication_server_properties"] = None
            __props__.__dict__["enqueue_server_properties"] = None
            __props__.__dict__["errors"] = None
            __props__.__dict__["gateway_server_properties"] = None
            __props__.__dict__["health"] = None
            __props__.__dict__["instance_no"] = None
            __props__.__dict__["kernel_patch"] = None
            __props__.__dict__["kernel_version"] = None
            __props__.__dict__["load_balancer_details"] = None
            __props__.__dict__["message_server_properties"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["subnet"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["vm_details"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:workloads:SAPCentralInstance"), pulumi.Alias(type_="azure-native:workloads/v20221101preview:SAPCentralInstance"), pulumi.Alias(type_="azure-native:workloads/v20230401:SAPCentralInstance")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SAPCentralInstance, __self__).__init__(
            'azure-native:workloads/v20211201preview:SAPCentralInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SAPCentralInstance':
        """
        Get an existing SAPCentralInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SAPCentralInstanceArgs.__new__(SAPCentralInstanceArgs)

        __props__.__dict__["enqueue_replication_server_properties"] = None
        __props__.__dict__["enqueue_server_properties"] = None
        __props__.__dict__["errors"] = None
        __props__.__dict__["gateway_server_properties"] = None
        __props__.__dict__["health"] = None
        __props__.__dict__["instance_no"] = None
        __props__.__dict__["kernel_patch"] = None
        __props__.__dict__["kernel_version"] = None
        __props__.__dict__["load_balancer_details"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["message_server_properties"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["subnet"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["vm_details"] = None
        return SAPCentralInstance(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="enqueueReplicationServerProperties")
    def enqueue_replication_server_properties(self) -> pulumi.Output[Optional['outputs.EnqueueReplicationServerPropertiesResponse']]:
        """
        Defines the SAP Enqueue Replication Server (ERS) properties.
        """
        return pulumi.get(self, "enqueue_replication_server_properties")

    @property
    @pulumi.getter(name="enqueueServerProperties")
    def enqueue_server_properties(self) -> pulumi.Output[Optional['outputs.EnqueueServerPropertiesResponse']]:
        """
        Defines the SAP Enqueue Server properties.
        """
        return pulumi.get(self, "enqueue_server_properties")

    @property
    @pulumi.getter
    def errors(self) -> pulumi.Output['outputs.SAPVirtualInstanceErrorResponse']:
        """
        Defines the errors related to SAP Central Services Instance resource.
        """
        return pulumi.get(self, "errors")

    @property
    @pulumi.getter(name="gatewayServerProperties")
    def gateway_server_properties(self) -> pulumi.Output[Optional['outputs.GatewayServerPropertiesResponse']]:
        """
        Defines the SAP Gateway Server properties.
        """
        return pulumi.get(self, "gateway_server_properties")

    @property
    @pulumi.getter
    def health(self) -> pulumi.Output[str]:
        """
        Defines the health of SAP Instances.
        """
        return pulumi.get(self, "health")

    @property
    @pulumi.getter(name="instanceNo")
    def instance_no(self) -> pulumi.Output[str]:
        """
        The central services instance number.
        """
        return pulumi.get(self, "instance_no")

    @property
    @pulumi.getter(name="kernelPatch")
    def kernel_patch(self) -> pulumi.Output[str]:
        """
        The central services instance Kernel Patch level.
        """
        return pulumi.get(self, "kernel_patch")

    @property
    @pulumi.getter(name="kernelVersion")
    def kernel_version(self) -> pulumi.Output[str]:
        """
        The central services instance Kernel Version.
        """
        return pulumi.get(self, "kernel_version")

    @property
    @pulumi.getter(name="loadBalancerDetails")
    def load_balancer_details(self) -> pulumi.Output['outputs.LoadBalancerDetailsResponse']:
        """
        The Load Balancer details such as LoadBalancer ID attached to ASCS Virtual Machines
        """
        return pulumi.get(self, "load_balancer_details")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="messageServerProperties")
    def message_server_properties(self) -> pulumi.Output[Optional['outputs.MessageServerPropertiesResponse']]:
        """
        Defines the SAP Message Server properties.
        """
        return pulumi.get(self, "message_server_properties")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Defines the provisioning states.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Defines the SAP Instance status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def subnet(self) -> pulumi.Output[str]:
        """
        The central services instance subnet.
        """
        return pulumi.get(self, "subnet")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
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
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vmDetails")
    def vm_details(self) -> pulumi.Output[Sequence['outputs.CentralServerVmDetailsResponse']]:
        """
        The list of virtual machines corresponding to the Central Services instance.
        """
        return pulumi.get(self, "vm_details")

