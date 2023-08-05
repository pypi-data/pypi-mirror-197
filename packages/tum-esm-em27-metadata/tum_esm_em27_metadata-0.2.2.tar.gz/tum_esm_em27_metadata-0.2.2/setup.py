# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tum_esm_em27_metadata']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'types-requests>=2.28.11.8,<3.0.0.0']

setup_kwargs = {
    'name': 'tum-esm-em27-metadata',
    'version': '0.2.2',
    'description': "single source of truth for ESM's EM27 measurement logistics",
    'long_description': '# EM27 Metadata\n\nThis repository is the single source of truth for our EM27 measurement logistics: "Where has each station been on each day of measurements?" We selected this format over putting it in a database due to various reasons:\n\n-   Easy to read, modify and extend by selective group members using GitHub permissions\n-   Changes to this are more obvious here than in database logs\n-   Versioning (easy to revert mistakes)\n-   Automatic testing of the files integrities\n-   Easy import as a statically typed Python library\n\n<br/>\n\n## What does this data look like?\n\nThere is a set of locations in **`data/locations.json`**:\n\n```json\n[\n    {\n        "location_id": "BRU",\n        "details": "Industriegelände an der Brudermühlstraße",\n        "lon": 11.547,\n        "lat": 48.111,\n        "alt": 528\n    },\n    {\n        "location_id": "DLR",\n        "details": "DLR in Wessling",\n        "lon": 11.279,\n        "lat": 48.086,\n        "alt": 592\n    }\n]\n```\n\nThere is a set of sensors in **`data/sensors.json`** that measure at these location sites:\n\n```json\n[\n    {\n        "sensor_id": "ma",\n        "serial_number": 61,\n        "utc_offsets": [\n            { "from_date": "20150826", "to_date": "20220623", "utc_offset": 0 },\n            { "from_date": "20220624", "to_date": "20220926", "utc_offset": 2 },\n            { "from_date": "20220927", "to_date": "20221231", "utc_offset": 0 }\n        ],\n        "different_pressure_data_source": [\n            {\n                "from_date": "20220626",\n                "to_date": "20220926",\n                "source": "LMU-MIM01-height-adjusted"\n            },\n            {\n                "from_date": "20220626",\n                "to_date": "20220926",\n                "source": "mc"\n            }\n        ],\n        "pressure_calibration_factors": [\n            { "from_date": "20150826", "to_date": "20221231", "factor": 1 }\n        ],\n        "locations": [\n            { "from_date": "20181019", "to_date": "20181019", "location": "TUM_LAB" },\n            { "from_date": "20181020", "to_date": "20181030", "location": "LMU" },\n            { "from_date": "20181031", "to_date": "20220515", "location": "TUM_I" }\n        ]\n    }\n]\n```\n\nThere is a set of campaigns in **`data/campaigns.json`**:\n\n```json\n[\n    {\n        "campaign_id": "muccnet",\n        "from_date": "20190913",\n        "to_date": "21000101",\n        "stations": [\n            { "sensor": "ma", "default_location": "TUM_I", "direction": "center" },\n            { "sensor": "mb", "default_location": "FEL", "direction": "east" },\n            { "sensor": "mc", "default_location": "GRAE", "direction": "west" },\n            { "sensor": "md", "default_location": "OBE", "direction": "north" },\n            { "sensor": "me", "default_location": "TAU", "direction": "south" }\n        ]\n    }\n]\n```\n\n<br/>\n\n## How to add new measurement days?\n\n1. Possibly add new locations in `data/locations.json`\n2. Extend the list of locations in `data/sensors.json`\n3. Possibly add new campaign setups in `data/campaigns.json`\n\n<br/>\n\n## How can I know whether my changes were correct?\n\nWhenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed [here](https://github.com/tum-esm/em27-location-data/actions). If some have failed you can ask Moritz Makowski.\n\nA list of all integrity checks can be found in [`tests/README.md`](https://github.com/tum-esm/em27-location-data/tree/main/tests).\n\n<br/>\n\n## How to use it in your codebase?\n\n1. Install python library\n\n```bash\npoetry add tum_esm_em27_metadata\n# or\npip install tum_esm_em27_metadata\n```\n\n2. Create a personal access token for a GitHub account that has read access to the metadata repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\n\n3. Use the metadata anywhere\n\n```python\nimport tum_esm_em27_metadata\n\nem27_metadata_interface = tum_esm_em27_metadata.load_from_github(\n    github_repository = "org-name/repo-name",\n    access_token = "ghp_..."\n)\n\nmetadata = em27_metadata_interface.get(\n    sensor_id = "ma", date = "20220601"\n)  # is of type tum_esm_em27_metadata.types.SensorDataContext\n\nprint(metadata.dict())\n```\n\n... prints out:\n\n```json\n{\n    "sensor_id": "ma",\n    "serial_number": 61,\n    "utc_offset": 0,\n    "pressure_data_source": "ma",\n    "pressure_calibration_factor": 1,\n    "date": "20220601",\n    "location": {\n        "location_id": "TUM_I",\n        "details": "TUM Dach Innenstadt",\n        "lon": 11.569,\n        "lat": 48.151,\n        "alt": 539\n    }\n}\n```\n\n<br/>\n\n## For Developers: Publish the Packaga to PyPI\n\n```bash\nstubgen tum_esm_em27_metadata --output . && poetry build\npoetry publish\n```\n',
    'author': 'Moritz Makowski',
    'author_email': 'moritz.makowski@tum.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tum-esm/em27-metadata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
