'''
[![NPM version](https://badge.fury.io/js/cdk-http-pinger.svg)](https://badge.fury.io/js/cdk-http-pinger)
[![PyPI version](https://badge.fury.io/py/cdk-http-pinger.svg)](https://badge.fury.io/py/cdk-http-pinger)
![Release](https://github.com/pahud/cdk-http-pinger/workflows/Release/badge.svg?branch=main)

# `cdk-http-pinger`

HTTP Pinger for AWS CDK

# Sample

```python
import { Pinger } from 'cdk-http-pinger';

const app = new App();

const stack = new Stack(app, 'my-stack');

const pinger = new Pinger(stack, 'Pinger', { url: 'https://aws.amazon.com' });

new CfnOutput(stack, 'HttpStatus', { value: pinger.httpStatus });
new CfnOutput(stack, 'HtmlTitle', { value: pinger.htmlTitle });
new CfnOutput(stack, 'URL', { value: pinger.url });
new CfnOutput(stack, 'Body', { value: pinger.body });
```
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


@jsii.enum(jsii_type="cdk-http-pinger.HttpMethod")
class HttpMethod(enum.Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"


class Pinger(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-http-pinger.Pinger",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        url: builtins.str,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[HttpMethod] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param url: 
        :param data: HTTP DATA. Default: - no http data used
        :param method: The HTTP Method. Default: HttpMethod.GET
        :param timeout: Timeout. Default: 1 minutes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a73ed248bb0cf7192d97d562bb953977c05ed040de65821d4eb1523aaf12469)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PingerProps(url=url, data=data, method=method, timeout=timeout)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="body")
    def body(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "body"))

    @builtins.property
    @jsii.member(jsii_name="htmlTitle")
    def html_title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "htmlTitle"))

    @builtins.property
    @jsii.member(jsii_name="httpStatus")
    def http_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpStatus"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_ceddda9d.CustomResource:
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))


@jsii.data_type(
    jsii_type="cdk-http-pinger.PingerProps",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "data": "data",
        "method": "method",
        "timeout": "timeout",
    },
)
class PingerProps:
    def __init__(
        self,
        *,
        url: builtins.str,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        method: typing.Optional[HttpMethod] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param url: 
        :param data: HTTP DATA. Default: - no http data used
        :param method: The HTTP Method. Default: HttpMethod.GET
        :param timeout: Timeout. Default: 1 minutes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83455327d976958de52c95c6806053f4e0ac105723991d4dc26f64723cfdcf36)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if data is not None:
            self._values["data"] = data
        if method is not None:
            self._values["method"] = method
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def url(self) -> builtins.str:
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''HTTP DATA.

        :default: - no http data used
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def method(self) -> typing.Optional[HttpMethod]:
        '''The HTTP Method.

        :default: HttpMethod.GET
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[HttpMethod], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Timeout.

        :default: 1 minutes
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PingerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpMethod",
    "Pinger",
    "PingerProps",
]

publication.publish()

def _typecheckingstub__4a73ed248bb0cf7192d97d562bb953977c05ed040de65821d4eb1523aaf12469(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    url: builtins.str,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    method: typing.Optional[HttpMethod] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83455327d976958de52c95c6806053f4e0ac105723991d4dc26f64723cfdcf36(
    *,
    url: builtins.str,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    method: typing.Optional[HttpMethod] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
