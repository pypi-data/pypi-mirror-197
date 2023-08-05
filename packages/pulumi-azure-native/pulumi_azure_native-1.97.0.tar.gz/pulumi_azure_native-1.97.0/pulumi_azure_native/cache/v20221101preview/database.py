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

__all__ = ['DatabaseArgs', 'Database']

@pulumi.input_type
class DatabaseArgs:
    def __init__(__self__, *,
                 cluster_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 client_protocol: Optional[pulumi.Input[Union[str, 'Protocol']]] = None,
                 clustering_policy: Optional[pulumi.Input[Union[str, 'ClusteringPolicy']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 eviction_policy: Optional[pulumi.Input[Union[str, 'EvictionPolicy']]] = None,
                 geo_replication: Optional[pulumi.Input['DatabasePropertiesGeoReplicationArgs']] = None,
                 modules: Optional[pulumi.Input[Sequence[pulumi.Input['ModuleArgs']]]] = None,
                 persistence: Optional[pulumi.Input['PersistenceArgs']] = None,
                 port: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Database resource.
        :param pulumi.Input[str] cluster_name: The name of the RedisEnterprise cluster.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[Union[str, 'Protocol']] client_protocol: Specifies whether redis clients can connect using TLS-encrypted or plaintext redis protocols. Default is TLS-encrypted.
        :param pulumi.Input[Union[str, 'ClusteringPolicy']] clustering_policy: Clustering policy - default is OSSCluster. Specified at create time.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[Union[str, 'EvictionPolicy']] eviction_policy: Redis eviction policy - default is VolatileLRU
        :param pulumi.Input['DatabasePropertiesGeoReplicationArgs'] geo_replication: Optional set of properties to configure geo replication for this database.
        :param pulumi.Input[Sequence[pulumi.Input['ModuleArgs']]] modules: Optional set of redis modules to enable in this database - modules can only be added at creation time.
        :param pulumi.Input['PersistenceArgs'] persistence: Persistence settings
        :param pulumi.Input[int] port: TCP port of the database endpoint. Specified at create time. Defaults to an available port.
        """
        pulumi.set(__self__, "cluster_name", cluster_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if client_protocol is not None:
            pulumi.set(__self__, "client_protocol", client_protocol)
        if clustering_policy is not None:
            pulumi.set(__self__, "clustering_policy", clustering_policy)
        if database_name is not None:
            pulumi.set(__self__, "database_name", database_name)
        if eviction_policy is not None:
            pulumi.set(__self__, "eviction_policy", eviction_policy)
        if geo_replication is not None:
            pulumi.set(__self__, "geo_replication", geo_replication)
        if modules is not None:
            pulumi.set(__self__, "modules", modules)
        if persistence is not None:
            pulumi.set(__self__, "persistence", persistence)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        The name of the RedisEnterprise cluster.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

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
    @pulumi.getter(name="clientProtocol")
    def client_protocol(self) -> Optional[pulumi.Input[Union[str, 'Protocol']]]:
        """
        Specifies whether redis clients can connect using TLS-encrypted or plaintext redis protocols. Default is TLS-encrypted.
        """
        return pulumi.get(self, "client_protocol")

    @client_protocol.setter
    def client_protocol(self, value: Optional[pulumi.Input[Union[str, 'Protocol']]]):
        pulumi.set(self, "client_protocol", value)

    @property
    @pulumi.getter(name="clusteringPolicy")
    def clustering_policy(self) -> Optional[pulumi.Input[Union[str, 'ClusteringPolicy']]]:
        """
        Clustering policy - default is OSSCluster. Specified at create time.
        """
        return pulumi.get(self, "clustering_policy")

    @clustering_policy.setter
    def clustering_policy(self, value: Optional[pulumi.Input[Union[str, 'ClusteringPolicy']]]):
        pulumi.set(self, "clustering_policy", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the database.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter(name="evictionPolicy")
    def eviction_policy(self) -> Optional[pulumi.Input[Union[str, 'EvictionPolicy']]]:
        """
        Redis eviction policy - default is VolatileLRU
        """
        return pulumi.get(self, "eviction_policy")

    @eviction_policy.setter
    def eviction_policy(self, value: Optional[pulumi.Input[Union[str, 'EvictionPolicy']]]):
        pulumi.set(self, "eviction_policy", value)

    @property
    @pulumi.getter(name="geoReplication")
    def geo_replication(self) -> Optional[pulumi.Input['DatabasePropertiesGeoReplicationArgs']]:
        """
        Optional set of properties to configure geo replication for this database.
        """
        return pulumi.get(self, "geo_replication")

    @geo_replication.setter
    def geo_replication(self, value: Optional[pulumi.Input['DatabasePropertiesGeoReplicationArgs']]):
        pulumi.set(self, "geo_replication", value)

    @property
    @pulumi.getter
    def modules(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ModuleArgs']]]]:
        """
        Optional set of redis modules to enable in this database - modules can only be added at creation time.
        """
        return pulumi.get(self, "modules")

    @modules.setter
    def modules(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ModuleArgs']]]]):
        pulumi.set(self, "modules", value)

    @property
    @pulumi.getter
    def persistence(self) -> Optional[pulumi.Input['PersistenceArgs']]:
        """
        Persistence settings
        """
        return pulumi.get(self, "persistence")

    @persistence.setter
    def persistence(self, value: Optional[pulumi.Input['PersistenceArgs']]):
        pulumi.set(self, "persistence", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        TCP port of the database endpoint. Specified at create time. Defaults to an available port.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


class Database(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_protocol: Optional[pulumi.Input[Union[str, 'Protocol']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 clustering_policy: Optional[pulumi.Input[Union[str, 'ClusteringPolicy']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 eviction_policy: Optional[pulumi.Input[Union[str, 'EvictionPolicy']]] = None,
                 geo_replication: Optional[pulumi.Input[pulumi.InputType['DatabasePropertiesGeoReplicationArgs']]] = None,
                 modules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModuleArgs']]]]] = None,
                 persistence: Optional[pulumi.Input[pulumi.InputType['PersistenceArgs']]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Describes a database on the RedisEnterprise cluster

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'Protocol']] client_protocol: Specifies whether redis clients can connect using TLS-encrypted or plaintext redis protocols. Default is TLS-encrypted.
        :param pulumi.Input[str] cluster_name: The name of the RedisEnterprise cluster.
        :param pulumi.Input[Union[str, 'ClusteringPolicy']] clustering_policy: Clustering policy - default is OSSCluster. Specified at create time.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[Union[str, 'EvictionPolicy']] eviction_policy: Redis eviction policy - default is VolatileLRU
        :param pulumi.Input[pulumi.InputType['DatabasePropertiesGeoReplicationArgs']] geo_replication: Optional set of properties to configure geo replication for this database.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModuleArgs']]]] modules: Optional set of redis modules to enable in this database - modules can only be added at creation time.
        :param pulumi.Input[pulumi.InputType['PersistenceArgs']] persistence: Persistence settings
        :param pulumi.Input[int] port: TCP port of the database endpoint. Specified at create time. Defaults to an available port.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabaseArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Describes a database on the RedisEnterprise cluster

        :param str resource_name: The name of the resource.
        :param DatabaseArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 client_protocol: Optional[pulumi.Input[Union[str, 'Protocol']]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 clustering_policy: Optional[pulumi.Input[Union[str, 'ClusteringPolicy']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 eviction_policy: Optional[pulumi.Input[Union[str, 'EvictionPolicy']]] = None,
                 geo_replication: Optional[pulumi.Input[pulumi.InputType['DatabasePropertiesGeoReplicationArgs']]] = None,
                 modules: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ModuleArgs']]]]] = None,
                 persistence: Optional[pulumi.Input[pulumi.InputType['PersistenceArgs']]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseArgs.__new__(DatabaseArgs)

            __props__.__dict__["client_protocol"] = client_protocol
            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["clustering_policy"] = clustering_policy
            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["eviction_policy"] = eviction_policy
            __props__.__dict__["geo_replication"] = geo_replication
            __props__.__dict__["modules"] = modules
            __props__.__dict__["persistence"] = persistence
            __props__.__dict__["port"] = port
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:cache:Database"), pulumi.Alias(type_="azure-native:cache/v20201001preview:Database"), pulumi.Alias(type_="azure-native:cache/v20210201preview:Database"), pulumi.Alias(type_="azure-native:cache/v20210301:Database"), pulumi.Alias(type_="azure-native:cache/v20210801:Database"), pulumi.Alias(type_="azure-native:cache/v20220101:Database"), pulumi.Alias(type_="azure-native:cache/v20230301preview:Database")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Database, __self__).__init__(
            'azure-native:cache/v20221101preview:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DatabaseArgs.__new__(DatabaseArgs)

        __props__.__dict__["client_protocol"] = None
        __props__.__dict__["clustering_policy"] = None
        __props__.__dict__["eviction_policy"] = None
        __props__.__dict__["geo_replication"] = None
        __props__.__dict__["modules"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["persistence"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clientProtocol")
    def client_protocol(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies whether redis clients can connect using TLS-encrypted or plaintext redis protocols. Default is TLS-encrypted.
        """
        return pulumi.get(self, "client_protocol")

    @property
    @pulumi.getter(name="clusteringPolicy")
    def clustering_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Clustering policy - default is OSSCluster. Specified at create time.
        """
        return pulumi.get(self, "clustering_policy")

    @property
    @pulumi.getter(name="evictionPolicy")
    def eviction_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Redis eviction policy - default is VolatileLRU
        """
        return pulumi.get(self, "eviction_policy")

    @property
    @pulumi.getter(name="geoReplication")
    def geo_replication(self) -> pulumi.Output[Optional['outputs.DatabasePropertiesResponseGeoReplication']]:
        """
        Optional set of properties to configure geo replication for this database.
        """
        return pulumi.get(self, "geo_replication")

    @property
    @pulumi.getter
    def modules(self) -> pulumi.Output[Optional[Sequence['outputs.ModuleResponse']]]:
        """
        Optional set of redis modules to enable in this database - modules can only be added at creation time.
        """
        return pulumi.get(self, "modules")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def persistence(self) -> pulumi.Output[Optional['outputs.PersistenceResponse']]:
        """
        Persistence settings
        """
        return pulumi.get(self, "persistence")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        """
        TCP port of the database endpoint. Specified at create time. Defaults to an available port.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Current provisioning status of the database
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        Current resource status of the database
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

