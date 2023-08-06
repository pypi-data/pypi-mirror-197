'''
# newrelic-alert-nrqlconditionstatic

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Alert::NrqlConditionStatic` v1.1.0.

## Description

Manage New Relic NRQL Static Alerts Condition

## References

* [Documentation](https://github.com/aws-ia/cloudformation-newrelic-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Alert::NrqlConditionStatic \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/NewRelic-Alert-NrqlConditionStatic \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Alert::NrqlConditionStatic`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-alert-nrqlconditionstatic+v1.1.0).
* Issues related to `NewRelic::Alert::NrqlConditionStatic` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-newrelic-resource-providers).

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


class CfnNrqlConditionStatic(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.CfnNrqlConditionStatic",
):
    '''A CloudFormation ``NewRelic::Alert::NrqlConditionStatic``.

    :cloudformationResource: NewRelic::Alert::NrqlConditionStatic
    :link: https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: jsii.Number,
        condition: typing.Union["ConditionInput", typing.Dict[builtins.str, typing.Any]],
        policy_id: jsii.Number,
    ) -> None:
        '''Create a new ``NewRelic::Alert::NrqlConditionStatic``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_id: Account ID the alerts condition should belong to.
        :param condition: 
        :param policy_id: Policy ID for the condition.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5466608dce42d575df8b92883cc462ff7ba2bb71635e3cf8ef9eef98f9c071fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNrqlConditionStaticProps(
            account_id=account_id, condition=condition, policy_id=policy_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrConditionId")
    def attr_condition_id(self) -> jsii.Number:
        '''Attribute ``NewRelic::Alert::NrqlConditionStatic.ConditionId``.

        :link: https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrConditionId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnNrqlConditionStaticProps":
        '''Resource props.'''
        return typing.cast("CfnNrqlConditionStaticProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.CfnNrqlConditionStaticProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "condition": "condition",
        "policy_id": "policyId",
    },
)
class CfnNrqlConditionStaticProps:
    def __init__(
        self,
        *,
        account_id: jsii.Number,
        condition: typing.Union["ConditionInput", typing.Dict[builtins.str, typing.Any]],
        policy_id: jsii.Number,
    ) -> None:
        '''Manage New Relic NRQL Static Alerts Condition.

        :param account_id: Account ID the alerts condition should belong to.
        :param condition: 
        :param policy_id: Policy ID for the condition.

        :schema: CfnNrqlConditionStaticProps
        '''
        if isinstance(condition, dict):
            condition = ConditionInput(**condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4807d36585cba25ce925f368729e99c958f5c5350e6c8dc8e273640836ba3e3e)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "condition": condition,
            "policy_id": policy_id,
        }

    @builtins.property
    def account_id(self) -> jsii.Number:
        '''Account ID the alerts condition should belong to.

        :schema: CfnNrqlConditionStaticProps#AccountId
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def condition(self) -> "ConditionInput":
        '''
        :schema: CfnNrqlConditionStaticProps#Condition
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast("ConditionInput", result)

    @builtins.property
    def policy_id(self) -> jsii.Number:
        '''Policy ID for the condition.

        :schema: CfnNrqlConditionStaticProps#PolicyId
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNrqlConditionStaticProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInput",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "name": "name",
        "nrql": "nrql",
        "terms": "terms",
        "description": "description",
        "expiration": "expiration",
        "runbook_url": "runbookUrl",
        "signal": "signal",
        "violation_time_limit_seconds": "violationTimeLimitSeconds",
    },
)
class ConditionInput:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        name: builtins.str,
        nrql: typing.Union["ConditionInputNrql", typing.Dict[builtins.str, typing.Any]],
        terms: typing.Union["ConditionInputTerms", typing.Dict[builtins.str, typing.Any]],
        description: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[typing.Union["ConditionInputExpiration", typing.Dict[builtins.str, typing.Any]]] = None,
        runbook_url: typing.Optional[builtins.str] = None,
        signal: typing.Optional[typing.Union["ConditionInputSignal", typing.Dict[builtins.str, typing.Any]]] = None,
        violation_time_limit_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Input settings for the static NRQL condition.

        :param enabled: Whether the NRQL condition is enabled.
        :param name: Name of the NRQL condition.
        :param nrql: The NRQL query that defines the signal for the condition.
        :param terms: List of critical and warning terms for the condition.
        :param description: The custom violation description.
        :param expiration: Settings for how violations are opened or closed when a signal expires.
        :param runbook_url: Runbook URL.
        :param signal: Configuration that defines the signal that the NRQL condition will use to evaluate.
        :param violation_time_limit_seconds: Duration after which a violation automatically closes in seconds.

        :schema: ConditionInput
        '''
        if isinstance(nrql, dict):
            nrql = ConditionInputNrql(**nrql)
        if isinstance(terms, dict):
            terms = ConditionInputTerms(**terms)
        if isinstance(expiration, dict):
            expiration = ConditionInputExpiration(**expiration)
        if isinstance(signal, dict):
            signal = ConditionInputSignal(**signal)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c197d9523e4633de7397f8db95b632c716d13f26dea7576c168a7a0fc2907f5)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument nrql", value=nrql, expected_type=type_hints["nrql"])
            check_type(argname="argument terms", value=terms, expected_type=type_hints["terms"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument runbook_url", value=runbook_url, expected_type=type_hints["runbook_url"])
            check_type(argname="argument signal", value=signal, expected_type=type_hints["signal"])
            check_type(argname="argument violation_time_limit_seconds", value=violation_time_limit_seconds, expected_type=type_hints["violation_time_limit_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "name": name,
            "nrql": nrql,
            "terms": terms,
        }
        if description is not None:
            self._values["description"] = description
        if expiration is not None:
            self._values["expiration"] = expiration
        if runbook_url is not None:
            self._values["runbook_url"] = runbook_url
        if signal is not None:
            self._values["signal"] = signal
        if violation_time_limit_seconds is not None:
            self._values["violation_time_limit_seconds"] = violation_time_limit_seconds

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Whether the NRQL condition is enabled.

        :schema: ConditionInput#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the NRQL condition.

        :schema: ConditionInput#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nrql(self) -> "ConditionInputNrql":
        '''The NRQL query that defines the signal for the condition.

        :schema: ConditionInput#Nrql
        '''
        result = self._values.get("nrql")
        assert result is not None, "Required property 'nrql' is missing"
        return typing.cast("ConditionInputNrql", result)

    @builtins.property
    def terms(self) -> "ConditionInputTerms":
        '''List of critical and warning terms for the condition.

        :schema: ConditionInput#Terms
        '''
        result = self._values.get("terms")
        assert result is not None, "Required property 'terms' is missing"
        return typing.cast("ConditionInputTerms", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The custom violation description.

        :schema: ConditionInput#Description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration(self) -> typing.Optional["ConditionInputExpiration"]:
        '''Settings for how violations are opened or closed when a signal expires.

        :schema: ConditionInput#Expiration
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional["ConditionInputExpiration"], result)

    @builtins.property
    def runbook_url(self) -> typing.Optional[builtins.str]:
        '''Runbook URL.

        :schema: ConditionInput#RunbookUrl
        '''
        result = self._values.get("runbook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signal(self) -> typing.Optional["ConditionInputSignal"]:
        '''Configuration that defines the signal that the NRQL condition will use to evaluate.

        :schema: ConditionInput#Signal
        '''
        result = self._values.get("signal")
        return typing.cast(typing.Optional["ConditionInputSignal"], result)

    @builtins.property
    def violation_time_limit_seconds(self) -> typing.Optional[jsii.Number]:
        '''Duration after which a violation automatically closes in seconds.

        :schema: ConditionInput#ViolationTimeLimitSeconds
        '''
        result = self._values.get("violation_time_limit_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputExpiration",
    jsii_struct_bases=[],
    name_mapping={
        "close_violations_on_expiration": "closeViolationsOnExpiration",
        "expiration_duration": "expirationDuration",
        "open_violation_on_expiration": "openViolationOnExpiration",
    },
)
class ConditionInputExpiration:
    def __init__(
        self,
        *,
        close_violations_on_expiration: typing.Optional[builtins.bool] = None,
        expiration_duration: typing.Optional[jsii.Number] = None,
        open_violation_on_expiration: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Settings for how violations are opened or closed when a signal expires.

        :param close_violations_on_expiration: Whether to close all open violations when the signal expires. Defaults to true. Default: true.
        :param expiration_duration: The amount of time (in seconds) to wait before considering if the signal has been lost. Max value of 172800 (48 hours).
        :param open_violation_on_expiration: Whether to create a new "lost signal" violation to capture that the signal expired. Defaults to false. Default: false.

        :schema: ConditionInputExpiration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__846f67673b497c31be12b89303a24452101a8a6c78c071d4ee975cef6a1650b2)
            check_type(argname="argument close_violations_on_expiration", value=close_violations_on_expiration, expected_type=type_hints["close_violations_on_expiration"])
            check_type(argname="argument expiration_duration", value=expiration_duration, expected_type=type_hints["expiration_duration"])
            check_type(argname="argument open_violation_on_expiration", value=open_violation_on_expiration, expected_type=type_hints["open_violation_on_expiration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if close_violations_on_expiration is not None:
            self._values["close_violations_on_expiration"] = close_violations_on_expiration
        if expiration_duration is not None:
            self._values["expiration_duration"] = expiration_duration
        if open_violation_on_expiration is not None:
            self._values["open_violation_on_expiration"] = open_violation_on_expiration

    @builtins.property
    def close_violations_on_expiration(self) -> typing.Optional[builtins.bool]:
        '''Whether to close all open violations when the signal expires.

        Defaults to true.

        :default: true.

        :schema: ConditionInputExpiration#CloseViolationsOnExpiration
        '''
        result = self._values.get("close_violations_on_expiration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expiration_duration(self) -> typing.Optional[jsii.Number]:
        '''The amount of time (in seconds) to wait before considering if the signal has been lost.

        Max value of 172800 (48 hours).

        :schema: ConditionInputExpiration#ExpirationDuration
        '''
        result = self._values.get("expiration_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def open_violation_on_expiration(self) -> typing.Optional[builtins.bool]:
        '''Whether to create a new "lost signal" violation to capture that the signal expired.

        Defaults to false.

        :default: false.

        :schema: ConditionInputExpiration#OpenViolationOnExpiration
        '''
        result = self._values.get("open_violation_on_expiration")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionInputExpiration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputNrql",
    jsii_struct_bases=[],
    name_mapping={"query": "query"},
)
class ConditionInputNrql:
    def __init__(self, *, query: builtins.str) -> None:
        '''The NRQL query that defines the signal for the condition.

        :param query: NRQL syntax that defines the query.

        :schema: ConditionInputNrql
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c2e373a3d0d7aa6400b9fa6b2cb104d6ce1e8fbadb854bf34f07199e881f67b)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }

    @builtins.property
    def query(self) -> builtins.str:
        '''NRQL syntax that defines the query.

        :schema: ConditionInputNrql#Query
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionInputNrql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputSignal",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation_delay": "aggregationDelay",
        "aggregation_method": "aggregationMethod",
        "aggregation_timer": "aggregationTimer",
        "aggregation_window": "aggregationWindow",
        "fill_option": "fillOption",
        "fill_value": "fillValue",
        "slide_by": "slideBy",
    },
)
class ConditionInputSignal:
    def __init__(
        self,
        *,
        aggregation_delay: typing.Optional[jsii.Number] = None,
        aggregation_method: typing.Optional["ConditionInputSignalAggregationMethod"] = None,
        aggregation_timer: typing.Optional[jsii.Number] = None,
        aggregation_window: typing.Optional[jsii.Number] = None,
        fill_option: typing.Optional["ConditionInputSignalFillOption"] = None,
        fill_value: typing.Optional[jsii.Number] = None,
        slide_by: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration that defines the signal that the NRQL condition will use to evaluate.

        :param aggregation_delay: How long we wait for data that belongs in each aggregation window.
        :param aggregation_method: The method that determines when we consider an aggregation window to be complete so that we can evaluate the signal for violations.
        :param aggregation_timer: How long we wait after each data point arrives to make sure we've processed the whole batch.
        :param aggregation_window: Aggregation window controls the duration of the time window used to evaluate the NRQL query, in seconds.
        :param fill_option: Option that determines the type of value that should be used to fill gaps (empty windows).
        :param fill_value: If using the static fill option, this the value used for filling.
        :param slide_by: This setting gathers data in overlapping time windows to smooth the chart line, making it easier to spot trends.

        :schema: ConditionInputSignal
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b908b7fce0aa23f68b0f7dfc300a0b30f1881c441c9e33e966aac3767dd6457)
            check_type(argname="argument aggregation_delay", value=aggregation_delay, expected_type=type_hints["aggregation_delay"])
            check_type(argname="argument aggregation_method", value=aggregation_method, expected_type=type_hints["aggregation_method"])
            check_type(argname="argument aggregation_timer", value=aggregation_timer, expected_type=type_hints["aggregation_timer"])
            check_type(argname="argument aggregation_window", value=aggregation_window, expected_type=type_hints["aggregation_window"])
            check_type(argname="argument fill_option", value=fill_option, expected_type=type_hints["fill_option"])
            check_type(argname="argument fill_value", value=fill_value, expected_type=type_hints["fill_value"])
            check_type(argname="argument slide_by", value=slide_by, expected_type=type_hints["slide_by"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aggregation_delay is not None:
            self._values["aggregation_delay"] = aggregation_delay
        if aggregation_method is not None:
            self._values["aggregation_method"] = aggregation_method
        if aggregation_timer is not None:
            self._values["aggregation_timer"] = aggregation_timer
        if aggregation_window is not None:
            self._values["aggregation_window"] = aggregation_window
        if fill_option is not None:
            self._values["fill_option"] = fill_option
        if fill_value is not None:
            self._values["fill_value"] = fill_value
        if slide_by is not None:
            self._values["slide_by"] = slide_by

    @builtins.property
    def aggregation_delay(self) -> typing.Optional[jsii.Number]:
        '''How long we wait for data that belongs in each aggregation window.

        :schema: ConditionInputSignal#AggregationDelay
        '''
        result = self._values.get("aggregation_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aggregation_method(
        self,
    ) -> typing.Optional["ConditionInputSignalAggregationMethod"]:
        '''The method that determines when we consider an aggregation window to be complete so that we can evaluate the signal for violations.

        :schema: ConditionInputSignal#AggregationMethod
        '''
        result = self._values.get("aggregation_method")
        return typing.cast(typing.Optional["ConditionInputSignalAggregationMethod"], result)

    @builtins.property
    def aggregation_timer(self) -> typing.Optional[jsii.Number]:
        '''How long we wait after each data point arrives to make sure we've processed the whole batch.

        :schema: ConditionInputSignal#AggregationTimer
        '''
        result = self._values.get("aggregation_timer")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def aggregation_window(self) -> typing.Optional[jsii.Number]:
        '''Aggregation window controls the duration of the time window used to evaluate the NRQL query, in seconds.

        :schema: ConditionInputSignal#AggregationWindow
        '''
        result = self._values.get("aggregation_window")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fill_option(self) -> typing.Optional["ConditionInputSignalFillOption"]:
        '''Option that determines the type of value that should be used to fill gaps (empty windows).

        :schema: ConditionInputSignal#FillOption
        '''
        result = self._values.get("fill_option")
        return typing.cast(typing.Optional["ConditionInputSignalFillOption"], result)

    @builtins.property
    def fill_value(self) -> typing.Optional[jsii.Number]:
        '''If using the static fill option, this the value used for filling.

        :schema: ConditionInputSignal#FillValue
        '''
        result = self._values.get("fill_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def slide_by(self) -> typing.Optional[jsii.Number]:
        '''This setting gathers data in overlapping time windows to smooth the chart line, making it easier to spot trends.

        :schema: ConditionInputSignal#SlideBy
        '''
        result = self._values.get("slide_by")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionInputSignal(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputSignalAggregationMethod"
)
class ConditionInputSignalAggregationMethod(enum.Enum):
    '''The method that determines when we consider an aggregation window to be complete so that we can evaluate the signal for violations.

    :schema: ConditionInputSignalAggregationMethod
    '''

    CADENCE = "CADENCE"
    '''CADENCE.'''
    EVENT_FLOW = "EVENT_FLOW"
    '''EVENT_FLOW.'''
    EVENT_TIMER = "EVENT_TIMER"
    '''EVENT_TIMER.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputSignalFillOption"
)
class ConditionInputSignalFillOption(enum.Enum):
    '''Option that determines the type of value that should be used to fill gaps (empty windows).

    :schema: ConditionInputSignalFillOption
    '''

    LAST_VALUE = "LAST_VALUE"
    '''LAST_VALUE.'''
    NONE = "NONE"
    '''NONE.'''
    STATIC = "STATIC"
    '''STATIC.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputTerms",
    jsii_struct_bases=[],
    name_mapping={
        "operator": "operator",
        "priority": "priority",
        "threshold": "threshold",
        "threshold_duration": "thresholdDuration",
        "threshold_occurrences": "thresholdOccurrences",
    },
)
class ConditionInputTerms:
    def __init__(
        self,
        *,
        operator: "ConditionInputTermsOperator",
        priority: "ConditionInputTermsPriority",
        threshold: jsii.Number,
        threshold_duration: jsii.Number,
        threshold_occurrences: "ConditionInputTermsThresholdOccurrences",
    ) -> None:
        '''List of critical and warning terms for the condition.

        :param operator: Operator used to compare against the threshold.
        :param priority: Priority determines whether notifications will be sent for violations or not.
        :param threshold: Value that triggers a violation.
        :param threshold_duration: The duration, in seconds, that the threshold must violate for in order to create a violation.
        :param threshold_occurrences: How many data points must be in violation for the specified thresholdDuration.

        :schema: ConditionInputTerms
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb11afc568a4bc3b5c1a4a3046767cce743fe24cb3e658f0da4e7e6000b1dac)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument threshold_duration", value=threshold_duration, expected_type=type_hints["threshold_duration"])
            check_type(argname="argument threshold_occurrences", value=threshold_occurrences, expected_type=type_hints["threshold_occurrences"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "priority": priority,
            "threshold": threshold,
            "threshold_duration": threshold_duration,
            "threshold_occurrences": threshold_occurrences,
        }

    @builtins.property
    def operator(self) -> "ConditionInputTermsOperator":
        '''Operator used to compare against the threshold.

        :schema: ConditionInputTerms#Operator
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast("ConditionInputTermsOperator", result)

    @builtins.property
    def priority(self) -> "ConditionInputTermsPriority":
        '''Priority determines whether notifications will be sent for violations or not.

        :schema: ConditionInputTerms#Priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast("ConditionInputTermsPriority", result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Value that triggers a violation.

        :schema: ConditionInputTerms#Threshold
        '''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def threshold_duration(self) -> jsii.Number:
        '''The duration, in seconds, that the threshold must violate for in order to create a violation.

        :schema: ConditionInputTerms#ThresholdDuration
        '''
        result = self._values.get("threshold_duration")
        assert result is not None, "Required property 'threshold_duration' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def threshold_occurrences(self) -> "ConditionInputTermsThresholdOccurrences":
        '''How many data points must be in violation for the specified thresholdDuration.

        :schema: ConditionInputTerms#ThresholdOccurrences
        '''
        result = self._values.get("threshold_occurrences")
        assert result is not None, "Required property 'threshold_occurrences' is missing"
        return typing.cast("ConditionInputTermsThresholdOccurrences", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConditionInputTerms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputTermsOperator"
)
class ConditionInputTermsOperator(enum.Enum):
    '''Operator used to compare against the threshold.

    :schema: ConditionInputTermsOperator
    '''

    ABOVE = "ABOVE"
    '''ABOVE.'''
    ABOVE_OR_EQUALS = "ABOVE_OR_EQUALS"
    '''ABOVE_OR_EQUALS.'''
    BELOW = "BELOW"
    '''BELOW.'''
    BELOW_OR_EQUALS = "BELOW_OR_EQUALS"
    '''BELOW_OR_EQUALS.'''
    EQUALS = "EQUALS"
    '''EQUALS.'''
    NOT_EQUALS = "NOT_EQUALS"
    '''NOT_EQUALS.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputTermsPriority"
)
class ConditionInputTermsPriority(enum.Enum):
    '''Priority determines whether notifications will be sent for violations or not.

    :schema: ConditionInputTermsPriority
    '''

    CRITICAL = "CRITICAL"
    '''CRITICAL.'''
    WARNING = "WARNING"
    '''WARNING.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-alert-nrqlconditionstatic.ConditionInputTermsThresholdOccurrences"
)
class ConditionInputTermsThresholdOccurrences(enum.Enum):
    '''How many data points must be in violation for the specified thresholdDuration.

    :schema: ConditionInputTermsThresholdOccurrences
    '''

    ALL = "ALL"
    '''ALL.'''
    AT_LEAST_ONCE = "AT_LEAST_ONCE"
    '''AT_LEAST_ONCE.'''


__all__ = [
    "CfnNrqlConditionStatic",
    "CfnNrqlConditionStaticProps",
    "ConditionInput",
    "ConditionInputExpiration",
    "ConditionInputNrql",
    "ConditionInputSignal",
    "ConditionInputSignalAggregationMethod",
    "ConditionInputSignalFillOption",
    "ConditionInputTerms",
    "ConditionInputTermsOperator",
    "ConditionInputTermsPriority",
    "ConditionInputTermsThresholdOccurrences",
]

publication.publish()

def _typecheckingstub__5466608dce42d575df8b92883cc462ff7ba2bb71635e3cf8ef9eef98f9c071fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: jsii.Number,
    condition: typing.Union[ConditionInput, typing.Dict[builtins.str, typing.Any]],
    policy_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4807d36585cba25ce925f368729e99c958f5c5350e6c8dc8e273640836ba3e3e(
    *,
    account_id: jsii.Number,
    condition: typing.Union[ConditionInput, typing.Dict[builtins.str, typing.Any]],
    policy_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c197d9523e4633de7397f8db95b632c716d13f26dea7576c168a7a0fc2907f5(
    *,
    enabled: builtins.bool,
    name: builtins.str,
    nrql: typing.Union[ConditionInputNrql, typing.Dict[builtins.str, typing.Any]],
    terms: typing.Union[ConditionInputTerms, typing.Dict[builtins.str, typing.Any]],
    description: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[typing.Union[ConditionInputExpiration, typing.Dict[builtins.str, typing.Any]]] = None,
    runbook_url: typing.Optional[builtins.str] = None,
    signal: typing.Optional[typing.Union[ConditionInputSignal, typing.Dict[builtins.str, typing.Any]]] = None,
    violation_time_limit_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__846f67673b497c31be12b89303a24452101a8a6c78c071d4ee975cef6a1650b2(
    *,
    close_violations_on_expiration: typing.Optional[builtins.bool] = None,
    expiration_duration: typing.Optional[jsii.Number] = None,
    open_violation_on_expiration: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c2e373a3d0d7aa6400b9fa6b2cb104d6ce1e8fbadb854bf34f07199e881f67b(
    *,
    query: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b908b7fce0aa23f68b0f7dfc300a0b30f1881c441c9e33e966aac3767dd6457(
    *,
    aggregation_delay: typing.Optional[jsii.Number] = None,
    aggregation_method: typing.Optional[ConditionInputSignalAggregationMethod] = None,
    aggregation_timer: typing.Optional[jsii.Number] = None,
    aggregation_window: typing.Optional[jsii.Number] = None,
    fill_option: typing.Optional[ConditionInputSignalFillOption] = None,
    fill_value: typing.Optional[jsii.Number] = None,
    slide_by: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb11afc568a4bc3b5c1a4a3046767cce743fe24cb3e658f0da4e7e6000b1dac(
    *,
    operator: ConditionInputTermsOperator,
    priority: ConditionInputTermsPriority,
    threshold: jsii.Number,
    threshold_duration: jsii.Number,
    threshold_occurrences: ConditionInputTermsThresholdOccurrences,
) -> None:
    """Type checking stubs"""
    pass
