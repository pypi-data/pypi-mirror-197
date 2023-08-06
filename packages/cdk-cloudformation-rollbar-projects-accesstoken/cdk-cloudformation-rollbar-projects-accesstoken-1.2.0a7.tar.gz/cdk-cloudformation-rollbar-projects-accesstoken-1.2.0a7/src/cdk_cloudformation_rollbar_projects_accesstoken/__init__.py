'''
# rollbar-projects-accesstoken

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Rollbar::Projects::AccessToken` v1.2.0.

## Description

Manage an access token for a Rollbar project.

## References

* [Documentation](https://github.com/aws-ia/cloudformation-rollbar-resource-providers)
* [Source](https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git)

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Rollbar::Projects::AccessToken \
  --publisher-id c830e97710da0c9954d80ba8df021e5439e7134b \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/c830e97710da0c9954d80ba8df021e5439e7134b/Rollbar-Projects-AccessToken \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Rollbar::Projects::AccessToken`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Frollbar-projects-accesstoken+v1.2.0).
* Issues related to `Rollbar::Projects::AccessToken` should be reported to the [publisher](https://github.com/aws-ia/cloudformation-rollbar-resource-providers).

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


class CfnAccessToken(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/rollbar-projects-accesstoken.CfnAccessToken",
):
    '''A CloudFormation ``Rollbar::Projects::AccessToken``.

    :cloudformationResource: Rollbar::Projects::AccessToken
    :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        project_id: jsii.Number,
        scopes: typing.Sequence["CfnAccessTokenPropsScopes"],
        rate_limit_window_count: typing.Optional[jsii.Number] = None,
        rate_limit_window_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``Rollbar::Projects::AccessToken``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Name to identify the access token.
        :param project_id: The project ID.
        :param scopes: Scopes to assign to the create access token.
        :param rate_limit_window_count: Number of requests for the defined rate limiting period.
        :param rate_limit_window_size: Period of time (in seconds) for the rate limit configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aefc5f3a0613e2365ba52526d96249fd49ec8bae7c06f22a4f6cda791576401)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessTokenProps(
            name=name,
            project_id=project_id,
            scopes=scopes,
            rate_limit_window_count=rate_limit_window_count,
            rate_limit_window_size=rate_limit_window_size,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAccessToken")
    def attr_access_token(self) -> builtins.str:
        '''Attribute ``Rollbar::Projects::AccessToken.AccessToken``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAccessToken"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''Attribute ``Rollbar::Projects::AccessToken.Status``.

        :link: https://github.com/aws-ia/cloudformation-rollbar-resource-providers.git
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnAccessTokenProps":
        '''Resource props.'''
        return typing.cast("CfnAccessTokenProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/rollbar-projects-accesstoken.CfnAccessTokenProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "project_id": "projectId",
        "scopes": "scopes",
        "rate_limit_window_count": "rateLimitWindowCount",
        "rate_limit_window_size": "rateLimitWindowSize",
    },
)
class CfnAccessTokenProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        project_id: jsii.Number,
        scopes: typing.Sequence["CfnAccessTokenPropsScopes"],
        rate_limit_window_count: typing.Optional[jsii.Number] = None,
        rate_limit_window_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Manage an access token for a Rollbar project.

        :param name: Name to identify the access token.
        :param project_id: The project ID.
        :param scopes: Scopes to assign to the create access token.
        :param rate_limit_window_count: Number of requests for the defined rate limiting period.
        :param rate_limit_window_size: Period of time (in seconds) for the rate limit configuration.

        :schema: CfnAccessTokenProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a218c5eb748a31ff61fe82ac9177008ad820c74781d78834b097f53f37027bca)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument rate_limit_window_count", value=rate_limit_window_count, expected_type=type_hints["rate_limit_window_count"])
            check_type(argname="argument rate_limit_window_size", value=rate_limit_window_size, expected_type=type_hints["rate_limit_window_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project_id": project_id,
            "scopes": scopes,
        }
        if rate_limit_window_count is not None:
            self._values["rate_limit_window_count"] = rate_limit_window_count
        if rate_limit_window_size is not None:
            self._values["rate_limit_window_size"] = rate_limit_window_size

    @builtins.property
    def name(self) -> builtins.str:
        '''Name to identify the access token.

        :schema: CfnAccessTokenProps#Name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> jsii.Number:
        '''The project ID.

        :schema: CfnAccessTokenProps#ProjectId
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scopes(self) -> typing.List["CfnAccessTokenPropsScopes"]:
        '''Scopes to assign to the create access token.

        :schema: CfnAccessTokenProps#Scopes
        '''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List["CfnAccessTokenPropsScopes"], result)

    @builtins.property
    def rate_limit_window_count(self) -> typing.Optional[jsii.Number]:
        '''Number of requests for the defined rate limiting period.

        :schema: CfnAccessTokenProps#RateLimitWindowCount
        '''
        result = self._values.get("rate_limit_window_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rate_limit_window_size(self) -> typing.Optional[jsii.Number]:
        '''Period of time (in seconds) for the rate limit configuration.

        :schema: CfnAccessTokenProps#RateLimitWindowSize
        '''
        result = self._values.get("rate_limit_window_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessTokenProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdk-cloudformation/rollbar-projects-accesstoken.CfnAccessTokenPropsScopes"
)
class CfnAccessTokenPropsScopes(enum.Enum):
    '''
    :schema: CfnAccessTokenPropsScopes
    '''

    WRITE = "WRITE"
    '''write.'''
    READ = "READ"
    '''read.'''
    POST_SERVER_ITEM = "POST_SERVER_ITEM"
    '''post_server_item.'''
    POST_CLIENT_ITEM = "POST_CLIENT_ITEM"
    '''post_client_item.'''


__all__ = [
    "CfnAccessToken",
    "CfnAccessTokenProps",
    "CfnAccessTokenPropsScopes",
]

publication.publish()

def _typecheckingstub__1aefc5f3a0613e2365ba52526d96249fd49ec8bae7c06f22a4f6cda791576401(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    project_id: jsii.Number,
    scopes: typing.Sequence[CfnAccessTokenPropsScopes],
    rate_limit_window_count: typing.Optional[jsii.Number] = None,
    rate_limit_window_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a218c5eb748a31ff61fe82ac9177008ad820c74781d78834b097f53f37027bca(
    *,
    name: builtins.str,
    project_id: jsii.Number,
    scopes: typing.Sequence[CfnAccessTokenPropsScopes],
    rate_limit_window_count: typing.Optional[jsii.Number] = None,
    rate_limit_window_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
