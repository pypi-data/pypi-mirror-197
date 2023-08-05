from typing import Any, Callable, Optional
from tum_esm_em27_metadata import types, utils


class EM27MetadataInterface:
    def __init__(
        self,
        locations: list[types.Location],
        sensors: list[types.Sensor],
        campaigns: list[types.Campaign],
    ):
        self.locations = locations
        self.sensors = sensors
        self.campaigns = campaigns

        self.location_ids = [s.location_id for s in self.locations]
        self.sensor_ids = [s.sensor_id for s in self.sensors]
        self.campaign_ids = [s.campaign_id for s in self.campaigns]

        utils.test_data_integrity(self.locations, self.sensors, self.campaigns)

    def get(self, sensor_id: str, date: str) -> types.SensorDataContext:
        """
        For a given `sensor_id` and `date`, return the metadata. Returns
        the `pydantic` type `tum_esm_em27_metadata.types.SensorDataContext`:

        ```python
        from pydantic import BaseModel

        class Location(BaseModel):
            location_id: str
            details: str
            lon: float
            lat: float
            alt: float

        class SensorDataContext(BaseModel):
            sensor_id: str
            serial_number: int
            utc_offset: float
            pressure_data_source: str
            pressure_calibration_factor: float
            date: str
            location: Location
        ```
        """

        # get the sensor
        assert sensor_id in self.sensor_ids, f'No location data for sensor_id "{sensor_id}"'
        sensor = list(filter(lambda s: s.sensor_id == sensor_id, self.sensors))[0]

        # get utc offset
        utc_offset_matches = list(
            filter(
                lambda o: o.from_date <= date <= o.to_date,
                sensor.utc_offsets,
            )
        )
        assert len(utc_offset_matches) == 1, f"no utc offset data for {sensor_id}/{date}"
        utc_offset = utc_offset_matches[0].utc_offset

        # get pressure data source
        pressure_data_source_matches = list(
            filter(
                lambda o: o.from_date <= date <= o.to_date,
                sensor.different_pressure_data_source,
            )
        )
        pressure_data_source = (
            sensor_id
            if len(pressure_data_source_matches) == 0
            else pressure_data_source_matches[0].source
        )

        # get pressure calibration factor
        pressure_calibration_factor_matches = list(
            filter(
                lambda o: o.from_date <= date <= o.to_date,
                sensor.pressure_calibration_factors,
            )
        )
        assert (
            len(pressure_calibration_factor_matches) == 1
        ), f"no pressure calibration data for {sensor_id}/{date}"
        pressure_calibration_factor = pressure_calibration_factor_matches[0].factor

        # get location at that date
        location_matches = list(
            filter(
                lambda l: l.from_date <= date <= l.to_date,
                sensor.locations,
            )
        )
        assert len(location_matches) == 1, f"no location data for {sensor_id}/{date}"
        location_id = location_matches[0].location_id
        location = list(filter(lambda l: l.location_id == location_id, self.locations))[0]

        # bundle the context
        return types.SensorDataContext(
            sensor_id=sensor_id,
            serial_number=sensor.serial_number,
            utc_offset=utc_offset,
            pressure_data_source=pressure_data_source,
            pressure_calibration_factor=pressure_calibration_factor,
            date=date,
            location=location,
        )


def load_from_github(
    github_repository: str,
    access_token: Optional[str] = None,
) -> EM27MetadataInterface:
    """loads an EM27MetadataInterface from GitHub"""

    _req: Callable[[str], list[Any]] = lambda t: utils.request_github_file(
        github_repository=github_repository,
        filepath=f"data/{t}.json",
        access_token=access_token,
    )

    return EM27MetadataInterface(
        locations=[types.Location(**l) for l in _req("locations")],
        sensors=[types.Sensor(**l) for l in _req("sensors")],
        campaigns=[types.Campaign(**l) for l in _req("campaigns")],
    )
