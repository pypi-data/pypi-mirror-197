from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Dict

from volosti_common.person.typedefs import (
    FullName,
    HashedPassword,
    ShortName,
    Username,
)

if sys.version_info < (3, 10):
    SLOTS: Dict[str, bool] = {}
else:
    SLOTS: Dict[str, bool] = {'slots': True}


@dataclass(**SLOTS)
class Account:
    username: Username
    hashed_password: HashedPassword
    profiles: list[Profile]


@dataclass(**SLOTS)
class Profile:
    short_name: ShortName
    full_name: FullName
