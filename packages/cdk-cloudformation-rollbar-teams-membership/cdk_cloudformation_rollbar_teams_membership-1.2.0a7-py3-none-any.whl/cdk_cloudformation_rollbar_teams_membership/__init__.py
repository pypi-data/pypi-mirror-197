'''
# rollbar-teams-membership

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Rollbar::Teams::Membership` v1.2.0.

## Description

Manage a team membership for a user or project on Rollbar.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-rollbar-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Rollbar::Teams::Membership \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Rollbar-Teams-Membership \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Rollbar::Teams::Membership`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Frollbar-teams-membership+v1.2.0).
* Issues related to `Rollbar::Teams::Membership` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-rollbar-resource-providers).

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


class CfnMembership(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/rollbar-teams-membership.CfnMembership",
):
    '''A CloudFormation ``Rollbar::Teams::Membership``.

    :cloudformationResource: Rollbar::Teams::Membership
    :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        member_id: jsii.Number,
        member_type: "CfnMembershipPropsMemberType",
        team_id: jsii.Number,
    ) -> None:
        '''Create a new ``Rollbar::Teams::Membership``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param member_id: The ID of the user or project to associate to the team.
        :param member_type: The type of membership.
        :param team_id: The team ID for the membership.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea123e27cc75e5bdca242b9e1d8833a80d30ee39589663f2f2784871538691c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMembershipProps(
            member_id=member_id, member_type=member_type, team_id=team_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnMembershipProps":
        '''Resource props.'''
        return typing.cast("CfnMembershipProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-teams-membership.CfnMembershipProps",
    jsii_struct_bases=[],
    name_mapping={
        "member_id": "memberId",
        "member_type": "memberType",
        "team_id": "teamId",
    },
)
class CfnMembershipProps:
    def __init__(
        self,
        *,
        member_id: jsii.Number,
        member_type: "CfnMembershipPropsMemberType",
        team_id: jsii.Number,
    ) -> None:
        '''Manage a team membership for a user or project on Rollbar.

        :param member_id: The ID of the user or project to associate to the team.
        :param member_type: The type of membership.
        :param team_id: The team ID for the membership.

        :schema: CfnMembershipProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafc1ebd3b0652566323493da91f11c969a38424f2525ddd7c4f12e19f069ce8)
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
            check_type(argname="argument member_type", value=member_type, expected_type=type_hints["member_type"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "member_id": member_id,
            "member_type": member_type,
            "team_id": team_id,
        }

    @builtins.property
    def member_id(self) -> jsii.Number:
        '''The ID of the user or project to associate to the team.

        :schema: CfnMembershipProps#MemberId
        '''
        result = self._values.get("member_id")
        assert result is not None, "Required property 'member_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def member_type(self) -> "CfnMembershipPropsMemberType":
        '''The type of membership.

        :schema: CfnMembershipProps#MemberType
        '''
        result = self._values.get("member_type")
        assert result is not None, "Required property 'member_type' is missing"
        return typing.cast("CfnMembershipPropsMemberType", result)

    @builtins.property
    def team_id(self) -> jsii.Number:
        '''The team ID for the membership.

        :schema: CfnMembershipProps#TeamId
        '''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMembershipProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/rollbar-teams-membership.CfnMembershipPropsMemberType"
)
class CfnMembershipPropsMemberType(enum.Enum):
    '''The type of membership.

    :schema: CfnMembershipPropsMemberType
    '''

    USER = "USER"
    '''user.'''
    PROJECT = "PROJECT"
    '''project.'''


__all__ = [
    "CfnMembership",
    "CfnMembershipProps",
    "CfnMembershipPropsMemberType",
]

publication.publish()

def _typecheckingstub__eea123e27cc75e5bdca242b9e1d8833a80d30ee39589663f2f2784871538691c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    member_id: jsii.Number,
    member_type: CfnMembershipPropsMemberType,
    team_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafc1ebd3b0652566323493da91f11c969a38424f2525ddd7c4f12e19f069ce8(
    *,
    member_id: jsii.Number,
    member_type: CfnMembershipPropsMemberType,
    team_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
