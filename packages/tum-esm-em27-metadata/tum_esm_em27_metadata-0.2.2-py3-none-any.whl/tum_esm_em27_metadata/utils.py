from datetime import datetime, timedelta
import json
from . import types
from typing import Any, Optional, Union
import requests

ALLOWED_EXTRA_PRESSURE_DATA_SOURCES = ["LMU-MIM01-height-adjusted"]


def request_github_file(
    github_repository: str,
    filepath: str,
    access_token: Optional[str] = None,
) -> list[Any]:
    """Sends a request and returns the content of the response, in unicode."""
    response = requests.get(
        f"https://raw.githubusercontent.com/{github_repository}/main/{filepath}",
        headers={
            "Authorization": f"token {access_token}",
            "Accept": "application/text",
        },
        timeout=10,
    )
    response.raise_for_status()
    return list(json.loads(response.text))


def test_data_integrity(
    locations: list[types.Location],
    sensors: list[types.Sensor],
    campaigns: list[types.Campaign],
) -> None:
    location_ids = [s.location_id for s in locations]
    sensor_ids = [s.sensor_id for s in sensors]
    campaign_ids = [s.campaign_id for s in campaigns]

    # unique ids
    assert len(set(location_ids)) == len(location_ids), "location ids are not unique"
    assert len(set(sensor_ids)) == len(sensor_ids), "sensor ids are not unique"
    assert len(set(campaign_ids)) == len(campaign_ids), "campaign ids are not unique"

    # reference existence in sensors.json
    for s in sensors:
        for l in s.locations:
            assert l.location_id in location_ids, f"unknown location id {l.location_id}"
        for p in s.different_pressure_data_source:
            assert p.source in (
                sensor_ids + ALLOWED_EXTRA_PRESSURE_DATA_SOURCES
            ), f"unknown pressure data source {p.source}"

    # reference existence in campaigns.json
    for c in campaigns:
        for s2 in c.stations:
            assert (
                s2.default_location_id in location_ids
            ), f"unknown location id {s2.default_location_id}"
            assert s2.sensor_id in sensor_ids, f"unknown sensor id {s2.sensor_id}"

    # integrity of time series in sensors.json
    for s in sensors:

        # TEST TIME SERIES INTEGRITY OF "utc_offsets",
        # "pressure_calibration_factors", and "locations"
        xss: list[
            Union[
                list[types.SensorUTCOffset],
                list[types.SensorPressureCalibrationFactor],
                list[types.SensorLocation],
            ]
        ] = [s.utc_offsets, s.pressure_calibration_factors, s.locations]
        for xs in xss:
            for x in xs:
                assert x.from_date <= x.to_date, (
                    "from_date has to smaller than to_date " + f"({x.from_date} > {x.to_date})"
                )
            for i in range(len(xs) - 1):
                x1, x2 = xs[i : i + 2]
                expected_x2_from_date = (
                    datetime.strptime(x1.to_date, "%Y%m%d") + timedelta(days=1)
                ).strftime("%Y%m%d")
                assert not (
                    expected_x2_from_date > x2.from_date
                ), f"time periods are overlapping: {x1.dict()}, {x1.dict()}"
                assert not (
                    expected_x2_from_date < x2.from_date
                ), f"time periods have gaps: {x1.dict()}, {x1.dict()}"

        # TEST TIME SERIES INTEGRITY OF "different_pressure_data_source"
        for x in s.different_pressure_data_source:
            assert x.from_date <= x.to_date, (
                "from_date has to smaller than to_date " + f"({x.from_date} > {x.to_date})"
            )
        for i in range(len(s.different_pressure_data_source) - 1):
            x1, x2 = s.different_pressure_data_source[i : i + 2]
            expected_x2_from_date = (
                datetime.strptime(x1.to_date, "%Y%m%d") + timedelta(days=1)
            ).strftime("%Y%m%d")
            assert not (
                expected_x2_from_date > x2.from_date
            ), f"time periods are overlapping: {x1.dict()}, {x1.dict()}"

        # TEST INTEGRITY OF ADJACENT "utc_offset" ITEMS
        for o1, o2 in zip(s.utc_offsets[:-1], s.utc_offsets[1:]):
            assert (
                o1.utc_offset != o2.utc_offset
            ), "two neighboring date ranges should not have the same utc_offset"

        # TEST INTEGRITY OF ADJACENT "utc_offset" ITEMS
        for p1, p2 in zip(s.pressure_calibration_factors[:-1], s.pressure_calibration_factors[1:]):
            assert (
                p1.factor != p2.factor
            ), "two neighboring date ranges should not have the same pressure calibration factor"

        # TEST INTEGRITY OF ADJACENT "utc_offset" ITEMS
        for l1, l2 in zip(s.locations[:-1], s.locations[1:]):
            assert (
                l1.location_id != l2.location_id
            ), "two neighboring date ranges should not have the same location_id"
