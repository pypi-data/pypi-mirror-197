'''
# databricks-clusters-job

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Databricks::Clusters::Job` v1.1.0.

## Description

Manage Jobs running on a cluster

## References

* [Documentation](https://github.com/aws-ia/cloudformation-databricks-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-databricks-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Databricks::Clusters::Job \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Databricks-Clusters-Job \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Databricks::Clusters::Job`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdatabricks-clusters-job+v1.1.0).
* Issues related to `Databricks::Clusters::Job` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-databricks-resource-providers).

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
    jsii_type="@cdk-cloudformation/databricks-clusters-job.AccessUser",
    jsii_struct_bases=[],
    name_mapping={"permission_level": "permissionLevel", "user_name": "userName"},
)
class AccessUser:
    def __init__(
        self,
        *,
        permission_level: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param permission_level: 
        :param user_name: 

        :schema: AccessUser
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25331c9fafd642e6165e7b9e21a75a42b12a090a059d7817dacb8afe3e80afd9)
            check_type(argname="argument permission_level", value=permission_level, expected_type=type_hints["permission_level"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if permission_level is not None:
            self._values["permission_level"] = permission_level
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def permission_level(self) -> typing.Optional[builtins.str]:
        '''
        :schema: AccessUser#PermissionLevel
        '''
        result = self._values.get("permission_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: AccessUser#UserName
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CfnJob(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/databricks-clusters-job.CfnJob",
):
    '''A CloudFormation ``Databricks::Clusters::Job``.

    :cloudformationResource: Databricks::Clusters::Job
    :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_control_list: typing.Optional[typing.Sequence[typing.Union[AccessUser, typing.Dict[builtins.str, typing.Any]]]] = None,
        creator_user_name: typing.Optional[builtins.str] = None,
        email_notifications: typing.Optional[typing.Union["EmailNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        existing_cluster_id: typing.Optional[builtins.str] = None,
        format: typing.Optional["CfnJobPropsFormat"] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        run_as_owner: typing.Optional[builtins.bool] = None,
        run_as_user_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["Schedule", typing.Dict[builtins.str, typing.Any]]] = None,
        settings: typing.Any = None,
        tags: typing.Any = None,
        tasks: typing.Optional[typing.Sequence[typing.Union["Task", typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Databricks::Clusters::Job``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_control_list: List of permissions to set on the job.
        :param creator_user_name: 
        :param email_notifications: 
        :param existing_cluster_id: If existing_cluster_id, the ID of an existing cluster that is used for all runs of this task. When running tasks on an existing cluster, you may need to manually restart the cluster if it stops responding. We suggest running jobs on new clusters for greater reliability.
        :param format: Used to tell what is the format of the job. This field is ignored in Create/Update/Reset calls. When using the Jobs API 2.1 this value is always set to "MULTI_TASK".
        :param max_concurrent_runs: An optional maximum allowed number of concurrent runs of the job. Set this value if you want to be able to execute multiple runs of the same job concurrently. This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters. This setting affects only new runs. For example, suppose the job's concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won't kill any of the active runs. However, from then on, new runs are skipped unless there are fewer than 3 active runs. This value cannot exceed 1000. Setting this value to 0 causes all new runs to be skipped. The default behavior is to allow only 1 concurrent run.
        :param name: An optional name for the job.
        :param run_as_owner: 
        :param run_as_user_name: 
        :param schedule: 
        :param settings: 
        :param tags: A map of tags associated with the job. These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.
        :param tasks: A list of task specifications to be executed by this job.
        :param timeout_seconds: An optional timeout applied to each run of this job. The default behavior is to have no timeout.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c681b98b0f7d35a1a9e2c6a90490fa0431368cfdb20880507fd1e173c12e643d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnJobProps(
            access_control_list=access_control_list,
            creator_user_name=creator_user_name,
            email_notifications=email_notifications,
            existing_cluster_id=existing_cluster_id,
            format=format,
            max_concurrent_runs=max_concurrent_runs,
            name=name,
            run_as_owner=run_as_owner,
            run_as_user_name=run_as_user_name,
            schedule=schedule,
            settings=settings,
            tags=tags,
            tasks=tasks,
            timeout_seconds=timeout_seconds,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> jsii.Number:
        '''Attribute ``Databricks::Clusters::Job.CreatedTime``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrJobId")
    def attr_job_id(self) -> jsii.Number:
        '''Attribute ``Databricks::Clusters::Job.JobId``.

        :link: https://github.com/aws-ia/cloudformation-databricks-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrJobId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnJobProps":
        '''Resource props.'''
        return typing.cast("CfnJobProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.CfnJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_list": "accessControlList",
        "creator_user_name": "creatorUserName",
        "email_notifications": "emailNotifications",
        "existing_cluster_id": "existingClusterId",
        "format": "format",
        "max_concurrent_runs": "maxConcurrentRuns",
        "name": "name",
        "run_as_owner": "runAsOwner",
        "run_as_user_name": "runAsUserName",
        "schedule": "schedule",
        "settings": "settings",
        "tags": "tags",
        "tasks": "tasks",
        "timeout_seconds": "timeoutSeconds",
    },
)
class CfnJobProps:
    def __init__(
        self,
        *,
        access_control_list: typing.Optional[typing.Sequence[typing.Union[AccessUser, typing.Dict[builtins.str, typing.Any]]]] = None,
        creator_user_name: typing.Optional[builtins.str] = None,
        email_notifications: typing.Optional[typing.Union["EmailNotifications", typing.Dict[builtins.str, typing.Any]]] = None,
        existing_cluster_id: typing.Optional[builtins.str] = None,
        format: typing.Optional["CfnJobPropsFormat"] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        run_as_owner: typing.Optional[builtins.bool] = None,
        run_as_user_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["Schedule", typing.Dict[builtins.str, typing.Any]]] = None,
        settings: typing.Any = None,
        tags: typing.Any = None,
        tasks: typing.Optional[typing.Sequence[typing.Union["Task", typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manage Jobs running on a cluster.

        :param access_control_list: List of permissions to set on the job.
        :param creator_user_name: 
        :param email_notifications: 
        :param existing_cluster_id: If existing_cluster_id, the ID of an existing cluster that is used for all runs of this task. When running tasks on an existing cluster, you may need to manually restart the cluster if it stops responding. We suggest running jobs on new clusters for greater reliability.
        :param format: Used to tell what is the format of the job. This field is ignored in Create/Update/Reset calls. When using the Jobs API 2.1 this value is always set to "MULTI_TASK".
        :param max_concurrent_runs: An optional maximum allowed number of concurrent runs of the job. Set this value if you want to be able to execute multiple runs of the same job concurrently. This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters. This setting affects only new runs. For example, suppose the job's concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won't kill any of the active runs. However, from then on, new runs are skipped unless there are fewer than 3 active runs. This value cannot exceed 1000. Setting this value to 0 causes all new runs to be skipped. The default behavior is to allow only 1 concurrent run.
        :param name: An optional name for the job.
        :param run_as_owner: 
        :param run_as_user_name: 
        :param schedule: 
        :param settings: 
        :param tags: A map of tags associated with the job. These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.
        :param tasks: A list of task specifications to be executed by this job.
        :param timeout_seconds: An optional timeout applied to each run of this job. The default behavior is to have no timeout.

        :schema: CfnJobProps
        '''
        if isinstance(email_notifications, dict):
            email_notifications = EmailNotifications(**email_notifications)
        if isinstance(schedule, dict):
            schedule = Schedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a9cf8391a22be3d77d6872a04c975b72ea9a4916efe0b716bee330b9df834b)
            check_type(argname="argument access_control_list", value=access_control_list, expected_type=type_hints["access_control_list"])
            check_type(argname="argument creator_user_name", value=creator_user_name, expected_type=type_hints["creator_user_name"])
            check_type(argname="argument email_notifications", value=email_notifications, expected_type=type_hints["email_notifications"])
            check_type(argname="argument existing_cluster_id", value=existing_cluster_id, expected_type=type_hints["existing_cluster_id"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument run_as_owner", value=run_as_owner, expected_type=type_hints["run_as_owner"])
            check_type(argname="argument run_as_user_name", value=run_as_user_name, expected_type=type_hints["run_as_user_name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tasks", value=tasks, expected_type=type_hints["tasks"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_control_list is not None:
            self._values["access_control_list"] = access_control_list
        if creator_user_name is not None:
            self._values["creator_user_name"] = creator_user_name
        if email_notifications is not None:
            self._values["email_notifications"] = email_notifications
        if existing_cluster_id is not None:
            self._values["existing_cluster_id"] = existing_cluster_id
        if format is not None:
            self._values["format"] = format
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if name is not None:
            self._values["name"] = name
        if run_as_owner is not None:
            self._values["run_as_owner"] = run_as_owner
        if run_as_user_name is not None:
            self._values["run_as_user_name"] = run_as_user_name
        if schedule is not None:
            self._values["schedule"] = schedule
        if settings is not None:
            self._values["settings"] = settings
        if tags is not None:
            self._values["tags"] = tags
        if tasks is not None:
            self._values["tasks"] = tasks
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def access_control_list(self) -> typing.Optional[typing.List[AccessUser]]:
        '''List of permissions to set on the job.

        :schema: CfnJobProps#AccessControlList
        '''
        result = self._values.get("access_control_list")
        return typing.cast(typing.Optional[typing.List[AccessUser]], result)

    @builtins.property
    def creator_user_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnJobProps#CreatorUserName
        '''
        result = self._values.get("creator_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_notifications(self) -> typing.Optional["EmailNotifications"]:
        '''
        :schema: CfnJobProps#EmailNotifications
        '''
        result = self._values.get("email_notifications")
        return typing.cast(typing.Optional["EmailNotifications"], result)

    @builtins.property
    def existing_cluster_id(self) -> typing.Optional[builtins.str]:
        '''If existing_cluster_id, the ID of an existing cluster that is used for all runs of this task.

        When running tasks on an existing cluster, you may need to manually restart the cluster if it stops responding. We suggest running jobs on new clusters for greater reliability.

        :schema: CfnJobProps#ExistingClusterId
        '''
        result = self._values.get("existing_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format(self) -> typing.Optional["CfnJobPropsFormat"]:
        '''Used to tell what is the format of the job.

        This field is ignored in Create/Update/Reset calls. When using the Jobs API 2.1 this value is always set to "MULTI_TASK".

        :schema: CfnJobProps#Format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional["CfnJobPropsFormat"], result)

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''An optional maximum allowed number of concurrent runs of the job.

        Set this value if you want to be able to execute multiple runs of the same job concurrently. This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters.

        This setting affects only new runs. For example, suppose the job's concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won't kill any of the active runs. However, from then on, new runs are skipped unless there are fewer than 3 active runs.

        This value cannot exceed 1000. Setting this value to 0 causes all new runs to be skipped. The default behavior is to allow only 1 concurrent run.

        :schema: CfnJobProps#MaxConcurrentRuns
        '''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''An optional name for the job.

        :schema: CfnJobProps#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_as_owner(self) -> typing.Optional[builtins.bool]:
        '''
        :schema: CfnJobProps#RunAsOwner
        '''
        result = self._values.get("run_as_owner")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def run_as_user_name(self) -> typing.Optional[builtins.str]:
        '''
        :schema: CfnJobProps#RunAsUserName
        '''
        result = self._values.get("run_as_user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        '''
        :schema: CfnJobProps#Schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["Schedule"], result)

    @builtins.property
    def settings(self) -> typing.Any:
        '''
        :schema: CfnJobProps#Settings
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''A map of tags associated with the job.

        These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.

        :schema: CfnJobProps#Tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tasks(self) -> typing.Optional[typing.List["Task"]]:
        '''A list of task specifications to be executed by this job.

        :schema: CfnJobProps#Tasks
        '''
        result = self._values.get("tasks")
        return typing.cast(typing.Optional[typing.List["Task"]], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''An optional timeout applied to each run of this job.

        The default behavior is to have no timeout.

        :schema: CfnJobProps#TimeoutSeconds
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/databricks-clusters-job.CfnJobPropsFormat")
class CfnJobPropsFormat(enum.Enum):
    '''Used to tell what is the format of the job.

    This field is ignored in Create/Update/Reset calls. When using the Jobs API 2.1 this value is always set to "MULTI_TASK".

    :schema: CfnJobPropsFormat
    '''

    SINGLE_TASK = "SINGLE_TASK"
    '''SINGLE_TASK.'''
    MULTI_TASK = "MULTI_TASK"
    '''MULTI_TASK.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.EmailNotifications",
    jsii_struct_bases=[],
    name_mapping={
        "no_alert_for_skipped_runs": "noAlertForSkippedRuns",
        "on_failure": "onFailure",
        "on_start": "onStart",
        "on_success": "onSuccess",
    },
)
class EmailNotifications:
    def __init__(
        self,
        *,
        no_alert_for_skipped_runs: typing.Optional[builtins.bool] = None,
        on_failure: typing.Optional[typing.Sequence[builtins.str]] = None,
        on_start: typing.Optional[typing.Sequence[builtins.str]] = None,
        on_success: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param no_alert_for_skipped_runs: If true, do not send email to recipients specified in on_failure if the run is skipped.
        :param on_failure: A list of email addresses to be notified when a run unsuccessfully completes. A run is considered to have completed unsuccessfully if it ends with an INTERNAL_ERROR life_cycle_state or a SKIPPED, FAILED, or TIMED_OUT result_state. If this is not specified on job creation, reset, or update the list is empty, and notifications are not sent.
        :param on_start: A list of email addresses to be notified when a run begins. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
        :param on_success: A list of email addresses to be notified when a run successfully completes. A run is considered to have completed successfully if it ends with a TERMINATED life_cycle_state and a SUCCESSFUL result_state. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.

        :schema: EmailNotifications
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450d234383fdb2b989d1de12e3b6f6553b271911dc58645ab0dfb84909cf85f6)
            check_type(argname="argument no_alert_for_skipped_runs", value=no_alert_for_skipped_runs, expected_type=type_hints["no_alert_for_skipped_runs"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_start", value=on_start, expected_type=type_hints["on_start"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if no_alert_for_skipped_runs is not None:
            self._values["no_alert_for_skipped_runs"] = no_alert_for_skipped_runs
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_start is not None:
            self._values["on_start"] = on_start
        if on_success is not None:
            self._values["on_success"] = on_success

    @builtins.property
    def no_alert_for_skipped_runs(self) -> typing.Optional[builtins.bool]:
        '''If true, do not send email to recipients specified in on_failure if the run is skipped.

        :schema: EmailNotifications#NoAlertForSkippedRuns
        '''
        result = self._values.get("no_alert_for_skipped_runs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of email addresses to be notified when a run unsuccessfully completes.

        A run is considered to have completed unsuccessfully if it ends with an INTERNAL_ERROR life_cycle_state or a SKIPPED, FAILED, or TIMED_OUT result_state. If this is not specified on job creation, reset, or update the list is empty, and notifications are not sent.

        :schema: EmailNotifications#OnFailure
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def on_start(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of email addresses to be notified when a run begins.

        If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.

        :schema: EmailNotifications#OnStart
        '''
        result = self._values.get("on_start")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def on_success(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of email addresses to be notified when a run successfully completes.

        A run is considered to have completed successfully if it ends with a TERMINATED life_cycle_state and a SUCCESSFUL result_state. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.

        :schema: EmailNotifications#OnSuccess
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailNotifications(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.Schedule",
    jsii_struct_bases=[],
    name_mapping={
        "pause_status": "pauseStatus",
        "quartz_cron_expression": "quartzCronExpression",
        "timezone_id": "timezoneId",
    },
)
class Schedule:
    def __init__(
        self,
        *,
        pause_status: typing.Optional["SchedulePauseStatus"] = None,
        quartz_cron_expression: typing.Optional[builtins.str] = None,
        timezone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pause_status: Indicate whether this schedule is paused or not.
        :param quartz_cron_expression: A Cron expression using Quartz syntax that describes the schedule for a job. See Cron Trigger for details. This field is required.
        :param timezone_id: A Java timezone ID. The schedule for a job is resolved with respect to this timezone. See Java TimeZone for details. This field is required.

        :schema: Schedule
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e04ba3dcce43462d5f40ecc65a527ef384b95972bea182f3689de11b177158f)
            check_type(argname="argument pause_status", value=pause_status, expected_type=type_hints["pause_status"])
            check_type(argname="argument quartz_cron_expression", value=quartz_cron_expression, expected_type=type_hints["quartz_cron_expression"])
            check_type(argname="argument timezone_id", value=timezone_id, expected_type=type_hints["timezone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pause_status is not None:
            self._values["pause_status"] = pause_status
        if quartz_cron_expression is not None:
            self._values["quartz_cron_expression"] = quartz_cron_expression
        if timezone_id is not None:
            self._values["timezone_id"] = timezone_id

    @builtins.property
    def pause_status(self) -> typing.Optional["SchedulePauseStatus"]:
        '''Indicate whether this schedule is paused or not.

        :schema: Schedule#PauseStatus
        '''
        result = self._values.get("pause_status")
        return typing.cast(typing.Optional["SchedulePauseStatus"], result)

    @builtins.property
    def quartz_cron_expression(self) -> typing.Optional[builtins.str]:
        '''A Cron expression using Quartz syntax that describes the schedule for a job.

        See Cron Trigger for details. This field is required.

        :schema: Schedule#QuartzCronExpression
        '''
        result = self._values.get("quartz_cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone_id(self) -> typing.Optional[builtins.str]:
        '''A Java timezone ID.

        The schedule for a job is resolved with respect to this timezone. See Java TimeZone for details. This field is required.

        :schema: Schedule#TimezoneId
        '''
        result = self._values.get("timezone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Schedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/databricks-clusters-job.SchedulePauseStatus")
class SchedulePauseStatus(enum.Enum):
    '''Indicate whether this schedule is paused or not.

    :schema: SchedulePauseStatus
    '''

    PAUSED = "PAUSED"
    '''PAUSED.'''
    UNPAUSED = "UNPAUSED"
    '''UNPAUSED.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.Task",
    jsii_struct_bases=[],
    name_mapping={
        "task_key": "taskKey",
        "depends_on": "dependsOn",
        "description": "description",
        "email_notifications": "emailNotifications",
        "existing_cluster_id": "existingClusterId",
        "libraries": "libraries",
        "max_retries": "maxRetries",
        "min_retry_interval_millies": "minRetryIntervalMillies",
        "notebook_task": "notebookTask",
        "pipeline_task": "pipelineTask",
        "python_wheel_task": "pythonWheelTask",
        "retry_on_timeout": "retryOnTimeout",
        "spark_jar_task": "sparkJarTask",
        "spark_python_task": "sparkPythonTask",
        "spark_submit_task": "sparkSubmitTask",
        "timeout_seconds": "timeoutSeconds",
    },
)
class Task:
    def __init__(
        self,
        *,
        task_key: builtins.str,
        depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        email_notifications: typing.Optional[typing.Union[EmailNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
        existing_cluster_id: typing.Optional[builtins.str] = None,
        libraries: typing.Optional[typing.Sequence[typing.Any]] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        min_retry_interval_millies: typing.Optional[jsii.Number] = None,
        notebook_task: typing.Optional[typing.Union["TaskNotebookTask", typing.Dict[builtins.str, typing.Any]]] = None,
        pipeline_task: typing.Optional[typing.Union["TaskPipelineTask", typing.Dict[builtins.str, typing.Any]]] = None,
        python_wheel_task: typing.Optional[typing.Union["TaskPythonWheelTask", typing.Dict[builtins.str, typing.Any]]] = None,
        retry_on_timeout: typing.Optional[builtins.bool] = None,
        spark_jar_task: typing.Optional[typing.Union["TaskSparkJarTask", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_python_task: typing.Optional[typing.Union["TaskSparkPythonTask", typing.Dict[builtins.str, typing.Any]]] = None,
        spark_submit_task: typing.Optional[typing.Union["TaskSparkSubmitTask", typing.Dict[builtins.str, typing.Any]]] = None,
        timeout_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param task_key: A unique name for the task. This field is used to refer to this task from other tasks. This field is required and must be unique within its parent job. On Update or Reset, this field is used to reference the tasks to be updated or reset. The maximum length is 100 characters.
        :param depends_on: An optional array of objects specifying the dependency graph of the task. All tasks specified in this field must complete successfully before executing this task. The key is task_key, and the value is the name assigned to the dependent task. This field is required when a job consists of more than one task.
        :param description: An optional description for this task. The maximum length is 4096 bytes.
        :param email_notifications: 
        :param existing_cluster_id: If existing_cluster_id, the ID of an existing cluster that is used for all runs of this task. When running tasks on an existing cluster, you may need to manually restart the cluster if it stops responding. We suggest running jobs on new clusters for greater reliability.
        :param libraries: An optional list of libraries to be installed on the cluster that executes the task. The default value is an empty list.
        :param max_retries: An optional maximum number of times to retry an unsuccessful run. A run is considered to be unsuccessful if it completes with the FAILED result_state or INTERNAL_ERROR life_cycle_state. The value -1 means to retry indefinitely and the value 0 means to never retry. The default behavior is to never retry.
        :param min_retry_interval_millies: An optional minimal interval in milliseconds between the start of the failed run and the subsequent retry run. The default behavior is that unsuccessful runs are immediately retried.
        :param notebook_task: 
        :param pipeline_task: 
        :param python_wheel_task: 
        :param retry_on_timeout: An optional policy to specify whether to retry a task when it times out. The default behavior is to not retry on timeout.
        :param spark_jar_task: 
        :param spark_python_task: 
        :param spark_submit_task: 
        :param timeout_seconds: An optional timeout applied to each run of this job task. The default behavior is to have no timeout.

        :schema: Task
        '''
        if isinstance(email_notifications, dict):
            email_notifications = EmailNotifications(**email_notifications)
        if isinstance(notebook_task, dict):
            notebook_task = TaskNotebookTask(**notebook_task)
        if isinstance(pipeline_task, dict):
            pipeline_task = TaskPipelineTask(**pipeline_task)
        if isinstance(python_wheel_task, dict):
            python_wheel_task = TaskPythonWheelTask(**python_wheel_task)
        if isinstance(spark_jar_task, dict):
            spark_jar_task = TaskSparkJarTask(**spark_jar_task)
        if isinstance(spark_python_task, dict):
            spark_python_task = TaskSparkPythonTask(**spark_python_task)
        if isinstance(spark_submit_task, dict):
            spark_submit_task = TaskSparkSubmitTask(**spark_submit_task)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__622ecd1526c16b235559620603f9da7c71e1da1e11f4c4c7b6c71bcd0e0c7d59)
            check_type(argname="argument task_key", value=task_key, expected_type=type_hints["task_key"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument email_notifications", value=email_notifications, expected_type=type_hints["email_notifications"])
            check_type(argname="argument existing_cluster_id", value=existing_cluster_id, expected_type=type_hints["existing_cluster_id"])
            check_type(argname="argument libraries", value=libraries, expected_type=type_hints["libraries"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument min_retry_interval_millies", value=min_retry_interval_millies, expected_type=type_hints["min_retry_interval_millies"])
            check_type(argname="argument notebook_task", value=notebook_task, expected_type=type_hints["notebook_task"])
            check_type(argname="argument pipeline_task", value=pipeline_task, expected_type=type_hints["pipeline_task"])
            check_type(argname="argument python_wheel_task", value=python_wheel_task, expected_type=type_hints["python_wheel_task"])
            check_type(argname="argument retry_on_timeout", value=retry_on_timeout, expected_type=type_hints["retry_on_timeout"])
            check_type(argname="argument spark_jar_task", value=spark_jar_task, expected_type=type_hints["spark_jar_task"])
            check_type(argname="argument spark_python_task", value=spark_python_task, expected_type=type_hints["spark_python_task"])
            check_type(argname="argument spark_submit_task", value=spark_submit_task, expected_type=type_hints["spark_submit_task"])
            check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_key": task_key,
        }
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if description is not None:
            self._values["description"] = description
        if email_notifications is not None:
            self._values["email_notifications"] = email_notifications
        if existing_cluster_id is not None:
            self._values["existing_cluster_id"] = existing_cluster_id
        if libraries is not None:
            self._values["libraries"] = libraries
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if min_retry_interval_millies is not None:
            self._values["min_retry_interval_millies"] = min_retry_interval_millies
        if notebook_task is not None:
            self._values["notebook_task"] = notebook_task
        if pipeline_task is not None:
            self._values["pipeline_task"] = pipeline_task
        if python_wheel_task is not None:
            self._values["python_wheel_task"] = python_wheel_task
        if retry_on_timeout is not None:
            self._values["retry_on_timeout"] = retry_on_timeout
        if spark_jar_task is not None:
            self._values["spark_jar_task"] = spark_jar_task
        if spark_python_task is not None:
            self._values["spark_python_task"] = spark_python_task
        if spark_submit_task is not None:
            self._values["spark_submit_task"] = spark_submit_task
        if timeout_seconds is not None:
            self._values["timeout_seconds"] = timeout_seconds

    @builtins.property
    def task_key(self) -> builtins.str:
        '''A unique name for the task.

        This field is used to refer to this task from other tasks. This field is required and must be unique within its parent job. On Update or Reset, this field is used to reference the tasks to be updated or reset. The maximum length is 100 characters.

        :schema: Task#TaskKey
        '''
        result = self._values.get("task_key")
        assert result is not None, "Required property 'task_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An optional array of objects specifying the dependency graph of the task.

        All tasks specified in this field must complete successfully before executing this task. The key is task_key, and the value is the name assigned to the dependent task. This field is required when a job consists of more than one task.

        :schema: Task#DependsOn
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this task.

        The maximum length is 4096 bytes.

        :schema: Task#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_notifications(self) -> typing.Optional[EmailNotifications]:
        '''
        :schema: Task#EmailNotifications
        '''
        result = self._values.get("email_notifications")
        return typing.cast(typing.Optional[EmailNotifications], result)

    @builtins.property
    def existing_cluster_id(self) -> typing.Optional[builtins.str]:
        '''If existing_cluster_id, the ID of an existing cluster that is used for all runs of this task.

        When running tasks on an existing cluster, you may need to manually restart the cluster if it stops responding. We suggest running jobs on new clusters for greater reliability.

        :schema: Task#ExistingClusterId
        '''
        result = self._values.get("existing_cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def libraries(self) -> typing.Optional[typing.List[typing.Any]]:
        '''An optional list of libraries to be installed on the cluster that executes the task.

        The default value is an empty list.

        :schema: Task#Libraries
        '''
        result = self._values.get("libraries")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''An optional maximum number of times to retry an unsuccessful run.

        A run is considered to be unsuccessful if it completes with the FAILED result_state or INTERNAL_ERROR life_cycle_state. The value -1 means to retry indefinitely and the value 0 means to never retry. The default behavior is to never retry.

        :schema: Task#MaxRetries
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_retry_interval_millies(self) -> typing.Optional[jsii.Number]:
        '''An optional minimal interval in milliseconds between the start of the failed run and the subsequent retry run.

        The default behavior is that unsuccessful runs are immediately retried.

        :schema: Task#MinRetryIntervalMillies
        '''
        result = self._values.get("min_retry_interval_millies")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notebook_task(self) -> typing.Optional["TaskNotebookTask"]:
        '''
        :schema: Task#NotebookTask
        '''
        result = self._values.get("notebook_task")
        return typing.cast(typing.Optional["TaskNotebookTask"], result)

    @builtins.property
    def pipeline_task(self) -> typing.Optional["TaskPipelineTask"]:
        '''
        :schema: Task#PipelineTask
        '''
        result = self._values.get("pipeline_task")
        return typing.cast(typing.Optional["TaskPipelineTask"], result)

    @builtins.property
    def python_wheel_task(self) -> typing.Optional["TaskPythonWheelTask"]:
        '''
        :schema: Task#PythonWheelTask
        '''
        result = self._values.get("python_wheel_task")
        return typing.cast(typing.Optional["TaskPythonWheelTask"], result)

    @builtins.property
    def retry_on_timeout(self) -> typing.Optional[builtins.bool]:
        '''An optional policy to specify whether to retry a task when it times out.

        The default behavior is to not retry on timeout.

        :schema: Task#RetryOnTimeout
        '''
        result = self._values.get("retry_on_timeout")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def spark_jar_task(self) -> typing.Optional["TaskSparkJarTask"]:
        '''
        :schema: Task#SparkJarTask
        '''
        result = self._values.get("spark_jar_task")
        return typing.cast(typing.Optional["TaskSparkJarTask"], result)

    @builtins.property
    def spark_python_task(self) -> typing.Optional["TaskSparkPythonTask"]:
        '''
        :schema: Task#SparkPythonTask
        '''
        result = self._values.get("spark_python_task")
        return typing.cast(typing.Optional["TaskSparkPythonTask"], result)

    @builtins.property
    def spark_submit_task(self) -> typing.Optional["TaskSparkSubmitTask"]:
        '''
        :schema: Task#SparkSubmitTask
        '''
        result = self._values.get("spark_submit_task")
        return typing.cast(typing.Optional["TaskSparkSubmitTask"], result)

    @builtins.property
    def timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''An optional timeout applied to each run of this job task.

        The default behavior is to have no timeout.

        :schema: Task#TimeoutSeconds
        '''
        result = self._values.get("timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Task(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.TaskNotebookTask",
    jsii_struct_bases=[],
    name_mapping={
        "notebook_path": "notebookPath",
        "base_parameters": "baseParameters",
    },
)
class TaskNotebookTask:
    def __init__(
        self,
        *,
        notebook_path: builtins.str,
        base_parameters: typing.Any = None,
    ) -> None:
        '''
        :param notebook_path: The path of the notebook to be run in the Databricks workspace or remote repository. For notebooks stored in the Databricks workspace, the path must be absolute and begin with a slash. For notebooks stored in a remote repository, the path must be relative. This field is required.
        :param base_parameters: Base parameters to be used for each run of this job. If the run is initiated by a call to run-now with parameters specified, the two parameters maps are merged. If the same key is specified in base_parameters and in run-now, the value from run-now is used. Use Task parameter variables to set parameters containing information about job runs. If the notebook takes a parameter that is not specified in the job's base_parameters or the run-now override parameters, the default value from the notebook is used

        :schema: TaskNotebookTask
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf4348bf7077cd719d83343da78cf1706879866ba64f3cbf413d8b217aa7731)
            check_type(argname="argument notebook_path", value=notebook_path, expected_type=type_hints["notebook_path"])
            check_type(argname="argument base_parameters", value=base_parameters, expected_type=type_hints["base_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "notebook_path": notebook_path,
        }
        if base_parameters is not None:
            self._values["base_parameters"] = base_parameters

    @builtins.property
    def notebook_path(self) -> builtins.str:
        '''The path of the notebook to be run in the Databricks workspace or remote repository.

        For notebooks stored in the Databricks workspace, the path must be absolute and begin with a slash. For notebooks stored in a remote repository, the path must be relative. This field is required.

        :schema: TaskNotebookTask#NotebookPath
        '''
        result = self._values.get("notebook_path")
        assert result is not None, "Required property 'notebook_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base_parameters(self) -> typing.Any:
        '''Base parameters to be used for each run of this job.

        If the run is initiated by a call to run-now with parameters specified, the two parameters maps are merged. If the same key is specified in base_parameters and in run-now, the value from run-now is used.

        Use Task parameter variables to set parameters containing information about job runs.

        If the notebook takes a parameter that is not specified in the job's base_parameters or the run-now override parameters, the default value from the notebook is used

        :schema: TaskNotebookTask#BaseParameters
        '''
        result = self._values.get("base_parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskNotebookTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.TaskPipelineTask",
    jsii_struct_bases=[],
    name_mapping={"pipeline_id": "pipelineId", "full_refresh": "fullRefresh"},
)
class TaskPipelineTask:
    def __init__(
        self,
        *,
        pipeline_id: builtins.str,
        full_refresh: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param pipeline_id: The full name of the pipeline task to execute.
        :param full_refresh: If true, a full refresh will be triggered on the delta live table.

        :schema: TaskPipelineTask
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be07107027cd44ade61f9db9a68717eef80b5821fd5623d3775fd0b9e83a2e07)
            check_type(argname="argument pipeline_id", value=pipeline_id, expected_type=type_hints["pipeline_id"])
            check_type(argname="argument full_refresh", value=full_refresh, expected_type=type_hints["full_refresh"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pipeline_id": pipeline_id,
        }
        if full_refresh is not None:
            self._values["full_refresh"] = full_refresh

    @builtins.property
    def pipeline_id(self) -> builtins.str:
        '''The full name of the pipeline task to execute.

        :schema: TaskPipelineTask#PipelineId
        '''
        result = self._values.get("pipeline_id")
        assert result is not None, "Required property 'pipeline_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def full_refresh(self) -> typing.Optional[builtins.bool]:
        '''If true, a full refresh will be triggered on the delta live table.

        :schema: TaskPipelineTask#FullRefresh
        '''
        result = self._values.get("full_refresh")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskPipelineTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.TaskPythonWheelTask",
    jsii_struct_bases=[],
    name_mapping={
        "package_name": "packageName",
        "entry_point": "entryPoint",
        "named_parameters": "namedParameters",
        "parameters": "parameters",
    },
)
class TaskPythonWheelTask:
    def __init__(
        self,
        *,
        package_name: builtins.str,
        entry_point: typing.Optional[builtins.str] = None,
        named_parameters: typing.Any = None,
        parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param package_name: Name of the package to execute.
        :param entry_point: Named entry point to use, if it does not exist in the metadata of the package it executes the function from the package directly using $packageName.$entryPoint().
        :param named_parameters: Command-line parameters passed to Python wheel task in the form of ["--name=task", "--data=dbfs:/path/to/data.json"]. Leave it empty if parameters is not null.
        :param parameters: Command-line parameters passed to Python wheel task. Leave it empty if named_parameters is not null.

        :schema: TaskPythonWheelTask
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2582be32d5cc12550bf6609f119b046a8a5e9aa2cf5a2ed3af169e7b184bfbc)
            check_type(argname="argument package_name", value=package_name, expected_type=type_hints["package_name"])
            check_type(argname="argument entry_point", value=entry_point, expected_type=type_hints["entry_point"])
            check_type(argname="argument named_parameters", value=named_parameters, expected_type=type_hints["named_parameters"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "package_name": package_name,
        }
        if entry_point is not None:
            self._values["entry_point"] = entry_point
        if named_parameters is not None:
            self._values["named_parameters"] = named_parameters
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def package_name(self) -> builtins.str:
        '''Name of the package to execute.

        :schema: TaskPythonWheelTask#PackageName
        '''
        result = self._values.get("package_name")
        assert result is not None, "Required property 'package_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entry_point(self) -> typing.Optional[builtins.str]:
        '''Named entry point to use, if it does not exist in the metadata of the package it executes the function from the package directly using $packageName.$entryPoint().

        :schema: TaskPythonWheelTask#EntryPoint
        '''
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def named_parameters(self) -> typing.Any:
        '''Command-line parameters passed to Python wheel task in the form of ["--name=task", "--data=dbfs:/path/to/data.json"]. Leave it empty if parameters is not null.

        :schema: TaskPythonWheelTask#NamedParameters
        '''
        result = self._values.get("named_parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Command-line parameters passed to Python wheel task.

        Leave it empty if named_parameters is not null.

        :schema: TaskPythonWheelTask#Parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskPythonWheelTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.TaskSparkJarTask",
    jsii_struct_bases=[],
    name_mapping={"main_class_name": "mainClassName", "parameters": "parameters"},
)
class TaskSparkJarTask:
    def __init__(
        self,
        *,
        main_class_name: builtins.str,
        parameters: typing.Any = None,
    ) -> None:
        '''
        :param main_class_name: The full name of the class containing the main method to be executed. This class must be contained in a JAR provided as a library.
        :param parameters: Parameters passed to the main method. Use Task parameter variables to set parameters containing information about job runs.

        :schema: TaskSparkJarTask
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e29e5f60db7136380d8ed8d443e0824ba7cf73e24ba17500ee376fbb599a38)
            check_type(argname="argument main_class_name", value=main_class_name, expected_type=type_hints["main_class_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "main_class_name": main_class_name,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def main_class_name(self) -> builtins.str:
        '''The full name of the class containing the main method to be executed.

        This class must be contained in a JAR provided as a library.

        :schema: TaskSparkJarTask#MainClassName
        '''
        result = self._values.get("main_class_name")
        assert result is not None, "Required property 'main_class_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Parameters passed to the main method.

        Use Task parameter variables to set parameters containing information about job runs.

        :schema: TaskSparkJarTask#Parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskSparkJarTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.TaskSparkPythonTask",
    jsii_struct_bases=[],
    name_mapping={"python_file": "pythonFile", "parameters": "parameters"},
)
class TaskSparkPythonTask:
    def __init__(
        self,
        *,
        python_file: builtins.str,
        parameters: typing.Any = None,
    ) -> None:
        '''
        :param python_file: The URI of the Python file to be executed. DBFS and S3 paths are supported. This field is required.
        :param parameters: Command line parameters passed to the Python file. Use Task parameter variables to set parameters containing information about job runs.

        :schema: TaskSparkPythonTask
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcaee6fea82effa1267547c315bbf8064b8f67a1fb3086d40e6b962e4c1e6f41)
            check_type(argname="argument python_file", value=python_file, expected_type=type_hints["python_file"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "python_file": python_file,
        }
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def python_file(self) -> builtins.str:
        '''The URI of the Python file to be executed.

        DBFS and S3 paths are supported. This field is required.

        :schema: TaskSparkPythonTask#PythonFile
        '''
        result = self._values.get("python_file")
        assert result is not None, "Required property 'python_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Command line parameters passed to the Python file.

        Use Task parameter variables to set parameters containing information about job runs.

        :schema: TaskSparkPythonTask#Parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskSparkPythonTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/databricks-clusters-job.TaskSparkSubmitTask",
    jsii_struct_bases=[],
    name_mapping={"parameters": "parameters"},
)
class TaskSparkSubmitTask:
    def __init__(self, *, parameters: typing.Any = None) -> None:
        '''
        :param parameters: Command-line parameters passed to spark submit. Use Task parameter variables to set parameters containing information about job runs.

        :schema: TaskSparkSubmitTask
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26abd145b33e49408f481fcdb45fd061a3889149f1e6f5e6eb2af03306bc33a)
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Command-line parameters passed to spark submit.

        Use Task parameter variables to set parameters containing information about job runs.

        :schema: TaskSparkSubmitTask#Parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskSparkSubmitTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessUser",
    "CfnJob",
    "CfnJobProps",
    "CfnJobPropsFormat",
    "EmailNotifications",
    "Schedule",
    "SchedulePauseStatus",
    "Task",
    "TaskNotebookTask",
    "TaskPipelineTask",
    "TaskPythonWheelTask",
    "TaskSparkJarTask",
    "TaskSparkPythonTask",
    "TaskSparkSubmitTask",
]

publication.publish()

def _typecheckingstub__25331c9fafd642e6165e7b9e21a75a42b12a090a059d7817dacb8afe3e80afd9(
    *,
    permission_level: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c681b98b0f7d35a1a9e2c6a90490fa0431368cfdb20880507fd1e173c12e643d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_control_list: typing.Optional[typing.Sequence[typing.Union[AccessUser, typing.Dict[builtins.str, typing.Any]]]] = None,
    creator_user_name: typing.Optional[builtins.str] = None,
    email_notifications: typing.Optional[typing.Union[EmailNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_cluster_id: typing.Optional[builtins.str] = None,
    format: typing.Optional[CfnJobPropsFormat] = None,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    run_as_owner: typing.Optional[builtins.bool] = None,
    run_as_user_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[Schedule, typing.Dict[builtins.str, typing.Any]]] = None,
    settings: typing.Any = None,
    tags: typing.Any = None,
    tasks: typing.Optional[typing.Sequence[typing.Union[Task, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a9cf8391a22be3d77d6872a04c975b72ea9a4916efe0b716bee330b9df834b(
    *,
    access_control_list: typing.Optional[typing.Sequence[typing.Union[AccessUser, typing.Dict[builtins.str, typing.Any]]]] = None,
    creator_user_name: typing.Optional[builtins.str] = None,
    email_notifications: typing.Optional[typing.Union[EmailNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_cluster_id: typing.Optional[builtins.str] = None,
    format: typing.Optional[CfnJobPropsFormat] = None,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    run_as_owner: typing.Optional[builtins.bool] = None,
    run_as_user_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[Schedule, typing.Dict[builtins.str, typing.Any]]] = None,
    settings: typing.Any = None,
    tags: typing.Any = None,
    tasks: typing.Optional[typing.Sequence[typing.Union[Task, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450d234383fdb2b989d1de12e3b6f6553b271911dc58645ab0dfb84909cf85f6(
    *,
    no_alert_for_skipped_runs: typing.Optional[builtins.bool] = None,
    on_failure: typing.Optional[typing.Sequence[builtins.str]] = None,
    on_start: typing.Optional[typing.Sequence[builtins.str]] = None,
    on_success: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e04ba3dcce43462d5f40ecc65a527ef384b95972bea182f3689de11b177158f(
    *,
    pause_status: typing.Optional[SchedulePauseStatus] = None,
    quartz_cron_expression: typing.Optional[builtins.str] = None,
    timezone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__622ecd1526c16b235559620603f9da7c71e1da1e11f4c4c7b6c71bcd0e0c7d59(
    *,
    task_key: builtins.str,
    depends_on: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    email_notifications: typing.Optional[typing.Union[EmailNotifications, typing.Dict[builtins.str, typing.Any]]] = None,
    existing_cluster_id: typing.Optional[builtins.str] = None,
    libraries: typing.Optional[typing.Sequence[typing.Any]] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    min_retry_interval_millies: typing.Optional[jsii.Number] = None,
    notebook_task: typing.Optional[typing.Union[TaskNotebookTask, typing.Dict[builtins.str, typing.Any]]] = None,
    pipeline_task: typing.Optional[typing.Union[TaskPipelineTask, typing.Dict[builtins.str, typing.Any]]] = None,
    python_wheel_task: typing.Optional[typing.Union[TaskPythonWheelTask, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_on_timeout: typing.Optional[builtins.bool] = None,
    spark_jar_task: typing.Optional[typing.Union[TaskSparkJarTask, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_python_task: typing.Optional[typing.Union[TaskSparkPythonTask, typing.Dict[builtins.str, typing.Any]]] = None,
    spark_submit_task: typing.Optional[typing.Union[TaskSparkSubmitTask, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf4348bf7077cd719d83343da78cf1706879866ba64f3cbf413d8b217aa7731(
    *,
    notebook_path: builtins.str,
    base_parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be07107027cd44ade61f9db9a68717eef80b5821fd5623d3775fd0b9e83a2e07(
    *,
    pipeline_id: builtins.str,
    full_refresh: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2582be32d5cc12550bf6609f119b046a8a5e9aa2cf5a2ed3af169e7b184bfbc(
    *,
    package_name: builtins.str,
    entry_point: typing.Optional[builtins.str] = None,
    named_parameters: typing.Any = None,
    parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e29e5f60db7136380d8ed8d443e0824ba7cf73e24ba17500ee376fbb599a38(
    *,
    main_class_name: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcaee6fea82effa1267547c315bbf8064b8f67a1fb3086d40e6b962e4c1e6f41(
    *,
    python_file: builtins.str,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26abd145b33e49408f481fcdb45fd061a3889149f1e6f5e6eb2af03306bc33a(
    *,
    parameters: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
