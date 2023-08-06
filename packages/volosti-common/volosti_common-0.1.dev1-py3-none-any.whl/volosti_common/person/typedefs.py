from typing import NewType

Username = NewType('Username', str)
RawPassword = NewType('RawPassword', str)
HashedPassword = NewType('HashedPassword', str)

ShortName = NewType('ShortName', str)
FullName = NewType('FullName', str)
