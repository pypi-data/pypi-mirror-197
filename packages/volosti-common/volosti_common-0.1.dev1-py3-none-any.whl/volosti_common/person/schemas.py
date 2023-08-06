from __future__ import annotations

from marshmallow import fields, validate

from volosti_common.common.schemas import TypedSchema
from volosti_common.person import queries, regexps

MAX_USERNAME_LENGTH = 32
INITIAL_USERNAME = fields.String(
    validate=validate.And(
        validate.Length(max=MAX_USERNAME_LENGTH),
        validate.Regexp(regexps.USERNAME),
    ),
    required=True,
)
CONFIRMING_USERNAME = fields.String(
    validate=validate.And(
        validate.Length(max=MAX_USERNAME_LENGTH),
    ),
    required=True,
)

MAX_PASSWORD_LENGTH = 256
INITIAL_RAW_PASSWORD = fields.String(
    validate=validate.And(
        validate.Length(min=8, max=MAX_PASSWORD_LENGTH),
        validate.Regexp(regexps.RAW_PASSWORD),
    ),
    required=True,
)
CONFIRMING_RAW_PASSWORD = fields.String(
    validate=validate.Length(max=MAX_PASSWORD_LENGTH),
    required=True,
)


class AccountChange(TypedSchema[queries.AccountChange]):
    __post_load_type__ = queries.AccountChange
    username = INITIAL_USERNAME


class PasswordChange(TypedSchema[queries.PasswordChange]):
    __post_load_type__ = queries.PasswordChange
    current_password = CONFIRMING_RAW_PASSWORD
    new_password = INITIAL_RAW_PASSWORD
    confirm_password = CONFIRMING_RAW_PASSWORD


class SignIn(TypedSchema[queries.SignIn]):
    __post_load_type__ = queries.SignIn
    username = CONFIRMING_USERNAME
    password = CONFIRMING_RAW_PASSWORD


class SignUp(TypedSchema[queries.SignUp]):
    __post_load_type__ = queries.SignUp
    username = INITIAL_USERNAME
    password = INITIAL_RAW_PASSWORD
    confirm_password = CONFIRMING_RAW_PASSWORD
