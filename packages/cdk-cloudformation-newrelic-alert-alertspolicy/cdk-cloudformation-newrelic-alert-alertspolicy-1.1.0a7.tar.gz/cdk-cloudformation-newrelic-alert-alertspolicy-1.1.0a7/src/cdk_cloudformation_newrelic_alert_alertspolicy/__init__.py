'''
# newrelic-alert-alertspolicy

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `NewRelic::Alert::AlertsPolicy` v1.1.0.

## Description

Manage New Relic AlertsPolicy

## References

* [Documentation](https://github.com/aws-ia/cloudformation-newrelic-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name NewRelic::Alert::AlertsPolicy \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/NewRelic-Alert-AlertsPolicy \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `NewRelic::Alert::AlertsPolicy`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fnewrelic-alert-alertspolicy+v1.1.0).
* Issues related to `NewRelic::Alert::AlertsPolicy` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-newrelic-resource-providers).

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
    jsii_type="@cdk-cloudformation/newrelic-alert-alertspolicy.AlertsPolicyInput",
    jsii_struct_bases=[],
    name_mapping={"incident_preference": "incidentPreference", "name": "name"},
)
class AlertsPolicyInput:
    def __init__(
        self,
        *,
        incident_preference: typing.Optional["AlertsPolicyInputIncidentPreference"] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param incident_preference: 
        :param name: Name of the alerts policy.

        :schema: AlertsPolicyInput
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f93694b132f84761cbe0f5e98500b1631c08057988c51583452e3b3905c89d0)
            check_type(argname="argument incident_preference", value=incident_preference, expected_type=type_hints["incident_preference"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if incident_preference is not None:
            self._values["incident_preference"] = incident_preference
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def incident_preference(
        self,
    ) -> typing.Optional["AlertsPolicyInputIncidentPreference"]:
        '''
        :schema: AlertsPolicyInput#IncidentPreference
        '''
        result = self._values.get("incident_preference")
        return typing.cast(typing.Optional["AlertsPolicyInputIncidentPreference"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the alerts policy.

        :schema: AlertsPolicyInput#Name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertsPolicyInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/newrelic-alert-alertspolicy.AlertsPolicyInputIncidentPreference"
)
class AlertsPolicyInputIncidentPreference(enum.Enum):
    '''
    :schema: AlertsPolicyInputIncidentPreference
    '''

    PER_CONDITION = "PER_CONDITION"
    '''PER_CONDITION.'''
    PER_CONDITION_AND_TARGET = "PER_CONDITION_AND_TARGET"
    '''PER_CONDITION_AND_TARGET.'''
    PER_POLICY = "PER_POLICY"
    '''PER_POLICY.'''


class CfnAlertsPolicy(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/newrelic-alert-alertspolicy.CfnAlertsPolicy",
):
    '''A CloudFormation ``NewRelic::Alert::AlertsPolicy``.

    :cloudformationResource: NewRelic::Alert::AlertsPolicy
    :link: https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account_id: jsii.Number,
        alerts_policy: typing.Union[AlertsPolicyInput, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Create a new ``NewRelic::Alert::AlertsPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param account_id: Account ID the alerts policy should belong to.
        :param alerts_policy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c0d6572abbf8b53dd98ede7b77667dae3942bf7a7743b0a09cd02bec430f99)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAlertsPolicyProps(
            account_id=account_id, alerts_policy=alerts_policy
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAlertsPolicyId")
    def attr_alerts_policy_id(self) -> jsii.Number:
        '''Attribute ``NewRelic::Alert::AlertsPolicy.AlertsPolicyId``.

        :link: https://github.com/aws-ia/cloudformation-newrelic-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAlertsPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAlertsPolicyProps":
        '''Resource props.'''
        return typing.cast("CfnAlertsPolicyProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/newrelic-alert-alertspolicy.CfnAlertsPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "alerts_policy": "alertsPolicy"},
)
class CfnAlertsPolicyProps:
    def __init__(
        self,
        *,
        account_id: jsii.Number,
        alerts_policy: typing.Union[AlertsPolicyInput, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Manage New Relic AlertsPolicy.

        :param account_id: Account ID the alerts policy should belong to.
        :param alerts_policy: 

        :schema: CfnAlertsPolicyProps
        '''
        if isinstance(alerts_policy, dict):
            alerts_policy = AlertsPolicyInput(**alerts_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99785532a88894d765710642978a0430364e4d4e165a6fe560aeddddf94cceb4)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument alerts_policy", value=alerts_policy, expected_type=type_hints["alerts_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "alerts_policy": alerts_policy,
        }

    @builtins.property
    def account_id(self) -> jsii.Number:
        '''Account ID the alerts policy should belong to.

        :schema: CfnAlertsPolicyProps#AccountId
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def alerts_policy(self) -> AlertsPolicyInput:
        '''
        :schema: CfnAlertsPolicyProps#AlertsPolicy
        '''
        result = self._values.get("alerts_policy")
        assert result is not None, "Required property 'alerts_policy' is missing"
        return typing.cast(AlertsPolicyInput, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlertsPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlertsPolicyInput",
    "AlertsPolicyInputIncidentPreference",
    "CfnAlertsPolicy",
    "CfnAlertsPolicyProps",
]

publication.publish()

def _typecheckingstub__5f93694b132f84761cbe0f5e98500b1631c08057988c51583452e3b3905c89d0(
    *,
    incident_preference: typing.Optional[AlertsPolicyInputIncidentPreference] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c0d6572abbf8b53dd98ede7b77667dae3942bf7a7743b0a09cd02bec430f99(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account_id: jsii.Number,
    alerts_policy: typing.Union[AlertsPolicyInput, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99785532a88894d765710642978a0430364e4d4e165a6fe560aeddddf94cceb4(
    *,
    account_id: jsii.Number,
    alerts_policy: typing.Union[AlertsPolicyInput, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass
