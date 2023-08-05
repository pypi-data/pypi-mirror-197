# EM27 Metadata

This repository is the single source of truth for our EM27 measurement logistics: "Where has each station been on each day of measurements?" We selected this format over putting it in a database due to various reasons:

-   Easy to read, modify and extend by selective group members using GitHub permissions
-   Changes to this are more obvious here than in database logs
-   Versioning (easy to revert mistakes)
-   Automatic testing of the files integrities
-   Easy import as a statically typed Python library

<br/>

## What does this data look like?

There is a set of locations in **`data/locations.json`**:

```json
[
    {
        "location_id": "BRU",
        "details": "Industriegelände an der Brudermühlstraße",
        "lon": 11.547,
        "lat": 48.111,
        "alt": 528
    },
    {
        "location_id": "DLR",
        "details": "DLR in Wessling",
        "lon": 11.279,
        "lat": 48.086,
        "alt": 592
    }
]
```

There is a set of sensors in **`data/sensors.json`** that measure at these location sites:

```json
[
    {
        "sensor_id": "ma",
        "serial_number": 61,
        "utc_offsets": [
            { "from_date": "20150826", "to_date": "20220623", "utc_offset": 0 },
            { "from_date": "20220624", "to_date": "20220926", "utc_offset": 2 },
            { "from_date": "20220927", "to_date": "20221231", "utc_offset": 0 }
        ],
        "different_pressure_data_source": [
            {
                "from_date": "20220626",
                "to_date": "20220926",
                "source": "LMU-MIM01-height-adjusted"
            },
            {
                "from_date": "20220626",
                "to_date": "20220926",
                "source": "mc"
            }
        ],
        "pressure_calibration_factors": [
            { "from_date": "20150826", "to_date": "20221231", "factor": 1 }
        ],
        "locations": [
            { "from_date": "20181019", "to_date": "20181019", "location": "TUM_LAB" },
            { "from_date": "20181020", "to_date": "20181030", "location": "LMU" },
            { "from_date": "20181031", "to_date": "20220515", "location": "TUM_I" }
        ]
    }
]
```

There is a set of campaigns in **`data/campaigns.json`**:

```json
[
    {
        "campaign_id": "muccnet",
        "from_date": "20190913",
        "to_date": "21000101",
        "stations": [
            { "sensor": "ma", "default_location": "TUM_I", "direction": "center" },
            { "sensor": "mb", "default_location": "FEL", "direction": "east" },
            { "sensor": "mc", "default_location": "GRAE", "direction": "west" },
            { "sensor": "md", "default_location": "OBE", "direction": "north" },
            { "sensor": "me", "default_location": "TAU", "direction": "south" }
        ]
    }
]
```

<br/>

## How to add new measurement days?

1. Possibly add new locations in `data/locations.json`
2. Extend the list of locations in `data/sensors.json`
3. Possibly add new campaign setups in `data/campaigns.json`

<br/>

## How can I know whether my changes were correct?

Whenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed [here](https://github.com/tum-esm/em27-location-data/actions). If some have failed you can ask Moritz Makowski.

A list of all integrity checks can be found in [`tests/README.md`](https://github.com/tum-esm/em27-location-data/tree/main/tests).

<br/>

## How to use it in your codebase?

1. Install python library

```bash
poetry add tum_esm_em27_metadata
# or
pip install tum_esm_em27_metadata
```

2. Create a personal access token for a GitHub account that has read access to the metadata repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

3. Use the metadata anywhere

```python
import tum_esm_em27_metadata

em27_metadata_interface = tum_esm_em27_metadata.load_from_github(
    github_repository = "org-name/repo-name",
    access_token = "ghp_..."
)

metadata = em27_metadata_interface.get(
    sensor_id = "ma", date = "20220601"
)  # is of type tum_esm_em27_metadata.types.SensorDataContext

print(metadata.dict())
```

... prints out:

```json
{
    "sensor_id": "ma",
    "serial_number": 61,
    "utc_offset": 0,
    "pressure_data_source": "ma",
    "pressure_calibration_factor": 1,
    "date": "20220601",
    "location": {
        "location_id": "TUM_I",
        "details": "TUM Dach Innenstadt",
        "lon": 11.569,
        "lat": 48.151,
        "alt": 539
    }
}
```

<br/>

## For Developers: Publish the Packaga to PyPI

```bash
poetry build
poetry publish
```
