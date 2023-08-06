'''
# rollbar-teams-team

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Rollbar::Teams::Team` v1.2.0.

## Description

Manage a team on Rollbar.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-rollbar-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Rollbar::Teams::Team \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Rollbar-Teams-Team \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Rollbar::Teams::Team`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Frollbar-teams-team+v1.2.0).
* Issues related to `Rollbar::Teams::Team` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-rollbar-resource-providers).

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


class CfnTeam(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/rollbar-teams-team.CfnTeam",
):
    '''A CloudFormation ``Rollbar::Teams::Team``.

    :cloudformationResource: Rollbar::Teams::Team
    :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_level: "CfnTeamPropsAccessLevel",
        name: builtins.str,
    ) -> None:
        '''Create a new ``Rollbar::Teams::Team``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param access_level: Can be standard, light, or view.
        :param name: Name of the team. Max length 32 characters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c132af3956fed0e7ff14f5dbb39e5a412e434f242df9cdfa6a3ccdc4d67123c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTeamProps(access_level=access_level, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccountId")
    def attr_account_id(self) -> jsii.Number:
        '''Attribute ``Rollbar::Teams::Team.AccountId``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAccountId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> jsii.Number:
        '''Attribute ``Rollbar::Teams::Team.Id``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnTeamProps":
        '''Resource props.'''
        return typing.cast("CfnTeamProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-teams-team.CfnTeamProps",
    jsii_struct_bases=[],
    name_mapping={"access_level": "accessLevel", "name": "name"},
)
class CfnTeamProps:
    def __init__(
        self,
        *,
        access_level: "CfnTeamPropsAccessLevel",
        name: builtins.str,
    ) -> None:
        '''Manage a team on Rollbar.

        :param access_level: Can be standard, light, or view.
        :param name: Name of the team. Max length 32 characters.

        :schema: CfnTeamProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e42e092d717c029a8192357e552bbe045c243f22e37f0fa2ff59712b6b436c)
            check_type(argname="argument access_level", value=access_level, expected_type=type_hints["access_level"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_level": access_level,
            "name": name,
        }

    @builtins.property
    def access_level(self) -> "CfnTeamPropsAccessLevel":
        '''Can be standard, light, or view.

        :schema: CfnTeamProps#AccessLevel
        '''
        result = self._values.get("access_level")
        assert result is not None, "Required property 'access_level' is missing"
        return typing.cast("CfnTeamPropsAccessLevel", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the team.

        Max length 32 characters.

        :schema: CfnTeamProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTeamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@cdk-cloudformation/rollbar-teams-team.CfnTeamPropsAccessLevel")
class CfnTeamPropsAccessLevel(enum.Enum):
    '''Can be standard, light, or view.

    :schema: CfnTeamPropsAccessLevel
    '''

    STANDARD = "STANDARD"
    '''standard.'''
    LIGHT = "LIGHT"
    '''light.'''
    VIEW = "VIEW"
    '''view.'''


__all__ = [
    "CfnTeam",
    "CfnTeamProps",
    "CfnTeamPropsAccessLevel",
]

publication.publish()

def _typecheckingstub__c132af3956fed0e7ff14f5dbb39e5a412e434f242df9cdfa6a3ccdc4d67123c7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_level: CfnTeamPropsAccessLevel,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e42e092d717c029a8192357e552bbe045c243f22e37f0fa2ff59712b6b436c(
    *,
    access_level: CfnTeamPropsAccessLevel,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
