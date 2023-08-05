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
    'GetHostPoolResult',
    'AwaitableGetHostPoolResult',
    'get_host_pool',
    'get_host_pool_output',
]

@pulumi.output_type
class GetHostPoolResult:
    """
    Represents a HostPool definition.
    """
    def __init__(__self__, application_group_references=None, cloud_pc_resource=None, custom_rdp_property=None, description=None, etag=None, friendly_name=None, host_pool_type=None, id=None, identity=None, kind=None, load_balancer_type=None, location=None, managed_by=None, max_session_limit=None, migration_request=None, name=None, object_id=None, personal_desktop_assignment_type=None, plan=None, preferred_app_group_type=None, registration_info=None, ring=None, sku=None, sso_client_id=None, sso_client_secret_key_vault_path=None, sso_secret_type=None, ssoadfs_authority=None, start_vm_on_connect=None, tags=None, type=None, validation_environment=None, vm_template=None):
        if application_group_references and not isinstance(application_group_references, list):
            raise TypeError("Expected argument 'application_group_references' to be a list")
        pulumi.set(__self__, "application_group_references", application_group_references)
        if cloud_pc_resource and not isinstance(cloud_pc_resource, bool):
            raise TypeError("Expected argument 'cloud_pc_resource' to be a bool")
        pulumi.set(__self__, "cloud_pc_resource", cloud_pc_resource)
        if custom_rdp_property and not isinstance(custom_rdp_property, str):
            raise TypeError("Expected argument 'custom_rdp_property' to be a str")
        pulumi.set(__self__, "custom_rdp_property", custom_rdp_property)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if friendly_name and not isinstance(friendly_name, str):
            raise TypeError("Expected argument 'friendly_name' to be a str")
        pulumi.set(__self__, "friendly_name", friendly_name)
        if host_pool_type and not isinstance(host_pool_type, str):
            raise TypeError("Expected argument 'host_pool_type' to be a str")
        pulumi.set(__self__, "host_pool_type", host_pool_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if load_balancer_type and not isinstance(load_balancer_type, str):
            raise TypeError("Expected argument 'load_balancer_type' to be a str")
        pulumi.set(__self__, "load_balancer_type", load_balancer_type)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if managed_by and not isinstance(managed_by, str):
            raise TypeError("Expected argument 'managed_by' to be a str")
        pulumi.set(__self__, "managed_by", managed_by)
        if max_session_limit and not isinstance(max_session_limit, int):
            raise TypeError("Expected argument 'max_session_limit' to be a int")
        pulumi.set(__self__, "max_session_limit", max_session_limit)
        if migration_request and not isinstance(migration_request, dict):
            raise TypeError("Expected argument 'migration_request' to be a dict")
        pulumi.set(__self__, "migration_request", migration_request)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if object_id and not isinstance(object_id, str):
            raise TypeError("Expected argument 'object_id' to be a str")
        pulumi.set(__self__, "object_id", object_id)
        if personal_desktop_assignment_type and not isinstance(personal_desktop_assignment_type, str):
            raise TypeError("Expected argument 'personal_desktop_assignment_type' to be a str")
        pulumi.set(__self__, "personal_desktop_assignment_type", personal_desktop_assignment_type)
        if plan and not isinstance(plan, dict):
            raise TypeError("Expected argument 'plan' to be a dict")
        pulumi.set(__self__, "plan", plan)
        if preferred_app_group_type and not isinstance(preferred_app_group_type, str):
            raise TypeError("Expected argument 'preferred_app_group_type' to be a str")
        pulumi.set(__self__, "preferred_app_group_type", preferred_app_group_type)
        if registration_info and not isinstance(registration_info, dict):
            raise TypeError("Expected argument 'registration_info' to be a dict")
        pulumi.set(__self__, "registration_info", registration_info)
        if ring and not isinstance(ring, int):
            raise TypeError("Expected argument 'ring' to be a int")
        pulumi.set(__self__, "ring", ring)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if sso_client_id and not isinstance(sso_client_id, str):
            raise TypeError("Expected argument 'sso_client_id' to be a str")
        pulumi.set(__self__, "sso_client_id", sso_client_id)
        if sso_client_secret_key_vault_path and not isinstance(sso_client_secret_key_vault_path, str):
            raise TypeError("Expected argument 'sso_client_secret_key_vault_path' to be a str")
        pulumi.set(__self__, "sso_client_secret_key_vault_path", sso_client_secret_key_vault_path)
        if sso_secret_type and not isinstance(sso_secret_type, str):
            raise TypeError("Expected argument 'sso_secret_type' to be a str")
        pulumi.set(__self__, "sso_secret_type", sso_secret_type)
        if ssoadfs_authority and not isinstance(ssoadfs_authority, str):
            raise TypeError("Expected argument 'ssoadfs_authority' to be a str")
        pulumi.set(__self__, "ssoadfs_authority", ssoadfs_authority)
        if start_vm_on_connect and not isinstance(start_vm_on_connect, bool):
            raise TypeError("Expected argument 'start_vm_on_connect' to be a bool")
        pulumi.set(__self__, "start_vm_on_connect", start_vm_on_connect)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if validation_environment and not isinstance(validation_environment, bool):
            raise TypeError("Expected argument 'validation_environment' to be a bool")
        pulumi.set(__self__, "validation_environment", validation_environment)
        if vm_template and not isinstance(vm_template, str):
            raise TypeError("Expected argument 'vm_template' to be a str")
        pulumi.set(__self__, "vm_template", vm_template)

    @property
    @pulumi.getter(name="applicationGroupReferences")
    def application_group_references(self) -> Sequence[str]:
        """
        List of applicationGroup links.
        """
        return pulumi.get(self, "application_group_references")

    @property
    @pulumi.getter(name="cloudPcResource")
    def cloud_pc_resource(self) -> bool:
        """
        Is cloud pc resource.
        """
        return pulumi.get(self, "cloud_pc_resource")

    @property
    @pulumi.getter(name="customRdpProperty")
    def custom_rdp_property(self) -> Optional[str]:
        """
        Custom rdp property of HostPool.
        """
        return pulumi.get(self, "custom_rdp_property")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of HostPool.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        The etag field is *not* required. If it is provided in the response body, it must also be provided as a header per the normal etag convention.  Entity tags are used for comparing two or more entities from the same requested resource. HTTP/1.1 uses entity tags in the etag (section 14.19), If-Match (section 14.24), If-None-Match (section 14.26), and If-Range (section 14.27) header fields. 
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[str]:
        """
        Friendly name of HostPool.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostPoolType")
    def host_pool_type(self) -> str:
        """
        HostPool type for desktop.
        """
        return pulumi.get(self, "host_pool_type")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.ResourceModelWithAllowedPropertySetResponseIdentity']:
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Metadata used by portal/tooling/etc to render different UX experiences for resources of the same type; e.g. ApiApps are a kind of Microsoft.Web/sites type.  If supported, the resource provider must validate and persist this value.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="loadBalancerType")
    def load_balancer_type(self) -> str:
        """
        The type of the load balancer.
        """
        return pulumi.get(self, "load_balancer_type")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> Optional[str]:
        """
        The fully qualified resource ID of the resource that manages this resource. Indicates if this resource is managed by another Azure resource. If this is present, complete mode deployment will not delete the resource if it is removed from the template since it is managed by another resource.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter(name="maxSessionLimit")
    def max_session_limit(self) -> Optional[int]:
        """
        The max session limit of HostPool.
        """
        return pulumi.get(self, "max_session_limit")

    @property
    @pulumi.getter(name="migrationRequest")
    def migration_request(self) -> Optional['outputs.MigrationRequestPropertiesResponse']:
        """
        The registration info of HostPool.
        """
        return pulumi.get(self, "migration_request")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> str:
        """
        ObjectId of HostPool. (internal use)
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="personalDesktopAssignmentType")
    def personal_desktop_assignment_type(self) -> Optional[str]:
        """
        PersonalDesktopAssignment type for HostPool.
        """
        return pulumi.get(self, "personal_desktop_assignment_type")

    @property
    @pulumi.getter
    def plan(self) -> Optional['outputs.ResourceModelWithAllowedPropertySetResponsePlan']:
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter(name="preferredAppGroupType")
    def preferred_app_group_type(self) -> str:
        """
        The type of preferred application group type, default to Desktop Application Group
        """
        return pulumi.get(self, "preferred_app_group_type")

    @property
    @pulumi.getter(name="registrationInfo")
    def registration_info(self) -> Optional['outputs.RegistrationInfoResponse']:
        """
        The registration info of HostPool.
        """
        return pulumi.get(self, "registration_info")

    @property
    @pulumi.getter
    def ring(self) -> Optional[int]:
        """
        The ring number of HostPool.
        """
        return pulumi.get(self, "ring")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.ResourceModelWithAllowedPropertySetResponseSku']:
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="ssoClientId")
    def sso_client_id(self) -> Optional[str]:
        """
        ClientId for the registered Relying Party used to issue WVD SSO certificates.
        """
        return pulumi.get(self, "sso_client_id")

    @property
    @pulumi.getter(name="ssoClientSecretKeyVaultPath")
    def sso_client_secret_key_vault_path(self) -> Optional[str]:
        """
        Path to Azure KeyVault storing the secret used for communication to ADFS.
        """
        return pulumi.get(self, "sso_client_secret_key_vault_path")

    @property
    @pulumi.getter(name="ssoSecretType")
    def sso_secret_type(self) -> Optional[str]:
        """
        The type of single sign on Secret Type.
        """
        return pulumi.get(self, "sso_secret_type")

    @property
    @pulumi.getter(name="ssoadfsAuthority")
    def ssoadfs_authority(self) -> Optional[str]:
        """
        URL to customer ADFS server for signing WVD SSO certificates.
        """
        return pulumi.get(self, "ssoadfs_authority")

    @property
    @pulumi.getter(name="startVMOnConnect")
    def start_vm_on_connect(self) -> Optional[bool]:
        """
        The flag to turn on/off StartVMOnConnect feature.
        """
        return pulumi.get(self, "start_vm_on_connect")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="validationEnvironment")
    def validation_environment(self) -> Optional[bool]:
        """
        Is validation environment.
        """
        return pulumi.get(self, "validation_environment")

    @property
    @pulumi.getter(name="vmTemplate")
    def vm_template(self) -> Optional[str]:
        """
        VM template for sessionhosts configuration within hostpool.
        """
        return pulumi.get(self, "vm_template")


class AwaitableGetHostPoolResult(GetHostPoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHostPoolResult(
            application_group_references=self.application_group_references,
            cloud_pc_resource=self.cloud_pc_resource,
            custom_rdp_property=self.custom_rdp_property,
            description=self.description,
            etag=self.etag,
            friendly_name=self.friendly_name,
            host_pool_type=self.host_pool_type,
            id=self.id,
            identity=self.identity,
            kind=self.kind,
            load_balancer_type=self.load_balancer_type,
            location=self.location,
            managed_by=self.managed_by,
            max_session_limit=self.max_session_limit,
            migration_request=self.migration_request,
            name=self.name,
            object_id=self.object_id,
            personal_desktop_assignment_type=self.personal_desktop_assignment_type,
            plan=self.plan,
            preferred_app_group_type=self.preferred_app_group_type,
            registration_info=self.registration_info,
            ring=self.ring,
            sku=self.sku,
            sso_client_id=self.sso_client_id,
            sso_client_secret_key_vault_path=self.sso_client_secret_key_vault_path,
            sso_secret_type=self.sso_secret_type,
            ssoadfs_authority=self.ssoadfs_authority,
            start_vm_on_connect=self.start_vm_on_connect,
            tags=self.tags,
            type=self.type,
            validation_environment=self.validation_environment,
            vm_template=self.vm_template)


def get_host_pool(host_pool_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHostPoolResult:
    """
    Get a host pool.
    API Version: 2021-02-01-preview.


    :param str host_pool_name: The name of the host pool within the specified resource group
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['hostPoolName'] = host_pool_name
    __args__['resourceGroupName'] = resource_group_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('azure-native:desktopvirtualization:getHostPool', __args__, opts=opts, typ=GetHostPoolResult).value

    return AwaitableGetHostPoolResult(
        application_group_references=__ret__.application_group_references,
        cloud_pc_resource=__ret__.cloud_pc_resource,
        custom_rdp_property=__ret__.custom_rdp_property,
        description=__ret__.description,
        etag=__ret__.etag,
        friendly_name=__ret__.friendly_name,
        host_pool_type=__ret__.host_pool_type,
        id=__ret__.id,
        identity=__ret__.identity,
        kind=__ret__.kind,
        load_balancer_type=__ret__.load_balancer_type,
        location=__ret__.location,
        managed_by=__ret__.managed_by,
        max_session_limit=__ret__.max_session_limit,
        migration_request=__ret__.migration_request,
        name=__ret__.name,
        object_id=__ret__.object_id,
        personal_desktop_assignment_type=__ret__.personal_desktop_assignment_type,
        plan=__ret__.plan,
        preferred_app_group_type=__ret__.preferred_app_group_type,
        registration_info=__ret__.registration_info,
        ring=__ret__.ring,
        sku=__ret__.sku,
        sso_client_id=__ret__.sso_client_id,
        sso_client_secret_key_vault_path=__ret__.sso_client_secret_key_vault_path,
        sso_secret_type=__ret__.sso_secret_type,
        ssoadfs_authority=__ret__.ssoadfs_authority,
        start_vm_on_connect=__ret__.start_vm_on_connect,
        tags=__ret__.tags,
        type=__ret__.type,
        validation_environment=__ret__.validation_environment,
        vm_template=__ret__.vm_template)


@_utilities.lift_output_func(get_host_pool)
def get_host_pool_output(host_pool_name: Optional[pulumi.Input[str]] = None,
                         resource_group_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHostPoolResult]:
    """
    Get a host pool.
    API Version: 2021-02-01-preview.


    :param str host_pool_name: The name of the host pool within the specified resource group
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
