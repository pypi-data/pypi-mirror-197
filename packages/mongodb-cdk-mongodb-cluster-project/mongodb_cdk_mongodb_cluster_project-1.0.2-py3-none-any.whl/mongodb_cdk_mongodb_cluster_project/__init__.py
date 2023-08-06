'''
# @mongodbatlas-awscdk/cluster

The official [MongoDB Atlas](https://www.mongodb.com/) AWS CDK resource for Node.js.

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `MongoDB::Atlas::Cluster` v1.0.0.

## Description

The cluster resource provides access to your cluster configurations. The resource lets you create, edit and delete clusters. The resource requires your Project ID.

## MongoDB Atlas API Docs

For more information about the API refer to: [API Endpoints](https://www.mongodb.com/docs/atlas/reference/api-resources-spec/#tag/Clusters)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name MongoDB::Atlas::Cluster \
  --publisher-id bb989456c78c398a858fef18f2ca1bfc1fbba082 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/bb989456c78c398a858fef18f2ca1bfc1fbba082/MongoDB-Atlas-Cluster \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `MongoDB::Atlas::Cluster`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fmongodb-atlas-cluster+v1.0.0).
* Issues related to `MongoDB::Atlas::Cluster` should be reported to the [publisher](https://github.com/mongodb/mongodbatlas-cloudformation-resources/issues).
* Feature requests should be [reported here](https://feedback.mongodb.com/forums/924145-atlas?category_id=392596)

## License

Distributed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.AdvancedAutoScaling",
    jsii_struct_bases=[],
    name_mapping={"compute": "compute", "disk_gb": "diskGb"},
)
class AdvancedAutoScaling:
    def __init__(
        self,
        *,
        compute: typing.Optional[typing.Union["Compute", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_gb: typing.Optional[typing.Union["DiskGb", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''AWS Automatic Cluster Scaling.

        :param compute: 
        :param disk_gb: 

        :schema: advancedAutoScaling
        '''
        if isinstance(compute, dict):
            compute = Compute(**compute)
        if isinstance(disk_gb, dict):
            disk_gb = DiskGb(**disk_gb)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d18b81adb1d348c704cd7ce6d97ea93341d53db8ac74a93c2304ebbe294ea3db)
            check_type(argname="argument compute", value=compute, expected_type=type_hints["compute"])
            check_type(argname="argument disk_gb", value=disk_gb, expected_type=type_hints["disk_gb"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute is not None:
            self._values["compute"] = compute
        if disk_gb is not None:
            self._values["disk_gb"] = disk_gb

    @builtins.property
    def compute(self) -> typing.Optional["Compute"]:
        '''
        :schema: advancedAutoScaling#Compute
        '''
        result = self._values.get("compute")
        return typing.cast(typing.Optional["Compute"], result)

    @builtins.property
    def disk_gb(self) -> typing.Optional["DiskGb"]:
        '''
        :schema: advancedAutoScaling#DiskGB
        '''
        result = self._values.get("disk_gb")
        return typing.cast(typing.Optional["DiskGb"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.AdvancedRegionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "analytics_auto_scaling": "analyticsAutoScaling",
        "analytics_specs": "analyticsSpecs",
        "auto_scaling": "autoScaling",
        "electable_specs": "electableSpecs",
        "priority": "priority",
        "read_only_specs": "readOnlySpecs",
        "region_name": "regionName",
    },
)
class AdvancedRegionConfig:
    def __init__(
        self,
        *,
        analytics_auto_scaling: typing.Optional[typing.Union[AdvancedAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        analytics_specs: typing.Optional[typing.Union["Specs", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling: typing.Optional[typing.Union[AdvancedAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
        electable_specs: typing.Optional[typing.Union["Specs", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[jsii.Number] = None,
        read_only_specs: typing.Optional[typing.Union["Specs", typing.Dict[builtins.str, typing.Any]]] = None,
        region_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Hardware specifications for nodes set for a given region.

        Each regionConfigs object describes the region's priority in elections and the number and type of MongoDB nodes that MongoDB Cloud deploys to the region. Each regionConfigs object must have either an analyticsSpecs object, electableSpecs object, or readOnlySpecs object. Tenant clusters only require electableSpecs. Dedicated clusters can specify any of these specifications, but must have at least one electableSpecs object within a replicationSpec. Every hardware specification must use the same instanceSize.

        Example:

        If you set "replicationSpecs[n].regionConfigs[m].analyticsSpecs.instanceSize" : "M30", set "replicationSpecs[n].regionConfigs[m].electableSpecs.instanceSize" : "M30"if you have electable nodes and"replicationSpecs[n].regionConfigs[m].readOnlySpecs.instanceSize" : "M30" if you have read-only nodes.",

        :param analytics_auto_scaling: 
        :param analytics_specs: 
        :param auto_scaling: 
        :param electable_specs: 
        :param priority: 
        :param read_only_specs: 
        :param region_name: 

        :schema: advancedRegionConfig
        '''
        if isinstance(analytics_auto_scaling, dict):
            analytics_auto_scaling = AdvancedAutoScaling(**analytics_auto_scaling)
        if isinstance(analytics_specs, dict):
            analytics_specs = Specs(**analytics_specs)
        if isinstance(auto_scaling, dict):
            auto_scaling = AdvancedAutoScaling(**auto_scaling)
        if isinstance(electable_specs, dict):
            electable_specs = Specs(**electable_specs)
        if isinstance(read_only_specs, dict):
            read_only_specs = Specs(**read_only_specs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__598b4f40138e39a15924208c786865138be1508cd2c38bc001b1d497c28c0268)
            check_type(argname="argument analytics_auto_scaling", value=analytics_auto_scaling, expected_type=type_hints["analytics_auto_scaling"])
            check_type(argname="argument analytics_specs", value=analytics_specs, expected_type=type_hints["analytics_specs"])
            check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
            check_type(argname="argument electable_specs", value=electable_specs, expected_type=type_hints["electable_specs"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument read_only_specs", value=read_only_specs, expected_type=type_hints["read_only_specs"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analytics_auto_scaling is not None:
            self._values["analytics_auto_scaling"] = analytics_auto_scaling
        if analytics_specs is not None:
            self._values["analytics_specs"] = analytics_specs
        if auto_scaling is not None:
            self._values["auto_scaling"] = auto_scaling
        if electable_specs is not None:
            self._values["electable_specs"] = electable_specs
        if priority is not None:
            self._values["priority"] = priority
        if read_only_specs is not None:
            self._values["read_only_specs"] = read_only_specs
        if region_name is not None:
            self._values["region_name"] = region_name

    @builtins.property
    def analytics_auto_scaling(self) -> typing.Optional[AdvancedAutoScaling]:
        '''
        :schema: advancedRegionConfig#AnalyticsAutoScaling
        '''
        result = self._values.get("analytics_auto_scaling")
        return typing.cast(typing.Optional[AdvancedAutoScaling], result)

    @builtins.property
    def analytics_specs(self) -> typing.Optional["Specs"]:
        '''
        :schema: advancedRegionConfig#AnalyticsSpecs
        '''
        result = self._values.get("analytics_specs")
        return typing.cast(typing.Optional["Specs"], result)

    @builtins.property
    def auto_scaling(self) -> typing.Optional[AdvancedAutoScaling]:
        '''
        :schema: advancedRegionConfig#AutoScaling
        '''
        result = self._values.get("auto_scaling")
        return typing.cast(typing.Optional[AdvancedAutoScaling], result)

    @builtins.property
    def electable_specs(self) -> typing.Optional["Specs"]:
        '''
        :schema: advancedRegionConfig#ElectableSpecs
        '''
        result = self._values.get("electable_specs")
        return typing.cast(typing.Optional["Specs"], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: advancedRegionConfig#Priority
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_only_specs(self) -> typing.Optional["Specs"]:
        '''
        :schema: advancedRegionConfig#ReadOnlySpecs
        '''
        result = self._values.get("read_only_specs")
        return typing.cast(typing.Optional["Specs"], result)

    @builtins.property
    def region_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: advancedRegionConfig#RegionName
        '''
        result = self._values.get("region_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedRegionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.AdvancedReplicationSpec",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_region_configs": "advancedRegionConfigs",
        "id": "id",
        "num_shards": "numShards",
        "zone_name": "zoneName",
    },
)
class AdvancedReplicationSpec:
    def __init__(
        self,
        *,
        advanced_region_configs: typing.Optional[typing.Sequence[typing.Union[AdvancedRegionConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        id: typing.Optional[builtins.str] = None,
        num_shards: typing.Optional[jsii.Number] = None,
        zone_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''List of settings that configure your cluster regions.

        For Global Clusters, each object in the array represents a zone where your clusters nodes deploy. For non-Global replica sets and sharded clusters, this array has one object representing where your clusters nodes deploy.

        :param advanced_region_configs: Hardware specifications for nodes set for a given region. Each regionConfigs object describes the region's priority in elections and the number and type of MongoDB nodes that MongoDB Cloud deploys to the region. Each regionConfigs object must have either an analyticsSpecs object, electableSpecs object, or readOnlySpecs object. Tenant clusters only require electableSpecs. Dedicated clusters can specify any of these specifications, but must have at least one electableSpecs object within a replicationSpec. Every hardware specification must use the same instanceSize. Example: If you set "replicationSpecs[n].regionConfigs[m].analyticsSpecs.instanceSize" : "M30", set "replicationSpecs[n].regionConfigs[m].electableSpecs.instanceSize" : "M30"if you have electable nodes and"replicationSpecs[n].regionConfigs[m].readOnlySpecs.instanceSize" : "M30" if you have read-only nodes.",
        :param id: Unique 24-hexadecimal digit string that identifies the replication object for a zone in a Multi-Cloud Cluster. If you include existing zones in the request, you must specify this parameter. If you add a new zone to an existing Multi-Cloud Cluster, you may specify this parameter. The request deletes any existing zones in the Multi-Cloud Cluster that you exclude from the request.
        :param num_shards: Positive integer that specifies the number of shards to deploy in each specified zone. If you set this value to 1 and "clusterType" : "SHARDED", MongoDB Cloud deploys a single-shard sharded cluster. Don't create a sharded cluster with a single shard for production environments. Single-shard sharded clusters don't provide the same benefits as multi-shard configurations.
        :param zone_name: Human-readable label that identifies the zone in a Global Cluster. Provide this value only if "clusterType" : "GEOSHARDED".

        :schema: advancedReplicationSpec
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34eb2a5895572b181e47e3e53788b1ded80f942ba8716a0cf8e81b00fe216552)
            check_type(argname="argument advanced_region_configs", value=advanced_region_configs, expected_type=type_hints["advanced_region_configs"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument num_shards", value=num_shards, expected_type=type_hints["num_shards"])
            check_type(argname="argument zone_name", value=zone_name, expected_type=type_hints["zone_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_region_configs is not None:
            self._values["advanced_region_configs"] = advanced_region_configs
        if id is not None:
            self._values["id"] = id
        if num_shards is not None:
            self._values["num_shards"] = num_shards
        if zone_name is not None:
            self._values["zone_name"] = zone_name

    @builtins.property
    def advanced_region_configs(
        self,
    ) -> typing.Optional[typing.List[AdvancedRegionConfig]]:
        '''Hardware specifications for nodes set for a given region.

        Each regionConfigs object describes the region's priority in elections and the number and type of MongoDB nodes that MongoDB Cloud deploys to the region. Each regionConfigs object must have either an analyticsSpecs object, electableSpecs object, or readOnlySpecs object. Tenant clusters only require electableSpecs. Dedicated clusters can specify any of these specifications, but must have at least one electableSpecs object within a replicationSpec. Every hardware specification must use the same instanceSize.

        Example:

        If you set "replicationSpecs[n].regionConfigs[m].analyticsSpecs.instanceSize" : "M30", set "replicationSpecs[n].regionConfigs[m].electableSpecs.instanceSize" : "M30"if you have electable nodes and"replicationSpecs[n].regionConfigs[m].readOnlySpecs.instanceSize" : "M30" if you have read-only nodes.",

        :schema: advancedReplicationSpec#AdvancedRegionConfigs
        '''
        result = self._values.get("advanced_region_configs")
        return typing.cast(typing.Optional[typing.List[AdvancedRegionConfig]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Unique 24-hexadecimal digit string that identifies the replication object for a zone in a Multi-Cloud Cluster.

        If you include existing zones in the request, you must specify this parameter. If you add a new zone to an existing Multi-Cloud Cluster, you may specify this parameter. The request deletes any existing zones in the Multi-Cloud Cluster that you exclude from the request.

        :schema: advancedReplicationSpec#ID
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_shards(self) -> typing.Optional[jsii.Number]:
        '''Positive integer that specifies the number of shards to deploy in each specified zone.

        If you set this value to 1 and "clusterType" : "SHARDED", MongoDB Cloud deploys a single-shard sharded cluster. Don't create a sharded cluster with a single shard for production environments. Single-shard sharded clusters don't provide the same benefits as multi-shard configurations.

        :schema: advancedReplicationSpec#NumShards
        '''
        result = self._values.get("num_shards")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def zone_name(self) -> typing.Optional[builtins.str]:
        '''Human-readable label that identifies the zone in a Global Cluster.

        Provide this value only if "clusterType" : "GEOSHARDED".

        :schema: advancedReplicationSpec#ZoneName
        '''
        result = self._values.get("zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedReplicationSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnCluster(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@mongodbatlas-awscdk/cluster.CfnCluster",
):
    '''A CloudFormation ``MongoDB::Atlas::Cluster``.

    :cloudformationResource: MongoDB::Atlas::Cluster
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        project_id: builtins.str,
        advanced_settings: typing.Optional[typing.Union["ProcessArgs", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_enabled: typing.Optional[builtins.bool] = None,
        bi_connector: typing.Optional[typing.Union["CfnClusterPropsBiConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        connection_strings: typing.Optional[typing.Union["ConnectionStrings", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        encryption_at_rest_provider: typing.Optional["CfnClusterPropsEncryptionAtRestProvider"] = None,
        labels: typing.Optional[typing.Sequence[typing.Union["CfnClusterPropsLabels", typing.Dict[builtins.str, typing.Any]]]] = None,
        mongo_db_major_version: typing.Optional[builtins.str] = None,
        paused: typing.Optional[builtins.bool] = None,
        pit_enabled: typing.Optional[builtins.bool] = None,
        profile: typing.Optional[builtins.str] = None,
        replication_specs: typing.Optional[typing.Sequence[typing.Union[AdvancedReplicationSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
        root_cert_type: typing.Optional[builtins.str] = None,
        termination_protection_enabled: typing.Optional[builtins.bool] = None,
        version_release_system: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``MongoDB::Atlas::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Human-readable label that identifies the advanced cluster.
        :param project_id: Unique identifier of the project the cluster belongs to.
        :param advanced_settings: 
        :param backup_enabled: Flag that indicates whether the cluster can perform backups. If set to true, the cluster can perform backups. You must set this value to true for NVMe clusters. Backup uses Cloud Backups for dedicated clusters and Shared Cluster Backups for tenant clusters. If set to false, the cluster doesn't use backups.
        :param bi_connector: Settings needed to configure the MongoDB Connector for Business Intelligence for this cluster.
        :param cluster_type: Configuration of nodes that comprise the cluster.
        :param connection_strings: Set of connection strings that your applications use to connect to this cluster. Use the parameters in this object to connect your applications to this cluster. See the MongoDB `Connection String URI Format <https://docs.mongodb.com/manual/reference/connection-string/>`_ reference for further details.
        :param disk_size_gb: Storage capacity that the host's root volume possesses expressed in gigabytes. Increase this number to add capacity. MongoDB Cloud requires this parameter if you set replicationSpecs. If you specify a disk size below the minimum (10 GB), this parameter defaults to the minimum disk size value. Storage charge calculations depend on whether you choose the default value or a custom value. The maximum value for disk storage cannot exceed 50 times the maximum RAM for the selected cluster. If you require more storage space, consider upgrading your cluster to a higher tier.
        :param encryption_at_rest_provider: Cloud service provider that manages your customer keys to provide an additional layer of encryption at rest for the cluster. To enable customer key management for encryption at rest, the cluster replicationSpecs[n].regionConfigs[m].{type}Specs.instanceSize setting must be M10 or higher and "backupEnabled" : false or omitted entirely.
        :param labels: Collection of key-value pairs between 1 to 255 characters in length that tag and categorize the cluster. The MongoDB Cloud console doesn't display your labels.
        :param mongo_db_major_version: Major MongoDB version of the cluster. MongoDB Cloud deploys the cluster with the latest stable release of the specified version.
        :param paused: Flag that indicates whether the cluster is paused or not.
        :param pit_enabled: Flag that indicates whether the cluster uses continuous cloud backups.
        :param profile: Profile used to provide credentials information, (a secret with the cfn/atlas/profile/{Profile}, is required), if not provided default is used.
        :param replication_specs: List of settings that configure your cluster regions. For Global Clusters, each object in the array represents a zone where your clusters nodes deploy. For non-Global replica sets and sharded clusters, this array has one object representing where your clusters nodes deploy.
        :param root_cert_type: Root Certificate Authority that MongoDB Cloud cluster uses. MongoDB Cloud supports Internet Security Research Group.
        :param termination_protection_enabled: Flag that indicates whether termination protection is enabled on the cluster. If set to true, MongoDB Cloud won't delete the cluster. If set to false, MongoDB Cloud will delete the cluster.
        :param version_release_system: Method by which the cluster maintains the MongoDB versions. If value is CONTINUOUS, you must not specify mongoDBMajorVersion
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dece8b180a8c79f207a5761dbeaf5c83c07a6098094cc48630e0dadd17f98696)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            name=name,
            project_id=project_id,
            advanced_settings=advanced_settings,
            backup_enabled=backup_enabled,
            bi_connector=bi_connector,
            cluster_type=cluster_type,
            connection_strings=connection_strings,
            disk_size_gb=disk_size_gb,
            encryption_at_rest_provider=encryption_at_rest_provider,
            labels=labels,
            mongo_db_major_version=mongo_db_major_version,
            paused=paused,
            pit_enabled=pit_enabled,
            profile=profile,
            replication_specs=replication_specs,
            root_cert_type=root_cert_type,
            termination_protection_enabled=termination_protection_enabled,
            version_release_system=version_release_system,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedDate")
    def attr_created_date(self) -> builtins.str:
        '''Attribute ``MongoDB::Atlas::Cluster.CreatedDate``.'''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedDate"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``MongoDB::Atlas::Cluster.Id``.'''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrMongoDBVersion")
    def attr_mongo_db_version(self) -> builtins.str:
        '''Attribute ``MongoDB::Atlas::Cluster.MongoDBVersion``.'''
        return typing.cast(builtins.str, jsii.get(self, "attrMongoDBVersion"))

    @builtins.property
    @jsii.member(jsii_name="attrStateName")
    def attr_state_name(self) -> builtins.str:
        '''Attribute ``MongoDB::Atlas::Cluster.StateName``.'''
        return typing.cast(builtins.str, jsii.get(self, "attrStateName"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnClusterProps":
        '''Resource props.'''
        return typing.cast("CfnClusterProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "project_id": "projectId",
        "advanced_settings": "advancedSettings",
        "backup_enabled": "backupEnabled",
        "bi_connector": "biConnector",
        "cluster_type": "clusterType",
        "connection_strings": "connectionStrings",
        "disk_size_gb": "diskSizeGb",
        "encryption_at_rest_provider": "encryptionAtRestProvider",
        "labels": "labels",
        "mongo_db_major_version": "mongoDbMajorVersion",
        "paused": "paused",
        "pit_enabled": "pitEnabled",
        "profile": "profile",
        "replication_specs": "replicationSpecs",
        "root_cert_type": "rootCertType",
        "termination_protection_enabled": "terminationProtectionEnabled",
        "version_release_system": "versionReleaseSystem",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        project_id: builtins.str,
        advanced_settings: typing.Optional[typing.Union["ProcessArgs", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_enabled: typing.Optional[builtins.bool] = None,
        bi_connector: typing.Optional[typing.Union["CfnClusterPropsBiConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_type: typing.Optional[builtins.str] = None,
        connection_strings: typing.Optional[typing.Union["ConnectionStrings", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        encryption_at_rest_provider: typing.Optional["CfnClusterPropsEncryptionAtRestProvider"] = None,
        labels: typing.Optional[typing.Sequence[typing.Union["CfnClusterPropsLabels", typing.Dict[builtins.str, typing.Any]]]] = None,
        mongo_db_major_version: typing.Optional[builtins.str] = None,
        paused: typing.Optional[builtins.bool] = None,
        pit_enabled: typing.Optional[builtins.bool] = None,
        profile: typing.Optional[builtins.str] = None,
        replication_specs: typing.Optional[typing.Sequence[typing.Union[AdvancedReplicationSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
        root_cert_type: typing.Optional[builtins.str] = None,
        termination_protection_enabled: typing.Optional[builtins.bool] = None,
        version_release_system: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The cluster resource provides access to your cluster configurations.

        The resource lets you create, edit and delete clusters. The resource requires your Project ID.

        :param name: Human-readable label that identifies the advanced cluster.
        :param project_id: Unique identifier of the project the cluster belongs to.
        :param advanced_settings: 
        :param backup_enabled: Flag that indicates whether the cluster can perform backups. If set to true, the cluster can perform backups. You must set this value to true for NVMe clusters. Backup uses Cloud Backups for dedicated clusters and Shared Cluster Backups for tenant clusters. If set to false, the cluster doesn't use backups.
        :param bi_connector: Settings needed to configure the MongoDB Connector for Business Intelligence for this cluster.
        :param cluster_type: Configuration of nodes that comprise the cluster.
        :param connection_strings: Set of connection strings that your applications use to connect to this cluster. Use the parameters in this object to connect your applications to this cluster. See the MongoDB `Connection String URI Format <https://docs.mongodb.com/manual/reference/connection-string/>`_ reference for further details.
        :param disk_size_gb: Storage capacity that the host's root volume possesses expressed in gigabytes. Increase this number to add capacity. MongoDB Cloud requires this parameter if you set replicationSpecs. If you specify a disk size below the minimum (10 GB), this parameter defaults to the minimum disk size value. Storage charge calculations depend on whether you choose the default value or a custom value. The maximum value for disk storage cannot exceed 50 times the maximum RAM for the selected cluster. If you require more storage space, consider upgrading your cluster to a higher tier.
        :param encryption_at_rest_provider: Cloud service provider that manages your customer keys to provide an additional layer of encryption at rest for the cluster. To enable customer key management for encryption at rest, the cluster replicationSpecs[n].regionConfigs[m].{type}Specs.instanceSize setting must be M10 or higher and "backupEnabled" : false or omitted entirely.
        :param labels: Collection of key-value pairs between 1 to 255 characters in length that tag and categorize the cluster. The MongoDB Cloud console doesn't display your labels.
        :param mongo_db_major_version: Major MongoDB version of the cluster. MongoDB Cloud deploys the cluster with the latest stable release of the specified version.
        :param paused: Flag that indicates whether the cluster is paused or not.
        :param pit_enabled: Flag that indicates whether the cluster uses continuous cloud backups.
        :param profile: Profile used to provide credentials information, (a secret with the cfn/atlas/profile/{Profile}, is required), if not provided default is used.
        :param replication_specs: List of settings that configure your cluster regions. For Global Clusters, each object in the array represents a zone where your clusters nodes deploy. For non-Global replica sets and sharded clusters, this array has one object representing where your clusters nodes deploy.
        :param root_cert_type: Root Certificate Authority that MongoDB Cloud cluster uses. MongoDB Cloud supports Internet Security Research Group.
        :param termination_protection_enabled: Flag that indicates whether termination protection is enabled on the cluster. If set to true, MongoDB Cloud won't delete the cluster. If set to false, MongoDB Cloud will delete the cluster.
        :param version_release_system: Method by which the cluster maintains the MongoDB versions. If value is CONTINUOUS, you must not specify mongoDBMajorVersion

        :schema: CfnClusterProps
        '''
        if isinstance(advanced_settings, dict):
            advanced_settings = ProcessArgs(**advanced_settings)
        if isinstance(bi_connector, dict):
            bi_connector = CfnClusterPropsBiConnector(**bi_connector)
        if isinstance(connection_strings, dict):
            connection_strings = ConnectionStrings(**connection_strings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__084f7228aa18b3cb835be8d0983ecf8a7ef30d75f393a10f8000e3abd6a3d51e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument advanced_settings", value=advanced_settings, expected_type=type_hints["advanced_settings"])
            check_type(argname="argument backup_enabled", value=backup_enabled, expected_type=type_hints["backup_enabled"])
            check_type(argname="argument bi_connector", value=bi_connector, expected_type=type_hints["bi_connector"])
            check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
            check_type(argname="argument connection_strings", value=connection_strings, expected_type=type_hints["connection_strings"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument encryption_at_rest_provider", value=encryption_at_rest_provider, expected_type=type_hints["encryption_at_rest_provider"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mongo_db_major_version", value=mongo_db_major_version, expected_type=type_hints["mongo_db_major_version"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument pit_enabled", value=pit_enabled, expected_type=type_hints["pit_enabled"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument replication_specs", value=replication_specs, expected_type=type_hints["replication_specs"])
            check_type(argname="argument root_cert_type", value=root_cert_type, expected_type=type_hints["root_cert_type"])
            check_type(argname="argument termination_protection_enabled", value=termination_protection_enabled, expected_type=type_hints["termination_protection_enabled"])
            check_type(argname="argument version_release_system", value=version_release_system, expected_type=type_hints["version_release_system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project_id": project_id,
        }
        if advanced_settings is not None:
            self._values["advanced_settings"] = advanced_settings
        if backup_enabled is not None:
            self._values["backup_enabled"] = backup_enabled
        if bi_connector is not None:
            self._values["bi_connector"] = bi_connector
        if cluster_type is not None:
            self._values["cluster_type"] = cluster_type
        if connection_strings is not None:
            self._values["connection_strings"] = connection_strings
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if encryption_at_rest_provider is not None:
            self._values["encryption_at_rest_provider"] = encryption_at_rest_provider
        if labels is not None:
            self._values["labels"] = labels
        if mongo_db_major_version is not None:
            self._values["mongo_db_major_version"] = mongo_db_major_version
        if paused is not None:
            self._values["paused"] = paused
        if pit_enabled is not None:
            self._values["pit_enabled"] = pit_enabled
        if profile is not None:
            self._values["profile"] = profile
        if replication_specs is not None:
            self._values["replication_specs"] = replication_specs
        if root_cert_type is not None:
            self._values["root_cert_type"] = root_cert_type
        if termination_protection_enabled is not None:
            self._values["termination_protection_enabled"] = termination_protection_enabled
        if version_release_system is not None:
            self._values["version_release_system"] = version_release_system

    @builtins.property
    def name(self) -> builtins.str:
        '''Human-readable label that identifies the advanced cluster.

        :schema: CfnClusterProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Unique identifier of the project the cluster belongs to.

        :schema: CfnClusterProps#ProjectId
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_settings(self) -> typing.Optional["ProcessArgs"]:
        '''
        :schema: CfnClusterProps#AdvancedSettings
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional["ProcessArgs"], result)

    @builtins.property
    def backup_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether the cluster can perform backups.

        If set to true, the cluster can perform backups. You must set this value to true for NVMe clusters. Backup uses Cloud Backups for dedicated clusters and Shared Cluster Backups for tenant clusters. If set to false, the cluster doesn't use backups.

        :schema: CfnClusterProps#BackupEnabled
        '''
        result = self._values.get("backup_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bi_connector(self) -> typing.Optional["CfnClusterPropsBiConnector"]:
        '''Settings needed to configure the MongoDB Connector for Business Intelligence for this cluster.

        :schema: CfnClusterProps#BiConnector
        '''
        result = self._values.get("bi_connector")
        return typing.cast(typing.Optional["CfnClusterPropsBiConnector"], result)

    @builtins.property
    def cluster_type(self) -> typing.Optional[builtins.str]:
        '''Configuration of nodes that comprise the cluster.

        :schema: CfnClusterProps#ClusterType
        '''
        result = self._values.get("cluster_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_strings(self) -> typing.Optional["ConnectionStrings"]:
        '''Set of connection strings that your applications use to connect to this cluster.

        Use the parameters in this object to connect your applications to this cluster. See the MongoDB `Connection String URI Format <https://docs.mongodb.com/manual/reference/connection-string/>`_ reference for further details.

        :schema: CfnClusterProps#ConnectionStrings
        '''
        result = self._values.get("connection_strings")
        return typing.cast(typing.Optional["ConnectionStrings"], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Storage capacity that the host's root volume possesses expressed in gigabytes.

        Increase this number to add capacity. MongoDB Cloud requires this parameter if you set replicationSpecs. If you specify a disk size below the minimum (10 GB), this parameter defaults to the minimum disk size value. Storage charge calculations depend on whether you choose the default value or a custom value. The maximum value for disk storage cannot exceed 50 times the maximum RAM for the selected cluster. If you require more storage space, consider upgrading your cluster to a higher tier.

        :schema: CfnClusterProps#DiskSizeGB
        '''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def encryption_at_rest_provider(
        self,
    ) -> typing.Optional["CfnClusterPropsEncryptionAtRestProvider"]:
        '''Cloud service provider that manages your customer keys to provide an additional layer of encryption at rest for the cluster.

        To enable customer key management for encryption at rest, the cluster replicationSpecs[n].regionConfigs[m].{type}Specs.instanceSize setting must be M10 or higher and "backupEnabled" : false or omitted entirely.

        :schema: CfnClusterProps#EncryptionAtRestProvider
        '''
        result = self._values.get("encryption_at_rest_provider")
        return typing.cast(typing.Optional["CfnClusterPropsEncryptionAtRestProvider"], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List["CfnClusterPropsLabels"]]:
        '''Collection of key-value pairs between 1 to 255 characters in length that tag and categorize the cluster.

        The MongoDB Cloud console doesn't display your labels.

        :schema: CfnClusterProps#Labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List["CfnClusterPropsLabels"]], result)

    @builtins.property
    def mongo_db_major_version(self) -> typing.Optional[builtins.str]:
        '''Major MongoDB version of the cluster.

        MongoDB Cloud deploys the cluster with the latest stable release of the specified version.

        :schema: CfnClusterProps#MongoDBMajorVersion
        '''
        result = self._values.get("mongo_db_major_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether the cluster is paused or not.

        :schema: CfnClusterProps#Paused
        '''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pit_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether the cluster uses continuous cloud backups.

        :schema: CfnClusterProps#PitEnabled
        '''
        result = self._values.get("pit_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''Profile used to provide credentials information, (a secret with the cfn/atlas/profile/{Profile}, is required), if not provided default is used.

        :schema: CfnClusterProps#Profile
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_specs(
        self,
    ) -> typing.Optional[typing.List[AdvancedReplicationSpec]]:
        '''List of settings that configure your cluster regions.

        For Global Clusters, each object in the array represents a zone where your clusters nodes deploy. For non-Global replica sets and sharded clusters, this array has one object representing where your clusters nodes deploy.

        :schema: CfnClusterProps#ReplicationSpecs
        '''
        result = self._values.get("replication_specs")
        return typing.cast(typing.Optional[typing.List[AdvancedReplicationSpec]], result)

    @builtins.property
    def root_cert_type(self) -> typing.Optional[builtins.str]:
        '''Root Certificate Authority that MongoDB Cloud cluster uses.

        MongoDB Cloud supports Internet Security Research Group.

        :schema: CfnClusterProps#RootCertType
        '''
        result = self._values.get("root_cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_protection_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether termination protection is enabled on the cluster.

        If set to true, MongoDB Cloud won't delete the cluster. If set to false, MongoDB Cloud will delete the cluster.

        :schema: CfnClusterProps#TerminationProtectionEnabled
        '''
        result = self._values.get("termination_protection_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version_release_system(self) -> typing.Optional[builtins.str]:
        '''Method by which the cluster maintains the MongoDB versions.

        If value is CONTINUOUS, you must not specify mongoDBMajorVersion

        :schema: CfnClusterProps#VersionReleaseSystem
        '''
        result = self._values.get("version_release_system")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.CfnClusterPropsBiConnector",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "read_preference": "readPreference"},
)
class CfnClusterPropsBiConnector:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        read_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Settings needed to configure the MongoDB Connector for Business Intelligence for this cluster.

        :param enabled: Flag that indicates whether MongoDB Connector for Business Intelligence is enabled on the specified cluster.
        :param read_preference: Data source node designated for the MongoDB Connector for Business Intelligence on MongoDB Cloud. The MongoDB Connector for Business Intelligence on MongoDB Cloud reads data from the primary, secondary, or analytics node based on your read preferences. Defaults to ANALYTICS node, or SECONDARY if there are no ANALYTICS nodes. Default: ANALYTICS node, or SECONDARY if there are no ANALYTICS nodes.

        :schema: CfnClusterPropsBiConnector
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c88cf126367ac663b9678d0b8b9832ee6314da98bc4e90e44c7c108243ea24d2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument read_preference", value=read_preference, expected_type=type_hints["read_preference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if read_preference is not None:
            self._values["read_preference"] = read_preference

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether MongoDB Connector for Business Intelligence is enabled on the specified cluster.

        :schema: CfnClusterPropsBiConnector#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_preference(self) -> typing.Optional[builtins.str]:
        '''Data source node designated for the MongoDB Connector for Business Intelligence on MongoDB Cloud.

        The MongoDB Connector for Business Intelligence on MongoDB Cloud reads data from the primary, secondary, or analytics node based on your read preferences. Defaults to ANALYTICS node, or SECONDARY if there are no ANALYTICS nodes.

        :default: ANALYTICS node, or SECONDARY if there are no ANALYTICS nodes.

        :schema: CfnClusterPropsBiConnector#ReadPreference
        '''
        result = self._values.get("read_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterPropsBiConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@mongodbatlas-awscdk/cluster.CfnClusterPropsEncryptionAtRestProvider"
)
class CfnClusterPropsEncryptionAtRestProvider(enum.Enum):
    '''Cloud service provider that manages your customer keys to provide an additional layer of encryption at rest for the cluster.

    To enable customer key management for encryption at rest, the cluster replicationSpecs[n].regionConfigs[m].{type}Specs.instanceSize setting must be M10 or higher and "backupEnabled" : false or omitted entirely.

    :schema: CfnClusterPropsEncryptionAtRestProvider
    '''

    AWS = "AWS"
    '''AWS.'''
    GCP = "GCP"
    '''GCP.'''
    AZURE = "AZURE"
    '''AZURE.'''
    NONE = "NONE"
    '''NONE.'''


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.CfnClusterPropsLabels",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class CfnClusterPropsLabels:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: 
        :param value: 

        :schema: CfnClusterPropsLabels
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94159bf88374ea41fb31442b2669fa2a10e54c0e6a504e59446a6bbbc600cd2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsLabels#Key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsLabels#Value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterPropsLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.Compute",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "max_instance_size": "maxInstanceSize",
        "min_instance_size": "minInstanceSize",
        "scale_down_enabled": "scaleDownEnabled",
    },
)
class Compute:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        max_instance_size: typing.Optional[builtins.str] = None,
        min_instance_size: typing.Optional[builtins.str] = None,
        scale_down_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Automatic Compute Scaling.

        :param enabled: Flag that indicates whether someone enabled instance size auto-scaling. Set to true to enable instance size auto-scaling. If enabled, you must specify a value for replicationSpecs[n].regionConfigs[m].autoScaling.compute.maxInstanceSize. Set to false to disable instance size automatic scaling.
        :param max_instance_size: Maximum instance size to which your cluster can automatically scale. MongoDB Cloud requires this parameter if "replicationSpecs[n].regionConfigs[m].autoScaling.compute.enabled" : true.
        :param min_instance_size: Minimum instance size to which your cluster can automatically scale. MongoDB Cloud requires this parameter if "replicationSpecs[n].regionConfigs[m].autoScaling.compute.enabled" : true.
        :param scale_down_enabled: Flag that indicates whether the instance size may scale down. MongoDB Cloud requires this parameter if "replicationSpecs[n].regionConfigs[m].autoScaling.compute.enabled" : true. If you enable this option, specify a value for replicationSpecs[n].regionConfigs[m].autoScaling.compute.minInstanceSize.

        :schema: compute
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a053c24b8d45162498f079b859694d6deb520f6092c9fbdf6648c56e638609)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument max_instance_size", value=max_instance_size, expected_type=type_hints["max_instance_size"])
            check_type(argname="argument min_instance_size", value=min_instance_size, expected_type=type_hints["min_instance_size"])
            check_type(argname="argument scale_down_enabled", value=scale_down_enabled, expected_type=type_hints["scale_down_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if max_instance_size is not None:
            self._values["max_instance_size"] = max_instance_size
        if min_instance_size is not None:
            self._values["min_instance_size"] = min_instance_size
        if scale_down_enabled is not None:
            self._values["scale_down_enabled"] = scale_down_enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether someone enabled instance size auto-scaling.

        Set to true to enable instance size auto-scaling. If enabled, you must specify a value for replicationSpecs[n].regionConfigs[m].autoScaling.compute.maxInstanceSize.
        Set to false to disable instance size automatic scaling.

        :schema: compute#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_instance_size(self) -> typing.Optional[builtins.str]:
        '''Maximum instance size to which your cluster can automatically scale.

        MongoDB Cloud requires this parameter if "replicationSpecs[n].regionConfigs[m].autoScaling.compute.enabled" : true.

        :schema: compute#MaxInstanceSize
        '''
        result = self._values.get("max_instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def min_instance_size(self) -> typing.Optional[builtins.str]:
        '''Minimum instance size to which your cluster can automatically scale.

        MongoDB Cloud requires this parameter if "replicationSpecs[n].regionConfigs[m].autoScaling.compute.enabled" : true.

        :schema: compute#MinInstanceSize
        '''
        result = self._values.get("min_instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scale_down_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether the instance size may scale down.

        MongoDB Cloud requires this parameter if "replicationSpecs[n].regionConfigs[m].autoScaling.compute.enabled" : true. If you enable this option, specify a value for replicationSpecs[n].regionConfigs[m].autoScaling.compute.minInstanceSize.

        :schema: compute#ScaleDownEnabled
        '''
        result = self._values.get("scale_down_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Compute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.ConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={
        "aws_private_link": "awsPrivateLink",
        "aws_private_link_srv": "awsPrivateLinkSrv",
        "private": "private",
        "private_endpoint": "privateEndpoint",
        "private_srv": "privateSrv",
        "standard": "standard",
        "standard_srv": "standardSrv",
    },
)
class ConnectionStrings:
    def __init__(
        self,
        *,
        aws_private_link: typing.Optional[builtins.str] = None,
        aws_private_link_srv: typing.Optional[builtins.str] = None,
        private: typing.Optional[builtins.str] = None,
        private_endpoint: typing.Optional[typing.Sequence[typing.Union["PrivateEndpoint", typing.Dict[builtins.str, typing.Any]]]] = None,
        private_srv: typing.Optional[builtins.str] = None,
        standard: typing.Optional[builtins.str] = None,
        standard_srv: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Collection of Uniform Resource Locators that point to the MongoDB database.

        :param aws_private_link: Private endpoint-aware connection strings that use AWS-hosted clusters with Amazon Web Services (AWS) PrivateLink. Each key identifies an Amazon Web Services (AWS) interface endpoint. Each value identifies the related mongodb:// connection string that you use to connect to MongoDB Cloud through the interface endpoint that the key names.
        :param aws_private_link_srv: Private endpoint-aware connection strings that use AWS-hosted clusters with Amazon Web Services (AWS) PrivateLink. Each key identifies an Amazon Web Services (AWS) interface endpoint. Each value identifies the related mongodb:// connection string that you use to connect to Atlas through the interface endpoint that the key names.
        :param private: Network peering connection strings for each interface Virtual Private Cloud (VPC) endpoint that you configured to connect to this cluster. This connection string uses the mongodb+srv:// protocol. The resource returns this parameter once someone creates a network peering connection to this cluster. This protocol tells the application to look up the host seed list in the Domain Name System (DNS). This list synchronizes with the nodes in a cluster. If the connection string uses this Uniform Resource Identifier (URI) format, you don't need to append the seed list or change the URI if the nodes change. Use this URI format if your driver supports it. If it doesn't, use connectionStrings.private. For Amazon Web Services (AWS) clusters, this resource returns this parameter only if you enable custom DNS.
        :param private_endpoint: List of private endpoint connection strings that you can use to connect to this cluster through a private endpoint. This parameter returns only if you deployed a private endpoint to all regions to which you deployed this clusters' nodes.
        :param private_srv: Network peering connection strings for each interface Virtual Private Cloud (VPC) endpoint that you configured to connect to this cluster. This connection string uses the mongodb+srv:// protocol. The resource returns this parameter when someone creates a network peering connection to this cluster. This protocol tells the application to look up the host seed list in the Domain Name System (DNS). This list synchronizes with the nodes in a cluster. If the connection string uses this Uniform Resource Identifier (URI) format, you don't need to append the seed list or change the Uniform Resource Identifier (URI) if the nodes change. Use this Uniform Resource Identifier (URI) format if your driver supports it. If it doesn't, use connectionStrings.private. For Amazon Web Services (AWS) clusters, this parameter returns only if you enable custom DNS.
        :param standard: Public connection string that you can use to connect to this cluster. This connection string uses the mongodb:// protocol.
        :param standard_srv: Public connection string that you can use to connect to this cluster. This connection string uses the mongodb+srv:// protocol.

        :schema: connectionStrings
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d04356e75cc428637d055746ced8d0285d85341e046b5a9d5c36f70d9284a8)
            check_type(argname="argument aws_private_link", value=aws_private_link, expected_type=type_hints["aws_private_link"])
            check_type(argname="argument aws_private_link_srv", value=aws_private_link_srv, expected_type=type_hints["aws_private_link_srv"])
            check_type(argname="argument private", value=private, expected_type=type_hints["private"])
            check_type(argname="argument private_endpoint", value=private_endpoint, expected_type=type_hints["private_endpoint"])
            check_type(argname="argument private_srv", value=private_srv, expected_type=type_hints["private_srv"])
            check_type(argname="argument standard", value=standard, expected_type=type_hints["standard"])
            check_type(argname="argument standard_srv", value=standard_srv, expected_type=type_hints["standard_srv"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_private_link is not None:
            self._values["aws_private_link"] = aws_private_link
        if aws_private_link_srv is not None:
            self._values["aws_private_link_srv"] = aws_private_link_srv
        if private is not None:
            self._values["private"] = private
        if private_endpoint is not None:
            self._values["private_endpoint"] = private_endpoint
        if private_srv is not None:
            self._values["private_srv"] = private_srv
        if standard is not None:
            self._values["standard"] = standard
        if standard_srv is not None:
            self._values["standard_srv"] = standard_srv

    @builtins.property
    def aws_private_link(self) -> typing.Optional[builtins.str]:
        '''Private endpoint-aware connection strings that use AWS-hosted clusters with Amazon Web Services (AWS) PrivateLink.

        Each key identifies an Amazon Web Services (AWS) interface endpoint. Each value identifies the related mongodb:// connection string that you use to connect to MongoDB Cloud through the interface endpoint that the key names.

        :schema: connectionStrings#AwsPrivateLink
        '''
        result = self._values.get("aws_private_link")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def aws_private_link_srv(self) -> typing.Optional[builtins.str]:
        '''Private endpoint-aware connection strings that use AWS-hosted clusters with Amazon Web Services (AWS) PrivateLink.

        Each key identifies an Amazon Web Services (AWS) interface endpoint. Each value identifies the related mongodb:// connection string that you use to connect to Atlas through the interface endpoint that the key names.

        :schema: connectionStrings#AwsPrivateLinkSrv
        '''
        result = self._values.get("aws_private_link_srv")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private(self) -> typing.Optional[builtins.str]:
        '''Network peering connection strings for each interface Virtual Private Cloud (VPC) endpoint that you configured to connect to this cluster.

        This connection string uses the mongodb+srv:// protocol. The resource returns this parameter once someone creates a network peering connection to this cluster. This protocol tells the application to look up the host seed list in the Domain Name System (DNS). This list synchronizes with the nodes in a cluster. If the connection string uses this Uniform Resource Identifier (URI) format, you don't need to append the seed list or change the URI if the nodes change. Use this URI format if your driver supports it. If it doesn't, use connectionStrings.private. For Amazon Web Services (AWS) clusters, this resource returns this parameter only if you enable custom DNS.

        :schema: connectionStrings#Private
        '''
        result = self._values.get("private")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_endpoint(self) -> typing.Optional[typing.List["PrivateEndpoint"]]:
        '''List of private endpoint connection strings that you can use to connect to this cluster through a private endpoint.

        This parameter returns only if you deployed a private endpoint to all regions to which you deployed this clusters' nodes.

        :schema: connectionStrings#PrivateEndpoint
        '''
        result = self._values.get("private_endpoint")
        return typing.cast(typing.Optional[typing.List["PrivateEndpoint"]], result)

    @builtins.property
    def private_srv(self) -> typing.Optional[builtins.str]:
        '''Network peering connection strings for each interface Virtual Private Cloud (VPC) endpoint that you configured to connect to this cluster.

        This connection string uses the mongodb+srv:// protocol. The resource returns this parameter when someone creates a network peering connection to this cluster. This protocol tells the application to look up the host seed list in the Domain Name System (DNS). This list synchronizes with the nodes in a cluster. If the connection string uses this Uniform Resource Identifier (URI) format, you don't need to append the seed list or change the Uniform Resource Identifier (URI) if the nodes change. Use this Uniform Resource Identifier (URI) format if your driver supports it. If it doesn't, use connectionStrings.private. For Amazon Web Services (AWS) clusters, this parameter returns only if you enable custom DNS.

        :schema: connectionStrings#PrivateSrv
        '''
        result = self._values.get("private_srv")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard(self) -> typing.Optional[builtins.str]:
        '''Public connection string that you can use to connect to this cluster.

        This connection string uses the mongodb:// protocol.

        :schema: connectionStrings#Standard
        '''
        result = self._values.get("standard")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def standard_srv(self) -> typing.Optional[builtins.str]:
        '''Public connection string that you can use to connect to this cluster.

        This connection string uses the mongodb+srv:// protocol.

        :schema: connectionStrings#StandardSrv
        '''
        result = self._values.get("standard_srv")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.DiskGb",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class DiskGb:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''Automatic cluster storage settings that apply to this cluster.

        :param enabled: Flag that indicates whether this cluster enables disk auto-scaling. The maximum memory allowed for the selected cluster tier and the oplog size can limit storage auto-scaling.

        :schema: diskGB
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc79927a171c19b4aa257843742e24c257efbff09ddee663b1f93f597b58987)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether this cluster enables disk auto-scaling.

        The maximum memory allowed for the selected cluster tier and the oplog size can limit storage auto-scaling.

        :schema: diskGB#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiskGb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.Endpoint",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_id": "endpointId",
        "provider_name": "providerName",
        "region": "region",
    },
)
class Endpoint:
    def __init__(
        self,
        *,
        endpoint_id: typing.Optional[builtins.str] = None,
        provider_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_id: Unique string that the cloud provider uses to identify the private endpoint.
        :param provider_name: Cloud provider in which MongoDB Cloud deploys the private endpoint.
        :param region: Region in which MongoDB Cloud deploys the private endpoint.

        :schema: endpoint
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3d6c3c0586597af0e8bcae390f0e587aa3eeabb439de9beb1d1ee2373acd11)
            check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if endpoint_id is not None:
            self._values["endpoint_id"] = endpoint_id
        if provider_name is not None:
            self._values["provider_name"] = provider_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def endpoint_id(self) -> typing.Optional[builtins.str]:
        '''Unique string that the cloud provider uses to identify the private endpoint.

        :schema: endpoint#EndpointID
        '''
        result = self._values.get("endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider_name(self) -> typing.Optional[builtins.str]:
        '''Cloud provider in which MongoDB Cloud deploys the private endpoint.

        :schema: endpoint#ProviderName
        '''
        result = self._values.get("provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region in which MongoDB Cloud deploys the private endpoint.

        :schema: endpoint#Region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Endpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.PrivateEndpoint",
    jsii_struct_bases=[],
    name_mapping={
        "connection_string": "connectionString",
        "endpoints": "endpoints",
        "srv_connection_string": "srvConnectionString",
        "type": "type",
    },
)
class PrivateEndpoint:
    def __init__(
        self,
        *,
        connection_string: typing.Optional[builtins.str] = None,
        endpoints: typing.Optional[typing.Sequence[typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]]]] = None,
        srv_connection_string: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''List of private endpoint connection strings that you can use to connect to this cluster through a private endpoint.

        This parameter returns only if you deployed a private endpoint to all regions to which you deployed this clusters' nodes.

        :param connection_string: Private endpoint-aware connection string that uses the mongodb:// protocol to connect to MongoDB Cloud through a private endpoint.
        :param endpoints: List that contains the private endpoints through which you connect to MongoDB Cloud when you use connectionStrings.privateEndpoint[n].connectionString or connectionStrings.privateEndpoint[n].srvConnectionString.
        :param srv_connection_string: Private endpoint-aware connection string that uses the mongodb+srv:// protocol to connect to MongoDB Cloud through a private endpoint. The mongodb+srv protocol tells the driver to look up the seed list of hosts in the Domain Name System (DNS). This list synchronizes with the nodes in a cluster. If the connection string uses this Uniform Resource Identifier (URI) format, you don't need to append the seed list or change the Uniform Resource Identifier (URI) if the nodes change. Use this Uniform Resource Identifier (URI) format if your application supports it. If it doesn't, use connectionStrings.privateEndpoint[n].connectionString.
        :param type: Enum: "MONGOD" "MONGOS" MongoDB process type to which your application connects. Use MONGOD for replica sets and MONGOS for sharded clusters.

        :schema: privateEndpoint
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14087db0e6f68df543886e9a37d6134936b16bc56ca69bc82941a209ebfe6b90)
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument endpoints", value=endpoints, expected_type=type_hints["endpoints"])
            check_type(argname="argument srv_connection_string", value=srv_connection_string, expected_type=type_hints["srv_connection_string"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if endpoints is not None:
            self._values["endpoints"] = endpoints
        if srv_connection_string is not None:
            self._values["srv_connection_string"] = srv_connection_string
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def connection_string(self) -> typing.Optional[builtins.str]:
        '''Private endpoint-aware connection string that uses the mongodb:// protocol to connect to MongoDB Cloud through a private endpoint.

        :schema: privateEndpoint#ConnectionString
        '''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoints(self) -> typing.Optional[typing.List[Endpoint]]:
        '''List that contains the private endpoints through which you connect to MongoDB Cloud when you use connectionStrings.privateEndpoint[n].connectionString or connectionStrings.privateEndpoint[n].srvConnectionString.

        :schema: privateEndpoint#Endpoints
        '''
        result = self._values.get("endpoints")
        return typing.cast(typing.Optional[typing.List[Endpoint]], result)

    @builtins.property
    def srv_connection_string(self) -> typing.Optional[builtins.str]:
        '''Private endpoint-aware connection string that uses the mongodb+srv:// protocol to connect to MongoDB Cloud through a private endpoint.

        The mongodb+srv protocol tells the driver to look up the seed list of hosts in the Domain Name System (DNS). This list synchronizes with the nodes in a cluster. If the connection string uses this Uniform Resource Identifier (URI) format, you don't need to append the seed list or change the Uniform Resource Identifier (URI) if the nodes change. Use this Uniform Resource Identifier (URI) format if your application supports it. If it doesn't, use connectionStrings.privateEndpoint[n].connectionString.

        :schema: privateEndpoint#SRVConnectionString
        '''
        result = self._values.get("srv_connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Enum: "MONGOD" "MONGOS" MongoDB process type to which your application connects.

        Use MONGOD for replica sets and MONGOS for sharded clusters.

        :schema: privateEndpoint#Type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivateEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.ProcessArgs",
    jsii_struct_bases=[],
    name_mapping={
        "default_read_concern": "defaultReadConcern",
        "default_write_concern": "defaultWriteConcern",
        "fail_index_key_too_long": "failIndexKeyTooLong",
        "javascript_enabled": "javascriptEnabled",
        "minimum_enabled_tls_protocol": "minimumEnabledTlsProtocol",
        "no_table_scan": "noTableScan",
        "oplog_size_mb": "oplogSizeMb",
        "sample_refresh_interval_bi_connector": "sampleRefreshIntervalBiConnector",
        "sample_size_bi_connector": "sampleSizeBiConnector",
    },
)
class ProcessArgs:
    def __init__(
        self,
        *,
        default_read_concern: typing.Optional[builtins.str] = None,
        default_write_concern: typing.Optional[builtins.str] = None,
        fail_index_key_too_long: typing.Optional[builtins.bool] = None,
        javascript_enabled: typing.Optional[builtins.bool] = None,
        minimum_enabled_tls_protocol: typing.Optional[builtins.str] = None,
        no_table_scan: typing.Optional[builtins.bool] = None,
        oplog_size_mb: typing.Optional[jsii.Number] = None,
        sample_refresh_interval_bi_connector: typing.Optional[jsii.Number] = None,
        sample_size_bi_connector: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Advanced configuration details to add for one cluster in the specified project.

        :param default_read_concern: Default level of acknowledgment requested from MongoDB for read operations set for this cluster.
        :param default_write_concern: Default level of acknowledgment requested from MongoDB for write operations set for this cluster.
        :param fail_index_key_too_long: Flag that indicates whether you can insert or update documents where all indexed entries don't exceed 1024 bytes. If you set this to false, mongod writes documents that exceed this limit but doesn't index them.
        :param javascript_enabled: Flag that indicates whether the cluster allows execution of operations that perform server-side executions of JavaScript.
        :param minimum_enabled_tls_protocol: Minimum Transport Layer Security (TLS) version that the cluster accepts for incoming connections. Clusters using TLS 1.0 or 1.1 should consider setting TLS 1.2 as the minimum TLS protocol version.
        :param no_table_scan: Flag that indicates whether the cluster disables executing any query that requires a collection scan to return results.
        :param oplog_size_mb: Storage limit of cluster's oplog expressed in megabytes. A value of null indicates that the cluster uses the default oplog size that MongoDB Cloud calculates.
        :param sample_refresh_interval_bi_connector: Number of documents per database to sample when gathering schema information.
        :param sample_size_bi_connector: Interval in seconds at which the mongosqld process re-samples data to create its relational schema.

        :schema: processArgs
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__232fbcc73e57592ccd057ca2cf4e8ed844aaaf96e358ee99bb7d5918158bd0e4)
            check_type(argname="argument default_read_concern", value=default_read_concern, expected_type=type_hints["default_read_concern"])
            check_type(argname="argument default_write_concern", value=default_write_concern, expected_type=type_hints["default_write_concern"])
            check_type(argname="argument fail_index_key_too_long", value=fail_index_key_too_long, expected_type=type_hints["fail_index_key_too_long"])
            check_type(argname="argument javascript_enabled", value=javascript_enabled, expected_type=type_hints["javascript_enabled"])
            check_type(argname="argument minimum_enabled_tls_protocol", value=minimum_enabled_tls_protocol, expected_type=type_hints["minimum_enabled_tls_protocol"])
            check_type(argname="argument no_table_scan", value=no_table_scan, expected_type=type_hints["no_table_scan"])
            check_type(argname="argument oplog_size_mb", value=oplog_size_mb, expected_type=type_hints["oplog_size_mb"])
            check_type(argname="argument sample_refresh_interval_bi_connector", value=sample_refresh_interval_bi_connector, expected_type=type_hints["sample_refresh_interval_bi_connector"])
            check_type(argname="argument sample_size_bi_connector", value=sample_size_bi_connector, expected_type=type_hints["sample_size_bi_connector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_read_concern is not None:
            self._values["default_read_concern"] = default_read_concern
        if default_write_concern is not None:
            self._values["default_write_concern"] = default_write_concern
        if fail_index_key_too_long is not None:
            self._values["fail_index_key_too_long"] = fail_index_key_too_long
        if javascript_enabled is not None:
            self._values["javascript_enabled"] = javascript_enabled
        if minimum_enabled_tls_protocol is not None:
            self._values["minimum_enabled_tls_protocol"] = minimum_enabled_tls_protocol
        if no_table_scan is not None:
            self._values["no_table_scan"] = no_table_scan
        if oplog_size_mb is not None:
            self._values["oplog_size_mb"] = oplog_size_mb
        if sample_refresh_interval_bi_connector is not None:
            self._values["sample_refresh_interval_bi_connector"] = sample_refresh_interval_bi_connector
        if sample_size_bi_connector is not None:
            self._values["sample_size_bi_connector"] = sample_size_bi_connector

    @builtins.property
    def default_read_concern(self) -> typing.Optional[builtins.str]:
        '''Default level of acknowledgment requested from MongoDB for read operations set for this cluster.

        :schema: processArgs#DefaultReadConcern
        '''
        result = self._values.get("default_read_concern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_write_concern(self) -> typing.Optional[builtins.str]:
        '''Default level of acknowledgment requested from MongoDB for write operations set for this cluster.

        :schema: processArgs#DefaultWriteConcern
        '''
        result = self._values.get("default_write_concern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_index_key_too_long(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether you can insert or update documents where all indexed entries don't exceed 1024 bytes.

        If you set this to false, mongod writes documents that exceed this limit but doesn't index them.

        :schema: processArgs#FailIndexKeyTooLong
        '''
        result = self._values.get("fail_index_key_too_long")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def javascript_enabled(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether the cluster allows execution of operations that perform server-side executions of JavaScript.

        :schema: processArgs#JavascriptEnabled
        '''
        result = self._values.get("javascript_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimum_enabled_tls_protocol(self) -> typing.Optional[builtins.str]:
        '''Minimum Transport Layer Security (TLS) version that the cluster accepts for incoming connections.

        Clusters using TLS 1.0 or 1.1 should consider setting TLS 1.2 as the minimum TLS protocol version.

        :schema: processArgs#MinimumEnabledTLSProtocol
        '''
        result = self._values.get("minimum_enabled_tls_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_table_scan(self) -> typing.Optional[builtins.bool]:
        '''Flag that indicates whether the cluster disables executing any query that requires a collection scan to return results.

        :schema: processArgs#NoTableScan
        '''
        result = self._values.get("no_table_scan")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def oplog_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Storage limit of cluster's oplog expressed in megabytes.

        A value of null indicates that the cluster uses the default oplog size that MongoDB Cloud calculates.

        :schema: processArgs#OplogSizeMB
        '''
        result = self._values.get("oplog_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_refresh_interval_bi_connector(self) -> typing.Optional[jsii.Number]:
        '''Number of documents per database to sample when gathering schema information.

        :schema: processArgs#SampleRefreshIntervalBIConnector
        '''
        result = self._values.get("sample_refresh_interval_bi_connector")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_size_bi_connector(self) -> typing.Optional[jsii.Number]:
        '''Interval in seconds at which the mongosqld process re-samples data to create its relational schema.

        :schema: processArgs#SampleSizeBIConnector
        '''
        result = self._values.get("sample_size_bi_connector")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcessArgs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@mongodbatlas-awscdk/cluster.Specs",
    jsii_struct_bases=[],
    name_mapping={
        "disk_iops": "diskIops",
        "ebs_volume_type": "ebsVolumeType",
        "instance_size": "instanceSize",
        "node_count": "nodeCount",
    },
)
class Specs:
    def __init__(
        self,
        *,
        disk_iops: typing.Optional[builtins.str] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        instance_size: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_iops: Target throughput desired for storage attached to your AWS-provisioned cluster. Only change this parameter if you:. set "replicationSpecs[n].regionConfigs[m].providerName" : "AWS". set "replicationSpecs[n].regionConfigs[m].electableSpecs.instanceSize" : "M30" or greater not including Mxx_NVME tiers. The maximum input/output operations per second (IOPS) depend on the selected .instanceSize and .diskSizeGB. This parameter defaults to the cluster tier's standard IOPS value. Changing this value impacts cluster cost. MongoDB Cloud enforces minimum ratios of storage capacity to system memory for given cluster tiers. This keeps cluster performance consistent with large datasets. Instance sizes M10 to M40 have a ratio of disk capacity to system memory of 60:1. Instance sizes greater than M40 have a ratio of 120:1.
        :param ebs_volume_type: Type of storage you want to attach to your AWS-provisioned cluster. STANDARD volume types can't exceed the default input/output operations per second (IOPS) rate for the selected volume size. PROVISIONED volume types must fall within the allowable IOPS range for the selected volume size."
        :param instance_size: Hardware specification for the instance sizes in this region. Each instance size has a default storage and memory capacity. The instance size you select applies to all the data-bearing hosts in your instance size. If you deploy a Global Cluster, you must choose a instance size of M30 or greater.
        :param node_count: Number of read-only nodes for MongoDB Cloud deploys to the region. Read-only nodes can never become the primary, but can enable local reads.

        :schema: specs
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__694443b4b954ff55627210ea03eefde90b658e531553a3406b6bae15153e18fe)
            check_type(argname="argument disk_iops", value=disk_iops, expected_type=type_hints["disk_iops"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument instance_size", value=instance_size, expected_type=type_hints["instance_size"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_iops is not None:
            self._values["disk_iops"] = disk_iops
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if instance_size is not None:
            self._values["instance_size"] = instance_size
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def disk_iops(self) -> typing.Optional[builtins.str]:
        '''Target throughput desired for storage attached to your AWS-provisioned cluster. Only change this parameter if you:.

        set "replicationSpecs[n].regionConfigs[m].providerName" : "AWS".
        set "replicationSpecs[n].regionConfigs[m].electableSpecs.instanceSize" : "M30" or greater not including Mxx_NVME tiers.
        The maximum input/output operations per second (IOPS) depend on the selected .instanceSize and .diskSizeGB. This parameter defaults to the cluster tier's standard IOPS value. Changing this value impacts cluster cost. MongoDB Cloud enforces minimum ratios of storage capacity to system memory for given cluster tiers. This keeps cluster performance consistent with large datasets.

        Instance sizes M10 to M40 have a ratio of disk capacity to system memory of 60:1.
        Instance sizes greater than M40 have a ratio of 120:1.

        :schema: specs#DiskIOPS
        '''
        result = self._values.get("disk_iops")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional[builtins.str]:
        '''Type of storage you want to attach to your AWS-provisioned cluster.

        STANDARD volume types can't exceed the default input/output operations per second (IOPS) rate for the selected volume size.

        PROVISIONED volume types must fall within the allowable IOPS range for the selected volume size."

        :schema: specs#EbsVolumeType
        '''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_size(self) -> typing.Optional[builtins.str]:
        '''Hardware specification for the instance sizes in this region.

        Each instance size has a default storage and memory capacity. The instance size you select applies to all the data-bearing hosts in your instance size. If you deploy a Global Cluster, you must choose a instance size of M30 or greater.

        :schema: specs#InstanceSize
        '''
        result = self._values.get("instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Number of read-only nodes for MongoDB Cloud deploys to the region.

        Read-only nodes can never become the primary, but can enable local reads.

        :schema: specs#NodeCount
        '''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Specs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AdvancedAutoScaling",
    "AdvancedRegionConfig",
    "AdvancedReplicationSpec",
    "CfnCluster",
    "CfnClusterProps",
    "CfnClusterPropsBiConnector",
    "CfnClusterPropsEncryptionAtRestProvider",
    "CfnClusterPropsLabels",
    "Compute",
    "ConnectionStrings",
    "DiskGb",
    "Endpoint",
    "PrivateEndpoint",
    "ProcessArgs",
    "Specs",
]

publication.publish()

def _typecheckingstub__d18b81adb1d348c704cd7ce6d97ea93341d53db8ac74a93c2304ebbe294ea3db(
    *,
    compute: typing.Optional[typing.Union[Compute, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_gb: typing.Optional[typing.Union[DiskGb, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598b4f40138e39a15924208c786865138be1508cd2c38bc001b1d497c28c0268(
    *,
    analytics_auto_scaling: typing.Optional[typing.Union[AdvancedAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    analytics_specs: typing.Optional[typing.Union[Specs, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling: typing.Optional[typing.Union[AdvancedAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    electable_specs: typing.Optional[typing.Union[Specs, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[jsii.Number] = None,
    read_only_specs: typing.Optional[typing.Union[Specs, typing.Dict[builtins.str, typing.Any]]] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34eb2a5895572b181e47e3e53788b1ded80f942ba8716a0cf8e81b00fe216552(
    *,
    advanced_region_configs: typing.Optional[typing.Sequence[typing.Union[AdvancedRegionConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    id: typing.Optional[builtins.str] = None,
    num_shards: typing.Optional[jsii.Number] = None,
    zone_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dece8b180a8c79f207a5761dbeaf5c83c07a6098094cc48630e0dadd17f98696(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    project_id: builtins.str,
    advanced_settings: typing.Optional[typing.Union[ProcessArgs, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_enabled: typing.Optional[builtins.bool] = None,
    bi_connector: typing.Optional[typing.Union[CfnClusterPropsBiConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    connection_strings: typing.Optional[typing.Union[ConnectionStrings, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    encryption_at_rest_provider: typing.Optional[CfnClusterPropsEncryptionAtRestProvider] = None,
    labels: typing.Optional[typing.Sequence[typing.Union[CfnClusterPropsLabels, typing.Dict[builtins.str, typing.Any]]]] = None,
    mongo_db_major_version: typing.Optional[builtins.str] = None,
    paused: typing.Optional[builtins.bool] = None,
    pit_enabled: typing.Optional[builtins.bool] = None,
    profile: typing.Optional[builtins.str] = None,
    replication_specs: typing.Optional[typing.Sequence[typing.Union[AdvancedReplicationSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
    root_cert_type: typing.Optional[builtins.str] = None,
    termination_protection_enabled: typing.Optional[builtins.bool] = None,
    version_release_system: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__084f7228aa18b3cb835be8d0983ecf8a7ef30d75f393a10f8000e3abd6a3d51e(
    *,
    name: builtins.str,
    project_id: builtins.str,
    advanced_settings: typing.Optional[typing.Union[ProcessArgs, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_enabled: typing.Optional[builtins.bool] = None,
    bi_connector: typing.Optional[typing.Union[CfnClusterPropsBiConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_type: typing.Optional[builtins.str] = None,
    connection_strings: typing.Optional[typing.Union[ConnectionStrings, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    encryption_at_rest_provider: typing.Optional[CfnClusterPropsEncryptionAtRestProvider] = None,
    labels: typing.Optional[typing.Sequence[typing.Union[CfnClusterPropsLabels, typing.Dict[builtins.str, typing.Any]]]] = None,
    mongo_db_major_version: typing.Optional[builtins.str] = None,
    paused: typing.Optional[builtins.bool] = None,
    pit_enabled: typing.Optional[builtins.bool] = None,
    profile: typing.Optional[builtins.str] = None,
    replication_specs: typing.Optional[typing.Sequence[typing.Union[AdvancedReplicationSpec, typing.Dict[builtins.str, typing.Any]]]] = None,
    root_cert_type: typing.Optional[builtins.str] = None,
    termination_protection_enabled: typing.Optional[builtins.bool] = None,
    version_release_system: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88cf126367ac663b9678d0b8b9832ee6314da98bc4e90e44c7c108243ea24d2(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    read_preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94159bf88374ea41fb31442b2669fa2a10e54c0e6a504e59446a6bbbc600cd2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a053c24b8d45162498f079b859694d6deb520f6092c9fbdf6648c56e638609(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    max_instance_size: typing.Optional[builtins.str] = None,
    min_instance_size: typing.Optional[builtins.str] = None,
    scale_down_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d04356e75cc428637d055746ced8d0285d85341e046b5a9d5c36f70d9284a8(
    *,
    aws_private_link: typing.Optional[builtins.str] = None,
    aws_private_link_srv: typing.Optional[builtins.str] = None,
    private: typing.Optional[builtins.str] = None,
    private_endpoint: typing.Optional[typing.Sequence[typing.Union[PrivateEndpoint, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_srv: typing.Optional[builtins.str] = None,
    standard: typing.Optional[builtins.str] = None,
    standard_srv: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc79927a171c19b4aa257843742e24c257efbff09ddee663b1f93f597b58987(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3d6c3c0586597af0e8bcae390f0e587aa3eeabb439de9beb1d1ee2373acd11(
    *,
    endpoint_id: typing.Optional[builtins.str] = None,
    provider_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14087db0e6f68df543886e9a37d6134936b16bc56ca69bc82941a209ebfe6b90(
    *,
    connection_string: typing.Optional[builtins.str] = None,
    endpoints: typing.Optional[typing.Sequence[typing.Union[Endpoint, typing.Dict[builtins.str, typing.Any]]]] = None,
    srv_connection_string: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__232fbcc73e57592ccd057ca2cf4e8ed844aaaf96e358ee99bb7d5918158bd0e4(
    *,
    default_read_concern: typing.Optional[builtins.str] = None,
    default_write_concern: typing.Optional[builtins.str] = None,
    fail_index_key_too_long: typing.Optional[builtins.bool] = None,
    javascript_enabled: typing.Optional[builtins.bool] = None,
    minimum_enabled_tls_protocol: typing.Optional[builtins.str] = None,
    no_table_scan: typing.Optional[builtins.bool] = None,
    oplog_size_mb: typing.Optional[jsii.Number] = None,
    sample_refresh_interval_bi_connector: typing.Optional[jsii.Number] = None,
    sample_size_bi_connector: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694443b4b954ff55627210ea03eefde90b658e531553a3406b6bae15153e18fe(
    *,
    disk_iops: typing.Optional[builtins.str] = None,
    ebs_volume_type: typing.Optional[builtins.str] = None,
    instance_size: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
