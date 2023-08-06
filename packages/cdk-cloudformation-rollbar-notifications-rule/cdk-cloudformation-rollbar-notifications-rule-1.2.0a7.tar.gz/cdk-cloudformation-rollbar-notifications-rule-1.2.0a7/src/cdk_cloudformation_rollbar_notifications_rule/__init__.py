'''
# rollbar-notifications-rule

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Rollbar::Notifications::Rule` v1.2.0.

## Description

Manage a notification rule for Rollbar.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-rollbar-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Rollbar::Notifications::Rule \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Rollbar-Notifications-Rule \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Rollbar::Notifications::Rule`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Frollbar-notifications-rule+v1.2.0).
* Issues related to `Rollbar::Notifications::Rule` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-rollbar-resource-providers).

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


class CfnRule(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.CfnRule",
):
    '''A CloudFormation ``Rollbar::Notifications::Rule``.

    :cloudformationResource: Rollbar::Notifications::Rule
    :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        email: typing.Optional[typing.Union["EmailRule", typing.Dict[builtins.str, typing.Any]]] = None,
        pager_duty: typing.Optional[typing.Union["PagerDutyRule", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["SlackRule", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook: typing.Optional[typing.Union["WebhookRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Rollbar::Notifications::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param email: 
        :param pager_duty: 
        :param slack: 
        :param webhook: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f867ea34e88c70473affad9e332b8e3257a3453557ebbcc95b490187dd8fb3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            email=email, pager_duty=pager_duty, slack=slack, webhook=webhook
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAction")
    def attr_action(self) -> builtins.str:
        '''Attribute ``Rollbar::Notifications::Rule.Action``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAction"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``Rollbar::Notifications::Rule.Id``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleType")
    def attr_rule_type(self) -> builtins.str:
        '''Attribute ``Rollbar::Notifications::Rule.RuleType``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleType"))

    @builtins.property
    @jsii.member(jsii_name="attrTrigger")
    def attr_trigger(self) -> builtins.str:
        '''Attribute ``Rollbar::Notifications::Rule.Trigger``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTrigger"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnRuleProps":
        '''Resource props.'''
        return typing.cast("CfnRuleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "pager_duty": "pagerDuty",
        "slack": "slack",
        "webhook": "webhook",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        email: typing.Optional[typing.Union["EmailRule", typing.Dict[builtins.str, typing.Any]]] = None,
        pager_duty: typing.Optional[typing.Union["PagerDutyRule", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["SlackRule", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook: typing.Optional[typing.Union["WebhookRule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Manage a notification rule for Rollbar.

        :param email: 
        :param pager_duty: 
        :param slack: 
        :param webhook: 

        :schema: CfnRuleProps
        '''
        if isinstance(email, dict):
            email = EmailRule(**email)
        if isinstance(pager_duty, dict):
            pager_duty = PagerDutyRule(**pager_duty)
        if isinstance(slack, dict):
            slack = SlackRule(**slack)
        if isinstance(webhook, dict):
            webhook = WebhookRule(**webhook)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b313356dfccec89383cb49c7e79817b9000d150050d076cbbfb3cbe9ebc6d747)
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument pager_duty", value=pager_duty, expected_type=type_hints["pager_duty"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if pager_duty is not None:
            self._values["pager_duty"] = pager_duty
        if slack is not None:
            self._values["slack"] = slack
        if webhook is not None:
            self._values["webhook"] = webhook

    @builtins.property
    def email(self) -> typing.Optional["EmailRule"]:
        '''
        :schema: CfnRuleProps#Email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional["EmailRule"], result)

    @builtins.property
    def pager_duty(self) -> typing.Optional["PagerDutyRule"]:
        '''
        :schema: CfnRuleProps#PagerDuty
        '''
        result = self._values.get("pager_duty")
        return typing.cast(typing.Optional["PagerDutyRule"], result)

    @builtins.property
    def slack(self) -> typing.Optional["SlackRule"]:
        '''
        :schema: CfnRuleProps#Slack
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["SlackRule"], result)

    @builtins.property
    def webhook(self) -> typing.Optional["WebhookRule"]:
        '''
        :schema: CfnRuleProps#Webhook
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional["WebhookRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.EmailRule",
    jsii_struct_bases=[],
    name_mapping={
        "trigger": "trigger",
        "action": "action",
        "config": "config",
        "filters": "filters",
    },
)
class EmailRule:
    def __init__(
        self,
        *,
        trigger: "EmailTrigger",
        action: typing.Optional[builtins.str] = None,
        config: typing.Any = None,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Create Email notification rules.

        :param trigger: 
        :param action: The action associated with this rule.
        :param config: 
        :param filters: 

        :schema: EmailRule
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b736a35eb1c458acdf57b7a5395abc2ed0c2c1400f2c8f2c232eda5f0abd02)
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger": trigger,
        }
        if action is not None:
            self._values["action"] = action
        if config is not None:
            self._values["config"] = config
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def trigger(self) -> "EmailTrigger":
        '''
        :schema: EmailRule#Trigger
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("EmailTrigger", result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action associated with this rule.

        :schema: EmailRule#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Any:
        '''
        :schema: EmailRule#Config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''
        :schema: EmailRule#Filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/rollbar-notifications-rule.EmailTrigger")
class EmailTrigger(enum.Enum):
    '''An error/ message is seen for the first time.

    :schema: EmailTrigger
    '''

    NEW_ITEM = "NEW_ITEM"
    '''new_item.'''
    OCCURRENCE = "OCCURRENCE"
    '''occurrence.'''
    DEPLOY = "DEPLOY"
    '''deploy.'''
    REACTIVATED_ITEM = "REACTIVATED_ITEM"
    '''reactivated_item.'''
    RESOLVED_ITEM = "RESOLVED_ITEM"
    '''resolved_item.'''
    NEW_VERSION = "NEW_VERSION"
    '''new_version.'''
    REOPENED_ITEM = "REOPENED_ITEM"
    '''reopened_item.'''
    OCCURRENCE_RATE = "OCCURRENCE_RATE"
    '''occurrence_rate.'''
    EXP_REPEAT_ITEM = "EXP_REPEAT_ITEM"
    '''exp_repeat_item.'''
    DAILY_SUMMARY = "DAILY_SUMMARY"
    '''daily_summary.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.PagerDutyConfig",
    jsii_struct_bases=[],
    name_mapping={"service_key": "serviceKey"},
)
class PagerDutyConfig:
    def __init__(self, *, service_key: typing.Optional[builtins.str] = None) -> None:
        '''
        :param service_key: PagerDuty Service API Key.

        :schema: PagerDutyConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b2a846986e3e1a11d44c9b2f9ebf67d48909432bd5342251ed69adb45dfa7e0)
            check_type(argname="argument service_key", value=service_key, expected_type=type_hints["service_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if service_key is not None:
            self._values["service_key"] = service_key

    @builtins.property
    def service_key(self) -> typing.Optional[builtins.str]:
        '''PagerDuty Service API Key.

        :schema: PagerDutyConfig#ServiceKey
        '''
        result = self._values.get("service_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagerDutyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.PagerDutyRule",
    jsii_struct_bases=[],
    name_mapping={
        "trigger": "trigger",
        "action": "action",
        "config": "config",
        "filters": "filters",
    },
)
class PagerDutyRule:
    def __init__(
        self,
        *,
        trigger: "PagerDutyTrigger",
        action: typing.Optional[builtins.str] = None,
        config: typing.Optional[typing.Union[PagerDutyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Create PagerDuty notification rules.

        :param trigger: 
        :param action: The action associated with this rule.
        :param config: 
        :param filters: 

        :schema: PagerDutyRule
        '''
        if isinstance(config, dict):
            config = PagerDutyConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ff0a04a7daadbb4527c51821efadbed81c4dd9f316562a42fe5aae7a0209a8)
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger": trigger,
        }
        if action is not None:
            self._values["action"] = action
        if config is not None:
            self._values["config"] = config
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def trigger(self) -> "PagerDutyTrigger":
        '''
        :schema: PagerDutyRule#Trigger
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("PagerDutyTrigger", result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action associated with this rule.

        :schema: PagerDutyRule#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Optional[PagerDutyConfig]:
        '''
        :schema: PagerDutyRule#Config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[PagerDutyConfig], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''
        :schema: PagerDutyRule#Filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagerDutyRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/rollbar-notifications-rule.PagerDutyTrigger")
class PagerDutyTrigger(enum.Enum):
    '''An error/ message is seen for the first time.

    :schema: PagerDutyTrigger
    '''

    NEW_ITEM = "NEW_ITEM"
    '''new_item.'''
    REACTIVATED_ITEM = "REACTIVATED_ITEM"
    '''reactivated_item.'''
    RESOLVED_ITEM = "RESOLVED_ITEM"
    '''resolved_item.'''
    OCCURRENCE_RATE = "OCCURRENCE_RATE"
    '''occurrence_rate.'''
    EXP_REPEAT_ITEM = "EXP_REPEAT_ITEM"
    '''exp_repeat_item.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.SlackRule",
    jsii_struct_bases=[],
    name_mapping={
        "trigger": "trigger",
        "action": "action",
        "config": "config",
        "filters": "filters",
    },
)
class SlackRule:
    def __init__(
        self,
        *,
        trigger: "SlackTrigger",
        action: typing.Optional[builtins.str] = None,
        config: typing.Any = None,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Create Slack notification rule.

        :param trigger: 
        :param action: The action associated with this rule.
        :param config: 
        :param filters: 

        :schema: SlackRule
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__780f6bd18349be802ea236c8f7dd4d998eb24833d6abef09b723ac00dbb3fb3c)
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger": trigger,
        }
        if action is not None:
            self._values["action"] = action
        if config is not None:
            self._values["config"] = config
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def trigger(self) -> "SlackTrigger":
        '''
        :schema: SlackRule#Trigger
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("SlackTrigger", result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action associated with this rule.

        :schema: SlackRule#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Any:
        '''
        :schema: SlackRule#Config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''
        :schema: SlackRule#Filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/rollbar-notifications-rule.SlackTrigger")
class SlackTrigger(enum.Enum):
    '''An error/ message is seen for the first time.

    :schema: SlackTrigger
    '''

    NEW_ITEM = "NEW_ITEM"
    '''new_item.'''
    OCCURRENCE = "OCCURRENCE"
    '''occurrence.'''
    DEPLOY = "DEPLOY"
    '''deploy.'''
    REACTIVATED_ITEM = "REACTIVATED_ITEM"
    '''reactivated_item.'''
    RESOLVED_ITEM = "RESOLVED_ITEM"
    '''resolved_item.'''
    NEW_VERSION = "NEW_VERSION"
    '''new_version.'''
    REOPENED_ITEM = "REOPENED_ITEM"
    '''reopened_item.'''
    OCCURRENCE_RATE = "OCCURRENCE_RATE"
    '''occurrence_rate.'''
    EXP_REPEAT_ITEM = "EXP_REPEAT_ITEM"
    '''exp_repeat_item.'''


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.WebhookConfig",
    jsii_struct_bases=[],
    name_mapping={"format": "format", "url": "url"},
)
class WebhookConfig:
    def __init__(
        self,
        *,
        format: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param format: Request/response format can be JSON or XML.
        :param url: Defines a webhook url for this specific rule.

        :schema: WebhookConfig
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2de09e02964be0b8c9380064edde5f1aa2040faa8732cce75376fcbca64791)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if format is not None:
            self._values["format"] = format
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''Request/response format can be JSON or XML.

        :schema: WebhookConfig#Format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''Defines a webhook url for this specific rule.

        :schema: WebhookConfig#Url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebhookConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-notifications-rule.WebhookRule",
    jsii_struct_bases=[],
    name_mapping={
        "trigger": "trigger",
        "action": "action",
        "config": "config",
        "filters": "filters",
    },
)
class WebhookRule:
    def __init__(
        self,
        *,
        trigger: "WebhookTrigger",
        action: typing.Optional[builtins.str] = None,
        config: typing.Optional[typing.Union[WebhookConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        filters: typing.Optional[typing.Sequence[typing.Any]] = None,
    ) -> None:
        '''Create Webhook notification rules.

        :param trigger: 
        :param action: The action associated with this rule.
        :param config: 
        :param filters: 

        :schema: WebhookRule
        '''
        if isinstance(config, dict):
            config = WebhookConfig(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8110816e1b9c5126a73974232ec9420ad5089e899fd72e19704b48b611801185)
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "trigger": trigger,
        }
        if action is not None:
            self._values["action"] = action
        if config is not None:
            self._values["config"] = config
        if filters is not None:
            self._values["filters"] = filters

    @builtins.property
    def trigger(self) -> "WebhookTrigger":
        '''
        :schema: WebhookRule#Trigger
        '''
        result = self._values.get("trigger")
        assert result is not None, "Required property 'trigger' is missing"
        return typing.cast("WebhookTrigger", result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action associated with this rule.

        :schema: WebhookRule#Action
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config(self) -> typing.Optional[WebhookConfig]:
        '''
        :schema: WebhookRule#Config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[WebhookConfig], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[typing.Any]]:
        '''
        :schema: WebhookRule#Filters
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebhookRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/rollbar-notifications-rule.WebhookTrigger")
class WebhookTrigger(enum.Enum):
    '''An error/ message is seen for the first time.

    :schema: WebhookTrigger
    '''

    NEW_ITEM = "NEW_ITEM"
    '''new_item.'''
    OCCURRENCE = "OCCURRENCE"
    '''occurrence.'''
    DEPLOY = "DEPLOY"
    '''deploy.'''
    REACTIVATED_ITEM = "REACTIVATED_ITEM"
    '''reactivated_item.'''
    RESOLVED_ITEM = "RESOLVED_ITEM"
    '''resolved_item.'''
    EXP_REPEAT_ITEM = "EXP_REPEAT_ITEM"
    '''exp_repeat_item.'''
    REOPENED_ITEM = "REOPENED_ITEM"
    '''reopened_item.'''
    OCCURRENCE_RATE = "OCCURRENCE_RATE"
    '''occurrence_rate.'''


__all__ = [
    "CfnRule",
    "CfnRuleProps",
    "EmailRule",
    "EmailTrigger",
    "PagerDutyConfig",
    "PagerDutyRule",
    "PagerDutyTrigger",
    "SlackRule",
    "SlackTrigger",
    "WebhookConfig",
    "WebhookRule",
    "WebhookTrigger",
]

publication.publish()

def _typecheckingstub__9f867ea34e88c70473affad9e332b8e3257a3453557ebbcc95b490187dd8fb3f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    email: typing.Optional[typing.Union[EmailRule, typing.Dict[builtins.str, typing.Any]]] = None,
    pager_duty: typing.Optional[typing.Union[PagerDutyRule, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[SlackRule, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook: typing.Optional[typing.Union[WebhookRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b313356dfccec89383cb49c7e79817b9000d150050d076cbbfb3cbe9ebc6d747(
    *,
    email: typing.Optional[typing.Union[EmailRule, typing.Dict[builtins.str, typing.Any]]] = None,
    pager_duty: typing.Optional[typing.Union[PagerDutyRule, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[SlackRule, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook: typing.Optional[typing.Union[WebhookRule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b736a35eb1c458acdf57b7a5395abc2ed0c2c1400f2c8f2c232eda5f0abd02(
    *,
    trigger: EmailTrigger,
    action: typing.Optional[builtins.str] = None,
    config: typing.Any = None,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b2a846986e3e1a11d44c9b2f9ebf67d48909432bd5342251ed69adb45dfa7e0(
    *,
    service_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ff0a04a7daadbb4527c51821efadbed81c4dd9f316562a42fe5aae7a0209a8(
    *,
    trigger: PagerDutyTrigger,
    action: typing.Optional[builtins.str] = None,
    config: typing.Optional[typing.Union[PagerDutyConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780f6bd18349be802ea236c8f7dd4d998eb24833d6abef09b723ac00dbb3fb3c(
    *,
    trigger: SlackTrigger,
    action: typing.Optional[builtins.str] = None,
    config: typing.Any = None,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2de09e02964be0b8c9380064edde5f1aa2040faa8732cce75376fcbca64791(
    *,
    format: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8110816e1b9c5126a73974232ec9420ad5089e899fd72e19704b48b611801185(
    *,
    trigger: WebhookTrigger,
    action: typing.Optional[builtins.str] = None,
    config: typing.Optional[typing.Union[WebhookConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    filters: typing.Optional[typing.Sequence[typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass
