'''
# databricks-clusters-cluster

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Databricks::Clusters::Cluster` v1.1.0.

## Description

Manage a Databricks Cluster

## References

* [Documentation](https://github.com/aws-ia/cloudformation-databricks-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-databricks-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Databricks::Clusters::Cluster \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Databricks-Clusters-Cluster \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Databricks::Clusters::Cluster`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdatabricks-clusters-cluster+v1.1.0).
* Issues related to `Databricks::Clusters::Cluster` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-databricks-resource-providers).

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
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.Autoscale",
    jsii_struct_bases=[],
    name_mapping={"max_workers": "maxWorkers", "min_workers": "minWorkers"},
)
class Autoscale:
    def __init__(self, *, max_workers: jsii.Number, min_workers: jsii.Number) -> None:
        '''Range defining the min and max number of cluster workers.

        :param max_workers: The maximum number of workers to which the cluster can scale up when overloaded. max_workers must be strictly greater than min_workers.
        :param min_workers: The minimum number of workers to which the cluster can scale down when underutilized. It is also the initial number of workers the cluster will have after creation.

        :schema: Autoscale
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdda6b335054253b59f73353b7500526d79f5959ad84774a8f06d6cd82c62fbd)
            check_type(argname="argument max_workers", value=max_workers, expected_type=type_hints["max_workers"])
            check_type(argname="argument min_workers", value=min_workers, expected_type=type_hints["min_workers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "max_workers": max_workers,
            "min_workers": min_workers,
        }

    @builtins.property
    def max_workers(self) -> jsii.Number:
        '''The maximum number of workers to which the cluster can scale up when overloaded.

        max_workers must be strictly greater than min_workers.

        :schema: Autoscale#MaxWorkers
        '''
        result = self._values.get("max_workers")
        assert result is not None, "Required property 'max_workers' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def min_workers(self) -> jsii.Number:
        '''The minimum number of workers to which the cluster can scale down when underutilized.

        It is also the initial number of workers the cluster will have after creation.

        :schema: Autoscale#MinWorkers
        '''
        result = self._values.get("min_workers")
        assert result is not None, "Required property 'min_workers' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Autoscale(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.AwsAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "availability": "availability",
        "ebs_volume_count": "ebsVolumeCount",
        "ebs_volume_iops": "ebsVolumeIops",
        "ebs_volume_size": "ebsVolumeSize",
        "ebs_volume_throughput": "ebsVolumeThroughput",
        "ebs_volume_type": "ebsVolumeType",
        "first_on_demand": "firstOnDemand",
        "spot_bid_price_percent": "spotBidPricePercent",
        "zone_id": "zoneId",
    },
)
class AwsAttributes:
    def __init__(
        self,
        *,
        availability: typing.Optional["AwsAttributesAvailability"] = None,
        ebs_volume_count: typing.Optional[jsii.Number] = None,
        ebs_volume_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_size: typing.Optional[jsii.Number] = None,
        ebs_volume_throughput: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional["AwsAttributesEbsVolumeType"] = None,
        first_on_demand: typing.Optional[jsii.Number] = None,
        spot_bid_price_percent: typing.Optional[jsii.Number] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Attributes set during cluster creation related to Amazon Web Services.

        :param availability: Availability type used for all subsequent nodes past the first_on_demand ones. Note: If first_on_demand is zero, this availability type will be used for the entire cluster.
        :param ebs_volume_count: The number of volumes launched for each instance. You can choose up to 10 volumes. This feature is only enabled for supported node types. Legacy node types cannot specify custom EBS volumes. For node types with no instance store, at least one EBS volume needs to be specified; otherwise, cluster creation will fail. These EBS volumes will be mounted at /ebs0, /ebs1, and etc. Instance store volumes will be mounted at /local_disk0, /local_disk1, and etc. If EBS volumes are attached, Databricks will configure Spark to use only the EBS volumes for scratch storage because heterogeneously sized scratch devices can lead to inefficient disk utilization. If no EBS volumes are attached, Databricks will configure Spark to use instance store volumes. If EBS volumes are specified, then the Spark configuration spark.local.dir will be overridden.
        :param ebs_volume_iops: The number of IOPS per EBS gp3 volume. This value must be between 3000 and 16000. The value of IOPS and throughput is calculated based on AWS documentation to match the maximum performance of a gp2 volume with the same volume size. For more information, see the EBS volume limit calculator.
        :param ebs_volume_size: The size of each EBS volume (in GiB) launched for each instance. For general purpose SSD, this value must be within the range 100 - 4096. For throughput optimized HDD, this value must be within the range 500 - 4096. Custom EBS volumes cannot be specified for the legacy node types (memory-optimized and compute-optimized).
        :param ebs_volume_throughput: The throughput per EBS gp3 volume, in MiB per second. This value must be between 125 and 1000.
        :param ebs_volume_type: The type of EBS volumes that will be launched with this cluster.
        :param first_on_demand: The first first_on_demand nodes of the cluster will be placed on on-demand instances. If this value is greater than 0, the cluster driver node will be placed on an on-demand instance. If this value is greater than or equal to the current cluster size, all nodes will be placed on on-demand instances. If this value is less than the current cluster size, first_on_demand nodes will be placed on on-demand instances and the remainder will be placed on availability instances. This value does not affect cluster size and cannot be mutated over the lifetime of a cluster.
        :param spot_bid_price_percent: The max price for AWS spot instances, as a percentage of the corresponding instance type's on-demand price. For example, if this field is set to 50, and the cluster needs a new i3.xlarge spot instance, then the max price is half of the price of on-demand i3.xlarge instances. Similarly, if this field is set to 200, the max price is twice the price of on-demand i3.xlarge instances. If not specified, the default value is 100. When spot instances are requested for this cluster, only spot instances whose max price percentage matches this field will be considered. For safety, we enforce this field to be no more than 10000.
        :param zone_id: Identifier for the availability zone/datacenter in which the cluster resides. You have three options:. Specify an availability zone as a string, for example: 'us-west-2a'. The provided availability zone must be in the same region as the Databricks deployment. For example, 'us-west-2a' is not a valid zone ID if the Databricks deployment resides in the 'us-east-1' region. Enable automatic availability zone selection ('Auto-AZ'), by setting the value 'auto'. Databricks selects the AZ based on available IPs in the workspace subnets and retries in other availability zones if AWS returns insufficient capacity errors. Do not specify a value. If not specified, a default zone will be used.

        :schema: AwsAttributes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6314732fb0c5259551cd079d3176d459622b013a40b8b6f039a7af0c664e78)
            check_type(argname="argument availability", value=availability, expected_type=type_hints["availability"])
            check_type(argname="argument ebs_volume_count", value=ebs_volume_count, expected_type=type_hints["ebs_volume_count"])
            check_type(argname="argument ebs_volume_iops", value=ebs_volume_iops, expected_type=type_hints["ebs_volume_iops"])
            check_type(argname="argument ebs_volume_size", value=ebs_volume_size, expected_type=type_hints["ebs_volume_size"])
            check_type(argname="argument ebs_volume_throughput", value=ebs_volume_throughput, expected_type=type_hints["ebs_volume_throughput"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument first_on_demand", value=first_on_demand, expected_type=type_hints["first_on_demand"])
            check_type(argname="argument spot_bid_price_percent", value=spot_bid_price_percent, expected_type=type_hints["spot_bid_price_percent"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability is not None:
            self._values["availability"] = availability
        if ebs_volume_count is not None:
            self._values["ebs_volume_count"] = ebs_volume_count
        if ebs_volume_iops is not None:
            self._values["ebs_volume_iops"] = ebs_volume_iops
        if ebs_volume_size is not None:
            self._values["ebs_volume_size"] = ebs_volume_size
        if ebs_volume_throughput is not None:
            self._values["ebs_volume_throughput"] = ebs_volume_throughput
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if first_on_demand is not None:
            self._values["first_on_demand"] = first_on_demand
        if spot_bid_price_percent is not None:
            self._values["spot_bid_price_percent"] = spot_bid_price_percent
        if zone_id is not None:
            self._values["zone_id"] = zone_id

    @builtins.property
    def availability(self) -> typing.Optional["AwsAttributesAvailability"]:
        '''Availability type used for all subsequent nodes past the first_on_demand ones.

        Note: If first_on_demand is zero, this availability type will be used for the entire cluster.

        :schema: AwsAttributes#Availability
        '''
        result = self._values.get("availability")
        return typing.cast(typing.Optional["AwsAttributesAvailability"], result)

    @builtins.property
    def ebs_volume_count(self) -> typing.Optional[jsii.Number]:
        '''The number of volumes launched for each instance.

        You can choose up to 10 volumes. This feature is only enabled for supported node types. Legacy node types cannot specify custom EBS volumes. For node types with no instance store, at least one EBS volume needs to be specified; otherwise, cluster creation will fail.

        These EBS volumes will be mounted at /ebs0, /ebs1, and etc. Instance store volumes will be mounted at /local_disk0, /local_disk1, and etc.

        If EBS volumes are attached, Databricks will configure Spark to use only the EBS volumes for scratch storage because heterogeneously sized scratch devices can lead to inefficient disk utilization. If no EBS volumes are attached, Databricks will configure Spark to use instance store volumes.

        If EBS volumes are specified, then the Spark configuration spark.local.dir will be overridden.

        :schema: AwsAttributes#EbsVolumeCount
        '''
        result = self._values.get("ebs_volume_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_iops(self) -> typing.Optional[jsii.Number]:
        '''The number of IOPS per EBS gp3 volume.

        This value must be between 3000 and 16000.

        The value of IOPS and throughput is calculated based on AWS documentation to match the maximum performance of a gp2 volume with the same volume size.

        For more information, see the EBS volume limit calculator.

        :schema: AwsAttributes#EbsVolumeIops
        '''
        result = self._values.get("ebs_volume_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_size(self) -> typing.Optional[jsii.Number]:
        '''The size of each EBS volume (in GiB) launched for each instance.

        For general purpose SSD, this value must be within the range 100 - 4096. For throughput optimized HDD, this value must be within the range 500 - 4096. Custom EBS volumes cannot be specified for the legacy node types (memory-optimized and compute-optimized).

        :schema: AwsAttributes#EbsVolumeSize
        '''
        result = self._values.get("ebs_volume_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_throughput(self) -> typing.Optional[jsii.Number]:
        '''The throughput per EBS gp3 volume, in MiB per second.

        This value must be between 125 and 1000.

        :schema: AwsAttributes#EbsVolumeThroughput
        '''
        result = self._values.get("ebs_volume_throughput")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional["AwsAttributesEbsVolumeType"]:
        '''The type of EBS volumes that will be launched with this cluster.

        :schema: AwsAttributes#EbsVolumeType
        '''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional["AwsAttributesEbsVolumeType"], result)

    @builtins.property
    def first_on_demand(self) -> typing.Optional[jsii.Number]:
        '''The first first_on_demand nodes of the cluster will be placed on on-demand instances.

        If this value is greater than 0, the cluster driver node will be placed on an on-demand instance. If this value is greater than or equal to the current cluster size, all nodes will be placed on on-demand instances. If this value is less than the current cluster size, first_on_demand nodes will be placed on on-demand instances and the remainder will be placed on availability instances. This value does not affect cluster size and cannot be mutated over the lifetime of a cluster.

        :schema: AwsAttributes#FirstOnDemand
        '''
        result = self._values.get("first_on_demand")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spot_bid_price_percent(self) -> typing.Optional[jsii.Number]:
        '''The max price for AWS spot instances, as a percentage of the corresponding instance type's on-demand price.

        For example, if this field is set to 50, and the cluster needs a new i3.xlarge spot instance, then the max price is half of the price of on-demand i3.xlarge instances. Similarly, if this field is set to 200, the max price is twice the price of on-demand i3.xlarge instances. If not specified, the default value is 100. When spot instances are requested for this cluster, only spot instances whose max price percentage matches this field will be considered. For safety, we enforce this field to be no more than 10000.

        :schema: AwsAttributes#SpotBidPricePercent
        '''
        result = self._values.get("spot_bid_price_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''Identifier for the availability zone/datacenter in which the cluster resides. You have three options:.

        Specify an availability zone as a string, for example: 'us-west-2a'. The provided availability zone must be in the same region as the Databricks deployment. For example, 'us-west-2a' is not a valid zone ID if the Databricks deployment resides in the 'us-east-1' region.

        Enable automatic availability zone selection ('Auto-AZ'), by setting the value 'auto'. Databricks selects the AZ based on available IPs in the workspace subnets and retries in other availability zones if AWS returns insufficient capacity errors.

        Do not specify a value. If not specified, a default zone will be used.

        :schema: AwsAttributes#ZoneId
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.AwsAttributesAvailability"
)
class AwsAttributesAvailability(enum.Enum):
    '''Availability type used for all subsequent nodes past the first_on_demand ones.

    Note: If first_on_demand is zero, this availability type will be used for the entire cluster.

    :schema: AwsAttributesAvailability
    '''

    SPOT = "SPOT"
    '''SPOT.'''
    ON_DEMAND = "ON_DEMAND"
    '''ON_DEMAND.'''
    SPOT_WITH_FALLBACK = "SPOT_WITH_FALLBACK"
    '''SPOT_WITH_FALLBACK.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.AwsAttributesEbsVolumeType"
)
class AwsAttributesEbsVolumeType(enum.Enum):
    '''The type of EBS volumes that will be launched with this cluster.

    :schema: AwsAttributesEbsVolumeType
    '''

    GENERAL_PURPOSE_SSD = "GENERAL_PURPOSE_SSD"
    '''GENERAL_PURPOSE_SSD.'''
    THROUGHPUT_OPTIMIZED_HDD = "THROUGHPUT_OPTIMIZED_HDD"
    '''THROUGHPUT_OPTIMIZED_HDD.'''


class CfnCluster(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.CfnCluster",
):
    '''A CloudFormation ``Databricks::Clusters::Cluster``.

    :cloudformationResource: Databricks::Clusters::Cluster
    :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        apply_policy_default_values: typing.Optional[builtins.bool] = None,
        autoscale: typing.Optional[typing.Union[Autoscale, typing.Dict[builtins.str, typing.Any]]] = None,
        autotermination_minutes: typing.Optional[jsii.Number] = None,
        aws_attributes: typing.Optional[typing.Union[AwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_cores: typing.Optional[jsii.Number] = None,
        cluster_memory_mb: typing.Optional[jsii.Number] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        cluster_source: typing.Optional[builtins.str] = None,
        creator_user_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Any = None,
        default_tags: typing.Optional[typing.Union["CfnClusterPropsDefaultTags", typing.Dict[builtins.str, typing.Any]]] = None,
        driver: typing.Any = None,
        driver_instance_pool_id: typing.Optional[builtins.str] = None,
        driver_instance_source: typing.Optional[typing.Union["CfnClusterPropsDriverInstanceSource", typing.Dict[builtins.str, typing.Any]]] = None,
        driver_node_type_id: typing.Optional[builtins.str] = None,
        effective_spark_version: typing.Optional[builtins.str] = None,
        enable_elastic_disk: typing.Optional[builtins.bool] = None,
        enable_local_disk_encryption: typing.Optional[builtins.bool] = None,
        idempotency_token: typing.Optional[builtins.str] = None,
        init_scripts: typing.Optional[typing.Sequence[typing.Union["InitScriptsListItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_pool_id: typing.Optional[builtins.str] = None,
        instance_source: typing.Optional[typing.Union["CfnClusterPropsInstanceSource", typing.Dict[builtins.str, typing.Any]]] = None,
        node_type_id: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        runtime_engine: typing.Optional[builtins.str] = None,
        spark_conf: typing.Any = None,
        spark_env_vars: typing.Any = None,
        spark_version: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Databricks::Clusters::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param apply_policy_default_values: Whether to use policy default values for missing cluster attributes.
        :param autoscale: 
        :param autotermination_minutes: Automatically terminates the cluster after it is inactive for this time in minutes. If not set, this cluster will not be automatically terminated. If specified, the threshold must be between 10 and 10000 minutes. You can also set this value to 0 to explicitly disable
        :param aws_attributes: 
        :param cluster_cores: 
        :param cluster_memory_mb: 
        :param cluster_name: Cluster name requested by the user. This doesn't have to be unique. If not specified at creation, the cluster name will be an empty string.
        :param cluster_source: 
        :param creator_user_name: 
        :param custom_tags: 
        :param default_tags: 
        :param driver: 
        :param driver_instance_pool_id: The optional ID of the instance pool to use for the driver node. You must also specify instance_pool_id. Refer to Instance Pools API 2.0 for details.
        :param driver_instance_source: 
        :param driver_node_type_id: The node type of the Spark driver. This field is optional; if unset, the driver node type will be set as the same value as node_type_id defined above.
        :param effective_spark_version: 
        :param enable_elastic_disk: Autoscaling Local Storage: when enabled, this cluster will dynamically acquire additional disk space when its Spark workers are running low on disk space. This feature requires specific AWS permissions to function correctly - refer to Autoscaling local storage for details.
        :param enable_local_disk_encryption: Whether encryption of disks locally attached to the cluster is enabled.
        :param idempotency_token: An optional token that can be used to guarantee the idempotency of cluster creation requests. If the idempotency token is assigned to a cluster that is not in the TERMINATED state, the request does not create a new cluster but instead returns the ID of the existing cluster. Otherwise, a new cluster is created. The idempotency token is cleared when the cluster is terminated If you specify the idempotency token, upon failure you can retry until the request succeeds. Databricks guarantees that exactly one cluster will be launched with that idempotency token. This token should have at most 64 characters.
        :param init_scripts: The configuration for storing init scripts. Any number of destinations can be specified. The scripts are executed sequentially in the order provided. If cluster_log_conf is specified, init script logs are sent to //init_scripts.
        :param instance_pool_id: The optional ID of the instance pool to use for cluster nodes. If driver_instance_pool_id is present, instance_pool_id is used for worker nodes only. Otherwise, it is used for both the driver and worker nodes. Refer to Instance Pools API 2.0 for details.
        :param instance_source: 
        :param node_type_id: This field encodes, through a single value, the resources available to each of the Spark nodes in this cluster. For example, the Spark nodes can be provisioned and optimized for memory or compute intensive workloads A list of available node types can be retrieved by using the List node types API call. This field is required.
        :param num_workers: If num_workers, number of worker nodes that this cluster should have. A cluster has one Spark driver and num_workers executors for a total of num_workers + 1 Spark nodes.
        :param runtime_engine: The type of runtime engine to use. If not specified, the runtime engine type is inferred based on the spark_version value. Allowed values include: PHOTON: Use the Photon runtime engine type. STANDARD: Use the standard runtime engine type. This field is optional.
        :param spark_conf: 
        :param spark_env_vars: An object containing a set of optional, user-specified environment variable key-value pairs. Key-value pairs of the form (X,Y) are exported as is (that is, export X='Y') while launching the driver and workers. In order to specify an additional set of SPARK_DAEMON_JAVA_OPTS, we recommend appending them to $SPARK_DAEMON_JAVA_OPTS as shown in the following example. This ensures that all default Databricks managed environmental variables are included as well. Example Spark environment variables: {"SPARK_WORKER_MEMORY": "28000m", "SPARK_LOCAL_DIRS": "/local_disk0"} or {"SPARK_DAEMON_JAVA_OPTS": "$SPARK_DAEMON_JAVA_OPTS
        :param spark_version: The runtime version of the cluster. You can retrieve a list of available runtime versions by using the Runtime versions API call. This field is required.
        :param ssh_public_keys: SSH public key contents that will be added to each Spark node in this cluster. The corresponding private keys can be used to login with the user name ubuntu on port 2200. Up to 10 keys can be specified.
        :param start_time: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdbd7f90ef58dc6b80a7c369dd6485e775ef4c174318055a1dd0a80d66cebf4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            apply_policy_default_values=apply_policy_default_values,
            autoscale=autoscale,
            autotermination_minutes=autotermination_minutes,
            aws_attributes=aws_attributes,
            cluster_cores=cluster_cores,
            cluster_memory_mb=cluster_memory_mb,
            cluster_name=cluster_name,
            cluster_source=cluster_source,
            creator_user_name=creator_user_name,
            custom_tags=custom_tags,
            default_tags=default_tags,
            driver=driver,
            driver_instance_pool_id=driver_instance_pool_id,
            driver_instance_source=driver_instance_source,
            driver_node_type_id=driver_node_type_id,
            effective_spark_version=effective_spark_version,
            enable_elastic_disk=enable_elastic_disk,
            enable_local_disk_encryption=enable_local_disk_encryption,
            idempotency_token=idempotency_token,
            init_scripts=init_scripts,
            instance_pool_id=instance_pool_id,
            instance_source=instance_source,
            node_type_id=node_type_id,
            num_workers=num_workers,
            runtime_engine=runtime_engine,
            spark_conf=spark_conf,
            spark_env_vars=spark_env_vars,
            spark_version=spark_version,
            ssh_public_keys=ssh_public_keys,
            start_time=start_time,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterId")
    def attr_cluster_id(self) -> builtins.str:
        '''Attribute ``Databricks::Clusters::Cluster.ClusterId``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterId"))

    @builtins.property
    @jsii.member(jsii_name="attrInitScriptsSafeMode")
    def attr_init_scripts_safe_mode(self) -> _aws_cdk_ceddda9d.IResolvable:
        '''Attribute ``Databricks::Clusters::Cluster.InitScriptsSafeMode``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(_aws_cdk_ceddda9d.IResolvable, jsii.get(self, "attrInitScriptsSafeMode"))

    @builtins.property
    @jsii.member(jsii_name="attrLastActivityTime")
    def attr_last_activity_time(self) -> jsii.Number:
        '''Attribute ``Databricks::Clusters::Cluster.LastActivityTime``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrLastActivityTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastRestartedTime")
    def attr_last_restarted_time(self) -> jsii.Number:
        '''Attribute ``Databricks::Clusters::Cluster.LastRestartedTime``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrLastRestartedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLastStateLossTime")
    def attr_last_state_loss_time(self) -> jsii.Number:
        '''Attribute ``Databricks::Clusters::Cluster.LastStateLossTime``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrLastStateLossTime"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Attribute ``Databricks::Clusters::Cluster.State``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrStateMessage")
    def attr_state_message(self) -> builtins.str:
        '''Attribute ``Databricks::Clusters::Cluster.StateMessage``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStateMessage"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnClusterProps":
        '''Resource props.'''
        return typing.cast("CfnClusterProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "apply_policy_default_values": "applyPolicyDefaultValues",
        "autoscale": "autoscale",
        "autotermination_minutes": "autoterminationMinutes",
        "aws_attributes": "awsAttributes",
        "cluster_cores": "clusterCores",
        "cluster_memory_mb": "clusterMemoryMb",
        "cluster_name": "clusterName",
        "cluster_source": "clusterSource",
        "creator_user_name": "creatorUserName",
        "custom_tags": "customTags",
        "default_tags": "defaultTags",
        "driver": "driver",
        "driver_instance_pool_id": "driverInstancePoolId",
        "driver_instance_source": "driverInstanceSource",
        "driver_node_type_id": "driverNodeTypeId",
        "effective_spark_version": "effectiveSparkVersion",
        "enable_elastic_disk": "enableElasticDisk",
        "enable_local_disk_encryption": "enableLocalDiskEncryption",
        "idempotency_token": "idempotencyToken",
        "init_scripts": "initScripts",
        "instance_pool_id": "instancePoolId",
        "instance_source": "instanceSource",
        "node_type_id": "nodeTypeId",
        "num_workers": "numWorkers",
        "runtime_engine": "runtimeEngine",
        "spark_conf": "sparkConf",
        "spark_env_vars": "sparkEnvVars",
        "spark_version": "sparkVersion",
        "ssh_public_keys": "sshPublicKeys",
        "start_time": "startTime",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        apply_policy_default_values: typing.Optional[builtins.bool] = None,
        autoscale: typing.Optional[typing.Union[Autoscale, typing.Dict[builtins.str, typing.Any]]] = None,
        autotermination_minutes: typing.Optional[jsii.Number] = None,
        aws_attributes: typing.Optional[typing.Union[AwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
        cluster_cores: typing.Optional[jsii.Number] = None,
        cluster_memory_mb: typing.Optional[jsii.Number] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        cluster_source: typing.Optional[builtins.str] = None,
        creator_user_name: typing.Optional[builtins.str] = None,
        custom_tags: typing.Any = None,
        default_tags: typing.Optional[typing.Union["CfnClusterPropsDefaultTags", typing.Dict[builtins.str, typing.Any]]] = None,
        driver: typing.Any = None,
        driver_instance_pool_id: typing.Optional[builtins.str] = None,
        driver_instance_source: typing.Optional[typing.Union["CfnClusterPropsDriverInstanceSource", typing.Dict[builtins.str, typing.Any]]] = None,
        driver_node_type_id: typing.Optional[builtins.str] = None,
        effective_spark_version: typing.Optional[builtins.str] = None,
        enable_elastic_disk: typing.Optional[builtins.bool] = None,
        enable_local_disk_encryption: typing.Optional[builtins.bool] = None,
        idempotency_token: typing.Optional[builtins.str] = None,
        init_scripts: typing.Optional[typing.Sequence[typing.Union["InitScriptsListItem", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_pool_id: typing.Optional[builtins.str] = None,
        instance_source: typing.Optional[typing.Union["CfnClusterPropsInstanceSource", typing.Dict[builtins.str, typing.Any]]] = None,
        node_type_id: typing.Optional[builtins.str] = None,
        num_workers: typing.Optional[jsii.Number] = None,
        runtime_engine: typing.Optional[builtins.str] = None,
        spark_conf: typing.Any = None,
        spark_env_vars: typing.Any = None,
        spark_version: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        start_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manage a Databricks Cluster.

        :param apply_policy_default_values: Whether to use policy default values for missing cluster attributes.
        :param autoscale: 
        :param autotermination_minutes: Automatically terminates the cluster after it is inactive for this time in minutes. If not set, this cluster will not be automatically terminated. If specified, the threshold must be between 10 and 10000 minutes. You can also set this value to 0 to explicitly disable
        :param aws_attributes: 
        :param cluster_cores: 
        :param cluster_memory_mb: 
        :param cluster_name: Cluster name requested by the user. This doesn't have to be unique. If not specified at creation, the cluster name will be an empty string.
        :param cluster_source: 
        :param creator_user_name: 
        :param custom_tags: 
        :param default_tags: 
        :param driver: 
        :param driver_instance_pool_id: The optional ID of the instance pool to use for the driver node. You must also specify instance_pool_id. Refer to Instance Pools API 2.0 for details.
        :param driver_instance_source: 
        :param driver_node_type_id: The node type of the Spark driver. This field is optional; if unset, the driver node type will be set as the same value as node_type_id defined above.
        :param effective_spark_version: 
        :param enable_elastic_disk: Autoscaling Local Storage: when enabled, this cluster will dynamically acquire additional disk space when its Spark workers are running low on disk space. This feature requires specific AWS permissions to function correctly - refer to Autoscaling local storage for details.
        :param enable_local_disk_encryption: Whether encryption of disks locally attached to the cluster is enabled.
        :param idempotency_token: An optional token that can be used to guarantee the idempotency of cluster creation requests. If the idempotency token is assigned to a cluster that is not in the TERMINATED state, the request does not create a new cluster but instead returns the ID of the existing cluster. Otherwise, a new cluster is created. The idempotency token is cleared when the cluster is terminated If you specify the idempotency token, upon failure you can retry until the request succeeds. Databricks guarantees that exactly one cluster will be launched with that idempotency token. This token should have at most 64 characters.
        :param init_scripts: The configuration for storing init scripts. Any number of destinations can be specified. The scripts are executed sequentially in the order provided. If cluster_log_conf is specified, init script logs are sent to //init_scripts.
        :param instance_pool_id: The optional ID of the instance pool to use for cluster nodes. If driver_instance_pool_id is present, instance_pool_id is used for worker nodes only. Otherwise, it is used for both the driver and worker nodes. Refer to Instance Pools API 2.0 for details.
        :param instance_source: 
        :param node_type_id: This field encodes, through a single value, the resources available to each of the Spark nodes in this cluster. For example, the Spark nodes can be provisioned and optimized for memory or compute intensive workloads A list of available node types can be retrieved by using the List node types API call. This field is required.
        :param num_workers: If num_workers, number of worker nodes that this cluster should have. A cluster has one Spark driver and num_workers executors for a total of num_workers + 1 Spark nodes.
        :param runtime_engine: The type of runtime engine to use. If not specified, the runtime engine type is inferred based on the spark_version value. Allowed values include: PHOTON: Use the Photon runtime engine type. STANDARD: Use the standard runtime engine type. This field is optional.
        :param spark_conf: 
        :param spark_env_vars: An object containing a set of optional, user-specified environment variable key-value pairs. Key-value pairs of the form (X,Y) are exported as is (that is, export X='Y') while launching the driver and workers. In order to specify an additional set of SPARK_DAEMON_JAVA_OPTS, we recommend appending them to $SPARK_DAEMON_JAVA_OPTS as shown in the following example. This ensures that all default Databricks managed environmental variables are included as well. Example Spark environment variables: {"SPARK_WORKER_MEMORY": "28000m", "SPARK_LOCAL_DIRS": "/local_disk0"} or {"SPARK_DAEMON_JAVA_OPTS": "$SPARK_DAEMON_JAVA_OPTS
        :param spark_version: The runtime version of the cluster. You can retrieve a list of available runtime versions by using the Runtime versions API call. This field is required.
        :param ssh_public_keys: SSH public key contents that will be added to each Spark node in this cluster. The corresponding private keys can be used to login with the user name ubuntu on port 2200. Up to 10 keys can be specified.
        :param start_time: 

        :schema: CfnClusterProps
        '''
        if isinstance(autoscale, dict):
            autoscale = Autoscale(**autoscale)
        if isinstance(aws_attributes, dict):
            aws_attributes = AwsAttributes(**aws_attributes)
        if isinstance(default_tags, dict):
            default_tags = CfnClusterPropsDefaultTags(**default_tags)
        if isinstance(driver_instance_source, dict):
            driver_instance_source = CfnClusterPropsDriverInstanceSource(**driver_instance_source)
        if isinstance(instance_source, dict):
            instance_source = CfnClusterPropsInstanceSource(**instance_source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f650b2e7718c1b77942561e86fa647b4da4df8a9d793ba217e635d4a81671ce)
            check_type(argname="argument apply_policy_default_values", value=apply_policy_default_values, expected_type=type_hints["apply_policy_default_values"])
            check_type(argname="argument autoscale", value=autoscale, expected_type=type_hints["autoscale"])
            check_type(argname="argument autotermination_minutes", value=autotermination_minutes, expected_type=type_hints["autotermination_minutes"])
            check_type(argname="argument aws_attributes", value=aws_attributes, expected_type=type_hints["aws_attributes"])
            check_type(argname="argument cluster_cores", value=cluster_cores, expected_type=type_hints["cluster_cores"])
            check_type(argname="argument cluster_memory_mb", value=cluster_memory_mb, expected_type=type_hints["cluster_memory_mb"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument cluster_source", value=cluster_source, expected_type=type_hints["cluster_source"])
            check_type(argname="argument creator_user_name", value=creator_user_name, expected_type=type_hints["creator_user_name"])
            check_type(argname="argument custom_tags", value=custom_tags, expected_type=type_hints["custom_tags"])
            check_type(argname="argument default_tags", value=default_tags, expected_type=type_hints["default_tags"])
            check_type(argname="argument driver", value=driver, expected_type=type_hints["driver"])
            check_type(argname="argument driver_instance_pool_id", value=driver_instance_pool_id, expected_type=type_hints["driver_instance_pool_id"])
            check_type(argname="argument driver_instance_source", value=driver_instance_source, expected_type=type_hints["driver_instance_source"])
            check_type(argname="argument driver_node_type_id", value=driver_node_type_id, expected_type=type_hints["driver_node_type_id"])
            check_type(argname="argument effective_spark_version", value=effective_spark_version, expected_type=type_hints["effective_spark_version"])
            check_type(argname="argument enable_elastic_disk", value=enable_elastic_disk, expected_type=type_hints["enable_elastic_disk"])
            check_type(argname="argument enable_local_disk_encryption", value=enable_local_disk_encryption, expected_type=type_hints["enable_local_disk_encryption"])
            check_type(argname="argument idempotency_token", value=idempotency_token, expected_type=type_hints["idempotency_token"])
            check_type(argname="argument init_scripts", value=init_scripts, expected_type=type_hints["init_scripts"])
            check_type(argname="argument instance_pool_id", value=instance_pool_id, expected_type=type_hints["instance_pool_id"])
            check_type(argname="argument instance_source", value=instance_source, expected_type=type_hints["instance_source"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
            check_type(argname="argument num_workers", value=num_workers, expected_type=type_hints["num_workers"])
            check_type(argname="argument runtime_engine", value=runtime_engine, expected_type=type_hints["runtime_engine"])
            check_type(argname="argument spark_conf", value=spark_conf, expected_type=type_hints["spark_conf"])
            check_type(argname="argument spark_env_vars", value=spark_env_vars, expected_type=type_hints["spark_env_vars"])
            check_type(argname="argument spark_version", value=spark_version, expected_type=type_hints["spark_version"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apply_policy_default_values is not None:
            self._values["apply_policy_default_values"] = apply_policy_default_values
        if autoscale is not None:
            self._values["autoscale"] = autoscale
        if autotermination_minutes is not None:
            self._values["autotermination_minutes"] = autotermination_minutes
        if aws_attributes is not None:
            self._values["aws_attributes"] = aws_attributes
        if cluster_cores is not None:
            self._values["cluster_cores"] = cluster_cores
        if cluster_memory_mb is not None:
            self._values["cluster_memory_mb"] = cluster_memory_mb
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if cluster_source is not None:
            self._values["cluster_source"] = cluster_source
        if creator_user_name is not None:
            self._values["creator_user_name"] = creator_user_name
        if custom_tags is not None:
            self._values["custom_tags"] = custom_tags
        if default_tags is not None:
            self._values["default_tags"] = default_tags
        if driver is not None:
            self._values["driver"] = driver
        if driver_instance_pool_id is not None:
            self._values["driver_instance_pool_id"] = driver_instance_pool_id
        if driver_instance_source is not None:
            self._values["driver_instance_source"] = driver_instance_source
        if driver_node_type_id is not None:
            self._values["driver_node_type_id"] = driver_node_type_id
        if effective_spark_version is not None:
            self._values["effective_spark_version"] = effective_spark_version
        if enable_elastic_disk is not None:
            self._values["enable_elastic_disk"] = enable_elastic_disk
        if enable_local_disk_encryption is not None:
            self._values["enable_local_disk_encryption"] = enable_local_disk_encryption
        if idempotency_token is not None:
            self._values["idempotency_token"] = idempotency_token
        if init_scripts is not None:
            self._values["init_scripts"] = init_scripts
        if instance_pool_id is not None:
            self._values["instance_pool_id"] = instance_pool_id
        if instance_source is not None:
            self._values["instance_source"] = instance_source
        if node_type_id is not None:
            self._values["node_type_id"] = node_type_id
        if num_workers is not None:
            self._values["num_workers"] = num_workers
        if runtime_engine is not None:
            self._values["runtime_engine"] = runtime_engine
        if spark_conf is not None:
            self._values["spark_conf"] = spark_conf
        if spark_env_vars is not None:
            self._values["spark_env_vars"] = spark_env_vars
        if spark_version is not None:
            self._values["spark_version"] = spark_version
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def apply_policy_default_values(self) -> typing.Optional[builtins.bool]:
        '''Whether to use policy default values for missing cluster attributes.

        :schema: CfnClusterProps#ApplyPolicyDefaultValues
        '''
        result = self._values.get("apply_policy_default_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def autoscale(self) -> typing.Optional[Autoscale]:
        '''
        :schema: CfnClusterProps#Autoscale
        '''
        result = self._values.get("autoscale")
        return typing.cast(typing.Optional[Autoscale], result)

    @builtins.property
    def autotermination_minutes(self) -> typing.Optional[jsii.Number]:
        '''Automatically terminates the cluster after it is inactive for this time in minutes.

        If not set, this cluster will not be automatically terminated. If specified, the threshold must be between 10 and 10000 minutes. You can also set this value to 0 to explicitly disable

        :schema: CfnClusterProps#AutoterminationMinutes
        '''
        result = self._values.get("autotermination_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aws_attributes(self) -> typing.Optional[AwsAttributes]:
        '''
        :schema: CfnClusterProps#AwsAttributes
        '''
        result = self._values.get("aws_attributes")
        return typing.cast(typing.Optional[AwsAttributes], result)

    @builtins.property
    def cluster_cores(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnClusterProps#ClusterCores
        '''
        result = self._values.get("cluster_cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_memory_mb(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnClusterProps#ClusterMemoryMb
        '''
        result = self._values.get("cluster_memory_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''Cluster name requested by the user.

        This doesn't have to be unique. If not specified at creation, the cluster name will be an empty string.

        :schema: CfnClusterProps#ClusterName
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_source(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterProps#ClusterSource
        '''
        result = self._values.get("cluster_source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator_user_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterProps#CreatorUserName
        '''
        result = self._values.get("creator_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_tags(self) -> typing.Any:
        '''
        :schema: CfnClusterProps#CustomTags
        '''
        result = self._values.get("custom_tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def default_tags(self) -> typing.Optional["CfnClusterPropsDefaultTags"]:
        '''
        :schema: CfnClusterProps#DefaultTags
        '''
        result = self._values.get("default_tags")
        return typing.cast(typing.Optional["CfnClusterPropsDefaultTags"], result)

    @builtins.property
    def driver(self) -> typing.Any:
        '''
        :schema: CfnClusterProps#Driver
        '''
        result = self._values.get("driver")
        return typing.cast(typing.Any, result)

    @builtins.property
    def driver_instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''The optional ID of the instance pool to use for the driver node.

        You must also specify instance_pool_id. Refer to Instance Pools API 2.0 for details.

        :schema: CfnClusterProps#DriverInstancePoolId
        '''
        result = self._values.get("driver_instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def driver_instance_source(
        self,
    ) -> typing.Optional["CfnClusterPropsDriverInstanceSource"]:
        '''
        :schema: CfnClusterProps#DriverInstanceSource
        '''
        result = self._values.get("driver_instance_source")
        return typing.cast(typing.Optional["CfnClusterPropsDriverInstanceSource"], result)

    @builtins.property
    def driver_node_type_id(self) -> typing.Optional[builtins.str]:
        '''The node type of the Spark driver.

        This field is optional; if unset, the driver node type will be set as the same value as node_type_id defined above.

        :schema: CfnClusterProps#DriverNodeTypeId
        '''
        result = self._values.get("driver_node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_spark_version(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterProps#EffectiveSparkVersion
        '''
        result = self._values.get("effective_spark_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_elastic_disk(self) -> typing.Optional[builtins.bool]:
        '''Autoscaling Local Storage: when enabled, this cluster will dynamically acquire additional disk space when its Spark workers are running low on disk space.

        This feature requires specific AWS permissions to function correctly - refer to Autoscaling local storage for details.

        :schema: CfnClusterProps#EnableElasticDisk
        '''
        result = self._values.get("enable_elastic_disk")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_local_disk_encryption(self) -> typing.Optional[builtins.bool]:
        '''Whether encryption of disks locally attached to the cluster is enabled.

        :schema: CfnClusterProps#EnableLocalDiskEncryption
        '''
        result = self._values.get("enable_local_disk_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def idempotency_token(self) -> typing.Optional[builtins.str]:
        '''An optional token that can be used to guarantee the idempotency of cluster creation requests.

        If the idempotency token is assigned to a cluster that is not in the TERMINATED state, the request does not create a new cluster but instead returns the ID of the existing cluster. Otherwise, a new cluster is created. The idempotency token is cleared when the cluster is terminated

        If you specify the idempotency token, upon failure you can retry until the request succeeds. Databricks guarantees that exactly one cluster will be launched with that idempotency token.

        This token should have at most 64 characters.

        :schema: CfnClusterProps#IdempotencyToken
        '''
        result = self._values.get("idempotency_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def init_scripts(self) -> typing.Optional[typing.List["InitScriptsListItem"]]:
        '''The configuration for storing init scripts.

        Any number of destinations can be specified. The scripts are executed sequentially in the order provided. If cluster_log_conf is specified, init script logs are sent to //init_scripts.

        :schema: CfnClusterProps#InitScripts
        '''
        result = self._values.get("init_scripts")
        return typing.cast(typing.Optional[typing.List["InitScriptsListItem"]], result)

    @builtins.property
    def instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''The optional ID of the instance pool to use for cluster nodes.

        If driver_instance_pool_id is present, instance_pool_id is used for worker nodes only. Otherwise, it is used for both the driver and worker nodes. Refer to Instance Pools API 2.0 for details.

        :schema: CfnClusterProps#InstancePoolId
        '''
        result = self._values.get("instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_source(self) -> typing.Optional["CfnClusterPropsInstanceSource"]:
        '''
        :schema: CfnClusterProps#InstanceSource
        '''
        result = self._values.get("instance_source")
        return typing.cast(typing.Optional["CfnClusterPropsInstanceSource"], result)

    @builtins.property
    def node_type_id(self) -> typing.Optional[builtins.str]:
        '''This field encodes, through a single value, the resources available to each of the Spark nodes in this cluster.

        For example, the Spark nodes can be provisioned and optimized for memory or compute intensive workloads A list of available node types can be retrieved by using the List node types API call. This field is required.

        :schema: CfnClusterProps#NodeTypeId
        '''
        result = self._values.get("node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def num_workers(self) -> typing.Optional[jsii.Number]:
        '''If num_workers, number of worker nodes that this cluster should have.

        A cluster has one Spark driver and num_workers executors for a total of num_workers + 1 Spark nodes.

        :schema: CfnClusterProps#NumWorkers
        '''
        result = self._values.get("num_workers")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def runtime_engine(self) -> typing.Optional[builtins.str]:
        '''The type of runtime engine to use.

        If not specified, the runtime engine type is inferred based on the spark_version value. Allowed values include:

        PHOTON: Use the Photon runtime engine type.

        STANDARD: Use the standard runtime engine type.

        This field is optional.

        :schema: CfnClusterProps#RuntimeEngine
        '''
        result = self._values.get("runtime_engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_conf(self) -> typing.Any:
        '''
        :schema: CfnClusterProps#SparkConf
        '''
        result = self._values.get("spark_conf")
        return typing.cast(typing.Any, result)

    @builtins.property
    def spark_env_vars(self) -> typing.Any:
        '''An object containing a set of optional, user-specified environment variable key-value pairs.

        Key-value pairs of the form (X,Y) are exported as is (that is, export X='Y') while launching the driver and workers. In order to specify an additional set of SPARK_DAEMON_JAVA_OPTS, we recommend appending them to $SPARK_DAEMON_JAVA_OPTS as shown in the following example. This ensures that all default Databricks managed environmental variables are included as well. Example Spark environment variables: {"SPARK_WORKER_MEMORY": "28000m", "SPARK_LOCAL_DIRS": "/local_disk0"} or {"SPARK_DAEMON_JAVA_OPTS": "$SPARK_DAEMON_JAVA_OPTS

        :schema: CfnClusterProps#SparkEnvVars
        '''
        result = self._values.get("spark_env_vars")
        return typing.cast(typing.Any, result)

    @builtins.property
    def spark_version(self) -> typing.Optional[builtins.str]:
        '''The runtime version of the cluster.

        You can retrieve a list of available runtime versions by using the Runtime versions API call. This field is required.

        :schema: CfnClusterProps#SparkVersion
        '''
        result = self._values.get("spark_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''SSH public key contents that will be added to each Spark node in this cluster.

        The corresponding private keys can be used to login with the user name ubuntu on port 2200. Up to 10 keys can be specified.

        :schema: CfnClusterProps#SshPublicKeys
        '''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def start_time(self) -> typing.Optional[jsii.Number]:
        '''
        :schema: CfnClusterProps#StartTime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.CfnClusterPropsDefaultTags",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "cluster_name": "clusterName",
        "creator": "creator",
        "vendor": "vendor",
    },
)
class CfnClusterPropsDefaultTags:
    def __init__(
        self,
        *,
        cluster_id: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        creator: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_id: 
        :param cluster_name: 
        :param creator: 
        :param vendor: 

        :schema: CfnClusterPropsDefaultTags
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d6c79c17a187fb11ed59ca4a45d0f56e5d9eac554aa3532e4815702fb61e32)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument creator", value=creator, expected_type=type_hints["creator"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if creator is not None:
            self._values["creator"] = creator
        if vendor is not None:
            self._values["vendor"] = vendor

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsDefaultTags#ClusterId
        '''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsDefaultTags#ClusterName
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creator(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsDefaultTags#Creator
        '''
        result = self._values.get("creator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vendor(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsDefaultTags#Vendor
        '''
        result = self._values.get("vendor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterPropsDefaultTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.CfnClusterPropsDriverInstanceSource",
    jsii_struct_bases=[],
    name_mapping={"instance_pool_id": "instancePoolId", "node_type_id": "nodeTypeId"},
)
class CfnClusterPropsDriverInstanceSource:
    def __init__(
        self,
        *,
        instance_pool_id: typing.Optional[builtins.str] = None,
        node_type_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_pool_id: 
        :param node_type_id: 

        :schema: CfnClusterPropsDriverInstanceSource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7480ebe33a81c7ca7c6390a833b769f6d8c2374d5429150837eb33dcc9e4e5)
            check_type(argname="argument instance_pool_id", value=instance_pool_id, expected_type=type_hints["instance_pool_id"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_pool_id is not None:
            self._values["instance_pool_id"] = instance_pool_id
        if node_type_id is not None:
            self._values["node_type_id"] = node_type_id

    @builtins.property
    def instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsDriverInstanceSource#InstancePoolId
        '''
        result = self._values.get("instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsDriverInstanceSource#NodeTypeId
        '''
        result = self._values.get("node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterPropsDriverInstanceSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.CfnClusterPropsInstanceSource",
    jsii_struct_bases=[],
    name_mapping={"instance_pool_id": "instancePoolId", "node_type_id": "nodeTypeId"},
)
class CfnClusterPropsInstanceSource:
    def __init__(
        self,
        *,
        instance_pool_id: typing.Optional[builtins.str] = None,
        node_type_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_pool_id: 
        :param node_type_id: 

        :schema: CfnClusterPropsInstanceSource
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ea7c4a7bb422f959b7d3d4094b52c6b81cdcda5711f2d5a41fe56983330f50)
            check_type(argname="argument instance_pool_id", value=instance_pool_id, expected_type=type_hints["instance_pool_id"])
            check_type(argname="argument node_type_id", value=node_type_id, expected_type=type_hints["node_type_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_pool_id is not None:
            self._values["instance_pool_id"] = instance_pool_id
        if node_type_id is not None:
            self._values["node_type_id"] = node_type_id

    @builtins.property
    def instance_pool_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsInstanceSource#InstancePoolId
        '''
        result = self._values.get("instance_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_type_id(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnClusterPropsInstanceSource#NodeTypeId
        '''
        result = self._values.get("node_type_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterPropsInstanceSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.InitScriptsListItem",
    jsii_struct_bases=[],
    name_mapping={"s3": "s3"},
)
class InitScriptsListItem:
    def __init__(
        self,
        *,
        s3: typing.Optional[typing.Union["S3Destination", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param s3: 

        :schema: InitScriptsListItem
        '''
        if isinstance(s3, dict):
            s3 = S3Destination(**s3)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00c388acafb18ce256355a22a175059dcba1bebe0f8fab958b9a52a76e44fe11)
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def s3(self) -> typing.Optional["S3Destination"]:
        '''
        :schema: InitScriptsListItem#S3
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3Destination"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InitScriptsListItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-cluster.S3Destination",
    jsii_struct_bases=[],
    name_mapping={"destination": "destination", "region": "region"},
)
class S3Destination:
    def __init__(
        self,
        *,
        destination: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param destination: 
        :param region: 

        :schema: S3destination
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b60a48606074181b7d9145dc424623948956aca28558a35d8e25c2f08b2a6a76)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''
        :schema: S3destination#Destination
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''
        :schema: S3destination#Region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Destination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Autoscale",
    "AwsAttributes",
    "AwsAttributesAvailability",
    "AwsAttributesEbsVolumeType",
    "CfnCluster",
    "CfnClusterProps",
    "CfnClusterPropsDefaultTags",
    "CfnClusterPropsDriverInstanceSource",
    "CfnClusterPropsInstanceSource",
    "InitScriptsListItem",
    "S3Destination",
]

publication.publish()

def _typecheckingstub__cdda6b335054253b59f73353b7500526d79f5959ad84774a8f06d6cd82c62fbd(
    *,
    max_workers: jsii.Number,
    min_workers: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6314732fb0c5259551cd079d3176d459622b013a40b8b6f039a7af0c664e78(
    *,
    availability: typing.Optional[AwsAttributesAvailability] = None,
    ebs_volume_count: typing.Optional[jsii.Number] = None,
    ebs_volume_iops: typing.Optional[jsii.Number] = None,
    ebs_volume_size: typing.Optional[jsii.Number] = None,
    ebs_volume_throughput: typing.Optional[jsii.Number] = None,
    ebs_volume_type: typing.Optional[AwsAttributesEbsVolumeType] = None,
    first_on_demand: typing.Optional[jsii.Number] = None,
    spot_bid_price_percent: typing.Optional[jsii.Number] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdbd7f90ef58dc6b80a7c369dd6485e775ef4c174318055a1dd0a80d66cebf4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    apply_policy_default_values: typing.Optional[builtins.bool] = None,
    autoscale: typing.Optional[typing.Union[Autoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    autotermination_minutes: typing.Optional[jsii.Number] = None,
    aws_attributes: typing.Optional[typing.Union[AwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_cores: typing.Optional[jsii.Number] = None,
    cluster_memory_mb: typing.Optional[jsii.Number] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    cluster_source: typing.Optional[builtins.str] = None,
    creator_user_name: typing.Optional[builtins.str] = None,
    custom_tags: typing.Any = None,
    default_tags: typing.Optional[typing.Union[CfnClusterPropsDefaultTags, typing.Dict[builtins.str, typing.Any]]] = None,
    driver: typing.Any = None,
    driver_instance_pool_id: typing.Optional[builtins.str] = None,
    driver_instance_source: typing.Optional[typing.Union[CfnClusterPropsDriverInstanceSource, typing.Dict[builtins.str, typing.Any]]] = None,
    driver_node_type_id: typing.Optional[builtins.str] = None,
    effective_spark_version: typing.Optional[builtins.str] = None,
    enable_elastic_disk: typing.Optional[builtins.bool] = None,
    enable_local_disk_encryption: typing.Optional[builtins.bool] = None,
    idempotency_token: typing.Optional[builtins.str] = None,
    init_scripts: typing.Optional[typing.Sequence[typing.Union[InitScriptsListItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_pool_id: typing.Optional[builtins.str] = None,
    instance_source: typing.Optional[typing.Union[CfnClusterPropsInstanceSource, typing.Dict[builtins.str, typing.Any]]] = None,
    node_type_id: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    runtime_engine: typing.Optional[builtins.str] = None,
    spark_conf: typing.Any = None,
    spark_env_vars: typing.Any = None,
    spark_version: typing.Optional[builtins.str] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f650b2e7718c1b77942561e86fa647b4da4df8a9d793ba217e635d4a81671ce(
    *,
    apply_policy_default_values: typing.Optional[builtins.bool] = None,
    autoscale: typing.Optional[typing.Union[Autoscale, typing.Dict[builtins.str, typing.Any]]] = None,
    autotermination_minutes: typing.Optional[jsii.Number] = None,
    aws_attributes: typing.Optional[typing.Union[AwsAttributes, typing.Dict[builtins.str, typing.Any]]] = None,
    cluster_cores: typing.Optional[jsii.Number] = None,
    cluster_memory_mb: typing.Optional[jsii.Number] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    cluster_source: typing.Optional[builtins.str] = None,
    creator_user_name: typing.Optional[builtins.str] = None,
    custom_tags: typing.Any = None,
    default_tags: typing.Optional[typing.Union[CfnClusterPropsDefaultTags, typing.Dict[builtins.str, typing.Any]]] = None,
    driver: typing.Any = None,
    driver_instance_pool_id: typing.Optional[builtins.str] = None,
    driver_instance_source: typing.Optional[typing.Union[CfnClusterPropsDriverInstanceSource, typing.Dict[builtins.str, typing.Any]]] = None,
    driver_node_type_id: typing.Optional[builtins.str] = None,
    effective_spark_version: typing.Optional[builtins.str] = None,
    enable_elastic_disk: typing.Optional[builtins.bool] = None,
    enable_local_disk_encryption: typing.Optional[builtins.bool] = None,
    idempotency_token: typing.Optional[builtins.str] = None,
    init_scripts: typing.Optional[typing.Sequence[typing.Union[InitScriptsListItem, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_pool_id: typing.Optional[builtins.str] = None,
    instance_source: typing.Optional[typing.Union[CfnClusterPropsInstanceSource, typing.Dict[builtins.str, typing.Any]]] = None,
    node_type_id: typing.Optional[builtins.str] = None,
    num_workers: typing.Optional[jsii.Number] = None,
    runtime_engine: typing.Optional[builtins.str] = None,
    spark_conf: typing.Any = None,
    spark_env_vars: typing.Any = None,
    spark_version: typing.Optional[builtins.str] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d6c79c17a187fb11ed59ca4a45d0f56e5d9eac554aa3532e4815702fb61e32(
    *,
    cluster_id: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    creator: typing.Optional[builtins.str] = None,
    vendor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7480ebe33a81c7ca7c6390a833b769f6d8c2374d5429150837eb33dcc9e4e5(
    *,
    instance_pool_id: typing.Optional[builtins.str] = None,
    node_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ea7c4a7bb422f959b7d3d4094b52c6b81cdcda5711f2d5a41fe56983330f50(
    *,
    instance_pool_id: typing.Optional[builtins.str] = None,
    node_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c388acafb18ce256355a22a175059dcba1bebe0f8fab958b9a52a76e44fe11(
    *,
    s3: typing.Optional[typing.Union[S3Destination, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60a48606074181b7d9145dc424623948956aca28558a35d8e25c2f08b2a6a76(
    *,
    destination: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
