from _typeshed import Incomplete as Incomplete
from tum_esm_em27_metadata import types as types
from typing import Optional

class EM27MetadataInterface:
    locations: Incomplete
    sensors: Incomplete
    campaigns: Incomplete
    location_ids: Incomplete
    sensor_ids: Incomplete
    campaign_ids: Incomplete
    def __init__(self, locations: list[types.Location], sensors: list[types.Sensor], campaigns: list[types.Campaign]) -> None: ...
    def get(self, sensor_id: str, date: str) -> types.SensorDataContext: ...

def load_from_github(github_repository: str, access_token: Optional[str] = ...) -> EM27MetadataInterface: ...
