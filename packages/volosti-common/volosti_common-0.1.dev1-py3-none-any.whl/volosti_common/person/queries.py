import typing

from typing_extensions import NotRequired

from volosti_common.person.typedefs import (
    FullName,
    RawPassword,
    ShortName,
    Username,
)


class AccountChange(typing.TypedDict, total=False):
    username: Username


class PasswordChange(typing.TypedDict):
    current_password: RawPassword
    new_password: RawPassword
    confirm_password: RawPassword


class ProfileChange(typing.TypedDict, total=False):
    short_name: ShortName
    full_name: FullName


class SignIn(typing.TypedDict):
    username: Username
    password: RawPassword


class SignUp(typing.TypedDict):
    username: Username
    password: RawPassword
    confirm_password: RawPassword
