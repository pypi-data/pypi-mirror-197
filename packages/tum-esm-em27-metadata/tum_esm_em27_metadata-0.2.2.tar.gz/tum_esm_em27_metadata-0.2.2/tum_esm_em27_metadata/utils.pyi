from . import types as types
from _typeshed import Incomplete as Incomplete
from typing import Any, Optional

ALLOWED_EXTRA_PRESSURE_DATA_SOURCES: Incomplete

def request_github_file(github_repository: str, filepath: str, access_token: Optional[str] = ...) -> list[Any]: ...
def test_data_integrity(locations: list[types.Location], sensors: list[types.Sensor], campaigns: list[types.Campaign]) -> None: ...
