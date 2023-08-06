'''
# newrelic-agent-configuration

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Agent::Configuration` v1.1.0.

## Description

Manage New Relic Server-Side Agent Configuration

## References

* [Documentation](https://github.com/aws-ia/cloudformation-newrelic-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Agent::Configuration \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/NewRelic-Agent-Configuration \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Agent::Configuration`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-agent-configuration+v1.1.0).
* Issues related to `NewRelic::Agent::Configuration` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-newrelic-resource-providers).

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
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInput",
    jsii_struct_bases=[],
    name_mapping={"settings": "settings"},
)
class AgentConfigurationInput:
    def __init__(
        self,
        *,
        settings: typing.Optional[typing.Union["AgentConfigurationInputSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param settings: Input data about the entities you want to update and the settings to use.

        :schema: AgentConfigurationInput
        '''
        if isinstance(settings, dict):
            settings = AgentConfigurationInputSettings(**settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab52a3c8e8048c6f73869865b33ff3566d716f8d39ebdbbcdfa239842420ab77)
            check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if settings is not None:
            self._values["settings"] = settings

    @builtins.property
    def settings(self) -> typing.Optional["AgentConfigurationInputSettings"]:
        '''Input data about the entities you want to update and the settings to use.

        :schema: AgentConfigurationInput#Settings
        '''
        result = self._values.get("settings")
        return typing.cast(typing.Optional["AgentConfigurationInputSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettings",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "apm_config": "apmConfig",
        "browser_config": "browserConfig",
        "error_collector": "errorCollector",
        "slow_sql": "slowSql",
        "thread_profiler": "threadProfiler",
        "tracer_type": "tracerType",
        "transaction_tracer": "transactionTracer",
    },
)
class AgentConfigurationInputSettings:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        apm_config: typing.Optional[typing.Union["AgentConfigurationInputSettingsApmConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        browser_config: typing.Optional[typing.Union["AgentConfigurationInputSettingsBrowserConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        error_collector: typing.Optional[typing.Union["AgentConfigurationInputSettingsErrorCollector", typing.Dict[builtins.str, typing.Any]]] = None,
        slow_sql: typing.Optional[typing.Union["AgentConfigurationInputSettingsSlowSql", typing.Dict[builtins.str, typing.Any]]] = None,
        thread_profiler: typing.Optional[typing.Union["AgentConfigurationInputSettingsThreadProfiler", typing.Dict[builtins.str, typing.Any]]] = None,
        tracer_type: typing.Optional[typing.Union["AgentConfigurationInputSettingsTracerType", typing.Dict[builtins.str, typing.Any]]] = None,
        transaction_tracer: typing.Optional[typing.Union["AgentConfigurationInputSettingsTransactionTracer", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Input data about the entities you want to update and the settings to use.

        :param alias: The new name for the application.
        :param apm_config: Provides fields to set general APM application settings.
        :param browser_config: 
        :param error_collector: The error collector captures information about uncaught exceptions and sends them to New Relic for viewing.
        :param slow_sql: In APM, when transaction traces are collected, there may be additional Slow query data available.
        :param thread_profiler: Settings for the thread profiler.
        :param tracer_type: Input object for setting the type of tracing performed.
        :param transaction_tracer: Transaction Tracer settings related to APM applications.

        :schema: AgentConfigurationInputSettings
        '''
        if isinstance(apm_config, dict):
            apm_config = AgentConfigurationInputSettingsApmConfig(**apm_config)
        if isinstance(browser_config, dict):
            browser_config = AgentConfigurationInputSettingsBrowserConfig(**browser_config)
        if isinstance(error_collector, dict):
            error_collector = AgentConfigurationInputSettingsErrorCollector(**error_collector)
        if isinstance(slow_sql, dict):
            slow_sql = AgentConfigurationInputSettingsSlowSql(**slow_sql)
        if isinstance(thread_profiler, dict):
            thread_profiler = AgentConfigurationInputSettingsThreadProfiler(**thread_profiler)
        if isinstance(tracer_type, dict):
            tracer_type = AgentConfigurationInputSettingsTracerType(**tracer_type)
        if isinstance(transaction_tracer, dict):
            transaction_tracer = AgentConfigurationInputSettingsTransactionTracer(**transaction_tracer)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6254e0f3eb1d566a852bb9cb2188b37356c1674a9dfcc5caf75a86b751fcceef)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument apm_config", value=apm_config, expected_type=type_hints["apm_config"])
            check_type(argname="argument browser_config", value=browser_config, expected_type=type_hints["browser_config"])
            check_type(argname="argument error_collector", value=error_collector, expected_type=type_hints["error_collector"])
            check_type(argname="argument slow_sql", value=slow_sql, expected_type=type_hints["slow_sql"])
            check_type(argname="argument thread_profiler", value=thread_profiler, expected_type=type_hints["thread_profiler"])
            check_type(argname="argument tracer_type", value=tracer_type, expected_type=type_hints["tracer_type"])
            check_type(argname="argument transaction_tracer", value=transaction_tracer, expected_type=type_hints["transaction_tracer"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if apm_config is not None:
            self._values["apm_config"] = apm_config
        if browser_config is not None:
            self._values["browser_config"] = browser_config
        if error_collector is not None:
            self._values["error_collector"] = error_collector
        if slow_sql is not None:
            self._values["slow_sql"] = slow_sql
        if thread_profiler is not None:
            self._values["thread_profiler"] = thread_profiler
        if tracer_type is not None:
            self._values["tracer_type"] = tracer_type
        if transaction_tracer is not None:
            self._values["transaction_tracer"] = transaction_tracer

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''The new name for the application.

        :schema: AgentConfigurationInputSettings#Alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def apm_config(self) -> typing.Optional["AgentConfigurationInputSettingsApmConfig"]:
        '''Provides fields to set general APM application settings.

        :schema: AgentConfigurationInputSettings#ApmConfig
        '''
        result = self._values.get("apm_config")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsApmConfig"], result)

    @builtins.property
    def browser_config(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsBrowserConfig"]:
        '''
        :schema: AgentConfigurationInputSettings#BrowserConfig
        '''
        result = self._values.get("browser_config")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsBrowserConfig"], result)

    @builtins.property
    def error_collector(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsErrorCollector"]:
        '''The error collector captures information about uncaught exceptions and sends them to New Relic for viewing.

        :schema: AgentConfigurationInputSettings#ErrorCollector
        '''
        result = self._values.get("error_collector")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsErrorCollector"], result)

    @builtins.property
    def slow_sql(self) -> typing.Optional["AgentConfigurationInputSettingsSlowSql"]:
        '''In APM, when transaction traces are collected, there may be additional Slow query data available.

        :schema: AgentConfigurationInputSettings#SlowSql
        '''
        result = self._values.get("slow_sql")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsSlowSql"], result)

    @builtins.property
    def thread_profiler(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsThreadProfiler"]:
        '''Settings for the thread profiler.

        :schema: AgentConfigurationInputSettings#ThreadProfiler
        '''
        result = self._values.get("thread_profiler")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsThreadProfiler"], result)

    @builtins.property
    def tracer_type(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsTracerType"]:
        '''Input object for setting the type of tracing performed.

        :schema: AgentConfigurationInputSettings#TracerType
        '''
        result = self._values.get("tracer_type")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsTracerType"], result)

    @builtins.property
    def transaction_tracer(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsTransactionTracer"]:
        '''Transaction Tracer settings related to APM applications.

        :schema: AgentConfigurationInputSettings#TransactionTracer
        '''
        result = self._values.get("transaction_tracer")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsTransactionTracer"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsApmConfig",
    jsii_struct_bases=[],
    name_mapping={
        "apdex_target": "apdexTarget",
        "use_server_side_config": "useServerSideConfig",
    },
)
class AgentConfigurationInputSettingsApmConfig:
    def __init__(
        self,
        *,
        apdex_target: typing.Optional[jsii.Number] = None,
        use_server_side_config: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Provides fields to set general APM application settings.

        :param apdex_target: The desired target for the APDEX measurement of this application.
        :param use_server_side_config: Sets if installed agents should override local settings with ones set here.

        :schema: AgentConfigurationInputSettingsApmConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ae29d45520d6cc6ec140bde1121c1087a77481b23513d49ebb0ac5acda2ed5)
            check_type(argname="argument apdex_target", value=apdex_target, expected_type=type_hints["apdex_target"])
            check_type(argname="argument use_server_side_config", value=use_server_side_config, expected_type=type_hints["use_server_side_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apdex_target is not None:
            self._values["apdex_target"] = apdex_target
        if use_server_side_config is not None:
            self._values["use_server_side_config"] = use_server_side_config

    @builtins.property
    def apdex_target(self) -> typing.Optional[jsii.Number]:
        '''The desired target for the APDEX measurement of this application.

        :schema: AgentConfigurationInputSettingsApmConfig#ApdexTarget
        '''
        result = self._values.get("apdex_target")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_server_side_config(self) -> typing.Optional[builtins.bool]:
        '''Sets if installed agents should override local settings with ones set here.

        :schema: AgentConfigurationInputSettingsApmConfig#UseServerSideConfig
        '''
        result = self._values.get("use_server_side_config")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsApmConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsBrowserConfig",
    jsii_struct_bases=[],
    name_mapping={"apdex_target": "apdexTarget"},
)
class AgentConfigurationInputSettingsBrowserConfig:
    def __init__(self, *, apdex_target: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param apdex_target: The desired target for the APDEX measurement of this application.

        :schema: AgentConfigurationInputSettingsBrowserConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4973440c04ffb65a8ca18cef1a01720ee3d1591ea405e304530a096478323d5)
            check_type(argname="argument apdex_target", value=apdex_target, expected_type=type_hints["apdex_target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apdex_target is not None:
            self._values["apdex_target"] = apdex_target

    @builtins.property
    def apdex_target(self) -> typing.Optional[jsii.Number]:
        '''The desired target for the APDEX measurement of this application.

        :schema: AgentConfigurationInputSettingsBrowserConfig#ApdexTarget
        '''
        result = self._values.get("apdex_target")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsBrowserConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsErrorCollector",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "expected_error_classes": "expectedErrorClasses",
        "expected_error_codes": "expectedErrorCodes",
        "ignored_error_classes": "ignoredErrorClasses",
        "ignored_error_codes": "ignoredErrorCodes",
    },
)
class AgentConfigurationInputSettingsErrorCollector:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        expected_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        expected_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignored_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignored_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''The error collector captures information about uncaught exceptions and sends them to New Relic for viewing.

        :param enabled: Enable error collector.
        :param expected_error_classes: Prevents specified exception classes from affecting error rate or Apdex score while still reporting the errors to APM.
        :param expected_error_codes: A comma-separated list comprised of individual and dashed ranges of HTTP status codes to be marked as expected and thus prevented from affecting error rate or Apdex score.
        :param ignored_error_classes: Specified exception class names will be ignored and will not affect error rate or Apdex score, or be reported to APM.
        :param ignored_error_codes: A comma-separated list comprised of individual and dashed ranges of HTTP status codes that should not be treated as errors.

        :schema: AgentConfigurationInputSettingsErrorCollector
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee7deb5b965725dcfc21bf0929320029e7ca6555d985fef886b1d598fa01fa62)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expected_error_classes", value=expected_error_classes, expected_type=type_hints["expected_error_classes"])
            check_type(argname="argument expected_error_codes", value=expected_error_codes, expected_type=type_hints["expected_error_codes"])
            check_type(argname="argument ignored_error_classes", value=ignored_error_classes, expected_type=type_hints["ignored_error_classes"])
            check_type(argname="argument ignored_error_codes", value=ignored_error_codes, expected_type=type_hints["ignored_error_codes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if expected_error_classes is not None:
            self._values["expected_error_classes"] = expected_error_classes
        if expected_error_codes is not None:
            self._values["expected_error_codes"] = expected_error_codes
        if ignored_error_classes is not None:
            self._values["ignored_error_classes"] = ignored_error_classes
        if ignored_error_codes is not None:
            self._values["ignored_error_codes"] = ignored_error_codes

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable error collector.

        :schema: AgentConfigurationInputSettingsErrorCollector#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expected_error_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Prevents specified exception classes from affecting error rate or Apdex score while still reporting the errors to APM.

        :schema: AgentConfigurationInputSettingsErrorCollector#ExpectedErrorClasses
        '''
        result = self._values.get("expected_error_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def expected_error_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A comma-separated list comprised of individual and dashed ranges of HTTP status codes to be marked as expected and thus prevented from affecting error rate or Apdex score.

        :schema: AgentConfigurationInputSettingsErrorCollector#ExpectedErrorCodes
        '''
        result = self._values.get("expected_error_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignored_error_classes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specified exception class names will be ignored and will not affect error rate or Apdex score, or be reported to APM.

        :schema: AgentConfigurationInputSettingsErrorCollector#IgnoredErrorClasses
        '''
        result = self._values.get("ignored_error_classes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignored_error_codes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A comma-separated list comprised of individual and dashed ranges of HTTP status codes that should not be treated as errors.

        :schema: AgentConfigurationInputSettingsErrorCollector#IgnoredErrorCodes
        '''
        result = self._values.get("ignored_error_codes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsErrorCollector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsSlowSql",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class AgentConfigurationInputSettingsSlowSql:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''In APM, when transaction traces are collected, there may be additional Slow query data available.

        :param enabled: Whether or not slow_sql is enabled.

        :schema: AgentConfigurationInputSettingsSlowSql
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c66ae2c9a6f3a6908dc4542f647e18d48c7905b36923dd2e92d0a77472fa374)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether or not slow_sql is enabled.

        :schema: AgentConfigurationInputSettingsSlowSql#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsSlowSql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsThreadProfiler",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class AgentConfigurationInputSettingsThreadProfiler:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''Settings for the thread profiler.

        :param enabled: Is thread profiling enabled for this application?

        :schema: AgentConfigurationInputSettingsThreadProfiler
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a716eb07cfef10647959f1c46dbeea1343672e4997f7d93f1fd6448ca9bf846)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Is thread profiling enabled for this application?

        :schema: AgentConfigurationInputSettingsThreadProfiler#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsThreadProfiler(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsTracerType",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class AgentConfigurationInputSettingsTracerType:
    def __init__(
        self,
        *,
        value: typing.Optional["AgentConfigurationInputSettingsTracerTypeValue"] = None,
    ) -> None:
        '''Input object for setting the type of tracing performed.

        :param value: 

        :schema: AgentConfigurationInputSettingsTracerType
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d1b5d811fcea1289c4ac88b58a277c4aa328655058990f3d9cd6f3315bb2202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsTracerTypeValue"]:
        '''
        :schema: AgentConfigurationInputSettingsTracerType#Value
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsTracerTypeValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsTracerType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsTracerTypeValue"
)
class AgentConfigurationInputSettingsTracerTypeValue(enum.Enum):
    '''
    :schema: AgentConfigurationInputSettingsTracerTypeValue
    '''

    CROSS_APPLICATION_TRACER = "CROSS_APPLICATION_TRACER"
    '''CROSS_APPLICATION_TRACER.'''
    DISTRIBUTED_TRACING = "DISTRIBUTED_TRACING"
    '''DISTRIBUTED_TRACING.'''
    NONE = "NONE"
    '''NONE.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsTransactionTracer",
    jsii_struct_bases=[],
    name_mapping={
        "capture_memcache_keys": "captureMemcacheKeys",
        "enabled": "enabled",
        "explain_enabled": "explainEnabled",
        "explain_threshold_type": "explainThresholdType",
        "explain_threshold_value": "explainThresholdValue",
        "log_sql": "logSql",
        "record_sql": "recordSql",
        "stack_trace_threshold": "stackTraceThreshold",
        "transaction_threshold_type": "transactionThresholdType",
        "transaction_threshold_value": "transactionThresholdValue",
    },
)
class AgentConfigurationInputSettingsTransactionTracer:
    def __init__(
        self,
        *,
        capture_memcache_keys: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        explain_enabled: typing.Optional[builtins.bool] = None,
        explain_threshold_type: typing.Optional["AgentConfigurationInputSettingsTransactionTracerExplainThresholdType"] = None,
        explain_threshold_value: typing.Optional[jsii.Number] = None,
        log_sql: typing.Optional[builtins.bool] = None,
        record_sql: typing.Optional["AgentConfigurationInputSettingsTransactionTracerRecordSql"] = None,
        stack_trace_threshold: typing.Optional[jsii.Number] = None,
        transaction_threshold_type: typing.Optional["AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType"] = None,
        transaction_threshold_value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Transaction Tracer settings related to APM applications.

        :param capture_memcache_keys: Enable or disable the capture of memcache keys from transaction traces.
        :param enabled: If true, this enables the Transaction Tracer feature, enabling collection of transaction traces.
        :param explain_enabled: If true, enables the collection of explain plans in transaction traces.
        :param explain_threshold_type: Relevant only when explain_enabled is true. Can be set to automatic configuration (APDEX_F) or manual (see explainThresholdValue)
        :param explain_threshold_value: Threshold (in seconds) above which the agent will collect explain plans.
        :param log_sql: Set to true to enable logging of queries to the agent log file instead of uploading to New Relic.
        :param record_sql: Obfuscation level for SQL queries reported in transaction trace nodes.
        :param stack_trace_threshold: Specify a threshold in seconds. The agent includes stack traces in transaction trace nodes when the stack trace duration exceeds this threshold.
        :param transaction_threshold_type: Relevant only when TransactionTracer is enabled. Can be set to automatic configuration (APDEX_F) or manual (see TransactionThresholdValue).
        :param transaction_threshold_value: Threshold (in seconds) that transactions with a duration longer than this threshold are eligible for transaction traces.

        :schema: AgentConfigurationInputSettingsTransactionTracer
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54bc86215566a26758cc5c10d103ca08883011b05fb1060bf3c73630e837aa33)
            check_type(argname="argument capture_memcache_keys", value=capture_memcache_keys, expected_type=type_hints["capture_memcache_keys"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument explain_enabled", value=explain_enabled, expected_type=type_hints["explain_enabled"])
            check_type(argname="argument explain_threshold_type", value=explain_threshold_type, expected_type=type_hints["explain_threshold_type"])
            check_type(argname="argument explain_threshold_value", value=explain_threshold_value, expected_type=type_hints["explain_threshold_value"])
            check_type(argname="argument log_sql", value=log_sql, expected_type=type_hints["log_sql"])
            check_type(argname="argument record_sql", value=record_sql, expected_type=type_hints["record_sql"])
            check_type(argname="argument stack_trace_threshold", value=stack_trace_threshold, expected_type=type_hints["stack_trace_threshold"])
            check_type(argname="argument transaction_threshold_type", value=transaction_threshold_type, expected_type=type_hints["transaction_threshold_type"])
            check_type(argname="argument transaction_threshold_value", value=transaction_threshold_value, expected_type=type_hints["transaction_threshold_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capture_memcache_keys is not None:
            self._values["capture_memcache_keys"] = capture_memcache_keys
        if enabled is not None:
            self._values["enabled"] = enabled
        if explain_enabled is not None:
            self._values["explain_enabled"] = explain_enabled
        if explain_threshold_type is not None:
            self._values["explain_threshold_type"] = explain_threshold_type
        if explain_threshold_value is not None:
            self._values["explain_threshold_value"] = explain_threshold_value
        if log_sql is not None:
            self._values["log_sql"] = log_sql
        if record_sql is not None:
            self._values["record_sql"] = record_sql
        if stack_trace_threshold is not None:
            self._values["stack_trace_threshold"] = stack_trace_threshold
        if transaction_threshold_type is not None:
            self._values["transaction_threshold_type"] = transaction_threshold_type
        if transaction_threshold_value is not None:
            self._values["transaction_threshold_value"] = transaction_threshold_value

    @builtins.property
    def capture_memcache_keys(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable the capture of memcache keys from transaction traces.

        :schema: AgentConfigurationInputSettingsTransactionTracer#CaptureMemcacheKeys
        '''
        result = self._values.get("capture_memcache_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''If true, this enables the Transaction Tracer feature, enabling collection of transaction traces.

        :schema: AgentConfigurationInputSettingsTransactionTracer#Enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def explain_enabled(self) -> typing.Optional[builtins.bool]:
        '''If true, enables the collection of explain plans in transaction traces.

        :schema: AgentConfigurationInputSettingsTransactionTracer#ExplainEnabled
        '''
        result = self._values.get("explain_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def explain_threshold_type(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsTransactionTracerExplainThresholdType"]:
        '''Relevant only when explain_enabled is true.

        Can be set to automatic configuration (APDEX_F) or manual (see explainThresholdValue)

        :schema: AgentConfigurationInputSettingsTransactionTracer#ExplainThresholdType
        '''
        result = self._values.get("explain_threshold_type")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsTransactionTracerExplainThresholdType"], result)

    @builtins.property
    def explain_threshold_value(self) -> typing.Optional[jsii.Number]:
        '''Threshold (in seconds) above which the agent will collect explain plans.

        :schema: AgentConfigurationInputSettingsTransactionTracer#ExplainThresholdValue
        '''
        result = self._values.get("explain_threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def log_sql(self) -> typing.Optional[builtins.bool]:
        '''Set to true to enable logging of queries to the agent log file instead of uploading to New Relic.

        :schema: AgentConfigurationInputSettingsTransactionTracer#LogSql
        '''
        result = self._values.get("log_sql")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_sql(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsTransactionTracerRecordSql"]:
        '''Obfuscation level for SQL queries reported in transaction trace nodes.

        :schema: AgentConfigurationInputSettingsTransactionTracer#RecordSql
        '''
        result = self._values.get("record_sql")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsTransactionTracerRecordSql"], result)

    @builtins.property
    def stack_trace_threshold(self) -> typing.Optional[jsii.Number]:
        '''Specify a threshold in seconds.

        The agent includes stack traces in transaction trace nodes when the stack trace duration exceeds this threshold.

        :schema: AgentConfigurationInputSettingsTransactionTracer#StackTraceThreshold
        '''
        result = self._values.get("stack_trace_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transaction_threshold_type(
        self,
    ) -> typing.Optional["AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType"]:
        '''Relevant only when TransactionTracer is enabled.

        Can be set to automatic configuration (APDEX_F) or manual (see TransactionThresholdValue).

        :schema: AgentConfigurationInputSettingsTransactionTracer#TransactionThresholdType
        '''
        result = self._values.get("transaction_threshold_type")
        return typing.cast(typing.Optional["AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType"], result)

    @builtins.property
    def transaction_threshold_value(self) -> typing.Optional[jsii.Number]:
        '''Threshold (in seconds) that transactions with a duration longer than this threshold are eligible for transaction traces.

        :schema: AgentConfigurationInputSettingsTransactionTracer#TransactionThresholdValue
        '''
        result = self._values.get("transaction_threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AgentConfigurationInputSettingsTransactionTracer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsTransactionTracerExplainThresholdType"
)
class AgentConfigurationInputSettingsTransactionTracerExplainThresholdType(enum.Enum):
    '''Relevant only when explain_enabled is true.

    Can be set to automatic configuration (APDEX_F) or manual (see explainThresholdValue)

    :schema: AgentConfigurationInputSettingsTransactionTracerExplainThresholdType
    '''

    APDEX_F = "APDEX_F"
    '''APDEX_F.'''
    VALUE = "VALUE"
    '''VALUE.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsTransactionTracerRecordSql"
)
class AgentConfigurationInputSettingsTransactionTracerRecordSql(enum.Enum):
    '''Obfuscation level for SQL queries reported in transaction trace nodes.

    :schema: AgentConfigurationInputSettingsTransactionTracerRecordSql
    '''

    OBFUSCATED = "OBFUSCATED"
    '''OBFUSCATED.'''
    RAW = "RAW"
    '''RAW.'''
    OFF = "OFF"
    '''OFF.'''


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType"
)
class AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType(
    enum.Enum,
):
    '''Relevant only when TransactionTracer is enabled.

    Can be set to automatic configuration (APDEX_F) or manual (see TransactionThresholdValue).

    :schema: AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType
    '''

    APDEX_F = "APDEX_F"
    '''APDEX_F.'''
    VALUE = "VALUE"
    '''VALUE.'''


class CfnConfiguration(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.CfnConfiguration",
):
    '''A CloudFormation ``NewRelic::Agent::Configuration``.

    :cloudformationResource: NewRelic::Agent::Configuration
    :link: https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        agent_configuration: typing.Union[AgentConfigurationInput, typing.Dict[builtins.str, typing.Any]],
        guid: builtins.str,
    ) -> None:
        '''Create a new ``NewRelic::Agent::Configuration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param agent_configuration: 
        :param guid: The GUID for the affected Entity.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98b6392a81d326161e89acd8620e13c5899322f6d63cc4158be734495bbbdb3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationProps(
            agent_configuration=agent_configuration, guid=guid
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnConfigurationProps":
        '''Resource props.'''
        return typing.cast("CfnConfigurationProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-agent-configuration.CfnConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={"agent_configuration": "agentConfiguration", "guid": "guid"},
)
class CfnConfigurationProps:
    def __init__(
        self,
        *,
        agent_configuration: typing.Union[AgentConfigurationInput, typing.Dict[builtins.str, typing.Any]],
        guid: builtins.str,
    ) -> None:
        '''Manage New Relic Server-Side Agent Configuration.

        :param agent_configuration: 
        :param guid: The GUID for the affected Entity.

        :schema: CfnConfigurationProps
        '''
        if isinstance(agent_configuration, dict):
            agent_configuration = AgentConfigurationInput(**agent_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea5bdc0475decd5e223aa60c1d7b6791511b3f3b08b2afd7d46ae9c346952b3)
            check_type(argname="argument agent_configuration", value=agent_configuration, expected_type=type_hints["agent_configuration"])
            check_type(argname="argument guid", value=guid, expected_type=type_hints["guid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_configuration": agent_configuration,
            "guid": guid,
        }

    @builtins.property
    def agent_configuration(self) -> AgentConfigurationInput:
        '''
        :schema: CfnConfigurationProps#AgentConfiguration
        '''
        result = self._values.get("agent_configuration")
        assert result is not None, "Required property 'agent_configuration' is missing"
        return typing.cast(AgentConfigurationInput, result)

    @builtins.property
    def guid(self) -> builtins.str:
        '''The GUID for the affected Entity.

        :schema: CfnConfigurationProps#Guid
        '''
        result = self._values.get("guid")
        assert result is not None, "Required property 'guid' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AgentConfigurationInput",
    "AgentConfigurationInputSettings",
    "AgentConfigurationInputSettingsApmConfig",
    "AgentConfigurationInputSettingsBrowserConfig",
    "AgentConfigurationInputSettingsErrorCollector",
    "AgentConfigurationInputSettingsSlowSql",
    "AgentConfigurationInputSettingsThreadProfiler",
    "AgentConfigurationInputSettingsTracerType",
    "AgentConfigurationInputSettingsTracerTypeValue",
    "AgentConfigurationInputSettingsTransactionTracer",
    "AgentConfigurationInputSettingsTransactionTracerExplainThresholdType",
    "AgentConfigurationInputSettingsTransactionTracerRecordSql",
    "AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType",
    "CfnConfiguration",
    "CfnConfigurationProps",
]

publication.publish()

def _typecheckingstub__ab52a3c8e8048c6f73869865b33ff3566d716f8d39ebdbbcdfa239842420ab77(
    *,
    settings: typing.Optional[typing.Union[AgentConfigurationInputSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6254e0f3eb1d566a852bb9cb2188b37356c1674a9dfcc5caf75a86b751fcceef(
    *,
    alias: typing.Optional[builtins.str] = None,
    apm_config: typing.Optional[typing.Union[AgentConfigurationInputSettingsApmConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    browser_config: typing.Optional[typing.Union[AgentConfigurationInputSettingsBrowserConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    error_collector: typing.Optional[typing.Union[AgentConfigurationInputSettingsErrorCollector, typing.Dict[builtins.str, typing.Any]]] = None,
    slow_sql: typing.Optional[typing.Union[AgentConfigurationInputSettingsSlowSql, typing.Dict[builtins.str, typing.Any]]] = None,
    thread_profiler: typing.Optional[typing.Union[AgentConfigurationInputSettingsThreadProfiler, typing.Dict[builtins.str, typing.Any]]] = None,
    tracer_type: typing.Optional[typing.Union[AgentConfigurationInputSettingsTracerType, typing.Dict[builtins.str, typing.Any]]] = None,
    transaction_tracer: typing.Optional[typing.Union[AgentConfigurationInputSettingsTransactionTracer, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ae29d45520d6cc6ec140bde1121c1087a77481b23513d49ebb0ac5acda2ed5(
    *,
    apdex_target: typing.Optional[jsii.Number] = None,
    use_server_side_config: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4973440c04ffb65a8ca18cef1a01720ee3d1591ea405e304530a096478323d5(
    *,
    apdex_target: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee7deb5b965725dcfc21bf0929320029e7ca6555d985fef886b1d598fa01fa62(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    expected_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    expected_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignored_error_classes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignored_error_codes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c66ae2c9a6f3a6908dc4542f647e18d48c7905b36923dd2e92d0a77472fa374(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a716eb07cfef10647959f1c46dbeea1343672e4997f7d93f1fd6448ca9bf846(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d1b5d811fcea1289c4ac88b58a277c4aa328655058990f3d9cd6f3315bb2202(
    *,
    value: typing.Optional[AgentConfigurationInputSettingsTracerTypeValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54bc86215566a26758cc5c10d103ca08883011b05fb1060bf3c73630e837aa33(
    *,
    capture_memcache_keys: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    explain_enabled: typing.Optional[builtins.bool] = None,
    explain_threshold_type: typing.Optional[AgentConfigurationInputSettingsTransactionTracerExplainThresholdType] = None,
    explain_threshold_value: typing.Optional[jsii.Number] = None,
    log_sql: typing.Optional[builtins.bool] = None,
    record_sql: typing.Optional[AgentConfigurationInputSettingsTransactionTracerRecordSql] = None,
    stack_trace_threshold: typing.Optional[jsii.Number] = None,
    transaction_threshold_type: typing.Optional[AgentConfigurationInputSettingsTransactionTracerTransactionThresholdType] = None,
    transaction_threshold_value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98b6392a81d326161e89acd8620e13c5899322f6d63cc4158be734495bbbdb3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    agent_configuration: typing.Union[AgentConfigurationInput, typing.Dict[builtins.str, typing.Any]],
    guid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea5bdc0475decd5e223aa60c1d7b6791511b3f3b08b2afd7d46ae9c346952b3(
    *,
    agent_configuration: typing.Union[AgentConfigurationInput, typing.Dict[builtins.str, typing.Any]],
    guid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
