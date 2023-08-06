'''
# rollbar-projects-project

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Rollbar::Projects::Project` v1.1.0.

## Description

Manage a project on Rollbar.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-rollbar-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Rollbar::Projects::Project \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Rollbar-Projects-Project \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Rollbar::Projects::Project`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Frollbar-projects-project+v1.1.0).
* Issues related to `Rollbar::Projects::Project` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-rollbar-resource-providers).

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


class CfnProject(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/rollbar-projects-project.CfnProject",
):
    '''A CloudFormation ``Rollbar::Projects::Project``.

    :cloudformationResource: Rollbar::Projects::Project
    :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        email: typing.Optional[typing.Union["Email", typing.Dict[builtins.str, typing.Any]]] = None,
        pager_duty: typing.Optional[typing.Union["PagerDuty", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["Slack", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook: typing.Optional[typing.Union["Webhook", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new ``Rollbar::Projects::Project``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Name of the project. Must start with a letter; can contain letters, numbers, spaces, underscores, hyphens, periods, and commas. Max length 32 characters.
        :param email: 
        :param pager_duty: 
        :param slack: 
        :param webhook: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80fa35ccaa438e0c5a732e7a096acb34bf262c309214b2541e93590ceff8829)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProjectProps(
            name=name, email=email, pager_duty=pager_duty, slack=slack, webhook=webhook
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountId")
    def attr_account_id(self) -> jsii.Number:
        '''Attribute ``Rollbar::Projects::Project.AccountId``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``Rollbar::Projects::Project.Id``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Attribute ``Rollbar::Projects::Project.Status``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnProjectProps":
        '''Resource props.'''
        return typing.cast("CfnProjectProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-projects-project.CfnProjectProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "email": "email",
        "pager_duty": "pagerDuty",
        "slack": "slack",
        "webhook": "webhook",
    },
)
class CfnProjectProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        email: typing.Optional[typing.Union["Email", typing.Dict[builtins.str, typing.Any]]] = None,
        pager_duty: typing.Optional[typing.Union["PagerDuty", typing.Dict[builtins.str, typing.Any]]] = None,
        slack: typing.Optional[typing.Union["Slack", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook: typing.Optional[typing.Union["Webhook", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Manage a project on Rollbar.

        :param name: Name of the project. Must start with a letter; can contain letters, numbers, spaces, underscores, hyphens, periods, and commas. Max length 32 characters.
        :param email: 
        :param pager_duty: 
        :param slack: 
        :param webhook: 

        :schema: CfnProjectProps
        '''
        if isinstance(email, dict):
            email = Email(**email)
        if isinstance(pager_duty, dict):
            pager_duty = PagerDuty(**pager_duty)
        if isinstance(slack, dict):
            slack = Slack(**slack)
        if isinstance(webhook, dict):
            webhook = Webhook(**webhook)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03da369a28f1f2025a1ca071206300b2d1c4ad1e1c957bb5875cdec979bb623d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument email", value=email, expected_type=type_hints["email"])
            check_type(argname="argument pager_duty", value=pager_duty, expected_type=type_hints["pager_duty"])
            check_type(argname="argument slack", value=slack, expected_type=type_hints["slack"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if email is not None:
            self._values["email"] = email
        if pager_duty is not None:
            self._values["pager_duty"] = pager_duty
        if slack is not None:
            self._values["slack"] = slack
        if webhook is not None:
            self._values["webhook"] = webhook

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the project.

        Must start with a letter; can contain letters, numbers, spaces, underscores, hyphens, periods, and commas. Max length 32 characters.

        :schema: CfnProjectProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def email(self) -> typing.Optional["Email"]:
        '''
        :schema: CfnProjectProps#Email
        '''
        result = self._values.get("email")
        return typing.cast(typing.Optional["Email"], result)

    @builtins.property
    def pager_duty(self) -> typing.Optional["PagerDuty"]:
        '''
        :schema: CfnProjectProps#PagerDuty
        '''
        result = self._values.get("pager_duty")
        return typing.cast(typing.Optional["PagerDuty"], result)

    @builtins.property
    def slack(self) -> typing.Optional["Slack"]:
        '''
        :schema: CfnProjectProps#Slack
        '''
        result = self._values.get("slack")
        return typing.cast(typing.Optional["Slack"], result)

    @builtins.property
    def webhook(self) -> typing.Optional["Webhook"]:
        '''
        :schema: CfnProjectProps#Webhook
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional["Webhook"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-projects-project.Email",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "include_request_params": "includeRequestParams",
    },
)
class Email:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        include_request_params: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configuring Email notifications integration.

        :param enabled: Enable the Email notifications globally.
        :param include_request_params: Whether to include request parameters.

        :schema: Email
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62867bddcb348e8f14e187d3b68f340fee9de5aa3d4be1e493fbcb032dfb1b66)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument include_request_params", value=include_request_params, expected_type=type_hints["include_request_params"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if include_request_params is not None:
            self._values["include_request_params"] = include_request_params

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Enable the Email notifications globally.

        :schema: Email#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def include_request_params(self) -> typing.Optional[builtins.bool]:
        '''Whether to include request parameters.

        :schema: Email#IncludeRequestParams
        '''
        result = self._values.get("include_request_params")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Email(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-projects-project.PagerDuty",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "service_key": "serviceKey"},
)
class PagerDuty:
    def __init__(self, *, enabled: builtins.bool, service_key: builtins.str) -> None:
        '''Configuring PagerDuty notifications integration.

        :param enabled: Enable the PagerDuty notifications globally.
        :param service_key: PagerDuty Service API Key.

        :schema: PagerDuty
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1712e562d32e8811295c6614faaef12cc87499cb6fbfdd1da5d91c3a256f72)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_key", value=service_key, expected_type=type_hints["service_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "service_key": service_key,
        }

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Enable the PagerDuty notifications globally.

        :schema: PagerDuty#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def service_key(self) -> builtins.str:
        '''PagerDuty Service API Key.

        :schema: PagerDuty#ServiceKey
        '''
        result = self._values.get("service_key")
        assert result is not None, "Required property 'service_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PagerDuty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-projects-project.Slack",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "enabled": "enabled",
        "service_account_id": "serviceAccountId",
        "show_message_buttons": "showMessageButtons",
    },
)
class Slack:
    def __init__(
        self,
        *,
        channel: builtins.str,
        enabled: builtins.bool,
        service_account_id: jsii.Number,
        show_message_buttons: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configuring Slack notifications integration.

        :param channel: The default Slack channel to send the messages.
        :param enabled: Enable the Slack notifications globally.
        :param service_account_id: You can find your Service Account ID in https://rollbar.com/settings/integrations/#slack.
        :param show_message_buttons: Show the Slack actionable buttons.

        :schema: Slack
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dafa82447552f4b8d9ba030d2161e2f06c53d42aa62f0b898978fe1fe74cadb)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_account_id", value=service_account_id, expected_type=type_hints["service_account_id"])
            check_type(argname="argument show_message_buttons", value=show_message_buttons, expected_type=type_hints["show_message_buttons"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel": channel,
            "enabled": enabled,
            "service_account_id": service_account_id,
        }
        if show_message_buttons is not None:
            self._values["show_message_buttons"] = show_message_buttons

    @builtins.property
    def channel(self) -> builtins.str:
        '''The default Slack channel to send the messages.

        :schema: Slack#Channel
        '''
        result = self._values.get("channel")
        assert result is not None, "Required property 'channel' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Enable the Slack notifications globally.

        :schema: Slack#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def service_account_id(self) -> jsii.Number:
        '''You can find your Service Account ID in https://rollbar.com/settings/integrations/#slack.

        :schema: Slack#ServiceAccountId
        '''
        result = self._values.get("service_account_id")
        assert result is not None, "Required property 'service_account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def show_message_buttons(self) -> typing.Optional[builtins.bool]:
        '''Show the Slack actionable buttons.

        :schema: Slack#ShowMessageButtons
        '''
        result = self._values.get("show_message_buttons")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Slack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-projects-project.Webhook",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "url": "url"},
)
class Webhook:
    def __init__(self, *, enabled: builtins.bool, url: builtins.str) -> None:
        '''Configuring Webhook notifications integration.

        :param enabled: Enable the webhook notifications globally.
        :param url: The webhook url.

        :schema: Webhook
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac920542acfd990b49126e7758a9dd36b500df4187ee114184727bd76c3dc64)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
            "url": url,
        }

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''Enable the webhook notifications globally.

        :schema: Webhook#Enabled
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The webhook url.

        :schema: Webhook#Url
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Webhook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProject",
    "CfnProjectProps",
    "Email",
    "PagerDuty",
    "Slack",
    "Webhook",
]

publication.publish()

def _typecheckingstub__a80fa35ccaa438e0c5a732e7a096acb34bf262c309214b2541e93590ceff8829(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    email: typing.Optional[typing.Union[Email, typing.Dict[builtins.str, typing.Any]]] = None,
    pager_duty: typing.Optional[typing.Union[PagerDuty, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[Slack, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook: typing.Optional[typing.Union[Webhook, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03da369a28f1f2025a1ca071206300b2d1c4ad1e1c957bb5875cdec979bb623d(
    *,
    name: builtins.str,
    email: typing.Optional[typing.Union[Email, typing.Dict[builtins.str, typing.Any]]] = None,
    pager_duty: typing.Optional[typing.Union[PagerDuty, typing.Dict[builtins.str, typing.Any]]] = None,
    slack: typing.Optional[typing.Union[Slack, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook: typing.Optional[typing.Union[Webhook, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62867bddcb348e8f14e187d3b68f340fee9de5aa3d4be1e493fbcb032dfb1b66(
    *,
    enabled: builtins.bool,
    include_request_params: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1712e562d32e8811295c6614faaef12cc87499cb6fbfdd1da5d91c3a256f72(
    *,
    enabled: builtins.bool,
    service_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dafa82447552f4b8d9ba030d2161e2f06c53d42aa62f0b898978fe1fe74cadb(
    *,
    channel: builtins.str,
    enabled: builtins.bool,
    service_account_id: jsii.Number,
    show_message_buttons: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac920542acfd990b49126e7758a9dd36b500df4187ee114184727bd76c3dc64(
    *,
    enabled: builtins.bool,
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
